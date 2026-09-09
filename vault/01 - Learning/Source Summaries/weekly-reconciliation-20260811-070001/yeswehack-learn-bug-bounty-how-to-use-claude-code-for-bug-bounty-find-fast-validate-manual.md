---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.027783+00:00
source_quality: 8
source_id: yeswehack-learn-bug-bounty
source_role: practitioner_commentary
source_trust: curated_secondary
promotion_policy: corroboration_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, validation_technique, false_positive_condition, evidence_requirement, reportability_criterion, hunting_methodology, tooling_procedure]
classification: technique
vulnerability_class: AI / LLM Security
---

# How to use Claude Code for Bug Bounty: find fast, validate manually

- URL: `https://www.yeswehack.com/learn-bug-bounty/llm-series-claude`
- Source ID / role / trust: `yeswehack-learn-bug-bounty` / `practitioner_commentary` / `curated_secondary`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`https://www.yeswehack.com/blog/learn-bug-bounty`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `daily_deep_content`
- Content chars: `18290`
- Classification: **technique**
- Vulnerability class: **AI / LLM Security**

## Source summary

- A sensible split: Opus : Strong reasoning with complex problem-solving, verification and chaining odd behaviours into exploitable vulnerabilities Sonnet : Great for recon and mapping attack surface Haiku : Great for high-volume tasks where speed matters most, such as processing tool output or structuring large amounts of data LATEST CLAUDE CODE MODELS Find out more on Anthropic’s documentation hub As a Bug Bounty hunter, using different models for different purposes can save tokens and allow you to build a team of specialised LLM agents, balancing speed, cost and reasoning quality.
- Claude Code is an agentic command-line tool that can read and edit files, run shell commands and connect to your existing Bug Bounty tooling through the Model Context Protocol (MCP) .
- Choosing the right Claude model for each Job Token cost and latency add up fast in an agentic loop, so you don’t necessarily need to use the most capable model for every task.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, validation_technique, false_positive_condition, evidence_requirement, reportability_criterion, hunting_methodology, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
