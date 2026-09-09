# Static CI Credential-Capability Proof

Use this method when a source-confirmed CI trust crossing can expose a secret, but the credential's live presence, scopes, account grants, or downstream permissions are not safely observable.

## Objective

Replace the weak conclusion “impact depends on unknown token permissions” with the strongest source-supported capability statement, while separating:

1. **demonstrated execution** — attacker-controlled code reaches the credential-bearing context;
2. **source-confirmed intended use** — exact operations the repository performs with that credential;
3. **documented configuration intent** — comments or setup docs describing expected scopes;
4. **conditional downstream impact** — paths requiring branch rules, environments, approvals, or another credential;
5. **unproven live state** — current secret presence, validity, scopes, repository grants, or bypass status.

Do not access, print, hash, exfiltrate, or exercise a real production credential merely to upgrade an impact claim.

## Reportability: intended primitives versus unintended composition

Do not dismiss a CI finding because Git hooks, cache restoration, workflow dispatch, or secret injection each behave as documented. Ask whether their **composition violates the workflow's stated trust boundary**. Strong reportability indicators include:

- untrusted code is deliberately isolated from credentials;
- a later “clean” job receives a secret;
- executable metadata, configuration, artifacts, or workspace state from the untrusted job is restored into that trusted job;
- the trusted job automatically invokes the transferred state;
- repository comments, history, or design discussion show that job separation was the intended mitigation.

Manual maintainer review/dispatch, first-cache ownership, exact restore, and reaching the privileged sink are exploitability prerequisites and should be prominent limitations. They are not an `accepted_behavior` disposition by themselves when the maintainer intended to approve a narrow operation—not arbitrary execution in the credential-bearing job.

A report can be worthy on trusted-job code execution plus concrete repository-automation authority even when package publication, protected-branch bypass, and private-repository access remain unproven. Lead with the defeated boundary and exact credential uses; keep conditional release/OIDC chains secondary.

## Procedure

### 1. Pin the source boundary

Record the exact repository commit/tag and whether the clone is shallow. Hash the source files used as evidence. Treat mutable external Actions, default-branch checkouts, and unpinned helper repositories as time-dependent evidence, not as properties pinned by the reviewed commit.

### 2. Inventory every secret reference

Search the complete fixed tree for the exact secret name and aliases assigned from it, such as `GH_TOKEN`, `GITHUB_TOKEN`, `NODE_AUTH_TOKEN`, or tool-specific variables.

Produce a deterministic list of every file and line. Count both **unique files** and **exact occurrences**; assert both counts plus the per-file line map in the final verifier so repeated references, comments, aliases, later additions, or omissions fail visibly.

For each reference, record whether the secret is bound at workflow, job, step, action-input, or command scope. A secret name in one workflow does not imply it is available in another. Treat comments that explain why the secret is needed as permission-intent evidence, but keep them distinct from actual secret bindings.

### 3. Map credential-bearing sinks

Trace each alias to exact operations and targets:

- `git push`, remote URL, destination ref, force mode, tag, or branch;
- `gh api` endpoint and method;
- PR/issue create, update, comment, merge, label, or review operations;
- workflow dispatch, rerun, artifact read, or run-management operations;
- release creation/upload;
- registry login/publish;
- deployment or environment actions;
- cross-repository checkout or push.

Preserve the target repository/ref and all prerequisites. Distinguish a same-repository branch push from a selected PR-head push, fork write, protected-branch write, or cross-repository write.

Also map **credential-exposure boundaries**, even when the credential is not yet at a final API sink:

- unpinned external repository/default-branch checkout receiving the secret;
- dependency installation or lifecycle scripts executed with the secret in scope;
- privileged `workflow_run` jobs consuming PR-influenced artifacts;
- mutable Actions or helper scripts invoked while the secret is present.

For external or mutable code not contained in the pinned tree, record that the exposure is source-confirmed but concrete downstream sinks are time-dependent and not fixed by the reviewed commit.

### 4. Treat scope comments as intent, not live proof

Repository comments such as “requires `repo`, `read:org`, and write access” materially support intended configuration. Quote them exactly and normalize naming only with an explicit note.

They do **not** prove:

- the secret currently exists or is nonempty;
- the token is valid;
- actual granted scopes;
- the owning account's repository set;
- SSO authorization;
- branch/ruleset bypass;
- environment approval or registry authority.

Phrase the result as “source-documented intended permission” or “credential intended for these operations,” not “verified live permission.”

### 5. Trace separate credential boundaries

Inventory all release, package, tag, deployment, and cross-repository workflows independently. Record every credential source:

- separate PAT or GitHub App token;
- default `GITHUB_TOKEN` plus declared permissions;
- OIDC `id-token: write`;
- registry secret;
- protected environment;
- manual approval or `release_created` output.

Never attribute one credential's operations to another merely because both belong to the same bot identity or repository.

A package workflow in the repository does not prove the compromised token can publish. If publishing uses another token or OIDC, classify direct publication through the compromised token as **disproved by source** unless another exact path exists.

### 6. Model indirect paths with gates

An indirect path may exist when the compromised credential can influence a branch, tag, PR, artifact, or workflow that later receives stronger credentials. Write it as a gate chain:

```text
credential write authority
  -> permitted target branch/tag
  -> branch/ruleset/approval conditions
  -> trusted workflow trigger
  -> release or deployment gate
  -> stronger credential/OIDC operation
```

If any required write, merge, bypass, environment, or release condition is absent from source, disposition the chain as **conditional**, not proven.

For branch-triggered OIDC publication or deployment paths, enumerate these gates separately instead of collapsing them into “can push a branch”:

1. authority to create or update a branch matching the workflow trigger;
2. authority to add or modify the workflow file when the path requires attacker-controlled workflow code;
3. repository Actions policy accepting that branch/ref and workflow;
4. environment, approval, or release-output conditions;
5. registry/trusted-publisher acceptance of the repository, workflow, environment, and ref identity;
6. package/version/provenance checks performed by publish scripts.

A source-visible branch trigger plus `id-token: write` is a **concrete conditional owner-validation lead**, not package takeover proof. Conversely, do not dismiss it as purely speculative when the exact trigger and privileged sink are present—record the missing gates precisely.

### 7. Use history carefully

Local Git history can corroborate bot-attributed automation and release patterns, but:

- shallow clones make provenance and parent analysis incomplete;
- author/committer fields are not authentication proof;
- a bot identity may use multiple distinct tokens.

Use history as supporting context, never as the sole permission proof.

### 8. Keep optional public metadata separate

Branch `protected` flags, rulesets, Actions settings, and package metadata may improve the model when obtained through separately approved read-only collection. If the task is local-only or a metadata lookup is blocked, do not work around it. Record that the setting remains unproven and complete the source proof without it.

When background reviewers were dispatched before the user narrows scope, their already-running public-metadata work may finish afterward. Do not silently present the result as local-only and do not use it to prove permissions. Record that public unauthenticated metadata was observed, distinguish it from authenticated/live-credential access, exclude it from the fixed-source permission proof unless the user permits its use, and adjudicate the remaining local findings independently.

### 9. Produce dual evidence

Create:

- a human-readable capability map with exact `path:line` citations;
- machine-readable JSON containing source commit, secret-reference count/files, direct operations, target refs/repositories, separate credentials, claim dispositions, and explicit non-actions.

Recommended disposition vocabulary:

| State | Meaning |
|---|---|
| `source-confirmed` | Exact operation and target are present in pinned source |
| `strongly source-supported` | Intended capability is shown by concrete sinks but live success was not observed |
| `configuration intent` | Comment/docs describe expected scopes or access |
| `conditional only` | Additional unobserved policy/credential gates are required |
| `disproved by source` | Exact examined path uses a separate credential or cannot reach the claimed sink |
| `unproven` | Source cannot reveal the required live state |

### 10. Run an adversarial claim-kill gate

Before promotion, fail the audit if the report says or implies:

- live token scopes were confirmed;
- protected branches can be bypassed without ruleset evidence;
- specific private repositories are reachable from a broad scope comment;
- package publication follows merely because a release workflow exists;
- cross-repository access belongs to the compromised token when source uses another credential;
- two credentials are equivalent merely because they share a bot account, author identity, or naming convention.

Independently adjudicate parallel-review results before promotion. A reviewer summary is a lead, not evidence: re-check the cited source, reject conclusions that conflate secret names or principals, preserve valid conditional paths with their missing gates, and record the adjudication. Do not average contradictory reviewers into ambiguous wording.

Validate evidence schemas using their actual current field names rather than assumptions copied from an older audit wrapper. Run the final hash/audit only after the last report and ledger edit.

## Strongest safe impact wording

Use this pattern:

> If the secret is configured as the workflow expects, attacker-controlled code can capture a credential that the pinned source explicitly uses for [exact operations] against [exact repository/ref targets]. Resulting authority is bounded by the credential owner's live grants and repository policy. [Named higher-impact outcomes] remain conditional or unproven because [specific separate credential or missing policy gate].

## Verification checklist

- [ ] Exact fixed commit/tag and shallow-clone state recorded.
- [ ] Every secret reference and alias inventoried; unique-file count, exact-occurrence count, and per-file line map agree.
- [ ] Every credential-bearing sink has a target repository/ref and method.
- [ ] Mutable external checkouts, dependency lifecycle execution, and privileged artifact consumers receiving the secret are recorded as exposure boundaries.
- [ ] Scope comments are labeled configuration intent.
- [ ] Release/package/deployment workflows were traced separately.
- [ ] Separate PAT, default token, OIDC, registry, and environment boundaries are not conflated—even when they share a bot identity.
- [ ] Indirect impact includes every branch, workflow-file, Actions-policy, merge, ruleset, environment, registry-trust, release, and approval gate.
- [ ] Parallel-review conclusions were source-checked and contradictions explicitly adjudicated.
- [ ] Public unauthenticated metadata, authenticated API use, and fixed-source proof are labeled separately.
- [ ] Live secret presence/scopes and specific private-repository access remain explicit non-claims unless authoritatively proven.
- [ ] Human and machine-readable evidence agree.
- [ ] Overclaim and credential-pattern scans pass.
- [ ] Final artifact hashes were generated after all edits.
