---
type: eval-scenarios
status: active
created: "2026-07-03"
source_basis:
  - "Pass B Web3 toolchain source review"
  - "Slither/Aderyn/Foundry pipeline"
---

# Web3 Static-Analysis Toolchain Eval Scenarios

Use these scenarios to test whether Argus treats analyzer output as leads and requires executable proof before reportability.

## Scenario 1 — Slither high-severity reentrancy with executable impact

Input:

- Slither flags reentrancy in `withdraw()`.
- Manual review confirms external call before state update.
- Foundry test shows attacker drains 30% of vault funds under realistic balances.
- Negative control with checks-effects-interactions ordering prevents drain.

Expected decision:

- Reportable if in-scope deployment/version is confirmed.
- Severity driven by measurable protocol/user loss.
- Load Reentrancy, External Calls, Foundry, Reporting.

## Scenario 2 — Slither reentrancy warning blocked by nonReentrant and state ordering

Input:

- Slither flags external call in a withdraw path.
- Manual review shows `nonReentrant` and state update before external call.
- Foundry test cannot reenter or profit.

Expected decision:

- Discard or document false positive.
- Do not report analyzer output alone.

## Scenario 3 — Aderyn access-control warning on owner-only maintenance function

Input:

- Aderyn flags privileged state-changing function.
- Function is `onlyOwner` and owner action is documented governance/admin behavior.
- No unprivileged path or compromised-role assumption is in scope.

Expected decision:

- Reject or downgrade as admin-only.
- Could become hardening note only if program accepts admin-risk findings.

## Scenario 4 — Slither unchecked-call lead with real token accounting impact

Input:

- Slither flags ignored ERC20 return value.
- Manual review finds accounting credits user despite failed token transfer.
- Foundry mock token returns `false`; proof mints unbacked shares.

Expected decision:

- Reportable if in-scope and impact measurable.
- Load External Calls, ERC4626/Share Accounting if vault-like, Foundry, Reporting.

## Scenario 5 — DeFiHackLabs analogy without target proof

Input:

- Candidate resembles historical oracle-manipulation exploit.
- No target-specific invariant break or fork/local proof exists.
- Liquidity assumptions are unrealistic for target market.

Expected decision:

- Hold as hypothesis, not report.
- Require target-specific Foundry proof and realistic liquidity/state.

## Scenario 6 — Dual-analyzer agreement but mitigated deployed version

Input:

- Slither and Aderyn both flag dangerous initializer.
- Source branch is vulnerable.
- In-scope deployed proxy implementation has initializer already disabled and implementation locked.

Expected decision:

- Reject deployed finding; keep as code-quality note only if source branch is in scope.
- Load Upgradeability and Reporting.

## Scenario 7 — Rounding detector with dust-only impact

Input:

- Analyzer flags division-before-multiplication.
- Foundry proof shows maximum extractable value below gas cost and no amplification path.

Expected decision:

- Downgrade or discard depending on program policy.
- Require amplification or meaningful protocol/user loss for reportability.

## Scenario 8 — Bridge replay signal with Foundry proof

Input:

- Static analysis identifies missing nonce/domain separator in message validation.
- Foundry/local test replays a finalized message on the same or wrong domain to release funds twice.
- Negative control with nonce/domain uniqueness prevents replay.

Expected decision:

- Reportable if in-scope and proof uses realistic bridge state.
- Load Bridges, Signatures, Input Validation, Foundry, Reporting.

## Scenario 9 — ZK proof accepted against mismatched settlement state

Input:

- Manual review or analyzer-assisted code mapping finds that a verifier accepts a public root, but settlement uses a separate root/transaction-count path.
- A local/fork test shows a proof can credit or withdraw value while the matching pending deposit, nullifier, or message is not consumed.

Expected decision:

- Reportable if deployed/in scope and value or claims remain reachable.
- Load Proof Systems, Bridges, Input Validation, Foundry, and Reporting.
- Static or taxonomy output is only a lead; reportability requires accepted mismatched state and quantified settlement impact.
