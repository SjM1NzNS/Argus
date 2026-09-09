# Legacy cybersecurity vault enrichment pattern — 2026-07

Use when the user drops old/past cybersecurity vaults into `~/Downloads` and asks Argus to harvest useful additions for the active `$HOME/SecurityResearch` workspace.

## What worked

1. Load the Argus workspace skill and Obsidian/filesystem workflow first.
2. Inventory candidate vaults locally before editing anything:
   - count markdown files and total bytes per downloaded vault;
   - identify top-level topic/source-material/methodology structure;
   - compare against active playbook directories under `02 - Vulnerability Playbooks`.
3. Prefer the newest/most structured legacy vault as the primary source, but keep older vaults as provenance.
4. Score candidates by class-level value, not by raw quantity:
   - operations/methodology notes;
   - attack-chain/reportability/evidence gates;
   - tooling workflow maps;
   - authoritative corpora with actionable methodology;
   - gaps in current playbooks.
5. Promote concise class-level lessons into active playbooks. Do **not** copy source-material mirrors wholesale.
6. Write a review note under `00 - System/legacy-vault-enrichment-review-YYYY-MM-DD.md` summarizing what was reviewed, promoted, deferred, and intentionally not promoted.
7. Add/patch a monthly changelog entry under `07 - Skill Changelog/YYYY-MM.md`.
8. Verify touched files are non-empty and contain no `TODO`/`TBD` placeholders.

## Promotion targets used successfully

- `02 - Vulnerability Playbooks/Web2/Attack Chains/overview.md` — cross-vulnerability escalation layer: XSS→ATO, open redirect→OAuth code theft, SSRF→metadata/cloud creds, upload→parser/storage/RCE impact, IDOR→ATO/workflow impact, JWT→privilege escalation, race/business logic chains.
- `10 - Tools/Burp Suite Extension Tooling.md` — tool-selection map for Auth Analyzer, Autorize/PwnFox, Param Miner, Collaborator Everywhere, InQL, Logger++, Turbo Intruder, BCheck/HAE, Hackvertor, SignSaboteur, AutoRepeater, YesWeCaido.
- `08 - Templates/reporting-evidence-template.md` — triage-friendly report skeleton with positive control, exploit/variant request, negative control, account/object model, impact, safety notes, and remediation.
- Existing Web2 checklists — patch compact evidence gates into Authentication & Session, XSS, SSRF, File Upload, GraphQL, REST API.
- `00 - System/web2-skill-index.md` — add routing for Attack Chains / Severity Escalation and Burp Tooling workflows.

## Good candidate categories for later passes

- AI/LLM/MCP: OWASP AI Testing Guide, AISVS, LLM Top 10, MCP Top 10; extract prompt disclosure, runtime exfiltration, plugin/tool boundary violations, excessive agency, MCP token/secret exposure, and confused-deputy reportability gates.
- Mobile: MASTG/MASVS, Hacker101, YesWeHack Android/iOS; extract APK/IPA workflow, WebView/App Transport/filesystem/inter-app communication, mobile OAuth/deep-link/token-storage evidence gates.
- Cloud/CI-CD: S3 permissions, pipeline secret exposure, artifact/package provenance, GitHub Actions/OIDC/cloud trust misconfiguration.
- Web3: OWASP Smart Contract Top 10/SCSVS/SCSTG alignment for flash-loan-facilitated attacks, unchecked external calls, proxy/upgradeability, input validation, and eval scenarios.

## Pitfalls

- Avoid noisy note dumps. A 4,000+ note legacy vault should produce a small number of active class-level upgrades plus a review note, not thousands of copied notes.
- `_Archive/` and source-material mirrors are provenance by default. Promote only specific methodology, evidence gates, false-positive filters, reportability rules, and eval ideas.
- Do not persist public API keys, tokens, credentials, or old secrets from legacy notes into active playbooks; redact if referenced.
- Do not create one-session skills for a single imported vault. Update the class-level Argus workflow skill and add a `references/` note if session detail matters.
