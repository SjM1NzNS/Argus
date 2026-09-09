---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.082590+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# Contact us - PortSwigger

- URL: `https://portswigger.net/contact`
- Source group: `backfill_deep_content`
- Content chars: `1228`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Sales and customer support Our team are the first port of call for sales support, quotations, licensing and subscriptions, procurement, and customer queries.
- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
