# OSS Public-Prior-Art and Repository-Saturation Gates

Use this reference after a fixed-commit OSS audit surfaces one or more technically valid candidates. Its purpose is to prevent alternate exploit narratives, independent rediscovery, or adjacent sinks from being promoted when an open issue, pull request, advisory, or active hardening series already covers the same root cause.

## Core principle

Technical validity and novelty are independent verdicts.

A candidate can have:

- an exact source-to-sink chain;
- a deterministic local reproduction;
- a meaningful capability increase;
- passing negative controls;

and still be a **duplicate/no-go** because public prior art already identifies the root and the proposed public fix blocks the candidate.

Judge novelty by root cause and remediation—not by payload, entry point, filename, or impact story.

## Prior-art classification

Assign one of these before submission:

| Class | Test | Default disposition |
|---|---|---|
| Exact duplicate | Same source, sink, invariant, and remediation | No-go |
| Same-root consequence | Different exploit sequence or impact, but the public fix blocks it without another change | No-go or disclose only as corroboration if privately requested |
| Adjacent family | Same subsystem/security family, but independent source, invariant, and remediation | Continue only with an explicit differential |
| Incomplete fix | Public patch closes its stated case; current patched source still fails a one-variable bypass that requires additional remediation | Candidate, after exact current-source proof |
| Distinct root | Public fix does not block the candidate and candidate fix does not block public issue | Continue |

### Two-way remediation test

For candidate `C` and prior art `P`, ask:

1. Does `P`'s proposed fix block `C`?
2. Does `C`'s proposed fix block `P`?

Interpretation:

- yes/yes usually means same root;
- yes/no often means `C` is a consequence or narrower variant of `P`;
- no/yes may mean `C` is a broader root, but only if its report and proof center that broader invariant;
- no/no supports distinctness, subject to source and actor-model review.

Do not call a candidate distinct merely because it reaches a different file overwrite, credential, queue, policy consumer, or downstream impact.

## Search sequence

Run the duplicate gate before spending heavily on a full exploit package, then repeat it after root cause is known.

### Pass 1: repository-local public state

Search open and closed:

- issues and pull requests;
- PR titles, bodies, comments, and full file diffs;
- security advisories;
- release notes and changelogs;
- commit history for the sink, guard, normalization variable, and prior fixes;
- tests mentioning the invariant or negative behavior.

Search both symptom and mechanism terms. Examples:

```text
path traversal | symlink | nofollow | digest mismatch | verify hash
credential log | raw response | token leak | duplicate record
working directory | output root | cache integrity | quote coverage
```

A title-only search is insufficient. Read the patch: a general guard introduced at a shared layer may close a more dramatic exploit chain that the PR body never names.

For worker, sidecar, or internal-service candidates, search exact class names, route literals, configuration keys, and lifecycle terms (`set-context`, `clear-context`, worker reuse, thread/process cleanup), not only the impact label. Save a per-candidate query ledger before local validation. An open PR with an exact route/root-cause match is a stop signal even when a separate downstream authentication flaw makes the impact more severe.

### Pass 2: class-level advisories and downstream history

Check:

- CVEs/GHSAs touching the same method or security invariant;
- package advisory databases;
- forks carrying validation changes;
- downstream consumers that pin affected releases;
- prior reports in the local vault.

For advisories touching the same method, write an explicit root-cause differential. Example distinction:

```text
prior: proof covered zero/some records but completeness was not enforced
candidate: proof covers a genuine record, but verification state is transferred
           to a different duplicate value
```

Method overlap alone is not duplication; invariant and remediation overlap decide it.

### Pass 3: active hardening-series saturation

Inspect neighboring open PR numbers, shared authorship, timestamps, touched files, and common language. A repository is likely saturated when several concurrent public patches cover multiple nearby trust boundaries in the same subsystem.

Signals:

- consecutive or near-consecutive security PRs;
- multiple unmerged fixes in the same parser/downloader/auth module;
- one PR's diff exposes adjacent unsafe logging or validation code;
- several independently found candidates map to that series;
- public contributors are clearly running the same audit class.

Saturation does not prove every candidate is duplicate. It raises the novelty burden and often makes a pivot higher ROI than squeezing a same-file distinction.

## Efficient evidence order

1. Pin current commit and released affected tag.
2. Establish the candidate's exact invariant and source chain.
3. Search public prior art and read candidate fixes.
4. Run the two-way remediation test.
5. Only then build the expensive end-to-end proof if distinctness survives.

Exception: a tiny deterministic control may be worth running first to understand the root. Stop expanding it once an exact public fix is found.

## Handling parallel-agent findings

Subagent results are leads, not verified facts.

For each returned candidate:

1. independently verify source revision and exact source lines;
2. independently read any matching public PR/advisory;
3. reproduce only if novelty survives or reproduction is needed to classify the root;
4. do not inherit claims that a file was written, a test passed, or a workspace is clean without reading back or rerunning;
5. preserve useful local controls even when disposition becomes duplicate, but label them as duplicate evidence rather than a report candidate.

When several agents rediscover related flaws, consolidate by root and shared fix. Do not create one report per exploit story.

## Common misleading distinctions

### Different sink after the same unsafe object creation

A public fix that rejects escaping symlink targets at materialization may also block a later same-invocation overwrite through a reserved filename. The later write makes impact clearer but usually does not create a distinct root.

### Different payload after the same missing integrity check

Writing executable bytes, poisoning metadata, or corrupting a cache are consequences of accepting bytes without verifying the claimed digest. If one public patch recomputes and enforces the digest before all consumers, those stories group together.

### Successful-path logging versus malformed-error logging

These can be technically different sinks. But when an open patch already states that live credentials must not enter logs/errors in the same method and its diff exposes the successful-path logging, grouping risk is high. Continue only if the program rewards incomplete-fix expansions and the remediation is demonstrably independent.

### CI execution without a privileged sink

External code execution on a GitHub-hosted lint or review job is not an approval bypass by itself. Require a secret, write token, OIDC exchange, signing/publish/deploy action, self-hosted boundary, privileged artifact consumer, or another concrete capability beyond intended untrusted CI execution.

## Disposition language

Use precise labels:

- `confirmed_technical_duplicate_no_submit`
- `same_root_consequence_no_submit`
- `adjacent_public_family_high_grouping_risk`
- `incomplete_fix_candidate_current_source_proven`
- `distinct_root_candidate`
- `repository_saturated_pivot`

Record:

- candidate source chain;
- matching public URL and patch;
- shared and distinct mechanisms;
- two-way remediation result;
- whether local reproduction was performed;
- why more reproduction was stopped;
- next pivot.

## Completion checklist

- [ ] Current commit/default branch is pinned; do not assume `main`.
- [ ] Open and closed issues/PRs were searched by symptom and mechanism.
- [ ] Matching PR bodies and diffs—not only titles—were read.
- [ ] Advisories touching the same method have an explicit invariant differential.
- [ ] The two-way remediation test was recorded.
- [ ] A different exploit story was not mistaken for a different vulnerability.
- [ ] Parallel-agent claims were independently source-checked before promotion.
- [ ] Active hardening-series saturation was considered.
- [ ] Duplicate controls are retained but not framed as fresh findings.
- [ ] The vault/checkpoint/report statuses agree after the final decision.
