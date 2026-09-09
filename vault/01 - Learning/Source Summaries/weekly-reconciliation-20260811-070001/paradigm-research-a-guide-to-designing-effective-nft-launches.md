---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.119285+00:00
source_quality: 10
source_id: paradigm-research
source_role: primary_research
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, hunting_methodology]
classification: technique
vulnerability_class: Authentication / Session
---

# A Guide to Designing Effective NFT Launches

- URL: `https://www.paradigm.xyz/writing/a-guide-to-designing-effective-nft-launches`
- Source ID / role / trust: `paradigm-research` / `primary_research` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://www.paradigm.xyz/writing`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `39963`
- Classification: **technique**
- Vulnerability class: **Authentication / Session**

## Source summary

- Many lessons have been learned since, with today’s projects having a working product before launching a token and distributing it to incentivize usage and decentralize governance.
- / Writing [ M ] A Guide to Designing Effective NFT Launches 10.13.2021 By Hasu, Anish Agnihotri [L] Listen [S] Share 1 Examples of user harm 1.1 Exploitable fairness 1.2 Gas auctions 1.3 Gas inefficiency 1.4 Exclusive minting 1.5 Trusted operators 2 Goals of a good launch 2.1 Obscurity is no excuse for bad design 3 Unbundling NFT launches 3.1 Phase 1: Bidding 3.2 Phase 2: Clearing 3.3 Phase 3: Distribution 3.4 Phase 4: Metadata reveal 4 Our reference implementation 5 Conclusion Blockchains revolutionized fundraising for open-source software, but not everything worked right from the start.
- As a result, developers have to design mechanisms that are efficient and robust to exploitation.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, hunting_methodology`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
