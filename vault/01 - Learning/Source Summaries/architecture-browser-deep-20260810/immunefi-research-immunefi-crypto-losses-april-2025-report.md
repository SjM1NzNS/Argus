---
type: learning-source-summary
compiled_at: 2026-08-10T20:43:59.411413+00:00
source_quality: 5
source_id: immunefi-research
source_role: primary_research
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [reportability_criterion]
classification: severity rule
vulnerability_class: Accounting / Invariants
---

# Immunefi Crypto Losses April 2025 Report

- URL: `https://immunefi.com/blog/research/immunefi-crypto-losses-april-2025-report`
- Source ID / role / trust: `immunefi-research` / `primary_research` / `primary`
- Acquisition provenance: cadence=`backfill`, method=`browser_dom`, discovered-from=`https://immunefi.com/blog/research/`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `3728`
- Classification: **severity rule**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- Fraud Analysis In April 2025, hacks continued to be the predominant cause of losses compared to fraud, accounting for 100% of the total losses.
- Share on or Copy Copied RESEARCH YOU MIGHT ALSO LIKE The Ecosystem Vulnerability Scoreboard: 6 Years of DeFi Loss Data 12 min read Nearly Every Long-Running Bug Bounty Program on Immunefi Has Found a Critical Bug 8 min read What an Onchain Hack Actually Costs: 2024-2025 Update 8 min read

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `reportability_criterion`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
