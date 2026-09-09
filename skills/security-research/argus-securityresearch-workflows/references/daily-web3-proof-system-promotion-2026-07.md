# Daily Web3 proof-system promotion pattern — 2026-07

Session pattern from daily Argus learning promotion on 2026-07-04.

## When to use

Use this reference during daily learning promotion when the latest ingest is sparse overall but includes one or more concrete Web3 incident writeups, checklists, or postmortems with extractable proof/evidence lessons.

## Pattern

1. Audit both execution and content quality before promotion:
   - total static/browser records;
   - count of `actual_content` records;
   - index/listing/skipped/seen counts;
   - actual-content ratio.
2. Treat noisy records conservatively:
   - DOM/app bootstrap/import-map/CSS captures are not methodology even if labeled `actual_content`;
   - index/listing pages are discovery context only;
   - broad checklists can reinforce gates, but should not be copied wholesale.
3. Route through `web3-skill-index.md` and add a new class-level playbook only when an actual missing class appears. In this session the missing class was `Web3/Proof Systems`, covering ZK circuits, rollups, public inputs, private witnesses, nullifiers, verifier-to-settlement boundaries, and proof-authorized settlement.
4. Promote into class-level notes, not source-specific one-offs:
   - create `02 - Vulnerability Playbooks/Web3/<Class>/overview.md`, `test-checklist.md`, `invariants.md`, `evidence-requirements.md`, `false-positives.md`, `reportability.md`, and `attack-patterns.md` when the class is new;
   - patch adjacent playbooks such as Bridges, Input Validation, Signatures, External Calls, and Foundry/Reporting as needed;
   - add routing triggers to `00 - System/web3-skill-index.md`.
5. Add eval scenarios that force report/hold/discard decisions instead of just storing lessons.
6. Write support outputs:
   - source summary under `01 - Learning/Source Summaries/`;
   - promotion review under `01 - Learning/Skill Patch Proposals/`;
   - rejected/deferred note under `01 - Learning/Rejected Lessons/` when noisy records exist;
   - system report under `00 - System/`;
   - monthly changelog entry under `07 - Skill Changelog/YYYY-MM.md`.
7. Verify every touched file is non-empty and contains no `TODO`/`TBD`; also verify new index `Load:` paths exist and are non-empty.

## Web3 proof-system lessons promoted

From a concrete incident writeup, extract proof-system methodology as evidence gates:

- A valid cryptographic proof is not automatically a valid settlement authorization.
- Require binding between public inputs, private witnesses, roots, nullifiers, transaction counts, verifier/circuit version, and settlement parameters.
- Proof-system reports need accepted mismatched proof/state plus measurable settlement impact, not just taxonomy labels.
- Deprecated/legacy rollup or escape-hatch paths remain relevant if funds, claims, or privileged controls remain reachable.

Adjacent lesson examples:

- Wallet signing: public-only nonce derivation or omitted secret prefix is reportable only with a vulnerable deployed version and local non-production key-recovery proof.
- Token wrappers/approvals: events or simulated profit are not enough; verify allowance consumption, balance deltas, residual approval cleanup, spender allowlists, and code hash/upgradeability assumptions.

## Verification snippet shape

Use a local script to check touched paths:

- file exists;
- file content is non-empty;
- no `TODO`/`TBD` placeholders;
- index `Load:` paths for the newly added class exist and are non-empty.

Do not claim success until verification passes.
