# Learning ingest: deep content over index metadata (2026-06)

## Trigger

During the 2026-06-30 learning-ingest review, the user corrected the workflow: the ingest was producing too much listing/index/source-root metadata and not enough actual learning material. Future runs should fetch and classify substantive content pages, not just enumerate sources.

## Durable lesson

A learning ingestion run is only useful if it distinguishes:

- **actual content** — article/advisory/report/docs page with substantial extractable text and a concrete technique, exploit path, reportability lesson, or remediation pattern;
- **index/topic/listing metadata** — topic pages, homepage feeds, report lists, GitHub org/repo landing pages, all-topics pages;
- **deferred candidates** — promising deep links discovered from indexes but not fetched because of caps/robots/budget.

Index pages are useful for discovery, but compiler output must not treat them as lessons unless they produce deep linked resources.

## What changed in the workflow

Patch pattern applied to the learning ingest:

1. Keep `run_learning_ingest.sh` as a small wrapper and move the actual implementation to `11 - Scripts/learning/learning_ingest.py` so the parser/fetcher can be tested with `python3 -m py_compile`.
2. Extract body text from semantic/content-bearing tags (`article`, `main`, `section`, `p`, `li`, headings, `pre`, `code`, tables, blockquotes), not only title/meta description.
3. Add per-record fields:
   - `content_excerpt`
   - `content_char_count`
   - `content_quality`
   - `page_kind`
4. Split statuses:
   - `fetched_content`
   - `fetched_index_metadata`
   - `fetched_metadata`
5. Add content-quality counts to the run summary.
6. Score linked resources before fetching. Prefer concrete advisories, CVEs/GHSAs, writeups, docs, reports, dated blog posts, Rekt postmortems, and vulnerability-specific pages over homepages, product pages, policies, lists, social/share links, PDFs, and broad tools.
7. For AppSec.fyi root discovery, prioritize high-yield security topics before alphabetical generic pages:
   - IDOR/BOLA/AuthZ
   - API security
   - AuthN/OAuth/JWT
   - file upload/storage/secrets
   - SSRF/GraphQL/XSS/CSRF/deserialization/RCE
8. Split daily mode from one-time/backfill mode:
   - daily cron skips `cadence: one_time_full` core roots such as HackTricks, PortSwigger all-topics, OWASP, Solidity docs, etc.;
   - full/backfill runs opt in with `ARGUS_INCLUDE_BACKFILL=1`.
9. For continuous-monitoring roots, treat the root/listing as discovery only and fetch top ranked deep links into `source_group=daily_deep_content`.
## Current source split

Daily/continuous cron sources include medium-priority feeds (`ARGUS_PRIORITY_ONLY=0`) and should remain focused on fresh/current posts, reports, advisories, and postmortems:

- AppSec.fyi root/topic pages as discovery only; compile only fetched linked resources.
- Web2 continuous sources: Bug Bounty Daily (high-priority daily), Critical Thinking Podcast Notes, Intigriti Hacking Tools Blog, YesWeHack Learn Bug Bounty, HackerOne Hacktivity, Google Project Zero, PortSwigger Research, Embrace The Red Blog, Simon Willison Blog.
- Web3 continuous sources: Rekt, Immunefi Blog/Research, Solodit, Code4rena, Sherlock, Cantina, ChainSecurity, BlockSec, Paradigm.

One-time/backfill sources are heavyweight reference corpora and should not run in daily cron:

- Web2: HackTricks, PortSwigger Web Security Academy all topics, OWASP GitHub/WSTG/ASVS/API Security/Cheat Sheets, Arcanum Security Arc PI Taxonomy.
- Web3: Solidity docs/security considerations, OWASP SCSVS/Smart Contract Security, Immunefi Learn/Severity Classification, Trail of Bits, OpenZeppelin, Damn Vulnerable DeFi.

## Verification signal

A healthy bounded run should show non-trivial `fetched_content` records and examples of actual pages, such as:

- MDN or PortSwigger article/docs pages
- GitHub/GitLab security advisories
- concrete CVE/GHSA reports
- specific vulnerability writeups
- individual audit/postmortem reports

A run with mostly `fetched_index_metadata` and very few `fetched_content` records is not meeting the user's intent.

## Suggested cron/runtime knobs

When tuning the daily cron, prefer giving enough budget to fetch actual linked resources while keeping caps bounded:

```text
ARGUS_PRIORITY_ONLY=0
ARGUS_MIN_CONTENT_CHARS=1200
ARGUS_MAX_TOTAL_SECONDS=420
ARGUS_MAX_SOURCES_PER_GROUP=20
ARGUS_MAX_APPSEC_LINK_FETCHES=25
ARGUS_MAX_APPSEC_LINK_RECORDS=80
ARGUS_MAX_DAILY_DEEP_LINK_FETCHES=35
ARGUS_MAX_DEEP_LINKS_PER_SOURCE=5
ARGUS_REFETCH_SEEN_AFTER_DAYS=30
```

Use the dedicated one-time/backfill runner for heavyweight reference sources:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_learning_backfill_once.sh"
```

The backfill runner is a bounded same-site crawl/scrape, not a single URL fetch. It uses:

```text
ARGUS_INCLUDE_BACKFILL=1
ARGUS_MAX_TOTAL_SECONDS=1800
ARGUS_MAX_BACKFILL_DEEP_LINK_FETCHES=300
ARGUS_MAX_BACKFILL_LINKS_PER_SOURCE=75
ARGUS_MAX_BACKFILL_CRAWL_DEPTH=4
ARGUS_MAX_APPSEC_LINK_FETCHES=0
ARGUS_MAX_APPSEC_LINK_RECORDS=0
ARGUS_RUN_LABEL=backfill-YYYYMMDD-HHMMSS
```

Backfill runs must write to a unique inbox label (via `ARGUS_RUN_LABEL`) rather than the date-only daily inbox, otherwise a dry run/backfill can overwrite the day's `learning-candidates.jsonl` and compiler outputs.

Do not make either run a noisy dump. The goal is fewer, higher-quality deep resources.

Daily runs should be incremental. The ingest maintains URL/content seen-state at `~/.config/argus/learning-seen-urls.json`; daily deep links already seen are skipped as `skipped_seen_url` until `ARGUS_REFETCH_SEEN_AFTER_DAYS` elapses. This keeps daily learning focused on new articles/resources while still allowing periodic refetch for changed content.

## Compiler guidance

Automated compiler command:

```bash
python3 "$HOME/SecurityResearch/11 - Scripts/learning/compile_learning_inbox.py"
```

Or for a specific inbox:

```bash
python3 "$HOME/SecurityResearch/11 - Scripts/learning/compile_learning_inbox.py" "$HOME/SecurityResearch/01 - Learning/Inbox/YYYY-MM-DD"
```

The compiler writes:

- source summaries under `01 - Learning/Source Summaries/YYYY-MM-DD/`
- patch proposals under `01 - Learning/Skill Patch Proposals/YYYY-MM-DD-compiler-proposals.md`
- discovery/skipped audit under `01 - Learning/Rejected Lessons/YYYY-MM-DD-discovery-only-and-skipped.md`
- eval proposals under `06 - Evals/Learning Proposals/YYYY-MM-DD-compiler-eval-proposals.md`
- run report under `01 - Learning/Inbox/YYYY-MM-DD/learning-compiler-run.md`

When compiling an inbox:

1. Prefer `local_processing_status=fetched_content` and `content_quality=actual_content`.
2. Use index/topic/listing pages only to explain discovery context or to choose deep links for the next run.
3. Reject or defer broad source-root records that lack a technique, exploit path, or reportability lesson.
4. For each accepted source, extract:
   - vulnerability class
   - attacker path
   - affected object/actor/tenant boundary
   - proof requirements
   - false-positive/downgrade gate
   - reportability/severity lesson
   - playbook or eval patch proposal
5. Promotion into mature playbooks is review-gated, not wholesale. Prioritize high-signal methodology pages/taxonomies/evals first, and explicitly reject product/commercial/repo-chrome records even if the compiler scored them as text-heavy actual content.

## Pitfall

A run can be successful operationally (`cron ran`, `records written`) but still fail its learning objective if records are dominated by index/listing metadata. Always audit **what was fetched**, not just whether the cron executed.

A backfill crawl can be operationally successful while still including duplicate/noisy pages. Filter multilingual HackTricks mirrors, generic welcome/FAQ pages, product/pricing/login/support pages, PortSwigger product/company/commercial pages, Academy certification/Hall-of-Fame/all-labs pages, and GitHub/OWASP repo chrome (`issues`, `pulls`, `actions`, `activity`, `settings`, `releases`, administrative dotfiles/README/LICENSE/CONTRIBUTING/Makefile) when the intended source is Web Security Academy/OWASP methodology content.

Some daily sources are high-value but low-yield for static fetching because they are browser-rendered, dynamic, or robots-blocked for the script. Mark them `handling: browser_dom_required` and process them with the browser DOM ingest rather than forcing static ingest to bypass robots. Current examples: Solodit, HackerOne Hacktivity, Cantina ended opportunities, Immunefi Research, BlockSec Blog, Paradigm Writing, Code4rena Reports, Sherlock Audits, and ChainSecurity Blog.

For browser DOM ingestion, treat configured roots as discovery/index pages and compile only linked content. Filter source-specific noise aggressively: Immunefi customer/listing pages, BlockSec compliance/VASP/business posts, Paradigm fellowship/predictions/general writing pages, Sherlock/Cantina generic listing pages, ChainSecurity generic audit-completed/customer posts, and source roots such as Solodit list pages.

Daily runs should create a lightweight digest after compiler output:

```bash
python3 "$HOME/SecurityResearch/11 - Scripts/learning/create_learning_digest.py" "$HOME/SecurityResearch/01 - Learning/Inbox/<daily-run>"
```

The digest ranks high-signal, watchlist, and likely-noise candidates so promotion review starts from concrete methodology/invariant/evidence changes instead of reading the full proposal file.

Daily orchestrator command:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_daily_learning_ingest.sh"
```

It runs both static daily ingest and browser DOM ingest, combines component outputs into one `daily-*` inbox while preserving component folders for forensics, and compiles the combined inbox into source summaries/proposals by default (`ARGUS_COMPILE_AFTER_INGEST=1`).

One-time/backfill orchestrator command:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_one_time_learning_ingest.sh"
```

It runs only heavyweight reference/backfill sources, writes a `one-time-*` inbox, and compiles that inbox into source summaries/proposals by default. Do not schedule one-time/backfill with daily cron.

Low-level browser DOM ingest remains available:

```bash
bash "$HOME/SecurityResearch/11 - Scripts/learning/run_browser_dom_ingest.sh"
```

This writes a normal `browser-dom-*` inbox with `browser_fetched_content` records. The compiler accepts both `fetched_content` and `browser_fetched_content` when `content_quality=actual_content`. Static daily ingest should record `browser_dom_required` sources as manual/browser-required rather than producing misleading low-yield static output.
