---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.034335+00:00
source_quality: 8
classification: technique
vulnerability_class: API Security
---

# Workflow runs · OWASP/wstg · GitHub

- URL: `https://github.com/OWASP/wstg/actions`
- Source group: `backfill_deep_content`
- Content chars: `7199`
- Classification: **technique**
- Vulnerability class: **API Security**

## Source summary

- No matching users. ⌥ + click/return to exclude Push on master CodeQL #81: by kingthorin 48s master master 48s Comment Comment #1789: completed by dependabot Bot 9s 9s View workflow file Bump actions/cache from 6.0.0 to 6.1.0 in the dependencies group Markdown Lint Check #861: Pull request #1437 opened by dependabot Bot 6s dependabot/github_actions/dependencies-d5b8684899 dependabot/github_actions/dependencies-d5b8684899 6s View #1437 View workflow file github_actions in /. - Update #1439826257 Dependabot Updates #454: by dependabot Bot 1m 11s master master 1m 11s Enhance REST API Testing Methodologies (Issue #492) (#1427) Deploy Latest WSTG Content to Web #447: Commit c4f1e27 pushed by kingthorin 28s master master 28s View workflow file Enhance REST API Testing Methodologies (Issue #492) (#1427) Deploy Latest Checklists #203: Commit c4f1e27 pushed by kingthorin 23s master master 23s View workflow file Push on master CodeQL #80: by kingthorin 49s master master 49s Comment Comment #1788: completed by kingthorin 10s 10s View workflow file Comment Comment #1787: completed by kingthorin 11s 11s View workflow file Comment Comment #1786: completed by kingthorin 11s 11s View workflow file Enhance REST API Testing Methodologies (Issue #492) Markdown Terminology Lint Check #1965: Pull request #1427 synchronize by kingthorin 31s PaarthPandey10:new-492 PaarthPandey10:new-492 31s View #1427 View workflow file Enhance REST API Testing Methodologies (Issue #492) Markdown Lint Check #2368: Pull request #1427 synchronize by kingthorin 28s PaarthPandey10:new-492 PaarthPandey10:new-492 28s View #1427 View workflow file Enhance REST API Testing Methodologies (Issue #492) Markdown Link Check #2432: Pull request #1427 synchronize by kingthorin 27s PaarthPandey10:new-492 PaarthPandey10:new-492 27s View #1427 View workflow file Comment Comment #1785: completed by rbsec 11s 11s View workflow file Comment Comment #1784: completed by rbsec 11s 11s View workflow file Comment Comment #1783: completed by rbsec 10s 10s View workflow file More small wording changes, tweaks and improvements Markdown Lint Check #2367: Pull request #1436 opened by rbsec 22s rbsec:more_misc_fixes rbsec:more_misc_fixes 22s View #1436
- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...
- Notifications You must be signed in to change notification settings Fork 1.6k Star 9.5k Code Issues 35 Pull requests 8 Actions Models Security and quality 0 Insights Additional navigation options Code Issues Pull requests Actions Models Security and quality Insights Actions: OWASP/wstg Actions All workflows Workflows Markdown Link Check Markdown Link Check Markdown Link Check (Full Repository) Markdown Link Check (Full Repository) Markdown Lint Check Markdown Lint Check Markdown Terminology Lint Check Markdown Terminology Lint Check Build Ebooks Build Ebooks CodeQL CodeQL Comment Comment Copilot cloud agent Copilot cloud agent Copilot code review Copilot code review Delete Old Workflow Runs Delete Old Workflow Runs Show more workflows...

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
