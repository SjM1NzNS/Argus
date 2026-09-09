# Daily governance-capture promotion pattern — 2026-07

Use when a lightweight daily learning run contains a concrete Web3 governance incident/writeup but the rest of the run is mostly listings, skipped/seen records, or SPA/bootstrap noise.

## Trigger

- Daily ingest has a small number of `actual_content` records.
- One record describes a governance attack/capture where the attacker followed governance rules rather than exploiting an obvious smart-contract bug.
- The incident includes enough methodology to extract class-level gates: quorum/threshold economics, proposal payload opacity, voting-power acquisition, timelock/response window, and treasury/control impact.

## Promotion steps

1. Audit the run quality first: count combined records, `actual_content`, listing/index records, skipped/seen/robots/link-limit records, and browser-DOM actual-content count.
2. Route through `argus-vault-routing` and load Web3 Governance and Reporting notes from `00 - System/web3-skill-index.md` before editing.
3. Promote only the class-level lesson, not the incident narrative:
   - market-acquired or borrowed/delegated quorum capture;
   - proposal-content camouflage where benign text hides harmful calldata;
   - zero/too-short timelock for treasury/control actions;
   - proposal/vote/execution evidence matrix;
   - false-positive filters for low turnout, accepted tokenholder control, centralization-only, or postmortem analogy.
4. Patch Web3 Governance invariants and attack patterns, and Web3 Reporting reportability gates.
5. Add a source summary under `01 - Learning/Source Summaries/` and eval scenarios under `06 - Evals/Web3/`.
6. Update the monthly changelog.
7. Verify touched files exist, are non-empty, and contain no `TODO`/`TBD` placeholders.
8. Clear only the reviewed disposable daily inbox directories for that run after verified promotion; do not clear unrelated manual/backfill inbox material.

## Pitfalls

- Do not report or encode “low voter turnout” by itself as a vulnerability. The durable gate is whether the target-specific governance security model promises thresholds/timelocks/payload review/emergency response that an economically realistic attacker can bypass or defeat.
- Do not promote listing pages, SPA import maps, repository overviews, or thin contest metadata as methodology. Defer them until targeted deep content is fetched.
- Do not use historical incident records as proof for a live target; they are Zone 0/class-level methodology only until the target has an executable local/fork/on-chain proof.
