---
type: eval-scenarios
status: active
created: "2026-07-05"
source_basis:
  - "Daily promotion 2026-07-05: Solodit/Cyfrin Accountable findings"
---

# Web3 Vault Accounting and Lifecycle Eval Scenarios — Daily 2026-07-05

Use these scenarios to check whether Argus distinguishes reportable vault accounting/lifecycle failures from gas-only or hardening observations.

## Scenario 1 — Accrued penalties compound unintentionally

Input:

- A vault strategy computes a late penalty from `_totalAssets`.
- `_totalAssets` includes `accruedPenalties`.
- Accrual runs through common hooks such as borrow, repay, NAV/rate publish, deposit, mint, and redeem.
- A local test shows two equivalent time periods produce different total penalties depending only on how often hooks are called, and users are overcharged against the stated simple-interest model.

Expected decision:

- Reportable if deployed/in-scope and the overcharge or accounting distortion is measurable.
- Load Share Accounting, ERC4626/Vaults, Rounding & Precision, State Machines when lifecycle hooks are involved, and Reporting.
- Required proof: expected formula, actual formula, call-frequency control, before/after balances, actor path, and quantified user/protocol impact.

## Scenario 2 — Duplicate totalSupply read is only gas optimization

Input:

- A function calls a helper that reads `totalSupply` and then reads `totalSupply` again before any shares are minted.
- The repeated read returns the same value.
- No balance, share, price, or state transition changes; only gas use changes.

Expected decision:

- Not reportable as a security bug in normal bounty programs.
- Record as gas/hardening only if the program accepts optimization findings.
- Reject escalation unless the redundant read creates stale-data behavior, reentrancy exposure, or economic/state impact.

## Scenario 3 — Empty epoch passes into non-terminal stuck state

Input:

- Users cancel every request in an open deposit epoch, reducing `pendingCount` to zero while the epoch remains `Open`.
- A keeper/NAV update or force-pass path moves the empty epoch to `Passed`.
- Finalization to `Settled` only occurs inside `settle` or `refund`, but no pending requests remain to trigger those paths.
- A local test shows funds, shares, claims, or further lifecycle progress are blocked.

Expected decision:

- Reportable lifecycle/state-machine issue if an accepted actor can trigger it and impact is more than cosmetic.
- Load State Machines, ERC4626/Vaults, Input Validation, and Reporting.
- Required proof: state graph, transaction sequence, `pendingCount` and status before/after, reachability analysis, and quantified locked-fund/protocol-blocking impact.

## Scenario 4 — Empty epoch finalizes safely through recovery path

Input:

- The same all-cancelled epoch can become `Passed`, but a public keeper or documented recovery function finalizes it to `Settled` without loss.
- No funds or claims are stuck and later deposits/withdrawals proceed normally.

Expected decision:

- Not reportable or low-priority hardening.
- Record the recovery path as a negative control.

## Scenario 5 — Lifecycle issue requires excluded admin misuse

Input:

- Only a trusted owner can force an epoch into a bad state.
- The program excludes owner/governance centralization and no unprivileged or low-privileged route reaches the transition.

Expected decision:

- Usually not reportable.
- Downgrade unless the admin role is in-scope, compromised by another bug, or the contract promises trust-minimized safety against that role.
