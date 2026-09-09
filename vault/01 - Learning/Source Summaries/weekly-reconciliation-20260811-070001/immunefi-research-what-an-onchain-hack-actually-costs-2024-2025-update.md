---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.077719+00:00
source_quality: 10
source_id: immunefi-research
source_role: primary_research
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, reportability_criterion]
classification: Web3 skill update
vulnerability_class: AI / LLM Security
---

# What an Onchain Hack Actually Costs: 2024-2025 Update

- URL: `https://immunefi.com/blog/research/what-an-onchain-hack-actually-costs-2024-2025-update`
- Source ID / role / trust: `immunefi-research` / `primary_research` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://immunefi.com/blog/research/`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `13308`
- Classification: **Web3 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- That work introduced Amador's Hack Impact Estimate, a framework for measuring exploit damage well beyond the headline theft figure.
- Home Customers Whitehat Spotlight Security Guides Research Get Protected What an Onchain Hack Actually Costs: 2024-2025 Update Copy Copied 25 Mar 2026 • 8 min read What an Onchain Hack Actually Costs: 2024-2025 Update Immunefi An Immunefi research report on what a crypto exploit actually does to a protocol, beyond the stolen funds, based on five years of onchain incident data.
- Updated hack impact estimate for 2024-2025: A protocol hacked today should expect to lose roughly $25,000,000 USD in direct theft, see its token shed 61% of its value over the next six months, and face sustained price depression that 84% of hacked tokens never recover from within that window.

## Extracted methodology

- Affected surface: Web3 protocol / smart contract
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, reportability_criterion`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
