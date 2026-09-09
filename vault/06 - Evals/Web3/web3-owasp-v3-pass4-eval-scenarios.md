---
type: eval-scenarios
status: draft
created: "2026-07-02"
source_basis:
  - "V3 corpus extraction pass 4 — Web3 OWASP alignment"
---

# Web3 OWASP Alignment Eval Scenarios — V3 Pass 4

Use these scenarios to check whether Web3 routing applies OWASP taxonomy without over-reporting taxonomy-only issues.

## Scenario 1 — Flash loan exists but no invariant break

A lending protocol can be called inside an Aave flash loan, but collateral checks use a robust Chainlink feed, caps apply, and no borrow/liquidation/share accounting invariant breaks.

Expected decision:

- Not reportable.
- Route to Flash Loans only as a checked lead.

## Scenario 2 — Flash-loan amplified oracle manipulation

A protocol values collateral using a same-block AMM spot price. A fork PoC borrows liquidity, moves the pool price, borrows against inflated collateral, unwinds, repays, and exits with positive profit while protocol debt is undercollateralized.

Expected decision:

- Reportable oracle/economic finding with flash-loan amplifier.
- Required proof: realistic liquidity/fees, call sequence, profit/loss, controls showing robust oracle/cap would block.

## Scenario 3 — Unchecked ERC20 return with stuck accounting

A reward claim calls `token.transfer()` but ignores `false`. Rewards are cleared even though no tokens transfer, causing user loss for a supported non-standard token.

Expected decision:

- Reportable unchecked external call if token is supported/in-scope and loss is measurable.
- Required proof: mock or real supported token behavior, before/after reward balance, failed transfer result.

## Scenario 4 — External call after finalized state with checked return

A withdrawal updates balances before calling a fixed non-upgradeable token, checks return/revert, and no callback or cross-function path can observe inconsistent state.

Expected decision:

- Not reportable.
- External call exists but is safely handled.

## Scenario 5 — Unprotected implementation initialization

An upgradeable implementation contract is not locked. A fork PoC initializes the implementation directly, but the proxy state and funds are unaffected and no function can selfdestruct or upgrade the proxy.

Expected decision:

- Usually not reportable or low severity unless implementation control affects proxy/funds.
- Required gate: show proxy/control/fund/freeze impact.

## Scenario 6 — Proxy reinitializer resets owner

A reinitializer callable through the proxy lets any user reset owner and call `upgradeTo` to a malicious implementation in a fork test.

Expected decision:

- Reportable upgradeability/access-control finding.
- Required proof: actor model, reinitializer call, owner change, upgrade execution, fund/control impact.

## Scenario 7 — Input validation weird value but harmless

A fee setter accepts `0` fee from governance, but zero fee is documented and does not break accounting or security invariants.

Expected decision:

- Not reportable.
- Weird or broad input is not a bug without invariant impact.

## Scenario 8 — Invalid config breaks collateral factor

A low-priv role can set collateral factor above 100%. A fork PoC opens an undercollateralized borrow and leaves protocol with bad debt.

Expected decision:

- Reportable input-validation/access-control/economic finding.
- Required proof: role boundary, invalid value, borrow sequence, bad debt calculation.

## Scenario 9 — OWASP label without exploit path

A report says “SC06 unchecked external call” because `.call` appears in source, but the return value is checked and failure reverts.

Expected decision:

- Reject as taxonomy-only false positive.
- OWASP mapping is secondary support, not impact proof.

## Scenario 10 — OWASP-aligned report with executable proof

A report maps an exploit to SC05/SC06/S3, includes Foundry fork test, attacker actor model, invariant before/after, quantified protocol loss, and false-positive gates.

Expected decision:

- Report-ready if scope and impact match program rules.
