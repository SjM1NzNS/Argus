---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.050698+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# ASVS/.markdownlint.jsonc at master · OWASP/ASVS · GitHub

- URL: `https://github.com/OWASP/ASVS/blob/master/.markdownlint.jsonc`
- Source group: `backfill_deep_content`
- Content chars: `3624`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...
- Notifications You must be signed in to change notification settings Fork 815 Star 3.5k Code Issues 100 Pull requests 8 Discussions Actions Projects Models Wiki Security and quality 0 Insights Additional navigation options Code Issues Pull requests Discussions Actions Projects Models Wiki Security and quality Insights Files Expand file tree master Breadcrumbs ASVS / .markdownlint.jsonc Copy path Blame More file actions Blame More file actions Latest commit History History History 19 lines (16 loc) · 998 Bytes master Breadcrumbs ASVS / .markdownlint.jsonc Copy path Top File metadata and controls Code Blame 19 lines (16 loc) · 998 Bytes Raw Copy raw file Download raw file Open symbols panel Edit and raw actions 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 { // https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md "MD004" : { "style" : " asterisk " }, // ul-style "MD007" : { "indent" : " 4 " }, // ul-style "MD013" : false , // line-length "MD024" : { "allow_different_nesting" : true }, // no-duplicate-header "MD026" : { "punctuation" : " .,;: " }, // no-trailing-punctuation (allows !?) "MD033" : false , // no-inline-html "MD034" : false , // bare URLs "MD035" : { "style" : " --- " }, // hr-style "MD036" : { "punctuation" : " .,;:!。 " }, // no-emphasis-as-header "MD041" : false , // first-line-h1 "MD046" : { "style" : " fenced " } , // code-block-style "MD049" : { "style" : " underscore " }, // emphasis-style "MD050" : { "style" : " asterisk " } // strong-style } Footer Footer navigation Terms Privacy Security Status Community Docs Contact Manage cookies Do not share my personal information

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
