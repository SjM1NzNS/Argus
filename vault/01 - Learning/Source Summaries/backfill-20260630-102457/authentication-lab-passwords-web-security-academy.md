---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.002273+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: Authentication / Session
---

# Authentication lab passwords | Web Security Academy

- URL: `https://portswigger.net/web-security/authentication/auth-lab-passwords`
- Source group: `backfill_deep_content`
- Content chars: `2629`
- Classification: **Web2 skill update**
- Vulnerability class: **Authentication / Session**

## Source summary

- Authentication vs authorization How vulnerabilities arise Impact of vulnerable authentication Vulnerabilities in password-based authentication Brute-force attacks Brute-forcing usernames Brute-forcing passwords Enumerating usernames Flaws in brute-force protection Account locking User rate limiting Exploiting HTTP basic authentication Vulnerabilities in multi-factor authentication Two-factor authentication tokens Bypassing two-factor authentication Bypassing two-factor authentication with flawed verification Brute-forcing two-factor authentication codes Vulnerabilities in other authentication mechanisms Keeping users logged in Resetting user passwords Sending passwords by email Resetting passwords using a URL Changing user passwords Vulnerabilities in OAuth authentication Securing your authentication mechanisms View all authentication labs Web Security Academy Authentication vulnerabilities Password list Authentication lab passwords You can copy and paste the following list to Burp Intruder to help you solve the Authentication labs.
- Burp Scanner Burp Suite's web vulnerability scanner Product comparison What's the difference between Pro and DAST?
- 123456 password 12345678 qwerty 123456789 12345 1234 111111 1234567 dragon 123123 baseball abc123 football monkey letmein shadow master 666666 qwertyuiop 123321 mustang 1234567890 michael 654321 superman 1qaz2wsx 7777777 121212 000000 qazwsx 123qwe killer trustno1 jordan jennifer zxcvbnm asdfgh hunter buster soccer harley batman andrew tigger sunshine iloveyou 2000 charlie robert thomas hockey ranger daniel starwars klaster 112233 george computer michelle jessica pepper 1111 zxcvbn 555555 11111111 131313 freedom 777777 pass maggie 159753 aaaaaa ginger princess joshua cheese amanda summer love ashley nicole chelsea biteme matthew access yankees 987654321 dallas austin thunder taylor matrix mobilemail mom monitor monitoring montana moon moscow Find vulnerabilities in your authentication using Burp Suite Try for free Burp Suite Vulnerabilities Customers Company Insights © 2026 PortSwigger Ltd.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
