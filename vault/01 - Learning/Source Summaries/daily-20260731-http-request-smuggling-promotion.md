---
type: source-summary
status: reviewed
created: "2026-07-31"
run: daily-20260731-073001
promotion: HTTP request smuggling / desynchronization
---

# Daily lightweight review — HTTP request smuggling promotion

## Run audit

- Combined records: **148**.
- Actual-content records selected by the compiler: **26** (**17.6%**).
- Other quality labels: 27 index/listing, 2 metadata-only, 42 not-fetched, 2 source-native-required, 1 unchanged, 48 unknown.
- Static lane: 5 records, all `not_fetched` (`robots_blocked` or fetch error).
- Browser-DOM lane: 5 records, all index/listing discovery pages.
- Promotion decision: **one** concise class-level promotion; compiler boilerplate was not copied.

## Promoted lesson

The YesWeHack HTTP request-smuggling guide exposed a missing Argus class. Preview.is returned strong on-topic corroboration: PortSwigger's desync research (`0.9988`), Fastly's defense analysis (`0.9979`), and an HTTP/2 downgrade walkthrough (`0.9969`). The promoted rule is evidence- and safety-first:

1. Bind the hypothesis to two real HTTP components and their exact framing semantics.
2. Treat a timeout, status code, scanner label, or accepted ambiguous header as a lead only.
3. Prefer a direction-specific non-poisoning discriminator; run second-message proof only in local/owned/owner-coordinated lanes.
4. Require exact wire bytes, connection reuse/order, backend parser evidence, unique owned canaries, and fresh-connection/patched controls.
5. Separate parser differential from impact; severity follows the proven unauthorized data/action/cache/routing consequence.

Sources:

- https://www.yeswehack.com/learn-bug-bounty/http-request-smuggling-guide-vulnerabilities
- https://portswigger.net/blog/http-desync-attacks-request-smuggling-reborn
- https://www.fastly.com/blog/demystifying-fastlys-defense-against-http-desynchronization-attacks
- https://outpost24.com/blog/request-smuggling-http-2-downgrading/

## Manual disposition of every actual-content record

| # | Record | Disposition |
|---:|---|---|
| 1 | Bug Bounty Daily | Reject: Next.js/import-map/bootstrap shell, not learning content. |
| 2 | CTBBP episode 1 | Defer: first 6,000 stored characters are site-wide episode navigation, so the episode body was not reviewable from the retained excerpt. |
| 3 | CTBBP episode 10 | Defer: same navigation-dominated excerpt issue. |
| 4 | CTBBP episode 102 | Defer: same excerpt issue; generic micro-agent topic already covered by autonomous-hackbot methodology. |
| 5 | CTBBP episode 108 | Defer: same excerpt issue; SaaS-specific claims were not recoverable from the retained record. |
| 6 | CTBBP episode 111 | Defer: same excerpt issue; no DOMPurify bypass detail was promoted. |
| 7 | Intigriti BugQuest broken access control | Reject as duplicate broad curriculum; existing Access Control matrices are more specific. |
| 8 | Intigriti broken access-control guide | Reject as duplicate class overview. |
| 9 | Intigriti business-logic guide | Reject as duplicate broad methodology; no new invariant/evidence gate. |
| 10 | YesWeHack HTTP request smuggling guide | **Promote:** missing class-level routing plus safe differential/evidence/impact gates. |
| 11 | YesWeHack LLM/agentic CLI/MCP guide | Reject as duplicate tooling guidance; existing Argus orchestration and MCP gates are stricter. |
| 12 | YesWeHack Claude Code blind-lab article | Reject as duplicate “discover fast, validate manually” lesson; no raw model output was accepted as proof. |
| 13 | YesWeHack SSTI/cache/business-logic tips | Reject as mixed secondary advice; dedicated SSTI and business-logic playbooks already cover the durable gates. |
| 14 | YesWeHack OS command-injection guide | Watchlist: high-signal class gap, but broad payload-oriented material needs a separate source-backed safety/eval pass rather than a second daily promotion. |
| 15 | Project Zero FORCEDENTRY | Defer: historical, mobile/native exploit engineering; off the lightweight Web2 promotion lane. |
| 16 | Project Zero Android DNG exploit | Defer to a mobile parser/source review; no generic exploit recipe promoted. |
| 17 | Project Zero Windows path-lookup races | Defer to a native/desktop TOCTOU pass; not a web-target evidence update. |
| 18 | Project Zero Pixel Dolby chain | Defer to a mobile media-decoder/sandbox pass. |
| 19 | PortSwigger email parser research | Duplicate: already promoted in the 2026-07-28 OAuth/OIDC email-identity binding pass. |
| 20 | Embrace The Red local developer AI article | Reject as duplicate of existing local-agent capability/confused-deputy and lifecycle gates. |
| 21 | Simon Willison OpenAI/Hugging Face incident commentary | Defer: useful watchlist, but secondary/speculative details require the primary incident disclosures and containment configuration before promotion. |
| 22 | Simon Willison agentic AI archive index | Reject: listing/index page. |
| 23 | `llm` 0.32rc1 release | Reject: release metadata without a security invariant. |
| 24 | HackerOne Rails Vips transformer report #3553340 | Watchlist: concrete untrusted-operation/file-write lead, but requires fixed-diff/current-release provenance and impact-boundary review; existing CVE-2026-66066 processor gates partially overlap. |
| 25 | BlockSec July 2026 newsletter | Reject as secondary digest: governance capture already promoted; oracle/signer-compromise items add incident context but no new executable proof gate today. |
| 26 | WordPress release feed | Reject: release index/listing content, not a specific security lesson. |

## Acquisition-quality note

Five CTBBP records were labeled `actual_content`, but the retained `content_excerpt` contained only the first 6,000 characters and was dominated by a shared episode index. Their full-content hashes differed, so they were not relabeled as duplicate pages; they were excluded because the durable excerpt did not expose reviewable article-specific content. This is an excerpt-selection limitation, not proof that the underlying pages lack content.

## Scope and non-actions

No broad crawl, backfill, Google/authorized program target request, desync probe, payload execution, or third-party interaction was performed. Preview.is material was Zone 0 corroboration only.
