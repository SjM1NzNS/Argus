---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.399705+00:00
source_quality: 5
classification: severity rule
vulnerability_class: Web3 General
---

# Research - The Immunefi Blog

- URL: `https://immunefi.com/blog/research`
- Source group: `browser_dom_linked_resources`
- Content chars: `1388`
- Classification: **severity rule**
- Vulnerability class: **Web3 General**

## Source summary

- Home Customers Whitehat Spotlight Security Guides Research Get Protected Research RESEARCH—43 POSTS The Ecosystem Vulnerability Scoreboard: 6 Years of DeFi Loss Data Immunefi maps six years of DeFi protocol losses across major ecosystems.
- RESEARCH Nearly Every Long-Running Bug Bounty Program on Immunefi Has Found a Critical Bug Five years of Immunefi data shows that 93.9% of bug bounty programs running 5+ years have surfaced a confirmed critical vulnerability.
- RESEARCH What an Onchain Hack Actually Costs: 2024-2025 Update An Immunefi research report on what a crypto exploit actually does to a protocol, beyond the stolen funds, based on five years of onchain in RESEARCH 93% of Critical Crypto Vulns Are Disclosed on Immunefi.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
