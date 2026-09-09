# CI Lower-Precondition Trigger-Breadth Review

Use this when a CI finding already has a demonstrated execution or worker-compromise sink, but its current trigger depends on approvals, labels, config changes, maintainer status, races, or multiple commits.

## Governing rule

Once a serious sink is established, do **not** spend the next pass only enumerating more post-compromise capabilities. First search horizontally for a different input or pipeline that reaches the same sink with fewer attacker prerequisites.

The preferred candidate is the route with the smallest credible prerequisite set, not the most elaborate impact narrative.

## Trigger inventory

Map every independent entry surface, even when the original finding came from only one of them:

- ordinary project/test pipelines;
- repository-wide `BUILD`, `MODULE`, workspace, package, and Starlark/config files;
- module/archive/patch/overlay ingestion;
- generated workspaces and dependency/repository evaluation;
- PR, fork, branch, merge-queue, comment, label, schedule, dispatch, and retry triggers;
- config-change approval blocks and the exact file classes they cover;
- first-time contributor, prior contributor, collaborator, code-owner, and maintainer distinctions;
- separate pipelines that share the same worker queue or step generator.

For each route, record:

```text
attacker input
-> trigger/provider condition
-> checkout/ref
-> validation or block decision
-> generated task/target
-> process-execution phase
-> worker/container/host boundary
```

## Prerequisite minimization table

Compare candidates explicitly:

| Gate | Route A | Route B |
|---|---:|---:|
| commits/state transitions | | |
| prior contribution | | |
| maintainer/collaborator role | | |
| genuine approval | | |
| persistent label/comment | | |
| sensitive config change | | |
| existing module/package structure | | |
| timing/race dependence | | |
| live mutation needed for proof | | |

A route is materially easier only if it removes real gates, not merely changes syntax.

## Expected-untrusted-code counterfactual

Ordinary CI execution of fork-controlled code is often intended. Do not report that fact alone.

When a simpler route is found, shift the root-cause statement to the first unsafe boundary after intended execution, such as:

- reusable rather than ephemeral worker;
- privileged container;
- host networking;
- Docker/container-runtime socket;
- writable agent state;
- static or reusable agent credentials;
- shared cache/artifact state;
- cross-queue or cross-organization authority.

The reportable chain should read like:

```text
lowest-precondition untrusted trigger
-> intended code execution
-> unsafe isolation or reusable authority
-> demonstrated or source-supported security impact
```

Do not call expected test execution RCE without proving the isolation/authority failure.

## Source-first controls

1. Pin the workflow and pipeline-provider configuration.
2. Inspect every provider trigger flag, fork setting, branch filter, label filter, and manual block.
3. Read the actual target selection and config-change gate; list executable file classes outside the gate.
4. Invoke the exact local gate function with representative changed paths and no approval marker.
5. Invoke the exact step generator and retain queue, image, privilege, network, environment, and volume fields.
6. Use a harmless local fixture through the real build/dependency mechanism. Prefer a declared output or temporary marker and a causal negative control.
7. Use public builds only as passive liveness evidence; never trigger CI merely to prove the route.
8. Search public history for the intended security invariant and for collision signals.

## Repository-phase execution

For Bazel-like systems, distinguish action-sandbox execution from repository/module evaluation. Repository rules and module extensions may execute processes before ordinary action sandboxing. Similar early phases exist in package-manager lifecycle hooks, build-system configure steps, generated code, plugin loading, and dependency resolution.

A local proof should establish the real phase and target selection without touching production sockets, credentials, callbacks, or workers.

## Novelty and duplicate gate

A new trigger can be distinct from a prior authorization bug even when both reach the same unsafe worker. Require differences in:

- pipeline;
- attacker-controlled file/input class;
- authorization decision;
- timing/state machine;
- prerequisites;
- remediation.

Then run two-way remediation:

- fixing the old approval bug should not close the new ordinary-code route;
- isolating the worker should close the dangerous impact for both routes.

If a suspicious public test PR or similarly titled control already exists, record high collision risk without inventing its undisclosed root cause.

## Stop conditions

Stop deeper post-compromise enumeration when:

- a materially lower-precondition route is proven;
- the unsafe worker boundary and highest defensible same-plane impact are established;
- trusted/source/release escalation still lacks an independent capability gate;
- additional live proof would require triggering external CI, reading secrets, or mutating infrastructure.

At that point, reframe the report around the easiest trigger plus the unsafe boundary. Preserve harder routes as corroborating alternatives rather than the lead narrative.
