# Internal Query Authorization and Indirect Serializer Disclosure

Use this reference when a user-visible endpoint resolves one authorized anchor object, then expands relationships through an internal query, cache, index, graph traversal, submission/group identifier, topic, dependency set, or batch key.

The recurring failure class is:

```text
visible anchor -> internal relation query -> unfiltered related objects -> generic serializer -> private bytes
```

A correct authorization check on the anchor does **not** authorize every related result.

## Source-review method

1. **Pin the exact source revision.** Record the application and dependency/submodule commits. Parallel-agent summaries are leads only; reread and rerun from the parent session's exact checkout before promotion.
2. **Find the public ingress.** Record the REST/RPC/CLI route and prove ordinary or anonymous reachability through a legitimate visible anchor.
3. **Separate anchor resolution from expansion.** Identify where the endpoint stops using the caller-aware resource and begins an internal lookup such as `byGroupId`, `bySubmissionId`, `findRelated`, cache fetch, or index predicate.
4. **Treat internal queries as untrusted data sources.** Search for explicit caller visibility flags and per-result authorization. Method names like `Internal*Query` are a warning, not a finding.
5. **Trace every result to bytes.** Follow sorting, preloading, plugin enrichers, serializers, and option-controlled field expansion. A serializer that receives `CurrentUser` may tailor fields without rejecting an unreadable object; verify both behaviors independently.
6. **Compare sibling callers.** Search all callers of the same internal query. A neighboring endpoint that explicitly checks `READ`/visibility is high-signal evidence that the query itself is not an authorization boundary.
7. **Compare branches in the same endpoint.** Open-versus-merged, single-versus-batch, cached-versus-uncached, and current-versus-historical branches often diverge. Hard-coded `hidden = 0`, empty filtered sets, or bypassed caller arguments deserve focused controls.

## Owned-fixture proof

Build the smallest fixture containing two related objects:

- one object remains readable to the test actor;
- one object becomes unreadable after the relation is created;
- all content is synthetic and unmistakably canary data.

Then require this matrix:

| Control | Expected secure behavior |
|---|---|
| Direct read of visible anchor | Succeeds |
| Direct read of hidden object | 404/403 or equivalent denial |
| Indirect relation endpoint through anchor | Must not return hidden object bytes |
| Patched/visibility-aware path | Returns visible objects only or an opaque hidden count |

For a positive vulnerability proof, assert exact hidden bytes rather than object count or timing. Useful canaries include:

- private subject/title;
- full commit or description message;
- review/comment text;
- private filenames;
- owner/author identity fields;
- revision/object identifiers;
- plugin-defined fields.

Request each normal response-expansion option separately or in a bounded combined test. Do not imply file bodies, patches, secrets, or bulk records unless the fixture actually returns them.

## Configuration and data-shape discipline

Distinguish three layers:

1. **Code flaw:** missing per-result authorization once mixed-visibility results exist.
2. **State prerequisite:** one relation/group ID contains objects with divergent current visibility.
3. **Configuration needed to create that state:** topic-wide submit, cross-project grouping, ref ACL changes, reindex timing, migration history, or another supported feature.

A configuration-dependent fixture can prove a real flaw, but the report must name the exact setting and avoid calling it default. Search for a lower-precondition default path; if none exists, preserve the configuration boundary in title, severity, and reproduction.

## False-positive gates

Kill or downgrade when:

- the internal query enforces caller visibility by default and the endpoint does not disable it;
- resource construction rechecks every related object before formatting;
- the serializer omits the entire object rather than merely hiding selected fields;
- only counts, timing, ordering, or existence are exposed and the mission requires sensitive bytes;
- the hidden object cannot share the relation key under any supported production configuration;
- the test actor already has direct equivalent access to the returned fields.

Do not let a strong no-go for direct object fetch, Git pack transfer, or archive download erase a separate metadata/message disclosure through a relation endpoint. Record scope-specific no-go and winning branches independently.

## Remediation shape

Prefer a caller-aware expansion that partitions visible and hidden results before sorting, plugin enrichment, or serialization:

```text
internal results
  -> per-result READ test using request user
  -> visible list + hidden count
  -> serialize visible list only
```

When the product already exposes an option such as `NON_VISIBLE_*`, return only an opaque count. Never pass hidden objects to generic serializers or plugin hooks merely because the response later intends to suppress them.

Regression coverage should include:

- ordinary and anonymous actors where supported;
- direct hidden-object denial;
- default and response-expansion options;
- ACL changes after relation creation;
- cross-project/ref and same-project variants;
- reindex/cache paths;
- full existing test class, not only the new method.

## Evidence and review gates

- Run the focused test uncached.
- Run the full owning test class/suite and parse JUnit failures/errors.
- Preserve the exact patch and verify it applies to a fresh worktree at the pinned commit.
- Hash logs, JUnit XML, patch, and final reports after the last edit.
- If a subagent's background process or checkout is isolated, do not inherit its claimed pass; rerun locally and record the exact HEAD.
- Keep technical validity, hosted-deployment proof, OSS repository eligibility, and program routing as separate verdicts.
