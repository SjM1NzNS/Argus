# Web3 AMM Fee Split-Proofness and Stateful Differential Testing

Use this reference when reviewing AMM/DEX fee instructions, especially wrapper-style VM programs, heterogeneous token decimals, exact-in/exact-out paths, or post-audit arithmetic changes.

## 1. Prove scoped reachability before building a PoC

Repositories may contain more instructions than the bounty-scoped router dispatches. Before promoting a fee or AMM behavior:

1. Identify the exact scoped entry point/router.
2. Trace its opcode/function dispatcher.
3. Confirm the suspect instruction is actually reachable through that dispatcher.
4. Reject repository-wide demonstrations that depend on non-dispatched instructions unless another scoped route exists.

This avoids spending time reproducing a real but unscoped arithmetic property.

## 2. Compare rounding direction across parallel fee paths

Build a compact table for every fee implementation:

| Path | Exact-in formula | Exact-out formula | Rounding | Recipient/ledger effect |
|---|---|---|---|---|
| Flat input fee | fee removed before pricing | fee added after pricing | ceil/floor | retained or transferred |
| Fixed protocol fee | same | same | ceil/floor | recipient transfer/pull |
| Dynamic protocol fee | same | same | ceil/floor | external provider + recipient |

A mismatch between maker/protocol-favoring `ceilDiv` and floor-rounded parallel paths is a high-value hypothesis seed.

For percentage fee `f / BPS`, floor rounding permits zero-fee chunks whenever:

```text
chunkAmount * f < BPS
```

Repeated chunks can therefore accumulate a large intended fee while each individual fee remains zero.

## 3. Use heterogeneous decimals to reveal economic impact

Dust-only tests with two 18-decimal tokens can hide the practical effect as a few wei. Use a standard low-decimal input token and a high-precision output token:

- input token: 0–2 decimals;
- output token: 18 decimals;
- normalize economic units through the AMM's supported rate multipliers;
- make fixtures independent of deployment-address ordering.

This separates fee-unit granularity from output rounding. A 0-decimal ERC-20 is still standard ERC-20 behavior; do not conflate it with fee-on-transfer or rebasing tokens.

## 4. Stateful single-versus-split harness

Snapshot immediately after strategy creation/funding, then execute two branches:

1. **Single:** one swap for total amount `T`.
2. **Split:** `N` sequential swaps of `T/N` against the same evolving strategy state.

Capture at least:

- total taker input/output;
- fee-recipient token delta;
- maker virtual/Aqua input and output balances;
- maker/taker real token balances;
- any protocol accounting accumulator.

Run all split calls from one batching test/contract invocation when transaction-cost objections may matter.

Required controls:

- no-fee curve control: proves the AMM itself does not reward splitting;
- correctly rounded fee control: isolates the suspect fee implementation;
- fixed and dynamic/provider variants when they share a helper;
- both token address orderings or address-independent rate/balance setup.

A conserved global balance does not kill a fee-enforcement finding. The bypassed amount may remain with the maker while the configured fee recipient receives less and the taker receives a pricing advantage. Distinguish accounting conservation from policy/fee correctness.

## 5. Exact-out additivity trap

An exact-out test is vacuous if it compares returned output amounts: output is caller-fixed by definition. For exact-out split-proofness compare:

```text
inputRequired(single total output)
vs
sum(inputRequired(each split output against evolving state))
```

Also compare fee-recipient deltas. Do not treat equality of caller-requested outputs as additivity coverage.

For exact-in, compare total output from one input amount versus the sum of outputs from the stateful split sequence.

## 6. Known-issue archaeology and reportability

When historical docs say rounding favors makers or swaps are split-proof:

- do not reject the lead merely because rounding is discussed;
- look for an explicit exception allowing a concrete wrong-way rounding violation;
- distinguish accepted transfer timing or quote/swap divergence from fee-rounding semantics;
- search removed Git history, audit-era branches, tests, and current known-issues;
- keep prior-private-audit duplicate risk explicit when reports are unavailable.

Report impact as facts first:

- configured recipient expected `X`, received `Y`;
- taker received `Δ` extra output or paid `Δ` less input;
- maker/accounting ledger delta and where bypassed units remained;
- token-decimal and batching prerequisites.

Do not overclaim severity. Candidate impact may map to loss/avoidance of tokens intended for transaction fees, but the program should control final classification.

## 7. Verification and artifact gates

Before promotion:

- focused PoC passes with logged numeric deltas;
- negative controls pass;
- full repository suite passes;
- formatter/linter passes;
- exact scoped dispatcher is cited;
- source lines and pinned revision are recorded;
- report draft separates **The problem** from **Impact analysis**;
- target ledgers/checkpoint/tested-items are synchronized;
- no submission occurs without the user's explicit approval.

## 8. Decompose the economic flow precisely

A fee bypass can conserve all tokens and still create an eligible loss. Compare the atomic and split branches party by party:

| Party | Measure |
|---|---|
| Taker | Same aggregate input; additional output or reduced required input |
| Fee recipient | Expected fee versus actual received fee |
| Maker strategy | Where uncollected input remains and how much additional output it provides |
| Protocol ledger | Conservation, solvency, and whether any deficit exists |

Do not shorthand the result as “the taker keeps the fee” when the token flow actually leaves the uncollected input with the maker and compensates the taker through extra output. State the exact transfer path. Likewise, do not call conserved accounting a false-positive gate when the violated invariant is fee enforcement rather than solvency.

For a report, lead with a compact differential such as:

```text
same aggregate taker input
recipient: X -> 0
maker input balance: +X relative to atomic
additional taker output: Δ
accounting deficit: none
```

## 9. Apply a hostile reportability review

Keep an internal critic artifact separate from the submitted report. Evaluate at least:

- **Impact semantics:** Does the program treat avoided fees as “tokens intended for transaction fees,” or only theft of already-collected fees?
- **Practical granularity:** Is the proof limited to wei-level dust, or can a standard low-decimal/high-unit-value token make each zero-fee chunk meaningful?
- **Execution cost:** Same-transaction batching removes repeated base transactions but not per-router-call gas. Do not claim universal profitability without a value/gas break-even case.
- **Canonical deployment:** The opcode may be scoped and reachable while practical exploitation still depends on a strategy enabling it and holding suitable liquidity.
- **Known-issue archaeology:** Search current notes, removed docs, audit-era branches, tests, and linked reports. Record unavailable private/prior audits as duplicate risk, not as proof of novelty.
- **Victim identity:** Name the configured recipient and its exact shortfall; do not substitute the maker or Aqua when their balances are conserved.
- **Non-claims:** Explicitly reject insolvency, arbitrary reserve drain, unsupported-token dependence, and universal profitability when they are not proven.

A strong candidate can remain submission-worthy with conditional profitability, but the condition must be visible in the impact section rather than buried in an internal note.

## 10. Treat remediation as a design trade-off

Upward rounding is a direct split-resistance fix, but `ceil` on every positive fee can impose a one-raw-unit minimum that is disproportionate for tiny trades. Present the invariant first—transaction granularity must not reduce a nonzero aggregate fee to zero—then offer design choices:

1. explicit upward rounding, preferably full-precision `mulDiv` with a rounding mode;
2. fractional-remainder accumulation by strategy/recipient/token across fills;
3. a minimum fee-bearing trade size or minimum fee policy;
4. aggregate fee accounting at a batching/settlement layer.

Regression tests should cover each selected policy's own edge case, including zero configured fee, tiny trades, exact-in/exact-out, and repeated splits.

## 11. Produce a small portal-ready package

Create two distinct artifacts:

- a concise submit-ready report with **The problem**, **Impact analysis**, expected/actual behavior, remediation, prerequisites, and non-claims;
- an internal hostile review containing rating/acceptance debate, likely rejection arguments, duplicate risk, and unresolved evidence gaps.

Keep rating language out of the submit-ready report unless the form explicitly requests it. Attach the focused PoC initially and hold broad logs/controls for request. Before delivery:

- rerun the exact focused command;
- verify every cited file and source line;
- reject TODO/TBD/placeholders, JWT-shaped strings, and private values;
- generate byte-identical Markdown/text copies when useful for portal or messaging transfer;
- hash the final report, review, and PoC attachment;
- synchronize the target checkpoint without marking the finding submitted.
