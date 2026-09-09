---
type: source-summary
status: promoted
created: "2026-07-10"
run: daily-20260710-073001
---

# Daily 2026-07-10 lightweight review — IDOR/access-control promotion

## Reviewed

- Static ingest: `01 - Learning/Inbox/daily-20260710-073001-static/learning-candidates.jsonl`
  - 155 records; 3 actual-content records; 57 index/listing records; 89 not-fetched/skipped records.
- Browser DOM ingest: `01 - Learning/Inbox/daily-20260710-073001-browser-dom/learning-candidates.jsonl`
  - 60 records; 1 actual-content record; 13 index/listing records; 43 skipped-seen records.
- Manual Preview.is note: `01 - Learning/Inbox/manual-preview-is-20260710-062018/preview-is-results.md`
  - MCP/tool-description poisoning material; high-signal but already covered by current AI/LLM MCP playbooks, so no separate promotion today.

## Promoted lesson

Source: `https://chs.us/guides/idor/` via AppSec.fyi linked-resource discovery for IDOR / Access Control.

Concise Argus lesson: IDOR/BOLA review should include a structured identifier-surface sweep before replay testing. Look beyond obvious path IDs: query/body/header/context selectors, client-supplied IDs on create/update, alias routes such as `me`/`self`/`current`, HTTP method/content-type/format/path-version variants, non-REST surfaces such as GraphQL/WebSocket/gRPC, and second-order/blind actions. These remain leads until an owned two-account/object matrix proves an unauthorized read/write/action.

## Deferred / noisy

- `https://bugbountydaily.com`: fetched as SPA/import-map/bootstrap text, not extractable vulnerability methodology.
- `https://github.com/uphiago/recon-skills/`: repository overview page only; previous targeted user-source review already handled this source family. Needs per-file review before class-level promotion.
- `https://blocksec.com/blog/trace-ai-track-stolen-crypto`: product/feature post about stolen-crypto tracing; useful watchlist item, but no new Web3 vulnerability proof-system or reportability gate.
- AppSec.fyi topic/listing records and skipped/deferred linked resources: discovery only until concrete deep pages are fetched.

## Files promoted

- `02 - Vulnerability Playbooks/Web2/Access Control/test-checklist.md`
- `02 - Vulnerability Playbooks/Web2/Access Control/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Access Control/false-positives.md`
- `06 - Evals/Web2/access-control-variant-surface-eval-scenarios.md`
- `07 - Skill Changelog/2026-07.md`
