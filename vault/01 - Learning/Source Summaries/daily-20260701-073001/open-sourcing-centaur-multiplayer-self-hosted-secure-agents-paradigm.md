---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.415947+00:00
source_quality: 6
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Open Sourcing Centaur: Multiplayer, self-hosted, secure agents - Paradigm

- URL: `https://www.paradigm.xyz/2026/05/open-sourcing-centaur-multiplayer-self-hosted-secure-agents`
- Source group: `browser_dom_linked_resources`
- Content chars: `14283`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- About Team Portfolio Writing Open Source Careers Research Open Sourcing Centaur: Multiplayer, self-hosted, secure agents 05.21.2026|Georgios KonstantopoulosArjun BalajiZygimantas MagelinskasMatthew SlipperGoksu ToprakAkshaan KakarDan RobinsonOmar AzizAchal Srinivasan Today we’re open sourcing Centaur, the self-hosted runtime from Paradigm and Tempo for multiplayer, secure AI agents.
- Centaur is a shared agent that can use tools, run for hours or days, survive restarts, and operate with real credentials without ever seeing the raw secrets.
- You can add a tool once and every agent can use it.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
