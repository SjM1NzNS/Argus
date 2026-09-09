---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.057230+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Issues · OWASP/ASVS · GitHub

- URL: `https://github.com/OWASP/ASVS/issues`
- Source group: `backfill_deep_content`
- Content chars: `4946`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...
- Notifications You must be signed in to change notification settings Fork 815 Star 3.5k Code Issues 100 Pull requests 8 Discussions Actions Projects Models Wiki Security and quality 0 Insights Additional navigation options Code Issues Pull requests Discussions Actions Projects Models Wiki Security and quality Insights Issues Assigned to me Created by me Mentioned Recent activity Views Projects Milestones Labels Feedback Preview Collapse sidebar Issues Search Issues is : issue state : open is:issue state:open Search Labels Milestones New issue Issue creation is restricted in this repository Search results Open Closed Requesting Appendix E credit: J-XL (commented on #3335, endorsed by project lead) Status: Open. # 3365 In OWASP/ASVS; · J-XL opened on Jun 24, 2026 Clarification of language around HSTS 4) proposal for review Issue contains clear proposal for add/change something Issue contains clear proposal for add/change something V3 (prev V50) Group issues related to Web Frontend Group issues related to Web Frontend Status: Open. # 3364 In OWASP/ASVS; · tautology0 opened on Jun 24, 2026 Inconsistent chapter introductions 5) awaiting PR A proposal hs been accepted and reviewed and we are now waiting for a PR A proposal hs been accepted and reviewed and we are now waiting for a PR Status: Open. # 3363 In OWASP/ASVS; · jmanico opened on Jun 22, 2026 Include info/requirements about Post Quantum Cryptography Status: Open. # 3361 In OWASP/ASVS; · randomstuff opened on May 29, 2026 Improve clarity of TLS version requirements in V9.1.3 V12 (prev V9) Status: Open. # 3360 In OWASP/ASVS; · sujalavnelavai opened on May 29, 2026 ASVS CycloneDX Export is Invalid 6) PR awaiting review Status: Open. # 3354 In OWASP/ASVS; · stevespringett opened on Apr 14, 2026 Reduce maximum lifetime of OAuth authorization code (10.4.3) V10 (prev V51) Group issues related to OAuth Group issues related to OAuth Status: Open. # 3353 In OWASP/ASVS; · randomstuff opened on Apr 12, 2026 Proposal: add requirements to verify correct implementation of OAuth PAR and JAR V10 (prev V51) Group issues related to OAuth Group issues related to OAuth Status: Open. # 3352 In OWASP/ASVS; · mirokarv opened on Apr 2, 2026 Proposal: High-legibility fonts requirement Status: Open. # 3349 In OWASP/ASVS; · narfbg opened on Mar 23, 2026 proposal: add requirement to verify that using a sanitization is an accepted solution for that data or flow V1 (prev V5) Status: Open. # 3346 In OWASP/ASVS; · elarlang opened on Mar 9, 2026 V11.1.4 restates cryptographic inventory requirement already covered by V11.1.2 V11 (prev V6) Status: Open. # 3345 In OWASP/ASVS; · tghosth opened on Mar 5, 2026 V4.3.3-derived requirement accidentally deleted, mapping is stale V13 (prev V14) Status: Open. # 3344 In OWASP/ASVS; · tghosth opened on Mar 5, 2026 Footer Footer navigation Terms Privacy Security Status Community Docs Contact Manage cookies Do not share my personal information

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
