---
name: ai-security-research-cascade
description: Design controlled AI security research cascades.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [SecurityResearch, AI, Evaluation, Falsification]
---

# Controlled AI Security Research Cascades

This skill turns the methodology in [James Kettle's HTTP Terminator research](https://portswigger.net/research/can-ai-do-novel-security-research) into a reusable, controlled research loop. It does not authorize target testing, provide exploit payloads, or treat model output as evidence. It depends on expert review, deterministic evaluation, explicit authorization, isolated tooling, and preserved discovery lineage.

## When to Use

- “Design an AI-assisted security research program.”
- “Build a hypothesis-generation and evaluation loop.”
- “Use RFCs, advisories, or source material as research inspiration.”
- “Test whether an AI can rediscover or invent a technique.”
- “Turn anomalies into a structured discovery cascade.”
- “Reduce false positives in autonomous security research.”
- “Decide what belongs to AI, deterministic code, or a human.”
- “Validate novelty without confusing rediscovery with invention.”

## Prerequisites

- No package installation is required for the methodology itself.
- No credentials are required for local fixtures, static review, or hypothesis generation.
- Live evaluation requires explicit written authorization, an exact scope boundary, request/side-effect budgets, owned or synthetic controls, and a stop condition.
- The operator must understand the research domain well enough to recognize rediscovery, unrealistic deployment assumptions, and false positives.
- Use isolated evaluation fixtures first. Keep secrets, raw user data, and capability-bearing URLs out of model prompts.
- In Argus, load `argus-vault-routing` and the matching class playbook before any target-specific work.
- For a bypass, payload, CVE, mitigation, exploit technique, false-positive, or reportability question, invoke through the `terminal` tool:

```bash
argus-preview-rag "<the exact problem>" --k 5 --min-score 0.1 --save
```

Treat retrieved material as source context, not runtime proof or authorization.

## How to Run

1. Load this skill with `skill_view(name='ai-security-research-cascade')`.
2. Gather public or operator-supplied inspiration with `web_extract`; use `read_file` and `search_files` for local material.
3. Create an isolated `research-run.md` with `write_file` using the blueprint in Procedure step 1.
4. Use `delegate_task` for independent, fresh-context hypothesis generation; provide one micro-inspiration fragment per task.
5. Implement deterministic normalization, deduplication, evaluation, and safety gates with `execute_code`, or invoke an existing project harness through the `terminal` tool.
6. Record every observation, control, error, and disposition with `write_file` or `patch`; verify the completed run with `read_file`.

## Quick Reference

- Source: `https://portswigger.net/research/can-ai-do-novel-security-research`
- Blueprint: `Objective -> Evaluation strategy -> Inspiration sources -> Cascade routes`
- Phases: `Ideation -> Evaluation -> Weaponization -> Cascade`
- Roles: `AI -> variation and hypotheses`
- Roles: `Code -> gates, measurements, normalization, repeatability`
- Roles: `Human -> objective, novelty judgment, cascade leaps, authorization`
- Micro-inspiration size: `1-3 sentences`
- Hypotheses per fragment: `1-5`
- Evidence states: `hypothesis | evaluated | impact_validated | reportable`
- Terminal states: `reportable | disproved | blocked | coverage_gap | duplicate`
- Novelty classes: `trigger | pattern | class | weaponization | enhancement`
- Safety rule: `model output is never proof`
- Scaling rule: `fix evaluation and data quality before scaling ideation`
- Adoption reference: `references/http-terminator-adoption-gates.md`
- Filesystem phase-boundary reference: `references/descriptor-stable-offline-run-phases.md`

## Procedure

1. **Write the research contract before generating ideas.**

   Use `write_file` to create `research-run.md` with this structure:

   ```markdown
   # Research Run
   ## Objective
   ## Novelty Definition
   ## Authorization and Safety Boundary
   ## Evaluation Strategy
   ## Inspiration Sources
   ## Cascade Routes
   ## Deterministic Gates
   ## Hypothesis Ledger
   ## Evaluation Ledger
   ## Discovery Lineage
   ## Coverage Gaps
   ## Final Dispositions
   ```

   Define what counts as a novel trigger, pattern, class, weaponization method, or enhancement for the chosen domain. Require either cross-implementation behavior or a realistic supported deployment path; a source-only oddity is a lead, not a discovery. Completion criterion: objective, novelty threshold, authorization, budgets, and stop conditions are explicit.

2. **Design the evaluation primitive first.**

   Start from the security invariant, then define a causal differential that can detect unexpected violations without assuming one exact malicious output. Establish a stable baseline, one-variable candidate input, negative control, repetition policy, noise threshold, and controlled success oracle. Put measurement and verdict logic in deterministic code via `execute_code` or an existing harness invoked through `terminal`; the model must not decide its own success. Completion criterion: the evaluator detects a known positive, rejects a known negative, and represents inconclusive runs as `coverage_gap` rather than safe.

3. **Run a technique-rediscovery benchmark.**

   Select a valuable technique already known to the operator but absent from the prompt. Begin with a concrete high-value question, review low-value answers, explicitly rule those families out, and rerun from fresh context. Score exact rediscovery, false positives, duplicates, and unusable ideas; do not count plausible prose as success. Completion criterion: the baseline exposes whether the system can generate useful hypotheses before autonomous scale is attempted.

4. **Generate with micro-inspiration, not a giant context.**

   Split authoritative sources into independently attributable fragments of `1-3 sentences`. Give each fresh `delegate_task` exactly one fragment, the objective, prohibited low-value families, and a request for `1-5` hypotheses. Do not pre-load the model with the full technique history: extra context creates anchoring and rediscovery risk. Normalize and deduplicate outputs with deterministic code while preserving provenance in the appropriate layer. The strict offline packager preserves source URL/hash, run ID/timestamp, fragment ID, and hypothesis lineage; keep section/capture/model identity in a separate operator-reviewed research record bound to the run rather than adding undeclared fields to worker result JSON. Completion criterion: every normalized hypothesis maps to one or more contributing inspiration fragments, all contributing fragment lineages survive deduplication, and duplicates cannot inflate yield.

5. **Evaluate candidates under the narrowest safe boundary.**

   Start with a loopback fixture or fixed-source harness. For tool adoption, review the repository at a fixed revision and separate offline ideation stages from target-touching stages; use `references/http-terminator-adoption-gates.md` for the HTTP Terminator example. For multi-phase local packagers, treat existing run directories as adversarial filesystem boundaries: retain parent/run descriptors, perform every run-local read/write relative to them, and recheck device/inode identity before success; follow `references/descriptor-stable-offline-run-phases.md`. Do not treat ambient proxy history, a URL corpus, a placeholder denylist, or a log-only request filter as a scope boundary. A live check is a separate phase and may occur only inside explicit scope, using the smallest safe request, owned controls, strict pacing, bounded response capture, and immediate stop on instability or success. Store actual tool output and causal controls; never store model claims as observations. Completion criterion: each candidate has one disposition and the ledger cardinality equals the normalized hypothesis count.

6. **Separate weaponization from evaluation.**

   Promote only candidates that passed the deterministic evaluator. Run impact analysis in fresh context with only sanitized evidence and fixed harness interfaces; retain success checks in non-model-controlled code. Prefer owned or synthetic proof, avoid real-user data, and early-exit once the minimum reportability threshold is demonstrated. Completion criterion: impact, actor, preconditions, and negative controls are closed without exceeding the approved side-effect budget.

7. **Turn anomalies into a discovery cascade.**

   Preserve unexpected output even when it is outside the original detector's class. Add bounded anomaly detectors for unexplained status, length, timing, parser, state, binary/text, or multi-response behavior, then place anomalies in a manual-review queue rather than auto-labeling them vulnerabilities. For fresh-context analysis, use the source's cascade questions:

   ```text
   Look at the observed behavior and consider 1-3 plausible hypotheses that explain it.

   Do any of these hypotheses have security implications beyond this attack class?

   Extrapolate beyond the attack class to the logical extreme.
   ```

   The human reviews broad conceptual jumps, rejects unsafe or unsupported routes, and feeds approved hypotheses back through the same evaluator. Completion criterion: every cascade edge records `parent evidence -> hypothesis -> evaluator -> disposition`.

8. **Move stable responsibilities from AI to code.**

   Start AI-heavy only to prototype quickly. As failure modes become known, transfer normalization, deduplication, scope enforcement, request construction boundaries, success oracles, evidence limits, and stop conditions into deterministic code. Execute each phase with fresh context and pass only sanitized evidence plus immutable scripts so faulty reasoning does not contaminate later phases. Completion criterion: repeated runs use versioned prompts, model identity, evaluator version, and identical deterministic gates.

9. **Falsify novelty and close the run.**

   Search prior art with `web_search` and retrieve primary sources with `web_extract`; in Argus, also run the Preview.is query required in Prerequisites. Have an independent `delegate_task` attempt to disprove novelty, deployment realism, causal attribution, and reportability. Distinguish autonomous discovery from a human/AI joint discovery in the final lineage. Completion criterion: every hypothesis is reportable, disproved, blocked, duplicate, or a declared coverage gap, and the final claims are backed by retained tool output.

## Pitfalls

- **Ideation-first scaling.** Thirty thousand ideas are useless if the evaluator is noisy or narrow. Build and test the oracle first.
- **Context contamination.** Full papers and technique names anchor output toward rediscovery. Use one small attributed fragment per fresh context.
- **Expertise gap.** An obscure known technique can look novel to a newcomer. Require expert and primary-source prior-art review.
- **Expected-output tunnel vision.** A detector that recognizes only a known exploit class suppresses the most valuable anomalies. Detect invariant violations first, classify second.
- **Model-owned verdicts.** Agents can satisfy or bypass their own success criteria. Keep verdict logic deterministic and immutable to the hypothesis generator.
- **Disposable-code sediment.** Repeated AI-generated harness rewrites prevent reliable iteration. Move stable behavior into tested code.
- **Cross-phase contamination.** Carrying conversation history from ideation into evaluation encourages confirmation bias. Use fresh contexts and evidence-only handoffs.
- **Harness bugs as target evidence.** Malformed requests, retries, connection reuse, or parser mistakes can create convincing false positives. Reproduce with a corrected harness and causal controls.
- **Fake-reality safety.** Do not disguise live systems as simulations or rely on prompt framing for authorization. Enforce scope and destinations in the tool layer.
- **Implicit targeting.** Proxy history, imported URL files, saved preferences, and previous-session queues are inputs—not authorization. Require an explicit default-deny destination contract for each run.
- **Log-only filtering.** A handler that records a prohibited request and then continues it is observability, not prevention. Verify every egress gate against an owned sink and require zero sink requests.
- **Convenience automation resurrection.** Periodic scans, auto-import, corpus upload, OAST, or victim-request strategies may resume from defaults or persisted state. Force them off at startup and enable them only through a reviewed run artifact.
- **Unreviewed binary dependencies.** Do not load prebuilt scanner/framework JARs merely because they are present. Bind provenance, hash, source correspondence, and license before execution.
- **Harness/schema drift.** Build installed-CLI E2E fixtures from live parser constants and current known-good test helpers. If a temporary verifier fails on an assumed field name, inspect the live schema and rerun; do not misclassify the harness defect as a release blocker. When a newly enforced per-item ceiling makes an older aggregate-overflow fixture unreachable (for example, bounded packet count × bounded prompt size can no longer exceed the artifact ceiling), replace the stale negative with a maximum-cardinality positive compatibility test: require the producer to succeed, assert every emitted item and the exact aggregate bytes stay within downstream limits, and pass the artifact unchanged through the consumer. Do not weaken the earlier ceiling merely to preserve an impossible test.
- **Premature seal invalidation.** Reproduce a suspected post-seal blocker with a read-only probe before invalidating reviews. Distinguish local parsing helpers from network resolution and treat unavailable optional instrumentation as no evidence—not a pass or failure. Once any sealed artifact really changes, invalidate every outstanding verdict and reseal.
- **Dispatch mistaken for approval.** Background reviewer dispatch is not independent approval. Final status must remain verification-incomplete until every required machine-parseable verdict returns, verifies the same seal before and after review, and contains no blocker.
- **Autonomous cascade overreach.** AI handles local variations better than broad conceptual leaps. Keep a human at the cascade review boundary.
- **One-off implementation oddities.** Original code behavior may be irrelevant if no realistic system composition makes it exploitable.
- **Unsafe impact collection.** Do not acquire live credentials or user data merely to strengthen triage. Use owned controls and stop at minimum sufficient proof.
- **Model or prompt drift.** Yield changes across versions. Preserve model identity, prompt, fragment, evaluator version, and run timestamp in the outer research record. Do not add them as undeclared fields to a strict packager schema; bind the reviewed record separately when the packager does not expose those fields.
- **Run-path check-then-use races.** For a new run, writing through the caller-declared name after `mkdir` can adopt a replacement inode; stage through an unpredictable private directory and publish with an atomic no-replace rename. For every phase, retain parent/run descriptors, traverse nested run-local evidence with `openat`-style no-follow opens, recheck both the run entry and parent pathname device/inode before success, and roll back only invocation-owned files through the retained descriptor.
- **Premature release sealing.** A seal created before the final adversarial self-audit is not an approval artifact. Invalidate it immediately when any blocker appears, disregard audits tied to the stale checksum, rerun the entire matrix, and dispatch replacement reviewers only after a new verified seal exists.
- **Zero findings interpreted as safety.** Missing partitions, timeouts, skipped hypotheses, or failed workers are coverage gaps, not negative evidence.

## Verification

Use `read_file` on the completed `research-run.md`. The skill worked only if the file contains the four-part blueprint, an authorization boundary, a deterministic evaluator with positive and negative controls, one disposition per normalized hypothesis, complete inspiration-to-finding lineage, explicit coverage gaps, and no claim supported only by model output.
