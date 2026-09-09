---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.393922+00:00
source_quality: 8
classification: vulnerability pattern
vulnerability_class: Bridge / Proof Validation
---

# Rekt - <!-- -->Aztec Bridge - Rekt

- URL: `https://rekt.news/aztec-bridge-rekt`
- Source group: `daily_deep_content`
- Content chars: `16243`
- Classification: **vulnerability pattern**
- Vulnerability class: **Bridge / Proof Validation**

## Source summary

- Aztec Bridge - Rekt Wednesday, June 24, 2026 Aztec Connect - Aztec Labs - Rekt read this article also in : On June 14th, an attacker drained $2.28 million from a deprecated Aztec Connect contract that Aztec Labs had wound down in 2023 and handed back the admin keys on in 2024 , exploiting a mismatch between the ZK proof verification layer and the L1 settlement logic.
- The exploit came from a mismatch between the verified rollup transaction set and the L1 settlement processing boundary. numRealTxs was not effectively bound to the transaction set enforced by the proof , so the proof path and the L1 settlement logic interpreted the transaction list differently.
- The read was careful and restrained : A call to escapeHatch() on the Private Rollup Bridge contract , 1,158 ETH to the caller, no reverts, no unusual internal flows, the proof package went through.

## Extracted methodology

- Affected surface: Bridge, rollup, proof verification, or settlement boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
