---
type: source-summary
run: daily-20260730-073001
reviewed: "2026-07-30"
promotion: "Web2 Access Control derived-representation authorization parity"
---

# Daily 2026-07-30 — derived-representation authorization promotion

## Run quality

- Manually reviewed all **5 actual-content records** from **217 canonical combined records** (**2.3%** actual content).
- The run remained discovery-heavy: **72 index/listing records**, **132 not-fetched records**, and 8 metadata/thin/source-native-required/other records.
- Static ingestion supplied 2 actual-content records; browser-DOM ingestion supplied 5, including the two source-native disclosed reports that materially enabled review.

## Manual dispositions

1. **Bug Bounty Daily** — rejected as CSS/import-map/base64 application bootstrap. MCP/model dependency strings caused an unsupported AI/LLM classification; no vulnerability methodology was extracted.
2. **WordPress official release feed** — no promotion. WordPress 7.1 Beta 4 supplied beta-testing and maintenance context, while the 7.0.2 security material is already promoted in the WordPress CVE Intelligence playbook.
3. **Rocket.Chat report #3473145** — retained as source-native corroboration of the DNS-rebinding SSRF lesson promoted on 2026-07-29. Its validate-then-fetch split and DNS-change proof add no gate beyond the existing exact-product-path, actual-peer, every-answer, redirect, safe-impact, and address-pinning requirements.
4. **HackerOne report #3577216** — promoted narrowly. The canonical report view applied disclosure/visibility policy, while `exportReportPdf` selected underlying timeline activity without repeating per-activity authorization. This is a reusable derived-representation projection failure rather than a PDF-specific flaw.
5. **BlockSec crypto-address risk screening** — rejected as product/compliance guidance outside the vulnerability-methodology lane; the compiler's AI/LLM classification was unsupported.

## Promoted lesson

Model every representation as an independent authorization projection:

```text
requester + role + tenant + object
→ source records
→ per-record/per-field visibility policy
→ template/serializer or async job
→ stored artifact
→ retrieval authorization
→ requester-visible bytes
```

Authorization to view the parent object, invoke an export mutation, or download the generated file does not prove that each embedded row and field was selected under the same requester-aware policy. Safe evidence needs owned allowed/restricted canaries, the same lower-role requester and object through canonical and derived paths, the actual parsed artifact, a higher-role positive control, and stale/share/revocation controls. An accepted job, page-count difference, or artifact URL alone is not proof.

Severity follows the sensitivity and breadth of the restricted content and the actor's prerequisites—not the output format. Remediation should centralize requester-aware query/projection policy before serialization and verify parity across interactive, API, GraphQL, PDF/CSV, email/notification, timeline/audit, search/index, cache, and generated-download paths.

## External reference check

- [HackerOne report #3577216](https://hackerone.com/reports/3577216) is the source-native basis for the per-activity export projection failure.
- [SentinelOne — What Is Insecure Direct Object Reference?](https://www.sentinelone.com/cybersecurity-101/cybersecurity/insecure-direct-object-reference/), Preview.is score `0.9135`, independently identifies downloads, exports, and report endpoints as frequently missed object-authorization surfaces. This is Zone 0 corroboration, not target evidence.
- The SSRF Preview.is wrapper returned HTTP 500; one direct API retry returned five matches. [StackShield's DNS-rebinding guidance](https://stackshield.io/blog/laravel-ssrf-http-client-vulnerability), score `0.9932`, repeated the validation-to-fetch re-resolution and address-pinning lesson already promoted on 2026-07-29, so no second SSRF patch was made.
- The export retrieval also returned generic PDF documentation and unrelated release material; those matches were rejected.

## Compiler correction and boundaries

The generated summaries/proposals used boilerplate actor/object language and misclassified Bug Bounty Daily, WordPress release material, the Rocket.Chat SSRF report, and BlockSec risk screening. They were superseded rather than promoted. No live target, Google, authorized program, broad crawl, or backfill activity occurred.
