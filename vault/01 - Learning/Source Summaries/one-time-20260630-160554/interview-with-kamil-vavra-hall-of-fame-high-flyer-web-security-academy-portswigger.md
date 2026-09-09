---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.068233+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# Interview with Kamil Vavra - Hall of Fame high flyer | Web Security Academy - PortSwigger

- URL: `https://portswigger.net/web-security/getting-started/kamil-vavra/index.html`
- Source group: `backfill_deep_content`
- Content chars: `10565`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- The first vulnerability that I ever learned about, roughly 15 years ago, was cross-site scripting .
- I knew how to exploit XSS, SQLi, everything in the OWASP Top 10, but my English was so bad.
- It's my favorite vulnerability to this day, so I naturally started with XSS - I even learned a few new things.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
