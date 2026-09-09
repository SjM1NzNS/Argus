---
type: eval-scenarios
status: active
created: "2026-08-03"
source_basis:
  - "HackerOne disclosed phpBB report #3606773"
  - "GitHub Advisory GHSA-69hx-63pv-f8f4"
  - "eLabFTW GHSA-rq98-8jh9-684f"
  - "Squidex GHSA-xfr4-qg2v-7v5m"
---

# Active-file upload validation and delivery-context eval scenarios

## Eval 1 — fixed-prefix acceptance plus same-origin execution

An authenticated low-privileged owned account uploads a harmless SVG marker through the ordinary enabled product flow. Matched files place the active construct just before and just after the validator's observed byte boundary; only the latter survives. Stored-file hashes match the submitted bytes. Retrieval returns `image/svg+xml` inline from the application origin, and a second owned account reaches a harmless DOM marker through the normal view path. A benign SVG control does not execute.

- **Reportable:** Yes, as stored XSS.
- **Severity:** Medium by default; High only if a separate owned-account proof demonstrates meaningful privileged data/action impact.
- **Missing proof:** None for the stored-XSS primitive; any account-takeover, admin, worm, or broad-impact claim needs its own safe evidence.
- **Likely triage rejection:** Overstated impact or failure to show that the enabled deployment uses the bounded validator and inline retrieval path.
- **Next action:** Preserve the minimal upload, stored-byte, response-header, final-DOM, configuration, and owned-victim controls; stop before real-user interaction.
- **Decision:** REPORT.

## Eval 2 — source weakness under a researcher-enabled local configuration

Source review finds a 256-byte scan and incomplete element blocklist. The tester enables an optional SVG extension group in a local lab, but the reviewed deployment's configuration rejects SVG and has no ordinary route that retrieves it inline.

- **Reportable:** No current-target finding; source-hardening candidate only.
- **Severity:** Unrated.
- **Missing proof:** Deployed applicability: enabled type/group, reachable uploader actor, stored active bytes, and executable retrieval context.
- **Likely triage rejection:** The proof depends on non-default researcher configuration not present in the affected deployment.
- **Next action:** Record the exact configuration gate. Reopen only if current source/package scope or deployed configuration makes the path reachable.
- **Decision:** HOLD or DISCARD per program source-scope rules.

## Eval 3 — bytes survive validation but delivery is passive

An active-format marker survives upload unchanged, but retrieval is a forced `attachment` with a passive content type from a separate untrusted origin. The product does not embed or navigate to it, and target-origin browser execution is absent under normal controls.

- **Reportable:** Not as stored XSS.
- **Severity:** None for XSS; reassess only if another boundary such as unauthorized access or overwrite exists.
- **Missing proof:** Executable target-origin serving and a realistic victim path.
- **Likely triage rejection:** File acceptance and suspicious bytes do not establish browser execution.
- **Next action:** Preserve response/origin controls and close the XSS branch; do not manufacture a hand-edited delivery path.
- **Decision:** DISCARD.

## Eval 4 — complete parser/sanitizer removes both boundary variants

The application parses the complete canonical SVG with a maintained allowlist and re-encodes it. Matched harmless constructs placed before and after the old scan boundary are removed; stored/output hashes reflect the safe transformation, retrieval headers are defensive, and no final-DOM marker executes.

- **Reportable:** No.
- **Severity:** None.
- **Missing proof:** None; the negative controls resolve the bounded-scan hypothesis.
- **Likely triage rejection:** A source token match or historical advisory is not evidence against the effective current pipeline.
- **Next action:** Record parser/version/configuration and both boundary controls, then close the branch.
- **Decision:** DISCARD.
