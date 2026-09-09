---
type: skill-reference
status: active
created: "2026-07-03"
---

# Pass C AI/LLM Taxonomy Promotion Pattern

Use this reference when repeating or repairing Pass C-style AI/LLM taxonomy/source promotion.

## Sources

- `Arcanum-Sec/arc_pi_taxonomy`
- `Arcanum-Sec/ai-sec-resources`

## Promotion rules

1. Fetch selected source files into `01 - Learning/Inbox/<run-label>/`; do not bulk import every resource or payload.
2. Treat the Arcanum Prompt Injection Taxonomy as a classification/routing system, not exploit proof.
3. Promote high-signal nodes into Argus playbooks: indirect input, supply-chain/RAG pipeline, MCP tool-definition injection, tool rug-pull, prompt worm/sleeper, rules-file backdoor, confused deputy, tool-call spoofing, retrieval ranking manipulation, tool squatting, sensitive-data exfiltration, and cross-tenant leakage.
4. Treat the AI Security Resource Hub as a watchlist/lab catalog; use self-hosted or explicitly authorized targets only.
5. Update source summary, system review note, AI/LLM playbook, Web2 index, evals, changelog, and no-placeholder verification.

## Reportability rule

Taxonomy codes (`PIT-*`) are secondary support. A reportable AI/LLM finding needs attacker-controlled source, model/tool ingestion path, account/tenant/role model, trace/tool evidence, positive and negative controls, concrete boundary impact, and cleanup state.
