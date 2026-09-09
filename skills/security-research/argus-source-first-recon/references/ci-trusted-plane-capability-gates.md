# CI trusted-plane capability gates

Use this reference after lower-trust CI code execution or worker-host control is established and severity depends on crossing into source, trusted workers, release, signing, publication, or user-consumed artifacts.

## Evidence classes

Keep every edge in one of five classes:

1. **Source-proven:** exact identity, credential, operation, and consumer are connected in pinned source.
2. **Configuration-intended:** source shows a secret lookup/API client or publisher, but deployed IAM, token validity, or effective scopes are absent.
3. **Identity-dependent:** the edge can be answered only from the exact worker/service identity, authoritative deployed IAM, or a secret-safe capability check.
4. **Passive negative evidence:** bounded public records show separation or no overlap; useful, but not mathematical proof.
5. **Disproved:** an explicit namespace, organization, project, credential, cache, artifact, or rebuild boundary kills the proposed path.

Do not collapse configuration intent into a confirmed credential claim.

## Workflow

### 1. Revalidate current source before testing impact

- Record reviewed and current remote commits.
- Diff only the security-relevant paths first: runner/action code, pipeline generators, startup scripts, infrastructure definitions, and release workflows.
- If a workflow pin changed, compare the pinned subtree/object, not only commit IDs:

```bash
git rev-parse OLD:actions/example
git rev-parse NEW:actions/example
git diff --name-only OLD..NEW -- actions/example
```

A pin bump with an identical subtree is not a fix. Conversely, a repository HEAD change outside the relevant paths does not invalidate a pinned review.

### 2. Draw explicit trust planes

For each plane record:

- CI organization, cluster, queue, and agent enrollment token;
- cloud project/account and service identity;
- Secret Manager/KMS lookup project;
- cache, artifact, state, and log namespaces;
- container registry/repository and mutable versus digest-pinned references;
- source-write, release, signing, and publication credentials;
- the exact trusted consumer and whether it rebuilds canonical source.

Shared queue names, `cloud-platform` OAuth scope, `configure-docker`, authenticated pulls, common host naming, or one Terraform backend bucket are not authorization edges by themselves.

### 3. Test a fixed gate matrix

At minimum evaluate:

1. lower-trust agent/API token accepted by the trusted CI organization;
2. lower-trust cloud identity can create/overwrite/delete a mutable trusted image;
3. lower-trust cache is read by a trusted build;
4. lower-trust artifact/log/state becomes executable trusted input;
5. source write or merge without the intended fresh approval;
6. publication/signing material writable before trusted postsubmit;
7. a physical/virtual worker crosses pools without a reliable reset;
8. a trusted Secret Manager/API credential is readable by the lower-trust identity.

For each gate write: source prerequisite, safe test, observed result, missing edge, classification, and severity effect.

### 4. Use passive public checks correctly

Permitted read-only evidence can include bounded anonymous `GET`, `HEAD`, or `OPTIONS` requests, current remote Git reads, public CI job metadata, and public registry manifests.

- Preserve pipeline/build ranges, request count, errors, distinct hostnames, distinct agent IDs, and cross-organization intersections.
- Zero intersection in a bounded sample supports pool separation but never proves universal separation or token rejection.
- A live mutable manifest proves the trusted sink exists. It does not prove the lower-trust identity can write it.
- `OPTIONS`/`405`, public bucket `401`, or anonymous read success only characterize the anonymous caller.
- Never use `POST` to an upload-session endpoint as a “permission probe”; even an empty request can create server state.

### 5. Treat registry bearer tokens as opaque capabilities

A registry token endpoint may return a token after a request for `pull,push` scope without exposing the granted actions. Unless the token has authoritative readable claims or a non-mutating permission endpoint confirms the action, do not call push granted.

Safe conclusions:

- manifest `GET 200` + digest: exact image/tag currently exists and is readable;
- source always-pull + mutable tag: a trusted consumer sink exists;
- no authoritative writer binding: writer edge remains conditional;
- failed or unsupported `OPTIONS`: not an IAM result.

The decisive writer proof is authoritative deployed IAM or an identity-context capability check for exact permissions such as object create plus overwrite/delete or repository upload authority. Do not perform an upload merely to establish severity.

### 6. Require exact identity-context proof

For cross-project registry, bucket, KMS, service-account impersonation, or Secret Manager claims, obtain one of:

- authoritative deployed IAM/configuration naming the exact lower-trust principal; or
- an explicitly authorized, secret-safe `testIamPermissions`/equivalent check executed as that principal.

Do not substitute the research workstation's account, an anonymous caller, or a different CI token. If the exact identity is unavailable, mark the gate `identity-dependent / not passed` rather than “denied” or “allowed.”

### 7. Re-run the local causal controls

After current-source comparison, rerun the exact local state machine, parser/loader/generator/runner harness, boundary model, and upstream regression tests. Record each command and semantic result in machine-readable evidence. Re-run package/final-state verification after the last evidence write.

### 8. Bound severity and reportability

A lower-trust worker compromise can exceed one disposable VM through reusable same-organization agent material, API tokens, queues, or external cache/state. That can support High without proving Critical.

Require at least one proven crossing into source write, trusted-worker execution, executable cross-plane state, release/signing, publication, or unwitting downstream consumption before claiming a trusted supply-chain compromise. If the only open edge is deployed IAM, state the exact permission and principal still needed.

Methodology/RAG sources define false-positive gates; they are not proof of the target's deployed IAM or token scopes.

## Evidence shape

Retain:

- current-source pin/tree comparison;
- gate matrix with classifications;
- passive sample request budget and errors;
- manifest digest but no bearer token value;
- exact missing principal/permission edge;
- local revalidation results;
- explicit non-actions and non-claims;
- whether the canonical report/package was intentionally left unchanged because no stronger chain passed.

## Common pitfalls

- Treating a changed workflow pin as a changed action without comparing subtree hashes.
- Treating requested registry scope as granted scope.
- Treating anonymous access behavior as the worker service account's IAM result.
- Treating queue-name equality across CI organizations as cross-organization scheduling authority.
- Calling zero host overlap proof of impossible pool crossover.
- Calling a mutable image Critical before proving the lower-trust writer.
- Rebuilding a submission package after only negative or conditional escalation evidence.
