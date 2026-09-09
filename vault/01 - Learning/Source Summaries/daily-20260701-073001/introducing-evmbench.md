---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.416415+00:00
source_quality: 5
classification: severity rule
vulnerability_class: AI / LLM Security
---

# Introducing EVMbench

- URL: `https://www.paradigm.xyz/2026/02/evmbench`
- Source group: `browser_dom_linked_resources`
- Content chars: `2951`
- Classification: **severity rule**
- Vulnerability class: **AI / LLM Security**

## Source summary

- When we started working on this project, top models were only able to exploit less than 20% of the critical, fund-draining Code4rena bugs.
- As LLMs rapidly improve at finding exploits, it is important that we have visibility into and influence over the risks they could create for crypto.
- EVMbench is an open evaluation framework that tests AI agents across detecting, patching, and exploiting vulnerabilities.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
