---
type: source-summary
status: reviewed
created: "2026-08-08"
run: manual-user-security-articles-20260808
promotion: "MFA assurance states, native stream-parser bounds, and HDF5/libvips external-reference file reads"
---

# Manual user-source review — authentication, Ruby Prism, and avatar processing

## Run audit

- User-supplied articles: **3**.
- Static captures: **3/3 HTTP 200**, all classified as substantive `actual_content`.
- Full raw HTML, offline text, headers, hashes, and upstream Ruby PR metadata/patch were preserved.
- Promotion decision: three narrow class-level updates; no article payload, secret, token, real-customer access step, or live crash procedure was promoted.
- Persistent monitoring configuration was not changed. The Intigriti parent blog is already monitored; the two independent sources remain one-time user-supplied captures.

## 1. Intigriti — insecure 2FA implementations

Source: https://www.intigriti.com/researchers/blog/hacking-tools/broken-authentication-7-advanced-ways-of-bypassing-insecure-2-fa-implementations

Author: blackbird-eu. Article date: 2024-12-07; page reported last updated 2026-08-08.

**Standalone source quality: approximately 4/10.** It is useful as a generic checklist/eval seed, but provides no accepted report, full request/response evidence, primary-standard citations, or triage outcome, and the captured traversal code/diagrams are placeholders. It is not report evidence. Promotion below relies on stronger class-level corroboration and Argus evidence gates.

**Promoted narrowly:** model MFA as a server-side assurance state machine. Test pre-MFA/provisional sessions against protected endpoints; bind factor artifacts to account, session, purpose, and attempt; cover replay/expiry, alternate login/API/mobile/OAuth paths, backup/recovery and remembered-device state, password reset, and MFA enrollment/disable. Internal verifiers must bind success to the expected challenge/account rather than trusting a generic status.

**Safety/evidence gates:** one owned account by default; exactly two owned accounts only for an explicit binding swap; low-volume negative controls; no OTP brute force, resends, push fatigue, lockouts, or live races. A dashboard shell, redirect bypass, client flag, or changed response is not proof unless a protected server-side capability is granted.

**Not promoted:** the article's literal common-code guesses, traversal string, broad “try all payloads” advice, or any high-volume automation.

The internal-verifier/path-normalization case is retained only as a synthetic contract-test pattern: a fixed verifier route must return an explicit account/challenge-bound result. It is not a target lead or reusable traversal payload without source-derived reachability and an end-to-end assurance upgrade.

Preview.is returned strong corroboration:

- `0.9611` — https://portswigger.net/web-security/race-conditions — transient pre-MFA sub-state model.
- `0.9577` — https://www.hackerone.com/blog/how-inadequate-authentication-logic-led-mfa-bypass-and-account-takeover — active session issued before factor completion and client-cookie-only gating.

These are Zone 0 methodology sources, not proof about a current target.

## 2. Cantina — Ruby Prism stream-boundary overflow

Source: https://www.cantina.security/blog/one-emoji-is-enough-to-crash-ruby

Article date: 2026-08-04.

**Promoted narrowly:** a nominal read limit is not necessarily a hard post-transformation byte bound. Encoding-aware reads can extend to complete a character; the destination must reserve worst-case headroom, validate returned types, clamp the actual copy length, reserve termination space, and test boundary-adjacent cases. File, in-memory string, and stream/`stdin` parser paths must be treated independently.

The article reports a stack overflow in Prism's Ruby stream bridge and gives affected Ruby ranges. Upstream ruby/prism PR #4172 independently confirms the contract/root-cause and complete fix pattern; it was merged as `70147e5b449eac2e5c0ef614db6ee89ea9288cb3`. The reviewed upstream metadata does **not** map the fix to Ruby maintenance releases, so the playbook requires commit/backport or authoritative release-advisory evidence rather than inventing a patched version. No CVE identifier was observed.

**Safety/evidence gates:** local, maintainer-owned, or explicitly approved sanitizer harness only; exact crash input stays in quarantined raw source; package presence and a local crash do not prove remote reachability, meaningful denial of service, RCE, or sandbox escape.

Preview.is returned the Cantina article itself at `0.9955`; the lower-ranked results were unrelated Ruby/Rack advisories and were rejected as corroboration. Upstream PR #4172 is the primary independent fix source.

## 3. Abdelmounaim — Leaky Avatar

Source: https://abdelmounaim.xyz/posts/leaky-avatar/

Article date: 2026-07-18.

**Promoted narrowly:** libvips-backed “image” paths may expose non-image loaders selected by detected content. The article describes `matload` processing MATLAB v7.3/HDF5 content whose external-storage reference is read by the worker and transformed into output pixels. This adds a concrete external-reference route to the existing CVE-2026-66066 loader/saver/delegate model.

**Applicability gates:** deployed libvips/HDF5 versions; `matload` compiled and effectively enabled; untrusted arbitrary-byte upload; actual analyzer/transform reachability; worker filesystem namespace/readability; external-reference resolution; and decoded output matching an inert dedicated server-side canary. A changed multipart MIME, accepted upload, error banner, or package presence is not file-read proof.

**Safety/evidence gates:** validate only with a researcher-owned canary in a local/owned or explicitly approved worker. Never substitute process environment, service-account tokens, cloud credentials, database/source-control secrets, or customer data. Stop at the canary and route any source-backed secret/capability hypothesis through the secret-validation policy and explicit approval.

**Not promoted:** the article's generator, sensitive paths, token acquisition, role assumption, cloud credential minting, object listing, customer-data access, or implied permission/reportability. Those remain unverified author claims and unsafe transfer material.

Preview.is returned strong primary class corroboration:

- `0.9976` — https://discuss.rubyonrails.org/t/cve-2026-66066-possible-arbitrary-file-read-and-remote-code-execution-in-active-storage-variant-processing/91432
- `0.9953` — https://github.com/rails/rails/security/advisories/GHSA-xr9x-r78c-5hrm

The Rails sources corroborate arbitrary file read through unsafe libvips operations and the blocking/rotation remediation model; the exact HDF5 external-storage mechanism comes from the reviewed article.

## Promoted artifacts

- `02 - Vulnerability Playbooks/Web2/Authentication & Session/{overview,test-checklist,false-positives,evidence-requirements}.md`
- `02 - Vulnerability Playbooks/Web2/Native Parser & Streaming Interfaces/{overview,test-checklist,false-positives,evidence-requirements}.md`
- `02 - Vulnerability Playbooks/Web2/File Upload/{overview,test-checklist,false-positives,evidence-requirements}.md`
- `02 - Vulnerability Playbooks/Web2/Attack Chains/overview.md`
- `00 - System/web2-skill-index.md`
- `06 - Evals/Web2/authentication-mfa-assurance-state-eval-scenarios.md`
- `06 - Evals/Web2/native-parser-streaming-boundary-eval-scenarios.md`
- `06 - Evals/Web2/file-upload-rails-libvips-untrusted-operations-eval-scenarios.md`

## Validation

- Local deterministic validator: **PASS** — 19 promoted/ledger files checked; YAML-frontmatter closure, code-fence balance, router entries, eval numbering, and stray patch markers clean.
- Capture integrity: **PASS** — 8 raw/upstream artifacts match the SHA-256 values in the acquisition manifest.
- Seen-state: **PASS** — 3 canonical URLs match ingest content hashes and lengths in `$HOME/.config/argus/learning-seen-urls.json`.
- Quarantine guard: **PASS** — checked promoted files contain none of the article's exact sensitive-path, generator, cloud-auth, or role-assumption strings.
- External links: **PASS** — all 8 cited article, upstream PR, PortSwigger/HackerOne, and Rails advisory URLs resolved with HTTP `200` on 2026-08-08.
- Promotion ledger: this reviewed source summary is the established learning-promotion record; no separate vault-wide changelog exists outside unrelated target dependencies.

## Scope and non-actions

No Google/authorized program target interaction, account login, OTP request, upload, parser execution, crash test, generator retrieval, secret access, cloud authentication, customer-data access, broad crawl, or persistent feed addition occurred. Preview.is was used only for exact target-independent technique corroboration under the external-RAG policy.
