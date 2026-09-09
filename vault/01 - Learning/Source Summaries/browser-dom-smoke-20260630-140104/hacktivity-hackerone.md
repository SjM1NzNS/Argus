---
type: learning-source-summary
compiled_at: 2026-06-30T12:02:12.839924+00:00
source_quality: 6
classification: Web2 skill update
vulnerability_class: Authentication / Session
---

# Hacktivity | HackerOne

- URL: `https://hackerone.com/hacktivity/overview?queryString=disclosed%3Atrue&sortField=latest_disclosable_activity_at&sortDirection=DESC&pageIndex=0`
- Source group: `web2_continuous_monitoring`
- Content chars: `8391`
- Classification: **Web2 skill update**
- Vulnerability class: **Authentication / Session**

## Source summary

- 9 curl Low Informative UAF read in mev_pollset_diff() trace path after curl_easy_pause() in socket callback Bug reported by homanp was disclosed 2 days ago Use After Free 9 curl Low Informative Use-after-free in `mev_forget_socket` when `curl_easy_pause()` is called from a `CURL_POLL_REMOVE` socket callback (incomplete fix of CVE-2026-9080) Bug reported by stze was disclosed 2 days ago Use After Free 13 curl Medium Not-applicable mbedTLS / wolfSSL / rustls backends silently skip hostname verification when CURLOPT_SSL_VERIFYPEER=0 Bug reported by d1sclose was disclosed 4 days ago Improper Validation of Certificate with Host Mismatch 8 curl Medium Not-applicable CURLOPT_HAPROXY_CLIENT_IP lacks input validation, enabling HAProxy PROXY protocol injection Bug reported by tneelc was disclosed 4 days ago CRLF Injection 31 Revive Adserver High Resolved PHP code injection in delivery-limitation `logical` validation bypass - XML-RPC setChannelTargeting Bug reported by doomtech was disclosed 5 days ago Code Injection 22 Revive Adserver Medium Resolved XML‑RPC login leak exposes valid session ID enabling unauthorized API access Bug reported by garuthacktvist was disclosed 5 days ago Improper Access Control - Generic 20 Revive Adserver Medium Resolved Reflected XSS via unsanitised refresh parameter in zone invocation tag Bug reported by kanon4 was disclosed 5 days ago Cross-site Scripting (XSS) - Reflected A missing sanitization of user input in the zone-include.php script of Revive Adserver 6.0.7 and earlier was reported.
- Search for reports Filter Sort Disclosed Undisclosed 0 curl Low Not-applicable setopt(VERIFYPEER) from callback bypasses TLS verify on connection reuse Bug reported by a6b30108 was disclosed 57 mins ago 1 curl Medium Informative ssh_config_matches is dead code: unauthorized SSH key reuse Bug reported by bigsize was disclosed 2 hrs ago Authentication Bypass by Primary Weakness 0 curl Informative CURLSHOPT_UNSHARE race can cause UAF in shared SSL session cache during HTTPS transfer Bug reported by smaeljaish771 was disclosed 2 hrs ago Use After Free 0 curl Low Not-applicable libcurl upload read callbacks miss recursive API guard, allowing prohibited multi API reentry and ASAN-confirmed UAF Bug reported by th3hound was disclosed 6 hrs ago 18 Discourse High $1,024 Resolved Denial of Service (DoS) Vulnerability in Drafts Creation Endpoint Bug reported by dpaysm was disclosed 10 hrs ago Uncontrolled Resource Consumption A Denial of Service (DoS) vulnerability was identified in the /drafts.json endpoint on the Discourse forum.
- Linking and unlinking banners or campaigns to zones could be triggered via crafted GET or POST requests without any verification of the CSRF token, allowing an attacker to perform these actions on behalf of an authenticated administrator.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
