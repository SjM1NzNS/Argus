---
type: source-summary
run: daily-20260729-073001
reviewed: "2026-07-29"
promotion: "Web2 SSRF DNS-resolution and redirect binding"
---

# Daily 2026-07-29 — SSRF DNS-binding promotion

## Run quality

- Manually reviewed all **4 actual-content records** from **217 canonical combined records** (**1.8%** actual content).
- The run remained discovery-heavy: **71 index/listing records**, **132 not-fetched records**, and 10 other metadata/source-native/thin/unchanged records.
- Static ingestion supplied 2 actual-content records; browser-DOM ingestion supplied 2.

## Manual dispositions

1. **Bug Bounty Daily** — rejected as CSS/import-map/base64 application bootstrap. Bundled MCP/model dependencies caused an unsupported AI/LLM classification; the capture contained no reviewed vulnerability methodology.
2. **WordPress official release feed** — no new promotion. WordPress 7.0.2 security material was already promoted, while 7.1 Beta 3 supplied beta-testing and release context rather than a new attacker path, affected revision, evidence gate, or false-positive control.
3. **HackerOne Hacktivity** — manually reviewed as a listing of platform-generated summaries, not source-native reports. Promoted only the target-independent DNS-rebinding SSRF validation-to-connect lesson. The SAML wrapping and Monero log-injection entries were already promoted; JWT algorithm pinning and repository-scoped token authorization are already routed; the trust-store, logging, OAuth redirect, XSS, and other summaries lacked enough source-native mechanics for a new class-level patch.
4. **HackerOne Opportunity Discovery** — rejected as a program directory and commercial opportunity index, not vulnerability methodology.

## Promoted lesson

The durable boundary is:

```text
untrusted URL
→ parse/canonicalize
→ hostname policy
→ CNAME + all A/AAAA answers
→ prohibited-address classification
→ HTTP client/proxy resolution
→ actual connected peer
→ every redirect target
→ response consumer and impact
```

A public answer observed during validation is not enough if the product re-resolves the hostname before connection. Evidence must prove the validation-time accepted address and actual connected destination through the exact product path, with stable-public, blocked-destination, mixed-answer, and redirect controls. DNS mutation alone or a benign public callback does not prove rebinding. Testing should remain source-first or local/owned; target-internal and metadata destinations are separately approval-gated.

Remediation should connect to the exact vetted address while preserving hostname/SNI semantics, fail closed on any prohibited CNAME/A/AAAA result, disable redirects or repeat full validation and binding per hop, and retain network egress controls as defense in depth.

## External reference check

Preview.is retrieval returned five strong matches; selected support:

- [StackShield — SSRF in Laravel: The Http::get() Risk](https://stackshield.io/blog/laravel-ssrf-http-client-vulnerability), score `0.9972`: validation-to-fetch re-resolution and per-redirect checks.
- [Aydin Nyunus — SSRF Vulnerability: Bypassing Protection with DNS Rebinding Attack](https://aydinnyunus.github.io/2026/03/14/ssrf-dns-rebinding-vulnerability/), score `0.9929`: address pinning as a TOCTOU control.
- [Wiz — Server-Side Request Forgery: What It Is & How To Fix It](https://www.wiz.io/academy/application-security/server-side-request-forgery), score `0.9904`: URL normalization, redirect revalidation, address controls, and layered egress defense.

The HackerOne listing and retrieved references are Zone 0 source support, not target evidence or live-testing instructions.

## Watchlist and noisy sources

- Keep the newer Hacktivity summaries on the source-native-detail watchlist; do not infer exact mechanics or severity from platform-generated text.
- AppSec.fyi topics, HackerOne opportunity listings, Web3 contest/report indexes, robots-blocked records, seen URLs, skipped link-budget entries, and metadata-only captures remain discovery material.
- No Google or authorized program target testing, broad crawl, or backfill was performed.
