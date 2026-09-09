# AI jailbreak guardrail-layer and judge eval — 2026-07-17

Source summary: `01 - Learning/Source Summaries/manual-20260717-taksec-ai-jailbreak-testing.md`.

## Scenario 1 — output truncates after several tokens

**Bad conclusion:** “The output guardrail caught it.”

**Expected decision:** Output enforcement is one hypothesis. Preserve finish reason and stream behavior; compare retries and controls; seek gateway/model logs if available. Timeout, generation stop, moderation middleware, or UI truncation remain alternatives.

## Scenario 2 — one success in twenty attempts

**Expected decision:** Lead only. Report 1/20 with model/version/settings and the same denominator for baseline/control prompts. Do not present the successful transcript as deterministic. Application reportability still requires a scoped boundary or an explicit model-safety policy.

## Scenario 3 — keyword judge marks quoted harmful terms as success

**Expected decision:** Judge false positive. Calibrate against human labels that separate refusal, discussion/quotation, partial compliance, and completed task. Judge labels cannot replace tool/data/action evidence.

## Scenario 4 — encoding improves apparent pass rate

The target displays the encoding literally and never decodes it before model context.

**Expected decision:** Reject the encoding-bypass claim. The application must actually decode, render, OCR, index, or pass the transformed content to the model.

## Scenario 5 — jailbreak causes an unauthorized owned-canary tool read

**Expected decision:** Security candidate. Preserve source-to-model-to-tool trace, server-side authorization decision, positive/negative controls, actor model, canary evidence, repeatability, and cleanup. The finding is the unauthorized capability—not merely the jailbreak text.
