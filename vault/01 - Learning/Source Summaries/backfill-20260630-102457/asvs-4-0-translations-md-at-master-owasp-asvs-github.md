---
type: learning-source-summary
compiled_at: 2026-06-30T08:31:42.051260+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# ASVS/4.0/TRANSLATIONS.md at master · OWASP/ASVS · GitHub

- URL: `https://github.com/OWASP/ASVS/blob/master/4.0/TRANSLATIONS.md`
- Source group: `backfill_deep_content`
- Content chars: `4575`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Navigation Menu Platform AI CODE CREATION GitHub Copilot Write better code with AI GitHub Copilot app Direct agents from issue to merge MCP Registry New Integrate external tools DEVELOPER WORKFLOWS Actions Automate any workflow Codespaces Instant dev environments Issues Plan and track work Code Review Manage code changes APPLICATION SECURITY GitHub Advanced Security Find and fix vulnerabilities Code security Secure your code as you build Secret protection Stop leaks before they start EXPLORE Why GitHub Documentation Blog Changelog Marketplace View all features Solutions BY COMPANY SIZE Enterprises Small and medium teams Startups Nonprofits BY USE CASE App Modernization DevSecOps DevOps CI/CD View all use cases BY INDUSTRY Healthcare Financial services Manufacturing Government View all industries View all solutions Resources EXPLORE BY TOPIC AI Software Development DevOps Security View all topics EXPLORE BY TYPE Customer stories Events & webinars Ebooks & reports Business insights GitHub Skills SUPPORT & SERVICES Documentation Customer support Community forum Trust center Partners View all resources Open Source COMMUNITY GitHub Sponsors Fund open source developers PROGRAMS Security Lab Maintainer Community Accelerator GitHub Stars Archive Program REPOSITORIES Topics Trending Collections Enterprise ENTERPRISE SOLUTIONS Enterprise platform AI-powered developer platform AVAILABLE ADD-ONS GitHub Advanced Security Enterprise-grade security features Copilot for Business Enterprise-grade AI features Premium Support Enterprise-grade 24/7 support Pricing Search code, repositories, users, issues, pull requests...
- Notifications You must be signed in to change notification settings Fork 815 Star 3.5k Code Issues 100 Pull requests 8 Discussions Actions Projects Models Wiki Security and quality 0 Insights Additional navigation options Code Issues Pull requests Discussions Actions Projects Models Wiki Security and quality Insights Files Expand file tree master Breadcrumbs ASVS / 4.0 / TRANSLATIONS.md Copy path Blame More file actions Blame More file actions Latest commit History History History 20 lines (18 loc) · 4.54 KB master Breadcrumbs ASVS / 4.0 / TRANSLATIONS.md Copy path Top File metadata and controls Preview Code Blame 20 lines (18 loc) · 4.54 KB Raw Copy raw file Download raw file Edit and raw actions v4.x - Translations The following translations of versions v4.0.1-v4.0.3 were prepared: v4.0.3 OWASP Application Security Verification Standard 4.0.3 Spanish (PDF) and other formats . (Thanks to Carlos Allendes and Hans Herrera ) OWASP Application Security Verification Standard 4.0.3 Simplified Chinese (PDF) and other formats . (Thanks to Unc1e ) OWASP Application Security Verification Standard 4.0.3 Arabic (PDF) and other formats . (Thanks to Aref Shaheed and Mhd Ghassan Alhabash) OWASP Application Security Verification Standard 4.0.3 Russian (PDF) and other formats . (Thanks to Andrei Titov ) OWASP Application Security Verification Standard 4.0.3 French (PDF) and other formats . (Thanks to Cédric Lallier , Alexandre Joly , Sebastien Gioria , and Marc Aubry ) OWASP Application Security Verification Standard 4.0.3 German (PDF) and other formats . (Thanks to Jörg Brünner ) OWASP Application Security Verification Standard 4.0.3 Portuguese (PDF) and other formats . (Thanks to Cesar Kohl ) OWASP Application Security Verification Standard 4.0.3 Italian (PDF) and other formats . (Thanks to Riccardo Sirigu ) v4.0.2 OWASP Application Security Verification Standard 4.0.2 German (PDF) and Microsoft Word format . (Thanks to Jörg Brünner ) OWASP Application Security Verification Standard 4.0.2 Russian (PDF) and Microsoft Word format . (Thanks to Sergey Diakonov ) v4.0.1 OWASP Application Security Verification Standard 4.0.1 Persian (PDF) (Thanks to CERT of Ferdowsi University of Mashhad / Ardalan Foroughipour ) OWASP Application Security Verification Standard 4.0.1 Japanese (PDF) (Thanks to Software ISAC Japan / Riotaro OKADA ) OWASP Application Security Verification Standard 4.0.1 Turkish (PDF) (Thanks to Fatih ERSINADIM ) Footer Footer navigation Terms Privacy Security Status Community Docs Contact Manage cookies Do not share my personal information

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
