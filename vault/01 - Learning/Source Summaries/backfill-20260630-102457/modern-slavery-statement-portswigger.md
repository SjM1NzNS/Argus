---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:41.995707+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Modern Slavery Statement - PortSwigger

- URL: `https://portswigger.net/modern-slavery-statement`
- Source group: `backfill_deep_content`
- Content chars: `7288`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Employee wellbeing as an active safeguard PortSwigger operates on a fully office-based model and all employees work from our physical premises.
- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?
- All employees also have access to our Wellbeing resources and Help@Hand, our Bupa-backed Employee Assistance Programme, which provides confidential mental health and wellbeing support independent of line management.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
