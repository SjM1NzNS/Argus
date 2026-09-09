# Daily learning digest and review-gated promotion — 2026-07

Session-specific reference for the Argus learning cron improvements.

## Daily pipeline shape

The daily orchestrator should now behave as:

```text
static daily ingest
→ browser DOM ingest
→ combined daily inbox
→ compiler outputs
→ daily learning digest
→ review-gated promotion
```

Key script paths:

- `11 - Scripts/learning/run_daily_learning_ingest.sh`
- `11 - Scripts/learning/browser_dom_ingest.py`
- `11 - Scripts/learning/compile_learning_inbox.py`
- `11 - Scripts/learning/create_learning_digest.py`

The digest is a review aid, not an automatic promotion mechanism.

## Browser DOM filtering lessons

Dynamic/security-report sources are useful but noisy. Treat browser DOM roots and listing pages as discovery surfaces unless a concrete report/post/writeup is extracted.

Useful generic browser DOM noise terms:

- customers
- compliance
- fellowship
- predictions
- VASP/regulatory/business posts
- contest/opportunities root pages
- generic partner/customer/news pages

Source-specific examples:

- Immunefi: filter/deprioritize customers/listing/bug-bounty roots.
- BlockSec: filter compliance, VASP, regulatory, business/partner posts.
- Paradigm: filter fellowship, predictions, generic writing roots.
- Sherlock/Cantina: listing roots are discovery only; prefer concrete reports/competitions with extractable vuln detail.
- Solodit roots: discovery only.

## Digest classification

A daily digest should divide compiled actual-content records into:

- high-signal promotion candidates;
- watchlist/context-only items;
- likely noise/defer items.

Good high-signal indicators:

- exploit/writeup/report/postmortem with attacker path;
- evidence requirement or false-positive lesson;
- concrete invariant or reportability gate;
- source-derived endpoint or object-boundary lesson;
- reproducible safe test idea.

Defer if the item is mainly commercial, compliance, generic listing/index, broad trend commentary, or source-root content.

## Promotion discipline

Do not promote compiler proposals wholesale. For each candidate:

1. Read the source summary/digest entry.
2. Route to the existing mature playbook/eval.
3. Promote only concrete methodology/evidence/false-positive/reportability lessons.
4. Add eval coverage if the lesson changes triage decisions.
5. Add changelog and promotion-review note.
6. Verify no TODO/TBD markers were introduced.

Examples promoted from the daily digest:

- Node.js/HackerOne TOCTOU → Race Conditions playbook and eval.
- Prompt injection as role confusion → AI & LLM Security false-positive gates.
- Gravity Bridge denom/address mapping → Bridge invariants and eval.
- OOXML/container parser checks → File Upload parser lifecycle checklist.
- Based Loans oracle/config lookup failure → Web3 oracle attack patterns.
