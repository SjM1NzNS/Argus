---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.403519+00:00
source_quality: 6
classification: severity rule
vulnerability_class: Oracle / Economic
---

# Based Loans

- URL: `https://code4rena.com/reports/2021-04-basedloans`
- Source group: `browser_dom_linked_resources`
- Content chars: `30937`
- Classification: **severity rule**
- Vulnerability class: **Oracle / Economic**

## Source summary

- This leads to wrong oracle prices for the actual token which could in the worst case be used to borrow more tokens at a lower price or borrow more tokens by having a higher collateral value, essentially allowing undercollateralized loans that cannot be liquidated.
- Skip Navigation For Wardens Support Log in Based Loans Findings & Analysis Report 2021-05-27 Table of contents Overview About C4 Wardens Summary Scope Severity Criteria High Risk Findings [H-01] UniswapConfig getters return wrong token config if token config does not exist [H-02] uint(-1) index for not found Medium Risk Findings [M-01] Reward rates can be changed through flash borrows Low Risk Findings [G-01] requireNoError can be optimized [L-01] No account existence check for low-level call in CEther.sol [L-02] sweepToken() function removed in CErc20.sol from original Compound code [L-03] All except one Comptroller verify functions do not verify anything in Comptroller.sol/CToken.sol [L-04] Floating pragma used in Uniswap*.sol [L-05] Missing input validation may set COMP token to zero-address in Comptroller.sol [L-06] Missing zero/threshold check for maxAssets [L-07] Usage of address.transfer [L-08] Unbounded iteration on refreshCompSpeedsInternal [L-09] uint[] memory parameter is tricky [L-10] CarefulMath / safe math not allways used [L-11] Use ‘receive’ when expecting eth and empty call data [L-12] Allow borrowCap to be filled fully Non-Critical Findings [N-01] Outdated Compiler [N-02] Missed NatSpec @param for newly introduced parameter distributeAll [N-02] Privileged roles [N-03] UniswapAnchoredView’s PriceUpdated event is never fired [N-04] Multiple error enums with overlapping values [N-05] now is still used [N-06] Reliance on the fact that NO_ERROR = 0 [N-07] Alphabetical order not complied with (contrary to the comments) [N-08] requireNoError not used in a consistent way [N-09] uint(-1) [N-10] More readable constants [N-11] function getUnderlyingPrice compares against “cETH” [N-12] Use ‘interface’ keyword for interfaces [N-13] [Info] functions ‘getUnderlyingPriceView’ and ‘price’ are too similar [N-14] Requires a non-zero address check when deploying CErc20 tokens and CEther. [N-15] Missing event visibility in _setCompAddress() function Disclosures Overview About C4 Code 432n4 (C4) is an open organization that consists of security researchers, auditors, developers, and individuals with domain expertise in the area of smart contracts.
- Recommend fixing the non-existence check. ghoul-sol (Based Loans) confirmed: Addressed in this PR [H-02] uint(-1) index for not found Functions getTokenConfigBySymbolHash, getTokenConfigByCToken and getTokenConfigByUnderlying check returned index against max uint: index != uint(-1) -1 should indicate that the index is not found, however, a default value for an uninitialized uint is 0, so it is impossible to get -1.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
