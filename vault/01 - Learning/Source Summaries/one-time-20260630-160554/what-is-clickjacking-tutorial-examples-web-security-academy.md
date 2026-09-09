---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.060873+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# What is Clickjacking? Tutorial & Examples | Web Security Academy

- URL: `https://portswigger.net/web-security/clickjacking`
- Source group: `backfill_deep_content`
- Content chars: `11530`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Constructing an attack Using Clickbandit Clickjacking with prefilled form input Frame busting scripts Combining clickjacking with a DOM XSS attack Multistep clickjacking Preventing attacks X-Frame-Options Content Security Policy (CSP) View all clickjacking labs Web Security Academy Clickjacking Clickjacking (UI redressing) In this section we will explain what clickjacking is, describe common examples of clickjacking attacks and discuss how to protect against these attacks.
- Clickjacking attacks are not mitigated by the CSRF token as a target session is established with content loaded from an authentic website and with all requests happening on-domain.
- Frame busting scripts Clickjacking attacks are possible whenever websites can be framed.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
