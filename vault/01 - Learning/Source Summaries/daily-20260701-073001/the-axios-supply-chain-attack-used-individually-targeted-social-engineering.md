---
type: learning-source-summary
compiled_at: 2026-07-01T05:33:53.393023+00:00
source_quality: 5
classification: Web2 skill update
vulnerability_class: AI / LLM Security
---

# The Axios supply chain attack used individually targeted social engineering

- URL: `https://simonwillison.net/2026/Apr/3/supply-chain-social-engineering/`
- Source group: `daily_deep_content`
- Content chars: `3140`
- Classification: **Web2 skill update**
- Vulnerability class: **AI / LLM Security**

## Source summary

- More recent articles Have your agent record video demos of its work with shot-scraper video - 30th June 2026 Porting the Moebius 0.2B image inpainting model to run in the browser with Claude Code - 22nd June 2026 sqlite-utils 4.0rc1 adds migrations and nested transactions - 21st June 2026 This is The Axios supply chain attack used individually targeted social engineering by Simon Willison, posted on 3rd April 2026 .
- Next: Anthropic's Project Glasswing - restricting Claude Mythos to security researchers - sounds necessary to me Previous: Highlights from my conversation about agentic engineering on Lenny's Podcast Monthly briefing Sponsor me for $10/month and get a curated email digest of the month's most important LLM developments.
- A RAT is a Remote Access Trojan—this was the software which stole the developer’s credentials which could then be used to publish the malicious package.

## Extracted methodology

- Affected surface: Web/API/application surface
- Preconditions to verify: identify actor/tenant/object boundary, required role/session state, and whether the vulnerable action is read, write, delete, trigger, or value transfer.
- Minimal test method: reproduce with an owned/synthetic object first, then compare allowed vs disallowed actor/object pairs; preserve request deltas and response evidence.
- Evidence requirements: exact request/response pair, actor/object ownership proof, unauthorized impact, and negative controls showing the boundary should have blocked the action.
- False-positive gates: index/config/tool output is not proof; synthetic IDs only map behavior; severity needs demonstrated business/security impact.

## Compiler decision

- Use this as a patch proposal input, not a mature playbook edit, unless paired with eval coverage and changelog review.
