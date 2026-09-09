# Independently Pinned Web3 Scope Review

Use this pattern when a bounty program lists Solidity assets as independent `repository + commit + path` rows rather than one repository-wide commit.

## Scope normalization

1. Normalize the program scope into a machine-readable table containing at least repository, full commit, exact path, and exclusions.
2. Verify every `commit:path` object directly with Git; preserve stderr and per-row status rather than trusting one aggregate count.
3. Record duplicate paths at different commits as separate assets until official scope interpretation proves one supersedes another.

## Newest-tree reconciliation

A successful scan of repository HEAD is not authoritative for older-pinned rows.

1. Hash `git show <pinned-commit>:<path>` and the same path at the chosen analysis HEAD.
2. Reuse the HEAD result only when hashes match.
3. Route every changed row to an exact historical workspace.
4. If the scope has several historical commits, compare dependency/submodule tree hashes. Reuse a dependency workspace only when the Git tree hashes are identical.

## Historical workspace and baseline

- Keep the primary baseline clone immutable.
- Build historical revisions in detached worktrees or separate clones.
- Preserve exact dependency/submodule pins; do not silently compile historical source against current dependencies.
- Run untouched build/tests first. If one test is network/RPC-gated, preserve the failure, then run a clearly identified local-only subset rather than supplying unapproved RPC access.
- Record build totals, permitted test totals, excluded test names, revision, and evidence paths.

## Static-analysis filtering

1. Run scanners in the exact historical workspace needed to compile the source.
2. Preserve raw full-project output because tools may need dependency context.
3. Filter findings to exact scoped `commit:path` pairs before triage.
4. Treat dependency, test, and unlisted-file findings as context unless they establish impact through a scoped asset.
5. Distinguish scanner nonzero exits caused by detector findings from build/tool failure by validating the output artifact.

## Regression archaeology

For each changed scoped path, inspect post-pin commit messages and diffs. Security-shaped changes can reveal high-ROI hypotheses, but apply these gates:

- Is the older revision still independently in current scope?
- Is the issue already documented in audits, QA reports, release notes, or the known-issue index?
- Does a trusted upstream component already enforce the missing property?
- Is there a realistic unprivileged path and listed impact?
- Is the old code deployed/current, or only a superseded source artifact?

Do not report a historical fix as a novel vulnerability without resolving all five gates.

## Local invariant testing

- Keep PoC tests outside the immutable clone.
- Temporarily copy a test into the exact historical workspace, run it, preserve the log, remove the temporary copy, and verify baseline cleanliness.
- Prefer stateful/fuzz conservation tests over single examples: multiple users, cancellation/execution partitions, rounding boundaries, fee/no-fee variants, request clearing, escrow residue, attribution, and total supply/assets.
- Separate behavioral confirmation from reportability. A passing PoC can still be rejected when it depends on trusted admin configuration, an authorized caller, accidentally sent funds, unsupported assets, or a published known issue.

## Snapshot semantics for cross-contract tests

Independent file pins do not automatically define a synthetic runtime made from files copied across several commits.

- Default to testing each scoped file inside its own pinned commit snapshot with that snapshot's dependencies and neighboring contracts.
- Do not construct a mixed-commit overlay merely to make a cross-contract invariant convenient unless the program or deployment evidence explicitly establishes that combination.
- When a logical invariant spans independently pinned files, split it into snapshot-valid legs (for example, fee-enabled deposit conservation in the deposit queue's snapshot and fee-enabled redeem conservation in the redeem queue/FeeHandler snapshot).
- Hash-check apparently unchanged files before reusing a newer workspace. Read full commit IDs from the normalized scope table; do not hand-transcribe abbreviations.

## Metamorphic and reference-model fuzzing

Use metamorphic tests when exact expected values are hard to enumerate:

- compare one-shot settlement with partitioned settlement over the same economic path;
- compare aggregate tracker output with an independent signed reference model;
- assert conservation identities such as `deposit value = net issued shares value + fee liability` and `residual redeem asset value >= fee liability`;
- fuzz cancellation/execution partitions, mixed signs, time boundaries, zero-duration transitions, fee rates, and removal compaction.

Do not require exact equality when the implementation intentionally floors at several layers. Derive the tolerance from the arithmetic:

- a one-wei per-share HWM floor can become roughly `supply / 1e18` value wei at the next fee settlement;
- converting total-value dust back into per-share HWM units scales inversely with supply;
- per-request low-decimal asset conversion can leave less than one asset unit of residue per request.

A fuzz counterexample that fits a derived dust bound is a test-model correction, not a finding. Preserve the failed seed/log, explain the bound, patch the assertion, and rerun the full campaign. Never widen a tolerance without deriving it in protocol units and checking economic materiality.

For large fuzz harnesses, too many independent parameters and local arrays can trigger Solidity `stack too deep`. Pack fields into a few seeds, decode them in helper-scoped locals, and keep the independent model explicit rather than switching compilation modes solely to hide harness structure.

When inheriting a repository test contract, Foundry also discovers inherited base tests. Use both `--match-contract` and `--match-test` when the evidence claim is about one new fuzz invariant; otherwise report inherited test counts separately.

## Counterexample and known-issue subtraction

Before escalating a recognizable technique, check source comments, the target known-issue index, published audits/QA, and post-pin history. Generic external RAG precedents can classify a technique but are not target-specific proof.

If fuzzing reproduces a documented boundary (for example, a tiny request whose net output rounds to zero):

1. preserve the exact counterexample and map it to the published issue;
2. record it as reproduced and excluded rather than silently discarding it;
3. constrain the next invariant to the economically executable domain only when the exclusion is explicit;
4. continue looking for a materially distinct mechanism or actor path.

For fee/accounting tests, distinguish:

- unprivileged value extraction or insolvency;
- bounded arithmetic dust;
- admin-controlled claim sizing or configuration under a fully trusted-admin model;
- a published risk-accepted economic behavior.

Only the first category is a candidate without additional program-specific evidence.

## Evidence ledger

Update class-level target artifacts with:

- exact revision and path;
- hypothesis and invariant;
- positive/negative controls;
- fuzz run count and assertion set;
- raw log path;
- disposition: candidate, known issue, false positive, trusted configuration, blocked, or rejected;
- baseline Git cleanliness.

## Common pitfalls

- Typing a commit manually instead of reading it from the normalized scope table.
- Calling a newest-tree scan “scoped” when older pinned file contents changed.
- Sharing current submodules with historical source without checking tree identity.
- Treating a scanner's attacker-directed-transfer alert as proof without tracing who controls the stored recipient.
- Confusing a trusted delivery retry with an arbitrary attacker replay.
- Claiming a value-forwarding behavior is exploitable without proving deployed caller/selector configuration and protocol-fund provenance.
