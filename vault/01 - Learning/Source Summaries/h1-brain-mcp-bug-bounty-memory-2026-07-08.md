---
type: source-summary
source: https://github.com/PatrikFehrenbach/h1-brain
reviewed_at: 2026-07-08
status: promoted-methodology
---

# h1-brain — MCP-backed bug bounty memory and attack briefing

## Source reviewed

- Repo: `https://github.com/PatrikFehrenbach/h1-brain`
- Local clone: `$HOME/SecurityResearch/01 - Learning/Repos/h1-brain`
- Commit: `bc70765ea8dcb7d6e5db08c4637df191cf54a1b8`
- Blog series fetched to: `$HOME/SecurityResearch/01 - Learning/Inbox/manual-h1-brain-20260708/`

## What it does

`h1-brain` is an MCP server for HackerOne data. It syncs personal rewarded reports, accessible programs, scopes, report attachments, and public disclosed reports into local SQLite databases, then exposes MCP tools for search and target briefings.

Core idea: turn a researcher’s own paid findings plus public paid disclosures into searchable context that can be cross-referenced against fresh scope before a session.

## High-signal workflow lessons for Argus

1. **Start hunts with a structured memory briefing, not raw recon.**
   - Fresh scope / severity caps / instructions.
   - Past successful weakness classes.
   - Untouched bounty-eligible assets.
   - Public disclosed reports for the same program.
   - Candidate weakness classes that paid elsewhere but have not been tested here.

2. **Separate local memory queries from live API sync.**
   - Local searches over prior reports and public disclosures are cheap/offline.
   - API sync and scope refresh are explicit operations with credential handling and rate-limit behavior.

3. **Use weakness-pattern mining to choose a branch.**
   - Example pattern: past SSRFs cluster around webhooks, PDF/export, image proxy, callback URL parameters.
   - Cross-reference those patterns with untouched assets and public disclosures before selecting the next branch.

4. **Use previous reports as style/evidence templates, not blind payload recipes.**
   - Past write-ups help reproduce report structure, impact framing, and proof standards.
   - Payloads/PoCs must be adapted to current scope and safety gates.

5. **Keep public disclosures as comparator evidence.**
   - Useful for identifying recurring endpoint families and weakness types.
   - Not proof of vulnerability on the current target.

## Argus adaptation

Argus should adopt the briefing shape, not the repo’s aggressive instruction posture.

Recommended Argus `hack()`-equivalent briefing sections:

- Scope contract summary.
- Active owned accounts / prerequisites / blocked flows.
- Prior Argus findings and candidates for the same program.
- Weakness classes that have worked across active programs.
- Untouched in-scope assets or local/static branches.
- Public disclosure / external RAG patterns routed through playbooks.
- Suggested next branch with explicit evidence gates and no-prompt safety boundaries.

## Safety changes required before applying

The repo’s `hack_instructions.md` says to run subdomain enumeration, port scans, directory brute forcing, exploit PoCs, and “Do not ask permission — hack.” Do **not** import that behavior into Argus.

Argus adaptation must preserve:

- scope-contract gates;
- no broad recon without approval;
- local/static-first branch selection;
- OTP/auth one-account-at-a-time discipline;
- owned-object replay gates;
- conservative reportability and false-positive checks.

## Implementation notes

- The cloned repo’s `disclosed_reports.db` is a Git LFS pointer, not the actual database, because `git-lfs` is not installed locally. Pointer claims actual size `17485824` bytes.
- `server.py` expects `H1_USERNAME` and `H1_API_TOKEN` environment variables at import time; do not run it in Argus without a private credential plan.
- `fetch_attachment()` returns expiring S3 URLs and should be treated as sensitive; do not write full attachment URLs to notes.
- Public report DB FTS uses SQLite FTS5 across `title` and `vulnerability_information`.

## Promotion decision

Promote the methodology as an Argus hunt-briefing pattern. Do not import the repo’s broad live recon instructions or credential handling directly.
