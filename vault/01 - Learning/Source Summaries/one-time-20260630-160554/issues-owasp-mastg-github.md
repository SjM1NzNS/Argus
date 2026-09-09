---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.098817+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Issues · OWASP/mastg · GitHub

- URL: `https://github.com/OWASP/mastg/issues`
- Source group: `backfill_deep_content`
- Content chars: `4580`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...
- Notifications You must be signed in to change notification settings Fork 2.8k Star 13k Code Issues 183 Pull requests 37 Discussions Actions Projects Models Security and quality 0 Insights Additional navigation options Code Issues Pull requests Discussions Actions Projects Models Security and quality Insights Issues Assigned to me Created by me Mentioned Recent activity Views Projects Milestones Labels Feedback Preview Collapse sidebar Issues Search Issues is : issue state : open is:issue state:open Search Labels Milestones New issue Issue creation is restricted in this repository Search results Open Closed Check if we need changes due to this feedback ( shouldOverrideUrlLoading and shouldInterceptRequest ) for MASTG-DEMO-0158 Status: Open. # 3913 In OWASP/mastg; · cpholguera opened on Jun 26, 2026 Generalize MASTG-TEST-0375 for both implicit and explicit intents request-issue-assignment Status: Open. # 3906 In OWASP/mastg; · TheDauntless opened on Jun 23, 2026 Create MASTG-TEST — References to Outgoing Inter-App URLs Carrying Sensitive Data BLOCKED Status: Open. # 3905 In OWASP/mastg; · cpholguera opened on Jun 23, 2026 Review PR #3897 after merge (Android Deep Links) Status: Open. # 3902 In OWASP/mastg; · cpholguera opened on Jun 23, 2026 Add dynamic test and demo for integrity demos MASVS-RESILIENCE tests Status: Open. # 3899 In OWASP/mastg; · cpholguera opened on Jun 22, 2026 Consider new tool ipakeep BLOCKED iOS tools Status: Open. # 3898 In OWASP/mastg; · cpholguera opened on Jun 22, 2026 Review PR #3780 after merge (UIActivity Sharing) Status: Open. # 3896 In OWASP/mastg; · cpholguera opened on Jun 20, 2026 Review PR #3561 after merge (iOS Object Persistence) Status: Open. # 3895 In OWASP/mastg; · cpholguera opened on Jun 20, 2026 Research: Securely handling sensitive data in custom UIActivity (custom activity types) BLOCKED iOS Status: Open. # 3894 In OWASP/mastg; · cpholguera opened on Jun 20, 2026 Restore missing TECH from MASTG-TEST-0075 (Testing Custom URL Schemes, iOS) BLOCKED iOS techniques Status: Open. # 3893 In OWASP/mastg; · cpholguera opened on Jun 19, 2026 Evaluate proposal of adding "self-signed certificates over certificates issued by third-parties" for Pinning BEST Status: Open. # 3888 In OWASP/mastg; · cpholguera opened on Jun 17, 2026 [Android] TEST: Partial source code integrity Android BLOCKED MASVS-RESILIENCE tests Status: Open. # 3887 In OWASP/mastg; · Diolor opened on Jun 17, 2026 Footer Footer navigation Terms Privacy Security Status Community Docs Contact Manage cookies Do not share my personal information

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
