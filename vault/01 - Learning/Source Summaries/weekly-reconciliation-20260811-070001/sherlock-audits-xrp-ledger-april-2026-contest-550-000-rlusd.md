---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.100761+00:00
source_quality: 10
source_id: sherlock-audits
source_role: report_repository
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, false_positive_condition, reportability_criterion]
classification: Web2 skill update
vulnerability_class: Authentication / Session
---

# XRP Ledger - April 2026 Contest - 550,000 RLUSD

- URL: `https://audits.sherlock.xyz/contests/1260`
- Source ID / role / trust: `sherlock-audits` / `report_repository` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`browser_dom`, discovered-from=`https://audits.sherlock.xyz`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `browser_dom_linked_resources`
- Content chars: `412743`
- Classification: **Web2 skill update**
- Vulnerability class: **Authentication / Session**

## Source summary

- Details Scope Contest Results 2703 Issues 6 High 29 Medium 959 Invalid 857 MPT DEX BookStep uses the final Payment destination instead of the offer owner for input-side transfer-fee calculation H 0xastronatey 24,659 RLUSD 1242 Integer truncation in MPT input allows partially funded offers to be consumed for free M InfiniteSec 4,931 RLUSD 1636 PaymentBurn direct-step debt-direction mismatch allows source-issued IOU liability creation M Baazigar 4,931 RLUSD 1940 limitOut() MPT Rounding Causes False tecKILLED and AMM Bypass for Valid OfferCreate Trades M maigadoh 4,931 RLUSD 2668 MPT DEX/LendingProtocol arithmetic helpers throw `std::overflow_error` on extreme MPT/IOU amounts, escape `FlowException`-only handlers, surface as `tecINTERNAL` on DEX/payment paths; uncaught throw in `LoanPay::calculateBaseFee` terminates rippled M 6PottedL 4,931 RLUSD 2671 Co-signed TicketCreate without a Sponsorship object inflates the sponsorship's ReserveCount on consumption, converting a one-shot ticket grant into standing pre-funded reserve credits M 6PottedL 4,931 RLUSD 2706 Pathfinder constructor silently drops `srcAmount` after the MPT-DEX refactor, so `ripple_path_find` ranks paths with an unbounded source budget and returns suboptimal paths in `convert_all` mode M 6PottedL 4,931 RLUSD 775 MPT mulRatio Overflow Causes Payment Failure (tecINTERNAL) on Large Balances with Transfer Fee Um158057 2,465 RLUSD 879 Attacker will cause TxQ churn and liveness degradation for validator nodes 0x4non 2,465 RLUSD 914 MPT issuer will cause a crossed orderbook and block DEX pathfinding trades for token holders RustyLock 2,465 RLUSD 993 Batch makes same-Account `AccountTxnID` self-referential x15 2,465 RLUSD 1118 CheckCash still charges an extra reserve unit when auto-creating a destination's first free MPT holding sonanh08t4 2,465 RLUSD 1226 Any attacker will poison pathfinding and order-book listeners for XRPL node operators Thisisit 2,465 RLUSD 1374 Simulate underprices sponsor-multisigned transactions by sizing Fee before sponsor-signature autofill sonanh08t4 2,465 RLUSD 1414 ripple_path_find auto-source discovery counts dead MPT holdings toward max_auto_src_cur and aborts valid pathfinding sonanh08t4 2,465 RLUSD 1594 parseArray() Missing Element Name Validation Allows Hiding and Executing Non-Canonical Batch Inner Transactions InfiniteSec 2,465 RLUSD 1814 AMMDeposit skips LP trustline reserve for non-sponsored users, allowing under-reserve accounts t0x1c 2,465 RLUSD 1926 SponsorshipSet can succeed while leaving the grantor below its own reserve floor, creating a self-inflicted reserve lock and violating the expected post-transaction reserve invariant.
- Demonhatz 2,465 RLUSD 2027 CheckCash hard caps MPT DeliverMin at half of maxMPTokenAmount 0xBeastBoy 2,465 RLUSD 2193 ripple_path_find rejects valid sponsored account-creation routes sonanh08t4 2,465 RLUSD 2241 Delegated and sponsored transactions can be blocked from TxQ despite funded fee payers pkqs90 2,465 RLUSD 2278 Delegates can be blocked from authorized multisigned transactions pkqs90 2,465 RLUSD 2320 [Sponsored Fees and Reserves] LoanSet can apply a borrower reserve sponsor to lender-owned holdings and lock usable sponsor XRP unineko 2,465 RLUSD 2342 [Sponsored Fees and Reserves] Sponsored token EscrowFinish can falsely reject net-zero reserve recycling and lock escrowed funds unineko 2,465 RLUSD 2563 `account_currencies` omits current MPT send/receive assets even when live MPT transfers succeed sonanh08t4 2,465 RLUSD 2692 OfferCreate `flowCross` throws and returns `tecINTERNAL` for large MPT amounts with a non-zero transfer fee, because `mulRoundImpl` lacks the 128-bit Number fallback that `multiply` has 6PottedL 2,465 RLUSD 2712 `changeSpotPriceQuality` routes IOU(in)/MPT(out) AMM pools through the wrong-side anchoring path because the predicate only treats XRP as integer-precision 6PottedL 2,465 RLUSD 2781 OfferCreate throws uncaught division-by-zero (tefEXCEPTION) on a buy offer with a large MPT TakerPays and an IOU TakerGets when the IOU issuer has TickSize set 6PottedL 2,465 RLUSD 918 Holder deletes MPToken to permanently block AMMClawback for requireAuth MPTs H maigadoh 2,426 RLUSD 918 Holder deletes MPToken to permanently block AMMClawback for requireAuth MPTs H maigadoh 2,426 RLUSD 1004 AMMClawback can be vetoed by the target holder missing paired MPT object H destiny_rs 2,426 RLUSD 1932 MPT Clawback from AMM Permanently Blockable via MPToken Deletion + Single-Asset XRP Withdrawal H Demonhatz 2,426 RLUSD 2240 LPs can permanently block auth-gated MPT AMM clawback H pkqs90 2,426 RLUSD 2313 AMMClawback fails to create/authorize MPToken for holder as required by spec H 0xeix 2,426 RLUSD 2698 A holder who deposits a permissioned MPT into an AMM and then self-unauthorizes their MPToken permanently disables the issuer's AMMClawback path for that holder, stranding the issuer's asset in the pool H 6PottedL 2,426 RLUSD 792 [MPT DEX] `fixAMMClawbackRounding` causes MPT-leg zero/shortfall in partial `AMMClawback`, breaking clawback proportionality while returning `tesSUCCESS` M forsec 2,219 RLUSD 792 [MPT DEX] `fixAMMClawbackRounding` causes MPT-leg zero/shortfall in partial `AMMClawback`, breaking clawback proportionality while returning `tesSUCCESS` M forsec 2,219 RLUSD 2226 Silent Zero MPT Recovery in AMMClawback Roun
- Contests Leaderboards Bug Bounties Featured Help Center Connect Contests XRP Ledger - April 2026 XRP Ledger - April 2026 Finished Bug Bounty Contest The XRP Ledger (XRPL) is a decentralized layer 1 blockchain renowned for its decade-long reliability and stability in tokenizing and exchanging crypto-native and real-world assets.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, false_positive_condition, reportability_criterion`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
