---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.059352+00:00
source_quality: 5
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Arcanum PI Taxonomy - Prompt Injection Attack Classification

- URL: `https://arcanum-sec.github.io/arc_pi_taxonomy/`
- Source group: `web2_core_theory`
- Content chars: `2209`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Direct delivery Indirect delivery Either LOCAL Requires local model-weight access (click a card to learn more) Attack Intents Goals and objectives of prompt injection attacks Attack Techniques Methods used to execute prompt injection attacks Attack Evasions Obfuscation methods to avoid detection Attack Inputs Attack surfaces and input vectors for injection Prompt injection can occur both directly (user input) and indirectly (via external data sources).
- Prompt Injection Taxonomy v1.6.1 Attack Classification System for AI red teaming and penetration testing.
- This section captures interesting attack surfaces and input vectors for prompt injection attacks.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
