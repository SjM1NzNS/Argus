# Web3 audit pause, portfolio review, and opportunity radar

Use this pattern when a bounded smart-contract review reaches diminishing returns, the user wants to preserve it for later, or Argus needs to monitor for more tractable newly launched opportunities.

## Pause as resumable, not abandoned

1. Update the authoritative scope contract—not just prose notes:
   - set `status: paused_resumable`;
   - set `hunting_enabled: false`;
   - refresh the UTC timestamp;
   - preserve all authorization/network restrictions.
2. Rewrite `checkpoint.md` as the single resume entry point. Include:
   - exact scope/pin model and immutable worktree locations;
   - untouched baseline result;
   - targeted PoCs/invariants and exact pass counts;
   - candidate disposition ledger (known issue, accepted risk, trusted role, dust, invariant pass, unresolved);
   - current finding count and whether any report is submission-ready;
   - clean-repository and temporary-test cleanup state;
   - materially distinct remaining branches only;
   - a precise resume procedure.
3. Append a timestamped `hunt-log.md` entry explaining why the review paused and confirming no target interaction occurred beyond the approved mode.
4. Keep hypotheses, tested-items, fuzz logs, known-issue mappings, audit references, and PoCs. Do not compress them into a vague “no bugs found” conclusion.
5. Verify the scope contract and checkpoint after edits. A pause is incomplete if `hunting_enabled` remains true.

## Delayed-review reconciliation after a pause

A pause decision is provisional until all already-dispatched workers and long-running analyzers have returned. If delayed output arrives after the checkpoint:

1. Compare it against the current source pins and deployment reconciliation; do not blindly reopen from a worker's self-reported priority.
2. Separate genuinely distinct root causes from same-noun overlap. For example, a fee-base accounting asymmetry is not automatically the same issue as an epoch-rollover bug merely because both affect “utilization.” Read the exact prior finding before subtracting it.
3. Promote only the strongest surviving lead into one narrow kill experiment. Keep broad hunting disabled while validating it.
4. Require executable positive and negative controls, quantified economics, full-position cleanup, and provenance:
   - prove the suspected residue/state transition exists;
   - measure irreversible attacker cost, returned principal, residual accounting credit, and remaining shares/claims;
   - fuzz a realistic bounded input domain;
   - assert the candidate credit cannot exceed cost unless the exploit thesis specifically predicts amplification;
   - inspect Git blame/history and the audited revision to determine whether the behavior predates the audit or is a post-audit semantic delta.
5. Do not treat “residual accounting after a closed position” as reportable by itself. Show a complete reward/profit/loss sequence that beats fees, gas, opportunity cost, and protocol lower-bound behavior.
6. If the economic/novelty gate fails, mark the hypothesis invalidated, preserve the spike and logs, append the delayed result to the checkpoint/log, refresh the scope timestamp, verify original repositories remain clean, and keep the campaign paused.
7. If it survives, reopen only that hypothesis branch and update the authoritative scope contract before additional testing.

This prevents two opposite errors: ignoring late evidence after declaring completion, and reopening an entire saturated campaign because a reviewer found an interesting but unprofitable state asymmetry.

## Diminishing-return decision gate

Pause or reduce allocation when most new hypotheses repeatedly converge on:

- already disclosed/accepted findings;
- fully trusted governance or administrative behavior;
- documented deployment assumptions;
- bounded rounding dust with no amplification;
- temporary denial/failure with no accepted economic impact;
- code paths absent from the independently pinned deployed snapshot.

A zero-finding review can still be a successful capability evaluation when it demonstrates exact pin reconciliation, historical dependency recovery, executable invariants, reference-model fuzzing, known-issue subtraction, actor-model discipline, and non-overclaiming.

## Read-only opportunity radar

Maintain target discovery separately from active hunting.

1. Monitor official opportunity pages such as Immunefi, Code4rena, Sherlock, Cantina, and CodeHawks. Social posts are discovery only; verify every candidate against its official page.
2. Compare current entries with a persisted previous-state file. Report only new or materially changed opportunities: launch, scope/repo, reward, deadline, PoC rules, or known-issue/audit changes.
3. Rank tractability rather than headline bounty. Prefer:
   - narrow public Solidity scope;
   - Foundry tests or reproducible local setup;
   - recent or unaudited changes;
   - clear accepted impacts and PoC rules;
   - sufficient remaining contest time;
   - low known-issue/audit saturation.
4. Penalize bridges, custom cryptography, sprawling multichain scope, missing public source, unclear deployment mapping, heavy prior-audit saturation, and deadlines too short for responsible review.
5. Keep the radar read-only: no cloning, initialization, live calls, contract interaction, registration, or testing until the user selects a target and a current scope contract is captured.
6. Keep notifications compact: at most three ranked changes; otherwise a one-line no-change status.
7. For recurring jobs, use a self-contained prompt, dedicated state path, official-source requirement, explicit no-testing boundary, pinned model/provider where supported, and verify the resulting job configuration.

### Change-materiality and portfolio-priority gate

A platform `Last Updated` timestamp is only a discovery signal. Do not treat it as fresh code, fresh scope, or a reason to begin a hunt unless the official source exposes a concrete delta.

Classify each monitored change as one of:

- **confirmed fresh scope** — a newly added repository, file, deployment, or contract with a visible addition date;
- **confirmed code/deployment delta** — an immutable commit or verified deployment mapping establishes what changed;
- **rules/economics delta** — reward, impact, deadline, KYC, Safe Harbor, triage, arbitration, or PoC requirements visibly changed;
- **opaque metadata update** — only the page timestamp advanced and no revision history or dated asset change is exposed;
- **status removal/closure signal** — a listing disappeared or stopped accepting submissions, without inferring why.

Rank confirmed fresh scope and code/deployment deltas above opaque metadata updates, even when the opaque program has a cleaner repository shape. Preserve both of these distinctions in the recommendation:

- **best immediate novelty opportunity** — the freshest bounded asset with a plausible unsaturated review window;
- **best long-form tractability target** — the cleanest repository, framework, impact table, and dispute/triage posture if novelty is not time-sensitive.

For the top candidates, compare official live pages on:

1. exact newly added asset or deployment and its addition date;
2. source repository, immutable pin/deployment reconciliation, framework, tests, and baseline reproducibility;
3. scope breadth, dependency/chain count, and accounting or bridge complexity;
4. prior audits, known issues, inherited implementations, and whether the new asset is configuration-only or a meaningful semantic delta;
5. accepted impacts, PoC mode, mutation/network constraints, KYC, Safe Harbor, managed triage, and arbitration;
6. critical/high payout mechanics, guaranteed minimums, discretionary language, participant pool, deadline, and entry or submission fees;
7. likely time to establish provenance, build the baseline, subtract duplicates, and reach one executable high-value branch.

When economics are acceptable but uncertainty remains, recommend a **bounded source-only preflight**, not a full hunt. Define candidate-specific kill gates before initialization, such as:

- no trustworthy source-to-deployment mapping;
- newly scoped deployments are configuration-only clones with no meaningful unaudited delta;
- the exact component is already covered by audits, known issues, or inherited exclusions;
- all plausible impacts require trusted-role misuse, forbidden oracle/third-party interaction, or unsupported live testing;
- the remaining reward or contest runway cannot justify executable proof and hostile review.

A high headline bounty must not outrank a smaller fresh component merely because its maximum is larger. Conversely, freshness alone must not override KYC, legal posture, unsafe reproduction rules, weak triage, or dependency sprawl. Report the trade-off explicitly and recommend one next bounded action. Keep monitoring separate from target initialization; current scope capture and user approval remain mandatory.

## Contest participation go/no-go gate

Do not turn a radar score or headline reward into an automatic recommendation to hunt. At decision time, re-open the live official contest page because scope, allocation, status, and rules can change within a day.

1. Resolve which contest the user means when several are active. If one has just materially changed, use it as the explicit assumption and state how the answer differs for the alternatives.
2. Decompose displayed rewards into the amount actually available to ordinary participants versus lead-senior, judge, referral, or conditional allocations. Report both the participant pool and its percentage of the headline total; use participant economics in the decision.
3. Recalculate fit from the live page: nSLOC/file count, remaining time, chain count, language/framework, direct repository and source pin, accepted impacts, PoC rules, KYC/Safe Harbor, trusted-role assumptions, and whether source access requires account connection. If the page omits a timezone, do not invent an exact remaining-duration timestamp.
4. Inspect every officially linked `SECURITY.md`, known-issue list, audit folder, AI scan, and recent report. Count visible artifacts and note their dates. A same-week report or scan is a major saturation penalty even when the scope is narrow.
5. Subtract explicitly trusted actors and inputs before ranking hypotheses. Admin/guardian/servicer-provided values, trusted off-chain accounting, supported tokens, and accepted design choices can eliminate most scanner output. Prioritize only untrusted or accepted low-privilege paths that can produce the contest's minimum severity.
6. Recommend a **bounded qualification sprint** instead of full commitment when source/build/test details are still gated:
   - obtain the exact repository and commit;
   - capture scope, specs, invariants, and exclusions;
   - prove the untouched local test baseline;
   - index prior findings for duplicate subtraction;
   - map scope and run analyzers as lead generators;
   - continue only if one plausible reportable PoC branch or several concrete unsaturated invariant branches survive.
7. Define stop conditions before starting: unbuildable source, no exact pin, all valuable paths depend on trusted-role misuse, obvious branches are already disclosed, or remaining time cannot support executable proof and hostile review.
8. Keep career/learning value separate from expected payout. A small, single-chain accounting/state-machine contest may justify a short portfolio sprint even when saturation makes full-time expected value poor.

For lending/vault contests, initially prioritize cross-position contamination, ledger-versus-vault conservation, asynchronous deposit/redemption lifecycle edges, NFT transfer/stuck states, repeated accrual/NAV ordering, and untrusted input bounds. Deprioritize trusted-role bad values, dust-only rounding, EIP-only deviations, unsupported tokens, and findings already present in official audit material.

## Career/portfolio interpretation

Do not infer that one saturated protocol review determines whether the user is suited to Web3 auditing. Separate:

- **auditing capability**: code comprehension, invariant design, testing, accounting reasoning, false-positive subtraction, and report writing;
- **target economics**: audit saturation, scope size, freshness, accepted impacts, and opportunity timing;
- **career fit**: enjoyment of concentrated state-machine reasoning and variable feedback versus broader AppSec architecture, developer collaboration, cloud/API/auth work, and more stable employment paths.

A robust hybrid recommendation is Web2/Product AppSec as a broad professional base plus selective smart-contract auditing as a specialization, then compare both tracks through concrete portfolio work rather than hypothetical preference alone.
