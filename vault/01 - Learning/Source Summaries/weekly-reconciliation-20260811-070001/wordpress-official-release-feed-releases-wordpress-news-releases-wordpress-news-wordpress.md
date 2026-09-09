---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.042216+00:00
source_quality: 10
source_id: wordpress-official-release-feed
source_role: authority
source_trust: primary
promotion_policy: review_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, evidence_requirement]
classification: severity rule
vulnerability_class: AI / LLM Security
---

# Releases – WordPress News Releases – WordPress News WordPress 7.0.3 release WordPress 7.1 Release Candidate 1 WordPress 7.1 Beta 4 WordPress 7.1 Beta 3 WordPress 7.0.2 Release WordPress 7.1 Beta 1 WordPress 7.0.1 Maintenance Release WordPre

- URL: `https://wordpress.org/news/category/releases/feed/`
- Source ID / role / trust: `wordpress-official-release-feed` / `authority` / `primary`
- Acquisition provenance: cadence=`weekly`, method=`feed`, discovered-from=`direct root`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `wordpress_official_security_intelligence`
- Content chars: `15664`
- Classification: **severity rule**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Contributor+ stored cross-site scripting (XSS) in posts via the emoji settings element reported by Asaf Mozes ( amosec ) Contributor+ stored cross-site scripting (XSS) in the Post Content block reported by N05ec@LZU Contributor+ stored cross-site scripting (XSS) in Quick Edit on sites with a large number of users reported by Naveen S and Ajmal Moochingal Contributor+ stored cross-site scripting (XSS) in the Post Date block reported by Alex Concha of the WordPress Security Team A privilege escalation issue on multisite networks with user registration enabled, allowing a user to create a new site reported by Aikido Security An information disclosure issue in the Latest Comments block exposing comments on password-protected posts reported by Ehtisham Siddiqui of the WordPress Security Team Enumeration of post slugs reported by HDWSec Disclosure of notes in comment feeds reported by Elio Gubser Author+ CSS injection via a bypass of the safe CSS attribute filter reported by Anthropic Bypass of the email address confirmation flow reported by Omar Hasan A server-side request forgery (SSRF) issue in URL validation allowing requests to link-local ranges reported by Andrew Mohawk and multiple independent reporters Backports As a courtesy, these fixes are being backported, where necessary, to all branches eligible to receive security fixes (currently through 4.7).
- Releases &#8211; WordPress News https://wordpress.org/news The latest news about WordPress and the WordPress community Fri, 07 Aug 2026 09:50:53 +0000 en-US hourly 1 https://wordpress.org/?v=7.2-alpha-63171 https://s.w.org/favicon.ico?2 Releases &#8211; WordPress News https://wordpress.org/news 32 32 14607090 WordPress 7.0.3 release https://wordpress.org/news/2026/08/wordpress-7-0-3-release/ Thu, 06 Aug 2026 18:55:30 +0000 https://wordpress.org/news/?p=21327 WordPress 7.0.3 is now available WordPress 7.0.3 is now available which features several security fixes.
- Security updates included in this release The security team would like to thank the following people for responsibly reporting vulnerabilities and allowing them to be fixed in this release: Pre-auth reflected cross-site scripting (XSS) on the login screen with potential to lead to PHP code execution reported by the team at pwn.ai .

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, evidence_requirement`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `false`
- Independent corroboration: `conditional`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
