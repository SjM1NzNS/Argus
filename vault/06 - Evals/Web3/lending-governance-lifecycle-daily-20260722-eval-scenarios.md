---
type: eval-scenarios
domain: web3
classes: [lending, governance]
created: "2026-07-22"
source_basis:
  - "https://blocksec.com/blog/web3-security-barnbridge-defituna-exploits"
---

# Lending and governance lifecycle eval scenarios — daily 2026-07-22

## Scenario 1 — dust truncates to zero while debt remains

A leveraged position holds a positive dust amount that rounds to zero in quote-value units. Debt is non-zero, but a special `total == 0` branch returns healthy.

- Reportable: yes, after executable target-specific proof.
- Severity: high/critical only when realistic state produces measurable bad debt or protocol loss.
- Missing proof: exact rounding boundary, accepted state transition, realistic liquidity/capital, debt delta, and local/fork loss assertion.
- Triage rejection reason: reject if another enforced layer blocks borrowing/settlement or the branch is unreachable.
- Next action: run normal-value, exact-zero, and dust-to-zero controls with identical debt.
- Decision: hold until executable economic proof.

## Scenario 2 — checked pool differs from executed route

A protocol checks its canonical pool against an oracle, then executes caller-supplied aggregator accounts through a different low-liquidity pool without a minimum output derived from debt/oracle value.

- Reportable: yes, if the route mismatch enables an undercollateralized position or loss.
- Severity: based on reproducible bad debt/loss, not route control alone.
- Missing proof: route/account binding, hostile-pool feasibility, post-swap output, health result, and protocol loss.
- Triage rejection reason: reject if aggregator validation, mint/account constraints, post-swap valuation, or slippage bounds constrain the actual route.
- Next action: compare normal route, hostile route, and route-bound/min-output negative control.
- Decision: hold until local/fork invariant break.

## Scenario 3 — deprecated governance remains executable with value at risk

A retired protocol still exposes proposal and execution authority over a module with residual user approvals. An unprivileged actor can satisfy the documented vote path and execute a payload that transfers approved assets.

- Reportable: candidate if current scope includes the deployed module and the actor gains incremental transfer/control capability.
- Severity: based on safely proven consumable value at risk.
- Missing proof: current callable state, vote/threshold path, exact payload, approval/balance provenance, and local/fork or complete on-chain trace.
- Triage rejection reason: do not reject merely because the protocol is deprecated; reject if scope excludes it or authority/value is absent.
- Next action: inventory governor/timelock/executor targets and quantify residual balances/allowances without consuming production assets.
- Decision: hold until authority and value-at-risk proof.

## Scenario 4 — genuinely retired governance

The old governor is permanently disabled, executors and roles are revoked, targets reject old-module calls, balances are zero, and no usable approvals remain.

- Reportable: no.
- Severity: none.
- Missing proof: none after current-state and negative-call controls.
- Triage rejection reason: no executable authority or value at risk.
- Next action: preserve the retirement evidence and close the branch.
- Decision: discard.
