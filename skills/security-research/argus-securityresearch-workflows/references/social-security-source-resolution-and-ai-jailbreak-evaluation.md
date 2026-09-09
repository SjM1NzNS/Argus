# Social security-source resolution and AI jailbreak evaluation

Use this reference when a user supplies X/social posts as potential security learning, especially thread roundups or AI jailbreak/red-team methodology.

## Resolve the original source before promotion

1. Open the exact post URL first and preserve author, timestamp, post text, media, and directly exposed links.
2. If the post is a thread/index, expand replies and inspect DOM links and media. Use the publisher’s own site, newsletter, sitemap, or search index to resolve linked originals.
3. Read-only public metadata/mirrors may corroborate post IDs, media, and conversation IDs, but they do not prove missing reply/article content.
4. Evaluate every linked article at its original URL. A roundup headline is discovery metadata, not methodology authority.
5. If article titles or URLs remain inaccessible, create a deferred review note containing the exact source, attempted resolution paths, and re-review gate. Never infer article identities or promote lessons from branding alone.

## Provenance states

- **Resolved:** original post and linked primary source were read.
- **Partially resolved:** post text/media were read but linked thread/article content is missing.
- **Corroborated:** a mirror or secondary source confirms metadata/content already observed from the original.
- **Deferred:** source looks potentially useful but primary content is unavailable.
- **Rejected:** primary content was reviewed and lacked actionable methodology or duplicated stronger existing material.

## Deferred roundup resolution and cross-class promotion

When the user later supplies the missing article URLs for a deferred social roundup:

1. Reopen the existing deferred record rather than creating a parallel unresolved narrative. Mark it resolved/superseded, list the supplied primary URLs, and point to the durable promotion summary. Preserve the earlier no-inference rationale as a valid provenance decision.
2. Fetch and read each original article independently. If a page is dynamic or cluttered, use a local HTML-to-text/browser extraction path; do not promote from title, search snippet, or roundup copy.
3. Route each article by **root cause**, including every cross-domain class in an exploit chain. A five-link roundup may legitimately patch Deserialization, XSS, File Upload, Authentication/JWT, REST/tooling, and Attack Chains rather than becoming one broad “bug bounty classics” playbook.
4. Run Preview.is/RAG lookup separately for each technique. Independent calls prevent one rate limit or source failure from suppressing unrelated articles; retry only missed/weak queries and cite returned URLs.
5. Compare each lesson against current class playbooks. Patch missing evidence, false-positive, reportability, or routing gates first; create a new class-level playbook only when the index has a genuine class gap. Put source-specific detail in a source summary/eval or this skill’s `references/`, not in a narrow one-session skill.
6. For historical exploit chains, extract reusable feasibility gates and modern negative controls—browser/version behavior, product patch state, attacker-controlled carrier, local-component reachability, cryptographic trust sequence—rather than copying payloads as current live-target instructions.
7. Update the class index, source summary, evals, monthly changelog, and stale deferred record together. Verify every source URL is preserved, every new index `Load:` path exists, actual unfinished markers are absent, and temporary article/RAG captures are removed only after durable artifacts pass.

A useful cross-source review question is: **what must be true before this payload or primitive becomes attacker-feasible?** Examples include exact serialization transformations and classpath compatibility, browser-deliverable file bytes rather than manual proxy control, every website-to-local-process chain link, framework fit before corpus fuzzing, and verified JWT trust/authorization change rather than parse acceptance.

## AI jailbreak methodology promotion

Treat compact social advice such as baseline → mutate → repeat → automate → judge as a lab workflow, not as authority for broad target spraying.

### Guardrail-layer attribution

Visible behavior suggests hypotheses only:

- blocked before generation → possible input/gateway control;
- starts then truncates → possible output moderation, model stop, timeout, middleware, or UI behavior;
- natural-language refusal → possible system/model policy, fine-tuning, moderation, or output rewriting.

Require traces, finish reasons, provider errors, request/response metadata, logs, or controlled comparisons before naming the enforcement layer.

### Experimental design

1. Establish direct baseline and same-meaning benign control.
2. Change one mutation family at a time: framing, roleplay, encoding, splitting, formatting, or composition.
3. Repeat baseline and mutation conditions—not only the promising prompt.
4. Record full denominator, success count/rate, model/provider/version, timestamp, temperature/seed/settings when available, and exact rubric.
5. Keep refusals and judge disagreements. Do not retain only successful transcripts or count near-duplicate variants as independent techniques.
6. Calibrate keyword/LLM judges against human labels for refusal, discussion/quotation, refusal-with-details, partial compliance, and completed task.
7. Treat judge labels as triage only; human review plus target traces and impact decide reportability.

### Reportability

Generic unsafe output or jailbreak-only behavior is usually not an application-security finding. Require either explicit program acceptance of model-safety bypasses or a concrete target boundary break: unauthorized data, tool execution, persistence, victim/cross-user influence, account/tenant crossing, or security-sensitive workflow control.

## Promotion and verification

- Compare against existing class playbooks before adding payloads or techniques; patch gates rather than duplicate lists.
- Create a concise source summary, relevant eval scenarios, playbook/index patch if needed, and changelog entry.
- Read back newly written raw/source files before promotion. Generated tool arguments can accidentally preserve literal truncation markers.
- Scan for actual unfinished markers (`TODO`, `TBD`, literal `...[truncated]`), but do not reject legitimate prose containing words such as “placeholder.”
- After inserting numbered checklist steps, verify the full sequence is monotonic and unique.
- Clear only disposable raw/RAG captures after durable summaries/deferred notes have passed verification.
