---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.399484+00:00
source_quality: 5
classification: Web3 skill update
vulnerability_class: Web3 General
---

# Customers - The Immunefi Blog

- URL: `https://immunefi.com/blog/customers`
- Source group: `browser_dom_linked_resources`
- Content chars: `1528`
- Classification: **Web3 skill update**
- Vulnerability class: **Web3 General**

## Source summary

- Home Customers Whitehat Spotlight Security Guides Research Get Protected Customers CUSTOMERS—38 POSTS Immunefi and Ripple Announce $200,000 Attackathon to Secure Proposed XRPL Lending Protocol Ripple and Immunefi are collaborating to launch a $200,000 Attackathon to secure the proposed XRPL Lending Protocol as part of the instituti CUSTOMERS VeChain launches a $200K Attackathon on Immunefi to secure the Hayabusa Upgrade VeChain has partnered with Immunefi to launch an Attackathon focused on one of the most significant blockchain upgrades of the year: the Hay CUSTOMERS Virtuals Protocol Launches a $200,000 Bug Bounty Program on Immunefi Virtuals Protocol has launched a $200,000 Bug Bounty Program on Immunefi, reinforcing its commitment to securing its ecosystem and protectin CUSTOMERS Injective Launches a $500,000 Bug Bounty Program on Immunefi Injective has launched a $500,000 Bug Bounty Program on Immunefi!
- They’re building a lightning-fast interoperable Layer 1 blockchain to po CUSTOMERS Baanx Launches $50,000 Bug Bounty Program on Immunefi Baanx has launched a $50,000 Bug Bounty Program on Immunefi, inviting security researchers to help secure its smart contracts, as well as its web and mobile applications.
- CUSTOMERS Immunefi and Plume Network Partner to Secure the Modular Future of DeFi We’re thrilled to announce our latest mainnet Attackathon in collaboration with Plume Network, the first modular blockchain built specifically for real-world asset (RWA) tokenization.

## Extracted methodology

- Affected surface: Web3 protocol / smart contract
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
