---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.084175+00:00
source_quality: 4
source_id: solodit-by-cyfrin-findings-filtered-by-recency
source_role: report_repository
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [evidence_requirement, reportability_criterion]
classification: severity rule
vulnerability_class: Accounting / Invariants
---

# Shieldify's finding: [L-01] Provenance Fields Can Be Silently Rewritten on Locked Reports: Up_2026-07-22

- URL: `https://solodit.cyfrin.io/issues/l-01-provenance-fields-can-be-silently-rewritten-on-locked-reports-shieldify-none-up-markdown`
- Source ID / role / trust: `solodit-by-cyfrin-findings-filtered-by-recency` / `report_repository` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://solodit.cyfrin.io/?i=HIGH%2CMEDIUM%2CLOW%2CGAS&maxf=&minf=&rf=alltime&sd=Desc&sf=Recency`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `2854`
- Classification: **severity rule**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- Start researching Findings #66923 [L-01] Provenance Fields Can Be Silently Rewritten on Locked Reports Up ・ Jul 22, 2026 Severity Low Risk Description The "does this update expand capacity" check only inspects feeValueWeth, bribeValueWeth, and conservativeUpPriceWeth.
- Since publishGaugeEpochValue unconditionally overwrites all stored fields (including these) whenever the capacity check passes, an authorized publisher can rewrite a locked report's provenance data, pointing it at an entirely different source block or dataset, as long as the resulting emission-relevant values don't increase.
- Location of Affected Code File: contracts/gauge-caps/GaugeCapController.sol#L340-L352 function _reportExpandsCapacity( StoredReport storage stored, GaugeEpochValueReport calldata _report ) internal view returns (bool) { if (_report.status != REPORT_STATUS_VALID) return false; if (stored.status != REPORT_STATUS_VALID) return true; uint256 oldDenominator = stored.feeValueWeth + stored.bribeValueWeth; uint256 newDenominator = _report.feeValueWeth + _report.bribeValueWeth; if (newDenominator > oldDenominator) return true; if (stored.conservativeUpPriceWeth == 0) return true; return _report.conservativeUpPriceWeth < stored.conservativeUpPriceWeth; } Recommendation Extend _reportExpandsCapacity() (or add a parallel check) to also freeze provenance fields once stored.locked == true, i.e., disallow changes to sourceEpoch, sourceBlockHash, routeConfigHash, and sourceDataHash after locking, independent of whether the financial values are being corrected downward.

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
