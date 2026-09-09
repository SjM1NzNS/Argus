---
type: eval-case
domain: web3
status: populated
name: oracle-manipulation-valid
expected_decision: "report"
created: ""
updated: "2026-06-29"
---

# Oracle Manipulation Valid

## Scenario

A lending market uses a thin AMM spot price for collateral. In a fork PoC, an unprivileged attacker flash-loan/manipulates pool price within realistic liquidity, borrows against inflated collateral, unwinds, and leaves bad debt. Profit/loss is quantified after fees.

## 1. Is this reportable?

Yes. The Oracles playbook requires realistic manipulation path, liquidity/cost assumptions, execution sequence, and measurable protocol impact.

## 2. What severity?

High/Critical if realistic capital path creates protocol loss/insolvency; Medium if constrained

## 3. What proof is missing?

Exact production liquidity assumptions, oracle update timing, slippage/fee model, and scope confirmation for deployed market.

## 4. What would triage reject?

Triage would reject if liquidity/capital assumptions are impossible or if robust feed/TWAP checks are bypassed unrealistically.

## 5. What is the next action?

Preserve fork state, transaction sequence, cost/profit calculation, and run Impact review.

## 6. Should Argus report, hold, or discard?

Decision: report.

## Expected Argus reasoning

The playbook allows realistic oracle-impact findings with proof.
