---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.408340+00:00
source_quality: 6
classification: severity rule
vulnerability_class: Authentication / Session
---

# Uniswap Labs / uniswap-v4 competition | Cantina

- URL: `https://cantina.xyz/competitions/e2cf6906-ec8b-4c78-a585-74ac90615659`
- Source group: `browser_dom_linked_resources`
- Content chars: `10892`
- Classification: **severity rule**
- Vulnerability class: **Authentication / Session**

## Source summary

- Opportunities Leaderboard Discover Cantina Log in Sign up uniswap-v4 @uniswap Completed Instructions Leaderboard Total reward $2,350,000 No deposit required Status Completed Findings submitted 451 Start date 6 Sep 2024 End date 1 Oct 2024 The Uniswap protocol is a peer-to-peer system designed for exchanging cryptocurrencies (ERC-20 Tokens) on the Ethereum blockchain.
- The protocol is implemented as a set of persistent, non-upgradable smart contracts; designed to prioritize censorship resistance, security, self-custody, and to function without any trusted intermediaries who may selectively restrict access.
- Please note there must be sufficient information and undeniable Proof of concept which should be easily verifiable for the loss amount for the finding to be considered Critical with absolutely no ambiguity.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
