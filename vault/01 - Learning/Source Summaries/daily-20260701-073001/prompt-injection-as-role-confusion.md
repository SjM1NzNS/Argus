---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.393402+00:00
source_quality: 5
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Prompt Injection as Role Confusion

- URL: `https://simonwillison.net/2026/Jun/22/prompt-injection-as-role-confusion/`
- Source group: `daily_deep_content`
- Content chars: `2837`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- They call the underlying mechanism "role confusion", and describe it as a key challenge in addressing prompt injection in today's models: Unless LLMs achieve genuine role perception, we think injection defense will remain a perpetual whack-a-mole game.
- Recent articles Have your agent record video demos of its work with shot-scraper video - 30th June 2026 Porting the Moebius 0.2B image inpainting model to run in the browser with Claude Code - 22nd June 2026 sqlite-utils 4.0rc1 adds migrations and nested transactions - 21st June 2026 This is a link post by Simon Willison, posted on 22nd June 2026 .
- They found that "destyling" - rewriting text in a slightly different way such that it looked less like the expected format in a role tag - had a material impact on how the model classified the text: To a human reader, these two versions say the same thing.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
