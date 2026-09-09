---
type: learning-source-summary
compiled_at: 2026-06-30T12:02:12.842853+00:00
source_quality: 6
classification: Web3 skill update
vulnerability_class: Accounting / Invariants
---

# Immunefi Crypto Losses Q1 2025 Report

- URL: `https://immunefi.com/blog/research/immunefi-crypto-losses-q1-2025-report`
- Source group: `browser_dom_linked_resources`
- Content chars: `9746`
- Classification: **Web3 skill update**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- Total Losses: $1.6B Bybit: $1.46B Phemex, $69.1 Million On January 23, 2025, the Singapore-based cryptocurrency exchange Phemex suffered an exploit, resulting in over $69 million in losses drained from its hot wallets.
- Crypto Losses in Q1 2025 Key Takeaways in Q1 2025 The 2 major exploits of the quarter totaled $1.52 billion alone, accounting for 94% of all losses in Q1 2025.
- Overview As of March 2025, nearly $100 billion in capital was locked across Web3 protocols.

## Extracted methodology

- Affected surface: Web3 protocol / smart contract
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
