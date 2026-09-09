---
type: eval-scenarios
status: active
created: "2026-07-29"
source_basis:
  - "HackerOne Hacktivity platform-generated Rocket.Chat DNS-rebinding SSRF summary"
  - "Preview.is RAG corroboration reviewed 2026-07-29"
---

# SSRF DNS-resolution and redirect-binding eval scenarios

## Scenario 1 — validated public address differs from the connected destination

In an exact local product fixture, the validator accepts a researcher-controlled hostname while it resolves to a public owned canary. The shipped HTTP path resolves it again and connects to a prohibited owned/local canary after a controlled DNS transition. Stable-public and blocked-destination controls use the same parser, resolver, proxy/client, redirect policy, and response consumer.

- **Reportable:** Yes, once the real product path and prohibited destination transition are proven in an authorized environment.
- **Severity:** Medium candidate for internal reachability; raise only for demonstrated sensitive response use, credential exposure, or meaningful internal action.
- **Missing proof:** Actor reachability, exact validation and connection addresses/timestamps, response use, negative controls, and target-specific impact.
- **Triage rejection risk:** DNS changed, but no evidence shows the product connected to the changed destination.
- **Next action:** Preserve the smallest owned-canary differential and stop; queue separate approval for any higher-impact boundary.
- **Decision:** REPORT the proven primitive with bounded impact; HOLD any unproven escalation.

## Scenario 2 — the HTTP client pins the vetted address

The validator resolves and approves a public address, the production client connects to that exact address while preserving hostname/SNI semantics, and a controlled later DNS change does not alter the peer. Mixed A/AAAA answers containing a prohibited address fail closed.

- **Reportable:** No.
- **Severity:** None.
- **Missing proof:** None if the exact production path and controls are preserved.
- **Triage rejection reason:** DNS mutation did not create a validation-to-connect destination differential.
- **Next action:** Retain as the fix/negative control.
- **Decision:** DISCARD.

## Scenario 3 — redirect target bypasses the original URL decision

An owned public endpoint passes the initial policy and returns a redirect to a prohibited owned/local canary. The production fetcher follows the redirect without re-running parsing, resolution, address classification, and connection binding, and the canary proves the second hop was reached.

- **Reportable:** Yes, if the redirect behavior is reachable by the scoped actor and the prohibited second hop is proven safely.
- **Severity:** Medium candidate; severity follows the reached capability and response/action impact, not the redirect alone.
- **Missing proof:** Full redirect chain, actual second-hop peer, response use, stable-public redirect control, and actor/impact boundaries.
- **Triage rejection risk:** The report shows only a crafted `Location` header or a client-side redirect, not a server-side followed request.
- **Next action:** Reproduce in the exact owned/local fetch path and verify that disabling redirects or per-hop revalidation removes the behavior.
- **Decision:** HOLD until server-side follow and impact are proven; otherwise DISCARD.

## Scenario 4 — public callback plus speculative rebinding

A URL fetcher reaches a researcher-controlled public endpoint. The researcher can change DNS later, but has no trace of a second resolution, changed peer, redirect bypass, prohibited service reachability, sensitive response, or internal action.

- **Reportable:** Not as DNS-rebinding bypass.
- **Severity:** Unrated base SSRF/fetch lead.
- **Missing proof:** Validation-to-connect differential, actual peer evidence, prohibited destination, and concrete impact.
- **Triage rejection reason:** A public callback and mutable DNS are presented as though they prove internal SSRF.
- **Next action:** Review source or reproduce the exact client locally; do not probe target-internal or metadata addresses by default.
- **Decision:** HOLD the base primitive; DISCARD the rebinding claim.
