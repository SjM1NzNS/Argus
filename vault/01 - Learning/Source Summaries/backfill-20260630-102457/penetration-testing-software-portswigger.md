---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.000013+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: Web2 General
---

# Penetration testing software - PortSwigger

- URL: `https://portswigger.net/testers`
- Source group: `backfill_deep_content`
- Content chars: `2875`
- Classification: **Web2 skill update**
- Vulnerability class: **Web2 General**

## Source summary

- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?
- It's packed with features and extensions - with the world's leading web vulnerability scanner at its core.
- The addition of the vulnerability scanner helps speed up the testing process and provide a baseline level of analysis on all parts of the web application, and allows me to focus efforts on the more advanced, harder to find vulnerabilities.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
