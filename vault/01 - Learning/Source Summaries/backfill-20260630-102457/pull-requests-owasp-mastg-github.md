---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.028554+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Pull requests · OWASP/mastg · GitHub

- URL: `https://github.com/OWASP/mastg/pulls`
- Source group: `backfill_deep_content`
- Content chars: `6862`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...
- Notifications You must be signed in to change notification settings Fork 2.8k Star 13k Code Issues 183 Pull requests 37 Discussions Actions Projects Models Security and quality 0 Insights Additional navigation options Code Issues Pull requests Discussions Actions Projects Models Security and quality Insights Pull requests: OWASP/mastg Labels 48 Milestones 7 Labels 48 Milestones 7 New pull request New 37 Open 2,337 Closed 37 Open 2,337 Closed Author Filter by author Loading Uh oh!
- Please reload this page . assignee: Filter by this user Sort Sort by Newest Oldest Most commented Least commented Recently updated Least recently updated Best match Most reactions 👍 👎 😄 🎉 😕 ❤️ 🚀 👀 Pull requests list fill MASTG-KNOW-0107-Detection Mechanisms #3891 opened Jun 18, 2026 by simge-yigit Collaborator Loading… 1 task 1 2 Update DEMO-0128/ 0129 / 0130 and TEST-0364 / 0365 / 0366 and Add new DEMO for Broadcast Receivers ai-assisted demos #3884 opened Jun 16, 2026 by cpholguera Collaborator • Draft 1 of 2 tasks v2.1 Add New Test/Demo Sections Align TESTs 242-244 with iOS (Pinning) #3882 opened Jun 15, 2026 by cpholguera Collaborator • Draft Migrate demos and tests to v2.1 spec sections #3877 opened Jun 14, 2026 by Diolor Collaborator • Draft v2.1 Add New Test/Demo Sections 2 fill MASTG-KNOW-0106 App-Initiated Screenshots and Screen Recording #3858 #3874 opened Jun 14, 2026 by simge-yigit Collaborator Loading… 1 task 1 Draft: v2.1 specs #3873 opened Jun 14, 2026 by Diolor Collaborator • Draft v2.1 Add New Test/Demo Sections 1 fill MASTG-KNOW-0105 user-initiated screenshot/recording placeholder #3859 opened Jun 6, 2026 by simge-yigit Collaborator • Draft 1 task 1 3 Fixes #3855-Update MASTG-KNOW-0048.md #3856 opened Jun 5, 2026 by simge-yigit Collaborator Loading… 1 task 1 9 Add more test cases covering the v1 MASTG-TEST-0048: RE Tools Detection (android) (by @appknox) prio-low #3848 opened Jun 3, 2026 by ScreaMy7 Collaborator Loading… 5 of 6 tasks 1 12 Add iDump as alternative to frida-ios-dump in MASTG-TOOL-0050 #3799 opened May 14, 2026 by Fi5t Contributor Loading… 5 of 6 tasks 4 Add MASTG-TEST for Sensitive Data Stored Unencrypted via Java File APIs in the App Sandbox #3796 opened May 10, 2026 by Copilot AI • Draft 1 3 Add MASTG-KNOW-0x01: Android DataStore knowledge article #3785 opened May 3, 2026 by Copilot AI • Draft 1 10 Attestation (Android+ iOS): Best Practises, Know, Tests, Demos Android best practices knowledge MASVS-RESILIENCE #3756 opened Apr 2, 2026 by Diolor Collaborator Loading… 1 task 1 14 RFC: MAS-Assets #3755 opened Mar 31, 2026 by Diolor Collaborator • Draft Update MASTG-TECH-0142: add direct file system inspection of WebView storage directory #3739 opened Mar 7, 2026 by Copilot AI • Draft 1 Cluster workflows ai-assisted automation #3691 opened Feb 6, 2026 by Diolor Collaborator Loading… 1 task done 1 Add MASTG content for Android 16 accessibilityDataSensitive protection #3679 opened Jan 31, 2026 by Copilot AI • Draft 1 Added/Updated Android Network Knowledge, Test and Demo #3617 opened Jan 9, 2026 by bernhste Collaborator • Draft 2 tasks done 8 Add Google Data Safety and Privacy Policy retrieval support #3597 opened Dec 18, 2025 by Copilot AI Loading… 1 10 Fix and narrow terms for better scoping #3592 opened Dec 15, 2025 by cpholguera Collaborator • Draft Fix spelling errors and imp

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
