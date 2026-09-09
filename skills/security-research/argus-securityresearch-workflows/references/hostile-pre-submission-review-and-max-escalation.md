# Hostile Pre-Submission Review and Maximum Escalation

Use this gate after a technical exploit chain is reproducible but before marking a bounty finding `GO`, assigning severity, or preparing a submission.

## Objective

Separate four questions that are often incorrectly collapsed:

1. **Does the state transition or sink exist?**
2. **What literal capability follows?**
3. **Does that capability cross a meaningful security boundary for this target?**
4. **Is the root cause and impact novel enough to justify submission?**

A passing exploit control answers only the first question unless the remaining three are independently supported.

## Review sequence

### 1. Re-prove the exact chain

- Pin every repository, action, workflow, and runtime source revision.
- Reconstruct actor → prerequisite → authorization → head/state change → validation decision → sink.
- Verify whether authorization is bound to the reviewed SHA, sensitive-diff digest, object, principal, and expiry.
- Add negative controls for label/token absent, changed head, dismissed approval, blocked merge, and no sink.
- Keep local mocks honest: extract current functions or ASTs instead of paraphrasing behavior.

### 2. Split literal capability from incremental impact

Ask what the actor could already do through intended product behavior.

- A privileged container, host socket, or shell sink can prove literal host control.
- It does **not** automatically prove a new security boundary if the pool is intentionally untrusted and already executes contributor-controlled workloads.
- Identify the capability delta over the actor's normal role. If the result is only resource use or control of a disposable untrusted worker, say so.
- Search source, design docs, maintainer statements, and existing hardening comments for the intended trust model and equivalent-capability paths.

### 3. Expand post-compromise one boundary at a time

Review these branches without interacting with live credentials or infrastructure:

- host mounts and daemon sockets;
- metadata/service-account identity and OAuth scopes;
- agent registration material, queue/cluster/org scope, and expiry;
- writable agent state and persistence lifecycle;
- caches, artifacts, statuses, logs, and cross-job consumers;
- trusted versus untrusted organizations/projects/queues;
- main-branch writes, merge controls, postsubmit publication, release signing, and user-distributed artifacts.

Classify each claim:

| Tier | Meaning |
|---|---|
| Confirmed | Exact source/runtime evidence proves the capability. |
| Strong static consequence | Follows from documented platform behavior plus pinned target configuration, but was not exercised live. |
| Plausible only | Requires unknown IAM, token validity/scope, consumer behavior, or another unverified condition. |
| Excluded | Source or negative controls show the boundary is separate or the chain stops earlier. |

For intentionally untrusted CI, do not equate “untrusted” with “contains no reusable control-plane authority.” Continue source review through:

- host-readable agent registration tokens and their organization/queue tags;
- shared worker service accounts or managed identities;
- secret-manager paths intentionally used by sibling pipelines on the same identity;
- API-client operations proven by code and call sites, not merely token names;
- durable external builds, retries, caches, pointers/state, and artifact namespaces after one-job VM shutdown;
- exact trusted/untrusted org, project, service-account, registry, cache, artifact, and signing separation.

A public maintainer statement about intended isolation is a claim to test against bootstrap and infrastructure source. If source shows reusable same-organization agent material or intended cross-pipeline API authority, the impact may exceed one disposable VM while still stopping short of trusted/release compromise.

Never promote plausible credentials, rogue-agent registration, cache poisoning, or artifact tampering to demonstrated impact without the missing scope/consumer evidence. Phrase them as source-supported post-compromise consequences, and record that no live credential, IAM, agent, metadata, cache, artifact, or API operation occurred.

### 4. Run a hostile prior-art search

Do this even when an initial exact-phrase search was empty.

Search public issues, PRs, commits, discussions, and security PoCs using:

- exact control names, labels, skip flags, validation names, and function names;
- the sink (`shell`, workflow dispatch, artifact upload, publication, signing, etc.);
- impact terms (`arbitrary code`, `RCE`, `approval bypass`, `TOCTOU`);
- disclosure terms (`security-poc`, `VRP`, `bug bounty`, `responsible disclosure`);
- maintainer comments explaining whether the destination is trusted or intentionally untrusted.

Record whether prior art shares the **state transition**, **root cause**, **sink**, or only generic impact. A distinct state machine may still be grouped as a variant when the same control-to-sink root cause was already reported. Absence of the exact new phrase is not novelty proof.

### 5. Re-check current program fit

- Fetch current official scope/tier and reward rules.
- Check approval-bypass/TOCTOU language, root-cause grouping, duplicate policy, and required user-facing outcomes.
- For supply-chain claims, require a bridge to source integrity, published artifacts, package consumers, release signing, or another stated program outcome—not merely CI host control.
- Treat a public maintainer's trust-model statement as strong impact context, but not as the final program decision.

### 6. Review as a skeptical triager

Write the strongest rejection arguments first:

1. intended/equivalent capability;
2. no meaningful trust-boundary crossing;
3. duplicate or close variant;
4. missing live/runtime evidence;
5. prerequisite too privileged or social;
6. no user/source/publication impact;
7. severity overclaim.

For each, label the objection decisive, strong, moderate, or weak and provide the best honest rebuttal. Score technical validity, exploitability, incremental impact, program fit, novelty, evidence quality, and expected ROI separately.

Treat independent/delegated reviews as unverified leads until the parent checks exact raw captures, pinned source ranges, created files, regenerated evidence, and shared-worktree side effects. A reviewer verdict of **NO-GO as written** is not necessarily a terminal finding disposition: separate defects that invalidate the finding from remediable evidence/wording gaps. After correcting mandatory edits or discovering a stronger source-supported boundary, rerun the hostile review against the new canonical state rather than mechanically preserving the earlier verdict.

When reviews disagree, write a reconciliation table:

| Question | Technical reviewer | Escalation reviewer | Skeptical triager | Parent-verified resolution |
|---|---|---|---|---|

The final disposition must cite which objections were corrected, which remain strategic risks, and which claims were narrowed or expanded. Never let an asynchronous completion message silently override a package that was already declared final; a conclusion-changing review invalidates that package.

### 7. Choose an explicit disposition

- **GO:** chain, incremental boundary, program outcome, and novelty are all supported.
- **HOLD / narrow variant:** technical issue is real, but impact or duplicate risk prevents a high-confidence recommendation.
- **NO-GO as framed:** former severity/impact wording is misleading; preserve the technical finding only as hardening or possible-credit material.

Do not let earlier effort, packaging, or a previous `GO` status bias this decision.

### 8. Reconcile artifacts when the verdict changes

- Update the report's severity, impact, prior-art, explicit non-claims, and concise triage statement.
- Preserve earlier finding history in ledgers; append a superseding review rather than erasing it.
- Add a machine-readable worker/trust-boundary record and a condensed public-prior-art snapshot.
- Rebuild the private package and rerun all controls after the final build.
- Compare canonical report/evidence copies against packaged copies and verify archive checksums, ZIP integrity, and secret scans.
- In semantic verifiers, test expected booleans and numeric sentinels explicitly; avoid `all(mapping.values())` when a valid expected value may be `0`.

## Common failure modes

- Calling generic Docker-socket impact target-specific proof.
- Treating an intentionally untrusted runner as a trusted infrastructure boundary.
- Describing credentials as accessed when only exposure is source-supported.
- Declaring novelty after searching only the exact new state-transition phrase.
- Ignoring prior public security PoCs because their actor path differs.
- Treating a program's TOCTOU example as sufficient without the required impact outcome.
- Keeping `High` because the technical chain is elegant even after impact controls fail.
- Rebuilding a package before the report/qualification files are final, causing hash churn and stale copies.

## Minimum output

Produce:

1. a maximum-escalation table with confirmed/plausible/excluded tiers;
2. a hostile rejection analysis;
3. a prior-art/root-cause comparison;
4. an explicit GO/HOLD/NO-GO verdict;
5. updated ledgers and a verified private package when conclusions changed;
6. an explicit statement that no live target, credential, CI, worker, artifact, or submission action occurred unless separately authorized.
