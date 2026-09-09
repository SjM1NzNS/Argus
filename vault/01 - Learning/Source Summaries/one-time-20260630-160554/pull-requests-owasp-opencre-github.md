---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.096410+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# Pull requests · OWASP/OpenCRE · GitHub

- URL: `https://github.com/OWASP/OpenCRE/pulls`
- Source group: `backfill_deep_content`
- Content chars: `6577`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...
- Please reload this page . assignee: Filter by this user Sort Sort by Newest Oldest Most commented Least commented Recently updated Least recently updated Best match Most reactions 👍 👎 😄 🎉 😕 ❤️ 🚀 👀 Pull requests list feat(api): add GET /api/capabilities to expose myopencre feature flag #949 opened Jun 25, 2026 by skypank-coder Contributor Loading… 1 3 GSoC 2026 Module B — Week 3: Stage 2 LLM relevance classifier #947 opened Jun 25, 2026 by manshusainishab Contributor Loading… 4 feat(RFC): implement candidate retrieval checkpoints D1 and D2 #944 opened Jun 24, 2026 by Abhijeet2409 Contributor Loading… 11 feat(frontend): add reusable useUser hook and header auth UX #943 opened Jun 21, 2026 by skypank-coder Contributor Loading… 1 4 week_3: Module C (The Librarian) — C.1 candidate retriever (in-memory + pgvector) + pipeline switch #937 opened Jun 18, 2026 by PRAteek-singHWY Contributor Loading… 7 feat(workstream-c): add cheatsheet categorizer and grouping #934 opened Jun 15, 2026 by shreeshtripurwarcomp23-coder Contributor Loading… 7 Move files out of root directory to highlight README (#571) #933 opened Jun 14, 2026 by SurbhiAgarwal1 Loading… 1 3 Research k09 mapping #927 opened Jun 11, 2026 by SurbhiAgarwal1 Loading… 1 19 week_2: Module C (The Librarian) — C.0 input boundary: SectionValidator + ExplicitLinkResolver #925 opened Jun 10, 2026 by PRAteek-singHWY Contributor Loading… 3 week_1: Module C (The Librarian) — RFC contracts + eval harness + golden dataset #922 opened Jun 9, 2026 by PRAteek-singHWY Contributor Loading… 8 GSOC-Week1-Module_A #920 opened Jun 7, 2026 by ParthAggarwal16 Contributor Loading… 7 Retry transient failures during upstream sync #900 opened May 6, 2026 by Bornunique911 Contributor Loading… 2 Improved boilerplate, github link scrolling to readme, and completing… #896 opened Apr 30, 2026 by robvanderveer Collaborator Loading… 4 Fix: Prevent infinite loop in gap_analysis preload (#885) #895 opened Apr 29, 2026 by PRAteek-singHWY Contributor Loading… 1 1 Feat/litellm unified client #892 opened Apr 28, 2026 by northdpole Collaborator Loading… 3 fix: remove fragile URL fallback from MyOpenCRE CSV download #880 opened Apr 14, 2026 by PRAteek-singHWY Contributor Loading… 1 Fix weak-link deduplication in gap_analysis: check correct dict level #879 opened Apr 11, 2026 by PRAteek-singHWY Contributor Loading… 1 Add refresh scripts for OWASP resources for issue 471 #877 opened Apr 11, 2026 by Bornunique911 Contributor Loading… 36 RFC: User Authentication and Online MyOpenCRE Mapping #876 opened Apr 9, 2026 by skypank-coder Contributor Loading… 6 fix: pin dependencies to exact versions using pip-tools #874 opened Apr 8, 2026 by shiwani42 Contributor Loading… 5 tasks done 1 Normalize OWASP cheat sheet references #865 opened Apr 6, 2026 by Bornunique911 Contributor Loading… 15 feat: add automated Heroku data health equivalency checks #864 opened Apr 5, 2026 by PRAteek-
- OWASP / OpenCRE Public Notifications You must be signed in to change notification settings Fork 117 Star 161 Code Issues 82 Pull requests 78 Discussions Actions Projects Models Security and quality 0 Insights Additional navigation options Code Issues Pull requests Discussions Actions Projects Models Security and quality Insights Pull requests: OWASP/OpenCRE Labels 16 Milestones 5 Labels 16 Milestones 5 New pull request New 78 Open 558 Closed 78 Open 558 Closed Author Filter by author Loading Uh oh!

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
