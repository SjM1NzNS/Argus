---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.396876+00:00
source_quality: 5
classification: Web2 skill update
vulnerability_class: IDOR / BOLA / Access Control
---

# API1:2019 — Broken object level authorization

- URL: `https://apisecurity.io/encyclopedia/content/owasp/api1-broken-object-level-authorization.htm`
- Source group: `appsec_fyi_linked_resources`
- Content chars: `1574`
- Classification: **Web2 skill update**
- Vulnerability class: **IDOR / BOLA / Access Control**

## Source summary

- This attack is also known as IDOR (Insecure Direct Object Reference).
- The lack of proper authorization checks allows attackers to access the specified resource.
- Home Encyclopedia OWASP API Top 10 Events Newsletter Contact Us API Security Encyclopedia OWASP API Security Top 10 API1:2019 — Broken object level authorization API2:2019 — Broken authentication API3:2019 — Excessive data exposure API4:2019 — Lack of resources and rate limiting API5:2019 — Broken function level authorization API6:2019 — Mass assignment API7:2019 — Security misconfiguration API8:2019 — Injection API9:2019 — Improper assets management API10:2019 — Insufficient logging and monitoring OWASP API Security Top 10 cheat sheet Share this article: API1:2019 — Broken object level authorization Attackers substitute the ID of their own resource in the API call with an ID of a resource belonging to another user.

## Extracted methodology

- Affected surface: Object, tenant, account, or authorization boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
