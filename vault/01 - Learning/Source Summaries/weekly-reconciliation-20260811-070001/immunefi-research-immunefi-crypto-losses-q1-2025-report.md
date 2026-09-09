---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.075553+00:00
source_quality: 10
source_id: immunefi-research
source_role: primary_research
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, validation_technique]
classification: Web3 skill update
vulnerability_class: Accounting / Invariants
---

# Immunefi Crypto Losses Q1 2025 Report

- URL: `https://immunefi.com/blog/research/immunefi-crypto-losses-q1-2025-report`
- Source ID / role / trust: `immunefi-research` / `primary_research` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://immunefi.com/blog/research/`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `9746`
- Classification: **Web3 skill update**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- Total Losses: $1.6B Bybit: $1.46B Phemex, $69.1 Million On January 23, 2025, the Singapore-based cryptocurrency exchange Phemex suffered an exploit, resulting in over $69 million in losses drained from its hot wallets.
- Crypto Losses in Q1 2025 Key Takeaways in Q1 2025 The 2 major exploits of the quarter totaled $1.52 billion alone, accounting for 94% of all losses in Q1 2025.
- Overview As of March 2025, nearly $100 billion in capital was locked across Web3 protocols.

## Extracted methodology

- Affected surface: Web3 protocol / smart contract
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, validation_technique`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
