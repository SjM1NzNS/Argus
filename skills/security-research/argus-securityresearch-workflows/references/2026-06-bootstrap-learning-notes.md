# 2026-06 Argus Workspace Bootstrap and Learning Ingestion Notes

This reference captures reusable details from the initial Argus workspace bootstrap and learning dry run.

## Created workspace classes

The workspace follows these class directories:
- `00 - System`: operating policies and prompts
- `01 - Learning`: inbox, Web2/Web3 learning notes, source summaries, skill patch proposals, rejected lessons
- `02 - Vulnerability Playbooks`: Web2/Web3 playbook folders
- `03 - Targets`: target workspaces after scope contract
- `04 - Reports`: drafts/submitted/accepted/rejected/duplicates
- `05 - Agent Outputs`: Codex/specialist/tool-output reviews
- `06 - Evals`: Web2/Web3 eval stubs and proposals
- `07 - Skill Changelog`: monthly skill update log
- `08 - Templates`: YAML-frontmatter note templates
- `09 - Raw Evidence`: sensitive raw evidence, mode `0700`
- `10 - Tool Output`: general tool outputs
- `11 - Scripts`: learning/hunts/utils scripts
- `12 - Logs`: cron/learning/hunts/errors logs

## Core policy files

High-value policy files under `00 - System`:
- `autopilot.md`
- `learning-engine.md`
- `source-quality.md`
- `evidence-and-reportability.md`
- `specialist-dispatcher.md`
- `skill-router.md`
- `skill-gap-policy.md`
- `tool-policy.md`
- `reconftw-policy.md`
- `burp-policy.md`
- `secret-validation-policy.md`
- `web2-skill-index.md`
- `web3-skill-index.md`
- `target-initialization.md`
- `initialize-target-prompt.md`
- `learning-compiler-prompt.md`
- `manual-learning-run.md`

## Learning dry-run outputs

A high-signal dry-run compiler pass should produce:
- source summary under `01 - Learning/Source Summaries/`
- Web2/Web3 technique extraction notes under `01 - Learning/Web2` and `01 - Learning/Web3`
- skill patch proposals under `01 - Learning/Skill Patch Proposals/`
- eval update proposals under `06 - Evals/Web2` and `06 - Evals/Web3`
- monthly changelog draft entries under `07 - Skill Changelog/YYYY-MM.md`

## Initial extracted lessons

Web2:
- Access control requires two owned principals/objects and server-side authorization evidence.
- Identifiers are leads, not findings.
- Auth/session issues need state-transition evidence.
- OAuth/SSO issues need token/account/client impact, not just redirect weirdness.
- GraphQL authorization is resolver/mutation-level.
- XSS needs execution context, browser/CSP feasibility, victim model, and meaningful impact.
- SSRF/webhooks require safe validation design and often Zone 3 approval.
- Secrets require redaction and offline-first validation.

Web3:
- Reentrancy requires callback-capable path, invariant break, and measurable impact.
- Rounding/share-accounting bugs require economic impact, not dust-only math.
- Oracle findings require realistic manipulation/staleness path and impact sequence.
- Admin-only issues are usually invalid unless trust boundary/program policy says otherwise.
- Postmortems are impact-realism sources, not direct report evidence.

## Learning ingestion hardening from first real smoke test

A full non-dry run can time out if AppSec.fyi linked resources or dynamic sites expand too far. Preserve these controls in future script changes:

- `ARGUS_MAX_TOTAL_SECONDS` caps total runtime.
- `ARGUS_MAX_SOURCES_PER_GROUP` caps fetches per source group.
- `ARGUS_PRIORITY_ONLY=1` skips non-high-priority sources for cron/smoke runs.
- `ARGUS_MAX_APPSEC_LINK_FETCHES` caps actual metadata fetches for AppSec.fyi linked resources.
- `ARGUS_MAX_APPSEC_LINK_RECORDS` caps total linked-resource records, including skipped/deferred records.
- Social/share URLs from X/Twitter, LinkedIn, Facebook, Reddit, and Hacker News should be marked `rejected_low_signal` or filtered.
- Dynamic sources such as Solodit/Cyfrin and HackerOne Hacktivity should become `manual_review_required` placeholders rather than failing the run.

Cron-safe bounded line pattern:

```cron
30 7 * * * ARGUS_PRIORITY_ONLY=1 ARGUS_MAX_TOTAL_SECONDS=180 ARGUS_MAX_SOURCES_PER_GROUP=6 ARGUS_MAX_APPSEC_LINK_FETCHES=8 ARGUS_MAX_APPSEC_LINK_RECORDS=25 /bin/bash "$HOME/SecurityResearch/11 - Scripts/learning/run_learning_ingest.sh" >> "$HOME/SecurityResearch/12 - Logs/cron/learning-cron.log" 2>&1
```

## Initial playbook files created from learning pass

The first high-signal playbook build created these class-level drafts:

Web2 Access Control:
- `overview.md`
- `test-checklist.md`
- `false-positives.md`
- `evidence-requirements.md`
- `reportability.md`

Web2 Secret Exposure:
- `overview.md`
- `false-positives.md`
- `evidence-requirements.md`
- `reportability.md`

Web2 XSS:
- `overview.md`
- `test-checklist.md`
- `false-positives.md`
- `evidence-requirements.md`
- `reportability.md`

Web3 Reentrancy:
- `overview.md`
- `attack-patterns.md`
- `false-positives.md`

Web3 Share Accounting / ERC4626:
- `Share Accounting/invariants.md`
- `ERC4626/overview.md`
- `ERC4626/attack-patterns.md`
- `ERC4626/false-positives.md`

Web3 Oracles:
- `overview.md`
- `attack-patterns.md`
- `false-positives.md`

Next best follow-up after this build: run evals against the new playbooks before using them in live hunts.

## First eval pass results

The first eval pass populated and checked:
- `Web2/weak-idor-invalid.md`
- `Web2/real-idor-valid.md`
- `Web2/firebase-config-not-secret.md`
- `Web2/secret-exposure-valid.md`
- `Web3/reentrancy-valid.md`
- `Web3/reentrancy-nonimpactful.md`
- `Web3/oracle-manipulation-valid.md`
- `Web3/oracle-manipulation-unrealistic.md`
- `Web3/rounding-low-impact.md`

Reusable eval pattern:
- Populate TODO-only eval stubs with concrete scenarios and expected decisions.
- Verify each eval answers reportability, severity, missing proof, triage rejection, next action, and report/hold/discard.
- Write a consolidated eval pass report under `06 - Evals/YYYY-MM-DD-playbook-eval-pass.md`.
- Patch the playbook immediately if the eval exposes a missing gate.
- Update `07 - Skill Changelog/YYYY-MM.md` after eval-driven patches.

Eval-driven patches from this pass:
- `Web2/Secret Exposure/reportability.md`: add exposure-alone/no-use guidance, safe validation boundary, and warning against severity assumptions from unvalidated credential capability.
- `Web3/Share Accounting/invariants.md`: add dust-only/below-gas/amplification/economic-impact severity gate.
- `Web3/ERC4626/false-positives.md`: cross-check Share Accounting invariants and reject non-amplifiable dust-only effects.

## Next proposal batch files created

From the patch proposals and skill gaps, the next batch created:

Web2 OAuth & SSO:
- `overview.md`
- `test-checklist.md`
- `false-positives.md`
- `evidence-requirements.md`
- `reportability.md`

Web2 GraphQL:
- `overview.md`
- `test-checklist.md`
- `false-positives.md`
- `evidence-requirements.md`
- `reportability.md`

Web2 SSRF / Webhooks:
- `SSRF/overview.md`
- `SSRF/test-checklist.md`
- `SSRF/false-positives.md`
- `SSRF/evidence-requirements.md`
- `SSRF/reportability.md`
- `Webhooks/test-checklist.md`

Web3 Access Control / Upgradeability:
- `Access Control/overview.md`
- `Access Control/attack-patterns.md`
- `Access Control/false-positives.md`
- `Upgradeability/overview.md`
- `Upgradeability/attack-patterns.md`
- `Upgradeability/false-positives.md`

Web3 Reporting:
- `Reporting/postmortem-translation.md`
- `Reporting/reportability.md`

Key gates from the next batch:
- OAuth: open redirects are leads unless token/account/session impact is shown.
- GraphQL: introspection/schema visibility is a lead unless unauthorized resolver/mutation impact is reproduced.
- SSRF/Webhooks: benign callbacks are leads; internal/metadata/port/protocol testing is Zone 3 unless explicitly allowed.
- Web3 Access Control: “admin can do admin things” is invalid unless a boundary is broken or policy accepts centralization risk.
- Web3 Reporting: postmortem analogy is not report evidence; translate incidents into invariants, code patterns, evals, and PoCs.

Next best follow-up after this batch: run evals for `oauth-open-redirect-low-or-invalid`, `oauth-csrf-medium`, `graphql-introspection-lead-only`, `graphql-bfla-valid`, `ssrf-blind-callback-hold`, `admin-only-issue-invalid`, and `postmortem-translation-not-report-evidence`.

## Initial skill gaps

- Web2 XSS context/impact playbook
- Web2 OAuth & SSO account-linking playbook
- Web3 postmortem-to-bounty translation playbook
- Web3 share-accounting invariant checklist
