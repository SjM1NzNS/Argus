---
type: eval-scenarios
status: active
created: "2026-07-24"
source: "Code4rena Jupiter Lend M-01 via Solodit"
---

# Transformed numeric safety-bound eval scenarios

## Scenario 1 — source cap exceeds downstream fixed-point domain

A lending protocol caps an oracle-derived debt/collateral ratio below the raw integer maximum. After decimal scaling into a fixed-point library, reachable extreme-market values below the configured cap exceed the library's accepted maximum and revert liquidation and health checks.

- **Reportable:** Yes, after executable local/fork proof.
- **Severity:** Medium candidate; raise only with quantified realistic bad debt or insolvency.
- **Missing proof:** Reachable market state, exact first-reverting boundary, liquidation/health-path trace, affected assets/positions, and bad-debt or freeze impact.
- **Triage rejection risk:** Constant mismatch without reachable state or impact.
- **Next action:** Test normal, `max_safe - 1`, `max_safe`, `max_safe + 1`, and configured-cap values across every sibling consumer.
- **Decision:** HOLD until impact proof; REPORT when liveness and economic impact are demonstrated.

## Scenario 2 — inverse path is safe but direct-ratio path reverts

A developer selected a cap by checking an inverse-price conversion. A second path consumes the direct ratio with different scaling and a tighter domain bound.

- **Reportable:** Yes if the second path is reachable and safety-critical.
- **Severity:** Medium candidate when liquidation/recovery is disabled; otherwise Low/hold.
- **Missing proof:** Consumer-by-consumer derivation and execution showing the exact divergence.
- **Triage rejection risk:** Treating one algebraic calculation as proof that deployed code reaches the failing path.
- **Next action:** Derive admissible input intervals independently for inverse and direct consumers; assert intermediate values and final state.
- **Decision:** REPORT only the consumer proven to fail; do not generalize to all math paths.

## Scenario 3 — out-of-range value fails closed without disabling recovery

Values beyond the supported economic range are rejected before mutation, while liquidation, repay, withdrawal, and bad-debt handling remain available through a bounded fallback or explicit terminal state.

- **Reportable:** No.
- **Severity:** None.
- **Missing proof:** None if recovery-path controls pass.
- **Triage rejection reason:** Correct fail-closed validation with preserved safety-critical liveness.
- **Next action:** Preserve as a negative control.
- **Decision:** DISCARD.

## Scenario 4 — only an impossible test state reaches the boundary

The first failing value requires impossible oracle decimals, an unlistable asset, or a price outside every reachable feed/configuration bound.

- **Reportable:** No under current deployment assumptions.
- **Severity:** Informational hardening at most.
- **Missing proof:** A realistic route to the state.
- **Triage rejection reason:** Unreachable configuration/test artifact.
- **Next action:** Confirm deployment constraints and document them.
- **Decision:** DISCARD or WATCHLIST if configuration can change.
