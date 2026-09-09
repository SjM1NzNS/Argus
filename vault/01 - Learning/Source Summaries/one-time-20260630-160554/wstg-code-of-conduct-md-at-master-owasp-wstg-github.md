---
type: learning-source-summary
compiled_at: 2026-06-30T14:09:49.107439+00:00
source_quality: 8
classification: Web2 skill update
vulnerability_class: File Upload / Media Processing
---

# wstg/CODE_OF_CONDUCT.md at master · OWASP/wstg · GitHub

- URL: `https://github.com/OWASP/wstg/blob/master/CODE_OF_CONDUCT.md`
- Source group: `backfill_deep_content`
- Content chars: `5949`
- Classification: **Web2 skill update**
- Vulnerability class: **File Upload / Media Processing**

## Source summary

- Notifications You must be signed in to change notification settings Fork 1.6k Star 9.5k Code Issues 34 Pull requests 7 Actions Models Security and quality 0 Insights Additional navigation options Code Issues Pull requests Actions Models Security and quality Insights Files Expand file tree master Breadcrumbs wstg / CODE_OF_CONDUCT.md Copy path Blame More file actions Blame More file actions Latest commit History History History 75 lines (56 loc) · 3.32 KB master Breadcrumbs wstg / CODE_OF_CONDUCT.md Copy path Top File metadata and controls Preview Code Blame 75 lines (56 loc) · 3.32 KB Raw Copy raw file Download raw file Outline Edit and raw actions Contributor Covenant Code of Conduct Our Pledge In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to make participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.
- Our Standards Examples of behavior that contributes to creating a positive environment include: Using welcoming and inclusive language Being respectful of differing viewpoints and experiences Gracefully accepting constructive criticism Focusing on what is best for the community Showing empathy towards other community members Examples of unacceptable behavior by participants include: The use of sexualized language or imagery and unwelcome sexual attention or advances Trolling, insulting/derogatory comments, and personal or political attacks Public or private harassment Publishing others' private information, such as a physical or electronic address, without explicit permission Other conduct which could reasonably be considered inappropriate in a professional setting Our Responsibilities Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.
- Examples of representing a project or community include using an official project email address, posting via an official social media account, or acting as an appointed representative at an online or offline event.

## Extracted methodology

- Affected surface: File upload / media parser / async processing surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
