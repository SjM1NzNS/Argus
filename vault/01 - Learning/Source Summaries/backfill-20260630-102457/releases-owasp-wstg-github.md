---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.044544+00:00
source_quality: 9
classification: Web2 skill update
vulnerability_class: API Security
---

# Releases · OWASP/wstg · GitHub

- URL: `https://github.com/OWASP/wstg/releases`
- Source group: `backfill_deep_content`
- Content chars: `11834`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- No results found View all tags Release v4.2 Latest Latest Published here: https://owasp.org/www-project-web-security-testing-guide/v42/ - Guide: - Add GraphQL API testing scenario and details (WSTG-APIT-01). - Add Test Objectives to all scenarios. - Add Testing for HTTP Method Overriding (WSTG-CONF-06). - Add to Review Webpage Content for Information Leakage (WSTG-INFO-05). - Add Testing for Session Hijacking (WSTG-SESS-09). - Add to Testing for Bypassing Authorization Schema (WSTG-ATHZ-02). - Add to Testing for Local File Inclusion (WSTG-INPV-11.1). - Add Appendix F: Leveraging Dev Tools. - Add Testing for Server-Side Request Forgery (WSTG-INPV-19). - Add to Testing for Weak Lock Out Mechanism (WSTG-ATHN-03). - Merge section Fingerprint Web Application (WSTG-INFO-09) into Fingerprint Web Application Framework (WSTG-INFO-08). - Merge section Testing for HTTP Verb Tampering (WSTG-INPV-03) into Test HTTP Methods (WSTG-CONF-06). - Merge section Testing for Stack Traces (WSTG-ERRH-02) into Testing for Improper Error Handling (WSTG-ERRH-01). - Update Frontispiece (Chapter 1). - Update Introduction (Chapter 2). - Update Test HTTP Strict Transport Security (WSTG-CONF-07). - Update Review Webserver Metafiles for Information Leakage (WSTG-INFO-03). - Update Penetration Testing Methodologies (Chapter 3.8). - Update Test HTTP Methods (WSTG-CONF-06). - Update Test Upload of Malicious Files (WSTG-BUSL-09). - Update Testing for Weak Encryption (WSTG-CRYP-04). - Update Testing for SSI Injection (WSTG-INPV-08). - Update Testing for Format String Injection (WSTG-INPV-13). - Update DOM-Based Cross Site Scripting to include sources, sinks, and their corresponding references (WSTG-CLNT-01). - Remove Testing for Buffer Overflow (WSTG-INPV-13). - Rewrite Fuzz Vectors (Appendix C). - Rewrite Testing for Weak Transport Layer Security (WSTG-CRYP-01). - Rewrite Role Definitions (WSTG-IDNT-01). - Rewrite Weak Lockout (WSTG-ATHN-03). - Rewrite Testing for Credentials Transported over an Encrypted Channel (WSTG-ATHN-01). - Rewrite Session Fixation Testing (WSTG-SESS-03). - Rewrite Testing for Improper Error Handling (WSTG-ERRH-01). - Rewrite Reporting section. - Update Test for Process Timing (WSTG-BUSL-04). - Update Contributor Guide, Style Guide, and Content Templates. - Standardize HTTP request/response examples. - Establish consistent terminology. - Change MiTM terminology to manipulator-in-the-middle, aligning with other industry projects such as ZAP. - Add reference and linking details. - Update references an
- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
