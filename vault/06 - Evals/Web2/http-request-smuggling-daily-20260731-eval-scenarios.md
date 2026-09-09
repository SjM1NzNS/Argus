---
type: eval-scenarios
status: active
created: "2026-07-31"
source_basis:
  - "YesWeHack HTTP request smuggling guide"
  - "PortSwigger HTTP desynchronization research"
---

# HTTP request smuggling / desynchronization eval scenarios

## Eval 1 — scanner timeout on shared production

A desync scanner reports H2.TE because one ambiguous request timed out. No backend logs, connection identity, owned second-message canary, or matched timing control exists.

- **Reportable:** No; candidate only.
- **Severity:** Unrated.
- **Missing proof:** A bound two-hop parser differential, reused-connection effect, and concrete impact.
- **Likely triage rejection:** Generic timeout/scanner evidence can be caused by edge rejection, translation, or backend latency.
- **Next action:** Stop broad probing; request an owner-coordinated staging/local reproduction or one explicitly approved non-poisoning discriminator.
- **Decision:** HOLD.

## Eval 2 — owned local CL.TE differential

An exact proxy/backend pair is reproduced locally. Front-end logs show one request forwarded, backend logs show a shorter first message plus a queued owned canary on the same connection. Fresh-connection and unambiguous-framing controls eliminate the effect.

- **Reportable:** Yes as a confirmed desynchronization primitive if the deployed chain matches.
- **Severity:** Medium candidate; raise only for separately proven boundary impact.
- **Missing proof:** Current scoped deployment equivalence and a safe owned impact path.
- **Likely triage rejection:** “Lab-only” if product versions/configuration or hop topology do not match production.
- **Next action:** Capture exact deployment provenance and use one owner-approved owned-canary impact check.
- **Decision:** HOLD pending deployment binding; REPORT if binding is established.

## Eval 3 — HTTP/2 downgrade strips framing header

The client-facing hop accepts an HTTP/2 request containing a transfer-framing header but strips it before generating HTTP/1.1. Backend logs show one complete request, no queued bytes, and no timing or response-order differential.

- **Reportable:** No.
- **Severity:** None.
- **Missing proof:** None; the negative control resolves the hypothesis.
- **Likely triage rejection:** Header acceptance at the edge is not backend desynchronization.
- **Next action:** Record the enforced translation behavior and close the branch.
- **Decision:** DISCARD.

## Eval 4 — owner-coordinated staging cache/routing effect

On an owned staging replica matching production, an ambiguous framing request causes the next unique owned canary to be routed under the attacker's prefixed path on the same backend connection. No-reuse, strict-framing, and patched-proxy controls prevent the effect; no third-party traffic is present.

- **Reportable:** Yes.
- **Severity:** Medium by default; High only if an owned authorization/session/cache control demonstrates meaningful unauthorized data or action.
- **Missing proof:** Exact scoped deployment/version/configuration and the specific impact claimed in the report.
- **Likely triage rejection:** Overstated impact if only route corruption—not unauthorized capability—is shown.
- **Next action:** Preserve the minimal wire/log/canary evidence and report the proven consequence without extrapolating cross-user compromise.
- **Decision:** REPORT.
