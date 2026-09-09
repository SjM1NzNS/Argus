---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.053873+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: File Upload / Media Processing
---

# ASVS/Makefile at master · OWASP/ASVS · GitHub

- URL: `https://github.com/OWASP/ASVS/blob/master/Makefile`
- Source group: `backfill_deep_content`
- Content chars: `4193`
- Classification: **Web2 skill update**
- Vulnerability class: **File Upload / Media Processing**

## Source summary

- Notifications You must be signed in to change notification settings Fork 815 Star 3.5k Code Issues 100 Pull requests 8 Discussions Actions Projects Models Wiki Security and quality 0 Insights Additional navigation options Code Issues Pull requests Discussions Actions Projects Models Wiki Security and quality Insights Files Expand file tree master Breadcrumbs ASVS / Makefile Copy path Blame More file actions Blame More file actions Latest commit History History History 19 lines (14 loc) · 1.19 KB master Breadcrumbs ASVS / Makefile Copy path Top File metadata and controls Code Blame 19 lines (14 loc) · 1.19 KB Raw Copy raw file Download raw file Open symbols panel Edit and raw actions 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 latest : 5.0 all : 5.0 4.0 4.0-LANGS := $( shell cd 4.0 && git status --porcelain | sed 's/[ A-Z?]\+ \"\?4.0\///g' | sed 's/\/. * //g' | sed -n '/^\(ar\|de\|en\|es\|fr\|pt\|ru\|zh-cn\) /p' | tr '\n' ' ') 5.0 : docker docker run --rm --user $( id -u ) : $( id -g ) -v " ` pwd ` /5.0:/data " -v " ` pwd ` /docker:/scripts " -e " TARGET=5.0 " -e " FORMATS= $( FORMATS ) " -e " LANGS= $( LANGS ) " ghcr.io/owasp/asvs/documentbuilder:latest 5.0-clean : docker docker run --rm --user $( id -u ) : $( id -g ) -v " ` pwd ` /5.0:/data " -v " ` pwd ` /docker:/scripts " -e " TARGET=clean " -e " FORMATS= $( FORMATS ) " -e " LANGS= $( LANGS ) " ghcr.io/owasp/asvs/documentbuilder:latest 4.0 : docker docker run --rm --user $( id -u ) : $( id -g ) -v " ` pwd ` /4.0:/data " -v " ` pwd ` /docker:/scripts " -e " TARGET=4.0 " -e " FORMATS= $( FORMATS ) " -e " LANGS= $( 4.0-LANGS ) " ghcr.io/owasp/asvs/documentbuilder:latest 4.0-clean : docker docker run --rm --user $( id -u ) : $( id -g ) -v " ` pwd ` /4.0:/data " -v " ` pwd ` /docker:/scripts " -e " TARGET=clean " -e " FORMATS= $( FORMATS ) " ghcr.io/owasp/asvs/documentbuilder:latest .PHONY : 5.0 5.0-clean 4.0 4.0-clean docker docker : docker pull ghcr.io/owasp/asvs/documentbuilder:latest || docker build --pull --tag ghcr.io/owasp/asvs/documentbuilder:latest --network host docker Footer Footer navigation Terms Privacy Security Status Community Docs Contact Manage cookies Do not share my personal information
- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...

## Extracted methodology

- Affected surface: File upload / media parser / async processing surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
