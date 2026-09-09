---
type: source-summary
status: promoted
created: "2026-07-03"
sources:
  - "https://github.com/trailofbits/skills"
  - "https://github.com/trailofbits/claude-code-config"
  - "https://github.com/shuvonsec/claude-bug-bounty"
  - "https://github.com/SnailSploit/Claude-Red"
run_label: "manual-20260703-pass-a-agent-skill-mining"
---

# Pass A — Agent-skill source summary

## Scope

Reviewed selected high-signal files from four agent-skill/config repositories. Raw selected source files are preserved under:

```text
01 - Learning/Inbox/manual-20260703-pass-a-agent-skill-mining/
```

This was **not** a bulk import. The review promoted only Argus-safe methodology: validation gates, source-to-impact chain discipline, AI-agent workflow risk models, context-building requirements, and reportability checks.

## Source takeaways

### Trail of Bits skills

Promoted lessons:

- GitHub Actions workflows that invoke AI coding agents are a CI/CD sub-class needing explicit workflow review.
- Static review must trace attacker-controlled GitHub event fields through `env:` intermediaries, prompt fields, CLI data-fetch commands, PR-target checkout paths, logs, and eval/exec of AI output.
- Dangerous sandbox/tool configs (`danger-full-access`, unsafe safety strategy, `--yolo`, broad `Bash(*)`) are amplifiers, not always standalone findings.
- Wildcard user/bot allowlists amplify exposure when combined with external triggers and tainted prompts.
- Audit-context quality improves when every claim is tied to file/line evidence, all caller/callee assumptions are tracked, and unresolved assumptions are explicit.

### Trail of Bits claude-code-config

Promoted lessons:

- Agent configs should be inventoried before changes: permissions, hooks, MCP servers, statusline/telemetry, commands, and local policy files.
- PR/review workflows benefit from multiple passes: local context, external second opinion when tools exist, sandbox warnings, and explicit skip reporting when an optional tool is unavailable.
- MCP templates are useful only when secrets remain in environment/config stores, not notes or prompts.

### shuvonsec/claude-bug-bounty

Promoted lessons:

- A finding candidate should pass a short go/no-go gate before report drafting.
- Weak primitives are killed unless they have a concrete chain: e.g. open redirect without OAuth/code impact, DNS-only SSRF, GraphQL introspection alone, self-XSS, or missing headers.
- AuthZ candidates require cross-identity proof: session A reaches session B data/action; fresh sessions reproduce; anonymous/authenticated behavior differs.
- Chaining should start only after primitive A is confirmed by exact request/response, then test sibling endpoints and adjacent mechanisms.

### SnailSploit Claude-Red

Promoted lessons:

- Web vuln skills are useful as method inventories but must be safety-filtered into evidence gates and safe proof patterns.
- High-signal classes for Argus already map to existing playbooks: IDOR/BOLA, GraphQL, file upload, business logic, race conditions, OAuth, AI security, reporting, and fast triage.
- Do not import red-team infrastructure/evasion material into active bug-bounty routing.

## Promoted Argus updates

- New playbook: `02 - Vulnerability Playbooks/Web2/CI-CD & Supply Chain/agentic-ai-actions.md`.
- Updated CI/CD index triggers for agentic GitHub Actions / Codex / Claude Code / Gemini CLI / wildcard allowlists / unsafe sandboxes.
- Strengthened `00 - System/evidence-and-reportability.md` with a compact 7-question pre-report gate.
- Strengthened `00 - System/autopilot.md` with Pass A kill/continue heuristics for weak findings and chain seeds.
- Strengthened `argus-securityresearch-workflows` to point future sessions at Pass A source-review behavior.

## Do not promote

Do not import wholesale:

- EDR evasion, keylogger, shellcode, initial-access, or unrestricted red-team operator skills.
- Payload lists without target context, owned proof, or reportability gates.
- Autonomous scanning defaults that skip scope, approval, logs, or adversarial validation.
