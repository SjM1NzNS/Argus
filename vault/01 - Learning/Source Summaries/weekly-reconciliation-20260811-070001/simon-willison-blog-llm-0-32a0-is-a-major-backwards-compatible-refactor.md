---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.032907+00:00
source_quality: 8
source_id: simon-willison-blog
source_role: practitioner_commentary
source_trust: curated_secondary
promotion_policy: corroboration_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, validation_technique, evidence_requirement, tooling_procedure]
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# LLM 0.32a0 is a major backwards-compatible refactor

- URL: `https://simonwillison.net/2026/Apr/29/llm/`
- Source ID / role / trust: `simon-willison-blog` / `practitioner_commentary` / `curated_secondary`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`https://simonwillison.net`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `daily_deep_content`
- Content chars: `11309`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Here’s what that looks like as a Python API consumer: import asyncio import llm model = llm . get_model ( "gpt-5.5" ) prompt = "invent 3 cool dogs, first talk about your motivations" def describe_dog ( name : str , bio : str ) -> str : """Record the name and biography of a hypothetical dog.""" return f" { name } : { bio } " def sync_example (): response = model . prompt ( prompt , tools = [ describe_dog ], ) for event in response . stream_events (): if event . type == "text" : print ( event . chunk , end = "" , flush = True ) elif event . type == "tool_call_name" : print ( f" \n Tool call: { event . chunk } (" , end = "" , flush = True ) elif event . type == "tool_call_args" : print ( event . chunk , end = "" , flu
- Previous versions of LLM modeled the world in terms of prompts and responses.
- Send the model a text prompt, get back a text response. import llm model = llm . get_model ( "gpt-5.5" ) response = model . prompt ( "Capital of France?" ) print ( response . text ()) This made sense when I started working on the library back in April 2023.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, validation_technique, evidence_requirement, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
