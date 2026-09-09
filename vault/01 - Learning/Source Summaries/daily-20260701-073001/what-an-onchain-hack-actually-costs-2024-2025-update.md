---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.399246+00:00
source_quality: 6
classification: Web3 skill update
vulnerability_class: AI / LLM Security
---

# What an Onchain Hack Actually Costs: 2024-2025 Update

- URL: `https://immunefi.com/blog/research/what-an-onchain-hack-actually-costs-2024-2025-update`
- Source group: `browser_dom_linked_resources`
- Content chars: `13308`
- Classification: **Web3 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- That work introduced Amador's Hack Impact Estimate, a framework for measuring exploit damage well beyond the headline theft figure.
- Home Customers Whitehat Spotlight Security Guides Research Get Protected What an Onchain Hack Actually Costs: 2024-2025 Update Copy Copied 25 Mar 2026 • 8 min read What an Onchain Hack Actually Costs: 2024-2025 Update Immunefi An Immunefi research report on what a crypto exploit actually does to a protocol, beyond the stolen funds, based on five years of onchain incident data.
- Updated hack impact estimate for 2024-2025: A protocol hacked today should expect to lose roughly $25,000,000 USD in direct theft, see its token shed 61% of its value over the next six months, and face sustained price depression that 84% of hacked tokens never recover from within that window.

## Extracted methodology

- Affected surface: Web3 protocol / smart contract
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
