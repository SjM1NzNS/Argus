---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.123124+00:00
source_quality: 9
source_id: paradigm-research
source_role: primary_research
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [validation_technique]
classification: Web2 skill update
vulnerability_class: API Security
---

# Joining Paradigm as Research Advisor

- URL: `https://www.paradigm.xyz/writing/joining-paradigm-21`
- Source ID / role / trust: `paradigm-research` / `primary_research` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://www.paradigm.xyz/writing`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `3914`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- I am excited to be working with Dan Robinson, Matt Huang, and the rest of the Paradigm investing and research teams to advise the next generation of crypto startups.
- This has dovetailed with my experience as a quantitative trader, from trading bonds and interest rate derivatives as a partner in a hedge fund while an MIT undergrad, to more recently developing stat arb strategies for trading stocks.
- Since DeFi summer, I have become interested in understanding the mechanisms for decentralized trading, in particular automated market makers such as Uniswap.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `validation_technique`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
