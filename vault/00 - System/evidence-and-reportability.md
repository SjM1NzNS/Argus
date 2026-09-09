# ARGUS EVIDENCE AND REPORTABILITY RULES

Finding states:

1. Lead
2. Hypothesis
3. Testable candidate
4. Evidence-backed candidate
5. Reportable finding
6. Submitted report
7. Accepted / rejected / duplicate / informative

Argus must not skip states.

A finding is not report-ready until:

- it is in scope
- it is reproducible or sufficiently evidenced
- it has clear impact
- it has a clean attacker/victim/protocol model where applicable
- it does not require access to real user data
- secret validation, if applicable, is sufficient and safe
- the Skeptic Agent has tried to disprove it
- the Impact Agent agrees it is reportable
- the downgrade argument is weaker than the severity argument

Before recommending severity, Argus must produce:

1. The strongest invalidity argument.
2. The strongest downgrade argument.
3. Missing evidence.
4. Minimum proof required to survive triage.

## Seven-question pre-report gate — Pass A 2026-07-03

Promoted from external agent-skill source review. Before drafting any report, answer these quickly and lethally. One failed answer means `kill`, `downgrade`, `needs-owned-object`, or `needs-approval` — not report drafting.

1. Can this be reproduced now with exact steps, request, response, and setup?
2. Is the exact asset in scope and the bug class not excluded by program policy?
3. Does the attacker model avoid privileged/admin-only assumptions?
4. Is this undocumented or unintended behavior rather than public/expected design?
5. Does the proof show concrete impact beyond technical possibility or status-code difference?
6. Is it outside the common N/A set, or is there a proven second-link chain?
7. Do positive and negative controls prove the boundary with owned/test accounts, objects, repos, or contracts?

Common automatic downgrades/kills unless chained: missing headers, GraphQL introspection alone, self-XSS, open redirect alone, DNS-only SSRF, CORS without credentialed data access, logout CSRF, banner/version disclosure, missing cookie flags alone, source maps without secrets/capability, public API key with no demonstrated capability.

AuthZ findings require cross-identity proof: session/account A reaches session/account B data or action, a fresh session reproduces, and anonymous vs authenticated behavior is understood.

## Autonomous/model-generated candidate validation — 2026-07-03

Promoted from Joseph Thacker's Hackbot lessons.

If a candidate was generated or materially shaped by an autonomous agent, model, scanner, or long-running harness, add an adversarial validator pass before report drafting:

- attempt to disprove the exploit chain, not polish the report;
- reproduce the issue from raw evidence rather than trusting the model narrative;
- test the most likely false-positive explanation first;
- verify positive and negative controls with owned/test accounts or safe evidence;
- confirm the agent did not skip over auth, scope, intended-public behavior, caching, CORS non-impact, self-XSS, client-side-only behavior, or synthetic/test data;
- record the validation result and exact evidence path.

A validator pass may return `kill`, `downgrade`, `needs-owned-object`, `needs-approval`, or `survives-validation`. Only `survives-validation` can move to report drafting.

If evidence is insufficient, Argus must recommend hold or discard.

## Web2 High/Critical gate

No High or Critical Web2 severity without:

- in-scope asset
- realistic attacker model
- owned/test victim model where needed
- unauthorized access/change/action
- sensitive data, account impact, financial impact, admin impact, tenant impact, or meaningful business impact
- reproducible request/response evidence
- server-side enforcement failure
- Skeptic review
- downgrade argument

## Web3 High/Critical gate

No High or Critical Web3 severity without:

- in-scope contract/protocol
- realistic attacker transaction path
- no privileged/admin assumptions
- local or fork PoC
- measurable attacker profit, protocol loss, user loss, permanent freeze, governance/control impact, or accepted protocol impact
- invariant violation
- Skeptic review
- downgrade argument
