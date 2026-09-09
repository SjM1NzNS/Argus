---
type: source-summary
status: promoted
created: "2026-07-05"
sources:
  - "daily-20260705-073001-static"
  - "daily-20260705-073001-browser-dom"
---

# Daily 2026-07-05 source summary — Solodit/Cyfrin vault accounting and lifecycle

## Run quality audit

- Static run: 146 records; 1 `actual_content` record, 56 index/listing records, 84 not-fetched/skipped records.
- Browser DOM run: 60 records; 8 `actual_content` records, 13 index/listing records, 36 seen/skipped records, 1 thin-content record.
- Actual deep content ratio across combined records: 9 / 206.
- Promotion was limited to concrete Web3 methodology from Solodit/Cyfrin Accountable findings. HackerOne directory/CWE/hacktivity pages were treated as discovery context, not playbook lessons. Bug Bounty Daily static content was DOM/import-map/bootstrap noise despite being labeled `actual_content`.

## Promoted lessons

### Vault fee/penalty bases can accidentally self-compound

Source: Solodit/Cyfrin Accountable finding: `AccountableYield::_accruePenalties` includes `accruedPenalties` in the penalty base.

Operational lesson:

- For vaults and strategies, inspect whether accrual bases include already-accrued fees/penalties.
- If the protocol promises simple interest or linear late penalties, including accrued penalties can make total penalty depend on how frequently hooks are called.
- Evidence requires formula comparison, call-frequency controls, before/after accounting state, and quantified user/protocol overcharge or undercharge.
- Duplicate reads or recomputation are not security findings unless they change economic state.

Promoted to:

- `02 - Vulnerability Playbooks/Web3/Share Accounting/invariants.md`
- `02 - Vulnerability Playbooks/Web3/ERC4626/attack-patterns.md`
- `02 - Vulnerability Playbooks/Web3/Rounding & Precision/attack-patterns.md`
- `06 - Evals/Web3/vault-accounting-lifecycle-daily-20260705-eval-scenarios.md`

### Epoch/queue lifecycle bugs require terminal progress checks

Source: Solodit/Cyfrin Accountable finding: `DepositGateway::_passEpoch` passes an emptied epoch into `Passed` where it never finalizes to `Settled`.

Operational lesson:

- State machines with epochs/queues must be tested for all-cancelled, zero-pending, forced-pass, refund, settle, and keeper/update paths.
- The key invariant is terminal progress: every non-terminal state with no live work must be able to safely finalize, reopen, or recover without locking funds/claims.
- Reportability requires accepted actor path plus concrete stuck funds, blocked claims, blocked progress, inconsistent accounting, or control impact.
- If a public/documented recovery path always finalizes without loss, downgrade as hardening.

Promoted to:

- `02 - Vulnerability Playbooks/Web3/State Machines/overview.md`
- `00 - System/web3-skill-index.md`
- `02 - Vulnerability Playbooks/Web3/ERC4626/attack-patterns.md`
- `06 - Evals/Web3/vault-accounting-lifecycle-daily-20260705-eval-scenarios.md`

## Deferred or rejected material

- Solodit/Cyfrin duplicate read / try-catch / storage-pointer findings: useful as gas/hardening examples only; promoted as false-positive/downgrade gates, not as vulnerability classes.
- HackerOne directory, CWE discovery, and Hacktivity listing: discovery/listing context; no concrete target-independent method beyond already-covered routing.
- Bug Bounty Daily static import-map/bootstrap content: DOM noise; no daily promotion.
- AppSec.fyi/index/listing and skipped/seen records: not promoted.
