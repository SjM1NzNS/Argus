# Validating asynchronous confused-deputy authorization chains

Use this workflow when an authenticated request queues a background job, long-running operation, worker task, event, or message that later performs a privileged read, network call, deployment, or credential operation.

## Core question

Do not stop at the request-time authorization check. Determine whether the asynchronous boundary preserves the **full initiating security context** or only a display name/user ID. A background component that receives a name without the caller credential may be reclassified as an internally authenticated service principal and become a confused deputy.

## Identity continuity trace

Record these as separate source-to-sink nodes:

1. **Request principal** — name, credential type/value, scopes, exact entity permissions.
2. **Queued representation** — every persisted field; distinguish a supplied principal-name string from a full `Principal` or credential.
3. **Subscriber restoration** — which thread-local/context fields are set, left stale, cleared, and restored in `finally`.
4. **Execution inheritance** — whether newly created threads/executors inherit the restored context.
5. **Internal client authentication** — which principal/headers a remote client derives from that context.
6. **Downstream authorization** — whether the service evaluates the original caller's exact entity ACL or accepts an internal token only.
7. **External sink** — the first point where the protected value is disclosed or an action occurs; do not require later workflow success when the sink is reached earlier.

Verify exact assignments. For example, if the request service passes `principal.getName()` into a lifecycle method and that method stores the supplied string, describe that precisely; do not inaccurately say the lifecycle method read the thread-local itself.

## Modular local canary suite

A full distributed deployment is often unnecessary. Prove each security-relevant seam with production classes and join the modules only when the dataflow is exact.

### A. Persistence/restoration canary

- Queue a fake operation under an external canary identity.
- Assert that the subscriber restores the expected user ID.
- Assert that the caller credential is absent rather than silently assuming it.
- Start a child thread/executor from the same point and assert the inherited identity and credential state.

### B. Authentication synthesis canary

- Use the real production authentication-context implementation and token codec/manager.
- Assert what principal type is produced from `userId + null credential`.
- Pass that principal through the real internal authorization path or the closest production enforcer.
- Add the decisive control: preserving an external caller credential must keep the principal external and subject to normal authorization.

### C. Real sink canary

- Use the real client/library that reaches the sink, not a hand-built HTTP approximation.
- Return a unique fake secret such as `VICTIM-KEY-TOKEN-CANARY` from a fake local store.
- Point the configured destination only at loopback and record the actual outgoing header/body.
- Deliberately reject or fail the later operation after the sink; this proves disclosure does not depend on workflow success.

### D. Negative control

- Make the protected read fail as unauthorized.
- Assert that the network receiver or privileged sink is never reached and no canary is emitted.
- This separates the authorization bypass from expected outbound connectivity.

## Production applicability gate

Before calling the chain report-ready:

- Ground that the vulnerable asynchronous feature is supported in the production product.
- Confirm the relevant outbound or privileged action is intended and reachable in deployment.
- Compare exact entity permissions, not only broad predefined roles.
- If broad built-in roles already possess secret access, state that explicitly and use a defensible custom least-privilege ACL/role attacker model only when the product supports that separation.
- Cite tests or authorization code showing that parent/container access and exact-secret access are independently grantable.
- Avoid claiming a live product configuration that was not verified.

## Path-distinction checks

- Separate synchronous validation from queued execution; the synchronous path may correctly preserve caller authorization.
- Separate single-item/remote worker paths from bulk/in-memory LRO paths. Similar feature names do not imply the same identity propagation.
- Confirm the concrete implementation selected by dependency injection and feature flags.
- Determine whether the protected read happens before later application parsing, deployment, or clone success.

## Duplicate and report gates

Search public issues/PRs by:

- lifecycle/subscriber class names;
- credential propagation and internal-auth class names;
- exact permission plus protected entity type;
- sink strategy/client class;
- adjacent security PRs that may fix only one execution path.

A public search cannot exclude private duplicates. Promote only when:

- the identity-loss seam is locally proven;
- internal-authority synthesis is locally proven with an external-credential control;
- the real sink receives a fake canary;
- denied access prevents the sink;
- production feature/permission applicability is documented; and
- no exact public duplicate is found.

## Test-run evidence integrity

Treat the test runner's structured result as authoritative, not a shell marker or process notification.

- With `mvn ... | tee ...`, enable `set -o pipefail`; otherwise Maven can fail while the shell reports exit `0` from `tee`.
- Never accept a printed `*_PASSED` marker unless Surefire reports the intended class/method, a **nonzero** test count, zero failures/errors, and Maven `BUILD SUCCESS`.
- Exact method selectors can silently run zero tests when the method name is stale and `failIfNoTests`/`failIfNoSpecifiedTests` is disabled. Confirm the fully qualified class and method in the log.
- Give each attempt a unique log filename. Do not overwrite a shared log during iterative or concurrent runs; if overwrite already occurred, preserve process IDs and timestamps as provenance anchors.
- Delayed background notifications may describe an older attempt. Order results by runner timestamp and classify each as canonical, failed, superseded, or zero-test before updating a finding.
- Keep failed attempts for auditability but create a small validation index naming the only canonical logs suitable for a report package.
- Environment/runtime fixes are not evidence that the hypothesis passed. Re-run the focused test after the fix and preserve the decisive positive and negative controls.

## Evidence packaging

Preserve:

- one source-to-sink narrative with exact line anchors;
- individual logs for restoration, authentication, and sink/control tests;
- the mission-local test files as harness artifacts, clearly marked non-upstream;
- a validation index separating canonical passing logs from failed, superseded, overwritten, and zero-test attempts;
- a duplicate-screen record with queries and nearby non-duplicate fixes;
- a report draft that distinguishes locally confirmed modular proof from live production proof.
