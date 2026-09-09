---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.406143+00:00
source_quality: 6
classification: severity rule
vulnerability_class: Authentication / Session
---

# Centrifuge Protocol V3.1 Contest - 320,000 USDC

- URL: `https://audits.sherlock.xyz/contests/1028`
- Source group: `browser_dom_linked_resources`
- Content chars: `94683`
- Classification: **severity rule**
- Vulnerability class: **Authentication / Session**

## Source summary

- H asui - 549 Any user can inflate the share price when SimplePriceManager is used M Audittens $2,589 549 Any user can inflate the share price when SimplePriceManager is used M Audittens $2,589 576 User can inflate share price by not claiming his redeem, causing potential permanent fund loss M 6PottedL $2,589 673 Asynchronous Redeem Flow Creates Transient Share Price Inflation Exploitable by User-Controlled Withdrawal Delay M Cybrid $2,589 712 Prices computed in SimplePriceManager is off even after `BatchRequestManager#revokeShares()` is called M 0xpiken $2,589 926 Redemption withdrawals can be DOSed causing inflation of share prices M LeFy $2,589 942 Incorrect price update for redeems causes loss of funds for new depositors M TessKimy $2,589 77 Rounding residual cancels freeze batch request queue M x15 $571 77 Rounding residual cancels freeze batch request queue M x15 $571 187 Incorrectly handled subtraction leads to underflow resulting in permanent user fund lock and DOS M anonymousjoe $571 233 Any caller processing notifyDeposit/notifyRedeem will lock investors' funds by triggering an underflow in queued-cancel processing after partial approvals M hassan-truscova $571 424 A large depositor/redeemer will permanently lock small users’ deposits and redeems M jongwon $571 527 Global pending amounts invariant violation in `BatchRequestManager::_claimDeposit()` functions M blockace $571 647 Unrecoverable Share Token Due to Precision Loss in Batch Request Manager M Bobai23 $571 755 User deposit rounding leaves pending requests stuck M HeckerTrieuTien $571 792 Accounting mismatch on `BatchRequestManager` due to precision loss M TessKimy $571 803 Rounding in Redemption Claims Causes Permanent Loss of Uncla
- Built on immutable smart contracts, it enables permissionless deployment of customizable tokenization products.
- Show more Details Scope Contest Results 860 Issues 1 High 9 Medium 809 Invalid 397 Stranded ETH on batched `crosschainTransferShares` call M gh0xt $26,313 512 Inadequate gas reservation in `Gateway.handle()` try-catch block enables permanent DOS via batch-level gas exhaustion M 0x52 $26,313 560 `Gateway.withBatch()` lacks message count validation enabling permanent DOS via an excessive number of messages in a batch M 0x52 $26,313 635 Malicious adapters can exploit message batching via adapter-side reentrancy to cause message loss for any other pool M 0x52 $26,313 984 `MessageProcessor` fails to disable `unpaidMode` during `UntrustedContractUpdate` execution enabling permanent DOS via malicious unpayable batch creation M 0x52 $26,313 714 Gas engineering during `adapter` execution can be used to maliciously split critical message batches M 0x52 $7,104 714 Gas engineering during `adapter` execution can be used to maliciously split critical message batches M 0x52 $7,104 766 Unrestricted Access Allows Forcing Axelar Messages Into Retry Queue M typicalHuman $7,104 894 Axelar execution can be DoSed M 0xeix $7,104 3 Cross-chain share price updates revert due to unfunded batching M Ziusz $3,452 3 Cross-chain share price updates revert due to unfunded batching M Ziusz $3,452 359 `SimplePriceManager.onUpdate()` lack of forward execution fee leads dependent functions to revert M harry $3,452 434 Non-payable functions make new contracts' functions broken M bbl4de $3,452 662 Core Valuation Function (`setPrice`) Reverts Due to Unfunded Gateway Call M Cybrid $3,452 718 Calls Revert Due to Lack of Adapter Gas Fee M Tenalia-Audits $3,452 227 Missing check in approvedDeposits() in AsyncRequestManager.sol allows any pool manager to drain other pools H anonymousjoe $3,440 227 Missing check in approvedDeposits() in AsyncRequestManager.sol allows any pool manager to drain other pools H anonymousjoe $3,440 274 Malicious BRM permits global escrow drain H gh0xt $3,440 312 Missing validation in approvedDeposits() in AsyncRequestManager.sol allows any pool manager to drain other pools H anonymousjoe - 320 Missing check in fulfillDepositRequest() in AsyncRequestManager.sol allows any pool manager to drain other pools H anonymousjoe - 418 Vault Router Escrow funds can be stolen by any pool manager H skybluescar $3,440 483 Any pool manager can drain global escrow H skybluescar - 548 Pool manager will steal unapproved deposits of other pools H Audittens $3,440 577 Lack of input validation with custom Hub Request Manager permits Spoofing of messages which cause drains of all Funds from Global Escrow H 6PottedL $3,440 581 Switch of Spoke Request Managers whilst state is pending results in payload spoofing, which results in loss of all Funds held in Global Escrow.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
