---
type: learning-source-summary
status: reviewed-and-promoted
created: "2026-07-31"
domain: web2
finding_status: "0/5 target-specific findings; learning only"
---

# Five web-security articles — source verification and promotion summary

## Scope and handling

Reviewed the five user-supplied articles as **Zone 0 learning material**, not as proof or instructions for live-target action. No target was tested and no vulnerability report was produced. Historical CVEs and author demonstrations were decomposed into reusable class-level evidence gates, false-positive checks, and safe lab controls.

The normal collector fetched four sources. The Elementor page was blocked by `robots.txt`; it was reviewed through a browser-derived source note, canonical CVE record, Patchstack advisory, and the official WordPress SVN 3.5.5/3.5.6 frontend source instead.

## Preview.is cross-check

| Topic | Best relevant Preview.is match | Score | Use in promotion |
|---|---|---:|---|
| SSRF + ambient browser cookies | Intigriti CSRF guide | 0.897 | Moderate corroboration for cookie-delivery concepts only. Exact proxy-header-forwarding chain was not retrieved; normative RFC 6265bis and source-specific evidence control. |
| Zimbra memcache injection | SonarSource original article | 0.994 | Strong exact match. Used for response-queue/key-binding and routing-chain hypotheses; canonical CVE/vendor fixes still establish affected status. |
| Elementor CVE-2022-29455 | Results were different/current Elementor XSS issues | 0.9475 / 0.852 | Wrong vulnerability despite high lexical scores. Promoted **no exact claims** from these matches. Used CVE record, Patchstack, and SVN tag diff. |
| Python NaN injection | CISA bulletin describing analogous non-finite comparison bypass; Bishop Fox JSON interoperability | 0.7241 / 0.5743 | Useful class-level corroboration only. Exact Python behavior was checked against Python docs, RFC 8259, upstream demo source, and local reproduction. |
| Safari UXSS chain | Generic UXSS database; unrelated Safari Gatekeeper article | 0.8535 / 0.8019 | No exact chain match. Promoted no details from these results; used Apple/CVE records and the original research article. |

Saved Preview.is records:

- `manual-preview-is-20260731-131551` — SSRF/cookie query
- `manual-preview-is-20260731-131559` — Zimbra/memcache query
- `manual-preview-is-20260731-131609` and `manual-preview-is-20260731-131855` — Elementor queries
- `manual-preview-is-20260731-131831` — NaN query
- `manual-preview-is-20260731-131843` — Safari query

## Claim ledger

### 1. SSRF Vision

**Promoted**

- A browser-visible URL-fetching endpoint can create client-side credential impact when it behaves as a reverse proxy and forwards incoming cookie/authorization headers to an attacker-selected upstream.
- `HttpOnly` prevents script access through non-HTTP APIs; it does not prevent matching HTTP requests from carrying the cookie.
- SameSite is site-based rather than origin-based. Sibling subdomains can be cross-origin while remaining same-site when scheme and registrable domain align.
- A cookie with a parent-domain `Domain` attribute may be delivered to matching subdomains; host-only/`__Host-` cookies can break this chain.

**Held/rejected as universal claims**

- Ordinary server-side callbacks do not imply browser-cookie forwarding.
- SameSite alone does not establish or defeat the chain; exact cookie attributes, navigation context, scheme, path, partitioning, and browser behavior matter.
- Account takeover requires an authoritative/replayable credential and an owned-session proof, not merely an observed preference cookie.

Primary/normative sources:

- https://web.archive.org/web/20220618022718/https://gccybermonks.com/posts/ssrfvision/
- https://httpwg.org/http-extensions/draft-ietf-httpbis-rfc6265bis.html
- https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html

### 2. Zimbra memcache injection — CVE-2022-27924

**Confirmed**

- The canonical CVE record describes unauthenticated arbitrary Memcached command injection and arbitrary cached-entry overwrite in Zimbra Collaboration Suite 8.8.15 and 9.0.
- Zimbra identifies fixes in 8.8.15 P31.1 and 9.0.0 P24.1.
- SonarSource documents a route-cache consumer and a shared response stream whose consumer did not validate the response key, enabling a stronger cross-request routing/credential chain.

**Evidence boundary**

- Cache command injection, arbitrary state overwrite, response misassociation, victim routing, and cleartext credential capture are separate edges. A generic text-protocol injection should not inherit the full Zimbra impact without proving each edge.

Primary sources:

- https://www.cve.org/CVERecord?id=CVE-2022-27924
- https://www.sonarsource.com/blog/zimbra-mail-stealing-clear-text-credentials-via-memcache-injection/
- https://wiki.zimbra.com/wiki/Zimbra_Releases/8.8.15/P31.1
- https://wiki.zimbra.com/wiki/Zimbra_Releases/9.0.0/P24.1

### 3. Elementor DOM XSS — CVE-2022-29455

**Confirmed**

- The canonical record describes DOM-based reflected XSS in Elementor `<=3.5.5` and credits the supplied researcher/article.
- Official WordPress SVN source for 3.5.5 decodes action details from the URL hash and passes settings through lightbox/slideshow logic.
- The 3.5.6 source changes the branch/type handling before `showModal`, providing a primary fix differential.
- Patchstack classifies the issue as unauthenticated DOM-based reflected XSS affecting 3.5.5 and below.

**Held/rejected**

- “6.5 million websites” is historical prevalence context, not target applicability.
- An Elementor asset path, stale version string, or public CVE is not a current finding without plugin-active, exact version, reachable path, browser execution, CSP, and victim evidence.
- The durable lesson is full object-schema/sibling-branch review after a partial property fix—not reuse of a historical payload.

Primary sources:

- https://rotem-bar.com/hacking-65-million-websites-greater-cve-2022-29455-elementor
- https://www.cve.org/CVERecord?id=CVE-2022-29455
- https://plugins.svn.wordpress.org/elementor/tags/3.5.5/assets/js/frontend.js
- https://plugins.svn.wordpress.org/elementor/tags/3.5.6/assets/js/frontend.js
- https://patchstack.com/database/vulnerability/elementor/wordpress-elementor-plugin-3-5-5-unauthenticated-dom-based-reflected-cross-site-scripting-xss-vulnerability

### 4. Python NaN injection

**Confirmed class-level behavior**

- IEEE-754 NaN is unordered: equality with itself is false and ordered comparisons such as `<` and `>` are false.
- A rejection guard shaped as “below minimum OR above maximum” can therefore fail open if NaN survives parsing.
- RFC 8259 does not permit NaN or infinity JSON numbers. Python's standard `json` module nevertheless accepts and emits `NaN`, `Infinity`, and `-Infinity` by default.
- Sorting/aggregation/conversion behavior must be reproduced for the exact runtime and library.

**Local control — Python 3.11.15**

- `math.isnan(NaN)` true; `math.isfinite(NaN)` false.
- Naïve lower/upper rejection guard returned false for NaN; a positive chained-range acceptance returned false.
- `json.loads('NaN')` returned a NaN and `json.dumps()` emitted `NaN`.
- Sorting `[3.0, NaN, 2.0]` did not produce ordinary numeric order.
- Plain `int(NaN)` raised `ValueError`.

**Held/rejected**

- The article's old NumPy integer-cast result was not generalized to plain Python, current NumPy, other architectures, or a target.
- No generic privilege escalation, authentication bypass, auction win, or denial of service is promoted without a target-specific parser-to-impact chain.

Primary sources:

- https://web.archive.org/web/20211230172217/https://blog.bitdiscovery.com/2021/12/python-nan-injection/
- https://github.com/ProZachJ/ducktales
- https://docs.python.org/3/library/math.html#math.isfinite
- https://docs.python.org/3/library/json.html#infinite-and-nan-number-values
- https://www.rfc-editor.org/rfc/rfc8259#section-6

### 5. Safari UXSS chain

**Confirmed**

- CVE-2021-30861 is officially described as a validation issue that could allow bypassing Gatekeeper checks; Apple says it was addressed with improved validation and fixed in Safari 15/macOS Monterey 12.0.1-era updates.
- CVE-2021-30975 is separately described in Script Editor: viewing a scripting dictionary could bypass Gatekeeper checks and sandbox restrictions; Apple disabled JavaScript while viewing scripting dictionaries.
- The original article explicitly describes four bugs—two CVEs and two without CVEs—and composes iCloud shared-object mutability, application launching/handlers, local rendering/origin behavior, and final capability.

**Held/rejected**

- Neither CVE alone proves the full arbitrary-origin UXSS/camera/account-impact chain.
- File placement, Gatekeeper bypass, launch, webarchive/local rendering, arbitrary-origin script execution, camera permission reuse, and sandbox escape are separate evidence edges.
- Historical 2021 behavior is not evidence against a current supported Safari/macOS build.

Primary sources:

- https://www.ryanpickren.com/safari-uxss
- https://www.cve.org/CVERecord?id=CVE-2021-30861
- https://www.cve.org/CVERecord?id=CVE-2021-30975
- https://support.apple.com/en-us/103237
- https://support.apple.com/en-us/102876

## Promoted durable artifacts

- `02 - Vulnerability Playbooks/Web2/SSRF/overview.md`
- `02 - Vulnerability Playbooks/Web2/SSRF/false-positives.md`
- `02 - Vulnerability Playbooks/Web2/SSRF/evidence-requirements.md`
- `02 - Vulnerability Playbooks/Web2/Text Protocol Injection/overview.md` *(new)*
- `02 - Vulnerability Playbooks/Web2/XSS/overview.md`
- `02 - Vulnerability Playbooks/Web2/WordPress CVE Intelligence/overview.md`
- `02 - Vulnerability Playbooks/Web2/REST API/numeric-special-values.md` *(new)*
- `02 - Vulnerability Playbooks/Web2/Browser Integration/overview.md`
- `06 - Evals/Web2/web-security-five-cross-layer-20260731-eval-scenarios.md` *(23 scenarios)*
- `00 - System/web2-skill-index.md`

## Finding/reportability outcome

**0/5 target-specific findings.** All five sources are retained as historical technique and regression material. Any future target candidate must be routed through the relevant playbook and re-proven on the exact in-scope version/configuration using owned controls and adversarial false-positive gates.
