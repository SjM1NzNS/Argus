---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.083177+00:00
source_quality: 4
source_id: solodit-by-cyfrin-findings-filtered-by-recency
source_role: report_repository
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [evidence_requirement, reportability_criterion]
classification: Web3 skill update
vulnerability_class: Oracle / Economic
---

# Cyfrin's finding: `AccountableYield::_accrueFees` re-reads the vault `totalSupply` already loaded by `_accruedFeeShares`: Accountable Pr_2026-06-30

- URL: `https://solodit.cyfrin.io/issues/accountableyield_accruefees-re-reads-the-vault-totalsupply-already-loaded-by-_accruedfeeshares-cyfrin-none-accountable-pr-markdown`
- Source ID / role / trust: `solodit-by-cyfrin-findings-filtered-by-recency` / `report_repository` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://solodit.cyfrin.io/?i=HIGH%2CMEDIUM%2CLOW%2CGAS&maxf=&minf=&rf=alltime&sd=Desc&sf=Recency`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `2647`
- Classification: **Web3 skill update**
- Vulnerability class: **Oracle / Economic**

## Source summary

- AccountableYield.sol 504: (uint256 performanceFeeShares, uint256 managementFeeShares, uint256 newTotalAssets) = _accruedFeeShares(); 565: uint256 supply = IAccountableVault(vault_).totalSupply(); // inside _accruedFeeShares 511: uint256 totalSupply = IAccountableVault(vault).totalSupply(); // re-read on the same path, no mint between Recommended Mitigation: Have _accruedFeeShares also return the supply it already loads, and consume that value in _accrueFees (and in _sharePrice) instead of issuing a second totalSupply call.
- No shares are minted between the two reads (the fee-share mints happen later at src/strategies/AccountableYield.sol:545,549), so the second cross-contract STATICCALL returns an identical value and repeats work already done. _sharePrice (src/strategies/AccountableYield.sol:617-623) has the same pattern: it calls _accruedFeeShares and then re-reads totalSupply.
- Accountable: Fixed in commit aea937c Cyfrin: Verified. \clearpage Overview Impact Gas Quality 5.0 (1) Rarity 0.0 (0) Full report https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-30-cyfrin-accountable-pr75-v2.0.md Categories Tags Author(s) Immeas, Alix40 Cyfrin Private Audits Public Reports Pricing Aderyn Updraft Blockchain Basics Solidity 101 Foundry 101 All courses CodeHawks Competitions First Flights Leaderboard Solodit Docs Findings Audits Checklist Resources Blog Case Studies Success Stories Glossary Support Powered by Cyfrin Give us feedback!

## Extracted methodology

- Affected surface: Web3 protocol / smart contract
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
