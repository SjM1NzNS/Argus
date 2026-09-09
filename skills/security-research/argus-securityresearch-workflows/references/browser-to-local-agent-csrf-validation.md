# Browser-to-local-agent CSRF validation

Use this pattern for developer tools, desktop agents, IDE helpers, MCP/LLM servers, local admin APIs, and other loopback HTTP services whose endpoints can trigger meaningful actions.

## Source-first gate

Before runtime testing, trace the exact request path:

1. Identify state-changing routes that invoke agents, tools, jobs, files, cloud calls, or other side effects.
2. Record parser middleware and media-type conditions. A common discrepancy is JSON middleware followed by a route-level raw-body fallback that accepts `text/plain` and calls `JSON.parse()`.
3. Check request-integrity controls separately from response CORS:
   - Origin validation;
   - Host validation / DNS-rebinding resistance;
   - authentication or CSRF token;
   - Fetch Metadata checks;
   - allowed content types.
4. Establish listener defaults (`localhost`, explicit loopback, wildcard) and generated/deployed-container behavior separately.

## Harmless proof ladder

Use the smallest deterministic local side effect and no real model/API dependency:

1. Build a mock/deterministic agent or handler that writes an owned marker when invoked.
2. Send a protocol-level control with a foreign `Origin`, CORS-safelisted `Content-Type: text/plain`, and JSON text body.
3. Capture status, ACAO, request headers, and marker. Missing ACAO only proves the response is unreadable; it does not undo a state-changing request.
4. Repeat through a real browser from a distinct origin with:

```javascript
fetch(target, {
  method: 'POST',
  mode: 'no-cors',
  headers: {'Content-Type': 'text/plain'},
  body: JSON.stringify(payload),
});
```

5. Require server logs or marker evidence showing the request reached the side-effect sink. Do not treat page-side `fetch()` resolution alone as proof.
6. Run the relevant untouched product tests and verify the source checkout is clean after proof setup.
7. Add a content-type causal control from the same browser/origin with the same logical payload:
   - `text/plain` should deliver the POST and produce the marker;
   - `application/json` should require preflight and produce no marker when the foreign origin is not authorized;
   - malformed `text/plain` should fail parsing and produce no valid invocation.
8. Package one portable reproduction for triage: resolve repository/evidence paths relative to the script, start and stop the proof server automatically, discover its ephemeral port, declare browser/driver prerequisites, preserve positive and negative markers, and exit nonzero on failure. Do not make the reviewer reconstruct a multi-process sequence from hardcoded workstation paths.
9. Record the exact test command, pass count, browser/driver versions, OS, headed/headless mode, fresh-profile status, and clean `git status`; browser-to-local reachability can vary across those dimensions.

## Harness-fidelity gate

Purpose-built agents, loaders, and model doubles are valid isolation tools only when they preserve the product prerequisite being tested. Before trusting a matrix:

1. Make the custom loader enforce the real application-selection contract. A loader that returns the proof agent for every name silently eliminates the attacker’s `appName` prerequisite and invalidates unknown-app controls.
2. Add negative requests for both an unknown nonempty application name and a missing application name; require an invocation delta of zero for each. Capture the target-side lookup/error result separately from the browser’s opaque response.
   - Inspect session state after each negative. Some endpoints create/select the session **before** loading the application, so an unknown name can create an empty attacker-keyed session even though no agent runs, while a missing name may return before session creation.
   - Treat this as a narrower pre-lookup state side effect, not successful agent execution and not evidence that the valid-app prerequisite disappeared.
   - If the server internally constructs its session service, inject a shared in-memory service through the supported constructor/options interface so the harness can inspect state; do not reach into private fields.
   - Use unique user/session identifiers per case whenever session existence is an assertion, so a prior positive cannot contaminate a later negative.
3. Test discovery independently: dispatch cross-origin `/list-apps` or equivalent, then record whether the request arrived **and** whether the foreign page could read the response. An unauthenticated endpoint is not browser-readable discovery without ACAO or another read primitive.
4. Track `invocationDelta` per case, not only final marker existence. A marker left by an earlier case can make later negative controls appear positive.
5. If a harness defect is discovered, preserve the bad run under an explicit `invalid-harness`/`invalid-loader` label, exclude it from product claims, correct the fixture, and rerun all affected cases in clean sessions. Never merge corrected and invalid outputs into one evidence set.
6. Treat a product 4xx/5xx with zero invocation as a valid negative control even if internal error handling is inelegant; do not recast it as successful exploitation.

## Configuration-dependent impact-escalation ladder

After proving unauthorized agent invocation, do not jump directly from “a dangerous executor exists” to RCE. Build a product-path chain and preserve each dependency:

1. Inventory realistic/default agent tools and identify concrete sinks: filesystem mutation, network/cloud action, browser action, or code execution.
2. Prefer a supported application composition over a custom marker agent, e.g. product `LlmAgent` → toolset/function dispatch → product executor. Keep only model nondeterminism mocked when external API cost or refusal would make the proof unstable.
3. Make the deterministic model derive a harmless canary from the browser-supplied prompt and pass it into the tool arguments. A model that always emits a hard-coded script proves triggering but not attacker-controlled prompt-to-tool data flow.
4. Capture all boundaries independently:
   - request `Origin`, `Sec-Fetch-Site`, `Sec-Fetch-Mode`, and media type;
   - raw body received by the endpoint;
   - exact user text observed by the model;
   - tool names exposed to the model and selected tool call;
   - executor warning/process output;
   - final owned marker whose content equals the browser canary.
5. Inspect the selected tool implementation for `requestConfirmation()` or equivalent. Distinguish **no confirmation requested by this path** from **bypass of an enabled confirmation control**.
6. Use a harmless owned marker only—no credential access, persistence, network callbacks, destructive writes, or non-owned data.
7. Run untouched endpoint and tool/executor integration tests, verify the source checkout remains clean, and hash the preserved PoC/results when useful.

### Supported MCP safe-command escalation pattern

When the framework supports MCP or another first-class toolset but ships no default shell executor, do not abandon the RCE branch. Build the narrowest supported composition that preserves the framework path and makes authored components auditable:

1. Inventory the released source first. Record whether a command executor is shipped, merely documented through a generic tool transport, or absent. This determines prevalence language, not whether a safe conditional proof is worth running.
2. Prefer the product's own composition path, for example `LlmAgent → MCP toolset → MCP client/server → tool handler`, rather than bypassing dispatch by calling the handler directly.
3. Use a deterministic model only to isolate model nondeterminism. It must parse an attacker-supplied format such as `SAFE_EXEC canary=<owned> command=whoami`, copy the exact canary/allowlisted command into the real function-call arguments, and emit a final response only after the framework returns a function response.
4. Keep the proof sink deliberately harmless: invoke `exec.CommandContext` without a shell and allow only `whoami`, `id`, `hostname`, or `pwd`; log model observation and sink execution as separate JSONL records with canary, command, PID/UID, and stdout. Do not read environment variables, credential files, metadata services, or unrelated host data.
5. Send the request from the established unauthorized actor boundary—preferably an adjacent container/network namespace—and preserve host/peer namespace IDs, wildcard listener evidence, the full API function-call/function-response chain, and target-side execution log.
6. Add fail-closed controls:
   - `RequireConfirmation=false`: exactly one command execution;
   - `RequireConfirmation=true`: confirmation request present and zero sink executions;
   - unsupported command: model/tool refusal and zero execution;
   - unknown or missing application: zero model/tool execution;
   - loopback-only listener: peer transport failure when that control is available.
7. Run untouched framework tests for the toolset and HTTP handler, verify the released checkout remains clean, and package source, portable harness, machine-readable summary, raw responses, and checksums. Avoid cleanup constructs that trigger unnecessary destructive-command approval gates; prefer a fresh unique output directory or narrowly remove known generated files.

Report this as **configuration-dependent local command execution through a supported product tool path**. State which pieces are unmodified framework code and which are PoC-authored. A deterministic model plus purpose-built MCP command tool proves attacker-input propagation and concrete executor capability; it does not prove that the product ships a shell tool, that a normal live model will reliably choose it, or that RCE is universal/default.

Frame the result as two nested findings:

- unconditional proven primitive: unauthorized cross-origin/cross-site agent invocation;
- configuration-dependent escalation: concrete tool side effect or local code execution only when the selected application exposes that capability and the model selects it.

A deterministic `BaseLlm`-style test double can validly isolate product agent/tool/executor behavior, but keep its evidentiary boundary exact:

- if the test double extracts an attacker canary but independently chooses the tool and constructs the script, it proves prompt-derived attacker data reached real product dispatch/execution; it does **not** prove reliable attacker selection of an arbitrary command through a normal live model;
- say “unmodified framework components assembled in a purpose-built deterministic test application,” not “unmodified agent,” when the PoC authors the agent, instructions, skill, loader, model, or executor configuration;
- check whether the dangerous path is experimental, documented for trusted input, default-enabled, present in official user examples, or only exercised by integration tests. An intentional product path establishes capability, not prevalence;
- do not let a conditional executor title outrun the unconditional finding. Prefer an invocation/session-integrity title and place executor impact in a clearly labeled conditional subsection unless a live/default chain is separately proven.

Do not describe configuration-dependent command execution as default, universal, or reliably attacker-directed RCE without the corresponding evidence.

## Cross-site tightening without public-origin overclaim

A different loopback port may still be `Sec-Fetch-Site: same-site`. To remove that objection, serve the attacker page from a distinct hostname mapped locally to loopback and capture `Sec-Fetch-Site: cross-site`. This strengthens origin/site separation while remaining deterministic and non-public.

Disclose the remaining boundary exactly: a hostname mapped to loopback proves cross-site request integrity failure, but it does **not** prove that a public-address-space website can reach loopback through current PNA/LNA controls. Test public-origin reachability, `0.0.0.0`, or DNS rebinding as separate branches; absent Host validation is only a lead.

## Public-origin browser matrix

When public-to-loopback reachability controls reportability, test it directly from a real public document rather than extrapolating from a locally mapped hostname:

1. Load a stable public HTTPS document in a fresh disposable browser profile.
2. Execute the exact `no-cors`, safelisted request in that document context through CDP, WebDriver, or an equivalent page-context harness.
3. Record both the requested and actual document URL/origin before dispatch; redirects, HSTS/HTTPS upgrades, and CSP can invalidate an intended control.
4. Test `127.0.0.1`, `localhost`, and `0.0.0.0` separately. Treat aliases as independent address-space cases.
5. Capture browser network failures and console diagnostics, especially `LocalNetworkAccessPermissionDenied`, `InsecureLocalNetwork`, mixed-content classification, and CSP blocks.
6. Require server logs/model observations plus the OS marker for a positive result. An opaque response is expected and sufficient for a write-only side effect.
7. Repeat positive public-origin results in a second clean browser session and preserve both result sets.
8. Run at least one current browser from each materially different enforcement family when available. Report a browser/version matrix rather than calling the primitive universally reachable or universally blocked.

### Navigation-class bypass and valid JSON through `text/plain` forms

Do not stop after current Chrome blocks `fetch`, XHR, or Beacon with Local Network Access. Test **browser navigation request classes** separately: enforcement can differ even for the same public document, destination, method, and media type.

For endpoints whose raw-body fallback accepts JSON under `Content-Type: text/plain`, an HTML form can still serialize valid JSON despite inserting `name=value`. Absorb the mandatory `=` into a harmless padding field:

```javascript
const payload = JSON.stringify({input: {/* exact product request */}});
const form = document.createElement('form');
form.method = 'POST';
form.enctype = 'text/plain';
form.action = target;
form.target = '_blank'; // also test `_self` and a named hidden iframe separately

const input = document.createElement('input');
input.name = payload.slice(0, -1) + ',"__form_padding":"';
input.value = '"}';
form.append(input);
document.body.append(form);
form.submit();
```

The wire body ends as valid JSON plus form whitespace:

```text
...,"__form_padding":"="}\r\n
```

Validation rules:

1. Test direct top-level `_self`, new top-level `_blank`, and hidden/named iframe targets independently. A top-level navigation positive does not imply subframe delivery, and `_blank` matters because it can preserve the attacker page while the child navigates.
2. Preserve target-side `Content-Type`, `Origin`, `Sec-Fetch-Site`, `Sec-Fetch-Mode`, `Sec-Fetch-Dest`, full raw body, and exact canary. A representative navigation proof should show `text/plain`, `Origin: null` on HTTPS→HTTP downgrade, `cross-site`, `navigate`, and `document`—but claim only values actually captured.
3. Use a per-case invocation delta and unique canary. The fail-closed matrix should expect exact positives and exact zeros, then exit nonzero on any mismatch. A strong Chrome isolation matrix includes `fetch`, XHR, Beacon, hidden-iframe form, `_self` form, `_blank` form, fetch-via-307, and form-via-307.
4. Repeat positives in fresh profiles. Run a form-only headed control without accepting permission UI, so a headless-only artifact is excluded without contaminating the control by interacting with Local Network Access prompts.
5. Re-run the same asserted harness against a fresh published-package installation. Embed nearest `package.json` name/version and exact imported module paths into the result before deleting the temporary installation; separate source-build and published-runtime provenance.
6. Test ordinary `127.0.0.1` first. Treat numeric IPv4 canonicalizations (`127.1`, single-integer decimal, hex, octal) and IPv6 loopback `[::1]` as supplemental address cases, not prerequisites or substitutes for the direct proof.
7. Test public HTTP and HTTPS attacker documents separately, recording the actual final document URL. Do not infer one from the other.
8. Treat public 307 redirects, wildcard-DNS loopback aliases, `0.0.0.0`, LAN/public weak-host routes, and DNS rebinding as independent branches. Preserve negative controls rather than folding them into a broad “browser blocked” conclusion.
9. For DNS rebinding, a DNS service externally returning loopback is **not** success. Require the local target to capture the request and exact canary. Account for browser DNS pinning, live public connections, TTL/cache expiry, scheme upgrades, and same-port requirements. If a bounded controlled sequence changes DNS but no target request arrives, record that technique as tested-negative and do not claim rebinding.

This request-class split is a durable reportability lesson: “Chrome blocks public-origin fetch to loopback” can coexist with “the same Chrome version permits public-origin top-level form navigation to the same endpoint.” State the exact transport/version matrix rather than treating Local Network Access as a universal server-side request-integrity control.

Important interpretation details:

- A WebDriver/CDP page-context call is only useful when the harness also records the active public document URL/origin. Preserve the wire `Origin` separately; browsers may serialize `Origin: null` for an HTTPS-to-HTTP downgrade even though the active document is public.
- A public HTTP control must remain HTTP and allow `connect-src`; reject controls that redirect/upgrade to HTTPS or whose CSP blocks the request before address-space enforcement.
- Temporary tunnel hostnames can encounter stale local NXDOMAIN caching. A dedicated disposable browser may use DNS-over-HTTPS plus a host-resolver mapping to the tunnel provider's resolved public edge only as an evidence-recovery step: require valid TLS for the public hostname, preserve browser GET/tunnel request logs proving the page traversed the public service, disclose the mapping in the report, and retain an independent public-document control without that workaround when possible. Never describe a locally served page as public merely because its hostname looks public.
- `navigator.sendBeacon()` returning `true` means queued, not delivered. Check subsequent network errors and the server/marker before treating Beacon as a bypass.
- A headed WebDriver script timeout is not proof that a Local Network Access permission prompt appeared. Verify permission UI directly if the claim matters; otherwise label the timeout unresolved and run a form-only headed control without clicking or accepting permission UI.
- Use `set -o pipefail` when teeing PoC output, or preserve the underlying process status separately; otherwise a failed matrix can look like exit 0 because `tee` succeeded.
- Historical `0.0.0.0` or DNS-rebinding writeups are hypothesis sources, not evidence against the current browser. Current-browser negative controls can legitimately kill those escalation branches.

## Predictable default-session and state-injection escalation

After proving request delivery, inspect fallback behavior for omitted `appName`, `userId`, `sessionId`, and state fields. A route that silently selects predictable identifiers can turn an isolated invocation into injection into an existing privileged session.

Use an owned pre-existing-session control:

1. Pre-create the exact fallback app/user/session with sentinel state and zero events.
2. Send the browser request while omitting the identifiers that have defaults and include an attacker canary in the message and optional state delta.
3. Read the session locally after execution and compare before/after state and event count.
4. Preserve the ordered event sequence: attacker message/state, model tool call, tool response, and completion.
5. Prove any tool side effect independently with the same prompt-derived marker.
6. Frame this conditionally: existing-session injection is proven for the predictable fallback session; unrelated sessions still require their identifiers.

This branch can demonstrate session integrity loss, context poisoning, and inherited tool authority without reading the opaque browser response. Do not claim credential inheritance or secret access unless the controlled session actually contains and exercises that capability under a safe proof plan.

Before elevating predictable fallback identifiers into the main impact, search shipped clients, UI bundles, examples, and tests for call sites that actually omit the identifiers or use the fallback values. Check both source-level request types and built UI strings/flows: a client request interface that requires explicit `appName`/`userId`/`sessionId`, a runtime path that sends all three, and a UI that creates a session then reuses the returned ID are affirmative evidence that fallback collision is atypical in the shipped client path. Absence of fallback strings in a bundled UI supports that narrow conclusion but does not prove no third-party client uses them. Retain collision as a conditional aggravating factor rather than implying ordinary victim sessions use those keys. Preserve the search scope and distinguish “no call site found in this checkout/bundle” from a universal absence claim.

## Published artifact and raw-evidence gates

For OSS developer tools, do not infer affected released versions from a `main` checkout or changelog alone:

1. Inspect or reproduce against the actual published package/release artifact when available.
2. Record package name, exact version, archive integrity/hash, affected file path, and the relevant route/parser strings or runtime behavior.
3. Follow static archive inspection with a runtime proof against an isolated installation of the published package whenever its exported/deep-imported server can be started. Parameterize the same portable harness with package paths so source and release runs exercise identical cases.
4. Distinguish “one verified affected release” from the first affected version or a complete affected range. Enumerate every published version from the package registry and scan each archive for the route plus all behavior required by the exploit; preserve a machine-readable version matrix.
5. Runtime-test the current affected release even when older versions are only statically scanned. State the bounded conclusion precisely: for example, “route absent through X; route and parser present and runtime-proven in Y.”
6. Keep release-artifact verification separate from source-commit verification when the published build may differ. Record both core and devtool dependency versions from the isolated installation.

Do not let a handwritten summary stand in for raw browser/server evidence. When request headers matter to provenance or mitigations, instrument the proof server or browser harness to preserve the complete headers, raw body, destination alias, and a unique correlated canary in the machine-readable result. If the raw artifact does not contain a claimed `Origin` or Fetch Metadata value, qualify or remove that header claim even when the side-effect marker remains valid.

## Browser-boundary interpretation

Keep these claims separate:

- **Cross-origin request dispatch:** proven when a real browser causes the side effect.
- **Cross-origin response read:** requires ACAO/CORS proof and is unnecessary for CSRF impact.
- **Public-origin to loopback reachability:** may be restricted or permission-gated by Private/Local Network Access depending on browser and address-space context.
- **DNS rebinding:** requires its own Host/origin/address-space proof; absent Host validation is a lead, not proof of a successful rebinding exploit.
- **Universal RCE:** never infer this from agent invocation. State conditional downstream impact based on the loaded agent and enabled tool/confirmation model.

A two-loopback-origin Chrome proof validates the request-integrity flaw, but must be disclosed as `same-site`/local-origin evidence if that is what `Sec-Fetch-Site` shows. Do not silently generalize it to arbitrary public websites.

A distinct private-HTTP-origin positive to a loopback target is stronger than a same-loopback-port control because it proves real cross-origin form delivery, but it still does not establish a public-Internet drive-by. If both public HTTP and public HTTPS controls are negative, retain the private-origin result as a scoped LAN/private-origin integrity finding or defense-in-depth justification and say the public actor model is unproven. Testing public HTTP separately prevents mixed content from being treated as the only explanation for an HTTPS negative; it does not by itself identify LNA/PNA or headed/headless enforcement as the cause.

## Adversarial reportability gate

Promote only when all are true:

- the invoking origin is outside the service origin/trust boundary;
- default or realistic configuration accepts the safelisted request;
- a deterministic side effect proves agent/tool/job execution;
- the attacker gains incremental action capability rather than merely reading a public response;
- loopback/PNA/LNA, listener, authentication, and deployment caveats are explicit;
- targeting prerequisites are explicit: default/predictable port, valid application or agent identifier, server-running window, address alias, browser/OS support, enabled tool composition, and model behavior. An unreadable `/list-apps` response does not by itself solve cross-origin app-name discovery;
- predictable default-session evidence is framed as state/event integrity loss unless a separate safe control proves inherited credentials, authorization, or higher tool authority. A PoC-authored “privileged” sentinel is not privilege proof.

Before submission, run a hostile report critic pass:

1. Compare the title and every impact sentence against the strongest direct evidence, especially who chose the tool and constructed the command.
2. Separate intentional product capability from realistic prevalence: inspect experimental annotations, trusted-input warnings, defaults, official examples, integration tests, and deployed/typical use.
3. Verify the primary PoC is portable and reproduces the strongest unconditional claim without workstation-specific paths or undocumented companion processes.
4. Keep the report concise enough that weaker loopback controls, forged-Origin protocol checks, or raw evidence lists cannot obscure the public-origin/browser and side-effect proof.
5. Predict likely rejection/downgrade arguments—development-only listener, browser/version dependency, unknown app name, opt-in unsafe executor, mock-model mediation, remote IAM—and answer them with evidence or retain them as explicit limitations.
6. When later testing closes review blockers, add a dated closure addendum to the critical memo rather than rewriting history. Mark the original disposition as superseded, enumerate each closed blocker with its artifact, and retain unresolved/conditional branches. This prevents stale “HOLD” guidance from contradicting a revised submission-ready report while preserving the audit trail.
7. Reconcile late asynchronous reviewer output against the **current** artifact state, not the state at dispatch time. Classify each recommendation as already closed, still open, or newly surfaced. Act only on the latter two; when a new control changes the portable harness, rerun every affected source and published-package matrix, revalidate machine-readable assertions, refresh report wording, and regenerate the integrity manifest.

Prefer a balanced report split:

- **The problem:** parser/content-type discrepancy plus missing request-integrity validation.
- **Impact analysis:** unauthorized invocation/session mutation first, followed by conditional tool authority.
- **Not claimed:** hosted production compromise, universal or reliably attacker-directed RCE, secret theft, inherited session privilege, successful DNS rebinding, or browser-universal public-to-loopback reachability unless separately proven.

## Finalization and severity calibration

When the user asks to explain, finalize, and critically review the finding, create a new final submission artifact rather than silently mutating the historical draft/review into a contradictory record:

1. State the vulnerability in one trust-boundary sentence, then separate **proven**, **conditional**, and **not proven** consequences. Do not let proof from different browser controls collapse into one stronger same-run claim; say when delivery and session mutation were independently demonstrated through the same route.
2. Default to impact facts rather than requesting a severity or CVSS score. If the user or submission form explicitly asks for severity, rate only the strongest **unconditional** impact: exclude mock-model tool choice, opt-in unsafe executors, hypothetical credentials, and undocumented downstream actions from the base severity. Prefer one conservative severity/vector with metric rationale over a broad score range, and explain what additional real application-side proof would justify an upgrade.
3. Treat local-development context, server-running window, known/reachable port, valid application name, unreadable response, and user page visit as explicit acceptance and impact factors—not hidden caveats and not reasons to erase proven integrity loss.
4. Re-check the live official program tier/scope source at finalization time. Program-policy reward language is context for likely triage treatment, not product-specific proof.
5. Run a fresh hostile review against the **final** file. Use a gate table covering scope, released artifact, root-cause causality, real-browser provenance, target-side side effect, portability, negative controls, overclaim boundaries, regression tests, and proportional severity. Enumerate likely triage objections and residual risk even when the verdict is submission-ready.
6. Before declaring readiness, mechanically verify every referenced evidence path exists, machine-readable positive artifacts still assert success, code/harness syntax passes, Markdown fences are balanced, prohibited overclaim phrases are absent, and the product checkout is clean. Build assertions from each artifact's actual schema: inspect its keys/fields first instead of guessing names from prose or a sibling artifact. If an assertion fails, distinguish a verifier-field mismatch from a failed finding before changing report conclusions.
7. Update target ledgers and next-action notes to point to the final report and final critical review, not a superseded balanced draft. Preserve the old critic memo as audit history. Do not submit automatically unless the user explicitly requests submission.
8. If the final report is long, lead the portal body with summary, severity, primary reproduction, proven impact, and non-claims; attach or offer large raw matrices separately. Remove the conditional executor subsection entirely when form limits or triager-focus risk outweigh its contextual value.

## Remediation layers

Recommend defense in depth:

1. reject untrusted/missing Origin on browser-facing state-changing routes;
2. require `application/json` and remove arbitrary-media-type raw-body JSON fallback;
3. require authentication or an unguessable CSRF token;
4. validate Host against the configured listener;
5. reject unexpected `Sec-Fetch-Site` / `Sec-Fetch-Mode` where compatible;
6. preserve loopback binding for local development and document external deployment authentication requirements.

## Video PoC evidence gate

When a triager asks for a video, do not treat a polished harness summary as sufficient by itself. Make the recording independently legible and correlated:

1. Show the product starting, exact listener/port, browser/version, and tested application or agent.
2. Show the attacker-controlled page's real origin in the browser address bar, the request primitive, target, unique canary, and automatic/user-interaction behavior.
3. Show target-side evidence—not only page-side status—including the captured media type, Origin/Fetch Metadata, exact raw body, and unique canary.
4. Show a meaningful before/after side effect from the product's own state store or marker, preserving any victim sentinel and correlating the same canary through request and effect.
5. Link the runtime behavior to the affected parser/handler path on screen or in an adjacent source walkthrough. Keep conditional impact separate.
6. End with machine-readable assertions and the real process exit code. Package a sanitized raw result when the rendered screens are harness-authored.
7. Prefer one continuous sequence. For tunnels or slow prerequisites, have the harness emit a readiness marker after DNS/TLS/server checks and start screen capture only then, before launching the browser. This removes idle setup without an evidence splice.
8. Decode the entire finished video, sample frames from each stage, scan rendered/supporting artifacts for secrets and private paths, and hash the upload copy. Reject any run whose underlying assertions failed even if the recorder exited zero.
9. Keep the requested video focused. Full negative matrices and long logs belong in portable artifacts unless the reviewer specifically asks to see causal controls on video.

## Verification pitfall

Monorepo test filters are often resolved from the repository root even when a package owns the test. If a workspace-scoped command returns “No test files found,” correct the path/filter and rerun from the root; never count the empty discovery result as a pass. Record the corrected passing command, not the transient failed invocation as a durable tool limitation.
