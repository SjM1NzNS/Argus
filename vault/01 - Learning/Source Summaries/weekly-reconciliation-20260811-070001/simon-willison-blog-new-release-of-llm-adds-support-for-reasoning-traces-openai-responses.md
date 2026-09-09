---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.035142+00:00
source_quality: 7
source_id: simon-willison-blog
source_role: practitioner_commentary
source_trust: curated_secondary
promotion_policy: corroboration_required
promotion_status: proposal_only
knowledge_types: [evidence_requirement, reportability_criterion, tooling_procedure]
classification: Web2 skill update
vulnerability_class: Race Conditions / TOCTOU
---

# New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging

- URL: `https://simonwillison.net/2026/Aug/4/new-release-of-llm/`
- Source ID / role / trust: `simon-willison-blog` / `practitioner_commentary` / `curated_secondary`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`https://simonwillison.net`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `daily_deep_content`
- Content chars: `7806`
- Classification: **Web2 skill update**
- Vulnerability class: **Race Conditions / TOCTOU**

## Source summary

- Simon Willison’s Weblog New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging 4th August 2026 I released LLM 0.32 this morning, the most significant new version of LLM since the initial launch of the project.
- The new version includes support for visible reasoning traces, server-side provider tools, redesigned content-addressable SQLite logs, new models, and new features enabled by the OpenAI Responses API.
- Headline features for LLM CLI users Running LLM against reasoning models now displays their reasoning traces to standard error, so you can see what they are “thinking” without that information being included in the standard output that you might pipe to another tool.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `evidence_requirement, reportability_criterion, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
