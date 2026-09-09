---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.395158+00:00
source_quality: 8
classification: vulnerability pattern
vulnerability_class: Access Control / Admin Key
---

# Rekt - <!-- -->DxSale - Rekt

- URL: `https://rekt.news/dxsale-rekt`
- Source group: `daily_deep_content`
- Content chars: `19823`
- Classification: **vulnerability pattern**
- Vulnerability class: **Access Control / Admin Key**

## Source summary

- DxSale - Rekt Tuesday, June 2, 2026 DxSale - Admin Privileges - Rekt read this article also in : Nine months of patience, one admin key and $7.3 million gone .
- GoPlus put the primary drain at $7.3M and flagged that three additional locker contracts , whose ownership had also been transferred to the same attacker address, held an estimated $15.5M still at risk .
- Using owner privileges and EIP-7702 batch delegation , they unlocked and drained more than 1,400 liquidity pools on BNB Chain in a single coordinated flow .

## Extracted methodology

- Affected surface: Object, tenant, account, or authorization boundary
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
