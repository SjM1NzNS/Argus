---
type: eval-update-proposal
status: draft
created: "2026-06-29 11:53"
domain: web3
run: "2026-06-29-learning-dry-run"
---

# Web3 Eval Update Proposals — Learning Dry Run

## Proposed new/updated eval cases

1. `share-accounting-profit-valid.md` — ERC4626/share math bug with realistic unprivileged profit and invariant break.
2. `rounding-dust-only-invalid.md` — mathematically real but economically negligible rounding issue should be low/hold/discard.
3. `oracle-stale-price-valid.md` — stale/heartbeat/decimals issue with realistic borrow/liquidation path.
4. `postmortem-translation-not-report-evidence.md` — Rekt/Immunefi postmortem pattern requires scoped code, PoC, and impact before report.
5. `upgradeable-initializer-exposed-valid.md` — uninitialized implementation/proxy path with unprivileged takeover evidence.

## Required questions for each eval

- Is this reportable?
- What severity?
- What proof is missing?
- What would triage reject?
- What is the next action?
- Should Argus report, hold, or discard?
