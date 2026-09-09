---
type: source-summary
source: https://github.com/JailbrokenAI/wallbreaker
reviewed: "2026-07-09"
status: lab-candidate
license: AGPL-3.0-or-later
---

# Wallbreaker AI/LLM lab candidate

## Decision

Do **not** install Wallbreaker into the active Google/authorized program hunt environment yet.

Save it as an AI/LLM lab candidate and mine selected methodology into Argus playbooks/evals. Only run it against a target when:

1. the program exposes an in-scope AI/LLM/MCP surface;
2. there is a harmless owned-account / owned-object test plan;
3. the goal is boundary impact, not generic content-policy bypass.

## What the source provides

Wallbreaker is a terminal AI red-team harness for LLM/model/agent testing. Its README describes:

- repeated validation rather than treating one compliant response as proof;
- autonomous attack loops such as PAIR/TAP, Crescendo, best-of-N, seed sweeps, and campaign ladders;
- prompt transform/obfuscation engines such as Parseltongue/P4RS3LT0NGV3;
- LLM judge support and reliability validation;
- MCP/tool integration and transform tooling.

## Argus promotion scope

Promote only concepts, not raw payload corpora or live attack automation:

- repeated validation and pass-rate reporting;
- attack-loop structure as a lab/eval workflow;
- prompt transform taxonomy with target-processing proof gates;
- MCP/tool attack ideas mapped to existing tool poisoning / rug-pull / spoofing classes;
- judge reliability pitfalls and human-final evidence gates.

## Handling rules

- Do not bulk import the repository.
- Do not install into active hunt venvs by default.
- Treat jailbreak/payload output as lab material until a target-specific boundary impact exists.
- Strip or avoid unsafe objectives when converting ideas into eval scenarios.
- Keep AGPL license implications in mind before modifying/embedding code.

## Reportability reminder

A Wallbreaker-discovered model response is reportable only if Argus evidence shows unauthorized data access, tool execution, cross-user/tenant effect, persistent poisoning, secret exposure, or another concrete target-app boundary break. Jailbreak-only output remains non-reportable or informational hardening.
