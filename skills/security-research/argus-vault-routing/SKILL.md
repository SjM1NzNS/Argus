---
name: argus-vault-routing
description: Use when triaging Argus bug bounty targets, reviewing tool output, continuing hunts, or enriching the SecurityResearch vault; load Web2/Web3 vault skill indexes and route to the matching Obsidian playbooks before testing or reporting.
version: 1.2.2
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [argus, bug-bounty, obsidian, routing, playbooks, web2, web3]
    related_skills: [argus-securityresearch-workflows, obsidian]
---

# Argus Vault Routing

## Overview

Argus uses Obsidian notes as class-level bug bounty playbooks. This skill prevents missed coverage by requiring the active vault routing indexes to be checked whenever a target surface, tool output, hypothesis, or evidence gap appears.

This is a routing skill, not an exploit catalog. It tells the agent which vault notes to load next. The notes themselves live under `$HOME/SecurityResearch/02 - Vulnerability Playbooks/` and contain test checklists, evidence gates, reportability rules, false-positive filters, and eval scenarios.

## Core paths

- Vault root: `$HOME/SecurityResearch`
- Web2 index: `$HOME/SecurityResearch/00 - System/web2-skill-index.md`
- Web3 index: `$HOME/SecurityResearch/00 - System/web3-skill-index.md`
- Web2 playbooks: `$HOME/SecurityResearch/02 - Vulnerability Playbooks/Web2/`
- Web3 playbooks: `$HOME/SecurityResearch/02 - Vulnerability Playbooks/Web3/`
- Evals: `$HOME/SecurityResearch/06 - Evals/`
- Changelog: `$HOME/SecurityResearch/07 - Skill Changelog/YYYY-MM.md`

## When to Use

Load this skill when:

- continuing an Argus bug bounty target;
- processing scanner/tool output;
- deciding what playbook applies to a discovered surface;
- writing or reviewing a finding candidate;
- enriching vault notes or importing legacy methodology;
- a target mentions API, auth, OAuth, GraphQL, upload, storage, mobile, AI/LLM, CI/CD, Web3, smart contracts, or any specialized class in the indexes;
- unsure whether a lead is reportable, blocked, false positive, or needs more proof.

Do not use it as permission to run live recon or broad automation. Scope contract, target authorization, and approval queues still govern testing.

## Routing Workflow

1. **Classify the surface.** Extract concrete trigger terms from the current task or tool output: endpoint names, UI flows, file names, API technologies, cloud/storage words, mobile artifacts, smart-contract primitives, roles, IDs, signatures, or protocol concepts.

2. **Read the relevant index.**
   - Use Web2 index for web/API/mobile/cloud/AI/CI-CD findings.
   - Use Web3 index for smart contracts, on-chain protocols, signatures, bridges, AMMs, lending, governance, or OWASP smart-contract taxonomy.
   - Read both indexes when a surface crosses domains, such as a dApp frontend exposing API keys for smart-contract actions.

3. **Match all relevant trigger sections.** Do not stop at the first match if multiple classes apply. Example: an APK with Firebase config and deep links should route Mobile API, Secret Exposure, OAuth/SSO, and Cloud Storage as needed.

4. **Load the listed notes.** Read every `Load:` path for the matched section before testing or reporting. If the loaded note points to adjacent notes, follow the pointer when it changes evidence or reportability requirements.

5. **Apply evidence gates before action.** Use the loaded notes to decide whether the next step is safe local analysis, low-noise probing, approval-gated testing, owned-object replay, or branch-blocked pivoting.

6. **Update routing when gaps appear.** If a recurring trigger is missing, patch the appropriate index and changelog after adding or updating the corresponding playbook note.

Completion criterion: every material surface/hypothesis in the current task is mapped to at least one index section, or explicitly marked as having no current routing and queued as a gap.

## High-Signal Web2 Routing Clusters

Use `web2-skill-index.md` for these active clusters:

- Access Control / IDOR / BOLA / BFLA
- Authentication & Session
- OAuth / SSO
- GraphQL
- REST API / Business Logic
- HTTP Request Smuggling / Desynchronization, including CL.TE, TE.CL, TE.TE, H2.CL, H2.TE, HTTP/2 downgrade ambiguity, response-queue poisoning, and front-end/back-end framing disagreement
- AI / LLM Security, including MCP, RAG, vector stores, agent memory, tool manifests, plugin boundaries, excessive agency, and model/tool tokens
- XSS
- SSRF / Webhooks
- File Upload
- Cloud Storage, including S3/GCS/Azure, signed URLs, ACLs, upload policies, and object overwrite
- Secret Exposure, including CI logs, container layers, OIDC tokens, kubeconfigs, Terraform state, and package registry tokens
- CI/CD and Supply Chain, including GitHub Actions, GitLab CI, Jenkins, TeamCity, poisoned pipeline execution, OIDC trust, artifact signing, SBOM, dependency confusion, and mutable image tags
- Mobile API, including APK/IPA, AndroidManifest, exported components, app/universal links, URL schemes, WebViews, Keychain, ATS, network security config, Firebase config, and mobile local storage
- Rate Limits & Abuse
- Race Conditions / TOCTOU
- Attack Chains / Severity Escalation
- Tooling / Burp Workflow

## High-Signal Web3 Routing Clusters

Use `web3-skill-index.md` for these active clusters:

- ERC4626 / Vaults
- Lending
- AMM / DEX
- Bridges / Cross-chain Messaging
- Signatures / Permit / Replay
- Reentrancy
- External Calls / Unchecked Calls
- Flash Loans
- Upgradeability / Proxy, including UUPS, transparent proxy, beacon proxy, diamond/facet, reinitializer, proxy admin, storage gap, `proxiableUUID`, and implementation lock state
- Governance
- Oracle / Price Manipulation
- Access Control
- Input Validation
- Rounding & Precision
- OWASP Smart Contract Alignment, including SCSVS, SCSTG, SC01-SC10, and taxonomy/report mapping

## Reportability Discipline

Routing is only the first step. Before calling something a finding, require the loaded notes to answer:

- What is the exact actor model and scope relationship?
- What request, transaction, object, config, contract, artifact, or workflow proves the issue?
- What positive and negative controls were checked?
- What is the concrete impact: unauthorized data/action, account/tenant boundary break, code/artifact tamper, credential capability, protocol loss, insolvency, control change, freeze, or program-accepted impact?
- Which false-positive gates apply?
- What is the **incremental attacker capability** over documented configuration, intended actor authority, ordinary PR/account permissions, or supported ignore/filter controls? Run a counterfactual when the same actor may already produce the claimed outcome.
- Does a real consumer rely on the trusted distinction being corrupted, or is the distinction technically real but operationally ignored?
- Is the next validation step approval-gated, credentialed, destructive, or broad?

### Safe impact proof standard

For Argus bug bounty work, do **not** stop at speculative impact when a higher-fidelity safe proof is available. Prove the highest realistic impact with the minimum safe, non-destructive action, then stop:

- RCE/code execution proof may end at `whoami`, `id`, hostname, `pwd`, or a harmless marker file/output.
- Credential proof may use fake canaries, metadata-only identity/scope/expiry checks, key class/source, masked variable presence, or redacted prefix/suffix evidence.
- Data proof should prefer owned/canary records; if real sensitive data is unexpectedly exposed, record the smallest redacted proof needed and stop.
- Deployment/supply-chain proof should show attacker-controlled input reaching trusted build/deploy/artifact flow without shipping malicious artifacts to users or mutating production.
- Never dump full secrets, bulk collect data, persist access, destructively mutate production, or pivot beyond the validated boundary without explicit program permission and a scoped test plan.

See `references/safe-impact-proof-standard.md` for reusable examples and report wording.

For post-submission portal/reviewer transitions—including duplicate assignment, hidden canonical IDs, reward/credit disposition, appeal decisions, non-reframing, synchronized vault updates, and post-triage manifests—follow `references/program-triage-outcomes-and-canonical-differentiation.md`.

When a cohort of final outcomes raises a portfolio question—especially repeated duplicates, repeated `Infeasible` decisions, zero unique acceptances, or whether a newly verified challenger is “better than” the incumbent—follow `references/program-portfolio-calibration-from-triage-outcomes.md`. Diagnose novelty and threat-model failures separately; distinguish the best next bounded hunt from the best overall program and long-term payout ceiling; preserve pending incumbent follow-ups; then diversify at the program-selection layer while keeping execution source-first and deep. Do not respond to poor yield by shallow scanning, cosmetically reframing the same root causes, or claiming an entire private-invite batch is superior when only one brief is verified.

For live public-program comparison across Intigriti, YesWeHack, HackerOne, Bugcrowd, or similar platforms, follow `references/cross-platform-public-program-screening.md`. It defines platform-specific public data sources, recent-activity and saturation proxies, confidence penalties for unpublished metrics, competition-adjusted scoring, rejection logging, and the transition from a 3–5-per-platform shortlist to one or two source-first hunts. Never equate an all-time leaderboard, 90-day report count, managed-program label, or new directory listing with a live active-hunter count.

When a locally stored Intigriti Researcher API PAT is explicitly authorized for read-only all-program screening, also follow `references/intigriti-authenticated-program-inventory.md`. It covers secure PAT use, open/paid/VDP/CTF accounting, per-program detail and activity collection, persistent `403` brief gates, embedded brief-credential containment, BAC/API-first scoring, prior-shortlist reconciliation, sanitized `0600` artifacts, and deterministic no-secret/no-overclaim verification.

When the user pastes private/invitation-only program cards, follow `references/private-invite-inventory-and-selection.md`. Preserve displayed fields and incomplete rows without guessing, record a dated user-provided snapshot, keep card state/researcher access/local activation separate, and do not rank, initialize workspaces, or enable hunting unless explicitly requested. If an authenticated brief or researcher transcription arrives after provisional ranking, run the reference’s late-brief reconciliation: preserve exact scheme/host/path/tier and no-bounty labels, convert exclusions into route filters, distinguish source artifacts from owned controls, re-score access, propagate any changed winner, and keep hunting disabled pending a reviewed local contract.

When the user asks whether shortlisted or initialized programs “all have hunting enabled,” follow `references/live-program-hunting-status-verification.md`. Report platform submission state, researcher eligibility/access, and local Argus scope activation as three separate states; verify rendered submission controls/current platform APIs, timestamp the snapshot, and never bulk-enable draft scope contracts from an open-program result.

If these are not answered, keep the lead as a candidate or blocked branch rather than reporting.

## External RAG Assist

If local playbooks do not contain enough technique detail for a specific branch, use approved external RAG as a Zone 0 reference source, not as a testing instruction.

Current command:

```bash
argus-preview-rag "<target-independent technique query>" --save
```

Always read `00 - System/external-rag-source-policy.md` first. Returned writeups can suggest methods or false-positive checks, but the branch must still route back through this skill's Web2/Web3 indexes and survive evidence/validator gates.

## Cross-Domain Examples

- **Saved JS/source map/OpenAPI/HAR artifacts:** load the Web2 Source-First Artifact Mapping section and Hermes skill `argus-source-first-recon` before endpoint selection or evidence promotion. Parse locally, suppress candidate secret plaintext, reject fallback HTML as source maps, keep source-mentioned third-party hosts out of contact, and require a separate scope/actor/owned-data/request-budget plan for any replay.
- **WordPress/Elementor/plugin frontend with inline settings and REST contracts:** route Source-First Artifact Mapping, REST API/Business Logic, Access Control, XSS, and Secret Exposure together. Build executable closure from script tags, runtime chunks, and inline-config URLs; reduce literal `.js` parser artifacts locally; treat `/wp-json/` registration as contract metadata rather than anonymous authorization; redact nested nonces/IDs/client identifiers before contextual analysis; and require affected version + enabled feature + exact route/action/parameter sink before any CVE control. Prefer a parameterless read-only permission check and decline weak-impact reads that may expose user-entered suggestions or customer data.
- **SPA exposes a client API key:** route Secret Exposure, REST API, Cloud Storage, and Attack Chains; require no-key/wrong-key/client-key matrix and owned-object replay before report.
- **SPA exposes a public bearer upload-link flow:** route File Upload, Cloud Storage, REST API/Business Logic, Access Control, and Authentication/Session. Treat the public route and browser identifiers as intended until an owned-link positive control proves cross-link/object access, token weakness, upload-policy overreach, unintended public retrieval/execution, or unauthorized overwrite/modification. Do not enumerate link tokens or upload without a separate owned-object plan.
- **APK contains endpoints and Firebase config:** route Mobile API, Secret Exposure, REST API, OAuth/SSO, and Cloud Storage; treat APK as lead generation until live backend capability is proven.
- **GitHub Actions workflow uses OIDC:** route CI/CD Supply Chain and Secret Exposure; prove branch/workflow trust and identity/scope metadata without exfiltrating secrets.
- **PR approval/reviewer-bot lifecycle or branch-retarget finding:** route CI/CD Supply Chain, Race Conditions/TOCTOU, Business Logic, and Attack Chains together; load `references/ci-review-lifecycle-and-branch-protection-gates.md`. Compose event/activity/base filters with scheduled reviewer behavior, require review-to-head SHA binding, run the intended-untrusted-execution counterfactual, and keep production exploitability conditional until native rulesets and legacy branch protection are resolved. An unauthenticated `401` is an unresolved auth gate, never evidence that protection is absent. If an explicitly authorized read-only settings check still lacks repository-admin visibility, use bounded issue-event and targeted PR-history controls only as corroboration: attribute dismissals to the actual bot/app, preserve raw responses plus a deterministic manifest, and never treat zero observed `base_ref_changed` events as a negative configuration result.
- **LLM agent with tools and RAG:** route AI/LLM Security; also route Access Control, Secret Exposure, SSRF, or Cloud Storage if tool capabilities cross those boundaries.
- **External deep link or imported content can create/configure an autonomous agent:** route AI/LLM Security lifecycle integrity plus Authentication & Session, OAuth/SSO, Access Control, Attack Chains, and each affected connector class. Map draft → configuration → connector attachment → approval policy → real-tool Preview → publish/install → schedule/run → external instruction intake → egress/action → disable/revoke. Treat prior OAuth consent as ambient authority rather than current agent/run intent; require server-side transition evidence, owned canaries, and distinct confirmations. Do not copy credential-search, phishing, fraud, or persistence payloads from disclosures into live tests.
- **HTTP request-smuggling/desynchronization candidate:** route HTTP Request Smuggling, REST API/Business Logic, and Attack Chains; add Authentication & Session only when session/account impact is claimed. Bind the hypothesis to two real components and their exact framing semantics. A timeout, edge error, accepted ambiguous header, or scanner label is only a lead. Shared-production victim requests, response-queue probes, and repeated ambiguous traffic are approval-gated; prefer a direction-specific non-poisoning discriminator and local/owned/owner-coordinated second-message proof with exact wire bytes, connection reuse/order, backend parser evidence, unique canaries, and fresh-connection/patched controls.
- **Loopback developer/agent API:** route AI/LLM Security plus REST API/Business Logic, Authentication/Session, Access Control, and Attack Chains. For state-changing routes, inspect parser fallbacks for CORS-safelisted `text/plain`, test request integrity separately from response readability, and require a real-browser deterministic side effect. Tighten locally mapped cross-site evidence with a reproducible public-origin browser/version and `127.0.0.1`/`localhost`/`0.0.0.0` matrix when reachability affects reportability; queued Beacon acceptance is not delivery. Inspect omitted-identifier fallbacks and `stateDelta`: use an owned pre-existing default-session before/after control to prove or kill session/context injection. Disclose PNA/LNA, wire `Origin` versus active document origin, CSP/redirect controls, listener, Host validation, and DNS-rebinding proof limits. A missing ACAO header is not a CSRF defense. During report review, require a portable `text/plain` positive vs `application/json` preflight-negative control, distinguish PoC-authored model/tool choice from attacker-directed command choice, separate experimental/trusted-code capability from realistic prevalence, and keep the title on the unconditional invocation/session-integrity flaw unless a normal live/default RCE chain is proven.
- **Smart contract `.call` inside withdrawal:** route External Calls, Reentrancy, and Foundry PoC template; require executable state/invariant break.
- **Web3 report cites OWASP SC06:** route OWASP Alignment and External Calls; reject taxonomy-only claims without executable proof.

## Common Pitfalls

1. **First-match routing.** Many real findings span classes. Match every relevant index section before testing.
2. **Taxonomy-only reporting.** OWASP, MASVS, AI Top 10, or CI/CD category labels support reports but never replace impact proof.
3. **Lead-as-finding drift.** Public config, source maps, APK strings, workflow YAML, tool schemas, bucket names, or contract patterns are leads until capability/impact is proven.
4. **Unsafe validation.** Listing buckets, writing objects, invoking cloud APIs, uploading files, mutating accounts, publishing packages, or mainnet actions require scope/approval/owned-object plans. A mutation being “reversible” does not make it permitted: check whether the program prohibits the cleanup operation before creating the canary. UI cleanup has the same state semantics as the underlying DELETE/remove action. If cleanup is prohibited, seek a written waiver covering both mutation and restoration or keep the branch inconclusive.
5. **Stale routing.** If a pass creates a new playbook but does not update the index, future sessions can miss it. Patch the index and changelog immediately.
6. **Missing verification.** After index/playbook edits, verify every referenced file exists, is non-empty, and has no TODO/TBD placeholders.
7. **Generic fuzzy append anchors.** Large target logs repeat bullets such as `Evidence:` and `No action occurred.` Read the real tail and patch against unique section context; then reread both the tail and replaced block before hashing. Never let a fuzzy match silently move a triage event into an older hunt block.
8. **Production-service no-go becomes program no-go.** A source-valid vulnerability may be eligible through an OSS repository tier even when a named hosted deployment's route/configuration is unproven. Before final disposition, independently resolve repository/product program scope, hosted-service scope, technical impact, and deployed proof. Record separate verdicts and never use a live-service 404/429/custom login route to erase explicit OSS eligibility.
9. **Last-minute scope discovery is left only in chat.** When final routing changes after reports/manifests were written, patch every affected disposition table and mission index, then regenerate and verify report hashes. Do not finish with a correct verbal correction and stale artifacts.
10. **Published tier is presented as an irrevocable panel guarantee.** A live public scope file is the authoritative pre-submission basis, but a panel may later claim a different internal tier or identify a generated-list error. Capture a commit-pinned snapshot and rules excerpt before submission; say “the current published list classifies this as…” rather than promising eligibility. If the panel contradicts an exact record, follow `references/program-triage-outcomes-and-canonical-differentiation.md` for one factual correction instead of defensively rearguing the vulnerability.

## Verification Checklist

- [ ] Relevant Web2/Web3 index was read for the current surface.
- [ ] Every matched section's `Load:` paths were read before testing/reporting.
- [ ] Cross-domain surfaces were routed to all relevant classes.
- [ ] Evidence gates and false-positive filters from loaded notes were applied.
- [ ] Approval-gated actions were queued instead of run implicitly.
- [ ] Any missing trigger/playbook gap was documented or patched.
- [ ] For final program dispositions, technical validity, asset/repository eligibility, named production-deployment proof, program status, and reward/credit outcome were recorded separately; a production route/config no-go did not erase an explicit OSS/product scope entry, and canonical opacity was not filled with assumptions.
- [ ] Any late scope/routing correction was propagated into the mission README, report destination table, disposition artifact, and regenerated checksum manifest before closure.
- [ ] Post-triage active status surfaces were synchronized, stale waiting/submission states were checked, the actual hunt-log tail was reread, and a dedicated outcome manifest passed.
- [ ] For vault edits: index, playbook, eval/report, changelog, and no-TODO verification were completed.
