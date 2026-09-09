---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.394556+00:00
source_quality: 8
classification: severity rule
vulnerability_class: Bridge / Proof Validation
---

# Rekt - <!-- -->Aztec Connect - Rekt

- URL: `https://rekt.news/aztec-connect-rekt`
- Source group: `daily_deep_content`
- Content chars: `20746`
- Classification: **severity rule**
- Vulnerability class: **Bridge / Proof Validation**

## Source summary

- BlockSec Phalcon flagged the same transaction independently : Identifying the root cause as a mismatch between the verified rollup transaction set and the L1 settlement processing boundary, numRealTxs was not effectively bound to the transaction set enforced by the ZK proof, allowing the proof verification path and the settlement logic to interpret the transaction list differently.
- The attacker found a gap between two systems that were supposed to be talking to each other but weren't bound together, a ZK proof that verified one transaction set, and a settlement layer that executed against a different one .
- The following morning, a second attacker returned to the same vulnerability , submitting 14 more rollup calls across a fresh wallet and sweeping the residual DeFi bridge positions the first drain had left behind, another ~$88K gone before the day was out.

## Extracted methodology

- Affected surface: Bridge, rollup, proof verification, or settlement boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
