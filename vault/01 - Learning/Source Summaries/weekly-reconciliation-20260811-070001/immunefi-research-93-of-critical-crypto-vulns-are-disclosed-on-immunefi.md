---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.079960+00:00
source_quality: 10
source_id: immunefi-research
source_role: primary_research
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [evidence_requirement, reportability_criterion, hunting_methodology]
classification: severity rule
vulnerability_class: Bridge / Proof Validation
---

# 93% of Critical Crypto Vulns Are Disclosed on Immunefi.

- URL: `https://immunefi.com/blog/research/93-of-critical-crypto-vulns-are-disclosed-on-immunefi`
- Source ID / role / trust: `immunefi-research` / `primary_research` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://immunefi.com/blog/research/`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `13611`
- Classification: **severity rule**
- Vulnerability class: **Bridge / Proof Validation**

## Source summary

- HackenProof estimates run from 2018 through 2026.
- The closest competitor, HackenProof (the second-largest crypto-focused bug bounty platform), still trails by roughly 14.5x, and that comparison uses upper-bound assumptions favorable to HackenProof.
- Directly measured (Immunefi internal data) 7,695 confirmed BBP reports (audit competition submissions excluded) 1,143 confirmed BBP criticals scoped to blockchain and smart contract assets ~14.9% critical rate across valid BBP submissions Estimated (competitor platforms, from public sources) HackenProof.

## Extracted methodology

- Affected surface: Bridge, rollup, proof verification, or settlement boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `evidence_requirement, reportability_criterion, hunting_methodology`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
