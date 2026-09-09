# Artifact-write integrity and truncation gates

Use this whenever reports, ledgers, checkpoints, package manifests, or verifier inputs are created or patched through tools that may summarize long arguments/results.

## Failure mode

A UI or tool transcript may display placeholders such as:

```text
...[truncated]
[truncated]
```

These are presentation artifacts, not source content. If copied into a later write/patch payload—or if an already-shortened value is treated as complete—they can silently corrupt the durable artifact while the write itself reports success.

## Required workflow

1. Build edits from an original file read or a deliberately authored complete replacement, never from a summarized diff/result preview.
2. After every material write or patch, read back the changed section from the actual file.
3. Search the affected mission/package tree for literal truncation markers before final verification:

```regex
\.\.\.\[truncated\]|\[truncated\]
```

4. Treat any unexpected match as corruption. Replace it from authoritative source/context, then read back again.
5. Add explicit verifier assertions for high-value handoff/package files:

```python
assert "...[truncated]" not in text
assert "[truncated]" not in text
```

6. Re-run every dependent verifier after repair. A prior PASS does not cover artifacts modified afterward.

## Additional integrity checks

- Verify the expected section heading and terminal line exist after append-at-EOF operations.
- When replacing the final line of a file, confirm newline behavior by reading the tail.
- Preserve earlier finding IDs/statuses when updating shared ledgers; assert both the new and historical entries remain.
- For API evidence, save raw headers/body separately from the derived interpretation and verify the derived claim against both.
- Do not package until all writes are final, read-back verification passes, and no placeholder/TODO markers remain.

## Verifier design: filenames and semantics

A verifier can fail for its own bookkeeping errors even when the evidence is sound. Avoid turning descriptive aliases or prose formatting into false evidence failures.

1. Enumerate actual artifact filenames from the evidence directory or manifest; do not invent shortened aliases such as `rulesets.json` when the saved file is `repository-rulesets.json`.
2. Keep the control note's inventory synchronized with those exact names.
3. Parse structured artifacts and assert semantic fields (`protected is True`, required context/app/enforcement, event timestamps, head SHA) rather than exact JSON spacing or Markdown phrasing.
4. Reserve literal marker assertions for stable identifiers and verdict tokens. Prose markers such as a whole sentence are brittle and should not be the only proof of reconciliation.
5. Bind timestamps to the correct raw field (`created_at`, author date, committer date) and verify ordering from the saved objects rather than copied summaries.
6. Exclude derived notes/manifests from raw-evidence hashes only by an explicit, documented rule; then recompute and verify the expected count/digest after any raw-artifact change.
7. When a fail-fast assertion trips, diagnose the named invariant and inspect the authoritative artifact before rerunning. Never rerun an unchanged failing command as a substitute for diagnosis.

A useful final gate separates:

- raw-evidence integrity;
- semantic security assertions;
- report/ledger reconciliation;
- placeholder/credential scans.

This makes it clear whether a failure is in evidence, interpretation, or verifier bookkeeping.

## Reporting rule

Never describe a tool-reported successful write as a valid artifact until the file has been read back or a deterministic verifier has inspected it. Tool success proves the write operation occurred, not that the intended complete content was written.
