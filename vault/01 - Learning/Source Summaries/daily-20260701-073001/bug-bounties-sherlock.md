---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.405259+00:00
source_quality: 5
classification: Web2 skill update
vulnerability_class: Authentication / Session
---

# Bug Bounties - Sherlock

- URL: `https://audits.sherlock.xyz/bug-bounties`
- Source group: `browser_dom_linked_resources`
- Content chars: `2357`
- Classification: **Web2 skill update**
- Vulnerability class: **Authentication / Session**

## Source summary

- Contests Leaderboards Bug Bounties Featured Help Center Connect Bug Bounties Largest Sherlock Bug Bounty Usual Labs Payout 16,000,000 USDC Most Recent Sherlock Bug Bounty Pinto Payout 5,000 USDC All Gaming Infrastructure Lending Stablecoins Tokenization Trading Yield Bounty Size Last Updated Usual Labs 16,000,000 USDC Payout Apr 8, 2025 Last Updated Usual - Fira UZR (Usual Zero Rate) module 7,500,000 USDC Payout Jan 16, 2026 Last Updated Aave V4 2,500,000 USD Payout May 18, 2026 Last Updated Flying Tulip 1,000,000 USDC Payout Jun 18, 2026 Last Updated Cap 1,000,000 USDC Payout Oct 24, 2025 Last Updated SYMMIO 808,808 USDC Payout Oct 30, 2024 Last Updated Paradex 500,000 USDC Payout Jun 8, 2026 Last Updated Fira Protocol 500,000 USDC Payout Apr 9, 2026 Last Updated Midas 500,000 USDC Payout May 19, 2026 Last Updated Sherlock 500,000 USDC Payout Aug 8, 2024 Last Updated Scroll 250,000 USDC Payout Apr 2, 2026 Last Updated Sport.Fun 250,000 USDC Payout Jun 2, 2026 Last Updated Satlayer 200,000 USDC Payout Feb 11, 2025 Last Updated Yearn 200,000 USDC Payout May 15, 2026 Last Updated Vesu 100,000 USDC Payout Jun 10, 2026 Last Updated USX 100,000 USDC Payout May 3, 2026 Last Updated Phoenix 100,000 USDC Payout Feb 3, 2026 Last Updated Inverse Finance 100,000 DOLA Payout Mar 30, 2026 Last Updated Mellow Core Vaults 100,000 USDC Payout Sep 25, 2025 Last Updated MetaLend 100,000 USDC Payout Dec 22, 2025 Last Updated Seamless Leverage Tokens 100,000 USDC Payout Oct 10, 2025 Last Updated Exactly 100,000 USDC Payout Nov 14, 2024 Last Updated 40acres Finance Update June 30th 50,000 USDC Payout Mar 25, 2026 Last Updated Napier 50,000 USDC Payout Aug 20, 2024 Last Updated Axis Finance 50,000 USDC Payout Aug 15, 2024 Last Updated Flat Money 50,000 USDC Payout Apr 16, 2025 Last Updated Alphix - Dec 2025 30,000 USDC Payout Feb 11, 2026 Last Updated Union 30,000 USDC Payout Nov 10, 2024 Last Updated Rujira 25,000 USDC Payout Jun 22, 2026 Last Updated Axal - TEE & Server 25,000 USDC Payout Aug 5, 2025 Last Updated Monolith Stablecoin Factory 20,000 DOLA Payout May 19, 2026 Last Updated Rubicon (rubicon.finance) 15,000 USDC Payout Aug 18, 2025 Last Updated Pinto 5,000 USDC Payout Jun 24, 2026 Last Updated

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
