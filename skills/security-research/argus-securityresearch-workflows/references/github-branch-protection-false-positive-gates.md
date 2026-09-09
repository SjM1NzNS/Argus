# GitHub branch-protection false-positive gates

Use this reference when a GitHub approval-bypass, stale-review, TOCTOU, or automation candidate appears to reach `pulls.merge`, auto-merge, or a downstream publication sink.

## Core rule

An action-level decision or mocked successful merge is not production proof. Resolve every GitHub-native control that can reject the same head SHA before escalating source integrity or supply-chain impact.

## Read-only control matrix

Capture all surfaces because permissions and visibility differ:

1. Repository permission/viewer permission. Record `READ`, `WRITE`, `ADMIN`, and REST `permissions` fields.
2. `GET /repos/{owner}/{repo}/branches/{branch}`. For public repositories this can expose:
   - `protected`;
   - `protection.required_status_checks.contexts`;
   - `protection.required_status_checks.checks` including `app_id`;
   - `enforcement_level`.
3. `GET /repos/{owner}/{repo}/branches/{branch}/protection`. This commonly requires repository Administration read access. A `403` or `404` is **unknown/access-hidden**, never evidence that protection is absent.
4. `GET /repos/{owner}/{repo}/rulesets?includes_parents=true`.
5. `GET /repos/{owner}/{repo}/rules/branches/{branch}` for active rules applying to the exact branch.
6. GraphQL `branchProtectionRules`. Treat `totalCount: 0` under a read-only viewer skeptically: compare with known protected public repositories to detect visibility filtering.

Preserve raw HTTP body/status and stderr separately. Do not collapse a permission failure into a boolean setting.

## Hard-gate algorithm

1. List every required status context from the live branch record.
2. Bind each context to its producer:
   - workflow file;
   - job name/context;
   - expected app (`app_id`), if specified;
   - exact pinned action/source commit.
3. Replay the proposed PR lifecycle as GitHub event types (`opened`, `synchronize`, `edited`, `reopened`, etc.).
4. Apply workflow `types`, base-branch filters, path filters, and job conditions to the **candidate head SHA**.
5. Remember that required checks are SHA-bound. A success on H0 does not satisfy a required check on H1.
6. Determine whether the latest head can ever receive a successful required check without simultaneously invalidating the stale approval or authorization being exploited.
7. Model the real merge boundary separately:
   - `merge_attempted`;
   - `merge_blocked` and reason;
   - `merged_heads`;
   - labels or downstream side effects after success only.
8. Inspect the action's error handling. A normal `pulls.merge` call that catches `405/not mergeable` does not bypass branch protection.
9. Only compose downstream publication/package/registry impact if the protected-branch merge boundary is reachable.

A separate unknown such as native `dismiss_stale_reviews` can become non-decisive when an independently visible required check already blocks the lifecycle.

## Functional stale-review inference

If direct legacy review settings are admin-only, public timelines can provide supporting—not definitive—evidence:

- bind a PR that remained on the protected base;
- identify a new commit/push;
- identify a later `review_dismissed` event;
- record actor and delta;
- repeated custom-bot dismissals seconds after pushes suggest the custom workflow, not native dismissal, performed the invalidation.

Do not equate this with a direct setting read. It is unnecessary if another native control already kills the impact chain.

## Harness and verifier requirements

A production-aware local harness should import or assert the captured branch-control summary. Never leave `pulls.merge` mocked as unconditional success.

Minimum output:

```json
{
  "bot_approved_head": true,
  "merge_attempts": ["H1"],
  "merge_failures": [{"head": "H1", "reason": "required check missing"}],
  "merged_heads": [],
  "post_merge_labels": []
}
```

The deterministic verifier should fail unless:

- raw branch/rules artifacts exist;
- repository permission is recorded;
- required context, app binding, and enforcement are asserted;
- workflow event/base filters are bound to the latest source commit;
- the report distinguishes approval, merge attempt, and merge success;
- ledgers contain a later correction after any earlier conditional escalation;
- durable artifacts contain no truncation placeholders or credential-like prefixes.

## Credential-safe authenticated reads

- Use official user-mediated GitHub CLI authorization.
- Never copy tokens, browser cookies, passwords, device codes, or credential-store output into evidence.
- `gh auth status` can include a masked/token-bearing line; sanitize that line before persistence, then run a secret-prefix scan.
- Query only read-only endpoints unless the user separately authorizes a controlled mutation.
- Do not create or retarget a live target PR merely to resolve a configuration gate.

## Common false-positive traps

- Checking only `dismiss_stale_reviews` and missing a required status check that independently blocks merge.
- Treating REST `404`, GraphQL `0`, or an empty admin-only object as a disabled setting.
- Trusting an action-level harness whose merge mock ignores live protection.
- Binding workflows from an old commit while branch controls come from current `main`.
- Assuming an `edited` retarget event triggers a workflow subscribed only to `synchronize`.
- Counting a real downstream publication sink as impact before proving the protected merge can occur.
- Reporting bot approval as equivalent to source modification.

## Candidate-family triage after a hard gate

Do not blanket-kill every sibling candidate merely because they share an action, label, or downstream sink. Classify each candidate by the **earliest security boundary it must cross**:

| Candidate class | Decisive boundary | Typical disposition |
|---|---|---|
| Merge/source/publication chain | Latest-SHA required checks, review state, merge permissions | Kill when the protected merge cannot succeed |
| Pre-merge CI execution | Authorization freshness before the presubmit job loads the attacker-controlled head | Can survive even when merge is impossible |
| Eligibility/policy bypass | An explicit policy invariant and incremental privilege | Kill if implementation matches the documented trust model |

A required dismissal/status workflow can therefore have opposite effects on siblings: it may block a merge-dependent candidate while still running successfully on the new head and allowing a stale PR-wide CI authorization to be consumed before merge.

For every candidate in the family, record a binary decision table:

- **Report?** yes/no;
- **Continue?** submission-hardening, hunt for one named missing edge, or stop;
- **Impact boundary:** merge, pre-merge worker, label/state only, or no incremental capability;
- **Resurrection condition:** the specific new evidence that would reverse a kill.

This prevents a valid lower-boundary issue from being discarded with an invalid Critical chain and prevents an action-level quirk from inheriting the impact of a sibling.

## Prior art and shared-sink differential

When a public report already names the same label, validation skip, or execution sink, compare **root causes and counterfactual fixes**, not titles:

1. State the public prior art in the opening section.
2. Isolate the new candidate with the prior report's actor, grant path, self-approval, comment command, and merge path disabled.
3. Ask whether fixing the prior report leaves the new lifecycle defect exploitable, and whether fixing head binding/revocation leaves the prior same-head defect exploitable.
4. Treat a shared downstream sink as high duplicate risk even when the authorization defect is independently necessary.
5. Do not repackage the known sink, generic RCE, or speculative supply-chain consequence as novelty.

Generic external guidance can validate that label persistence across pushes is a recognized TOCTOU class and that authorization should bind to an immutable SHA. It cannot decide a program's duplicate grouping; that decision must remain an explicit risk in the submission.

## Current-pin revalidation before submission

A package built from an earlier action pin is not submission-ready merely because the old harness passes.

1. Capture the current workflow/action pin from the target repository.
2. Diff the exact affected file between the reviewed pin and current pin, for example:

```bash
git diff --unified=5 <old-pin> <current-pin> -- actions/<action>/index.js
```

3. An empty affected-file diff supports unchanged behavior but does not replace execution.
4. Repin the exact-code harness to the current commit and assert the checked-out bytes equal `git show <current-pin>:<path>`.
5. Rerun the root-cause-isolation lane and record current pin, source hash, label grant/removal counts, eligibility revalidation count, merge calls, and boundary reached.
6. If submitting, update source links, report prose, package manifest, and hashes after the repin. Do not mix current branch controls with stale action references.

## Critical disposition before package rebuild

Keep four verdicts separate during the hostile review:

1. **Technical validity:** does the exact current code still permit the state transition?
2. **Incremental impact:** what capability exists only because of the defect, compared with intended contributor behavior on the same worker class?
3. **Novelty/duplicate risk:** is the new root independently necessary even when a known report's actor, grant path, self-approval, merge path, and other prerequisites are disabled?
4. **Submission readiness:** do the canonical report, evidence, manifest, and packaged copies agree after current-pin and prior-art refreshes?

Do not rebuild the submission archive before deciding the first three. A stale-package mismatch is useful evidence that the old bundle must not be submitted; rebuilding too early can hide that fact and make package freshness influence the reportability decision.

Recommended sequence:

1. Run current-pin, root-isolation, sink, production-context, prior-art, and impact-boundary controls against canonical artifacts.
2. Write a binary hostile disposition that names the highest proven boundary and explicit non-claims.
3. Run the package validator and preserve both its command results and copy/hash comparison.
4. If controls pass but packaged copies differ, record `submission_ready=false`; keep the old archive for provenance and place an adjacent `*.BLOCKED.md` sidecar naming the authoritative review and exact mismatch reason.
5. Use a separate critical-review verifier whose PASS means **the disposition is evidence-consistent**. It must not accidentally mean that a superseded archive is valid. Require the expected package block as a positive assertion.
6. Reconcile the canonical finding report, current source links/pin, severity, and final disposition before rebuilding anything.
7. Only after the report survives review should a new concise archive be assembled and hashed.

A robust review result should serialize independent fields such as:

```json
{
  "technical": "VALID_HEAD_UNBOUND_AUTHORIZATION_TOCTOU",
  "impact": "SAME_UNTRUSTED_CI_PLANE_BOUNDED",
  "reportability": "CONDITIONAL_GO_LIFECYCLE_DELTA_ONLY",
  "severity": "MEDIUM_ENVIRONMENT_DEPENDENT",
  "submission_ready": false,
  "old_archive_blocked": true
}
```

The values are finding-specific; the separation is mandatory. A technically valid authorization bug can survive while its High/Critical supply-chain framing and existing package both fail.

### Prior-art capture and detector integrity

Prior-art evidence often changes shape independently of its meaning. Treat the refresh path and cached-verification path as one schema contract:

- parse exact current comments rather than relying on a single paraphrased phrase;
- preserve source URL, author, capture time, raw hash, and exact bounded interpretation;
- name detector fields for what the source actually says (for example, ephemeral/same-PR boundedness rather than a broader “not security sensitive” paraphrase);
- after changing an output key, run both `--refresh` and cached/default verification modes;
- make downstream disposition verifiers assert the serialized key actually written by the producer;
- never weaken the assertion merely to recover PASS.

First-party statements about disposable or untrusted workers are severity evidence, not automatic falsification. Compare the candidate with ordinary contributor execution and separately test for a new unsandboxed command path, reusable control-plane credential, cross-job persistence, trusted queue, publication path, or distributed-artifact consequence. If none is proven, preserve the authorization defect but cap the impact at the same untrusted plane.

## Worked lesson: BCR candidate-family split

A BCR candidate family produced three different outcomes from related reviewer behavior:

- a prior-contributor eligibility theory was killed because the implementation matched the documented participation model and produced no incremental privilege;
- a base-retarget stale-review theory reached bot approval and a merge attempt but was killed because the latest head could not receive the required `dismiss_approvals` check;
- a separate benign-H1 → unreviewed-H2 stale-label theory survived because its impact was pre-merge CI execution: dismissal ran on H2, the PR-wide authorization label remained, eligibility was not revalidated, and the presubmit sink consumed H2 before merge.

The lesson is class-level: branch protection resolves the boundary it governs; it does not automatically sanitize earlier authorization decisions or pre-merge execution paths.

## Worked lesson: BCR base-retarget review reuse

In the 2026-07-30 BCR review, the action-level stale-review defect caused bot approval and a merge attempt. The overlooked live `main` branch summary required GitHub Actions context `dismiss_approvals` with `enforcement_level=everyone`. H1 was pushed while the PR targeted an alternate branch; retarget-back emitted `edited`, while the check workflow subscribed only to `opened`, `synchronize`, and `reopened` on `main`. H1 therefore could not receive the required latest-SHA check. Correcting the harness changed `merged_heads` from a mocked success to `[]` and killed the Critical/source-merge chain while preserving the lower-severity stale-label observation.

## Authoritative sources

- Branch protection REST endpoint and permission requirements: https://docs.github.com/en/rest/branches/branch-protection?apiVersion=2022-11-28#get-branch-protection
- Rules applying to a branch: https://docs.github.com/en/rest/repos/rules?apiVersion=2022-11-28#get-rules-for-a-branch
- Required status checks before merging: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging
- Latest-commit-SHA troubleshooting: https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
