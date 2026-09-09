---
type: source-summary
source:
  - https://labs.zenity.io/p/agentforger-part-1-chatgpt-cross-site-agent-forgery
  - https://labs.zenity.io/p/agentforger-part-2-the-autonomous-insider
reviewed: "2026-07-23"
status: promoted
---

# Zenity AgentForger Parts 1–2 — source summary

## Sources

- *AgentForger, Part 1: ChatGPT Cross-Site Agent Forgery* — Mike Takahashi, 2026-07-23.
- *AgentForger, Part 2: The Autonomous Insider* — Mike Takahashi, 2026-07-23.
- Both live pages were reviewed directly on 2026-07-23.
- Preserved HTML:
  - `01 - Learning/Inbox/manual-agentforger-20260723/agentforger-part-1.html`
  - `01 - Learning/Inbox/manual-agentforger-20260723/agentforger-part-2.html`

## Root-cause lessons

1. Agent builders are security-sensitive state machines, not ordinary chat interfaces. Creation, configuration, connector attachment, approval policy, preview, publication, scheduling, execution, and revocation each need current-intent and authorization controls.
2. Externally supplied URL/deep-link initialization must remain inert draft data. Auto-submission inside an authenticated session can turn a navigation into a multi-step delegated-authority forgery.
3. Natural-language instructions must not control their own security policy. Approval downgrades, connector scope, publishing, preview execution, and scheduling require independent server-side enforcement and explicit user gestures.
4. Previous OAuth consent is ambient authority, not evidence that the user intends a new agent, new schedule, or new recipient to use it.
5. Preview is a security boundary when it invokes real tools. “Test” labels do not make downstream actions harmless or non-production.
6. Scheduling changes a one-click primitive into persistence. Disable/delete/revoke must terminate future and queued authority and be visible in inventory/audit.
7. Email, messages, documents, webpages, tickets, tool results, and RAG are data—not authenticated command channels. Sender/content filters cannot replace structured authorization.
8. Blast radius is compositional: cross-connector aggregation, victim-identity writes, external egress, and unattended repetition can exceed each connector's apparent individual risk.

## Safe handling decision

Promoted lifecycle integrity, safe-proof, mitigation, false-positive, evidence, routing, attack-chain, and eval methodology. Did **not** copy or operationalize the articles' credential-search, sensitive-data collection, phishing, fraud, external-command-loop, or high-frequency scheduling instructions. No OpenAI/ChatGPT account, connector, victim, or target was tested.

## Preview.is corroboration

Lookup returned five matches scoring `0.9356–0.9857`. High-signal corroboration included confused-deputy OAuth reuse, short-lived scope-bound agent tokens, independent tool authorization, and treating indirect content as an autonomous-workflow risk:

- https://towardsdatascience.com/the-mcp-security-survival-guide-best-practices-pitfalls-and-real-world-lessons/
- https://stytch.com/blog/mcp-vulnerabilities/
- https://www.penligent.ai/hackinglabs/claude-code-sandbox-bypass/
- https://nhimg.org/faq/why-is-indirect-prompt-injection-harder-than-xss/
- https://www.forcepoint.com/blog/x-labs/indirect-prompt-injection-payloads

These are Zone 0 corroboration only, not proof or instructions for live testing.
