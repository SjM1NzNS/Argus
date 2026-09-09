---
type: source-summary
status: promoted
created: "2026-07-03"
pass: "C"
sources:
  - "https://github.com/Arcanum-Sec/arc_pi_taxonomy"
  - "https://github.com/Arcanum-Sec/ai-sec-resources"
---

# Pass C AI/LLM Taxonomy Source Summary

## Scope

Pass C reviewed Arcanum AI-security sources for Argus-safe promotion:

- Arcanum Prompt Injection Taxonomy v1.6.1: 172 nodes across intents, techniques, evasions, and inputs.
- AI Security Resource Hub: curated free/self-hostable labs, CTFs, tools, bug-bounty programs, and references for AI/LLM security.

Selected source files were stored under:

`01 - Learning/Inbox/manual-20260703-pass-c-ai-llm-taxonomy/`

## Promoted lessons

1. Classify AI/LLM findings by **input surface**, **technique**, **evasion**, and **intent** rather than using “prompt injection” as a single bucket.
2. Treat Prompt Injection Taxonomy codes as secondary support and routing labels, not proof.
3. High-value Argus branches are indirect input, RAG/corpus poisoning, MCP/tool poisoning, tool rug-pull, rules-file backdoors, confused deputy, tool-call spoofing, cross-tenant leakage, and sensitive-data exfiltration.
4. Evasion techniques such as Base64, bidi/Trojan Source, and ANSI concealment are test variants only when the target actually decodes/renders/ingests them.
5. Resource Hub entries are a watchlist/lab catalog; promote only self-hosted or authorized-lab lessons into active playbooks.

## Key taxonomy nodes promoted

| Code | Title | Argus use |
|---|---|---|
| PIT-N-06 | Indirect Input | External content → model context boundary. |
| PIT-N-11 | Supply Chain / Pipeline | RAG ingestion, plugin/package, model/tool pipeline poisoning. |
| PIT-N-12 | Sensor / Cross-Modal | Multimodal/physical input injection routing. |
| PIT-T-42 | Tool-Definition Injection | MCP/tool schema poisoning. |
| PIT-T-43 | Tool Rug Pull | Tool definition/behavior changes after approval. |
| PIT-T-44 | Conditional Trigger-Gated Payload | Sleeper payloads in RAG/memory/tool definitions. |
| PIT-T-45 | Prompt Worm | Self-replicating memory/RAG/agent injection. |
| PIT-T-46 | Agent Instruction-File Injection | `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, `copilot-instructions` backdoor risk. |
| PIT-T-47 | Confused Deputy | Agent/tool authority confusion. |
| PIT-T-53 | Tool-Call Spoofing | Forged tool result/observation blocks. |
| PIT-T-64 | Retrieval Ranking Manipulation | RAG poisoning / embedding/reranker abuse. |
| PIT-T-65 | Tool-Preference Manipulation | Tool squatting / selection bias. |
| PIT-T-69 | Agentic Compliance Momentum | Benign-prefix action-loop priming. |
| PIT-I-19 | Sensitive Data Exfiltration | Data/tool/memory exfil impact anchor. |
| PIT-I-27 | Cross-Tenant Data Leakage | Shared RAG/memory/session isolation impact anchor. |

## Promotion outputs

- `02 - Vulnerability Playbooks/Web2/AI & LLM Security/prompt-injection-taxonomy.md`
- `00 - System/external-ai-llm-taxonomy-source-review-2026-07-03.md`
- `06 - Evals/Web2/ai-llm-taxonomy-eval-scenarios.md`
- Web2 AI/LLM routing trigger expansion.
