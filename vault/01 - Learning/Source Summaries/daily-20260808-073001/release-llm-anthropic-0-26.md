---
type: learning-source-summary
compiled_at: 2026-08-08T05:31:23.159455+00:00
source_quality: 5
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Release: llm-anthropic 0.26

- URL: `https://simonwillison.net/2026/Aug/4/llm-anthropic/`
- Source group: `daily_deep_content`
- Content chars: `1674`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Simon Willison’s Weblog 4th August 2026 Includes new features enabled by LLM 0.32 : New models: claude-fable-5 , claude-sonnet-5 , and claude-opus-5 . #75 , #76 Added server-side tools for WebSearch , WebFetch , CodeExecution , and AnthropicMCP , available through LLM's -T interface or Python tools= .
- The previous -o web_search* options have been removed in favor of -T WebSearch . #79 Upgraded to llm>=0.32 .
- Reasoning, tool calls, tool results, and server-side tool results now stream as typed events.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
