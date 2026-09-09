# ADK-style local agent API wildcard-bind proof pattern (2026-07)

Session-specific companion to `local-service-bind-scope-validation.md`. Use it when a localhost-described developer agent/API exposes stateful or tool-capable routes.

## Durable lesson

A wildcard bind becomes materially stronger than a passive information leak when an unauthenticated reachable peer can bootstrap its own application state and invoke the local agent. Do not center the report on existing-session guessing when the API itself exposes a self-contained sequence:

1. enumerate an application/agent name;
2. create an attacker-chosen user/session;
3. read the owned marker back;
4. invoke the agent with a harmless deterministic marker;
5. prove exactly one invocation in the developer process.

This removes dependence on victim session identifiers. Existing session, artifact, or debug-trace access remains conditional secondary impact.

## Source-first checklist

Map the complete route family before probing:

- app/agent enumeration;
- session list/read/create/delete;
- artifact list/read/delete;
- debug/event/trace routes;
- synchronous, streaming, and WebSocket agent-run routes;
- authentication middleware;
- Origin/Host/CORS handling;
- launcher bind address, help text, and startup logs;
- generated deployment commands that may intentionally require wildcard binding.

Record the exact reviewed commit. In Go, compare the advertised `localhost` URL to `http.Server.Addr`; `":<port>"` is wildcard.

### Sibling-implementation parity gate

When the repository designates another language implementation as the source of truth, inspect equivalent CLI behavior in sibling releases that **predate** the affected release. Preserve:

- the source-of-truth statement and exact permalink;
- sibling tag dates and commit IDs;
- source blob IDs or file hashes;
- the equivalent bind option, its default, and its explicit remote override.

A contemporaneous sibling that defaults to `127.0.0.1` and exposes `--host` materially weakens an “unavoidable shared launcher architecture” objection and shows a deployment-compatible fix already exists. Frame this as parity and expected-behavior evidence, not as an explicit security guarantee for the affected implementation.

## High-fidelity safe runtime proof

Use the real launcher and an in-memory session service with a deterministic no-tool agent.

- Prefer an untouched, shipped, credential-free example invoked through its normal CLI before relying on a researcher-authored in-process probe. Preserve the exact release tag, command, startup output, and sample source hash.
- For a stronger peer model, send the requests from a separate container/network namespace. Record both network-namespace inode identifiers and the peer's routed host address. A rootless Podman `host.containers.internal` path is acceptable evidence of cross-namespace reachability when a loopback-only listener refuses the same peer; describe it as an adjacent workload, not a second physical host.
- Disable HTTP proxy inheritance in the probe.
- Request the enumeration route through loopback and one non-loopback host address; require identical response data.
- Through the non-loopback address, create an attacker-chosen user/session with a fake marker, read it back, and call the agent-run route with a second marker.
- Instrument the deterministic agent to record invocation count and exact user text; require one invocation and exact equality.
- Run an otherwise equivalent listener explicitly on `127.0.0.1` and require the non-loopback request to fail.
- Before submission, produce one **clean full transcript**, not only a curated summary. It should preserve the exact host and peer scripts, image/tag, URLs, request bodies, relevant headers, HTTP statuses, namespace/address/route/listener facts, workflow outputs, prior-data response, negative-control failure, cleanup, and clean-worktree result. Keep a concise summary separately for triage speed.
- Avoid nested JSON inside a double-quoted `podman ... sh -c "..."` command: an outer shell can strip JSON quotes and turn a valid request into HTTP 400. Prefer a small peer script mounted read-only into the container, with single-quoted JSON bodies. Use fresh user/session IDs for every rerun so an earlier partial attempt cannot cause 409/stale-state ambiguity. If a run fails because of harness quoting, keep it only as internal debugging context and replace final evidence with a clean successful rerun; never package the failed transcript.
- Preserve the temporary test source and verbose output as evidence, then remove the test from the upstream clone and verify `git status --short` is empty.
- Run the affected package suites again after cleanup.
- If the official Web UI uses a predictable default user identity, create and run a normal owned canary conversation from the host, then have the peer list sessions for that default identity and read the discovered session. Recovering prior input/output events is stronger than inserting arbitrary state. Keep this identifier-dependent confidentiality branch secondary to self-contained invocation and cite the exact UI source/default.
- When validating a Go sample build, use `go build -o /tmp/<name> ./path/to/sample` or remove the default emitted binary before the clean-worktree gate.

Do not use real credentials, models, tools, secrets, external services, or non-owned data.

## CORS and CSRF distinction

CORS is not access control for a direct network peer. A non-browser client can call the API regardless of response ACAO.

Separately, a JSON handler that ignores `Content-Type` may accept a browser-safelisted `text/plain` form body. Treat that as a different browser-to-local integrity branch:

- validate actual browser form serialization, not only a manually constructed request body;
- if the browser inserts `=`, place it inside a harmless JSON string so the serialized body remains valid;
- require target-side state or invocation output because the cross-origin page need not read the response;
- test a distinct private HTTP origin against loopback in a fresh current browser, then test public HTTP and public HTTPS documents separately;
- a public HTTP negative helps rule out mixed content as the *only* explanation for an HTTPS negative, but it does not identify whether LNA/PNA, address-space policy, or headed/headless behavior caused the block;
- preserve successful private-origin evidence as defense-in-depth support while explicitly withholding an arbitrary public-drive-by claim when both public controls are negative;
- keep an `httptest` result as supporting evidence only when browser delivery is unproven or likely duplicate.

### Classification and related-report differentiation

Do not classify direct peer access to a wildcard-bound API as clickjacking. Clickjacking requires a deceptive or overlaid target interface that tricks a user into activating a hidden target control. Use the exploit primitive—not the presence of a browser or HTML—as the classification gate:

- **Direct routable peer → wildcard listener → unauthenticated API:** exposure to the wrong network sphere / insecure bind default; CWE-668 is usually the best primary class, with missing authentication as a contributing condition.
- **Foreign page → safelisted form/raw-body parsing → state-changing local API:** CSRF or cross-origin request integrity failure; CWE-352 may be primary when this is the main chain.
- **Hidden/overlaid target UI → deceived victim click:** clickjacking; do not use this label merely because an HTML form or iframe appeared in exploratory testing.

When a prior report against a sibling implementation also concerns an unauthenticated local agent API, perform a duplicate-differentiation matrix before submission:

1. repository/package and affected release;
2. root-cause code path;
3. listener scope and reachable boundary;
4. attacker actor and whether a victim browser/visit/click is required;
5. endpoint/parser primitive;
6. response readability;
7. demonstrated product-native impact; and
8. remediation independence.

Two reports are technically distinct when fixing one primary defect does not fix the other—for example, strict media-type/Origin/CSRF enforcement in a loopback-only JavaScript server does not correct a Go launcher's wildcard bind, while changing the Go bind default does not stop cross-site requests accepted by the JavaScript parser. Still disclose the relationship when the portal asks: a vendor may group separate implementations under one ecosystem-wide unauthenticated-development-API decision. To minimize duplicate risk, lead the wildcard report with direct adjacent-peer reachability and readable workflow/session impact; keep any browser-form variant secondary when an earlier browser-to-loopback report already exists.

## Actor-model and impact gate

Strongest conservative actor model:

1. developer runs the local web/API launcher on a laptop, workstation, VM, or shared development host;
2. another host or workload can reach the listener;
3. the peer enumerates the agent, creates its own session, and submits input;
4. the developer process executes the configured agent path.

Proven impact starts at unauthorized session mutation and deterministic agent invocation. Then actively chase the highest safe tool consequence **for internal disposition**, while separating proof development from initial-submission strategy. Prefer one exact harmless command—normally `whoami`—or an owned marker. Preserve the prompt-derived canary and command through model observation, framework dispatch, tool sink, and stdout.

If no shipped command tool or live model credential exists, a purpose-built deterministic model plus a purpose-built MCP/function tool can establish only a **configuration-specific tool-path illustration**. It is useful to answer “can this exposed API reach a configured tool?”, but it does not add a product-native command sink. Label every authored component and do not describe the result as default, universal, shipped-tool, representative-model, arbitrary-command, or RCE evidence.

Before including such an illustration in the initial portal report, run a hostile triager gate. If the untouched release already proves unauthorized workflow execution or owned-data disclosure, a researcher-authored command sink often adds little incremental value and can trigger an “expected framework behavior” or “manufactured RCE” dismissal. Default to retaining it privately/on request unless it demonstrates a product-shipped tool, representative ordinary application, or otherwise material incremental attacker capability. A single neutral sentence that impact inherits configured tools/privileges is usually enough for the initial report.

### Command-transport authenticity and source-inventory gate

Before claiming that a framework “ships no command executor,” search the pinned source broadly for process-launch APIs and classify every hit. Keep these distinct:

1. deployment/build utilities that launch fixed local programs;
2. developer-configured MCP/server bootstrap commands;
3. agent-invokable tools exposed by the configured server;
4. the model's selection of a tool and arguments; and
5. any command or argument the remote API caller can control per request.

A framework may ship and document `CommandTransport`/stdio MCP subprocess integration without shipping a default agent-invokable shell tool. Report that exact middle state. The server bootstrap command is developer-selected and normally fixed at load time; it is not equivalent to an attacker selecting an OS command through `/run`.

When the framework documents a subprocess MCP path, prefer it over an in-memory transport for the final bounded illustration:

- let the proof executable expose a dedicated `mcp-server` subcommand using stdio transport;
- have the normal agent process create the documented `CommandTransport` pointing to that subcommand;
- keep protocol stdout clean—diagnostics belong on stderr or in an independently opened target-side evidence file;
- preserve one prompt-derived canary through model observation, function-call arguments, MCP dispatch, the child sink, and stdout;
- record parent/model PID, child/tool PID, UID, and network-namespace IDs. Different PIDs with the same expected UID materially corroborate subprocess execution;
- make the sink accept only the one command needed by the proof, call `exec.CommandContext` directly without a shell, and support no arguments/interpolation;
- use `go build -mod=readonly` in the reproduction harness; do not run `go mod tidy` or rewrite supplied source during evidence reproduction;
- add exact checkout commit, required sibling-directory layout, tool prerequisites, and cleanup behavior to a README.

Control semantics must be exact:

- `RequireConfirmation=true` plus no approval proves only that the **initial invocation was deferred** and no execution was observed during that test. It does not prove that confirmation is an authorization boundary until approval/resumption, actor binding, replay, and attacker-supplied confirmation are evaluated.
- If an unsupported command is rejected by the deterministic model before it emits a tool call, label it a **model-selection safety check**. It does not independently test sink-side allowlisting.
- An unknown-application rejection is a routing prerequisite control, not evidence about command security.
- Use distinct canaries for independent runs and call them equivalent requests rather than “the same prompt.”

Do not overstate ownership: `CommandTransport` may belong to a pinned MCP SDK dependency while ADK/framework code documents and configures it. Name the framework components and dependency transport separately. Do not call a target-side log “independently written” when the proof application itself produced it; state the producer and process explicitly.

### Final package sequencing for mutable proof artifacts

Proof upgrades change source, evidence text, ZIP contents, report attachment hashes, package report copies, package checksum manifests, and the outer submission archive. Finalize in dependency order:

1. rerun the proof and controls;
2. finalize source inventory and concise evidence narrative;
3. rebuild and integrity-test the detailed artifact ZIP;
4. compute its and the concise evidence file's hashes;
5. patch those hashes into the report and evidence manifest;
6. copy the final report/evidence into the portal package;
7. regenerate a pure `SHA256SUMS` file;
8. run an independent validator for report attachment existence/hash equality, byte-identical report copies, ZIP members/integrity, secret markers, and clean checkout;
9. rebuild and test the outer archive last; and
10. record final port/process cleanup.

If a cleanup step needs recursive deletion, scope it to the generated evidence directory and obtain explicit approval. After approval, do not broaden the deletion target. A stale hash that was correct before the last edit is a package failure, not a cosmetic issue.

For a private/on-request purpose-built tool illustration, use neutral artifact names such as `conditional-mcp-tool-impact`; avoid `rce`, `safe-rce`, or similar labels that contradict the claim boundary. Build a compact supplement rather than dumping every mechanical request/session/log file. A good shape is: boundary README, source/module files, one reproduction script, positive request/response/target log, confirmation request/response/target log, listener/provenance/product-test records, and internal checksums. Keep the untouched-release initial portal package entirely free of this supplement unless a triager asks for it.

Do not claim public-Internet exposure, firewall/NAT bypass, secret theft, or universal/default RCE without separate proof.

## Intended deployment objection

A shared launcher may intentionally need wildcard binding in Cloud Run, Agent Engine, containers, or orchestration. This does not require local development to default to wildcard.

Recommended remediation shape:

- add an explicit host/bind-address option;
- default local use to `127.0.0.1` (and deliberately handle IPv6 loopback if desired);
- have generated deployment commands pass `0.0.0.0` explicitly;
- require authentication for non-loopback mode and strongly consider a per-start random session/bearer token even on loopback;
- validate `Origin` and `Host` for local browser-facing state-changing routes; do not rely on response CORS as request integrity;
- reject unexpected state-changing media types when JSON is required;
- make startup logs reflect actual listener scope.

This preserves deployment behavior while restoring the boundary promised by local CLI wording. When a close developer-tool advisory exists, compare its **fix layers** rather than its headline severity: loopback default, session token/authentication, and Origin/Host validation are often complementary because loopback alone does not stop every browser-originated write.

## Reportability review

A candidate is stronger when:

- localhost wording/logs conflict with runtime behavior;
- no authentication or remote-bind opt-in exists;
- the attacker can discover the agent and create its own session;
- state mutation and agent invocation are proven;
- a loopback-only negative control passes;
- the product is current and explicitly in scope.

Acceptance risk remains when network reachability is environment-dependent or wildcard development-server findings are treated as insecure deployment posture. Keep the report factual, split **The problem** from **Impact analysis**, and avoid assigning severity unless requested.

### Developer-run-machine collapse gate

The victim having to run a developer server does **not** invalidate a finding by itself. Developer machines may hold source, credentials, internal access, model quota, and privileged agent tools. The report can nevertheless collapse into documentation/hardening when all of the following remain plausible:

- the user intentionally starts a network-capable web/API server;
- the API has no principal/authentication model because it is designed for perimeter protection;
- the same wildcard behavior is required by official container/cloud deployment;
- localhost output is only a convenience URL, with no explicit loopback-only promise;
- the proof is same-host non-loopback rather than a second reachable host;
- peer-created state affects only the peer's own session; and
- the proof uses a PoC-authored deterministic callback without ordinary model, tool, quota, credential, or protected-data impact.

Run three verdicts separately:

1. **Technical validity:** does the wildcard listener and non-loopback API path exist?
2. **Incremental attacker capability:** does the peer gain something beyond intended network use of an open server?
3. **Program acceptance:** is the local loopback expectation and concrete victim impact strong enough to survive an intended-behavior rejection?

Do not let a technically correct primitive automatically become a “significant” report. If independent reviewers split between REPORT and HOLD, preserve the split in the internal review and raise acceptance risk rather than presenting false consensus.

### Upgrade ladder before submission

When the developer-run actor model is the weak link, prioritize these upgrades:

1. reproduce against the latest published release as well as reviewed HEAD;
2. run the ordinary documented local command or untouched official example, not only an in-process launcher fixture;
3. connect from a genuinely separate device/network namespace and record listener/firewall facts;
4. prove one harmless ordinary consequence, preferring credential-free evidence in this order: execute an untouched shipped workflow/function, recover a host-created prior owned conversation through an official predictable identity, write an owned marker through a standard/sample tool, or consume a minimal amount of owned model/API quota;
5. when the product has a Web UI, launch the supported combined UI + API mode and prove both components share the exposed listener before relying on the UI's default identity or session behavior;
6. locate official local-use documentation that promises or reasonably implies loopback-only access or omits required exposure warnings;
7. keep browser-to-local delivery as a separate branch unless a real browser proof exists.

Local-service precedents with malicious-web delivery or RCE show that developer tools can be security-sensitive, but they do not substitute for this target's delivery or impact proof. If live model credentials are unavailable, do not fabricate live-model behavior: first exhaust credential-free shipped workflows and normal owned prior-conversation evidence, then use a deterministic prompt-derived model with a supported function/MCP tool path only to disposition configured-tool reachability. Treat that result as a private configuration-specific illustration unless it adds product-native incremental capability. A successful released-workflow execution plus prior-conversation disclosure may already support REPORT with explicit acceptance risk and is often a cleaner initial submission than a prominent researcher-authored command sink.

When delayed asynchronous critics arrive after a draft was called final, reconcile them against the **current** artifact and identify stale-review assumptions before applying advice. Revise verdict/risk/control wording, rebuild any affected package, and make the usable bundle unambiguous. Preserve or clearly mark older bundles as superseded when deletion was not approved; delete/archive them only under the applicable cleanup policy. Never leave two similarly named bundles without a top-level “use this one” marker.

## Known-issue comparison discipline

Use similar reported developer-tool issues to sharpen proof and remediation, not to borrow severity:

1. Search by the exact primitive—unauthenticated local developer API, wildcard listener, browser-to-loopback write, agent/tool invocation—not only by product category.
2. Treat low-scoring RAG/news matches as discovery leads. Verify the claimed affected behavior and remediation against the official GHSA/CVE record and upstream fix commit.
3. Extract the accepted report's proof shape: released artifact, realistic command, attacker delivery, unauthenticated action, concrete side effect, and causal negative control.
4. Extract mitigation layers independently. A close local-AI precedent may combine loopback default, random session token, and Origin validation; that supports defense in depth but does not establish equal impact.
5. Also inspect disputed “trusted network” advisories. They predict the likely intentional-development-server rejection and help prioritize sibling parity, explicit local-use wording, a real peer, and one ordinary tool/model consequence.
6. Keep external precedents in internal review unless a short citation materially explains expected behavior or remediation. Do not let an RCE precedent make a deterministic workflow invocation sound like RCE.

## Final critical-review gate

Before promoting a technically strong wildcard-bind candidate to a final report:

1. Re-run the focused proof from the preserved source against the pinned revision; do not rely only on an earlier transcript.
2. Re-run affected package suites, remove the temporary probe from the checkout, and require a clean upstream worktree.
3. Review the proof under the strongest hostile objections: intentional container/cloud binding, development-server expectations, firewall/routing dependence, same-host non-loopback proof versus a physically separate peer, lack of dangerous-tool execution, and whether the API is intentionally unauthenticated behind a presumed local boundary.
4. Treat same-host non-loopback access plus an explicit `127.0.0.1` negative control as proof of listener scope, not proof that any particular remote firewall path is open. State remote routability as a precondition.
5. Make the self-contained `enumerate agent -> create attacker-owned session -> read marker -> invoke agent` sequence the primary impact. Do not dilute it with identifier-dependent existing-session speculation.
6. Pin exact source permalinks and revision in the report. Include expected/actual behavior and a deployment-compatible remediation that preserves explicit wildcard operation.
7. Keep severity advocacy out unless the portal requires it. A technically meaningful integrity boundary failure can be submission-worthy while still carrying moderate acceptance risk.
8. Produce byte-identical Markdown/text copies when useful, scan for secrets/JWT/private-key markers/placeholders, and verify every referenced attachment exists.
9. Keep a human-readable `MANIFEST.txt` for package intent/scope and a separate pure `SHA256SUMS` file containing only checksum rows. Validate the pure file with `sha256sum -c SHA256SUMS`; do not treat warnings caused by prose lines in a mixed manifest as a clean package gate.
10. Keep the **internal review bundle** complete: critical review, focused probe source/output, machine-readable result, cleanup/test record, failed harness runs when diagnostically useful, and hashes. Build a smaller **portal package** containing the report and the strongest clean released-sample transcript; include exact host/peer scripts when reviewers need reproducibility, but exclude failed harness transcripts and superseded packages.
11. Run three separate critics on any researcher-authored tool-impact branch: technical causation/control semantics, skeptical program triage value, and report/package clarity. If the triager critic recommends omission because the custom sink is expected framework behavior and the untouched evidence is already sufficient, default to a clean initial package without the branch and retain a neutral compact supplement on request.
11. If required external RAG/reference lookup fails after the normal wrapper and direct retry, record that in the internal review, promote no RAG-derived claim, and keep the submit-ready report grounded in primary source and owned runtime evidence.

## Evidence and submission bundle shapes

Internal review bundle:

- source/route map;
- machine-readable runtime result;
- verbose positive/negative-control output;
- preserved probe source;
- final report in Markdown and text when needed;
- adversarial/final critical review;
- cleanup and regression-test record;
- checksums or a manifest;
- clean-clone confirmation.

Portal package:

- final report in one preferred format;
- untouched released-sample separate-network transcript;
- prior-conversation transcript when that branch is part of the report;
- optional manifest;
- custom probe source/output only if it materially helps reproduction or triage requests it.
