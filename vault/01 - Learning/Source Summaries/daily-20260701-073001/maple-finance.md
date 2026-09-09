---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.404142+00:00
source_quality: 6
classification: severity rule
vulnerability_class: Accounting / Invariants
---

# Maple Finance

- URL: `https://code4rena.com/reports/2021-04-maple`
- Source group: `browser_dom_linked_resources`
- Content chars: `27670`
- Classification: **severity rule**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- Based on the OWASP methodogology, I’m judging this as Likelihood=Low (because of the requirement to get it past human review) and Impact=High (because of the impact of the bug if it were exploited to create a 0-collateral loan and default on it), resulting in a Severity of Medium. [M-02] Potential huge arbitrage opportunities / MPL price decrease When the protocol suffers a default, the BPT stakers are the first line of defense and the protocol trades the BPT pool tokens for the single-sided liquidity asset of the Balancer LIQUIDITY <> MPT pool. (PoolLib.handleDefault) Note that a pool token to single-asset trade
- Low Risk Findings [L-01] Cross-Chain Replay Attack [L-02] Missing check for Pool state on several functions in Pool.sol [L-03] Mirrored admin variables in global context, Pool, PoolFactory, Loan and LoanFactory may make it confusing for deployment and maintenance [L-04] Full payment does not consider late fees of the payment [L-05] Chainlink Price data could be stale [L-06] Chainlink Price oracle always assumes 8 decimals [L-07] Missing check on setManualPrice(int256 _price) [L-08] Missing non-zero check [L-09] MPL reward claims of balancer pools can be exploited [L-10] MPL USDC distributions can be withdrawn by anyone [L-11] LoanLib.unwind uses globals.fundingPeriod() [L-12] Uniswap DOS Non-Critical Findings Disclosures Overview About C4 Code 432n4 (C4) is an open organization that consists of security researchers, auditors, developers, and individuals with domain expertise in the area of smart contracts.
- We advise the same paradigm as _toWad to be applied, which is secure. lucas-manuel (Maple) acknowledged: We are aware that we cannot onboard liquidityAssets or collateralAssets with more that 18 decimals of precision, and will make that part of our onboarding criteria.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
