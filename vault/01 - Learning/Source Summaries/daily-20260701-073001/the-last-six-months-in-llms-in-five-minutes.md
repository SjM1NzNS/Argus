---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.391909+00:00
source_quality: 5
classification: severity rule
vulnerability_class: AI / LLM Security
---

# The last six months in LLMs in five minutes

- URL: `https://simonwillison.net/2026/May/19/5-minute-llms/`
- Source group: `daily_deep_content`
- Content chars: `6857`
- Classification: **severity rule**
- Vulnerability class: **AI / LLM Security**

## Source summary

- OpenAI and Anthropic had spent most of 2025 running Reinforcement Learning from Verifiable Rewards to increase the quality of code written by their models, especially when paired up with their Codex and Claude Code agent harnesses.
- Over the holiday period, from December to January, a whole lot of us took advantage of the break to have a poke at these new models and coding agents and see what they could do.
- The coding agents got really good... and the laptop-available models, while a lot weaker than the frontier, have started wildly outper

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
