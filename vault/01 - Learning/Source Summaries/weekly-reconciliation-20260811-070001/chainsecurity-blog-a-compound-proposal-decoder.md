---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.112881+00:00
source_quality: 9
source_id: chainsecurity-blog
source_role: primary_research
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [validation_technique, evidence_requirement, tooling_procedure]
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# A Compound Proposal Decoder

- URL: `https://www.chainsecurity.com/blog/a-compound-proposal-decoder`
- Source ID / role / trust: `chainsecurity-blog` / `primary_research` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://www.chainsecurity.com/blog`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `2893`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Audits Testimonials Why Us Institutional Team & Careers Blog Contact REQUEST AUDIT Back to Overview A Compound Proposal Decoder October 15, 2025 How it works How to Use It Helping the Community Understand Proposals Better More details on Github To help the Compound community dig deeper and verify proposals independently, ChainSecurity has developed the Compound Proposal Decoder, an open-source CLI tool that fetches and better displays everything that’s happening inside a Compound proposal. ‍ Understanding what a Compound governance proposal actually does can be tricky.
- While platforms like Tally do a great job of displaying proposal summaries, they often don’t show every detail, especially low-level data such as encoded transactions, rollups, and bridges.
- This requires a deeper understanding of the proposal flow and differs between protocols.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `validation_technique, evidence_requirement, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
