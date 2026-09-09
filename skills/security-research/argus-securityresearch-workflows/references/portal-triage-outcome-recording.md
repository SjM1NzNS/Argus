# Bug-bounty portal triage outcome recording

Use this workflow when a user supplies a program portal transition, reviewer comment, canonical/duplicate link, reward event, severity decision, or permission to disclose.

## 1. Treat the portal event as a new disposition source

Record exactly what was supplied:

- program reference ID;
- local finding ID and exact report title;
- old and new status;
- canonical/component changes, if any;
- comment number and verbatim reviewer text;
- reward/credit wording, if explicitly present;
- the local receipt timestamp, clearly distinguished from the unknown portal-event timestamp.

If the portal itself is accessible, inspect it first. Otherwise state that the source is a user-supplied portal event and whether a screenshot/export was supplied. Never manufacture a portal timestamp, canonical details, reward result, or hidden tracker contents.

## 2. Classify the disposition precisely

Do not collapse different labels into “invalid”:

### Duplicate

- The program says the root cause is already tracked.
- Preserve the canonical ID and program reference ID.
- The local technical proof may remain valid, but novelty/reward eligibility is gone.
- Do not appeal unless a concrete technical distinction from the canonical can be demonstrated.
- Do not resubmit cosmetic variants: a different payload, browser alias, sample app, generated target, or downstream effect behind the same enforcement defect is not a new root cause.

### Infeasible / Won't Fix / below threshold

- This is a severity, actor-model, prerequisite, or escalation-threshold decision unless the reviewer explicitly says the behavior is not reproducible.
- Preserve demonstrated technical evidence while recording the exact risk assumptions the program rejected.
- Do not call it a duplicate or false positive.
- Reopen only if new evidence materially changes the rejected risk basis: for example a default remote trigger, higher-trust delivery path, lower-privilege boundary, hosted/trusted-publication effect, or an independently removable root cause.

### Not reproducible / invalid / intended behavior

- Record the program's exact basis separately from local evidence quality.
- If local proof still reproduces, preserve the conflict and identify the missing environment/version/control rather than silently downgrading it to “false positive.”

## 3. Never infer reward, credit, or disclosure action

- If the comment does not mention reward or credit, record **not stated in the supplied event**.
- Permission to disclose publicly is not an instruction to publish.
- Do not file a GitHub issue, PR, advisory, blog post, or comment without explicit user direction.
- If publication is authorized but not requested, record `public disclosure permitted; no public side effect performed` and keep any disclosure outline local.

## 4. Update the full command-center state

Update every currently authoritative record that exists for the finding:

1. dedicated triage-outcome note beside the submitted report;
2. findings draft/register;
3. hypotheses entry, or add a compact outcome section if the candidate came from a broader hypothesis;
4. checkpoint;
5. next steps, removing stale “awaiting triage” or further-mining instructions;
6. append-only hunt log;
7. target map;
8. submitted-bundle README/status;
9. stale “feedback pending” notes, marking them superseded rather than deleting history.

Do not rewrite old report bodies merely to make them look post-triage; preserve the originally submitted artifact and add a separate outcome record.

## 5. Triage-outcome note schema

Include:

```markdown
# <finding> program triage outcome

- Finding:
- Title:
- Program reference:
- Outcome recorded locally UTC:
- Status transition:
- Canonical/component transition: # only if supplied
- Program outcome:
- Local disposition:
- Reward/credit outcome: # explicit or “not stated”
- Public disclosure state:

## Preserved portal text
## Technical disposition
## Program rationale and limiting prerequisites
## Appeal and future-variant gate
## Public-disclosure posture
## Retained evidence
## External corroboration boundary
```

Quote the portal response verbatim. Separate these three questions:

1. Was the behavior technically demonstrated?
2. Did the program consider it novel/reportable/severe enough?
3. Did the program state any reward, credit, or disclosure result?

## 6. Root-cause and future-variant gate

For every closed report, write a positive future gate rather than only “do not resubmit”:

- which enforcement boundary would need to differ;
- which prerequisite would need to disappear;
- which actor model would need to become stronger;
- which mitigation would need to fail independently;
- which hosted/high-trust path would materially change impact.

This prevents duplicate reframing while preserving legitimate research directions.

## 7. External research boundary

When reportability/duplicate/mitigation guidance triggers external RAG:

- treat the user-supplied portal response as the primary disposition source;
- use external matches only as methodology, label, or appeal precedent;
- cite the returned URL and state explicitly that it is not evidence about the current defect;
- do not let a secondary article overwrite the program's exact wording.

## 8. Integrity and verification

After all text updates are complete:

1. hash the outcome note and all modified command-center records;
2. write a separate `.sha256` manifest that does not include itself;
3. do not modify hashed files after writing the manifest;
4. run `sha256sum -c`;
5. verify the submitted report/email and referenced evidence still exist;
6. scan authoritative current-state files for stale statuses such as `awaiting triage`, `not submitted`, or `feedback pending`;
7. check Markdown fence balance and outcome-reference presence;
8. verify no publication side effect occurred unless explicitly requested.

Suggested final validation line:

```text
TRIAGE_VALIDATION_PASS status=<label> reference=<id> manifest_entries=<n> stale_current_status=0 public_side_effects=<none|verified>
```

## 9. Patch-placement pitfall

Broad fuzzy replacement against generic lines such as `Evidence:` can land in the wrong chronological block. For append-only logs:

- anchor on a unique heading plus neighboring lines, or use the exact current tail;
- inspect every returned diff;
- reread the affected neighborhood after insertion;
- if placement is wrong, restore the displaced line first, then append at the verified tail;
- only hash after this correction and final reread.

The durable lesson is not to avoid fuzzy patching; it is to use unique anchors and verify placement before declaring the triage record complete.
