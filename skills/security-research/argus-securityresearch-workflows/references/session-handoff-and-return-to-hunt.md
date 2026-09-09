# Session Handoff and Return-to-Hunt Protocol

Use this when a long security-research session is nearing a context limit, the user asks to clear/reset, repeated compression is degrading continuity, or a mission must pause before report/ledger packaging.

## Goal

A fresh session should be able to continue from authoritative files without repeating completed reconnaissance, source recovery, controls, or impact adjudication.

## Required handoff artifacts

Create or update a mission-local `checkpoint.md` containing:

1. **Saved UTC timestamp.**
2. **Current disposition:** mapped, confirmed, HOLD, killed, report candidate, submitted, or awaiting response.
3. **One-sentence exact claim** and actor model.
4. **Bounded impact and explicit non-claims.**
5. **Completed work:** provenance, controls, tests, public evidence, duplicate search, and policy/RAG routing.
6. **Exact source pins:** every independently moving repository/action/generated executable/deployment object.
7. **Canonical evidence paths:** scripts, JSON, raw captures, reports, manifests, and public URLs.
8. **Why prior no-go/hold logic changed**, if reopening an older branch.
9. **Remaining work only**, ordered and concrete.
10. **Safety stop:** actions that still require explicit approval, including submission, PR creation, labels, workflows, credentials, or live mutation.

Create `RETURN-TO-HUNT.md` with a pasteable prompt that:

- lists the exact files to read first;
- names the routing skills/indexes to reload;
- says which completed phases must not be repeated unless verification fails;
- preserves current claim/non-claim boundaries;
- states the remaining deliverables;
- requires final verification and user review;
- repeats the prohibition on unapproved live actions.

## Global pointer

Update the target/program-level checkpoint with only a concise pointer:

- current candidate and disposition;
- mission checkpoint path;
- return prompt path;
- remaining phase;
- key non-claims and approval boundary.

Do not duplicate the full mission narrative into every global ledger during an emergency handoff. Mark ledger reconciliation as remaining work rather than partially editing many files and creating drift.

## Task-state discipline

Before stopping:

- mark genuinely completed technical phases complete;
- leave exactly one packaging/reconciliation item in progress when appropriate;
- never mark report/package/submission complete merely because the technical chain is proven;
- record any failed verifier as unresolved unless its canonical evidence independently passed and the failure was only output parsing.

## Evidence discipline

- Prefer canonical JSON/artifact files over chat summaries.
- Record exact hashes/manifest generation as pending if final files are still changing.
- Treat checkpointed full source pins and test selectors as claims to verify, not immutable truth: before final packaging, compare API/head captures with the local checkout's full identity and inspect/run the exact current test methods.
- Never place an archive's own final hash in a file that will be included in that archive; keep checksum and final verification sidecars outside to avoid self-reference.
- If any packaged report, pin, evidence file, verifier, or README changes, rebuild the package and rerun required controls after that final build.
- Never copy secrets, tokens, private request bodies, or transient credentials into the return prompt.
- Preserve public-control provenance limits and source-versus-inference distinctions.
- If exact code emits noisy stdout, point the next session at the dedicated evidence file rather than an unparseable transcript.

For complete packaging gates and post-package ordering, use `references/private-review-package-and-post-package-verification.md`.

## Minimal return prompt template

```text
Resume <program/mission> from <absolute checkpoint path>.
Read: <checkpoint>, <source pins>, <canonical controls>, and the required routing indexes/skills.
Do not repeat <completed phases> unless verification fails.
Current disposition: <status>.
Claim only: <bounded claim>.
Do not claim: <explicit non-claims>.
Finish: <ordered remaining work>.
Rerun: <exact final verifiers>.
Stop for my review. Do not <approval-gated actions> without explicit approval.
```

## Verification checklist

- [ ] Mission checkpoint exists and contains disposition, exact claim, non-claims, pins, evidence, completed work, and remaining work.
- [ ] Return prompt is self-contained and uses absolute or unambiguous paths.
- [ ] Program checkpoint points to both handoff files.
- [ ] Task statuses distinguish technical completion from packaging/submission.
- [ ] No secret/capability material appears in either handoff file.
- [ ] The next session is told what not to repeat and what must still be verified.
