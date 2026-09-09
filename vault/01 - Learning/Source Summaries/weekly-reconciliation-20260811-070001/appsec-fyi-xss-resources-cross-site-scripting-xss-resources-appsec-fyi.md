---
type: learning-source-summary
compiled_at: 2026-08-11T05:03:52.021425+00:00
source_quality: 5
source_id: appsec-fyi-xss-resources
source_role: discovery_index
source_trust: discovery_only
promotion_policy: original_source_required
promotion_status: proposal_only
knowledge_types: [vulnerability_pattern, validation_technique, reportability_criterion, hunting_methodology, tooling_procedure]
classification: severity rule
vulnerability_class: Client-Side / XSS
---

# Cross-Site Scripting (XSS) Resources | appsec.fyi

- URL: `https://appsec.fyi/xss.html`
- Source ID / role / trust: `appsec-fyi-xss-resources` / `discovery_index` / `discovery_only`
- Acquisition provenance: cadence=`weekly`, method=`deep_link_discovery`, discovered-from=`direct root`
- Registry schema/digest: `2` / `cdfb32ac139b7826aa99b479fbf3ba207af5f2365d97942eaaf62f49e8bb643d`
- Source group: `web2_topic_indexes`
- Content chars: `289247`
- Classification: **severity rule**
- Vulnerability class: **Client-Side / XSS**

## Source summary

- The title suggests a practical, hands-on approach to security testing within web applications, emphasizing techniques for uncovering weaknesses accessible from the user's browser. → yeswehack.com Related (3) DOM XSS: What Is DOM-based Cross-Site Scripting And How can you Prevent it?
- From OWASP ⚠ Recently Exploited (CISA KEV) All KEV → CVE-2026-42897 Microsoft — Exchange Server Cross-Site Scripting added 2026-05-15 CVE-2025-48700 Synacor — Zimbra Collaboration Suite (ZCS) Cross-site Scripting added 2026-04-20 CVE-2025-66376 Synacor — Zimbra Collaboration Suite (ZCS) Cross-Site Scripting added 2026-03-18 📖 Read the XSS guide A long-form, source-cited deep dive synthesized from every resource below. → 📘 The comprehensive XSS guide on chs.us A hand-written, in-depth practitioner guide — attacks, testing, and prevention. → Level: All Beginner Intermediate Advanced News & advisories Date Added Link Excerpt 2026-08-09 NEW 2026 CVE-2026-64638: Critical Pre-Auth XSS Vulnerability in WordPress Allows Remote Code Execution news 4 min read Writeup of CVE-2026-64638, a critical pre-authentication reflected XSS vulnerability in WordPress versions up to 7.0.2.
- Reflected XSS executes via a crafted URL, Stored XSS persists in the application's database and fires for every visitor, and DOM-based XSS exploits client-side JavaScript that unsafely handles user input without any server round-trip.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Knowledge and promotion semantics

- Candidate knowledge types: `vulnerability_pattern, validation_technique, reportability_criterion, hunting_methodology, tooling_procedure`
- Promotion status: `proposal_only`; manual review required: `true`
- Original-source resolution required: `true`
- Independent corroboration: `required`
- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
