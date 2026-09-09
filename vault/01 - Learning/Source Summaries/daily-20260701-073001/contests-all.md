---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.405470+00:00
source_quality: 5
classification: Web2 skill update
vulnerability_class: Web2 General
---

# Contests - All

- URL: `https://audits.sherlock.xyz/connect`
- Source group: `browser_dom_linked_resources`
- Content chars: `1292`
- Classification: **Web2 skill update**
- Vulnerability class: **Web2 General**

## Source summary

- Contests Leaderboards Bug Bounties Featured Help Center Connect Contests All 299 Active 1 Upcoming Judging Contests 1 Escalations Open Sherlock Judging 1 Finished 296 Order by End Date DRE App - dreUSD Judging Contest 60,000 USDC Rewards Jun 17, 05:00 PM Start Date Progress: 94% XRP Ledger - April 2026 Sherlock Judging 550,000 RLUSD Rewards Apr 13, 05:00 PM Start Date Apr 27, 06:30 PM End Date Ethereum Fusaka Upgrade Finished 2,000,000 USDC Rewards Sep 15, 05:00 PM Start Date Oct 13, 05:00 PM End Date MakerDAO Endgame Finished 1,388,500 DAI Rewards Jul 8, 05:00 PM Start Date Aug 5, 05:00 PM End Date Optimism Finished 720,000 USDC Rewards Jan 23, 04:00 PM Start Date Feb 6, 04:00 PM End Date Optimism Fault Proofs Finished 500,000 USDC Rewards Mar 27, 04:00 PM Start Date Apr 4, 05:00 PM End Date Babylon Chain Launch (Phase-2) Finished 375,000 USDC Rewards Feb 4, 04:00 PM Start Date Mar 4, 04:00 PM End Date Aave V4 Finished 365,000 USDC Rewards Dec 1, 04:00 PM Start Date Jan 12, 04:00 PM End Date Centrifuge Protocol V3.1 Finished 250,000 USDC Rewards Oct 20, 05:00 PM Start Date Nov 17, 04:00 PM End Date Notional V3 Finished 310,000 USDC Rewards Mar 27, 05:00 PM Start Date May 15, 05:00 PM End Date

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
