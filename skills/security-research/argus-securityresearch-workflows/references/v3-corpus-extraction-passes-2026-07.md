# V3 corpus extraction passes — 2026-07

Session pattern for processing old `Cybersecurity - V3` vault material into the active Argus SecurityResearch vault.

## Trigger

Use when the user asks to process legacy `Cybersecurity - V3` corpus extraction passes, especially “starting with 1 until 4 in turns” after a legacy-vault enrichment review.

## Core rule

Do **not** wholesale import source mirrors. Promote concise class-level methodology, evidence gates, false-positive filters, reportability rules, routing/index updates, eval scenarios, changelog entries, and pass reports.

Target shape:

- Active playbooks under `~/SecurityResearch/02 - Vulnerability Playbooks/...`.
- Pass reports under `~/SecurityResearch/00 - System/v3-corpus-extraction-pass-N-<topic>-YYYY-MM-DD.md`.
- Eval scenarios under `~/SecurityResearch/06 - Evals/...`.
- Changelog entries under `~/SecurityResearch/07 - Skill Changelog/YYYY-MM.md`.
- Routing updates in `00 - System/web2-skill-index.md` or `00 - System/web3-skill-index.md`.

## Per-pass workflow

1. Load `obsidian` and `argus-securityresearch-workflows`.
2. Inventory current active target playbook files and relevant V3 source files.
3. Read representative/high-value V3 source notes rather than every mirror file.
4. Create or patch class-level active notes only.
5. Update the relevant skill index when routing changes.
6. Add eval scenarios for new gates.
7. Write a pass report.
8. Update the monthly changelog.
9. Verify touched files are non-empty and contain no `TODO`/`TBD` placeholders.

## Pass 1 — AI / LLM / MCP

Source root:

```text
~/Downloads/Cybersecurity - V3/Topics/AI LLM and MCP/
```

Target active area:

```text
~/SecurityResearch/02 - Vulnerability Playbooks/Web2/AI & LLM Security/
```

Completed output pattern from 2026-07-02:

- Added `mcp-security.md`.
- Added `rag-vector-memory.md`.
- Added `reportability.md`.
- Patched `overview.md`, `test-checklist.md`, `evidence-requirements.md`, `false-positives.md`.
- Added evals: `06 - Evals/Web2/ai-llm-mcp-v3-pass1-eval-scenarios.md`.
- Wrote report: `00 - System/v3-corpus-extraction-pass-1-ai-llm-mcp-2026-07-02.md`.
- Updated Web2 skill-index routing for MCP, RAG/vector, agent memory, tool manifests, plugin boundaries, excessive agency, model/tool tokens.

Key lessons to preserve:

- Report only concrete boundary breaks, not jailbreak text.
- Use owned canaries and benign control documents.
- Redact secrets and avoid real exfiltration payloads.
- Test MCP token/scope/authZ/schema/tool-poisoning boundaries.
- Treat public schemas/tool lists/config as non-findings without capability or sensitive disclosure.

## Pass 2 — Mobile

Source root:

```text
~/Downloads/Cybersecurity - V3/Topics/Mobile/
```

Target active area:

```text
~/SecurityResearch/02 - Vulnerability Playbooks/Web2/Mobile API/
```

Completed output pattern from 2026-07-02:

- Added `android-static-recon.md`.
- Added `ios-platform-testing.md`.
- Added `reportability.md`.
- Patched `overview.md`, `test-checklist.md`, `evidence-requirements.md`, `false-positives.md`.
- Added evals: `06 - Evals/Web2/mobile-api-v3-pass2-eval-scenarios.md`.
- Wrote report: `00 - System/v3-corpus-extraction-pass-2-mobile-2026-07-02.md`.
- Updated Web2 skill-index routing for APK/IPA, split APK, AndroidManifest, exported components, deep/app/universal links, URL schemes, WebView, Keychain, ATS, network-security config, Firebase config, and local mobile storage.

Key lessons to preserve:

- Mobile artifacts are usually lead-generation, not findings.
- Record APK/IPA provenance, package/bundle ID, version, source, split components, architecture, and hash.
- Android: map manifest, exported components, permissions, intent filters, network security config, backup/debug flags, native libraries, endpoints, cloud identifiers, and hardcoded values before live traffic.
- iOS: inspect `Info.plist`, entitlements, associated domains, URL schemes, universal links, ATS exceptions, Keychain/local storage, WebViews, and pasteboard/backup/log artifacts.
- Certificate pinning/jailbreak/root bypass is testing instrumentation unless it changes server-side authZ or reveals sensitive local data.
- Embedded mobile/cloud keys require no-key / wrong-key / embedded-key matrices and owned-object capability proof.

## Pass 3 — Cloud / CI-CD / Infrastructure

Source root:

```text
~/Downloads/Cybersecurity - V3/Topics/Cloud CI-CD and Infrastructure/
```

Target active areas:

```text
~/SecurityResearch/02 - Vulnerability Playbooks/Web2/Cloud Storage/
~/SecurityResearch/02 - Vulnerability Playbooks/Web2/Secret Exposure/
~/SecurityResearch/02 - Vulnerability Playbooks/Web2/CI-CD & Supply Chain/
```

Completed output pattern from 2026-07-02:

- Added `Cloud Storage/s3-permission-matrix.md`.
- Added `CI-CD & Supply Chain/overview.md`.
- Added `CI-CD & Supply Chain/artifact-dependency-provenance.md`.
- Patched `Cloud Storage/overview.md` and `Cloud Storage/test-checklist.md`.
- Patched `Secret Exposure/overview.md` and `Secret Exposure/evidence-requirements.md`.
- Added evals: `06 - Evals/Web2/cloud-cicd-v3-pass3-eval-scenarios.md`.
- Wrote report: `00 - System/v3-corpus-extraction-pass-3-cloud-cicd-infra-2026-07-02.md`.
- Updated Web2 skill-index routing for S3/GCS/Azure storage, ACLs, object overwrite, CI logs/variables/artifacts, container layers, deploy keys, service accounts, kubeconfigs, Terraform state, OIDC tokens, and CI/CD supply-chain triggers.

Key lessons to preserve:

- Use a capability-first cloud storage matrix: read, list, write, overwrite, delete, `READ_ACP`, `WRITE_ACP`, `FULL_CONTROL`, signed URL bypass, upload policy abuse.
- Start with low-impact `HEAD`/metadata and public/owned reads. Queue approval before listing, writing, deleting, private-object access, or ACL/policy modification.
- Treat served JS/asset overwrite as a supply-chain impact path only with an owned/approved test path and cleanup proof.
- CI/CD findings require a trust-boundary break: PR/fork code to privileged workflow, mutable script to secrets, OIDC to cloud role, artifact to deployment, or dependency to build execution.
- For secrets, preserve exposure context and use offline format/provider checks first; prefer identity/scope/expiry metadata for safe validation and never store full secrets.
- For dependency confusion, do not publish malicious packages. Use harmless reservation/proof package only if allowed, or document claimability plus target consumption path.
- Missing artifact signing, public workflow YAML, or unpinned dependencies are not reportable without attacker modification/consumption path.

## Pass 4 — Web3 OWASP alignment

Source root:

```text
~/Downloads/Cybersecurity - V3/Topics/Web3 and Smart Contracts/
```

Target active area:

```text
~/SecurityResearch/02 - Vulnerability Playbooks/Web3/
```

Completed output pattern from 2026-07-02:

- Added `OWASP Alignment/scsvs-scstg-top10-map.md`.
- Added `Flash Loans/attack-patterns.md`.
- Added `External Calls/unchecked-external-calls.md`.
- Added `Input Validation/attack-patterns.md`.
- Patched `Upgradeability/attack-patterns.md`, `Reentrancy/attack-patterns.md`, and `Reporting/reportability.md`.
- Added evals: `06 - Evals/Web3/web3-owasp-v3-pass4-eval-scenarios.md`.
- Wrote report: `00 - System/v3-corpus-extraction-pass-4-web3-owasp-2026-07-02.md`.
- Updated `00 - System/web3-skill-index.md` routing for External Calls, Flash Loans, Input Validation, OWASP Alignment, and expanded proxy/upgradeability triggers.

Key lessons to preserve:

- OWASP labels are secondary support only; require executable proof, realistic state, invariant break, and quantified value/control/freeze impact.
- Flash loans are amplifiers, not standalone vulnerabilities; route them through the broken primitive (oracle, voting, share accounting, liquidation, composability).
- Low-level calls, delegatecall, ERC token return quirks, hooks/callbacks, and configurable callees need failure/callback mocks plus before/after state evidence.
- Proxy findings require proxy-impact proof: unauthorized upgrade/init, storage corruption, implementation lock failure with proxy effect, or governance/timelock bypass.
- Input-validation findings require invariant/economic/control impact; accepting weird values alone is not enough.

## Pass 5 — next-corpus selection

No fixed source root was established in this session. Before running Pass 5, inventory remaining `~/Downloads/Cybersecurity - V3/Topics/` folders and choose the highest-value active-vault gap rather than assuming the next folder alphabetically.

Suggested selection workflow:

1. List remaining V3 topic folders and active playbook coverage.
2. Exclude already-processed families: AI/LLM/MCP, Mobile, Cloud/CI-CD/Infrastructure, Web3.
3. Prefer topics that fill missing active-vault routing/evidence/reportability gaps.
4. Write the selected source root and target active area into the pass report.

## Ambiguous pass-order handling

If the user gives conflicting pass instructions in one message (for example, “Proceed with pass 5” and “Proceed with pass 4”), execute the latest explicit pass if it is also the planned next incomplete pass; note the ambiguity in the pass report/final response.

## Pitfalls

- Do not store secrets, tokens, payloads intended to exfiltrate real secrets, or raw source dumps in active notes.
- Do not treat public config/schema/tool lists as findings without capability or sensitive disclosure.
- Do not turn model-safety issues into bug-bounty findings unless they cross a target-specific data/action/authorization boundary or the program explicitly accepts that class.
- Do not collapse mobile app testing into only API testing if source material covers APK/IPA, storage, deep links, WebViews, pinning, and platform IPC.
- Do not make destructive cloud/CI/CD tests default steps. Keep dangerous list/write/delete/ACL/resource-enumeration actions approval-gated.
