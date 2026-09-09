# Cryptographic Verifier Duplicate-Key and Policy-Composition Review

Use this reference when a verifier accepts collections of signed claims, measurements, certificate entries, PCRs, digests, identities, or authorization records. The class-level risk is not necessarily signature forgery: collection normalization can verify one value while downstream code attributes that result to another value sharing the same logical key.

## Core ambiguity pattern

Look for this sequence:

1. Untrusted input supplies a list of records with a logical key such as `(index, algorithm)`, `(issuer, serial)`, `(name, type)`, or `(subject, scope)`.
2. Verification collapses the list into a map keyed by only part of the record.
3. Duplicate handling is implicit: first-wins, last-wins, or any-match.
4. A signature, MAC, quote, Merkle proof, replay, or policy check succeeds using one duplicate.
5. A later loop marks, returns, or authorizes every record sharing the partial key without rechecking the exact value.
6. A downstream consumer applies a different duplicate rule, such as first-match-and-delete, and trusts the verifier's per-entry status.

The security invariant must include the exact verified tuple, not merely the partial key:

```text
logical identity + algorithm/domain separator + exact value/digest
```

## Source-first review procedure

### 1. Recover the intended uniqueness domain

- Read public API comments and data-model documentation.
- Determine which duplicates are legitimate. Example: the same numeric measurement index may be valid across different hash banks, while conflicting values for the same `(index, hash algorithm)` are ambiguous.
- Do not recommend rejecting all repeated indices when the protocol permits multi-algorithm records.

### 2. Trace normalization and marking separately

Search for:

- `map[key] = value` inside loops;
- set membership keyed by only an index/name;
- `any`, `first`, or `last` match behavior;
- per-entry booleans such as `verified`, `trusted`, `covered`, or `authorized`;
- post-verification loops that set those flags using only the partial key;
- stale verification flags that are not cleared before a later failed run.

Write the chain as:

```text
untrusted ordered list
  -> normalization rule
  -> exact value used by cryptographic check
  -> records marked verified
  -> downstream policy selection rule
  -> security decision
```

### 3. Use a three-control matrix

Prefer the project's in-process simulator or owned deterministic fixture:

| Case | Input | Expected purpose |
|---|---|---|
| Clean positive | genuine records only | Proves the fixture and signature path work |
| Forged-only negative | replace the genuine value with an attacker-chosen value | Proves cryptography rejects the forged value by itself |
| Duplicate candidate | forged/policy-approved value plus genuine/signed value with the same logical key | Proves duplicate handling bridges policy and verification |

Test both orderings. A first-wins/last-wins difference is causal evidence, not noise.

For a per-entry contract, assert that the forged record itself is not marked verified. A failing security-invariant regression test is stronger than merely observing an overall success return.

Keep the proof behind an opt-in build tag or equivalent local-test gate when adding it to a pinned source checkout, then run:

1. the opt-in candidate test; and
2. the untouched upstream suite without the local tag.

Hash the test and both outputs after the final edit.

### 4. Prove policy composition without live testing

Search public source consumers for the verifier method and per-entry trust accessor. High-signal downstream patterns include:

- policy validation before cryptographic verification;
- first-match-and-delete maps;
- order-preserving conversion into the verifier's record type;
- loops requiring every returned record to carry a verified bit;
- authorization, artifact admission, secret release, or identity issuance after those checks.

Pin the consumer commit and dependency version. Verify the defect exists in the exact released dependency tag used by the consumer. Source-only composition is impact evidence; it is not proof that a live deployment is reachable or exploitable.

A useful differential is:

```text
policy consumer sees forged duplicate first
cryptographic verifier sees genuine duplicate last
both layers report success under different duplicate semantics
```

### 5. Run the prior-art gate at the class and exact-root levels

Search:

- repository issues and pull requests for duplicate records, same-key ambiguity, per-entry verification, and the exact normalization variable;
- security advisories and CVEs involving the same verifier method;
- history introducing duplicate support or multi-bank/multi-algorithm handling;
- forks or downstream patches that reject/canonicalize duplicates.

A prior change allowing duplicate *partial keys* for different algorithms does not automatically authorize conflicting duplicates with the same full key. Conversely, an open PR with the exact sink and fix is decisive duplicate/no-go even when the issue was independently reproduced.

Record whether prior art shares:

- the exact full-key ambiguity;
- the same per-value false verification state;
- the same downstream policy bridge; and
- the same remediation.

Do not submit until historical advisories touching the same method have an explicit root-cause differential.

## Remediation matrix

Preferred fixes:

1. Reject conflicting duplicates with the same full logical key before verification.
2. Continue allowing protocol-valid duplicates that differ in the required domain separator, such as hash algorithm.
3. Track the exact record/digest used by the cryptographic computation.
4. Mark only the exact record whose value was used and matched.
5. Clear per-entry verification state at the start of every verification attempt.
6. Apply the same duplicate semantics to replay/event-log/policy helpers.
7. Add tests for:
   - unique clean records;
   - valid same-partial-key/different-algorithm records;
   - identical full-key duplicates;
   - conflicting full-key duplicates in both orders;
   - stale state after a successful then failed verification;
   - representative downstream policy composition.

## Reporting boundaries

Lead with exact-value verification confusion or policy composition—not signature forgery—when the signature remains valid over the genuine duplicate.

Separate:

- proven library invariant failure;
- source-supported downstream decision impact;
- conditional deployment impact;
- tested live impact.

Useful non-claims:

- no cryptographic signature was forged;
- no hardware root or key was compromised;
- no live consumer was tested;
- no specific production service is claimed exploitable without deployment evidence.

Severity depends on the downstream decision: diagnostic ambiguity may be Low, while authentication, secret release, or trusted artifact admission can be High. Preserve that dependency rather than assigning severity from the primitive alone.
