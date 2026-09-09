---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.085970+00:00
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

# Shieldify's finding: [L-02] `expiredIndexFloor` Strands a Gauge's Emission Share Whenever a Full Epoch Is Missed, in Every Cap Mode: Up_2026-07-22

- URL: `https://solodit.cyfrin.io/issues/l-02-expiredindexfloor-strands-a-gauges-emission-share-whenever-a-full-epoch-is-missed-in-every-cap-mode-shieldify-none-up-markdown`
- Source ID / role / trust: `solodit-by-cyfrin-findings-filtered-by-recency` / `report_repository` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://solodit.cyfrin.io/?i=HIGH%2CMEDIUM%2CLOW%2CGAS&maxf=&minf=&rf=alltime&sd=Desc&sf=Recency`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `5393`
- Classification: **severity rule**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- So in Enforced mode this is (at most) an accounting/attribution inconsistency, not a fund-loss bug.
- Location of Affected Code File: contracts/Voter.sol#L924-L952 function _settleExpiredEpochs() internal { uint256 currentEpoch = ProtocolTimeLibrary.epochStart(block.timestamp); if (activeCapEpoch == 0) { activeCapEpoch = currentEpoch; activeEpochStartIndex = index; _applyQueuedCapModeFor(currentEpoch); return; } if (activeCapEpoch >= currentEpoch) { _applyQueuedCapModeFor(currentEpoch); return; } ​ uint256 expiredEpoch = activeCapEpoch; uint256 burnAmount = epochReserve[expiredEpoch]; epochReserve[expiredEpoch] = 0; epochBurned[expiredEpoch] += burnAmount; epochSettled[expiredEpoch] = true; if (burnAmount != 0) liveAccountedReserve -= burnAmount; expiredIndexFloor = index; activeCapEpoch = currentEpoch; activeEpochStartIndex = index; _applyQueuedCapModeFor(currentEpoch); ​ if (burnAmount != 0) { IUp(rewardToken).burnFrom(address(this), burnAmount); } emit EpochCapSettled(expiredEpoch, expiredIndexFloor, burnAmount, liveAccountedReserve); } Impact Under Disabled/ObserveOnly mode (the modes the protocol launches in), any gauge that goes a full epoch without being touched by _updateFor()/distribute()/vote()/reset()/poke() loses its entire pro-rata emission share for that epoch.
- Overview Impact Low Quality 0.0 (0) Rarity 0.0 (0) Full report https://github.com/shieldify-security/audits-portfolio-md/blob/main/Up-Security-Review.md Categories Tags Author(s) Shieldify Security Cyfrin Private Audits Public Reports Pricing Aderyn Updraft Blockchain Basics Solidity 101 Foundry 101 All courses CodeHawks Competitions First Flights Leaderboard Solodit Docs Findings Audits Checklist Resources Blog Case Studies Success Stories Glossary Support Powered by Cyfrin Give us feedback!

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
