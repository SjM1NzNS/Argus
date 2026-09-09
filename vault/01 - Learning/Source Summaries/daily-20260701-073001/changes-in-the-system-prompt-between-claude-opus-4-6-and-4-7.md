---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.392635+00:00
source_quality: 5
classification: severity rule
vulnerability_class: AI / LLM Security
---

# Changes in the system prompt between Claude Opus 4.6 and 4.7

- URL: `https://simonwillison.net/2026/Apr/18/opus-system-prompt/`
- Source group: `daily_deep_content`
- Content chars: `7182`
- Classification: **severity rule**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Their system prompt archive now dates all the way back to Claude 3 in July 2024 and it’s always interesting to see how the system prompt evolves as they publish new models.
- I had Claude Code take the Markdown version of their system prompts , break that up into separate documents for each of the models and then construct a Git history of those files over time with fake commit dates representing the publication dates of each updated prompt— here’s the prompt I used with Claude Code for the web.
- The list of Claude tools mentioned in the system prompt now includes "Claude in Chrome—a browsing agent that can interact with websites autonomously, Claude in Excel—a spreadsheet agent, and Claude in Powerpoint —a slides agent.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
