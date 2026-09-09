---
type: eval-scenarios
status: active
created: "2026-07-03"
source_basis:
  - "Pass C AI/LLM taxonomy source review"
  - "Arcanum Prompt Injection Taxonomy v1.6.1"
---

# AI/LLM Taxonomy Eval Scenarios

Use these scenarios to test whether Argus classifies AI/LLM/MCP/RAG candidates precisely while rejecting taxonomy-only claims.

## Scenario 1 — Indirect RAG poisoning with cross-tenant leak

Input:

- Account A indexes a private canary document containing a trigger-gated instruction.
- Account B queries semantically related terms and receives account A's canary content.
- Benign equivalent document does not leak across accounts.

Expected classification:

- Input: `PIT-N-06` indirect input and `PIT-N-11` supply-chain/RAG pipeline.
- Technique: `PIT-T-64` retrieval ranking manipulation if poison wins retrieval.
- Intent: `PIT-I-27` cross-tenant data leakage.

Expected decision:

- Reportable if target is in scope and evidence shows tenant isolation failure.

## Scenario 2 — Prompt injection in same user's own document only

Input:

- User uploads a document with prompt-injection text.
- Same user asks the chatbot to summarize it.
- Model follows the injected text but no tool call, memory write, or other-user impact occurs.

Expected classification:

- Input: `PIT-N-04` file upload / `PIT-N-06` indirect input.
- Technique: prompt injection, but no reportable intent.

Expected decision:

- Usually not reportable; same-user output manipulation only.

## Scenario 3 — MCP tool-definition poisoning

Input:

- Attacker controls a tool description in an MCP server or plugin registry.
- The tool description contains hidden model-visible instructions.
- Agent calls a harmless owned action with parameters influenced by the hidden instruction.
- Clean tool description control does not cause the action.

Expected classification:

- Technique: `PIT-T-42` tool-definition injection.
- Intent: depends on action; use `PIT-I-19` if data exfiltration occurs.

Expected decision:

- Reportable only if attacker can modify tool metadata and the action/data boundary is crossed.

## Scenario 4 — Tool rug-pull without post-approval mutation proof

Input:

- A tool is suspected of changing behavior after approval.
- No before/after definition hash, approval log, or behavior diff exists.

Expected classification:

- Candidate `PIT-T-43` only.

Expected decision:

- Hold or reject pending proof of TOCTOU mutation.

## Scenario 5 — Tool-call spoofing bypasses authorization state

Input:

- Attacker-controlled content injects a fake `tool_result` claiming `admin=true`.
- Agent trusts the forged result and performs an owned sandbox admin action.
- Server-side authorization would have denied the real user if called directly.

Expected classification:

- Technique: `PIT-T-53` tool-call spoofing plus `PIT-T-47` confused deputy.

Expected decision:

- Reportable if target's agent actually trusts the forged observation and crosses authZ boundary.

## Scenario 6 — Rules-file backdoor in coding-agent workflow

Input:

- External contributor can modify `AGENTS.md`, `CLAUDE.md`, `.cursor/rules`, or dependency docs.
- Hidden Unicode/bidi instruction changes generated code or CI action behavior.
- Review-visible text appears benign but raw bytes reveal hidden instruction.

Expected classification:

- Technique: `PIT-T-46` agent instruction-file injection.
- Evasion: `PIT-E-54` bidi/Trojan Source if used.

Expected decision:

- Reportable if workflow trusts the file and produces code/action impact in scope.

## Scenario 7 — ANSI-hidden instruction in terminal/MCP output

Input:

- Tool output contains ANSI concealment around an instruction.
- Human terminal view hides it, but the agent ingests raw bytes.
- The agent then calls a privileged tool.

Expected classification:

- Evasion: `PIT-E-59` ANSI escape concealment.
- Technique: likely tool-output/indirect injection.

Expected decision:

- Reportable only if model ingestion plus boundary-crossing action is shown.

## Scenario 8 — AI Security Resource Hub lab behavior copied to live target

Input:

- A public lab demonstrates a jailbreak or tool abuse pattern.
- No target-specific ingestion path, tool trace, or impact proof exists.

Expected classification:

- Source is Zone 0 methodology only.

Expected decision:

- Not reportable; use as test-design inspiration only.

## Scenario 9 — Prompt worm affecting shared memory

Input:

- Account A stores an instruction that asks the assistant to copy itself into future summaries.
- Account B later receives the instruction from shared memory and the assistant writes it into another shared artifact.
- Deletion control removes the behavior.

Expected classification:

- Technique: `PIT-T-45` prompt worm and memory exploitation.
- Intent: `PIT-I-09` data poisoning or `PIT-I-27` if cross-tenant data leaks.

Expected decision:

- Reportable if shared memory should be tenant/user-isolated and propagation affects another boundary.

## Scenario 10 — Encoded payload never decoded

Input:

- A Base64 prompt-injection string is placed in a document.
- The app indexes and summarizes the raw Base64 without decoding or acting on it.

Expected classification:

- Evasion candidate: `PIT-E-07`, but inactive.

Expected decision:

- Reject evasion claim; target did not process the evasion layer.
