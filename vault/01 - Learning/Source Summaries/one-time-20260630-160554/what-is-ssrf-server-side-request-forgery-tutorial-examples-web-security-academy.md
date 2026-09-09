---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.075189+00:00
source_quality: 9
classification: severity rule
vulnerability_class: API Security
---

# What is SSRF (Server-side request forgery)? Tutorial & Examples | Web Security Academy

- URL: `https://portswigger.net/web-security/ssrf`
- Source group: `backfill_deep_content`
- Content chars: `12880`
- Classification: **severity rule**
- Vulnerability class: **API Security**

## Source summary

- To provide the stock information, the application must query various back-end REST APIs.
- It does this by passing the URL to the relevant back-end API endpoint via a front-end HTTP request.
- In this example, an attacker can modify the request to specify a URL local to the server: POST /product/stock HTTP/1.0 Content-Type: application/x-www-form-urlencoded Content-Length: 118 stockApi=http://localhost/admin The server fetches the contents of the /admin URL and returns it to the user.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
