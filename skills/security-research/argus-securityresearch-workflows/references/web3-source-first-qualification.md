# Web3 source-first qualification and invariant reconnaissance

Use this reference when deciding whether a shortlisted smart-contract bounty or contest deserves a sustained audit. The goal is a bounded, source-derived qualification pass—not a scanner sweep and not immediate target activation.

## 1. Separate shortlist, activation, and dedication

Track three states independently:

1. **shortlisted** — official-source monitoring found a potentially tractable opportunity;
2. **qualified/initialized** — current scope, rules, source revision, local-test authorization, and known issues were captured;
3. **dedicated review** — the qualification pass found unsaturated semantic surfaces or a plausible reportable hypothesis.

Daily radar notes are discovery evidence, not necessarily the canonical shortlist. Maintain or reconcile a canonical shortlist ledger with: date added, platform, live URL, subjective fit, current status, last official revalidation, and reason for promotion/demotion. Recheck live reward allocation, deadline/timezone, scope visibility, and repository access before making an effort decision; contest economics can change after the morning radar capture.

## 2. Prefer tractable source environments

For an initial Web3 review, prefer:

- exact file-mapped or commit-pinned public Solidity scope;
- Foundry tests and reproducible local setup;
- narrow asset/protocol surface;
- explicit accepted impacts and local/fork PoC rules;
- recent or post-audit code changes;
- docs, scripts, deployment configuration, snapshots, events, errors, and interfaces that expose intended behavior;
- a protocol class already covered by local playbooks.

Penalize:

- private/unlinked code or missing source revision;
- broad bridge/L1/L3/multichain dependency graphs;
- mature protocols with many recent audits/scans;
- heavily trusted off-chain inputs that remove obvious attack models;
- discretionary/conditional payout or small contestant share;
- short contest windows that do not cover comprehension cost.

A large advertised maximum is not a substitute for source access, proof quality, or unsaturated attack surface.

## 3. Static analyzers are reconnaissance, not the audit

Run Slither/Aderyn early and briefly to obtain:

- inheritance and call-graph hints;
- external calls and callback locations;
- state-variable and authorization leads;
- common defect sanity checks;
- detector locations that deserve source review.

Do not treat detector output as differentiated value or report evidence. Mature teams often run comparable checks. Every lead must survive exact scope, reachability, actor model, realistic state, known-issue, economic-impact, and executable-proof gates.

## 4. Solidity analogue of Web2 JS-first mapping

Map concepts as follows:

| Web2 source-first | Web3 protocol-source-first |
|---|---|
| JS bundles/chunks | scoped contracts, libraries, interfaces |
| routes/API bases | public/external entry points and external calls |
| object selectors | position/order/loan IDs, storage keys, shares, balances |
| feature flags | packed traits, role bits, modes, pause/config state |
| frontend workflows | tests, scripts, deployment flows, integration harnesses |
| source maps/build deltas | Git history, blame, PRs, tags, audit-era diffs |
| client assumptions | trust model, conservation rules, state-transition invariants |
| hidden endpoints | untested function compositions, callbacks, lifecycle edges |

Let source and tests identify exact reachable surfaces before inventing hypotheses.

## 5. Bounded qualification pass

### A. Lock scope and provenance

1. Capture every official scope row and explicit exclusion.
2. Record exact repository commits/tags; if the program does not pin a revision, create a local review pin and state that limitation.
3. Hash scoped files and record dependencies/submodules.
4. Capture official impacts, PoC rules, local/fork restrictions, KYC/triage/safe-harbor state, and deadline/reward allocation.
5. Locate prior audits, `SECURITY.md`, known issues, public fixes, and their corresponding revisions.
6. Build scoped diffs after the latest audit, bounty launch, or material program update.

### B. Build the protocol map

For every scoped entry point record:

```text
function → permitted actor → attacker-controlled input → state read/write
→ assets/claims affected → external calls/callbacks → intended invariant
→ existing tests → missing actor/state/order combinations
```

Also build:

- actor/trust matrix;
- asset and claim-flow diagram;
- state-machine/lifecycle graph;
- role and upgrade/config boundary map;
- cross-contract ledger reconciliation map;
- source-to-test coverage matrix.

### C. Mine tests as specification

Do more than run the suite. Compare each entry point against:

- actor type;
- initialized/empty/near-empty/terminal state;
- zero/minimum/maximum/boundary values;
- single versus repeated operation;
- standalone versus batch/multicall;
- success, revert, retry, partial completion, pause, and upgrade state;
- callback/reentrancy and operation ordering;
- quote/simulation/preview versus actual execution.

A large passing suite reveals the developers' modeled assumptions and therefore highlights unmodeled combinations.

### D. Review diffs before rereading mature code uniformly

Prioritize:

1. scoped changes after the latest audit;
2. changes after bounty launch/scope update;
3. newly introduced opcodes, modes, roles, or assets;
4. fixes applied to one of several parallel implementations;
5. tests added with bug fixes, followed by sibling paths missing the fix;
6. deployment/config changes that alter reachable behavior.

Diff-derived hypotheses usually have better expected value than generic detector findings.

### E. Generate source-derived tests

Use Foundry handlers, fuzzing, and invariants for exact candidate surfaces:

- conservation of assets, shares, debt, fees, and claims;
- no value increase without a documented source decrease;
- lifecycle transitions cannot skip, repeat, or become irrecoverably stuck;
- authorization remains valid across callbacks, transfers, batches, and role changes;
- quote/preview/simulation agrees with execution within a derived rounding bound;
- equivalent single/batched or exact-in/exact-out paths have consistent effects;
- revert/retry and partial completion do not leave stale accounting or locks.

For custom VMs, packed traits, calldata pointers, or transient storage, prioritize malformed/truncated sequences, bit boundaries, conflicting flags, namespace collisions, nested calls, cleanup after revert, and simulation/execution divergence.

For AMMs with virtual reserves, do not promote `quotedOut > realReserve` by itself. Seed extra unshipped maker wallet funds, execute the identical swap, and assert strategy ledger plus maker/taker balances before and after. An atomic insufficient-settlement revert kills theft/cap-bypass claims even when quote succeeds; evaluate each authorization/accounting mode independently.

Mutation-guided gap discovery can be useful locally: flip a rounding direction, remove a mask/check/lock, alter an offset, or reorder accounting. If existing tests still pass, that is a prioritization signal—not vulnerability proof.
## 6. Known-issue and false-positive subtraction

Search both **current sources and deleted Git history** before investing in a large PoC. Public audit indexes and current `docs/` may omit or remove auditor briefs, limitation catalogs, acknowledged findings, and audit context. Use `git log --all`, `-S'<exact phrase or identifier>'`, `-G'<root-cause regex>'`, tags, and `git show <commit>:<historical-path>`; preserve the commit/path/section that controls disposition. Run a broad early keyword pass, then an exact-symbol/root-cause pass once a minimal reproduction clarifies the mechanism. Absence from `HEAD` is not evidence that a behavior is unknown.

For token-transfer accounting candidates, distinguish nominal argument, actual sender decrease, actual receiver increase, internal ledger delta, and downstream asset/claim released. A virtual/real mismatch alone is not enough: prove an honest-party loss path, then apply supported-token and known-limitation gates. When Foundry fixtures require sorted token addresses, sort dynamically, derive swap direction from semantic input/output roles, and pass the same ordered reserves into both strategy construction and shipping/deposit setup; never assume deployment address order.

See `web3-known-issue-archaeology-and-accounting-poc.md` for the reusable Git-history search, token-accounting proof matrix, address-independent fixture pattern, and reject/promote dispositions.

Before escalating a candidate, reject or downgrade:

- disclosed/audited/publicly fixed behavior;
- excluded files, testnets, mocks, or unpinned revisions;
- malicious or incorrect behavior by explicitly trusted roles;
- impossible/unreachable state sequences;
- standards deviations without accepted impact;
- dust-only effects below fees/gas without amplification;
- nonstandard-token assumptions outside program scope;
- hypothetical loss without quantified, executable state transition;
- scanner-only labels without actor-controlled reachability.

## 7. Go/no-go gate

Dedicate more time only when at least one condition holds:

- material scoped post-audit delta exists;
- a high-impact actor/state/order combination is absent from tests;
- parallel paths disagree on accounting, authorization, or state transitions;
- implementation and tests/specs imply inconsistent invariants;
- a source-derived seam yields a plausible attacker-controlled sequence;
- an executable local PoC path can be outlined;
- the hypothesis survives prior-report and trusted-role subtraction.

Stop or defer when all meaningful changes are covered, source/version ambiguity prevents defensible reporting, remaining ideas depend on trusted-role mistakes, or only dust/standards/gas issues remain.

A practical first-pass budget is 2–4 hours: scope/provenance, build baseline, architecture map, test/diff mining, two or three invariant harness prototypes, then an explicit continue/stop decision.

## 8. Output artifacts

A qualification pass should produce compact, reusable artifacts:

- `scope-lock.json` or equivalent commit/file/hash ledger;
- `protocol-map.md`;
- `entrypoint-matrix.csv`;
- `state-machine.md`;
- `test-gap-matrix.md`;
- `post-audit-diff.md`;
- `known-issue-subtraction.md`;
- `qualification-decision.md` with continue/stop criteria;
- local PoC/harness files outside immutable clones.

Do not initialize a full hunt or claim a finding solely because the qualification pass found complexity or missing tests.
