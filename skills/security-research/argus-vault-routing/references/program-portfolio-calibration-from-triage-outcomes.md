# Program portfolio calibration from triage outcomes

Use this reference after a cohort of submitted bug-bounty reports has received final dispositions, or whenever repeated `Duplicate` / `Infeasible` results raise a question about whether to change programs.

## Purpose

Do not judge a hunting strategy from a raw win/loss count. Aggregate outcomes by what they diagnose:

| Outcome | Primary signal | What it does not prove |
|---|---|---|
| `Duplicate` | Novelty/competition lag: the program says the same or a broader defect is already tracked | Independent confirmation of every reproduction, severity, or impact claim |
| `Infeasible` / below threshold | Threat-model, prerequisite, intended-boundary, or incremental-impact calibration problem | That the underlying behavior did not occur |
| Invalid / not reproducible | Evidence, environment, version, or report clarity problem | Necessarily that the general technique is worthless |
| Unique accepted | Technical, novelty, and program-threshold gates all passed | That the same strategy will remain novel elsewhere |

Always preserve technical validity, program disposition, and reward/credit as separate axes.

## Cohort diagnosis

For every final report, record:

1. program and target class;
2. attacker source and prerequisite;
3. protected trust boundary claimed;
4. concrete confidentiality/integrity/action effect;
5. default/typical versus optional/misconfigured deployment;
6. prior-art visibility and canonical detail;
7. disposition and reviewer rationale;
8. economic outcome.

Then cluster by cause, not vulnerability label. Useful patterns:

- Repeated duplicates on reachable cross-user/network/origin boundaries mean the technical selection is plausible but the surfaces are saturated or reached too late.
- Repeated infeasibles on local tools, trusted config, malicious projects, or admin/developer workflows mean the reportability gate is firing too late.
- A duplicate that triage rates High/critical is a strong class-selection signal but still a novelty failure.
- No invalid/not-reproducible outcomes indicates evidence quality may be sound; it does not excuse zero unique acceptances.
- A cohort with zero unique acceptances should trigger portfolio diversification and a harder submission gate rather than cosmetic reframing.

Do not overfit one report. Use a small cohort (roughly 5–10 final dispositions) or a repeated root-cause pattern before changing the whole portfolio.

## Portfolio response: wide selection, narrow execution

“Cast wide” at the **program-selection layer**, not through shallow scanner traffic.

Recommended operating model:

1. Screen multiple paid programs offline for access, scope, economics, freshness, and multi-actor workflows.
2. Run short, source-first qualification passes on the best candidates.
3. Kill programs quickly when all meaningful surfaces are corporate-auth gated, dead, third-party, or same-authority hardening.
4. Deep-dive only the top one or two programs where source-derived paths expose a real actor/object/tenant boundary.
5. Retain a smaller high-bar lane for established programs and a freshness-monitoring lane for new assets/releases.

A 60/25/15 split—new or less-contested programs / existing high-bar programs / freshness monitoring—is an illustrative starting point, not a permanent rule. Rebalance from measured outcomes and access friction.

## Incumbent-versus-challenger allocation

Use this when the user asks whether a shortlisted, invited, or newly verified target is “better than” an established incumbent hunt. Do not collapse the question into one universal ranking. Resolve at least three distinct decisions:

1. **Best next bounded hunt:** which target has the highest marginal probability of producing a unique, reportable result per research hour now?
2. **Best overall program:** which has the strongest long-term scope, payout ceiling, and high-impact opportunity?
3. **Best current portfolio allocation:** which incumbent follow-ups must be preserved while a challenger receives a qualification sprint?

### Evidence ledger

Compare only what is currently source-backed:

| Dimension | Required evidence |
|---|---|
| Marginal pipeline state | Remaining active candidates, exhausted branches, pending reviewer responses, and whether the next step is a fresh reset or a near-complete proof |
| Empirical program yield | Unique acceptances, duplicates, threshold/infeasible outcomes, invalids, rewards, and dominant failure mode—not raw report count alone |
| Practical access | Exact paid assets, self-registration/test credentials, owned-account/object controls, regional/KYC/fee/hardware/contract gates |
| Scope usability | Paid versus no-bounty source artifacts, excluded paths/identifier forms/classes, unlisted backend risk, and whether meaningful proof requires side effects |
| Competition | Named recent-activity or participation proxies with uncertainty; private invitation is friction, not proof of low saturation |
| Economics | Severity-specific attainable rewards as well as the headline maximum; quantify ceilings but do not let a jackpot dominate expected yield |
| Unfinished value | Pending corrections/appeals, separately reportable candidates, requested follow-ups, or evidence packages that should not be abandoned during rotation |

If only one private brief is verified, compare that target individually. Do not claim that the entire invitation batch beats the incumbent.

### Decision rule

A lower-ceiling challenger can be the better **next hunt** when all of the following hold:

- the incumbent’s marginal branches show repeated duplicate, threshold, or same-authority failures;
- the challenger has legitimate no-cost owned controls and source-rich actor/object/tenant boundaries;
- a short passive/source-first pass can cheaply confirm or kill the opportunity;
- exclusions still leave plausible paid, reportable impact; and
- incumbent unfinished value can be maintained without opening another broad discovery branch.

This does not make the challenger the better **program overall**. State the distinction explicitly. A useful conclusion shape is:

> Next bounded hunt: Challenger > Incumbent. Long-term upside: Incumbent > Challenger. Portfolio action: preserve named incumbent follow-ups, run one challenger qualification sprint, then apply explicit stop gates.

### Bounded rotation plan

1. Close prerequisite scope/submission-control checks and create the exact inactive contract before testing.
2. Run a time-boxed source-first qualification pass; define the budget in hours or one mission rather than “hunt until something appears.”
3. Derive first lanes from real product objects and roles, not generic vulnerability lists.
4. Stop quickly if meaningful APIs are unlisted, useful identifiers/classes are excluded, access requires payment/contract/third-party effects, or the remaining surface cannot support the desired severity.
5. Preserve pending incumbent reviewer responses and already reportable independent candidates as a maintenance lane.
6. Reallocate only after recording qualification hours, surviving boundaries, and the challenger’s practical stop/go result.

Avoid false precision: expected value is usually ordinal because active-hunter counts and acceptance probabilities are unpublished. Use “better next session,” “better long-term upside,” and “not yet comparable” rather than inventing bounty probabilities.

## Program selection scorecard

For a live, source-backed comparison of public programs—including Intigriti, YesWeHack, HackerOne, and Bugcrowd data sources, recent-activity proxies, confidence penalties, scoring, and verification—also load `references/cross-platform-public-program-screening.md`.

Prefer programs with:

- clear paid policy, safe harbor, and responsive triage;
- self-service access and two researcher-owned accounts;
- multi-user, multi-role, or multi-tenant workflows;
- mobile apps or source-rich SPAs with first-party APIs;
- invitations, shares, exports, reports, uploads, jobs, webhooks, OAuth linking, recovery, billing, or role transitions;
- newly added assets, recent launches, releases, acquisitions, or feature changes;
- awkward but legitimate barriers (regional language, mobile onboarding, specialized workflow) that reduce competition;
- safe canary creation and cleanup compatible with program rules.

Deprioritize:

- fee-gated opportunities without pre-cleared economics;
- corporate-only authentication with no legitimate entitlement path;
- unclear/no-reward VDPs when payout is the goal;
- local developer tools where the attacker already controls host/config/project authority;
- public config, debug metadata, or scanner findings without incremental capability;
- huge scopes whose reachable assets are mostly redirects, dead hosts, or third-party gates.

Optimize for competition-adjusted expected value, not obscurity alone.

## Hard pre-submission gate

Require all of the following before a bounty submission:

- [ ] Attacker-controlled input comes from a materially lower-trust actor.
- [ ] Trigger is reachable through a normal, supported, preferably default workflow.
- [ ] The attacker does not already possess equivalent code/config/host authority.
- [ ] A real authorization, account, tenant, origin, privilege, publication, or data boundary is crossed.
- [ ] Concrete confidentiality, integrity, or privileged-action impact is safely demonstrated.
- [ ] Positive and negative controls use owned accounts/objects.
- [ ] Incremental capability survives the intended-functionality counterfactual.
- [ ] Root cause is fix-independent from known prior art or the differential is explicit.
- [ ] Changelogs, advisories, CVEs, issues, PRs, sibling implementations, and public writeups were checked.
- [ ] Novelty and impact can each be stated in one or two precise sentences.

Mandatory counterfactual:

> Why can’t this actor already produce the same result through their intended authority?

If that answer is weak, keep the lead as hardening/HOLD and pivot.

## Local and developer-tool gate

Before investing heavily in a local/OSS developer-tool candidate, require at least one:

- default remote or hostile-origin ingress;
- documented isolation boundary between mutually hostile local actors;
- official untrusted import/gallery/template/project path;
- lower-privilege actor without equivalent host/project/config capability;
- managed-service execution under higher trust;
- trusted publication/build/deploy consumer that acts on attacker-controlled input.

A denylist bypass, symlink follow, wildcard bind, loopback endpoint, or project-file mutation is only a primitive until this boundary is proven.

## Duplicate-risk reduction

- Prioritize newly introduced features and recently changed consumers over obvious CRUD objects.
- Search root causes, not only report titles or payload strings.
- Compare attacker source, missing control, sink, consumer, and fix independence.
- Do not treat another endpoint, model, browser, alias, or object type behind the same check as novel.
- When canonical details are private, record uncertainty; do not invent a differential.

## Operational metrics

Track per program and per class:

- qualification hours;
- deep-hunt hours;
- report count;
- duplicate rate;
- infeasible/threshold rate;
- invalid/reproduction rate;
- unique acceptance rate;
- reward/credit outcome;
- dominant prerequisite and boundary failure.

Use these to rebalance quarterly or after each meaningful cohort. The aim is not maximum submissions; it is higher unique-acceptance yield per research hour without lowering evidence quality.

## Secondary methodology references

- [The-XSS-Rat — 2026 Bug Bounty Guide](https://github.com/The-XSS-Rat/SecurityTesting/blob/master/Checklists/2026-bug-bounty-guide.md): obvious endpoints attract speed-hunter duplicates; neglected functions and legitimate barriers can improve novelty.
- [win3zz — RCE via Insecure JS Sandbox Bypass](https://medium.com/@win3zz/rce-via-insecure-js-sandbox-bypass-a26ad6364112): recommends focusing on less-tested applications/features rather than only popular programs.
- [Zhero — Eclipse on Next.js](https://zhero-web-sec.github.io/research-and-things/eclipse-on-nextjs-conditioned-exploitation-of-an-intended-race-condition): emphasizes exploitation methods or outcomes that materially differ from already published work.

These are secondary strategic references, not evidence about any private program or canonical finding.
