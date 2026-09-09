---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.102334+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: Authentication / Session
---

# Pull requests · OWASP/wstg · GitHub

- URL: `https://github.com/OWASP/wstg/pulls`
- Source group: `backfill_deep_content`
- Content chars: `4534`
- Classification: **Web2 skill update**
- Vulnerability class: **Authentication / Session**

## Source summary

- Please reload this page . assignee: Filter by this user Sort Sort by Newest Oldest Most commented Least commented Recently updated Least recently updated Best match Most reactions 👍 👎 😄 🎉 😕 ❤️ 🚀 👀 Pull requests list docs: add Mohammad Hossein Sadeghian to authors #1439 opened Jun 30, 2026 by m4sh-wacker Contributor Loading… WSTG-ATHN-03: Add credential stuffing and distributed brute force testing guidance #1356 opened Mar 9, 2026 by YK-03 Contributor Loading… 3 Add guidance for testing password reset token exposure via Referer headers #1355 opened Mar 6, 2026 by YK-03 Contributor Loading… 2 tasks done 10 Add WSTG-INPV-22: Testing for Insecure Deserialization (Fixes #7) #1345 opened Feb 24, 2026 by Galaxy-sc Contributor Loading… 2 tasks done 1 2 Enhance WSTG with Comprehensive API Security Testing Guidance #1298 opened Feb 1, 2026 by Godstaf Loading… 3 Add architectural threat modeling checklist for workflow and state abuse #1267 opened Dec 25, 2025 by balaakasam Loading… 2 tasks done 4 XSS Reorganization revise Needs quality review, updates, or revision work_in_progress Issue or PR not yet ready for review #1074 opened Jun 30, 2023 by manindar-mohan Contributor Loading… 2 tasks done v5.0 Release 1 61 ProTip!
- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
