---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.104249+00:00
source_quality: 9
source_id: cantina-competitions
source_role: report_repository
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [validation_technique, evidence_requirement, reportability_criterion]
classification: severity rule
vulnerability_class: Authentication / Session
---

# pump.fun / PumpSwap competition | Cantina

- URL: `https://cantina.xyz/competitions/19c5a5a6-f68d-4da8-b185-3f28c7f97bc1`
- Source ID / role / trust: `cantina-competitions` / `report_repository` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://cantina.xyz/opportunities/ended`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `3813`
- Classification: **severity rule**
- Vulnerability class: **Authentication / Session**

## Source summary

- The other code base is the pump swap contracts which facilitates liquidity provisioning and trading using a constant product formula to determine the price and lp tokens to represent liquidity positions.
- All coins created on Pump are fair-launch, meaning everyone has equal access to buy and sell when the coin is first created.
- Severity level Impact: High Impact: Medium Impact: Low Likelihood: High Critical/High (Conditional) High Medium Likelihood: Medium High Medium Low Likelihood: Low Medium Low Informational Critical severity: If an attack can result in a loss of more than 50% of the TVL then this can be considered as a critical severity finding.

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
