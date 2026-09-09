# OSS CI/CD workflow-command injection validation

Use this reference when reviewing a scanner, formatter, reporter, or CI helper that processes pull-request-controlled repository content and writes to a CI runner stream.

## Core audit path

Trace the entire actor chain, not only the library sink:

1. **Official workflow actor model** — verify the documented reusable workflow checks out and scans the pull-request commit, rather than only the trusted base branch.
2. **Automatic repository inputs** — inventory colocated config, manifests, ignore reasons, package metadata, paths, and report fields loaded without an explicit trusted override.
3. **Every logger/output sink** — search ordinary info/warning/error logs as well as table, JSON, SARIF, annotation, and reporter paths. A project may sanitize formatted reports while missing diagnostic logs.
4. **Runner semantics** — determine whether child-process stdout or stderr is forwarded to a runner that recognizes line-oriented workflow commands.
5. **Current release path** — establish which released version the official action pins. Do not rely only on `main`.

## Safe local proof pattern

Use a harmless command such as:

```text
::warning file=victim.go,line=1::ARGUS_WORKFLOW_COMMAND_CANARY
```

Do not trigger a remote CI run merely to prove parsing. A package-level regression test is usually enough to establish:

- repository-style config was actually parsed or auto-loaded;
- the attacker-controlled selector matched real internal data;
- the value reached the production logger;
- the command appeared at the beginning of a new raw output line.

Add a negative control using the product's own sanitizer. For GitHub Actions line-boundary injection, verify CR/LF become `%0D`/`%0A` and that no command can begin on a new line.

When the relevant function is package-private, temporarily place the test in the real package, run the exact package test, then move the test into mission evidence and confirm `git status --short` is clean.

## Release verification

After proving current `main`, run the identical test against the official released tag in a temporary detached worktree:

1. fetch the exact tag;
2. create a detached temporary worktree;
3. copy the same regression test into the package;
4. run the narrow test;
5. remove the test and worktree;
6. verify both repositories are clean.

This closes the common objection that the issue exists only on an unreleased branch.

## Security-intent evidence

Look for existing sanitizer helpers, regression tests, comments, and changelog entries fixing the same vulnerability class. A missed sink is more credible when the project already treats crafted repository fields and workflow commands as a security boundary.

## Impact discipline

Separate demonstrated behavior from command possibilities:

**Safe to claim when proven:**

- forged trusted-looking annotations;
- workflow-log/output integrity manipulation;
- creation of a runner-recognized workflow-command line.

**Conditional and requiring runner-specific proof:**

- masking manipulation via `add-mask`;
- command-parser suppression via `stop-commands`;
- persistence across steps.

**Do not infer from a raw command line alone:**

- arbitrary code execution;
- secret theft;
- legacy `set-output` or `set-env` exploitation on current runners;
- repository write access.

## Runner-state escalation workflow

After proving a raw line-start command, do not stop at enumerating possible commands. Compose the source half with the current runner's real command handlers and an actual downstream consumer.

1. **Pin current runner source** — record the exact `actions/runner` commit used for semantic validation.
2. **Map command lifetime** — inspect where each command stores state and whether that object is created per process, action handler, step, or job. In current runner architecture, distinguish `HostContext` singletons/state from `ActionCommandManager` instances created for handlers.
3. **Trace a concrete consumer** — identify later logs, annotations, job outputs, environment files, post-actions, artifact/SARIF upload, or workflow expressions that actually consume the modified state. A command primitive without a consumer is not an escalation.
4. **Use native runner tests** — prefer the runner's own test project and classes over a hand-written parser simulation. Read `src/global.json`, use the required SDK, and run the narrowest existing or temporary test.
5. **Compose an exact value, not merely a sentinel** — after a harmless canary proves the sink, choose a mask or command value that is guaranteed to occur in the real downstream format. Exercise the product's real serializer to establish that guarantee.
6. **Drive the production consumer** — if production skips outputs in `JobExtension.FinalizeJob`, construct the actual job-output message and invoke that method. Assert the affected outputs are absent and an unrelated unmasked control output remains. A unit test of `MaskSecrets(value) != value` alone is useful scaffolding but not the strongest final proof.
7. **Test process line boundaries separately** — proving raw `\r` or `\n` in product output is not enough if the runner receives already-split lines. Use the runner's native process reader (for example `ProcessInvoker`) to prove each boundary produces a standalone command line.
8. **Check current defaults, historical pinned revisions, and prevalence** — an impact behind a current opt-in such as `export-results: true` must be labeled conditional for the current revision, but do not stop at searching for explicit opt-ins. Public callers may pin older official revisions where the same output is unconditional. Fetch each caller's current workflow, resolve its pinned reusable-workflow revision, and classify that revision by behavior: pre-feature, unconditional, gated/default-off, gated/opted-in, or unresolved. Report file and repository counts separately, preserve moving-tag uncertainty, and disclose index/private-repository limits.
9. **Trace real downstream consumers** — search caller workflows for `needs.<job>.outputs.*`, workflow outputs, environment handoff, JSON parsing, comparison loops, and fail-open/fail-closed behavior. If a suppressed output becomes a missing expression property, verify the platform's missing-property semantics and reproduce the consumer's exact shell/expression logic with missing, positive-impact, and clean controls. Do not confuse safe `env`/`printf` handling with shell injection; the impact may instead be an empty-data security-check bypass.
10. **Measure independence, not only repository count** — group consumers by owner and workflow-template hash or normalized logic. Fifty copies under two owners are concrete deployments but not fifty independent implementations; report both totals and concentration.
11. **Freeze and clean** — save temporary runner tests as patches, run `git apply --check` after restoring the clean pinned repository, hash patch/result/probe files, and verify all product/action/runner repositories are clean.

If the required .NET SDK is absent, a reproducible local setup path is to read Microsoft's official release metadata, select the exact `linux-x64` artifact required by `src/global.json`, verify its published SHA-512, and extract it under a user-local directory. The durable rule is checksum-verified, version-exact local tooling—not reliance on whichever system SDK happens to be installed.

## Current runner command-lifetime matrix

Treat this as a verification map, not a substitute for reading the pinned runner revision:

| Command/path | State or effect to inspect | Escalation gate |
|---|---|---|
| `warning` / `error` / `notice` | Issue added to the current execution context | Forged annotation is immediate; `error` does not automatically prove job failure |
| `add-mask` | Adds attacker-chosen value to job-wide `HostContext.SecretMasker` | Prove later log/issue redaction or a concrete secret-output rejection gate |
| `stop-commands` | Stop token stored on an action-command manager | Verify manager lifetime; do not claim cross-step persistence when managers are created per handler |
| `set-output` | Sets current step/action output | Require an official downstream `steps.<id>.outputs.*` consumer; no consumer means no impact chain |
| `save-state` | Stores state for the current action | Require a real post-action/state consumer |
| legacy `set-env` / `add-path` | Compatibility-gated handlers | Verify whether insecure compatibility is enabled; current default blocking kills the chain |
| `add-matcher` / `remove-matcher` | Modifies problem matchers on the root execution context | Prove downstream matching or known-owner removal; matcher-created issues do not imply process failure; account for regex timeout/removal before claiming DoS |
| `internal-set-repo-path` | Plugin-only repository tracking mutation | Confirm ordinary action output can register it; current runner omits it until a plugin handler explicitly enables it, closing the path for normal Docker actions |
| modern file commands (`GITHUB_OUTPUT`, `GITHUB_ENV`, `GITHUB_PATH`, `GITHUB_STATE`, summary) | Per-step files with runner-provided paths | Stdout/stderr injection does not automatically obtain or write those files; `stop-commands` does not disable them |

`add-mask` deserves special attention because the same job-wide masker may affect more than displayed logs. Current runner job-finalization code rejects a job output when masking changes its value. This supports a conditional integrity/availability chain when an official reusable workflow exports attacker-influenceable scan results and the chosen mask occurs in those values.

## Incremental-capability and intended-authority gate

A technically real runner-state mutation is not automatically a reportable security bypass. Before promoting a deployed chain, compare it with everything the same actor is already allowed to do through supported product controls.

Run this counterfactual explicitly:

| Question | Required analysis |
|---|---|
| Protected decision | What merge, release, artifact, credential, deployment, or user-data decision is supposedly bypassed? |
| Injection path | What exact input/state mutation makes that decision pass or disappear? |
| Intended-authority path | Can the same PR author use documented config, ignore/filter rules, workflow inputs, or ordinary repository changes to create the same decision outcome? |
| Incremental distinction | Does the injection corrupt trusted data or state that the intended path cannot control, and does a real consumer rely on that distinction? |
| Qualifying impact | Does the result satisfy the program's current source/build, artifact/package, credential, protected-action, or user-data impact category? |

Interpretation:

- **Same outcome through intended authority, no consumer uses the distinction:** technically valid hardening flaw; HOLD rather than report-ready.
- **Trusted baseline or separate state is corrupted, but downstream logic ignores that distinction:** preserve as an escalation lead, not proven impact.
- **A real consumer relies on the trusted distinction and the intended path cannot reproduce the pass:** incremental bypass established; proceed to reportability review.

For scanner comparisons, test the no-injection control with supported ignore configuration. If the consumer examines only vulnerability IDs remaining in the PR result, a PR-controlled ignore may already make the loop pass. Output omission then proves transport corruption but not necessarily a new security capability. Repository count and fail-open behavior cannot substitute for this counterfactual.

When rules are impact-category based, read the current official program language and project tier. Being in scope or high tier does not rescue a candidate that misses the qualifying impact category. Record a HOLD decision in the report banner and target ledgers so an earlier “submission-ready” checkpoint is not accidentally revived.

## Escalation reporting discipline

Split impact by deployed workflow behavior, not only the current upstream default:

- **Default, demonstrated:** forged annotations and job-wide redaction of attacker-chosen strings in later logs/issues.
- **Current gated revision:** omission of exported workflow/job outputs only when the documented option is enabled.
- **Older pinned official revisions:** if callers pin an official revision that exports unconditionally, treat output omission as deployed impact for those callers—not as a hypothetical current opt-in.
- **Downstream consumer impact:** separately prove whether missing outputs fail open, fail closed, or merely break observability. Check the platform's missing-property coercion and run the exact consumer logic with missing, positive, and clean controls.
- **Rejected or unproven:** RCE, secret disclosure, uploaded SARIF-file mutation, legacy command enablement, or cross-step `stop-commands` persistence.

Do not rename output omission into "scan-result deletion" if artifacts or SARIF files remain intact. State precisely which transport is affected: logs, annotations, step outputs, job outputs, artifacts, or uploaded code-scanning results. If many consumers share one copied template, report repository count and owner/template concentration so prevalence is not inflated.

## Session example: OSV-Scanner

In the validated OSV-Scanner review, product current/release, official action, and runner revisions were frozen independently. Keep those identities separate; a runner commit must never be presented as a product commit.

The reusable technique was:

- prove both package-override and ignored-vulnerability reason sinks, not only the first discovered logger;
- run an LF/CR matrix on current source and the pinned release;
- use the product sanitizer as a negative control (`%0A` / `%0D`);
- independently feed CR through the runner's native `ProcessInvoker` and verify it becomes a standalone command line;
- replace the initial mask sentinel with `::add-mask::results` because the product's real machine JSON serializer guarantees a top-level `"results"` key;
- invoke the runner's real `ActionCommandManager` and `JobExtension.FinalizeJob`, proving both trusted-baseline and PR result outputs are absent while an unrelated control output remains;
- inspect every registered command and kill unsupported upgrades: per-handler `stop-commands`, unused `set-output`, unconsumed `save-state`, blocked legacy environment/path commands, plugin-gated `internal-set-repo-path`, and file commands outside the stdout channel;
- distinguish job-global matcher/annotation manipulation from process-result or artifact mutation;
- do not stop after finding zero explicit opt-ins on the current workflow. Resolve the revisions actually pinned by callers: older official revisions may export the same outputs unconditionally while the current revision defaults them off;
- trace downstream consumers of the omitted outputs. Verify platform missing-property semantics and run exact missing/positive/clean controls against their comparison logic;
- report deployment concentration. In the broader OSV-Scanner sample, many repositories pinned the older unconditional-export workflow, while most fail-open consumers shared one template under two owners.

This example establishes three general lessons. First, a stronger native proof can coexist with different behavior across current and historical official workflow revisions; report each deployed revision accurately. Second, option-string searches are not prevalence analysis: classify pinned code semantics, then prove what downstream consumers do when the affected output disappears. Third, prevalence plus fail-open behavior still does not prove incremental impact: compare the injected path with supported attacker-controlled ignore/filter configuration. If both produce the same protected outcome and no consumer relies on the corrupted trusted-baseline distinction, downgrade to HOLD until a stronger consumer or command effect is found.

## Verification checklist

- [ ] Official workflow and pinned release inspected
- [ ] Pull-request-controlled source established
- [ ] Auto-loaded config/manifest path established
- [ ] Raw logger sink established
- [ ] Harmless line-start command reproduced locally
- [ ] Every equivalent sink exercised, including package-level and vulnerability-level reasons where applicable
- [ ] LF and CR tested through both product logger and native runner process-reader boundary
- [ ] Sanitizer negative control reproduced
- [ ] Current and released product versions tested
- [ ] Current runner commit pinned and native test harness used for any escalated command claim
- [ ] Exact downstream-format value chosen and real serializer exercised
- [ ] Production consumer/finalizer invoked with affected outputs plus an unaffected control
- [ ] Command state lifetime established (handler/step/job)
- [ ] Concrete downstream consumer identified and tested
- [ ] Workflow option defaults recorded for the current revision
- [ ] Public callers' pinned workflow revisions resolved and classified as pre-feature, unconditional, gated/default-off, gated/opted-in, or unresolved
- [ ] Downstream output consumers identified; missing-property semantics verified
- [ ] Exact consumer logic tested with missing-output, positive-impact, and clean controls
- [ ] Repository count separated from owner/template concentration
- [ ] Intended-authority counterfactual run: documented config/ignore/filter/ordinary PR controls compared against the claimed bypass outcome
- [ ] A real consumer relies on a trusted distinction the intended actor cannot already control, or the candidate is explicitly marked HOLD
- [ ] Current official program impact categories and project tier checked independently of technical scope
- [ ] Search denominator, resolved count, unresolved refs, and coverage limits recorded
- [ ] Unsupported commands and impact upgrades explicitly killed
- [ ] Temporary tests saved as evidence patches, then removed
- [ ] Preserved patches pass `git apply --check` against restored pinned repositories
- [ ] Temporary hooks/worktrees removed
- [ ] Product, action, and runner repositories clean
- [ ] Evidence bundle leak-audited
- [ ] Report distinguishes logs, annotations, outputs, artifacts, and SARIF
- [ ] Report separates proven impact, conditional impact, and non-claims
