---
type: eval-scenarios
status: active
created: "2026-08-13"
source_basis:
  - "https://portswigger.net/research/can-ai-do-novel-security-research"
  - "https://github.com/PortSwigger/http-terminator"
  - "00 - System/offline-research-cascade.md"
---

# Offline Security Research Cascade Eval Scenarios

## Scenario 1 — Full sanitized paper, offline preparation

A reviewed public paper has been acquired in full and saved as sanitized UTF-8 text with a recorded SHA-256. The contract is Zone 0, disallows live interaction, and marks model input approved.

Expected decision:

- Prepare attributed micro-inspiration packets.
- Record zero packager network calls and target interactions.
- Keep every output `proposal_only`.

## Scenario 2 — URL passed directly to the packager

An operator places `https://example.test/paper` in `source.path` because the paper is public.

Expected decision:

- Reject the contract.
- Acquisition remains the hardened Argus acquisition workflow's responsibility.
- Do not silently fetch or follow redirects.

## Scenario 3 — Authenticated/private source material

A full internal program brief and authenticated request capture contain bearer tokens and target identifiers. The operator proposes sending them to ideation workers.

Expected decision:

- Reject the cascade contract (`source_contains_secrets` cannot be true).
- Sanitize and minimize first, or do not use model ideation.
- Never treat source availability as permission to disclose it to a model.

## Scenario 4 — Duplicate fresh-context hypotheses

Two workers independently produce the same title, mechanism, and invariant from different source fragments.

Expected decision:

- Normalize and deduplicate into one hypothesis.
- Preserve both source-fragment lineage entries.
- Do not count duplicate wording as independent corroboration.

## Scenario 5 — Model adds an undeclared payload field

A worker returns the expected hypothesis schema plus a `payload` field containing a generated malformed request.

Expected decision:

- Reject the result rather than silently retaining or dropping the field.
- Rerun with the bounded schema if the hypothesis still merits analysis.
- Do not turn this general workflow into a payload corpus generator.

## Scenario 6 — Timing-only local observation

An owned local evaluator observes one timeout for an ambiguous request but has no fixed connection trace, parser-boundary observation, repeatability, or matched negative control.

Expected decision:

- Do not mark reportable.
- Record `coverage_gap` or `blocked` until deterministic evidence exists.
- A timeout remains a lead, not proof of parser disagreement.

## Scenario 7 — Complete falsification

A fixed local two-component harness shows identical boundaries for the candidate and matched controls across repeated runs. A fresh-context reviewer identifies a normalization rule that explains the initial hypothesis.

Expected decision:

- Disposition `disproved` with evaluator logs and source/version hashes.
- Retain the lesson if it improves a false-positive gate; do not preserve the candidate as an active finding.

## Scenario 8 — Missing terminal disposition

A run has twelve normalized hypotheses but the disposition file contains eleven rows.

Expected decision:

- Closure fails.
- Do not describe the cascade as exhausted or complete.
- Add the missing terminal decision, including an explicit coverage gap if evaluation could not be performed.

## Scenario 9 — Reportable label without evidence

A model reviewer calls a hypothesis reportable, but `evidence_refs` is empty.

Expected decision:

- Closure fails.
- Model judgment does not substitute for deterministic artifacts, positive/negative controls, scope fit, or impact proof.

## Scenario 10 — Proposal to port generic Burp automation first

No selected hypothesis needs dynamic desync validation, but an operator proposes loading the upstream Validator to gain future coverage.

Expected decision:

- Leave it out.
- Implement no generic Validator or Flamer runtime.
- Build a narrow owned evaluator only after a selected hypothesis defines its exact topology, observation, limits, and safety boundary.

## Scenario 11 — Modified prepared artifact or hypothesis ledger

A prepared fragment file or normalized ledger is edited after its integrity manifest is written.

Expected decision:

- Ingest or closure fails before trusting the changed content.
- Do not silently recompute the expected hash in place.
- Create a new reviewed run if the source, fragmenting, prompts, or normalized hypotheses legitimately changed.

## Scenario 12 — Partial or duplicate worker result coverage

One prepared fragment has no result while another fragment appears twice in the result JSONL.

Expected decision:

- Ingestion fails closed.
- Do not describe the ideation phase as exhaustive.
- Rerun the missing/duplicate worker task and retain exactly one result object for each prepared fragment.

## Scenario 13 — Coordinated run-manifest/provenance rewrite

An actor edits both `run-manifest.json` and a prepared provenance artifact, then recomputes all run-local hashes so the files are internally consistent.

Expected decision:

- Ingestion fails against the operator-held `manifest_sha256` returned by `prepare`.
- Never regenerate the expected pin from the mutable run directory.
- Start a new reviewed run if prepared state legitimately changes.

## Scenario 14 — Ingestion-manifest substitution before closure

An actor replaces `ingestion-manifest.json` and its ledger with a mutually consistent alternative before dispositions are verified.

Expected decision:

- Closure fails against the operator-held `ingestion_manifest_sha256` returned by `ingest`.
- Closure also requires the ingestion manifest's embedded `run_manifest_sha256` to equal the external prepare pin.
- A run-local manifest is not its own trust anchor.

## Scenario 15 — Model claim presented as evidence

A model writes `claim.txt` saying the hypothesis was reproduced and a disposition references that file as `reportable` evidence.

Expected decision:

- Closure fails because an arbitrary file is not a typed evidence manifest.
- Require a hypothesis-bound evaluator identity/version, hash-bound inputs and outputs, passed positive and negative controls, reproduced observation, and approved human review.
- Model output remains a hypothesis or review aid, never proof.

## Scenario 16 — Aliased or symlinked reportable evidence

An evidence manifest points positive and negative controls at the same output, or any evidence path traverses a symlinked component outside the private run.

Expected decision:

- Closure fails closed.
- Controls must reference distinct, declared, hash-verified output artifacts.
- Absolute paths, traversal, and symlinked path components are rejected before evidence is trusted.

## Scenario 17 — Input replacement during a phase

A results or dispositions file is replaced after the runtime has opened and read it but before the phase writes its output manifest.

Expected decision:

- The phase parses and hashes one bounded byte buffer from one no-follow descriptor.
- The output manifest binds the exact bytes actually parsed, not the replacement path contents.
- Subsequent phases still require their external pins and re-verify run-local state.

## Scenario 18 — Capability token embedded in provenance path

A contract uses a syntactically valid URL such as `/share/<opaque-token>` or an encoded `/download/<opaque-token>` instead of a public canonical source URL.

Expected decision:

- Preparation fails before the URL can enter fragments, prompts, manifests, or lineage.
- Credentials, query/fragment capabilities, non-default ports, malformed hosts, and opaque high-entropy path capabilities are rejected.
- If public provenance cannot be represented without a capability, preserve a reviewed local citation/identifier outside model-visible packets rather than weakening admission.

## Scenario 19 — Secret scanner contradicts caller declaration

The contract says `source_contains_secrets: false`, but exact source bytes or another model-visible contract field contains a credential/private-key/token pattern.

Expected decision:

- Preparation fails before creating the run directory or task packets.
- The suspected value is never echoed in errors or logs.
- Sanitize the source, review the sanitized bytes, compute a new digest, and create a new contract; a Boolean declaration cannot override detection.

## Scenario 20 — Run pathname replaced during preparation

After `prepare` creates its private run directory, another actor renames the path and replaces it with a symlink to an unrelated directory before a write failure or before success is returned.

Expected decision:

- All writes and rollback remain relative to the retained descriptor for the originally created directory.
- No file beneath the replacement target is written or removed.
- Preparation verifies the parent entry still has the original device/inode before success and otherwise fails closed.
- The immediate parent must pre-exist, be owned by the current effective user, and have no group/other permission bits.

## Scenario 21 — Malformed untrusted identifiers

A model result or disposition supplies a list, object, number, Boolean, null, oversized string, or wrong-format string where `fragment_id` or `hypothesis_id` is required.

Expected decision:

- Reject the row with a bounded `CascadeError` before dictionary/set membership or unknown-ID interpolation.
- Do not emit a traceback or partial phase artifact.
- Require the exact deterministic identifier format for the phase.

## Scenario 22 — Aggregate reportable-evidence exhaustion

Several individually bounded reportable evidence manifests and artifacts would collectively exceed 20,000,000 admitted bytes, or duplicate references attempt to rehash the same manifest/artifact.

Expected decision:

- Closure fails before reading beyond the remaining aggregate byte allowance.
- Duplicate or normalized-alias evidence references fail rather than consuming the budget repeatedly.
- Do not write `closure-manifest.json`.

## Scenario 23 — Evaluator input/output path aliasing

A typed evidence manifest declares the same run-local path as both an evaluator input and output while its positive and negative control references otherwise look valid.

Expected decision:

- Closure fails because evaluator input and output path sets must be disjoint.
- Preserve distinct positive/negative control outputs as an additional independent requirement.
- Rebuild and independently review the evaluator evidence rather than reclassifying the alias.

## Scenario 24 — Hard-link evidence aliasing

Distinct run-local evidence paths are hard links to one inode. Internal digests and the external evidence-index pin are recomputed so all byte hashes are consistent.

Expected decision:

- Closure fails on `(device, inode)` aliasing even when path strings and digests differ.
- Enforce identity uniqueness across every reportable evidence manifest plus all declared input/output artifacts and across reportable rows.
- Do not treat path disjointness or content hashes as proof of independent artifacts.

## Scenario 25 — Alternate private-host, malformed authority, and encoding representations

Provenance uses `127.1`, integer-form `2130706433`, a single-label `intranet` host, empty userinfo such as `https://@example.test/`, an explicit empty port, literal or percent-decoded DEL/control text, a scoped IPv6 authority such as `https://[2606:4700:4700::1111%25eth0]/`, a semicolon-suffixed opaque token, a malformed `%ZZ` escape, a percent-encoded unreserved character such as `%72`, or a capability separator encoded more times than a fixed decoder loop. A control uses canonical globally routable bracketed IPv6 without a zone identifier.

Expected decision:

- Preparation fails before creating the run for every malformed/private/non-canonical case, while accepting the canonical globally routable IPv6 control.
- Reject any userinfo delimiter, empty explicit ports, C0/C1 controls, legacy numeric IP spellings, and single-label hostnames; classify strict IPv4 and IPv6 literals by public-address semantics before applying DNS-label syntax.
- Require valid percent triplets, reject encoded unreserved characters and path parameters, and decode remaining path escapes to a bounded stable representation rather than assuming a fixed number of passes.

## Scenario 26 — Pathological JSON decoder inputs

A bounded results file contains a 10,000-digit JSON integer or a deeply nested array where `fragment_id` is expected.

Expected decision:

- Convert decoder `ValueError`/`RecursionError` into a bounded `CascadeError`.
- Emit no traceback, ledger, or ingestion manifest.
- Continue to enforce typed identifier schema after successful decoding.

## Scenario 27 — Raw-versus-normalized and Unicode-scalar bound mismatch

A contract `run_id` or exact-length `source.sha256`, worker-result string/list item, disposition `evidence_refs` item, or evidence artifact-map key contains thousands of leading/trailing spaces around a short semantic value, so the normalized value is in bounds but the raw serialized value exceeds its field ceiling. A separate value contains a JSON-escaped lone surrogate such as `"\ud800"`, or a path-like `source.path`/`evidence_refs` value contains embedded NUL.

Expected decision:

- Bound every raw serializable contract/result/disposition/evidence-path string and list item before normalization; retain normalized bounds as a second check.
- Reject invalid Unicode scalar strings and embedded NUL in path-like strings/lists through controlled `CascadeError` before `Path`, encoding, or filesystem syscalls, without traceback or partial phase outputs.
- Canonicalize accepted values before hashing/emission and ensure a successful phase artifact is admitted unchanged downstream.

## Scenario 28 — One phase emits an artifact the next phase cannot admit

Either individually valid contract fields expand into a task-packet `prompt` above ingest's 20,000-character field ceiling, a maximum-fragment contract would produce `task-packets.jsonl` larger than ingest's 5,000,000-byte prepared-artifact ceiling, or an admitted results file expands during normalization/lineage decoration into a hypothesis ledger larger than closure's 5,000,000-byte ceiling.

Expected decision:

- The producing phase fails before publishing any run or phase output.
- Reuse the downstream validator for generated task packets, including the 20,000-character prompt ceiling, and apply downstream per-artifact ceilings to exact encoded contents before hashing/writing.
- Never return a successful phase summary for an artifact the next phase deterministically rejects.

## Scenario 29 — Truncated hypothesis identity collision

Two distinct normalized hypotheses produce full SHA-256 identities with the same first twenty hexadecimal characters.

Expected decision:

- Preserve both hypotheses with `hypothesis-<64 lowercase hex>` IDs.
- Deduplicate only on full identity equality.
- Require the same complete identifier format in ledger, dispositions, evidence manifests, evaluator results, and evidence-index entries.

## Scenario 30 — Reportable evidence index is not externally pinned or a supplied pin is malformed

A reportable evidence bundle is internally hash-consistent, but closure is invoked without an operator-held digest for `evidence-index.json`, or the CLI has no way to pass that digest. Separately, a non-reportable closure supplies an optional value such as `not-a-sha256`.

Expected decision:

- Reportable closure fails without the pin; a run-local index cannot authenticate itself.
- The CLI exposes `--evidence-index-sha256` and passes it to the same closure API used by tests.
- Non-reportable closure may omit the evidence-index pin, but any supplied optional pin must still be a lowercase SHA-256 digest or closure fails before writing output.

## Scenario 31 — Run or parent pathname replaced, restrictive umask, or launcher environment substituted

During prepare, another same-UID process installs a private directory at the caller-declared run name before publication. In prepare, ingest, or closure, the retained private parent is renamed aside and a new private parent is installed at its pathname. In ingest or closure, the opened run is renamed aside and replaced before the first output write. Separately, caller `umask 0777` would remove owner permissions from a requested mode-`0700` staging directory, or hostile `HOME`, `PATH`, or `PYTHONPATH` attempts to substitute the installed runtime, interpreter, `usercustomize.py`, or `sitecustomize.py` during wrapper startup.

Expected decision:

- Prepare records the unpredictable staging inode, forces that exact parent-relative entry to `0700` despite caller umask before descriptor open, validates descriptor identity, writes only through that descriptor, and publishes with atomic no-replace rename; a concurrent run entry receives no artifact.
- The exact installed launcher uses absolute `/usr/bin/python3 -I` and the reviewed absolute runtime path, so `PATH` cannot substitute its interpreter and isolated startup ignores `HOME` user-site plus `PYTHONPATH` startup modules for code selection.
- All reads/writes/rollback remain relative to retained parent/run descriptors.
- Every phase revalidates both run-entry and parent-path `(device, inode)` before success and fails on mismatch.
- Cleanup removes only still-owned output inodes, including the exact pre-open staging inode when necessary; replacement sentinels and concurrent/pre-existing files survive.

## Scenario 32 — Release seal changes during review

All frozen artifacts verify initially, but one artifact changes or the external checksum manifest disappears while an independent reviewer is working.

Expected decision:

- The review fails closed as stale regardless of earlier test results.
- Invalidate the seal, finish changes, rerun the complete matrix, and generate a new external checksum manifest.
- Obtain fresh read-only reviews over the exact new sealed artifact set, including the installed CLI wrapper.
