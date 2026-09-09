---
type: learning-source-summary
status: reviewed-and-partially-promoted
created: "2026-08-11"
domain: web2
source: "https://lostsec.medium.com/"
run_id: "manual-lostsec-learning-20260811"
finding_status: "0/10 target-specific findings; learning only"
article_access: "locked previews only"
---

# LostSec Medium — ten-writeup learning pass

## Scope and acquisition

Reviewed the ten newest entries exposed by LostSec's Medium RSS feed as **Zone 0 learning material**. No target was tested and no vulnerability report was produced.

The public profile HTML was blocked to the remote browser, but the direct RSS feed and profile sitemap were accessible. A bounded local Chrome acquisition successfully loaded all ten canonical InfoSec Writeups pages. Medium marked every post `isLockedPreviewOnly=true`; only 1,293–1,438 article-preview characters were available per post. The 2,563–2,693 characters seen by the corrected browser extractor include visible page chrome plus the preview—not the full article.

This access boundary matters: article-specific payloads, tool flags, exploit chains, and conclusions hidden behind the paywall were **not reviewed and were not promoted**. The run preserves rendered HTML, visible DOM text, clean article previews, sanitized response headers, SHA-256 hashes, and primary-source snapshots under:

`01 - Learning/Inbox/manual-lostsec-learning-20260811/`

## Source disposition

| Writeup | Route | Decision |
|---|---|---|
| [Finding & Exploiting Exposed Google API Keys](https://infosecwriteups.com/finding-exploiting-exposed-google-api-keys-for-bug-bounties-5ce6685a4927) | Secret Exposure | Promote the credential-capability-drift class and safe proof gates; not the locked article's testing steps. |
| [A Practical Workflow for Fuzzing and Scanning](https://infosecwriteups.com/a-practical-workflow-for-fuzzing-and-scanning-in-bug-bounty-64fa00ded29b) | Source-First Mapping | Hold the scanner pipeline. Argus remains JS/source-first; scanners are bounded confirmation/map generators, never mainline endpoint guessing. |
| [Hacking Microsoft IIS](https://infosecwriteups.com/hacking-microsoft-iis-from-recon-to-advanced-fuzzing-013989524fe2) | REST API / source-first | Hold. The preview names IIS 8.3/tilde concepts but does not expose enough method/evidence detail to promote operational steps. |
| [Mastering SQLMap and Ghauri](https://infosecwriteups.com/mastering-sqlmap-and-ghauri-a-practical-guide-to-waf-bypass-techniques-1aaa9eee9d32) | REST API / controlled payload corpus | Hold payloads and bypass steps. Preserve only the existing differential-confirmation rule: a tool/WAF anomaly is not SQLi proof. |
| [Monitor Targets Using Certificate Transparency Logs](https://infosecwriteups.com/monitor-bug-bounty-targets-in-real-time-using-certificate-transparency-logs-247caa34d0f9) | Source-First Mapping | Promote CT as a passive, scope-gated delta sensor that feeds source-first mapping. |
| [Hunting React2Shell CVE-2025-55182](https://infosecwriteups.com/from-recon-to-rce-hunting-react2shell-cve-2025-55182-for-bug-bounties-4e3a3ed79876) | Source-first dependency/CVE review | Hold as CVE-specific intelligence. Require affected package, exact version, React Server Components support, reachable path, and safe causal evidence. |
| [Authentication and Session Management Vulnerabilities](https://infosecwriteups.com/a-practical-guide-to-authentication-and-session-management-vulnerabilities-517f5412a02a) | Authentication & Session | Existing playbook already covers session rotation/invalidation, MFA/recovery, expiry, cookie policy, and actor controls; no new procedure promoted from the preview. |
| [Mass Assignment in Registration Flows](https://infosecwriteups.com/uncovering-invisible-privileges-the-ultimate-guide-to-mass-assignment-in-registration-flows-9ecd5ff40512) | REST API / Business Logic | Promote field-level authorization, DTO/allowlist, persistence/readback, and one-field owned controls. |
| [Hunting Bugs in User Registration](https://infosecwriteups.com/a-comprehensive-guide-to-hunting-bugs-in-user-registration-fe8b04dc39b8) | Authentication, Business Logic, Rate Limits | Route duplicate identity, verification, overwrite, race, parser, and rate-limit leads to existing playbooks. No locked article details promoted. |
| [Spring Boot Actuator Endpoints](https://infosecwriteups.com/actuator-unleashed-a-guide-to-finding-and-exploiting-spring-boot-actuator-endpoints-29252dcd9d79) | Secret Exposure | Promote management-endpoint configuration, false-positive, evidence, stop, and remediation gates from official Spring documentation plus RAG—not locked exploit steps. |

## Preview.is cross-check

| Topic | Best retrieved match | Score | Use |
|---|---|---:|---|
| Google API-key scope drift | [Truffle Security](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules) | 0.9986 | Strong exact-class corroboration; qualified by Google primary documentation. |
| Scanner/fuzzer workflow | Brzozowski automation retrospective (retrieved snapshot; source now returns `404`) | 0.9138 | Moderate practitioner material only; Argus source-first policy controls. |
| IIS 8.3/tilde enumeration | PT SWARM ASP.NET disclosure research (retrieved snapshot; current TLS chain is invalid) | 0.9818 | Relevant class material; no operational promotion from the locked preview. |
| SQLi/WAF bypass | [Vaadata WAF-bypass case study](https://www.vaadata.com/en/blog/exploiting-an-sql-injection-with-waf-bypass/) | 0.9891 | Confirms parser/differential class only; no payload promotion. |
| CT monitoring | [OWASP Subdomain Takeover Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Subdomain_Takeover_Prevention_Cheat_Sheet.html) | 0.9479 | Useful for ownership and dangling-resource false-positive gates; RFC 9162 is normative. |
| React2Shell | [StepSecurity analysis](https://www.stepsecurity.io/blog/critical-remote-code-execution-vulnerabilities-discovered-in-react-server-components-and-next-js) | 0.9975 | Corroborated only after the official React advisory established affected/fixed versions. |
| Session invalidation | [OnSecurity session-management review](https://onsecurity.io/article/session-management-vulnerabilities-what-developers-get-wrong-and-how-to-fix-them/) | 0.9770 | Class-level corroboration; existing Argus and OWASP session gates control. |
| Mass assignment | Redbot Security (retrieved snapshot; source now returns `404`) | 0.9981 | Exact-class corroboration; OWASP is the primary remediation source. |
| Registration edge cases | [django-allauth configuration](https://docs.allauth.org/en/dev/account/configuration.html) | 0.9763 | Narrow framework configuration; no universal registration claim promoted. |
| Spring Actuator | [Spring Boot official documentation](https://docs.spring.io/spring-boot/reference/actuator/endpoints.html) | 0.9761 | Primary exact-class source and promotion basis. |

Saved RAG runs: `manual-preview-is-20260811-112223`, `112229`, `112234`, `112241`, `112335`, `112342`, `112351`, `112358`, `112531`, and `112629`.

## Confirmed durable lessons

### API-key capability drift

Google's primary documentation says publicly exposed API keys can cause unauthorized data access or charges, recommends application and API restrictions, and recommends rotation/deletion of unneeded keys. The durable hunting rule is to model an API key as a mutable capability, not a permanent “public identifier.” Keep key existence, liveness, application restrictions, API restrictions, billable use, and data/admin access as separate claims. Never consume quota or private data to bridge an evidence gap.

Primary sources:

- https://docs.cloud.google.com/docs/authentication/api-keys-best-practices
- https://docs.cloud.google.com/api-keys/docs/add-restrictions-api-keys

### CT is a lead, not scope proof

RFC 9162 establishes CT as public certificate-transparency infrastructure. A newly logged SAN can improve recency and asset prioritization, but it does not prove ownership, program scope, DNS liveness, or deploy time. After explicit scope validation, perform a minimal baseline and then collect only referenced HTML/JS/config/maps for source-first mapping.

Primary source: https://www.rfc-editor.org/rfc/rfc9162.html

### Mass assignment is field-level authorization

OWASP recommends bindable-field allowlists and DTOs rather than direct binding to domain objects. For bounty proof, one extra property must be separated into accepted, echoed, persisted, and capability-changing states. Use an owned object, one source-derived field, fresh readback, a causal negative control, and cleanup.

Primary source: https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html

### Management endpoint impact is configuration-specific

Spring Boot documents that only `health` is exposed over HTTP/JMX by default and warns that endpoints may contain sensitive information. A banner, `/actuator` path, or basic health response is not RCE. Prove the exact exposed endpoint and smallest unauthorized data/action; do not bulk-download heap/log data or invoke state-changing operations live without explicit approval.

Primary source: https://docs.spring.io/spring-boot/reference/actuator/endpoints.html

### React2Shell applicability is prerequisite-bound

The official React advisory says CVE-2025-55182 affects `react-server-dom-webpack`, `react-server-dom-parcel`, and `react-server-dom-turbopack` versions 19.0, 19.1.0, 19.1.1, and 19.2.0, fixed in 19.0.1, 19.1.2, and 19.2.1. It also says apps not using React Server Components are not affected. Version/banner matching alone is therefore not an RCE finding.

Primary source: https://react.dev/blog/2025/12/03/critical-security-vulnerability-in-react-server-components

## Held or rejected

- No scanner-first or endpoint-guessing workflow displaced mandatory JS/source-first mapping.
- No IIS, SQLi/WAF, React2Shell, registration, or Actuator payload/exploit steps were promoted from locked previews.
- No tool success, response anomaly, framework fingerprint, public key string, default health endpoint, or CVE match was treated as impact.
- No article-specific claim hidden behind the paywall was reconstructed from unrelated sources and attributed to LostSec.
- This session produced **0 target-specific findings**.

## Browser-learning quality correction

The first browser pass counted serialized JSON inside `<script>` nodes as page text and incorrectly labeled the locked previews substantive. A TDD regression reproduced this with script/style/template/hidden content. `browser_runtime.extract_bounded_page()` now excludes script, style, noscript, template, SVG, hidden, inert, `aria-hidden`, and inline `display:none`/hidden-visibility ancestors while retaining the text-node scan bound. The corrected LostSec pass reports all ten pages as `index_or_listing` with 2,563–2,693 visible characters.

## Promoted artifacts

- `02 - Vulnerability Playbooks/Web2/Source-First Mapping/overview.md`
- `02 - Vulnerability Playbooks/Web2/Secret Exposure/overview.md`
- `02 - Vulnerability Playbooks/Web2/Secret Exposure/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Secret Exposure/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/Secret Exposure/reportability.md`
- `02 - Vulnerability Playbooks/Web2/Business Logic/overview.md`
- `02 - Vulnerability Playbooks/Web2/Business Logic/test-checklist.md`
- `00 - System/web2-skill-index.md`
- `06 - Evals/Web2/lostsec-preview-durable-gates-20260811-eval-scenarios.md` (24 scenarios)
- `11 - Scripts/learning/browser_runtime.py` and `tests/test_browser_runtime.py`

The source remains a useful **manual learning source**, but this one-time request did not mutate the recurring source registry. A future pass needs legitimate full-text access or author-shared free links before importing article-specific procedures.
