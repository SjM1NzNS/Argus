---
type: eval-scenarios
status: active
created: "2026-07-04"
source_basis:
  - "Daily promotion 2026-07-04: BlockSec June 2026 incident lessons"
---

# Web3 Proof Systems and Automation Eval Scenarios — Daily 2026-07-04

Use these scenarios to check whether Argus promotes proof-system, approval-consumption, and wallet-signing lessons without over-reporting source material alone.

## Scenario 1 — Valid proof bound to wrong settlement root

Input:

- A rollup/bridge proof verifies successfully.
- The private witness membership root is not constrained to the public root used by L1 settlement.
- A local/fork proof shows the attacker withdraws value backed by a fake private tree while settlement consumes the real public root.

Expected decision:

- Reportable if the deployment/version is in scope and value/claims remain reachable.
- Load Proof Systems, Bridges, Input Validation, Foundry, and Reporting.
- Required proof: mismatched root path, transaction sequence, positive/negative controls, and quantified unbacked withdrawal or double-spend impact.

## Scenario 2 — Proof taxonomy label with no mismatched state

Input:

- A report says the circuit may have weak constraints because it is a ZK rollup.
- Review shows public inputs, witness membership, nullifier, transaction count, asset, recipient, and domain are all bound before settlement.
- No transaction or local proof demonstrates unauthorized settlement.

Expected decision:

- Reject as taxonomy-only speculation.
- Keep as a checked lead only if a concrete binding gap is later identified.

## Scenario 3 — Bot simulation trusts fake wrapper allowance behavior

Input:

- A strategy/bot/protocol integration treats a wrapper or pool as trusted because events and simulated profit look correct.
- A local mock wrapper omits underlying `transferFrom()` allowance consumption while still returning apparent profit.
- Residual approvals can later be harvested by the wrapper/spender.

Expected decision:

- Reportable only if the target system is in scope and the attacker can cause unauthorized asset movement or residual approval drain.
- Required proof: spender identity, allowance before/after, missing consumption, residual approval cleanup failure, and asset-loss sequence.

## Scenario 4 — Deterministic public-only wallet signing nonce

Input:

- A wallet or signing library derives the signing nonce from only public transaction/message data and omits the required secret prefix/entropy.
- Two public signatures or one signature plus public inputs allow recovery of the private key in a local proof.

Expected decision:

- Critical report if the affected wallet/signing path is in scope and deployed to users.
- Load Signatures and Reporting.
- Required proof: vulnerable version, nonce derivation path, local key-recovery demonstration using non-production test keys, and affected actor/asset impact.

## Scenario 5 — Standard audited signing library with secret nonce input

Input:

- A wallet uses a standard audited Ed25519/ECDSA library.
- Nonce derivation includes required secret input or randomness, and tests cannot recover the key from public signatures.

Expected decision:

- Not reportable.
- Do not infer key compromise from custom-crypto concern alone.

## Scenario 6 — Out-of-range committee defaults to a BLS identity key

Input:

- A permissionless pull-oracle update accepts a caller-supplied committee ID.
- An out-of-range ID returns an all-zero/default public key; an all-zero signature and key satisfy the pairing equation as identity elements.
- A local/fork control shows the malformed update changes an owned test asset's consumed price, while a patched wrapper rejects the ID and identity inputs before the precompile.

Expected decision:

- Reportable verifier/oracle input-validation failure when the deployed in-scope path can affect borrow, liquidation, mint, redeem, or other value-bearing state.
- Load Proof Systems, Oracles, Input Validation, External Calls, Foundry, and Reporting.
- Required proof: lookup range, exact key/signature encoding, call-level and semantic return values, valid non-zero positive control, one-variable negative controls, before/after oracle state, and quantified economic impact.
- Reject or downgrade if the wrapper fails closed, equivalent checks occur before state mutation, the path is unreachable/deprecated with no value at risk, or only the precompile's mathematically correct result is shown without unauthorized state change.

Source: https://rekt.news/bonzo-finance-rekt
