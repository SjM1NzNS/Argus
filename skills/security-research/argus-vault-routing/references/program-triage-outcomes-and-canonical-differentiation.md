# Program triage outcomes and canonical differentiation

Use this reference when a bug-bounty portal or reviewer changes a submitted report to `Duplicate`, `Informative`, `Not applicable`, `Won't fix`, `Accepted`, or another final/intermediate program state.

## Core distinction

Keep three axes separate:

1. **Technical evidence disposition** — did the proof demonstrate the claimed behavior and boundary crossing?
2. **Program disposition** — accepted, duplicate, not applicable, informative, excluded, or unresolved.
3. **Economic/credit outcome** — reward, no reward, duplicate exclusion, or pending.

A duplicate does not by itself falsify the technical proof. It means the program says the same or a broader defect is already tracked. Conversely, duplicate status is not independent confirmation of every severity or impact claim in the submitted report.

## Source-first capture

Treat the current portal event, email, or user-supplied reviewer message as the primary disposition source. Preserve:

- program and report reference ID;
- exact status transition;
- canonical/duplicate identifier transition;
- reviewer comment number and verbatim text where supplied;
- reward/credit language;
- event timestamp when provided, otherwise label only the local receipt timestamp;
- whether canonical details or a screenshot were actually available.

Do not infer the canonical root cause from its number. Do not use session history as primary proof of the current portal state when the direct message or portal is available.

## Canonical root-cause differential

Before appealing or considering a variant, compare:

| Dimension | Question |
|---|---|
| Attacker source | Is the input/actor primitive materially different? |
| Trust boundary | Does the new path cross a different protected boundary? |
| Missing control | Is the absent or bypassed enforcement check independently removable? |
| Sink/consumer | Does a distinct component authorize, execute, disclose, mutate, publish, or merge? |
| Fix independence | Would fixing the canonical leave the proposed variant exploitable, and vice versa? |
| Incremental impact | Does the variant add capability that survives the canonical fix? |

Payload spelling, another browser alias, another sample app/agent, another object ID, a stronger downstream effect behind the same sink, or a new vulnerability label are not independent root causes.

If canonical details are hidden, record that the comparison is unavailable. Do not invent a distinction.

## Appeal gate

Recommend an appeal only when all are true:

1. enough canonical detail is available to compare technical causes;
2. a concrete mismatch can be stated in one or two sentences;
3. the mismatch is supported by preserved source/runtime evidence;
4. the proposed fix or enforcement boundary is independently different;
5. the appeal does not merely reargue severity, payload novelty, or presentation quality.

Otherwise close locally with no appeal. Reopen only if the program asks a specific question, reveals useful canonical detail, or changes status.

External writeups and RAG matches are secondary methodology support only. They may illustrate how duplicate appeals are evaluated, but they cannot establish what a private canonical contains.

## Published-scope versus panel-classification disputes

Treat a public scope/tier record and a review panel's case-specific classification as separate sources that can conflict.

Before submission:

1. Save the exact public repository/asset identifier, tier, product-vulnerability scope flag, source URL, retrieval timestamp, and file/content hash.
2. Prefer a commit-pinned permalink or immutable snapshot in addition to the live URL; verify that the commit predates submission.
3. Preserve the rules language that makes the list authoritative and the eligibility consequence of the listed tier.
4. Describe the result as **the current published classification**, not as a guarantee that the reward panel cannot apply a different internal classification.

After a tier/scope rejection:

1. Preserve the reviewer text and re-fetch the authoritative public source before replying.
2. Compare the exact repository/asset string, not a project nickname or adjacent repository.
3. If the reviewer-assigned tier conflicts with an exact public record, and the reviewer invites correction, send one narrow factual response containing the exact record, commit-pinned lines, pre-submission commit date, and relevant rules language.
4. Do not reargue exploit severity, CVSS, presentation quality, or vulnerability type when tier is the only stated rejection basis.
5. Ask the panel to reconcile the sources or identify the superseding authority. If it confirms that an internal classification or erroneous generated list controls, record that program outcome and stop unless new authoritative evidence appears.
6. Preserve the submitted technical artifact unchanged; update active status records to `rejected on disputed tier / factual correction pending` and avoid public disclosure while the correction is open.

A duplicate record in a generated scope file may indicate a data-quality issue, but it does not erase an exact published tier entry. Report the exact fact without speculating about why the duplicate exists.

## Synchronized vault update

Create one dedicated triage-outcome record, then update every active status surface that future sessions consult:

- target `findings-draft.md`;
- `hypotheses.md`;
- `checkpoint.md`;
- `next-steps.md`;
- chronological `hunt-log.md`;
- target map/index;
- mission report/evidence index when applicable.

The outcome record should include:

- report/reference/canonical IDs;
- exact portal transition and reviewer text;
- local disposition;
- technical-evidence interpretation;
- reward/credit outcome;
- appeal and follow-up gate;
- non-reframing rule;
- paths and hashes for retained report/video/evidence.

Preserve historical submitted reports and prior logs as historical artifacts. Update active status summaries rather than rewriting the original report as though it had always been a duplicate.

## Non-reframing rule

State the canonical causal chain explicitly—source → parser/transport behavior → missing control → sink → impact—and prohibit new submissions that still depend on that chain. Route future variants back through ordinary source-first and reportability gates. Proceed only when fix independence or a different protected consumer is established.

## Integrity and stale-state validation

After edits:

1. hash the outcome plus all changed active status files in a separate post-triage manifest;
2. verify the manifest immediately;
3. verify retained attachments against their pre-existing hashes;
4. confirm each active status surface contains the report ID, canonical, and final disposition;
5. search active summaries for stale `awaiting`, `ready to submit`, or `not submitted` states;
6. allow historical logs/reports to retain old states when clearly dated and superseded;
7. verify relative links and balanced Markdown fences;
8. reread the actual chronological log tail.

## Large-log patch pitfall

Do not append to a large hunt log by fuzzy-matching a generic final bullet such as `Evidence:` or `No action occurred.` Similar lines recur and can place the event inside an older block or replace unrelated evidence.

Safe pattern:

1. read the real tail immediately before editing;
2. anchor on the complete, unique final block or exact final line plus its section heading/context;
3. patch once;
4. reread the tail and the replaced source block;
5. restore any displaced line before proceeding;
6. only then hash the final files.

## Worked session pattern

A report changed from `Assigned` to `Duplicate`, gained a private canonical number, and the reviewer explicitly denied reward/credit. Correct handling was to retain the valid browser/session-mutation evidence, record duplicate as a novelty/program outcome, decline appeal because canonical details were unavailable, block cosmetic variants of the same request-integrity root cause, synchronize six active vault surfaces plus the target map, and generate a separate post-triage manifest.
