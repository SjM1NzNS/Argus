---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.106380+00:00
source_quality: 10
source_id: cantina-competitions
source_role: report_repository
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [validation_technique, evidence_requirement, reportability_criterion]
classification: severity rule
vulnerability_class: Authentication / Session
---

# Uniswap Labs / uniswap-v4 competition | Cantina

- URL: `https://cantina.xyz/competitions/e2cf6906-ec8b-4c78-a585-74ac90615659`
- Source ID / role / trust: `cantina-competitions` / `report_repository` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://cantina.xyz/opportunities/ended`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `10892`
- Classification: **severity rule**
- Vulnerability class: **Authentication / Session**

## Source summary

- Opportunities Leaderboard Discover Cantina Log in Sign up uniswap-v4 @uniswap Completed Instructions Leaderboard Total reward $2,350,000 No deposit required Status Completed Findings submitted 451 Start date 6 Sep 2024 End date 1 Oct 2024 The Uniswap protocol is a peer-to-peer system designed for exchanging cryptocurrencies (ERC-20 Tokens) on the Ethereum blockchain.
- The protocol is implemented as a set of persistent, non-upgradable smart contracts; designed to prioritize censorship resistance, security, self-custody, and to function without any trusted intermediaries who may selectively restrict access.
- Please note there must be sufficient information and undeniable Proof of concept which should be easily verifiable for the loss amount for the finding to be considered Critical with absolutely no ambiguity.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `validation_technique, evidence_requirement, reportability_criterion`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
