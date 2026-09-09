---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.407095+00:00
source_quality: 5
classification: Web3 skill update
vulnerability_class: Web3 General
---

# Opportunities | Cantina

- URL: `https://cantina.xyz/opportunities/ended`
- Source group: `web3_continuous_monitoring`
- Content chars: `1567`
- Classification: **Web3 skill update**
- Vulnerability class: **Web3 General**

## Source summary

- Opportunities Leaderboard Discover Cantina Log in Sign up Opportunities Take part in the industry's biggest security events.
- Payouts available $64.5M Total paid out $51.1M Vulnerabilities found 7,419 Researchers 17,579 All 53 Bounties 52 Competitions 1 Ended 142 eigenlayer-contracts Eigenlayer $2,500,000 in USDC Competition Completed Ended on 28 Mar 2025 uniswap-v4 Uniswap Labs $2,350,000 in USDC Competition Completed Ended on 1 Oct 2024 High Signal.
- The most innovative and familiar platform for competitive code review.

## Extracted methodology

- Affected surface: Web3 protocol / smart contract
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
