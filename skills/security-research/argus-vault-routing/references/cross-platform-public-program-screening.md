# Cross-platform public and private-invite bug-bounty program screening

Use this reference when comparing paid programs across two or more platforms, or when ranking a batch of private invites. It is especially relevant when the decision criteria include response speed, novelty, low competition, likely P1/P2 surface, and no-cost access.

This is a **selection workflow**, not authorization to test. Re-read the live brief and scope immediately before any target action. A private invite-card transcription is selection input, not a substitute for the authenticated brief.

## Core principle

Platforms rarely expose a live active-hunter count. Never present one as known. Estimate saturation from named proxies and keep the proxy visible in the output:

- recent reports (24 hours / 7 days / current month);
- reports received in the last 90 days;
- all-time leaderboard entries;
- program launch or migration date;
- newly added/updated scope;
- self-service versus request-only/KYC/regional/hardware access;
- breadth and obviousness of the attack surface;
- shared-code or sibling-program duplicate treatment.

Recent activity is generally more decision-useful than lifetime totals. A program with 88 lifetime reports and 27 in the last week is a current rush, not a quiet target.

## Collection sequence

When the user gives a platform order, preserve it in both research and presentation. For each platform:

1. Enumerate only open, paid programs; explicitly reject VDPs, suspended programs, and expired engagements.
2. Collect 3–5 plausible candidates before cross-platform scoring.
3. Verify each candidate on its direct live brief, not only a marketing directory card.
4. Record exact source URL, reward range/currency, access requirements, scope count/rating, program age/update signal, response metrics, and saturation proxies.
5. Distinguish first response, triage, bounty, and payment time. Do not collapse them into one “fast” label.
6. Note important rejected programs and the reason; this prevents a later session from re-selecting a current rush or stale listing.

## Platform-specific public data

### Intigriti

Useful public endpoints:

- Preview: `https://app.intigriti.com/api/core/public/programs/{company}/{handle}/preview`
- All-time leaderboard after obtaining `programId`: `https://app.intigriti.com/api/core/public/program/{programId}/leaderboard/alltime`

The preview response exposes open/status information, reward tables, currency, and program ID. The leaderboard count is **all-time Intigriti participation**, not a live hunter count and not global target saturation.

Always open the direct human-readable detail page. Marketing directories can lag live status; a listed program may already be suspended. A newly listed global brand or migrated program can have only a few Intigriti leaderboard entries while remaining heavily researched elsewhere.

Public response-time metrics may be absent. Score them as unknown/neutral with lower confidence rather than guessing from “managed,” platform reputation, or program age.

#### Private Intigriti invites

Use this evidence hierarchy and preserve the label in notes and tables:

1. **Exact paid brief verified:** authenticated detail page, scope, rules, reward table, access requirements, and submission control were directly inspected.
2. **User-provided invite card:** program name, invite date, reward card, update age, and card-open label were transcribed but the brief was not independently inspected.
3. **Separate public VDP context:** a same-company VDP can show brand maturity or product context, but its scope, status, rules, and leaderboard must never be substituted for the invited paid program.
4. **Product metadata only:** first-party websites, app stores, documentation, and store listings can support access-friction and source-richness analysis, but they do not establish bounty scope.

For a private-invite batch:

1. Save a dated inventory snapshot before scoring; preserve incomplete cards as incomplete rather than inferring missing rewards, update ages, or status.
2. Try the authenticated program list/direct brief first. Do not copy browser cookies, bypass login, solve CAPTCHAs, or treat an unauthenticated marketing page as the private brief.
3. Search Intigriti’s public directory by both exact program title and company name. This distinguishes an exact public paid program from a same-company VDP or no public listing.
4. When the brief is unavailable, label the ranking **provisional** and keep exact scope, rules, response metrics, test credentials, and submission readiness unresolved.
5. Use official product/app metadata only to estimate legitimate self-service access, client freshness, source richness, and business-object models. Explicitly say that a first-party app may still be out of paid scope.
6. Provide a mandatory authenticated-brief preflight and an immediate pivot condition for the selected target. Do not create or enable a hunt contract from the invite-card snapshot alone.
7. If one exact paid program is public, extract its full live detail, exclusions, access FAQ, recent activity, response statistics, preview API, and leaderboard. Use that stronger evidence only for that program.

A valid private-invite result can still choose a next **preflight candidate**, but it must not claim that every paid brief was checked when only invite cards and public product sources were available.

### YesWeHack

Useful public endpoints:

- Directory: `https://api.yeswehack.com/programs?filter[type][]=bug-bounty&page=N`
- Detail: `https://api.yeswehack.com/programs/{slug}`

High-value detail fields include:

- `bounty_reward_min`, `bounty_reward_max`;
- `stats.total_reports`;
- `stats.total_reports_last24_hours`;
- `stats.total_reports_last7_days`;
- `stats.total_reports_current_month`;
- `stats.average_first_time_response`;
- `scopes` and `account_access`.

Use the rendered page to confirm currency symbols and human-readable response wording. YesWeHack’s recent report counters are particularly useful for detecting a fresh hunter rush.

### HackerOne

Use the directory for launch-date and bounty filters, then the direct program page’s **Program highlights** and **Stats** sections. Capture separately:

- first response;
- triage;
- bounty time;
- reports received in the past 90 days;
- bounties paid/resolved and reward range where published.

`Reports received in 90 days` is not unique hunters. New launch dates can represent migrations or newly public versions of mature programs; check the 90-day report count before treating novelty as low saturation. High response efficiency does not compensate for hundreds or thousands of recent reports when low competition is a primary goal.

### Bugcrowd

Useful public directory endpoint:

`https://bugcrowd.com/engagements.json?category=bug_bounty&sort_by=starts&sort_direction=desc&page=N`

Useful fields include:

- `briefUrl`;
- `rewardSummary`;
- `scopeRank`;
- `accessStatus`;
- `badgeVariant`;
- `serviceLevel`;
- `isPrivate`.

Treat explicit `Priority Triage` / expedited-triage service levels as verified signals. A program name containing “Managed” is not a published response-time statistic. Bugcrowd generally does not expose public median response or current hunter/report volume, so saturation remains an age/access/scope estimate and should be labelled lower confidence.

## Competition-adjusted scoring

A useful default weighting is:

- 25% verified response/triage speed;
- 25% low saturation;
- 20% novelty/newness;
- 20% plausible P1/P2 boundary and reward ceiling;
- 10% no-cost access and fit with source-first owned-control testing.

Score each dimension on a common scale, calculate deterministically, and retain the component evidence. The numerical score is a prioritization aid, not a bounty forecast.

Confidence rules:

- Unknown response metrics receive a neutral or slightly penalized score, never an optimistic one.
- Platform-only participation counts are discounted for globally famous or migrated targets.
- Access friction can reduce competition, but also reduce researcher feasibility; reward it only when a legitimate no-cost path exists.
- High reward alone cannot rescue KYC, paid-phone, hardware-purchase, chain-fee, game/subscription purchase, deposit, customer-policy, bank-identity, business-registration, partner-tenant, or inaccessible corporate-auth requirements.
- Prefer source-rich SPAs/mobile clients, first-party APIs, multi-account/multi-role/multi-tenant workflows, and safe owned-object controls.

### Mandatory feasibility gate after scoring

The default model assigns only 10% to access, so a high-impact but inaccessible program can top the raw score. Always produce two distinct results when this occurs:

1. **Raw score:** the deterministic weighted result with all component evidence visible.
2. **Practical disposition:** `GO`, `PREFLIGHT`, `CONDITIONAL`, `HOLD`, or `REJECT` after applying access and evidence gates.

A program cannot be the immediate hunt target unless there is a legitimate, program-permitted, no-cost path to at least one meaningful owned control. If access is unresolved, it may be the next authenticated-brief preflight candidate but not an enabled hunt. Record exactly what would make a conditional target leapfrog the current choice, and define a fast pivot condition so inaccessible prestige targets do not consume the hunt.

Score **source richness** and **practical access** separately even when they share the 10% component:

- Public API documentation, schemas, current APK/IPA files, repositories, and developer portals can justify a high source-richness assessment.
- They do **not** justify a high access score unless the program permits a self-service owned account/object or supplies approved credentials, a sandbox, or a test tenant.
- Sales-provisioned or contract-backed sandboxes should normally remain low/conditional access, even when their documentation exposes ideal actor and state models.
- When an authenticated brief later reveals `no bounty` clients, unlisted backend hosts, path/object-form exclusions, or enterprise provisioning, recalculate the score and practical rank immediately; do not preserve the earlier winner for narrative consistency.

## First-pass output

Produce:

1. a 3–5 candidate table per platform in the requested order;
2. one strict top-three list across all platforms;
3. a short “first hunt lane” for each top candidate, derived from the program’s real product model rather than generic vulnerability labels;
4. caveats for access, shared code, fee/KYC/region constraints, and unpublished metrics;
5. notable rejections such as suspended programs or current report-volume spikes;
6. a source timestamp and direct program URLs;
7. for private invites, an evidence label for every row (`exact paid brief`, `invite card`, `separate VDP context`, or `product metadata only`), plus unresolved private-brief fields;
8. separate raw-score and practical-disposition tables whenever a feasibility gate changes the ranking;
9. a mandatory authenticated-brief preflight and an explicit pivot condition for the selected private program.

Phrase the outcome precisely. When most private briefs were unavailable, say **“recommended next preflight candidate”** or **“provisional next target pending brief import,”** not “all programs verified.”

For Argus, save durable snapshots under:

`$HOME/SecurityResearch/03 - Targets/Program Shortlists/`

The note must say that it is a selection snapshot and that live scope/status must be rechecked before testing.

### When the user asks to create the folders

Load `argus-securityresearch-workflows` and follow its linked reference `references/cross-platform-shortlist-workspace-initialization.md`. Materialize every selected candidate—not rejected near-misses—under a platform-qualified target name, mirror the Burp workspace, preserve the score/rank/first lane, and initialize every scope contract as draft with `hunting_enabled: false`. Create a central workspace inventory and verify the complete tree; do not turn a shortlist into authorization.

### When the user asks whether all programs have hunting enabled

Follow `references/live-program-hunting-status-verification.md`. Treat this as a fresh, dated audit rather than reusing the screening result. Separate: (1) platform open/accepting submissions, (2) researcher eligibility and practical access, and (3) local Argus scope activation. Application-open is conditional until accepted, HTTP 200 is not submission proof, and no draft contract should be bulk-enabled from the audit.

## Source-first transition

Selection should lead to **wide screening, narrow execution**:

- start one or two deep hunts, not all listed programs;
- request access to promising gated programs in parallel;
- map explicitly referenced JS/config/manifests/mobile artifacts before endpoint probing;
- use two owned accounts where permitted;
- stop or re-rank when meaningful surfaces are dead, third-party, corporate-auth gated, same-authority hardening, or require unapproved spend;
- require real actor/object/tenant boundaries before escalating a local sandbox, project-file, or trusted-config primitive.

## Common pitfalls

1. **Directory-card trust.** Verify direct status; directory data can be stale.
2. **Lifetime-count optimism.** Check recent activity; low lifetime totals can hide a launch-week rush.
3. **Platform-count overreach.** A tiny platform leaderboard does not mean a global brand is unhunted.
4. **Managed equals fast.** Only published SLA/median/service-level data supports a speed claim.
5. **Shared-family duplication.** Do not rank several sibling storefronts as independent opportunities when the platform treats one shared root cause as a duplicate.
6. **Fee friction disguised as novelty.** Regional numbers, KYC, hardware, subscriptions, deposits, and chain fees need an explicit no-cost path or pre-cleared economics.
7. **Reward-only ranking.** Prefer reachable high-impact boundaries over large theoretical maximums.
8. **No rejection log.** Preserve why obvious candidates were excluded.

## Verification checklist

- [ ] Every candidate is currently open and paid on its direct brief.
- [ ] Reward range and currency were checked on the detail page/API.
- [ ] Response, triage, bounty, and payment metrics remain distinct.
- [ ] Saturation claims name their proxy and time window.
- [ ] Unknown metrics are labelled and confidence-penalized.
- [ ] Recent activity was checked where available.
- [ ] Global maturity/migration risk was considered.
- [ ] Fee/KYC/region/hardware/account requirements were recorded.
- [ ] Shared-code sibling duplicate risk was considered.
- [ ] The top three follow the scoring evidence rather than platform preference alone.
- [ ] Saved Markdown contains all required sections and direct links.
- [ ] Embedded URLs were checked, and the live brief will be rechecked before testing.
