---
type: learning-source-summary
compiled_at: 2026-08-07T05:31:28.719781+00:00
source_quality: 9
classification: severity rule
vulnerability_class: AI / LLM Security
---

# Can AI do novel security research? Meet the HTTP Terminator | PortSwigger Research

- URL: `https://portswigger.net/research/can-ai-do-novel-security-research`
- Source group: `daily_deep_content`
- Content chars: `47225`
- Classification: **severity rule**
- Vulnerability class: **AI / LLM Security**

## Source summary

- My secondary objective was to push the "fully autonomous research" concept to complete failure by exceeding the capabilities of current SOTA models.
- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?
- It worked - I'll share an arsenal of new HTTP desync triggers, gadgets, and exploits that compromised banks, security solutions, and government infrastructure.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
