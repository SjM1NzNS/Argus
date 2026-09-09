# Authenticated Intigriti paid-program inventory and BAC/API screening

Use this procedure when the user authorizes a read-only inventory with a locally stored Intigriti Researcher API PAT and asks to rank paid programs. It extends the public/private screening references; it does not authorize testing.

## Credential and confidentiality boundary

- Read the PAT from a mode-`0600` local environment file; never place it in command arguments, stdout, notes, reports, hashes, or chat.
- Set `umask 077` before fetching. Keep raw API responses and derived files containing private-program details under a mode-`0700` directory with files mode `0600`.
- **Assume paid briefs may embed test usernames, passwords, tokens, tenant IDs, or private attachment links.** Never print or copy raw brief text into a general report. Build a sanitized projection containing only selection evidence.
- Before saving/delivering artifacts, compare the exact PAT and likely credential literals extracted from raw briefs against every output without printing either value.

## Read-only collection sequence

1. Verify only file existence, owner/mode, one expected environment assignment, and non-empty token length. Do not display the file.
2. Use the official Researcher API base `https://api.intigriti.com/external/researcher/v1` with `Authorization: Bearer <local token>` and a descriptive user agent.
3. Enumerate open records with `GET /programs?statusId=3&limit=500`; honor pagination/max-count if present.
4. Partition records before ranking:
   - zero maximum bounty -> VDP/no-bounty exclusion;
   - challenge/CTF -> non-production exclusion even when a reward is displayed;
   - positive maximum bounty -> paid-program set.
5. Fetch `GET /programs/{programId}` for every paid record. Cache each response separately with retries/backoff and record HTTP status without printing the body.
6. A paid/open list record whose detail returns `403` remains **brief-gated**. Preserve name/status/reward/access class, but do not infer scope, restrictions, access, or viability from product branding.
7. Fetch paginated `GET /program-activities` to derive scope/rules freshness. Treat activities as program-change evidence, not hunter/report activity.
8. For public programs, optionally collect:
   - `/api/core/public/programs/{company}/{handle}/preview`
   - `/api/core/public/program/{programId}/leaderboard/alltime`
   Parse company/handle from the official detail URL and URL-encode path components.
9. Retry transient network/HTTP failures, but preserve persistent access gates as evidence rather than bypassing them.

## Evidence model

Keep these fields separate:

- API list status (`Open`), access class (`Public`, `Registered`, `Application`, `InviteOnly`), and reward;
- exact scope/rules content retrieved versus brief-gated;
- researcher-specific submission control (still unresolved unless the rendered authenticated UI was checked);
- legitimate no-cost owned-control path;
- target KYC/card/deposit/subscription/region/hardware/business-contract friction;
- published validation targets versus actual historical response performance;
- public all-time leaderboard entries versus active hunters;
- scope/rules update age versus program launch age;
- local Argus activation (`hunting_enabled`), which remains separate from every platform state.

Never call a private/registered gate proof of low competition. Never call all-time leaderboard entries active hunters. If a public endpoint returns a capped list (for example 100 rows), label it capped/high rather than exact. Unknown response or saturation receives a neutral/penalized score, never an optimistic one.

## BAC/API-first scoring and hard gate

When the user explicitly prioritizes BAC/IDOR and API/GraphQL, a useful 100-point screen is:

- 30: BAC/API/GraphQL/business-impact and reward fit;
- 25: no-cost owned access, no target KYC/fee friction;
- 20: published validation speed;
- 15: named saturation proxy;
- 10: source richness plus scope/rules freshness.

Retain every component and recompute totals deterministically. Then apply practical dispositions such as `GO-PREFLIGHT`, `CREDENTIAL-PREFLIGHT`, `CONDITIONAL`, `HOLD`, and `REJECT`. Raw score never overrides missing credentials, payment/KYC/hardware requirements, unsafe shared state, legal/safe-harbour concerns, or unavailable exact brief content.

Prefer evidence-backed lanes with two owned actors/tenants, explicit APIs/schemas/mobile clients, role/tenant/object models, and dedicated test/sandbox environments. Provision accounts sequentially when the user requires one-account-at-a-time auth handling; the user handles password/OTP/TOTP.

## Output and reconciliation

Save a dated selection snapshot under:

`$HOME/SecurityResearch/03 - Targets/Program Shortlists/`

Recommended artifacts:

1. sanitized all-open inventory CSV with one disposition/reason per record;
2. paid-program shortlist scorecard CSV with component evidence and first lane;
3. Markdown decision note with counts, evidence limits, strict top three, credential-preflight queue, holds/rejections, and `hunting_enabled: false`.

If an older invite shortlist exists, explicitly reconcile changes: name the old winner, state which new authenticated evidence changed access/scope/reward/restrictions, update the practical winner, and leave the historical snapshot intact. Do not let the correction live only in chat.

## Verification

Fail closed unless all pass:

- all-open inventory row count equals the API record count;
- paid/zero-reward/CTF/brief-gated accounting reconciles;
- every shortlist row has a positive reward, open API record, and exact brief content;
- score arithmetic matches components;
- response and saturation wording preserves metric type and uncertainty;
- direct URLs resolve (retry transient failures; do not treat auth redirects as submission proof);
- no VDP/CTF appears in the shortlist;
- no PAT or likely program-supplied credential literal appears in outputs;
- output files are mode `0600`;
- note contains no TODO/TBD and explicitly says no target/Burp/scope activation occurred.

## Pitfalls

1. **Raw brief excerpts in terminal/report.** Private briefs can contain reusable credentials. Parse locally and emit sanitized fields only.
2. **Open list equals accessible brief.** Detail `403` is a practical evidence gate, not a reason to guess.
3. **Public leaderboard equals low hunters.** It is lifetime platform participation and may be capped or globally misleading.
4. **Published SLA equals actual response.** Preserve it as a target, not measured triage history.
5. **Invite gate rewarded twice.** Private access can reduce exposure and reduce feasibility; do not score it optimistically without a no-cost owned control.
6. **Old shortlist left authoritative.** Authenticated late-brief evidence must trigger explicit re-ranking and a supersession note.
7. **Wide inventory becomes wide testing.** Screen broadly, then preflight one self-service target and one supplied-credential target; do not bulk-create or enable hunts.
