---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.395807+00:00
source_quality: 8
classification: vulnerability pattern
vulnerability_class: Bridge / Proof Validation
---

# Rekt - <!-- -->Gravity Bridge - Rekt

- URL: `https://rekt.news/gravity-bridge-rekt`
- Source group: `daily_deep_content`
- Content chars: `18125`
- Classification: **vulnerability pattern**
- Vulnerability class: **Bridge / Proof Validation**

## Source summary

- Gravity Bridge, the Ethereum-Cosmos corridor and decentralized alternative to multisig bridges , was drained on May 29th in a denom mapping exploit.
- The attacker minted worthless tokens on Osmosis, embedded real Ethereum custody addresses inside a fabricated denom string, and called a permissionless function that the bridge accepted without question.
- Using the an address on Osmosis, the attacker created four fake tokens , one mirroring each real asset sitting in Gravity Bridge's Ethereum custody: USDC, USDT, WETH, and PAXG.

## Extracted methodology

- Affected surface: Bridge, rollup, proof verification, or settlement boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
