---
type: learning-source-summary
compiled_at: 2026-06-30T12:02:12.842173+00:00
source_quality: 5
classification: severity rule
vulnerability_class: Accounting / Invariants
---

# Immunefi Crypto Losses April 2025 Report

- URL: `https://immunefi.com/blog/research/immunefi-crypto-losses-april-2025-report`
- Source group: `browser_dom_linked_resources`
- Content chars: `3728`
- Classification: **severity rule**
- Vulnerability class: **Accounting / Invariants**

## Source summary

- Fraud Analysis In April 2025, hacks continued to be the predominant cause of losses compared to fraud, accounting for 100% of the total losses.
- Share on or Copy Copied RESEARCH YOU MIGHT ALSO LIKE The Ecosystem Vulnerability Scoreboard: 6 Years of DeFi Loss Data 12 min read Nearly Every Long-Running Bug Bounty Program on Immunefi Has Found a Critical Bug 8 min read What an Onchain Hack Actually Costs: 2024-2025 Update 8 min read

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
