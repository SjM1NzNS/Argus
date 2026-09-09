---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.404742+00:00
source_quality: 6
classification: severity rule
vulnerability_class: Accounting / Invariants
---

# Marginswap

- URL: `https://code4rena.com/reports/2021-04-marginswap`
- Source group: `browser_dom_linked_resources`
- Content chars: `39620`
- Classification: **severity rule**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- Skip Navigation For Wardens Support Log in Marginswap Findings & Analysis Report 2021-05-03 Table of contents Overview About C4 Wardens Summary Scope Severity Criteria High Risk Findings [H-01] Re-entrancy bug allows inflating balance [H-02] Missing fromToken != toToken check [H-03] Price feed can be manipulated [H-04] Inconsistent usage of applyInterest [H-05] Wrong liquidation logic [H-06] Users are credited more tokens when paying back debt with registerTradeAndBorrow [H-07] account.holdsToken is never set [H-08] Rewards cannot be withdrawn [H-09] lastUpdatedDay not initialized [H-11] Impossible to call withdrawReward fails due to run out of gas Medium Risk Findings [M-01] No default liquidationThresholdPercent [M-02] Missing checks if pairs equal tokens [M-03] No entry checks in crossSwap[Exact]TokensFor[Exact]Tokens [M-04] maintainer can be pushed out [M-05] Several function have no entry check [M-06] Users Can Drain Funds From MarginSwap By Making Undercollateralized Borrows If The Price Of A Token Has Moved More Than 10% Since The Last MarginSwap Borrow/Liquidation Involving Accounts Holding That Token. [M-07] diffMaxMinRuntime gets default value of 0 [M-08] PriceAware uses prices from getAmountsOut [M-09] Isolated margin contracts declare but do not set the value of liquidationThresholdPercent [M-10] Add a timelock to functions that set key variables Low Risk Findings [L-01] Events not indexed [L-02] getReserves does not check if tokens match [L-03] Role 9 in Roles.sol [L-04] Multisig wallets can’t be used for liquidate [L-05] Different solidity version in UniswapStyleLib.sol [L-06] sortTokens can be simplified [L-07] Duplicated Code In Admin.viewCurrentMaintenanceStaker() [L-08] Magic Numbers used in Admin._stake() When Constant Defined Above Can Be Used Instead [L-09] function initTranche should check that the share parameter is > 0 [L-10] runtime > 1 hours error message discrepancy [L-11] setLeveragePercent should check that new _leveragePercent >= 100 [L-12] An erroneous constructor’s argument could block the withdrawReward [L-13] Not emitting event for important state changes Non-Critical Findings Gas Optimizations Disclosures Overview About C4 Code 432n4 (C4) is an open organization that consists of security researchers, auditors, developers, and individuals with domain expertise in the area of smart contracts.
- High Risk Findings [H-01] Re-entrancy bug allows inflating balance One can call the MarginRouter.crossSwapExactTokensForTokens function first with a fake contract disguised as a token pair: crossSwapExactTokensForTokens(0.0001 WETH, 0, [ATTACKER_CONTRACT], [WETH, WBTC]).
- When the amounts are computed by the amounts = UniswapStyleLib.getAmountsOut(amountIn - fees, pairs, tokens); call, the attacker contract returns fake reserves that yield 1 WBTC for the tiny input.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
