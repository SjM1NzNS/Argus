# Private Review Package and Post-Package Verification

Use this protocol when an Argus finding is technically complete but must remain private pending adversarial or user review.

## Core invariant

The final archive is a frozen review artifact. Any correction to a packaged report, source pin, evidence file, verifier, manifest, or package README invalidates the old archive and requires:

1. rebuild the archive;
2. regenerate its sidecar checksum and package-verification record;
3. rerun the prescribed verifiers **after that rebuild**; and
4. update external ledgers and post-package verification records with the final hash.

Do not call a package final when later edits changed any input.

A late delegated/independent review is also an input when it changes evidence, severity, impact boundaries, prior-art treatment, or required source snapshots. Verify the review's claimed file writes and source ranges against the shared canonical state; if accepted, mark the previous archive/hash explicitly superseded, freeze the reconciled verdict, and rebuild from scratch. Never deliver an already-built package and then silently accept conclusion-changing asynchronous findings.

## Pre-package gates

### 1. Verify provenance independently

For every moving repository/action/generated executable:

- compare the saved API/head capture with the local checkout's full identity (for Git, `git rev-parse HEAD`);
- use the exact full identifier in source pins, report links, manifests, and verifier expectations;
- reject agreement based only on a short prefix;
- search canonical inputs for any superseded full identifier before packaging.

A handoff or Markdown pin is a pointer, not independent proof. If it disagrees with canonical captures or the checkout, correct it and document the audit correction.

### 1a. Rebuild every derived evidence file from raw inputs

Before packaging, inventory the raw artifacts that actually exist. Regenerate lifecycle summaries, counts, ordering tables, and citation ledgers with deterministic local scripts rather than manually transcribing IDs, SHAs, timestamps, or status counts.

Require each derived artifact to state:

- exact raw input filenames;
- generation command and schema/status;
- capture-time wording such as `observed head`, not permanently `current head`;
- missing raw responses/headers;
- provenance limits, including whether automation versus a human applied a marker;
- explicit non-claims.

Cross-check every report citation against the regenerated artifact, then search canonical and package trees for superseded exact values. If a derived file cites a raw artifact that is absent, either capture it safely before freeze or remove/narrow the claim—never leave a fictional inventory entry.

### 2. Validate exact test selectors

Do not trust checkpointed unittest/class/method names blindly. Before freezing the report:

- inspect the pinned test source or enumerate tests;
- run the exact selectors once;
- distinguish a selector/invocation mistake from a product-test failure;
- record the corrected canonical command in the report and checkpoint.

Only the final exact command and its successful result count as verification. Transient local command-entry or output-capture mistakes do not change the technical disposition, but the corrected invocation must be rerun cleanly.

### 3. Freeze claim boundaries

The report and package README must state:

- exact actor and prerequisites;
- maximum supported impact;
- explicit non-claims and trust-domain boundaries;
- local/public controls versus live proof;
- submission/live-action state.

Require the literal final disposition expected by the mission (for example, `REPORT CANDIDATE / GO`) rather than relying on an approximate synonym.

## Package contents

Prefer a compact, self-contained package containing:

- final report;
- qualification/disposition note when useful;
- source pins and focused source snapshots;
- canonical positive/negative control outputs;
- raw public evidence needed for ordering/provenance;
- verifier scripts and exact commands;
- external context clearly marked as non-proof;
- `MANIFEST.json` with per-file size and SHA-256;
- internal `SHA256SUMS` covering every packaged file except itself;
- README with review purpose, boundaries, and non-submission warning.

Avoid unrelated target history, credentials, private request bodies, or bulk source trees.

## Avoid checksum self-reference

Never place the archive's own final SHA-256 inside a file that is included in that archive. Doing so creates an impossible self-reference and guarantees a stale value after rebuild.

Keep these outside the archive:

- `<archive>.sha256`;
- package-verification JSON containing the archive hash;
- post-package rerun JSON;
- final-state verification JSON;
- target/global ledgers that record the final archive hash.

A packaged qualification note may point to those sidecars without embedding their value.

## Package verification gates

Before the post-package rerun, verify:

- all expected files exist and no symlinks escape the package root;
- internal `SHA256SUMS` verifies;
- archive CRC/test passes;
- exactly one expected archive root exists;
- extraction reproduces the package file set and hashes;
- a secret-shaped-content scan passes;
- archive size, file count, SHA-256, and generation time are recorded in machine-readable JSON.

Treat secret scanning as a gate, not proof that no sensitive data exists. Curate the inputs first.

## Post-package rerun

After the **final** package build:

1. run each local verifier;
2. run the exact named upstream positive and negative controls;
3. preserve canonical outputs outside the archive;
4. compare each output SHA-256 with its packaged copy when deterministic;
5. write a post-package JSON containing command, workdir, status, output path, hashes, and any audit correction.

Before calling that build final, freeze every packaged disposition input—including the critical-review verdict, qualification text, package README, manifest wording, and packaged verifier scripts. If a packaged verifier is corrected during the rerun, rebuild before rerunning it again; otherwise the passing script and the packaged script are different artifacts.

Semantic verification must encode the expected shape explicitly. Do not use `all(mapping.values())` when a valid assertion is represented by `0`, an empty list, or another falsey sentinel; check required booleans and numeric/string sentinels separately. A command returning zero is necessary but not sufficient—also parse the saved JSON/test output and confirm the intended assertions.

If a transcript differs only in volatile elapsed time while all assertions and test counts match, record that bounded difference instead of overclaiming byte identity. Prefer normalized/deterministic output formats for future packages.

If a substantive output changes, investigate it. If the report/package must change, rebuild and repeat the post-package rerun.

## Ledger reconciliation

Preserve prior finding history. Append or clearly supersede rather than deleting older no-go/disposition records.

Update the mission qualification and target-level hypotheses, tested-items, hunt-log, checkpoint, and next-steps with:

- current disposition and exact boundary;
- report/package paths;
- final archive hash (only in files outside the archive);
- verifier outcomes;
- corrections to stale selectors or source pins;
- explicit approval gate and next action (`review only`, when applicable).

Make the mission checkpoint clearly say the original remaining work is completed so a future session does not restart it.

## Final-state verifier

Run one final local verifier that fails closed unless all of these hold:

- archive hash equals the sidecar and recorded expected value;
- archive and internal checksums pass;
- package and post-package JSON records report pass;
- local checkout identity equals canonical provenance;
- superseded source identifiers are absent from canonical report/pins;
- report contains the exact disposition, impact boundary, and non-claims;
- every required ledger contains the current finding and preserves the prior finding history;
- checkpoint/next-steps are waiting for review, not packaging;
- final upstream output reports the expected test count and `OK`/pass state.

Save the final-state result outside the archive. Then stop: do not submit, create a PR, change labels, or trigger live CI without explicit approval.

## Common pitfalls

1. **Trusting a handoff's full SHA or test name.** Independently verify before packaging.
2. **Packaging a file that names the archive hash.** Keep archive-hash records external.
3. **Correcting the report after packaging without rebuilding.** Any packaged-input change invalidates finality.
4. **Rerunning tests before the last rebuild.** The required order is final build, then rerun.
5. **Claiming all outputs match when a volatile transcript changed.** Compare hashes and describe the exact bounded difference.
6. **Overwriting prior no-go history.** Preserve it and explain why the new actor/control chain reopens the class.
7. **Letting invocation typos masquerade as technical failures.** Correct the selector/path and rerun cleanly; preserve meaningful audit corrections.
8. **Letting `tee` mask verifier failure.** Use `set -o pipefail` or capture the verifier exit code explicitly when saving stdout; a pretty JSON file is not proof the verifier returned zero.
9. **Assuming evidence JSON key names.** Read the generated schema before writing the final verifier. Assert the actual nested keys and expected sentinels; a verifier crash or false negative caused by invented field names is a verifier defect, not finding evidence.
10. **Freezing before reviewer reconciliation.** A late accepted correction to evidence, impact, title, disposition, README, source map, or verifier requires a new package and hash even if the prior ZIP passed every integrity check.
