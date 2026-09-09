# Web3 deployed-proxy source reconciliation and bounded stop gate

Use this workflow when a bounty scope lists deployed contracts or proxies while the public repository contains newer source. The authoritative test target is the **current scoped address set and each address's current implementation**, not repository HEAD and not an earlier deployment table.

## 1. Freeze the current authoritative asset set

1. Re-open the official program scope immediately before reconciliation.
2. Expand every collapsed asset table and capture all rows, links, chains, addresses, and placeholder/Primacy-of-Impact rows.
3. Normalize the exact deployed addresses into the scope contract. Count deployed assets separately from non-address placeholders.
4. Treat any earlier extraction as provisional. Do not feed addresses from memory, repository READMEs, old notes, or prior deployments into the reconciliation loop.
5. Before finalization, assert exact address-set parity between the current scope contract and every deployment/reconciliation note. Search finalized campaign files for superseded addresses.

**Pitfall:** a technically correct source-match script run against stale deployment addresses creates a convincing but invalid lineage map. Catch this with address-set parity, not prose review.

## 2. Resolve proxy/beacon/direct form

For each current scoped address, record:

- chain and scoped address;
- proxy, beacon, implementation, or direct-contract form;
- current implementation address(es);
- explorer verification status and timestamp;
- current native/token balance where passive metadata is permitted;
- source contract name and compiler metadata.

Handle beacon systems explicitly: scope may separately list the factory, beacon, and implementation. Do not collapse them into one row.

Useful passive metadata paths:

- Blockscout-style explorer: `GET /api/v2/smart-contracts/<address>` and `GET /api/v2/addresses/<address>`.
- Etherscan/BaseScan-style pages: the proxy page exposes the current implementation; verified multi-file source may be embedded in `data-cname` / `data-csource` attributes when an API key is unavailable.

These are metadata reads only. Do not infer authorization for `eth_call`, fork credentials, transactions, or state changes from permission to inspect explorer metadata.

## 3. Match deployed source to Git history

For every verified implementation/direct contract:

1. Extract the exact verified source file containing the target contract.
2. Compute its Git blob ID with `git hash-object --stdin`.
3. Compute the current local file blob with `git hash-object <path>`.
4. If unequal, quantify the source delta and search history for exact containment:
   - enumerate `git rev-list --all -- <path>`;
   - compare `git rev-parse <commit>:<path>` with the explorer blob;
   - record newest/oldest exact matching commits and their messages.
5. If no exact source blob exists, retain the explorer source, record a bounded line delta against HEAD, inspect the changed functions, and avoid assigning an exact commit.
6. Distinguish:
   - exact current-head deployment;
   - exact historical audited/fixed deployment;
   - heterogeneous composition across several historical snapshots;
   - verified but non-exact lineage;
   - current repository code that is not deployed.

Source equivalence is stronger when compiler settings and deployed bytecode also match, but never claim bytecode equivalence from source text alone.

## 4. Reconcile audits, public fixes, and deployment

Build a subtraction ledger containing:

- exact audit repository revisions and in-scope files;
- contest revisions for every repository/submodule;
- public incidents/postmortems;
- disclosed bounty issues and merged fixes;
- unreleased fix branches;
- the deployed implementation lineage for each issue-bearing contract.

A newer repository fix is not automatically current scoped behavior. Conversely, an old deployed issue may still be ineligible when publicly disclosed, previously rewarded, or explicitly excluded as an unreleased/current-source fix. Require a materially distinct root cause or actor path.

## 5. Run bounded checks on the right snapshot

- Run untouched repository baselines for reproducibility, but label them as repository-head coverage unless they match deployed source.
- Prefer existing stateful/fuzz suites for cross-contract accounting, replay/idempotency, epoch transitions, conservation, withdrawals/claims, and authorization.
- Exclude an RPC-dependent fork test explicitly when credentials are not justified; preserve both the setup failure and a clean local-only rerun.
- Foundry accepts one `--match-path`; use one valid glob/brace pattern or separate commands. For a local-only baseline, use a precise `--no-match-path` for the credential-dependent file.
- Static analyzers produce leads. Validate generated JSON/report success even when their process exit is nonzero, then manually apply authorization, reachability, known-issue, deployed-version, and accepted-impact gates.
- Do not write a custom PoC merely to demonstrate activity. Add one only after a hypothesis survives those gates.

## 6. Value-at-risk without overclaiming

When passive metadata is allowed:

1. Record balances at exact scoped holders.
2. Obtain a timestamped token price from a public source.
3. Calculate each holder's approximate USD value and the program's formula payout ceiling.
4. State overlap assumptions explicitly; wrapping reserves, vault balances, and emissions reserves may or may not be independent.
5. Treat broken/stale TVL adapters as non-authoritative and prefer direct explorer balances.

Value establishes economic relevance, not vulnerability likelihood or direct affected funds.

## 7. Stop/continue decision

Continue only when at least one survives:

- a materially unaudited **deployed** delta;
- a heterogeneous-version composition seam with a concrete unprivileged path;
- deployment/source discrepancy not explained by audits or public fixes;
- missing stateful invariant with meaningful accepted impact;
- a materially distinct variant of a known issue.

Pause resumably when the current deployment is predominantly audited/publicly fixed snapshots, newer source is not live, static leads die under manual gates, existing fuzz/state tests pass, and deeper work trends toward excluded third-party or privileged behavior.

On pause:

- set authoritative status to `paused_first_pass_complete` or the campaign's equivalent;
- set `hunting_enabled: false`;
- preserve the corrected deployment map, audit/known-issue ledger, architecture map, tested items, hypotheses, raw logs, balances, and exact reopen triggers;
- verify YAML state, asset count, Git cleanliness, evidence-file existence, and stale-address absence before reporting completion.

## Reopen triggers

Re-run the authoritative address-set capture and implementation mapping when:

- a proxy/beacon implementation changes;
- the program adds/removes assets or changes exclusions/rewards;
- a newer audited branch deploys;
- a new incident or public fix appears;
- passive monitoring finds an unexplained source/implementation mismatch.
