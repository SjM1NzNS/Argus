# CI Head-Bound Authorization and Public Lifecycle Controls

Use this reference when CI execution, sensitive configuration, deployment, or publication is unlocked by a persistent label, approval, comment command, environment flag, check result, or manually unblocked build.

## Core invariant

Authorization for attacker-controlled CI input must be bound to the exact reviewed state:

```text
authorization.subject == current_head_sha
```

For sensitive configuration, strengthen this to:

```text
authorization.subject == (current_head_sha, sensitive_diff_digest)
```

A review being dismissed after a push is insufficient if a separate persistent authorization marker survives and the CI sink trusts that marker.

## Source-first workflow

### 1. Pin every independently moving object

Record separately:

- target repository commit;
- workflow file and exact action reference;
- exact executable action commit;
- current companion/deployment repository commit;
- generated/bundled action entrypoint actually invoked;
- worker/infrastructure source commit;
- capture timestamp and clean/shallow state.

Do not substitute a nearby companion checkout for an action pinned by SHA. Fetch or recover the exact action object, then compare it with current source. A clean current checkout does not prove the pinned executable was reviewed.

### 2. Model authorization as a state machine

Build a transition table before testing:

| Transition | Head | Review | Persistent marker | Expected security behavior |
|---|---|---|---|---|
| Initial PR | H1 | none | absent | sensitive CI blocked |
| Reviewed benign state | H1 | approved | added | sensitive CI may run for H1 |
| Synchronize/push | H2 | dismissed/stale | ? | marker must be revoked or H2 must be reauthorized |
| Scheduled/review rerun | H2 | none | ? | stale marker must not suppress validation |

Trace every workflow event that can alter review or marker state: `opened`, `reopened`, `synchronize`, `labeled`, `unlabeled`, scheduled scans, review submission/dismissal, force-push, and merge queue updates.

Search for both grant and revocation. `addLabels()` plus review dismissal with no `removeLabel()`/head binding is a high-signal differential, not proof by itself.

### 2a. Audit base-ref detours and review freshness separately

A head-changing push may escape the intended invalidation workflow if the PR temporarily targets another base. Treat base and head as independent authorization subjects.

For every reviewer/dismissal composition, inventory:

- whether base changes emit `edited` and whether that activity is subscribed;
- whether `branches:` / `branches-ignore:` filters are evaluated against the PR base;
- whether `synchronize` invalidation is skipped while the PR targets an alternate branch;
- whether scheduled reviewers enumerate all open PRs or explicitly request/re-check the protected base;
- whether a retarget back to the protected branch itself triggers invalidation;
- whether review validity uses `review.commit_id == current_head_sha`, or instead relies on author/committer timestamps;
- whether the author date is attacker-controlled and can make an older review appear newer than the current commit;
- whether native branch protection independently dismisses stale approvals even when the custom workflow misses the event.

A public rulesets page showing no rulesets does not prove legacy branch protection is absent. Treat native stale-review dismissal as a deployment gate that needs an authoritative read-only configuration view or a safe passive control. The existence of a custom dismissal workflow is supporting intent evidence, not conclusive proof that native dismissal is disabled.

Build the lifecycle table over `(base_ref, head_sha, review.commit_id, review.state, authorization marker)`, not only `(head, review, marker)`. Require a final base/head re-check immediately before any bot approval, merge, deployment, or publication call.

### 3. Construct both no-race and strongest-sink local controls

Avoid exploit stories that depend on winning auto-merge. First keep merge closed independently while testing CI authorization. Generic pattern:

1. Change two independently approved objects/modules.
2. Obtain legitimate approval for only object A on benign head H1.
3. Confirm a global CI marker is granted from `anyApproved` while `allApproved` remains false.
4. Move to H2 and change sensitive configuration for object B.
5. Execute the exact synchronize/dismissal handler.
6. Re-run the exact reviewer/scheduler logic.
7. Assert:
   - old approval is dismissed;
   - marker remains;
   - no revocation API was called;
   - H2 is not revalidated before marker trust;
   - merge remains closed.

Then add a **same-object strongest-sink lane** rather than assuming the merge-closed control captures maximum impact:

1. Keep only the object/module that the historical reviewer was authorized to approve.
2. Move to an unreviewed current head through the suspected lifecycle gap.
3. Execute the exact reviewer and merge logic.
4. Assert separately whether the stale review causes `allApproved`, a bot-authored approval, merge API invocation on the current head, publication, or another source-control decision.
5. Run the existing dismissal/revocation handler first as a causal counterfactual; the stronger sink must disappear.

This second lane can convert a same-untrusted-worker CI story into a source-integrity or publication authorization bypass. It may also remove prerequisites such as a persistent label, prior contribution, or a second head transition. Do not stop after proving `anyApproved`/marker grant when `allApproved` reaches a materially stronger sink.

Use mutable local API mocks around the exact pinned entrypoint. Preserve call logs and state snapshots. If exact code prints diagnostics, write canonical JSON evidence directly from the harness and validate that file; do not assume redirected stdout is pure JSON.

### 4. Prove the sensitive sink with exact code

Do not stop at “label persists.” Extract or import the exact current functions that:

- read labels/checks/environment;
- decide whether validation blocks;
- add skip flags or remove block steps;
- load attacker-controlled CI config;
- generate job commands;
- invoke shell/process/container execution;
- select queues, workers, credentials, mounts, network modes, or privilege.

Safe differential:

```text
marker absent  -> sensitive validator fails -> block present
marker present -> exact skip flag added      -> block absent
```

Mock the validator/process boundary so no target command executes. Separately verify command forwarding and worker configuration using extracted exact functions or upstream unit tests.

### 5. Use passive public lifecycle evidence

When production gate semantics are uncertain, inspect existing benign public PRs/builds instead of creating a target mutation. Seek one timeline with:

1. marker attached at T1;
2. approval dismissed or rendered stale at T2;
3. newer commit/head at T3;
4. dismissal/check completion at T4;
5. sensitive CI starts after T4 on the newer head;
6. no renewed approval on that head.

Capture PR metadata, commits, reviews, timeline events, current-head checks/statuses, and public build summary. Compare timestamps explicitly. This can prove production persistence and reachability without proving malicious execution.

State provenance limits: a public timeline may prove marker persistence even when it cannot prove whether automation or a human originally applied the marker. Combine it with the exact local grant-path control rather than conflating the two.

### 5a. Generate derived lifecycle evidence from raw captures

Raw captures are authoritative; handwritten summaries are not. Exact timestamps, review IDs, commit SHAs, status counts, and ordering are especially prone to copy/paste or stale-state errors.

For every passive lifecycle summary:

1. inventory the raw files actually present before citing them;
2. derive the summary with a deterministic local script that reads only those files;
3. label mutable state as `head observed in saved captures`, never permanently `current head`;
4. distinguish commit author/committer dates, force-push event time, check start/completion, and status creation time;
5. join dismissed-review timeline objects back to the raw review record by exact ID;
6. count approvals against the exact observed SHA, not against the PR generally;
7. state whether label origin was human, app-attributed, or unproven;
8. record missing captures such as PR metadata, files/diff response, and HTTP headers instead of claiming they exist;
9. preserve raw local mtimes only as filesystem metadata, not HTTP capture timestamps;
10. scan canonical and packaged artifacts for every superseded hash/timestamp/ID before finalization.

The generator output should include its command, raw input names, schema/status, interpretation, non-claims, and missing-evidence list. A regenerated summary changing any packaged byte invalidates the prior archive.

### 5b. Join the state machine and sink into one safe local control

Separate grant-state and sink verifiers are useful, but a skeptical reviewer can still object that the parser, loader, pipeline generator, task selector, and runner were never joined. Build one integrated local control when feasible:

- use exact pinned validation methods and current loader/generator/runner functions;
- demonstrate marker-absent block versus stale-marker suppression;
- feed one structurally valid temporary sensitive configuration;
- assert that its canary survives parsing and appears in the generated worker step;
- exercise the real task-selection and shell-helper path;
- mock only unavoidable SaaS/validator boundaries;
- if a real local process is needed, allowlist one fixed inert command such as `printf` into a temporary directory, record it explicitly, and verify cleanup;
- assert no network, target Docker daemon, metadata service, credential, or external API was contacted.

Record whether the final shell/process call was real or merely captured. Do not describe a recording mock as actual execution or a harmless local canary as production proof.

### 6. Bound worker impact adversarially

Separate:

- untrusted versus trusted CI organizations/projects/queues;
- PR workers versus release/signing/publication workers;
- intended source-build execution versus new sensitive-config execution;
- container compromise versus host compromise;
- worker-local credentials versus separate trusted credentials;
- source-supported facts versus plausible post-compromise capabilities.

A privileged container, host networking, writable agent home, or host Docker socket can make CI command execution a host-boundary compromise. Still do not claim trusted publication, signing, or adjacent projects without a source-supported bridge.

Do not stop the escalation review at “one disposable untrusted VM.” Map the entire same-plane credential and durable-state model from pinned infrastructure source:

- how agent registration tokens are decrypted, stored, scoped, rotated, and tagged to queues/clusters;
- which service account/managed identity backs each queue and which OAuth scope versus IAM role is evidenced;
- secret-manager/KMS paths intentionally used by another pipeline on the same worker identity;
- API-client methods actually implemented and exercised by repository code, including build creation, caller-controlled environment, branch-filter overrides, reads, and retries;
- whether a stolen registration token could enroll another same-organization agent until rotation;
- worker shutdown/replacement versus persistence in external tokens, builds, caches, buckets, or CI state;
- cache namespace inputs and whether repository/pipeline/commit/PR are absent;
- artifact object namespacing and missing IAM needed for cross-build overwrite claims;
- separately named trusted organizations/projects/service accounts, registries, signing credentials, and release workers.

A maintainer statement that an environment is “untrusted” or should contain “no sensitive credentials” is impact context, not a substitute for source review. If pinned bootstrap/client code shows reusable agent material or shared identity access to a cross-pipeline API credential, record that contradiction precisely. Classify the result as source-supported post-compromise capability until live token/IAM/queue scope is safely proven; never say the token was accessed.

Run the incremental-capability counterfactual:

> Could this exact actor already produce the same worker effect through an intended, reviewed path?

If yes, downgrade. If the new head's sensitive configuration was never approved and the actor lacks equivalent intended authority, preserve the incremental execution claim.

### 7. Duplicate and history review

Use history to identify:

- marker-introduction commit;
- earlier dismissal/revocation behavior;
- tests added with the grant path;
- whether grant and revocation were developed independently;
- public issues/PRs mentioning stale labels, head binding, synchronization, or dismissed approval.

Zero public search results are not proof against private duplicates. Phrase them only as “no matching public issue found with these queries.”

### 7a. Make the prior-report distinction a hard submission gate

When a prior report reaches the same CI execution sink, novelty must be established at the authorization/root-cause layer before severity or impact discussion. Do not report a known label, skip flag, arbitrary-command path, runner, or eventual impact as new merely because the new exploit story has different steps.

1. **Capture the prior report verbatim from its direct source.** Preserve the body, title, timestamps, URL, response provenance, and digest. Build the comparison from what the report actually claims, not a remembered summary or later comments.
2. **List the overlap first.** Explicitly enumerate shared marker, validation consumer, command/config sink, worker plane, and impact. These are prior art, not novelty.
3. **Define the candidate as a changed security decision.** State the old authorized subject and the new consumed subject, for example: `authorization valid for H1 -> consumed for H2 after H1 approval dismissal`.
4. **Build a root-cause-isolation lane.** Take a correctly authorized benign H1 as a valid precondition, then exercise only the H1-to-H2 transition. Assert zero calls to the prior report's grant path, zero self-approval/comment-command assumptions, zero merge calls, and no special actor status required by the prior chain. Keep any concrete automatic-grant route as a separate reachability lane, not the root-cause definition.
5. **Run two-way counterfactual remediation tests.** Ask whether head binding/revocation fixes the new candidate while leaving the prior same-head path, and whether the prior report's actor/self-approval/merge fixes leave stale H1-to-H2 authority. Also disclose any broad sink-level fix—such as removing the skip entirely—that blocks both.
6. **Use a report-shape consistency gate.** The title, first paragraph, root-cause section, primary PoC, remediation, and concise triage statement must all center the distinct authorization transition before discussing the shared execution sink. If they instead lead with known RCE/skip behavior, classify the candidate duplicate/no-go.
7. **Preserve grouping uncertainty.** A distinct lifecycle invariant can still be grouped with a prior report at the shared sink or broad root cause. Use `conditional_go_only_as_distinct_root` plus `duplicate_no_go_if_sink_grouped`; never imply that public non-mention excludes private duplication.

A machine-readable differential should record:

- prior-report direct-source URL and body digest;
- shared/known mechanism booleans;
- prior report's stated actor, grant timing, head identity, approval, and merge prerequisites;
- lifecycle elements not identified in that report body;
- root-cause-isolation assertions and excluded prior prerequisites;
- two-way remediation independence plus any shared sink-level fix;
- final reporting gate and explicit prohibited framing.

### 7b. Separate breadth expansion from trust-boundary escalation

After proving sensitive configuration execution, enumerate every attacker-controlled scheduler field—not only the first observed worker. Trace platform names, queue selectors, runner labels, container images, shell-command fields, and concurrency/priority inputs through the exact loader and step generator. A stale authorization may let H2 select Linux, ARM, macOS, or Windows queues even when H1 used only one platform. This is a real breadth expansion, but **cross-platform untrusted execution is not automatically trusted-plane compromise**.

Build the severity decision in four layers:

1. **Execution breadth:** Which exact queues, operating systems, and task fields can the unauthorized state select?
2. **Worker boundary:** Does the generated step expose privileged containers, host networking, Docker sockets, writable agent homes, metadata access, or host configuration?
3. **Reusable authority:** Which agent-registration material, API-client paths, service identities, caches, artifact stores, or durable state survive the original job?
4. **Trust crossing:** Can any confirmed capability reach source write, merge, trusted workers, publication, signing, release registries, or executable trusted inputs?

Keep credential claims capability-specific:

- a plaintext agent token in host configuration reachable through a proven host mount/socket is a confirmed worker credential path;
- a source function that retrieves an API token from Secret Manager proves the retrieval design and implemented API operations, but not that this particular worker identity has live IAM permission;
- a cluster-scoped agent token can support a same-organization rogue-agent hypothesis, but separate Buildkite organizations/clusters remain a hard evidence gate;
- token lifetime, IP restrictions, queue enrollment, and cross-organization access are live-state questions unless captured from authoritative configuration.

Run two counterfactuals before using worker takeover to raise severity:

> Could an intended, authorized untrusted job already reach the same host/token boundary?

If yes, treat that worker-isolation problem as a potentially separate finding rather than unique impact caused by the stale-authorization bug.

> Does the demonstrated capability cross from the designated untrusted plane into a trusted/release/publication plane?

If no, broad same-plane compromise can support High, but do not call it Critical merely because multiple queues, platforms, or agents are affected. A Critical escalation requires source-backed or secret-safe proof of at least one bridge such as trusted-org token access, write access to a trusted base image, executable cross-plane cache/artifact consumption, source merge/write, or release/signing/publication control.

Official Buildkite agent-token scope/lifetime reference: https://buildkite.com/docs/agent/self-hosted/tokens

## Required evidence artifacts

- source-provenance table with exact SHAs;
- local temporal state-machine JSON;
- exact sink differential JSON;
- integrated parser/loader/generator/runner local-control JSON when feasible;
- worker credential, queue, cache, durable-state, and trust-separation source map;
- upstream test output;
- deterministic passive-lifecycle generator, derived summary, and the raw API captures it actually consumes;
- verbatim direct-source capture of any decisive prior report plus a machine-readable root-cause differential;
- root-cause-isolated H1-to-H2 control that excludes the prior report's grant/actor/self-approval/merge prerequisites;
- two-way remediation-independence matrix and shared-sink disclosure;
- claim/non-claim impact boundary;
- verification commands and final hashes;
- session checkpoint before context reset or handoff.

## Remediation pattern

1. Revoke persistent authorization on every head-changing event before or with review dismissal.
2. Bind authorization to exact head SHA and, where practical, a sensitive-diff digest.
3. Represent approval as a head-bound check/status rather than a free-floating label.
4. Require the correct reviewer class for sensitive config; do not reuse `anyApproved` across unrelated objects.
5. Continue validating dangerous configuration even when ordinary CI is authorized.
6. Isolate untrusted jobs: avoid host Docker sockets, privileged containers, host networking, persistent writable agent state, and broad/static credentials.
7. Add regression tests for grant, synchronize, force-push, dismissal, revocation, reauthorization, and unrelated-object approval.

## BCR session example — 2026-07

A Bazel Central Registry review produced several reusable lessons:

- the exact BCR-pinned reviewer action differed from the initially preserved companion BCI checkout, so the exact pinned object was recovered;
- one of two module approvals granted global `presubmit-auto-run` while merge stayed closed;
- synchronize dismissed the review but never removed the label;
- the label caused `--skip_validation=presubmit_yml` and current task `shell_commands` flowed to privileged, host-networked Docker with the host socket;
- an initial hand-authored public-PR summary contained a wrong label timestamp, review ID/commit, and head SHA and cited a raw PR artifact that was not present; a deterministic generator rebuilt it from commits/reviews/timeline/check/status captures and changed `current head` to capture-time `observed head`;
- the public control supported stale-marker persistence and later-head CI reachability but did not prove automatic label origin or malicious production execution;
- a new integrated local control joined task validation, marker gate, current loader, current step generator, current runner selection, and one fixed temporary `printf` canary;
- infrastructure review showed that Linux host control could reach reusable same-organization agent material and a source-defined cross-pipeline Buildkite API-token retrieval path, plus shared cache and selected durable state; the agent path was confirmed from host configuration, while API-token access remained conditional on unproven live IAM;
- exact BCR task generation also showed that attacker-controlled H2 configuration could select macOS, macOS arm64, and Windows queues and accepted `shell_commands`, broadening affected untrusted assets without crossing into the separate trusted organization;
- the severity review therefore separated cross-platform/same-organization breadth from a true trust crossing, and retained High because no trusted-org token, source write, executable cross-plane cache/artifact, release, signing, or publication bridge was proven;
- the incremental-capability counterfactual was applied to worker-token exposure: if an intended authorized untrusted job can already reach the same host credential, that isolation weakness belongs in a separate finding rather than being counted as unique impact of stale authorization;
- close public prior art already disclosed the label, validation skip, arbitrary BCR Presubmit execution, and a same-head module-maintainer auto-grant/self-approval/merge chain;
- the candidate survived the duplicate gate only after a separate exact-action lane began with a valid benign-H1 label and reproduced H1-to-H2 reuse with zero grant, removal, and merge calls, no module-maintainer author, no self-approval, and no comment-command path;
- the final report disclosed that head binding/revocation fixes the lifecycle candidate without fixing the prior same-head path, while removing the shared validation skip blocks both and therefore preserves high duplicate/grouping risk;
- the title, opening, root cause, primary PoC, remediation, and triage statement were rebuilt around the authorization-subject transition rather than known RCE;
- no trusted publication/release/signing crossover was found, and the final disposition was `conditional_go_only_as_distinct_root / duplicate_no_go_if_sink_grouped`;
- the final disposition changed only after reconciling the technical, escalation, prior-art, and skeptical-triager reviews, then rebuilding and revalidating the private package;
- a later lifecycle pass found that the custom dismissal workflow omitted `edited`, applied only to PRs targeting the protected base, while the scheduled reviewer listed every open PR and treated `review.submitted_at >= commit.author.date` as freshness without binding `review.commit_id` to the current head;
- the reusable test sequence was `approved H0 on protected base -> retarget to alternate -> push backdated H1 while alternate -> retarget back -> scheduled review`; a passive owned-repository control established that an external fork author could change the base, without mutating the target repository;
- extending the harness from the mixed-module merge-closed lane to a same-module lane exposed the stronger sink: the stale H0 review satisfied `allModulesApproved`, the bot approved H1, and the exact merge path targeted unreviewed H1; running the existing dismissal first prevented approval and merge;
- this stronger lane needed neither the persistent presubmit label, prior contribution, nor H2, and therefore had to be reported as a source-control authorization candidate rather than worker RCE;
- the direct project-pipeline and unchanged-presubmit archive/overlay paths both reproduced, but adversarial review killed them as standalone findings because current source and maintainer statements treated arbitrary builds on throw-away untrusted workers as intended; they remain counterfactuals against claiming that a harder label path uniquely grants worker execution;
- the base-retarget candidate remained conditional until an authoritative read-only check could resolve native legacy branch-protection stale-review dismissal; a public rulesets page was not treated as proof about legacy protection.

This example is retained as a method illustration, not as authorization to create a live PR, alter a label, trigger third-party CI, inspect real credentials, enroll an agent, or contact cloud metadata/APIs.
