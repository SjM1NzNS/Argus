# CI review-lifecycle and branch-protection gates

Use this reference when a finding depends on pull-request approval state, workflow event coverage, bot-driven merge decisions, or repository protection settings.

## 1. Establish incremental capability before promoting CI execution

Contributor-controlled code executing in an explicitly untrusted builder is often intended behavior. Run this counterfactual first:

- Can an ordinary contributor already execute equivalent build logic on the same worker class?
- Is the worker documented as disposable/untrusted?
- Does the candidate reach a different boundary: source merge, trusted artifact publication, secrets, signing, deployment, trusted workers, or durable cross-build state?

If the answer stops at intended untrusted execution, keep the route as architecture evidence or a counterfactual—not a standalone finding. Promote only the concrete boundary crossing.

For a sensitive CI-configuration bypass, explicitly test lower-precondition baselines before calling the sink new execution or worker compromise:

- unchanged approved task configuration plus contributor-controlled source, patch, overlay, build rule, module extension, or test target;
- a separate ordinary fork/project pipeline that consumes contributor-controlled build files without the disputed label, approval, prior-contribution, or maintainer role;
- the exact queue, container/host context, mounts, identity, environment, and credential exposure reached by each route.

Compare prerequisites and capabilities, not just input syntax. Direct `shell_commands` can be an authorization-policy bypass without being incremental RCE when an ordinary build action already reaches the same privileged worker boundary. In that case, limit impact to the unique delta—such as task/platform selection or CI-resource use—and require a protected queue, distinct credential, trusted consumer, source write, publication, or distributed-artifact edge before promoting a security report.

## 2. Compose the complete PR lifecycle

Audit workflows and reviewer bots together rather than one file at a time:

1. List every workflow event and activity type (`opened`, `synchronize`, `reopened`, `edited`, review events, schedules).
2. Record `branches:` semantics and which PR base/ref each filter evaluates.
3. Check whether scheduled jobs enumerate all open PRs or re-check the expected base branch.
4. Model base retargeting, pushes while targeting an alternate base, retarget-back, force-push, reopen, and label/review persistence.
5. Trace the final authorization sink: label grant, bot approval, merge API, artifact publication, or deployment.
6. Re-check the exact head SHA and base immediately before the sink.

A workflow that handles `synchronize` only for the protected base may be skipped when a push occurs while the PR targets another base. If `edited` is omitted, retarget transitions may receive no invalidation at all.

## 3. Approval freshness must be identity-bound

Treat these as unsafe authorization clocks unless independently bound to the current head:

- commit author date;
- commit committer date;
- PR update time;
- mutable labels;
- review submission time alone.

Review freshness should verify at minimum:

```text
review.state == APPROVED
review.commit_id == current_head_sha
current_base == expected_protected_base
```

Author-controlled commit dates are not a substitute for `review.commit_id`. A final merge routine that checks only that the head has not changed since the bot began processing does not prove that a human approved that head.

## 4. Use a stateful exact-code harness

For safe local proof, load the repository's exact pinned action/module and mock only external APIs. Preserve state across calls:

- PR base and current head;
- commits with author/committer timestamps;
- reviews with `commit_id`, state, reviewer, and submission time;
- labels;
- bot review calls;
- merge calls and the head merged;
- dismissal and review-request calls;
- workflow-run observations.

Test both:

- **Positive lifecycle:** old approval survives the event/base gap and reaches the sink on a different head.
- **Negative counterfactual:** run the intended dismissal or exact-head check first; approval/merge/label effects must disappear.

Prefer a same-object/same-module lane when it exercises a stronger branch such as direct auto-merge. Keep mixed-object lanes only when they prove a separate precondition such as label grant without merge.

## 5. Deployment configuration is a hard false-positive gate

Source composition can prove a vulnerable decision path while live repository protection independently blocks it. Before an unqualified production claim, verify:

- native stale-review dismissal;
- required approving-review count;
- last-pusher approval restrictions;
- code-owner requirements;
- merge queue/rulesets;
- legacy branch protection distinct from public rulesets.

Public rulesets pages do not necessarily disclose legacy branch protection. If a passive unauthenticated branch-protection API request returns `401 Requires authentication` while rate-limit capacity remains, conclude only:

- the endpoint requires authentication;
- the setting remains unknown;
- the gate is neither passed nor falsified.

Do not infer that protection is absent. Do not use a token or signed-in browser without explicit authorization. Record the response headers/body and queue an authorized read-only settings check.

## 6. When the authorized settings check is access-blocked

After explicit authorization, exhaust available **read-only** access without converting the check into credential extraction:

1. Check for an already configured CLI/session/token by presence and capability only; never print secret values.
   - If the standard client is absent and installation is safe and authorized, install it from an official release or package source and verify its checksum/signature instead of treating binary absence as the access blocker.
   - Keep **tool availability**, **authentication**, and **repository authorization** as three separate gates. An installed client does not create a session, and an authenticated ordinary account may still lack repository-administration visibility.
2. Treat repository settings-page `404` responses as access-hiding behavior, not evidence that rules are absent.
3. If a signed-in browser cannot be controlled through the approved background interface, stop rather than scraping cookies, session databases, OAuth tokens, or password material.
4. Preserve the precise blocker: missing repository-admin visibility is different from a negative configuration result.

A bounded public-history control can add production context while the configuration remains inaccessible:

- query the repository issue-event endpoint for `base_ref_changed`, `review_dismissed`, and `head_ref_force_pushed`;
- set a page/time budget before retrieval and stop at that boundary;
- select a few source-derived PRs and preserve their reviews, commits, and timelines;
- attribute dismissals to the actual actor so custom workflow behavior is not misreported as native branch protection;
- distinguish ordinary post-review pushes from the exact retarget lifecycle under test.

Interpretation rules:

- Public `review_dismissed` events attributed to a repository bot/app prove that the custom dismissal path operates for those observed lifecycles.
- Zero `base_ref_changed` events in a bounded window means no matching public control was observed; it does **not** prove retargeting is impossible or native dismissal is disabled.
- Historical timelines cannot replace the decisive legacy protection field or an owned exact-lifecycle control.
- If no matching lifecycle exists, keep the finding conditional and request a repository administrator's read-only capture of `required_pull_request_reviews.dismiss_stale_reviews` plus any ruleset covering the protected base.

Preserve raw headers and bodies separately from the interpretation note. For larger bounded event sets, record a deterministic manifest digest over ordered filenames and body hashes, then extend the finding verifier to assert page counts, event counts, selected control records, the manifest digest, and absence of truncation artifacts. If a verifier fails after report wording changes, repair the artifact/verifier contract and rerun the exact-code harness plus all reconciliation checks before reporting success.

## 7. Close the post-merge publication edge

A trusted merge is often only the first half of a supply-chain claim. Before stopping at “source integrity,” determine whether ordinary merged content reaches a registry, package manager, release bucket, deployment, mirror, update channel, or resolver used by consumers.

Use a bounded, read-only production control:

1. Select a recent ordinary merged change that added or modified a uniquely identifiable, consumer-visible object.
2. Preserve the PR API metadata and file list so the merge timestamp, merge SHA, changed paths, and add/modify states are source-bound.
3. Fetch the object from the default branch and from the live publication endpoint, saving bodies and response headers separately.
4. Compare byte lengths and cryptographic hashes; byte identity is stronger than semantic similarity.
5. Inspect live `Last-Modified`, generation, ETag, or equivalent provenance headers and calculate the exact lag from merge to publication.
6. Check resolver/index metadata as well as the object itself so “uploaded” is not confused with “consumer-visible.”
7. Bind the endpoint to actual consumers using first-party documentation: default registry behavior, package-manager defaults, mirror semantics, or deployment architecture.
8. Map the proven chain to the program's current severity/rules language rather than assigning “Critical” from intuition.

Interpretation rules:

- A recent merged object that appears byte-identically in a live default registry within seconds or minutes strongly corroborates the **ordinary main-to-publication edge**.
- This does not identify the private sync trigger or credentials, and it does not prove that the candidate bypasses merge enforcement. Keep those gates separate.
- Do not claim affected users, malicious publication, or arbitrary payload acceptance unless separately demonstrated.
- Once both the authorization bypass and ordinary publication sink are proven, describe the result as one composed root cause with a stronger supply-chain impact—not as two bugs.
- Preserve a deterministic manifest over raw API responses, bodies, and headers, and extend the verifier to assert merge metadata, changed paths, body equality, timestamps, resolver visibility, hashes, and non-claims.

## 8. Reporting language

Use a conditional disposition until deployment controls are known:

> Exact workflow/action composition and local authorization-sink behavior are proven. Production exploitability remains conditional on the repository's native branch-protection dismissal settings, which are not publicly readable.

Separate these proof levels:

- exact local bot decision;
- live GitHub merge enforcement;
- post-merge publication/consumer impact.

Do not collapse a mocked merge call into a live merge, or a source merge into downstream package compromise without proving each subsequent edge.

## Evidence checklist

- [ ] Exact repository and action commits/pins recorded.
- [ ] Event/activity/base filters enumerated.
- [ ] Scheduled-job base filtering checked.
- [ ] Review `commit_id` binding checked.
- [ ] Author-controlled timestamps identified.
- [ ] Positive lifecycle and dismissal/head-binding counterfactual pass.
- [ ] Exact head passed to bot approval/merge recorded.
- [ ] Intended-untrusted-execution counterfactual completed.
- [ ] Native ruleset/legacy protection gate resolved or explicitly blocked.
- [ ] Tool availability, account authentication, and repository authorization recorded as separate states.
- [ ] No authenticated access or target mutation without authorization.
- [ ] Recent ordinary merge bound to live publication object with PR metadata/files preserved.
- [ ] Default-branch and live bodies hash-identical, or differences explicitly explained.
- [ ] Publication lag calculated from merge time and live provenance headers.
- [ ] Resolver/index visibility and first-party consumer/default documentation checked.
- [ ] Program severity language mapped to the composed chain without claiming affected users.
- [ ] Raw publication captures included in a deterministic manifest and verifier.
- [ ] Impact stops at the highest proven trust transition.
