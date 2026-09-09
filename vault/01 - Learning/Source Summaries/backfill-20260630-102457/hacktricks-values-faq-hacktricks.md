---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:41.981052+00:00
source_quality: 6
classification: Web2 skill update
vulnerability_class: Client-Side / XSS
---

# HackTricks Values & FAQ - HackTricks

- URL: `https://hacktricks.wiki/welcome/hacktricks-values-and-faq.html`
- Source group: `backfill_deep_content`
- Content chars: `8956`
- Classification: **Web2 skill update**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- Support HackTricks Check the subscription plans !
- HackTricks Values Tip These are the values of the HackTricks Project : Give FREE access to EDUCATIONAL hacking resources to ALL Internet.
- ORGANIZE all the hacking techniques in the book so it’s MORE ACCESSIBLE The HackTricks team has dedicated thousands of hours for free only to organize the content so people can learn faster HackTricks faq Tip Thank you so much for these resources, how can I thank you?

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
