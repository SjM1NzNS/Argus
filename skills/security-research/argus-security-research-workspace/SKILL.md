---
name: argus-security-research-workspace
description: "Operate and maintain the user's Argus SecurityResearch bug-bounty workspace: scope contracts, learning ingestion, playbooks, evals, cron, and target notes."
platforms: [linux]
---

# Argus SecurityResearch Workspace

Use this skill when the user asks to bootstrap, validate, maintain, or operate the Argus bug bounty workspace under `$HOME/SecurityResearch`, including learning ingestion, playbook creation, eval passes, target initialization, and authorized program-style target continuation.

This is a class-level workspace workflow skill. It should not store secrets, live target credentials, or full one-off hunt transcripts.

## Workspace paths

Default paths for this user:

- Main workspace: `$HOME/SecurityResearch`
- Burp projects: `$HOME/BurpSuite`
- Private Argus config: `$HOME/.config/argus`
- Learning scripts: `$HOME/SecurityResearch/11 - Scripts/learning`
- Learning logs: `$HOME/SecurityResearch/12 - Logs/learning`
- Cron logs: `$HOME/SecurityResearch/12 - Logs/cron`
- Raw evidence: `$HOME/SecurityResearch/09 - Raw Evidence`

Sensitive permissions expected:

- `$HOME/.config/argus`: `700`
- `$HOME/.config/argus/learning-sources.yaml`: `600`
- `$HOME/SecurityResearch/09 - Raw Evidence`: `700`

Do not modify sudoers or request passwordless sudo.

## Operating boundaries

Never install tools, run live recon, contact targets, test credentials, trigger webhooks, run broad scans, or use discovered secrets unless the user explicitly asks and the scope contract allows it.

Use Argus maturity and zone language:

- Lead
- Hypothesis
- Testable candidate
- Evidence-backed candidate
- Reportable finding
- Submitted report
- Accepted/rejected/duplicate/informative

Zones:

- Zone 0: learning/methodology, no live target interaction
- Zone 1: passive/low-impact recon, public code search, local analysis, surface mapping
- Zone 2: controlled low-noise active testing using owned/program-provided accounts, only if scope clearly allows
- Zone 3: noisy, destructive, sensitive, ambiguous, or higher-risk testing; requires approval

## Bootstrap validation workflow

When validating the workspace, check at minimum:

1. Required folder tree exists.
2. System policy files exist and are non-empty.
3. Templates exist and have YAML frontmatter.
4. Web2/Web3 playbook folders exist.
5. Eval stubs exist and are populated where expected.
6. Learning source config exists and is mode `600`.
7. Ingestion script exists and is executable.
8. Daily cron exists and logs to `12 - Logs/cron/learning-cron.log`.
9. `$HOME/BurpSuite` exists.
10. Private config and raw evidence directories have restrictive permissions.
11. Skill-router, skill-gap-policy, web2/web3 skill indexes exist and contain mappings.
12. Target initialization prompt includes automatic skill routing.
13. AppSec.fyi is configured as topic-page index, not generic feed.
14. Web3 sources include Rekt, Immunefi Blog/Research, and Solodit/Cyfrin.
15. No Argus-created passwordless sudo configuration exists.

Report PASS/FAIL, missing items, risky permissions, suggested fixes, and next Argus action.

## Continuous learning ingestion workflow

The ingestion config lives at:

`$HOME/.config/argus/learning-sources.yaml`

The script is:

`$HOME/SecurityResearch/11 - Scripts/learning/run_learning_ingest.sh`

Manual run:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_learning_ingest.sh"
```

Non-network smoke test:

```bash
ARGUS_DRY_RUN=1 bash "$HOME/SecurityResearch/11 - Scripts/learning/run_learning_ingest.sh"
```

Bounded priority run:

```bash
ARGUS_PRIORITY_ONLY=1 ARGUS_MAX_TOTAL_SECONDS=180 ARGUS_MAX_SOURCES_PER_GROUP=6 ARGUS_MAX_APPSEC_LINK_FETCHES=8 ARGUS_MAX_APPSEC_LINK_RECORDS=25 bash "$HOME/SecurityResearch/11 - Scripts/learning/run_learning_ingest.sh"
```

The daily cron should be bounded similarly:

```cron
30 7 * * * ARGUS_PRIORITY_ONLY=1 ARGUS_MAX_TOTAL_SECONDS=180 ARGUS_MAX_SOURCES_PER_GROUP=6 ARGUS_MAX_APPSEC_LINK_FETCHES=8 ARGUS_MAX_APPSEC_LINK_RECORDS=25 /bin/bash "$HOME/SecurityResearch/11 - Scripts/learning/run_learning_ingest.sh" >> "$HOME/SecurityResearch/12 - Logs/cron/learning-cron.log" 2>&1
```

Learning ingestion should store candidates and metadata only, not mirror sites or hoard articles. The compiler should produce source summaries, technique extraction notes, skill patch proposals, changelog entries, and eval update proposals.

Do not overwrite mature playbooks directly unless source quality is high and the lesson is specific/actionable.

### Learning cadence and registry audit workflow

Treat the registry as declared policy, not proof of runtime behavior. For learning-pipeline audits or migrations, trace each source through registry defaults, cadence/lane selection, shell-wrapper environment, scheduler timing, fetch behavior, seen state, combined manifest, reconciliation, compiler gates, promotion, cleanup, and historical logs.

For schema-v2 learning architecture, preserve these operational invariants:

1. Production wrappers pass an explicit executor cadence; do not rely on an implicit permissive `legacy` mode.
2. Use three executors: daily incremental, weekly reconciliation, and targeted backfill. `periodic` and `on_demand` are backfill trigger/eligibility modes, not reasons for broad overlapping cron jobs.
3. Weekly selection includes daily plus weekly roots and both static/browser lanes. The weekly run should replace that day's daily run or reconcile its exact manifest rather than duplicate it.
4. Targeted backfill requires an exact source-ID allowlist unless the operator explicitly requests all eligible sources.
5. Every root and discovered record carries source/parent IDs, record kind, source policy, acquisition method, run cadence, and registry schema/digest.
6. Static and browser lanes share one canonicalization/state contract, transactional locked writes, source-specific freshness, and unchanged-content behavior.
7. Reconciliation must pass or explicitly classify degradation before compiler/promotion jobs consume the run.
8. Downstream stages consume an explicit run manifest, never a lexically inferred “latest” directory.
9. Compiler output stays proposal-only; authority changes review context but never permits automatic mature-playbook promotion.
10. Validate acquisition semantics end to end: repository, transcript, feed, browser DOM, single-page, and deep-link declarations need matching runtime handlers.

During an active migration, files may change while the audit is running. Re-stat and re-read live wrappers and ingestors before finalizing findings, and separate historical production evidence from newly written but not-yet-scheduled code.

See `references/2026-08-10-learning-cadence-registry-audit.md` for the detailed audit method, observed integration gaps, durable invariants, and verification checklist.

## AppSec.fyi handling

Treat AppSec.fyi as a curated topic index, not authority.

Rules:

- Root page discovers topic pages.
- Topic pages such as `idor.html` and `xss.html` produce linked-resource candidates.
- Score original linked resources independently.
- Do not compile social share links, shallow posts, generic news, or unavailable/dynamic resources into skills.
- Filter or mark low-signal share URLs as `rejected_low_signal`.
- Prefer top high-signal links, deduped by URL.

## Web3 source handling

For Rekt, Immunefi, Solodit/Cyfrin, contest reports, and audit reports, extract protocol type, root cause, attacker path, impact, invariant lesson, test idea, false positives, reportability lesson, and skill patch recommendation.

Postmortems and vulnerability databases are realism sources, not report evidence. Convert them into invariants, evals, and test plans before applying them to a scoped target.

## Playbook creation workflow

When creating or patching playbooks from learning material:

1. Prefer class-level playbooks under `02 - Vulnerability Playbooks/`.
2. Add practical files like `overview.md`, `test-checklist.md`, `false-positives.md`, `evidence-requirements.md`, `reportability.md`, `attack-patterns.md`, or `invariants.md` as appropriate.
3. Embed gates that prevent false positives and severity inflation.
4. Create/update eval cases immediately for new reportability or severity rules.
5. Update `$HOME/SecurityResearch/07 - Skill Changelog/YYYY-MM.md`.
6. Run an eval pass before relying on new playbooks for live hunts.

High-yield initial playbooks already created in this workspace include Web2 Access Control, Secret Exposure, XSS, OAuth & SSO, GraphQL, SSRF/Webhooks; and Web3 Reentrancy, Share Accounting/ERC4626, Oracles, Access Control/Upgradeability, and Reporting/Postmortem Translation.

## Eval-pass workflow

An eval pass should:

1. Load the relevant eval stubs and playbooks.
2. Populate eval cases with scenario, reportability, severity, missing proof, triage rejection, next action, and report/hold/discard decision.
3. Produce a dated eval-pass report under `06 - Evals/`.
4. Patch playbooks immediately if the eval reveals a missing rule.
5. Update the skill changelog.
6. Verify files are non-empty and contain no `TODO` placeholders.

Useful regression cases from this session:

- Weak IDOR invalid: discard ID guessing without owned-account/object evidence.
- Real IDOR valid: report with two-account unauthorized read/write/action and impact.
- Firebase config not secret: discard public client config without capability.
- Secret exposure valid: hold/report only with redacted evidence, safe validation, or policy-supported exposure-alone rule.
- Reentrancy valid/nonimpactful: require callback path, invariant break, measurable impact.
- Oracle valid/unrealistic: require realistic manipulation path/cost and protocol impact.
- Rounding low impact: do not escalate dust-only or non-amplifiable math.
- OAuth open redirect: do not escalate without token/account/session impact.
- GraphQL introspection: lead only unless impact/policy support exists.
- Blind SSRF callback: lead/testable candidate; queue Zone 3 for internal/metadata validation.
- Admin-only Web3 issue: discard unless boundary broken or policy accepts centralization risk.
- Postmortem analogy: hypothesis/test plan only, not report evidence.

## Target workflow reminders

Before live target work, require a target scope contract under `03 - Targets/<Program>/`.

Target notes should include `scope.md`, `scope-contract.yaml`, `scope-domains.txt` when applicable, `surface-map.md`, `hypotheses.md`, `approval-queue.md`, `agent-log.md`, `findings.md`, evidence, and tool-output subdirectories.

After surface discovery, run skill routing and record loaded playbooks in `agent-log.md`.

For authorized program-like hunts, if an owned-object replay is blocked on account/session access, stop unauthenticated guessing, queue the blocker, and continue only safe Zone 1/local branches.

### High-signal branch pivot workflow

When a authorized program-style branch is blocked on role-specific account access or owned-object context:

1. Record the blocker and current verdict in the branch artifact, `checkpoint.md`, `agent-log.md`, and `approval-queue.md` if future owned-context work is needed.
2. Pick the next coherent scoped cluster from `scope-domains.txt` by relationship, not by isolated hostname: `admin + api + staging/design/q`, `portal + API`, `CMS + editor + API`, or `mobile API + dashboard`.
3. For each branch, create a self-contained scan directory with `targets.txt`, `reachability-triage.md`, `static-extraction-triage.md`, endpoint/config extraction, source-derived safe probes, and `branch-triage-YYYYMMDD.md`.
4. Use only a low-noise sequence unless explicitly approved otherwise: single root request, same-host static asset fetches, local JS route/config extraction, then source-derived `GET`/`OPTIONS` probes with synthetic IDs.
5. Treat broad static route maps, public helper endpoints, and CORS preflight oddities as leads only. They are not reportable unless sensitive authenticated data or owned-object action impact is demonstrated.
6. If protected routes consistently return `401`/required-auth and only public helper data is exposed, mark no finding, queue the needed owned context, and pivot rather than guessing more paths.

CORS/reportability rule for these branches: `ACAO: http://localhost:8080` with credentials or `ACAO: *` with `authorization` allowed is interesting, but reportable only with a browser proof that reads sensitive authenticated data or performs an authorized safe action. Wrong-audience tokens causing `500` are robustness signals, not findings, unless they leak data/stack traces or bypass auth.


### Owned-account / OTP authentication workflow

When authenticated validation requires email OTPs or short-lived verification codes:

1. Use **one account at a time**. Do not switch between two owned accounts mid-flow unless the user explicitly pivots.
2. State the exact account currently on the verification screen before asking for an OTP.
3. Never click resend, restart a login flow, or otherwise trigger a new OTP without explicit user approval.
4. If the browser/session resets before OTP submission, stop and ask before restarting because a new code may be sent.
5. Submit the provided OTP once, observe the exact result, and report it; do not immediately retry or request another code unless the user chooses to continue.
6. Do not store OTPs, passwords, bearer tokens, cookies, or session values in target artifacts. Record only redacted outcomes.
7. If a stable background browser harness is required for short-lived OTP pages, use an explicit one-shot OTP handoff mechanism rather than relying on background-process stdin, and type only into visible/enabled/non-hidden code inputs.
8. After a normal owned-account login succeeds, first establish an app-origin read-only baseline, then test localhost/CORS readability against the same endpoints. If the account is not authorized for the target admin surface and only `401`/`404` or public data is readable, mark the candidate non-reportable and pivot instead of forcing a second account.


## References

- `references/2026-08-10-learning-cadence-registry-audit.md` — end-to-end cadence/registry audit method, schema-v2 integration pitfalls, state/provenance invariants, and verification checklist.
