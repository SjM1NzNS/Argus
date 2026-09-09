---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.042969+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Issues · OWASP/wstg · GitHub

- URL: `https://github.com/OWASP/wstg/issues`
- Source group: `backfill_deep_content`
- Content chars: `5610`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...
- Notifications You must be signed in to change notification settings Fork 1.6k Star 9.5k Code Issues 35 Pull requests 8 Actions Models Security and quality 0 Insights Additional navigation options Code Issues Pull requests Actions Models Security and quality Insights Issues Assigned to me Created by me Mentioned Recent activity Views Milestones Labels Feedback Preview Collapse sidebar Known Issue: WSTG-INPV-13 is listed twice in checklist.json # 1165 · J0n-H4rr150n opened on Nov 19, 2024 5 Draft Notes for v4.3 Release # 1393 · kingthorin opened on Apr 5, 2026 Issues Search Issues is : issue state : open is:issue state:open Search Labels Milestones New issue Issue creation is restricted in this repository Search results Open Closed Draft Notes for v4.3 Release new New content to write New content to write repo A task specifically related to the project repository A task specifically related to the project repository work_in_progress Issue or PR not yet ready for review Issue or PR not yet ready for review Status: Open.
- Task # 1393 In OWASP/wstg; · kingthorin opened on Apr 5, 2026 · v4.3 Release Add: Testing for Security Control Bypass During Feature Flag Transitions new New content to write New content to write Status: Open. # 1265 In OWASP/wstg; · balaakasam opened on Dec 25, 2025 Proposed New Test Case: Detecting Workflow and State Transition Abuse new New content to write New content to write Status: Open. # 1262 In OWASP/wstg; · balaakasam opened on Dec 14, 2025 [Suggestion] 4.7.21 Testing for Parameter Input Handling enhancement A new or improved feature for the WSTG or repo A new or improved feature for the WSTG or repo Status: Open. # 1221 In OWASP/wstg; · websecnl opened on Jul 4, 2025 · v4.3 Release AI Crawlers new New content to write New content to write Status: Open. # 1204 In OWASP/wstg; · cmlh opened on Mar 29, 2025 · v4.3 Release v5.0 Release question Blocked: information required before proceeding Blocked: information required before proceeding Status: Open. # 1186 In OWASP/wstg; · xb8 opened on Feb 19, 2025 Known Issue: WSTG-INPV-13 is listed twice in checklist.json repo A task specifically related to the project repository A task specifically related to the project repository Status: Open. # 1165 In OWASP/wstg; · J0n-H4rr150n opened on Nov 19, 2024 WSTG-INFO include up-to-date tooling and examples new New content to write New content to write Status: Open. # 1058 In OWASP/wstg; · kingthorin opened on May 23, 2023 · v4.3 Release Adding Test for Outdated and Unsupported Components enhancement A new or improved feature for the WSTG or repo A new or improved feature for the WSTG or repo revise Needs quality review, updates, or revision Needs quality review, updates, or revision Status: Open. # 1017 In OWASP/wstg; · cyspad opened on Jan 7, 2023 Adding sections (description, impact...) for reports enhancement A new or improved feature for the WSTG or repo A new or improved feature for the WSTG or repo Status: Open. # 1006 In OWASP/wstg; · JulianGR opened on Dec 30, 2022 Review and update content about SameSite cookies revise Needs quality review, updates, or revision Needs quality review, updates, or revision Status: Open. # 1005 In OWASP/wstg; · rbsec opened on Dec 27, 2022 Inappropriate content (Testing for Cross Site Script Inclusion) help wanted revise Needs quality review, updates, or revision Needs quality review, updates, or revision Status: Open. # 954 In OWASP/wstg; · yhojann-cl opened on Jul 18, 2022 Footer Footer navigation Terms Privacy Security Status Community Docs Contact Manage cookies Do not share my personal information

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
