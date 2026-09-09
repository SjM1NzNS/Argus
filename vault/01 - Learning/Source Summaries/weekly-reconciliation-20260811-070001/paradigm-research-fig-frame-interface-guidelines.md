---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.121700+00:00
source_quality: 9
source_id: paradigm-research
source_role: primary_research
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: []
classification: technique
vulnerability_class: File Upload / Media Processing
---

# Fig: Frame Interface Guidelines

- URL: `https://www.paradigm.xyz/writing/fig`
- Source ID / role / trust: `paradigm-research` / `primary_research` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://www.paradigm.xyz/writing`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `5076`
- Classification: **technique**
- Vulnerability class: **File Upload / Media Processing**

## Source summary

- Frames turn any cast into an embedded interactive app in a Farcaster client such as Warpcast, redefining how content is viewed, engaged, and shared on social media.
- We provide all that guidance in the repository’s README, and in a separate Figma community file which you can fork and play with.
- Recently, Wevm built Frog UI, an extension of the Frog Framework that provides type-safe layout & styling primitives to help you build extensible and consistent dynamic Frame Image interfaces.

## Extracted methodology

- Affected surface: File upload / media parser / async processing surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `unclassified`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
