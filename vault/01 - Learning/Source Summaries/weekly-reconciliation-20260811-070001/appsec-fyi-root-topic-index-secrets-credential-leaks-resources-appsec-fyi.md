---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.051315+00:00
source_quality: 5
source_id: appsec-fyi-root-topic-index
source_role: discovery_index
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, evidence_requirement, reportability_criterion, hunting_methodology, tooling_procedure]
classification: Web2 skill update
vulnerability_class: API Security
---

# Secrets & Credential Leaks Resources | appsec.fyi

- URL: `https://appsec.fyi/secrets.html`
- Source ID / role / trust: `appsec-fyi-root-topic-index` / `discovery_index` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`https://appsec.fyi`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `web2_topic_indexes`
- Content chars: `195152`
- Classification: **Web2 skill update**
- Vulnerability class: **API Security**

## Source summary

- The research reproduced four attack techniques using documented REST API functionality, demonstrating the risk of credential theft and access to downstream systems without exploiting specific vulnerabilities like CVE-2025-68613. → thehackernews.com Related (3) Hunting Leaked PyPI Tokens: 62 Live, 125 Packages Exposed Securing Agentic AI Workflows in n8n: From Leaked API Keys to Encryption Key Compromise GitHub is Awash with Leaked AI Company Secrets 2026-08-05 NEW 2026 Credential Harvesting Explained: How Attackers Collect Secrets From Developer Machines beginner 12 min read Writeup on credential harvesting, detailing how attackers collect secrets from developer machines.
- The malware exfiltrates secrets to GitHub and attempts persistence by poisoning Claude and VS Code configuration files. → blog.gitguardian.com Related (3) The Worm That Keeps on Digging: TeamPCP Hits @antv in Latest Wave Supply Chain Campaign Targets SAP npm Packages with Credential-Stealing Malware Supply Chain Campaign Targets SAP npm Packages with Credential-Stealing Malware 2026-08-07 NEW 2026 Token Jacking: Cybercriminals Could Be Stealing Your AI Resources news 8 min read AI Library for mitigating AI token jacking, a technique where attackers steal API keys to illicitly access and resell AI processing power.
- Prevention requires secrets scanning in CI/CD pipelines, pre-commit hooks, environment-based secret injection, and credential rotation policies. ⚠ Recently Exploited (CISA KEV) All KEV → CVE-2024-28987 SolarWinds — Web Help Desk Hardcoded Credential added 2024-10-15 📖 Read the Secrets guide A long-form, source-cited deep dive synthesized from every resource below. → 📘 The comprehensive Secrets guide on chs.us A hand-written, in-depth practitioner guide — attacks, testing, and prevention. → Level: All Beginner Intermediate Advanced News & advisories Date Added Link Excerpt 2026-08-08 NEW 2026 tl;dv (Too Lazy; Didn't Validate): 181,874 Meetings Left Wide Open news 5 min read Tool for enumerating sensitive meeting data; exploits a lack of tenant isolation in tl;dv's Firestore database.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, evidence_requirement, reportability_criterion, hunting_methodology, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `true`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
