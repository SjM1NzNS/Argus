# Reusable Worker Cross-Task Isolation Review

Use this reference when an authorized source review reaches a reusable JVM, process pool, sidecar, job runner, plugin host, preview worker, connection validator, build agent, notebook kernel, or other service that executes code for more than one request, tenant, namespace, or identity.

## Security invariant

A task boundary is not an isolation boundary unless every attacker-controlled execution primitive and every authority-bearing context are either:

1. destroyed together; or
2. cryptographically and structurally bound to the same task identity on every use.

Serial execution (`concurrency=1`) prevents simultaneous races but does **not** prevent sequential cross-task persistence.

## Lifetime inventory

For every worker, record the lifetime and owner of:

| State or actor | Questions |
|---|---|
| Process/JVM | Is it reused? For how many requests or how long? Is it partitioned by tenant/namespace? |
| Threads/executors/timers | Can user code create them? Who interrupts, joins, cancels, or enumerates them after return? |
| Child processes | Are descendants killed as a process group/cgroup, or only the immediate task returned? |
| Classloaders/modules | Does closing the loader stop threads that retain it? Can static fields survive through parent-loaded classes? |
| Environment/files | Are credentials, metadata endpoints, sockets, and temporary files task-specific or process-global? |
| Sidecar context | Is identity held in one mutable field/cache? Is it keyed by task ID and caller? |
| Credential cache | What is the key, invalidation event, and fallback identity? |
| Local HTTP/IPC | Are both context-changing operations and authority-returning reads authenticated and task-bound? |

Treat configuration names such as “user-code isolation” as claims to verify, not proof. Read the actual completion path and restart threshold. “Restart after user code” may still mean after N requests or a periodic lifetime.

## Source-to-sink workflow

1. **Prove the low-privilege execution primitive.** Map the product role/permission that can upload or select code and invoke the reusable worker. Distinguish expected code execution in the caller’s own namespace from the claimed cross-namespace capability.
2. **Trace direct invocation.** Determine whether user code runs in-process, in a child process, or in a separately destroyed sandbox. Look for direct reflective/Guice/plugin invocation without a disposable process, owned executor, `ThreadGroup`, cgroup, or descendant cleanup.
3. **Trace completion.** Follow `finally`, response-body callbacks, counters, classloader closure, worker restart, and timeout paths. Explicitly search for interruption/join/kill logic; absence in the launcher alone is not enough if an outer supervisor performs cleanup.
4. **Trace the next task.** Show how a later request supplies a different namespace/identity to the same worker instance. Prove routing is a shared pool rather than tenant-pinned workers.
5. **Trace the authority read.** Follow the stale actor to the credential, metadata, secret, cache, filesystem, or privileged service. A local endpoint that authenticates context writes may still expose unauthenticated reads based on global current context.
6. **Close product impact.** Require separate identities/tenants and an authority-bearing sink such as a service-account token, secret, data read, write capability, or privileged action. Preserve deployment-level partitioning as an explicit gate when source cannot resolve it.

## Safe deterministic canary

Prefer a source-local harness with no live credentials or cloud calls:

1. Run the real sink-owning handler/service on loopback.
2. Replace the remote credential/cloud backend with a deterministic fake returning `<namespace>-TOKEN-CANARY`.
3. Establish an attacker task context and start a background thread through the same execution primitive under review.
4. Let the task return and exercise the real clear/completion path.
5. Install a victim context through the legitimate framework path.
6. Have only the lingering thread call the real local read endpoint.
7. Assert it receives the victim canary.

Required controls:

- no active context returns no token;
- destroying the worker/owned executor after task A prevents the read;
- binding the read to a per-task unforgeable capability prevents the read;
- authenticating context mutation alone does not count as a fix if the exploit performs no mutation;
- attacker and victim canaries are distinct and the assertion checks the exact victim value.

Label a manually created thread plus handler test honestly: it proves the persistence/sink composition, while exact supported-path execution requires the real plugin/launcher path or a separate launcher test.

## Prior-art differential

When a public issue or PR hardens the same sidecar/worker:

1. Read its body **and full diff** before expanding the harness.
2. State the public root in one sentence.
3. Run the two-way remediation test.
4. Test against the PR head or a byte-identified patch overlay when claiming an incomplete fix.

A context-write authentication patch and a cross-task stale-reader flaw can be distinct when:

- the candidate never calls the protected write/delete operation;
- legitimate framework code installs the victim context;
- the stale actor consumes an unbound read endpoint; and
- each remediation leaves the other issue intact.

Do not report the original unauthenticated write as fresh merely because a downstream authentication quirk makes its impact clearer.

## Harness reliability patterns

- Pre-create Mockito response mocks before entering `thenAnswer`; starting a new `when(...)` inside an unfinished answer can trigger `UnfinishedStubbingException`.
- Prefer literal wire-format fixture JSON or the product’s registered codec for time/URI/security types. Generic reflection serializers can fail under module encapsulation and test the serializer rather than the security invariant.
- Use `set -o pipefail` when piping Maven/Gradle output through `tee`; otherwise the shell may report success when the build failed.
- Preserve every failed run as harness-debug evidence, but only a passing exact assertion upgrades the candidate to `runtime_validated`.
- Keep temporary test files separate from the pinned source and record any build-only submodule placeholders or overlays.

## False-positive gates

Downgrade or block when:

- workers are actually disposable per task or strictly partitioned by namespace;
- user code cannot create a surviving actor under the supported runtime;
- an outer supervisor kills all threads/process descendants before reuse;
- the local authority endpoint binds every read to a per-task non-exportable capability;
- the next task cannot run under a different authority in the same worker;
- the only proven result is denial of service without accepted impact; or
- product roles do not let the proposed low-privilege actor reach the execution path.

## Completion checklist

- [ ] Process, thread, child-process, classloader, context, cache, file, and sidecar lifetimes are documented.
- [ ] Serial concurrency and lifecycle isolation are evaluated separately.
- [ ] Shared-pool routing across identities is source-proven or explicitly deployment-gated.
- [ ] The user-code entry point and product role are exact.
- [ ] Completion code was checked for interrupt/join/kill/cgroup cleanup.
- [ ] The authority-returning read is bound—or shown not bound—to the active task.
- [ ] Local proof uses fake canaries and the real sink-owning method/handler.
- [ ] Negative controls isolate persistence, context change, and caller binding.
- [ ] Public PRs/issues were searched before expensive validation and repeated after root cause was known.
- [ ] Technical validity, novelty, deployed reachability, and reportability have separate verdicts.
