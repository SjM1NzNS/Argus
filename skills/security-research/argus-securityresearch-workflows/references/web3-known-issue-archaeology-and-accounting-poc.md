# Web3 known-issue archaeology and token-accounting PoCs

Use this reference during source-first smart-contract qualification when current documentation is incomplete, audit links are missing, or a plausible token-accounting mismatch appears.

## 1. Search deleted history before building a large PoC

Current `README`, `docs/`, and public audit links are not the whole known-issue set. Before investing heavily in a candidate, search the repository's full history for removed audit briefs, limitation catalogs, audit context, acknowledged findings, and exact technique terms.

Reusable sequence:

```bash
git log --all --format='%h %cI %s' -- docs/ README.md SECURITY.md
git log --all -i -G'known|limitation|unsupported|audit|fee.?on.?transfer|rebas' -- .
git log --all -S'<exact identifier or phrase>' --format='%h %cI %s' -- .
git show <commit>:<deleted-or-historical-path>
```

Also inspect tags and audit-era commits. Absence from `HEAD` does not mean undisclosed. Preserve the commit, path, exact section, and disposition in `known-issue-subtraction.md`; do not copy an entire upstream document into the target report.

Run this gate twice:

1. **early keyword pass** before a costly harness;
2. **exact-symbol/root-cause pass** after a minimal reproduction clarifies the mechanism.

A reproduction of an explicitly unsupported behavior validates the harness but is not a reportable finding.

## 2. Nominal-versus-observed token accounting proof

When code credits an input argument and then calls ERC-20 `transfer`/`transferFrom`, model both quantities:

```text
nominal amount requested
actual sender decrease
actual receiver increase
protocol virtual/ledger delta
downstream asset or claim released
```

A useful local PoC asserts all five. It should prove the realistic honest-party loss path, not merely that a virtual balance differs from `balanceOf`.

Candidate token classes include fee-on-transfer, rebasing, callback-capable, double-entry, and unusual-return tokens. Apply program/token-support rules before reportability. If the protocol explicitly supports standard ERC-20 only or names the class as unsupported, retain the test as a regression/harness check and mark the hypothesis rejected.

## 3. Address-sorted Foundry fixtures

Do not assume Foundry deployment order places a newly deployed token above or below existing tokens. Protocol builders often require `tokenA < tokenB`, so brittle address assumptions can make a valid PoC fail in setup.

Robust pattern:

1. deploy candidate and clean/control tokens;
2. sort `tokenA`/`tokenB` dynamically by address;
3. derive `isAToB` from where the candidate input lands;
4. map initial reserves by semantic role (`reserveIn`, `reserveOut`) and then pass those exact ordered values to both strategy construction and shipping/deposit setup;
5. assert semantic balances through named token handles, not by assuming A/B;
6. run the targeted test, then the complete upstream suite with the PoC included.

If traces already prove the candidate mechanism but an assertion fails, inspect fixture ordering and reserve assignment before changing the hypothesis.

## 4. Reportability disposition

Record one of:

- **promote** — attacker-controlled, in-scope, supported state and accepted impact;
- **hold** — mechanism reproduced but deployment/support/impact remains unproven;
- **reject-known** — exact behavior disclosed or accepted historically;
- **reject-token-model** — requires an explicitly unsupported token class;
- **reject-self-harm** — only the configuring trusted actor is harmed;
- **reject-unreachable** — repository code lacks a scoped deployed dispatcher/entry path.

Keep rejected PoCs clearly labeled and uncommitted or outside immutable source clones. Never let a passing exploit-style test silently become a finding claim.

## 5. Virtual-reserve versus real-ledger-cap kill test

When an AMM prices against virtual reserves, a quote larger than the declared real output reserve is a lead—not proof of overdraft or theft. Separate three layers:

```text
pricing reserve used by the curve
strategy/accounting allowance used by settlement
maker's actual wallet balance and approval
```

Use a Foundry test that deliberately gives the maker **extra wallet balance beyond the strategy allowance**. This distinguishes an actual cap bypass from an ordinary insufficient-settlement revert:

1. initialize realistic real reserves and valid standard curve parameters;
2. ship/deposit only the declared strategy reserve;
3. mint additional unshipped output tokens to the maker and preserve approval;
4. request exact output just above the declared reserve but below the computed virtual reserve;
5. prove the quote succeeds and record the calculated input;
6. execute the identical swap;
7. assert the exact settlement result and all before/after state: strategy ledger, maker token balances, taker balances, callbacks, fees, and locks;
8. repeat for relevant transfer ordering or accounting modes when they differ.

Do not stop at `expectRevert()`. Atomicity is the decisive false-positive gate. If settlement reverts and every ledger/real balance is unchanged, reject theft and cap-bypass claims even if the quote looked executable. Retain only the narrower quote-versus-settlement behavior, then check whether documentation explicitly says quote omits allowance, balance, fee-transfer, or settlement feasibility.

Evaluate authorization modes separately. A direct/signature mode may treat maker-provided balances as pricing inputs rather than a spending cap, while an Aqua/vault/dynamic-balance mode may have a real ledger subtraction that enforces the cap. Do not transfer conclusions between modes without an executable test.

## 6. Cross-order callback/reentrancy equivalence test

A lock keyed by `orderHash`, pool ID, position ID, or strategy ID prevents same-object recursion but may still permit callback entry into a distinct object sharing one real wallet, allowance, vault, or liquidity source. Do not report the narrower lock merely because cross-object entry is reachable. Test whether nesting changes the economic result.

Build one attacker-controlled callback harness and require these controls:

1. **Same-object negative control:** callback reenters the outer object. Prove the lock rejects the inner call. If the callback catches the inner revert, verify the single outer paid operation still settles correctly.
2. **Different-object positive control:** callback enters a second valid object for the same maker/assets. Run both output-first and input-first settlement when caller traits can select ordering.
3. **Nested-versus-sequential equivalence:** snapshot the initial state, execute nested A→B, hash or record every relevant ledger and real-token balance, restore, execute A then B sequentially, and require identical economic state.
4. **Shared-liquidity overcommit control:** let both objects advertise independent capacity while the maker's real wallet can fund only one. Require complete atomic rollback—inner output, both input receipts, object ledgers, fees, callback state, and maker/taker balances.
5. **Impact gate:** promote only if nesting retains an inner transfer after outer failure, consumes more real funds than sequential execution, bypasses an object cap, observes stale state to obtain a better rate, or leaves a ledger/real-balance divergence unavailable through ordinary sequencing.

The core comparison is:

```text
nested final economic state == sequential final economic state
underfunded nested execution == pre-call economic state
```

Per-object ledger mutation, immediate ERC-20 transfers, and transaction atomicity may make cross-object composability safe even without a global lock. Conversely, a global wallet or shared reserve read before either nested write can create a real stale-snapshot bug; the state-equivalence control distinguishes the two.

### Minimal callback-harness details

- Keep the malicious callback state machine explicit: `reentryEnabled`, `entered`, inner success/revert data, and inner amounts.
- Repay each operation through the protocol's real callback path rather than minting directly into protocol accounting.
- Make the callback catch same-object lock failure for the negative control, but allow outer settlement failures to propagate for the atomicity control.
- When a large trait/config builder causes compiler inlining or stack-depth failures, and **all dynamic slices are empty**, construct the documented fixed-width wire header directly from authoritative bit constants. Cross-check header length and parser semantics; do not hand-pack dynamic offsets or use this shortcut when any tail data exists.
- Run the focused harness and then the complete upstream suite. Preserve both logs and label a safe result as a falsified hypothesis, not a vulnerability PoC.

## 7. Reconcile delayed parallel reviews after closeout

Background architecture, gap, and audit-diff workers may finish after the primary pass has already reached a stop decision. Reconcile them rather than appending their hypotheses uncritically:

1. compare each delayed lead against the **current** tested-items, known-issue ledger, and source pin;
2. reopen only materially stronger, previously untested hypotheses;
3. choose the smallest reportability-kill test first—authorization, reachability, atomicity, real balance loss, or supported-state gate;
4. rerun the focused test and complete suite;
5. update the hunt log and tested-items ledger with exact disposition and evidence paths;
6. preserve the original closeout if the lead is killed; do not let a stale worker ranking silently reopen the whole audit.

Worker output is source-review assistance, not verified proof. Independently verify commits, local paths, tests, and side effects before changing the finding decision.

## Session-derived examples

- In a 2026 Aqua/SwapVM qualification, a local test proved that a 10% transfer-tax input could produce a nominal Aqua callback credit larger than the maker's real receipt while settlement succeeded. The full suite passed with the PoC added. Historical Git archaeology then recovered a removed auditor brief explicitly classifying fee-on-transfer and rebasing tokens as unsupported/accepted. Correct disposition: `reject-known`, while retaining the harness and adding the historical-known-issue gate to future workflows.
- A delayed review later identified concentrated-liquidity quotes above the real Aqua reserve. A focused test shipped 100 output tokens, left an additional 100 in the maker wallet, and quoted just over the shipped cap. Quote succeeded, but settlement reverted atomically and all maker/taker/ledger balances remained unchanged. Correct disposition: reject theft/cap bypass; retain only documented quote-versus-settlement divergence.
- A subsequent callback test entered a distinct same-maker strategy while the outer order was locked. Both transfer orders settled as two fully paid swaps, a snapshot digest matched nested execution to sequential A-then-B execution, and a wallet funded for only one output caused the complete nested transaction to revert with no retained inner transfer or ledger delta. Correct disposition: cross-order entry was reachable composability, not stale-state double spending.
