# Offline cascade trust, schema, rollback, and identity hardening

Use this reference when implementing or auditing a multi-phase offline research pipeline whose prepared inputs, model results, evidence, and terminal dispositions cross trust boundaries.

## Core invariants

1. **External authentication of reportable evidence**
   - A reportable disposition must not authenticate its own evidence merely by naming or hashing files inside the same bundle.
   - Require an operator-supplied SHA-256 pin for an evidence index outside the model-produced disposition.
   - The pinned index should bind the run manifest, ingestion manifest, hypothesis ID, evidence manifest, evaluator result, and independent-review state.
   - Validate positive and negative controls from the pinned evaluator result, not from duplicate claims in an evidence manifest.
   - Require distinct control artifact paths and distinct artifact bytes; reject input/output overlap and aliases.

2. **Descriptor-stable, inode-owned rollback**
   - Open the run directory once and retain its descriptor and `(st_dev, st_ino)` identity through the phase.
   - Record each successfully created artifact as `(name, st_dev, st_ino)` immediately after creation and before returning to wrappers/callers.
   - On failure, unlink only when a fresh `stat(..., follow_symlinks=False)` still matches the recorded identity.
   - Never clean up a fixed list of expected names: a concurrent process may have inserted a same-name file.
   - If an exception can occur after a successful write but before its return value reaches the caller, pass a mutable ownership ledger into the write helper and register ownership internally before return.
   - Remove the run directory only when its original identity still matches and it is empty. Do not follow a replacement path.

3. **Recursive schema admission under fresh pins**
   - Exact top-level key checks are insufficient. Validate every nested field and every consumed value.
   - Reject Python boolean values where integers are required (`type(value) is int`, not `isinstance(value, int)`).
   - Validate timezone-aware ISO-8601 timestamps, bounded non-empty strings/lists, canonical IDs, lowercase SHA-256 values, allowed enums, and authorization booleans.
   - Parse and validate all hashed JSON/JSONL artifacts; a digest proves byte identity, not semantic validity.
   - Cross-bind run IDs, source provenance, fragment counts, packet coverage, result counts, ledger counts, and artifact digest maps.
   - Adversarial tests should modify exact bytes and deliberately recompute all applicable pins so rejection proves semantic validation rather than stale-hash detection.

4. **Collision-safe persisted identities**
   - Deduplicating by a full digest while persisting only a truncated prefix creates downstream aliasing.
   - Persist the full SHA-256 in hypothesis IDs when those IDs are used as map keys or trust bindings.
   - Apply the same format validator across ledgers, evidence indexes, dispositions, and closure manifests.
   - Add a forced-prefix regression: inject two distinct full digests sharing the old truncated prefix and require both records to remain independently addressable.

## TDD regression patterns

### Concurrent same-name rollback collision

Arrange a write wrapper that, before a later exclusive create, inserts a same-name sentinel through the retained run descriptor. Force the exclusive create to fail. Assert:

- the invocation's earlier artifact is removed;
- the concurrent sentinel survives unchanged;
- the run directory survives because it remains non-empty;
- no cleanup follows a renamed/replaced run path.

### Freshly re-pinned malformed artifact

1. Prepare a valid run.
2. Mutate one nested field in `run-manifest.json`, `fragments.jsonl`, `task-packets.jsonl`, or `ingestion-manifest.json`.
3. Recompute the artifact digest and every enclosing manifest/operator pin needed to make the altered bytes authentic.
4. Submit otherwise valid downstream input.
5. Require a controlled schema or cross-binding rejection.

This distinguishes recursive admission from accidental rejection at an earlier checksum gate.

### Shared legacy-prefix identity

Extract identity computation into a narrow helper. In a test, replace it with two 64-hex identities sharing the same first N hex characters used by the legacy persisted ID. Assert both full IDs are written, counted, and accepted by downstream validators.

## Verification sequence

1. Run narrow red regressions for each discovered blocker.
2. Implement the smallest invariant-preserving fix.
3. Run related race and valid-path tests together.
4. Run the complete focused module.
5. Run static checks and every production execution lane (static, browser, installed CLI) rather than treating unit tests as release proof.
6. Reconcile operator docs, schemas, examples, evals, and identifier formats.
7. Freeze the exact complete artifact set, verify its checksum seal, then obtain independent read-only reviews over that frozen set.

Do not claim release readiness after only the focused module passes; distinguish implementation-green from full E2E-verified and sealed.