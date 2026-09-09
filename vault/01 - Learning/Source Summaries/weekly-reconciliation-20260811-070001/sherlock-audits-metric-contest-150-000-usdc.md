---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.102990+00:00
source_quality: 10
source_id: sherlock-audits
source_role: report_repository
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, reportability_criterion]
classification: severity rule
vulnerability_class: API Security
---

# Metric Contest - 150,000 USDC

- URL: `https://audits.sherlock.xyz/contests/1279`
- Source ID / role / trust: `sherlock-audits` / `report_repository` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://audits.sherlock.xyz`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `10046`
- Classification: **severity rule**
- Vulnerability class: **API Security**

## Source summary

- A major on a CEX, a stock on the NYSE, even another pool, so a fraction of the capital does the same work.
- If the users create a pool with non-standard ERC20 tokens, the issues related to these are out of scope Are there any limitations on values set by admins (or other roles) in the codebase, including restrictions on array lengths?
- Are there any limitations on values set by admins (or other roles) in protocols you integrate with, including restrictions on array lengths?

## Extracted methodology

- Affected surface: Web/API/application surface
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
