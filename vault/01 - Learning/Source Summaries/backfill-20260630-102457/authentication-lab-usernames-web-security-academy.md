---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.002635+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: Authentication / Session
---

# Authentication lab usernames | Web Security Academy

- URL: `https://portswigger.net/web-security/authentication/auth-lab-usernames`
- Source group: `backfill_deep_content`
- Content chars: `2592`
- Classification: **Web2 skill update**
- Vulnerability class: **Authentication / Session**

## Source summary

- Authentication vs authorization How vulnerabilities arise Impact of vulnerable authentication Vulnerabilities in password-based authentication Brute-force attacks Brute-forcing usernames Brute-forcing passwords Enumerating usernames Flaws in brute-force protection Account locking User rate limiting Exploiting HTTP basic authentication Vulnerabilities in multi-factor authentication Two-factor authentication tokens Bypassing two-factor authentication Bypassing two-factor authentication with flawed verification Brute-forcing two-factor authentication codes Vulnerabilities in other authentication mechanisms Keeping users logged in Resetting user passwords Sending passwords by email Resetting passwords using a URL Changing user passwords Vulnerabilities in OAuth authentication Securing your authentication mechanisms View all authentication labs Web Security Academy Authentication vulnerabilities Username list Authentication lab usernames You can copy and paste the following list to Burp Intruder to help you solve the Authentication labs. carlos root admin test guest info adm mysql user administrator oracle ftp pi puppet ansible ec2-user vagrant azureuser academico acceso access accounting accounts acid activestat ad adam adkit admin administracion administrador administrator administrators admins ads adserver adsl ae af affiliate affiliates afiliados ag agenda agent ai aix ajax ak akamai al alabama alaska albuquerque alerts alpha alterwind am amarillo americas an anaheim analyzer announce announcements antivirus ao ap apache apollo app app01 app1 apple application applications apps appserver aq ar archie arcsight argentina arizona arkansas arlington as as400 asia asterix at athena atlanta atlas att au auction austin auth auto autodiscover Find vulnerabilities in your authentication using Burp Suite Try for free Burp Suite Vulnerabilities Customers Company Insights © 2026 PortSwigger Ltd.
- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
