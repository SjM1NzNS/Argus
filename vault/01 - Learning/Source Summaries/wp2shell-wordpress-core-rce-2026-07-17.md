---
type: source-summary
created: "2026-07-17"
source: "https://wp2shell.com/"
status: promoted
confidence: high-for-official-facts
---

# WP2Shell / WordPress Core pre-auth RCE — source summary

## Disposition

**Promoted with strict live-target gates.** The supplied site is a legitimate disclosure/checker page from Searchlight Cyber, and the core claims are corroborated by WordPress.org and WordPress's GitHub Security Advisories. Technical exploit details were intentionally withheld at review time; Argus did not submit any domain to the checker and did not attempt the vulnerability.

## Confirmed facts

- Disclosure date: 2026-07-17.
- `CVE-2026-63030` / `GHSA-ff9f-jf42-662q`: REST API batch-route confusion combined with SQLi yields pre-authentication RCE on stock WordPress without plugins.
- RCE-affected: `6.9.0–6.9.4`, `7.0.0–7.0.1`.
- RCE-fixed: `6.9.5`, `7.0.2`, and `7.1 beta2`.
- Companion `CVE-2026-60137` / `GHSA-fpp7-x2x2-2mjf`: facilitated SQL injection in `WP_Query` parameter `author__not_in`.
- SQLi-affected: `6.8.0–6.8.5`, `6.9.0–6.9.4`, `7.0.0–7.0.1`.
- SQLi-fixed: `6.8.6`, `6.9.5`, `7.0.2`.
- Versions before 6.8 are unaffected; 6.8.x does not have the REST confusion component and therefore must not be labeled with the combined RCE impact.
- WordPress enabled forced automatic updates because of severity.

## Patch-derived root-cause model

The public `7.0.1...7.0.2` diff changed three security-relevant areas:

1. `class-wp-query.php`: always parses `author__not_in` with a strict ID-list parser before generating an SQL `NOT IN` list, closing the scalar-vs-array sanitization gap.
2. `rest-api.php` and `class-wp-rest-server.php`: refuse to start a new top-level REST lifecycle while dispatch is already in progress; internal subrequests must use `dispatch()`.
3. `class-wp-rest-server.php`: on an invalid batch subrequest, preserve aligned entries in both match and validation bookkeeping.

This supports a general chain model: input-shape normalization flaw + nested lifecycle confusion + batch index/route confusion can change a moderate injection primitive into critical unauthenticated code execution.

## Safe operational guidance

- Do not submit third-party domains to `wp2shell.com`; it delegates probing to an external checker.
- Do not run exploit requests against live bounty targets autonomously.
- Prefer official release/version evidence, patch diff review, passive target evidence already exposed during normal browsing, and a vulnerable/fixed owned lab.
- Version evidence alone is a candidate, not proof of RCE.
- Update is primary mitigation. Emergency controls should block anonymous batch REST access in both pretty-permalink and `rest_route` forms and be checked for application breakage.

## Preview.is RAG result

Query `manual-preview-is-20260717-210034` returned no direct WP2Shell match. The top result (`https://nowotarski.info/wordpress-nonce-authorization/`, score `0.9079`) concerned a different WordPress plugin SQLi and was **not used** as evidence for this core CVE. Lower-score historical/general results were likewise deferred. This summary relies on the official sources below.

## Sources

- https://wp2shell.com/
- https://slcyber.io/research-center/wp2shell-pre-authentication-rce-in-wordpress-core
- https://wordpress.org/news/2026/07/wordpress-7-0-2-release/
- https://wordpress.org/documentation/wordpress-version/version-7-0-2/
- https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-ff9f-jf42-662q
- https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-fpp7-x2x2-2mjf
- https://github.com/WordPress/wordpress-develop/compare/7.0.1...7.0.2

## Local artifacts

- `01 - Learning/Inbox/manual-20260717-wp2shell/`
- `01 - Learning/Inbox/manual-preview-is-20260717-210034/`
