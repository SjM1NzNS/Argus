---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.087840+00:00
source_quality: 5
source_id: solodit-by-cyfrin-findings-filtered-by-recency
source_role: report_repository
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [evidence_requirement, reportability_criterion]
classification: severity rule
vulnerability_class: Oracle / Economic
---

# Shieldify's finding: [L-03] `governanceCapActive` Unconditionally Disables the `emergencyCouncil` Circuit Breaker in `_distributeEnforced()`: Up_2026-07-22

- URL: `https://solodit.cyfrin.io/issues/l-03-governancecapactive-unconditionally-disables-the-emergencycouncil-circuit-breaker-in-_distributeenforced-shieldify-none-up-markdown`
- Source ID / role / trust: `solodit-by-cyfrin-findings-filtered-by-recency` / `report_repository` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://solodit.cyfrin.io/?i=HIGH%2CMEDIUM%2CLOW%2CGAS&maxf=&minf=&rf=alltime&sd=Desc&sf=Recency`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `13006`
- Classification: **severity rule**
- Vulnerability class: **Oracle / Economic**

## Source summary

- Team Response Acknowledged. [I-02] CLTwapOracle.sol and Gauge._pendingFees() Are Unreferenced Dead Code Severity Informational Risk Description Two unrelated pieces of code in this codebase are fully defined but never invoked from anywhere: CLTwapOracle.sol implements an on-chain Uniswap V3 TWAP-based price oracle (adapted TickMath/OracleLibrary logic).
- It is not imported by any other contract in scope, not referenced by GaugeCapController.sol (which is the contract that would plausibly need an on-chain price cross-check), and the only places it's mentioned anywhere in the repository are its own file and the attribution line in NOTICE.md.
- This is notable because GaugeCapController's gauge-cap valuation is otherwise entirely trust-based (a governor-appointed publisher or signer-quorum submits values with no on-chain sanity check) — CLTwapOracle looks like it was built specifically to close that gap and then never wired in.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `evidence_requirement, reportability_criterion`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `true`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
