---
type: source-summary
source: "https://josephthacker.com/hacking/2026/07/01/we-built-a-hackbot.html"
fetched_at: "2026-07-03"
tags:
  - bug-bounty
  - autonomous-agents
  - argus
  - validation
  - observability
  - authenticated-testing
---

# Joseph Thacker — The Bug Bounty Singularity: Our Hackbot

## Why this matters to Argus

The article is directly relevant to Argus's operating model: AI-assisted bug bounty work becomes useful only when agents have **observability**, **persistent follow-through**, **adversarial validation**, and **stable authenticated session handling**. The article's strongest lessons match Argus's current direction, but they sharpen several system policies.

## Source facts extracted

- The authors describe a hackbot that found 126 bugs over five months.
- They report an early failure mode: polished AI-generated reports with high false-positive rates.
- Their first major fix was full logging of commands, requests, conclusions, and reasoning so humans could inspect what the agent actually did.
- Their second fix was persistence: long-running loops that turn weak signals into follow-up branches instead of stopping after a first plausible answer.
- They later added an orchestrator to cut losses on thin targets while pushing workers to continue on rich targets.
- Their third fix was a dedicated validator whose goal is to disprove findings, not confirm them.
- Their fourth fix was moving login/session maintenance to a real browser/profile on a real machine; cloud/headless agents stopped spending most of the budget on auth challenges and consumed live sessions instead.
- Their bug examples emphasize patterns Argus already prioritizes: post-auth IDOR/BOLA, unauthenticated APIs, OAuth/MCP scope issues, exposed client config/API keys with real capability, Firebase/Firestore anonymous auth, public JS/source-map route discovery, GraphQL guest exposure, stored XSS with realistic victim navigation, and chains from info leak to write/admin impact.

## Argus lessons promoted

1. **Observability is a first-class security control.** Every autonomous or semi-autonomous hunt branch should preserve enough command/request/decision logs to reconstruct why a lead was accepted, discarded, or blocked.
2. **Persistence needs an orchestrator.** Do not stop after first plausible failure on rich surfaces; do not burn tokens indefinitely on thin targets. Use branch quality, impact potential, and evidence yield as stop/continue criteria.
3. **Every candidate needs an adversary.** Keep Skeptic/Impact review mandatory. For autonomous output, the validator should actively try to kill the finding and identify strongest downgrade/invalidity arguments.
4. **Authenticated context is high ROI but must be disciplined.** Stable session handling should use real browser/profile workflows and one-account-at-a-time OTP/session discipline, while cloud/headless workers consume scoped session context rather than repeatedly fighting login pages.
5. **Bugs are often chains.** Treat weak primitives as possible chain seeds only when they lead to a realistic second system/action: IDOR→write/admin, config leak→signup/domain control, API key→capability, XSS→wallet/account action, OAuth/MCP scope mismatch→unauthorized action.

## Do-not-promote notes

- Do not import or reproduce exploit payloads against named third-party targets.
- Do not treat the reported bug counts or severity distribution as a target benchmark for Argus.
- Do not turn this into broad/noisy automation. The useful lesson is structured, observable, validated, scope-aware persistence.
- Do not fight anti-bot login systems. Use user-assisted or real-browser session handling within scope and account rules.

## Promoted changes

- Created `00 - System/autonomous-hackbot-lessons-2026-07.md`.
- Patched `00 - System/autopilot.md` with observability, orchestrated persistence, and real-browser session rules.
- Patched `00 - System/evidence-and-reportability.md` with adversarial validator requirements for autonomous/model-generated candidates.
- Added eval scenarios under `06 - Evals/Web2/autonomous-hackbot-ops-eval-scenarios.md`.
