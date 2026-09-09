---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.415328+00:00
source_quality: 5
classification: severity rule
vulnerability_class: Web3 General
---

# Writing

- URL: `https://www.paradigm.xyz/writing`
- Source group: `web3_continuous_monitoring`
- Content chars: `3447`
- Classification: **severity rule**
- Vulnerability class: **Web3 General**

## Source summary

- We aim to make prediction market data intuitive, accessible, and easy to explore.
- 02.04.2026|Storm Slivkoff Introducing EVMbench Paradigm and OpenAI build EVMbench as an open evaluation framework that tests AI agents across detecting, patching, and exploiting vulnerabilities.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
