---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.082125+00:00
source_quality: 10
source_id: immunefi-research
source_role: primary_research
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, reportability_criterion]
classification: severity rule
vulnerability_class: Accounting / Invariants
---

# Nearly Every Long-Running Bug Bounty Program on Immunefi Has Found a Critical Bug

- URL: `https://immunefi.com/blog/research/nearly-every-long-running-bug-bounty-program-on-immunefi-has-found-a-critical-bug`
- Source ID / role / trust: `immunefi-research` / `primary_research` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://immunefi.com/blog/research/`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `12682`
- Classification: **severity rule**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- A real critical, the kind that translates into drained funds or full protocol compromise.
- The Amador's Hack Impact Estimate puts the cost of an exploit at roughly $25 million in direct theft, a 61% six-month token decline, an 84% probability of no recovery, and a minimum of three months of lost organizational output.
- Home Customers Whitehat Spotlight Security Guides Research Get Protected Nearly Every Long-Running Bug Bounty Program on Immunefi Has Found a Critical Bug Copy Copied 20 Apr 2026 • 8 min read Nearly Every Long-Running Bug Bounty Program on Immunefi Has Found a Critical Bug Five years of Immunefi data shows that 93.9% of bug bounty programs running 5+ years have surfaced a confirmed critical vulnerability.

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
