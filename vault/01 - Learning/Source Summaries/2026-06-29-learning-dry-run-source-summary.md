---
type: source-summary
status: draft
created: "2026-06-29 11:53"
run: "2026-06-29-learning-dry-run"
---

# Argus Learning Dry Run Source Summary

## Ingestion run

- Script: `$HOME/SecurityResearch/11 - Scripts/learning/run_learning_ingest.sh`
- Inbox: `$HOME/SecurityResearch/01 - Learning/Inbox/2026-06-29/`
- Completed mode used for compiler input: `ARGUS_DRY_RUN=1`
- Note: a full non-dry run was attempted first but hit the 300s command timeout; the dry run completed cleanly and produced 38 candidate records.

## Sources that worked in targeted metadata fetch

- PortSwigger Web Security Academy - All Topics: https://portswigger.net/web-security/all-topics — All Web Security Academy topics | Web Security Academy - PortSwigger
- HackTricks: https://hacktricks.wiki/en/index.html — HackTricks - HackTricks
- OWASP WSTG: https://github.com/OWASP/wstg — GitHub - OWASP/wstg: The Web Security Testing Guide is a comprehensive Open Source guide to testing the security of web applications and web services. · GitHub
- OWASP ASVS: https://github.com/OWASP/ASVS — GitHub - OWASP/ASVS: Application Security Verification Standard · GitHub
- OWASP API Security: https://owasp.org/www-project-api-security/ — OWASP API Security Project | OWASP Foundation
- OWASP Cheat Sheet Series: https://github.com/OWASP/CheatSheetSeries — GitHub - OWASP/CheatSheetSeries: The OWASP Cheat Sheet Series was created to provide a concise collection of high value information on specific application security topics. · GitHub
- PortSwigger Research: https://portswigger.net/research — Web Security Research Papers - PortSwigger Research
- AppSec.fyi Root Topic Index: https://appsec.fyi — AppSec Resource Library by Carl Sampson — XSS, SQLi, SSRF, IDOR & More | appsec.fyi
- AppSec.fyi IDOR Resources: https://appsec.fyi/idor.html — Insecure Direct Object Reference (IDOR) Resources | appsec.fyi
- AppSec.fyi XSS Resources: https://appsec.fyi/xss.html — Cross-Site Scripting (XSS) Resources | appsec.fyi
- Solidity Security Considerations: https://docs.soliditylang.org/en/latest/security-considerations.html — Security Considerations — Solidity 0.8.36-develop documentation
- Immunefi Blog: https://immunefi.com/blog/ — The Immunefi Blog
- Immunefi Research: https://immunefi.com/blog/research/ — Research - The Immunefi Blog
- Rekt News: https://rekt.news — Rekt - <!-- -->Home

## Sources that failed in targeted metadata fetch

- None in targeted fetch.

## Sources requiring manual/dynamic review

- Solodit by Cyfrin - Findings Filtered by Recency: https://solodit.cyfrin.io/?i=HIGH%2CMEDIUM%2CLOW%2CGAS&maxf=&minf=&rf=alltime&sd=Desc&sf=Recency

## AppSec.fyi linked-resource candidates extracted

AppSec.fyi was treated as a topic index. The linked resources below are candidates and must be scored independently before skill changes.

- IDOR / Access Control: https://x.com/intent/tweet?text=Insecure%20Direct%20Object%20Reference%20%28IDOR%29%20Resources%20%E2%80%94%20appsec.fyi&url=https%3A%2F%2Fappsec.fyi%2Fidor.html — rejected_low_signal, social share URL; filter in future runs
- IDOR / Access Control: https://www.linkedin.com/sharing/share-offsite/?url=https://appsec.fyi/idor.html — rejected_low_signal, social share URL; filter in future runs
- IDOR / Access Control: https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html — quality 8, official/academy/repository
- IDOR / Access Control: https://infosecwriteups.com/breaking-down-two-simple-vulnerabilities-that-exposed-a-schools-admission-records-040bd636a7f3 — quality 6, linked resource
- IDOR / Access Control: https://foro3d.com/en/2026/abril/bug-bounty-de-max-213-fallos-y-22-millones-en-recompensas.html — quality 6, linked resource
- IDOR / Access Control: https://dev.to/kai_learner/how-to-find-idor-vulnerabilities-the-bug-bounty-hunters-practical-guide-46o8 — quality 6, linked resource
- IDOR / Access Control: https://www.penligent.ai/hackinglabs/idor-in-the-wild-what-cve-2025-13526-really-teaches-security-engineers/ — quality 6, linked resource
- IDOR / Access Control: https://infosecwriteups.com/build-an-idor-vulnerability-lab-why-where-clauses-dont-protect-your-api-e5bd6528c339 — quality 6, linked resource
- IDOR / Access Control: https://www.youtube.com/watch?v=wx5TwS0Dres — quality 5, talk/video; manual review needed
- IDOR / Access Control: https://infosecwriteups.com/bug-bounty-bootcamp-47-account-takeover-101-how-to-steal-everyones-account-legally-684fd8e3e198 — quality 6, linked resource
- XSS: https://x.com/intent/tweet?text=Cross-Site%20Scripting%20%28XSS%29%20Resources%20%E2%80%94%20appsec.fyi&url=https%3A%2F%2Fappsec.fyi%2Fxss.html — rejected_low_signal, social share URL; filter in future runs
- XSS: https://www.linkedin.com/sharing/share-offsite/?url=https://appsec.fyi/xss.html — rejected_low_signal, social share URL; filter in future runs
- XSS: https://owasp.org/www-community/attacks/xss/ — quality 8, official/academy/repository
- XSS: https://www.cisa.gov/known-exploited-vulnerabilities-catalog — quality 6, linked resource
- XSS: https://nvd.nist.gov/vuln/detail/CVE-2026-42897 — quality 6, linked resource
- XSS: https://nvd.nist.gov/vuln/detail/CVE-2025-48700 — quality 6, linked resource
- XSS: https://nvd.nist.gov/vuln/detail/CVE-2025-66376 — quality 6, linked resource
- XSS: https://www.rescana.com/post/cve-2026-10086-high-severity-xss-vulnerability-in-gitlab-enterprise-edition-analytics-dashboard-analysis-impact-and-miti — quality 6, linked resource
- XSS: https://cybersecuritynews.com/gitlab-vulnerabilities-xss-and-dos/ — quality 6, linked resource
- XSS: https://cyberpress.org/jenkins-patches-high-severity-plugin-vulnerability/ — quality 6, linked resource

## Compiler decision

No mature skills were overwritten. This run created source summaries, technique extraction notes, skill patch proposals, changelog draft entries, and eval update proposals only.
