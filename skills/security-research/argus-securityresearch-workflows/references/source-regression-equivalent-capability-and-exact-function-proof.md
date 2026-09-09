# Source Regression Proof and Equivalent-Capability Gate

Use this workflow for source-first security reviews where a current patch appears to weaken an authorization, trust-routing, sandbox, CI, or worker-isolation invariant.

## Why this gate matters

A source regression can be technically real, current, and reproducible while still adding no attacker capability. Before calling it reportable, compare the suspected bypass with every supported path available to the **same actor**. If an intended configuration, UI field, static agreement, ordinary role action, or documented workflow reaches the same sink with the same consequence, the regression may be hardening-only.

Do not let the effort spent proving the regression bias the reportability decision.

## Workflow

### 1. Pin both sides of the change

Record:

- repository and exact current commit;
- parent or last-known-safe commit;
- current remote default-branch commit at disposition time;
- clean-tree status;
- public PR/review discussion and timestamps.

Recheck the remote branch before final disposition when the change is fresh. Keep historical and current claims separate.

### 2. Separate request claims from authoritative state

Map each decision independently:

| Stage | Questions |
|---|---|
| Ingress | Which request fields, UI values, query parameters, or body properties can the actor control? |
| Authorization | Which role or object-access check admits the actor? Is it distinct from administrator/trusted-user status? |
| Safety gate | Does the gate use request metadata, an authoritative datastore entity, or precedence such as `request_value or model_value`? |
| Persistence | What trust/owner/project flags are actually stored? |
| Routing | Does queue, platform, tenant, project, or build selection reload authoritative state or reuse request state? |
| Runtime | Is there a later fail-closed check, warning-only check, assertion, or no check? |
| Sink | What exact parser, target, process, storage object, credential, or publication action is reached? |

An authority conflict is strongest when the safety gate trusts request metadata but downstream routing reloads a different authoritative object.

### 3. Write the security invariant first

Before building a positive bug demonstration, write the expected secure property as a failing test. Example shape:

```text
A non-Linux authoritative Job must be rejected even when the request claims Linux.
```

Include at least:

- negative control with no override;
- negative control with an obviously unsafe override;
- positive allowed control;
- suspected mismatch case.

Preserve the original RED output. If the upstream test environment is dependency-heavy, execute the **exact current function body** via AST with narrow fakes only at datastore/environment boundaries. Do not rewrite the function logic in the harness.

A stable evidence harness may mark the known invariant failure as expected only after the original failing output is preserved. Keep production source untouched.

### 4. Prove downstream continuation separately

Do not infer sink reach from the first gate. Execute or inspect the exact downstream components independently:

- authoritative queue/platform selection;
- persisted trust state;
- task classification;
- warning-versus-fatal runtime handling;
- call order from safety check to target/parser/process sink.

Machine-readable output should include the control matrix, queue/sink selected, stored trust state, warnings, and whether the safety function returned normally.

### 5. Prove the historical differential

Compare the exact parent and current conditions. A refactor can change semantics even when described as consolidation. Record whether the parent independently checked authoritative state and whether public review discussed the conflict.

This establishes regression provenance, not reportability by itself.

### 6. Run the same-actor equivalent-capability counterfactual

Before drafting or preserving a report candidate, enumerate every supported path the same actor can use:

- visible UI options and hidden/advanced fields;
- agreements, acknowledgements, or trust phrases;
- normal role actions and documented configuration;
- alternate endpoint variants;
- supported ignore/filter/approval mechanisms;
- ordinary object-owner or project-maintainer capabilities;
- existing paths to the same worker, queue, publication, or protected outcome.

Build an explicit matrix:

| Path | Actor prerequisite | Gate skipped or satisfied | Final sink | Incremental consequence |
|---|---|---|---|---|
| Suspected bypass | exact role | mechanism | sink | claimed delta |
| Intended path | same exact role? | supported mechanism | same/different sink | actual delta |

Kill or downgrade the report when all are true:

1. the same actor can invoke the intended path;
2. it reaches the same sink or protected outcome;
3. the suspected bypass changes only an acknowledgement, UI sequence, cosmetic state, or unenforced metadata;
4. no downstream consumer relies on the bypassed distinction;
5. no stronger data, credential, tenant, worker, or publication capability is gained.

A static statement such as “this input is safe” can be a weak design, but bypassing it is not automatically incremental impact if the same uploader is explicitly permitted to make that assertion and reaches the same worker either way.

### 7. Keep conditional exploitation from masking equivalence

A downstream target exploit, parser bug, or command primitive does not create incremental impact when both the bypass and intended path reach the same target under the same actor authority.

Separate:

- proven routing/safety regression;
- proven direct sink primitive;
- conditional target compromise;
- capability delta over the intended path.

The last item decides reportability.

### 8. Close cleanly when the gate fails

When a candidate is killed late:

1. write a canonical final disposition explaining the equivalent path;
2. add a prominent `ARCHIVED — DO NOT SUBMIT` banner to any report draft;
3. preserve the exact regression test as hardening evidence;
4. replace every stale `report candidate`, `owner review`, or `submission pending` marker in tested-items, hypotheses, hunt log, next steps, and checkpoint;
5. regenerate checksums/manifests after report edits;
6. verify no stale current-state marker remains;
7. state precise reopen conditions.

Useful final labels:

```text
CONFIRMED HARDENING REGRESSION / CLOSED NOT REPORTABLE / NO INCREMENTAL CAPABILITY
```

## Reopen conditions

Reopen only if evidence shows at least one of:

- the actor exploiting the mismatch cannot use the intended alternate path;
- production applies an authorization-backed trust decision absent from public source;
- the mismatch reaches a stronger queue, tenant, project, credential, storage object, or runtime;
- a downstream consumer makes the bypassed distinction security-relevant;
- maintainers state that the apparent intended path is not authorized for this role.

## Pitfalls

- **Current-HEAD regression is not synonymous with bounty impact.** Freshness and novelty do not replace the capability-delta test.
- **Do not postpone equivalence review until after report drafting.** Run it immediately after sink reach is proven.
- **Do not treat a warning-only runtime guard as unique impact** when a supported path reaches the same warning and sink.
- **Do not upgrade conditional target exploitation into proven host compromise.** Preserve the precondition explicitly.
- **Do not leave stale candidate state after a downgrade.** A technically accurate archived draft can still mislead future sessions unless it is prominently blocked and all ledgers are reconciled.
- **Do not reimplement the vulnerable function in the verifier.** Compile the exact pinned body and fake only its external dependencies.

## Minimal artifact set

```text
source-map.md
hypotheses.md
scripts/test_security_invariant.py
scripts/verify_regression.py
evidence/red-security-invariant.txt
evidence/regression-matrix.json
reports/<id>-adversarial-review.md
reports/<id>-final-disposition.md
```

The report draft is optional and should exist only after the equivalent-capability gate passes.
