---
type: learning-source-summary
compiled_at: 2026-08-07T05:31:28.720629+00:00
source_quality: 5
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# The Axios supply chain attack used individually targeted social engineering

- URL: `https://simonwillison.net/2026/Apr/3/supply-chain-social-engineering/`
- Source group: `daily_deep_content`
- Content chars: `3177`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- Next: Anthropic's Project Glasswing - restricting Claude Mythos to security researchers - sounds necessary to me Previous: Highlights from my conversation about agentic engineering on Lenny's Podcast Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments.
- More recent articles One-shotting a Raccoon Heist game using Claude Fable 5 - 5th August 2026 New release of LLM adds support for reasoning traces, OpenAI Responses, server-side tools, and smarter logging - 4th August 2026 Stateless MCP has recaptured my interest (and inspired mcp-explorer and datasette-mcp) - 31st July 2026 This is The Axios supply chain attack used individually targeted social engineering by Simon Willison, posted on 3rd April 2026 .
- A RAT is a Remote Access Trojan—this was the software which stole the developer’s credentials which could then be used to publish the malicious package.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
