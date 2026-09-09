# Local-service bind-scope validation and reportability

Use this pattern when a CLI, developer tool, report viewer, MCP server, dashboard, or embedded HTTP helper claims to serve on `localhost` or “locally.”

## Source gate

1. Freeze the reviewed commit/version and hash the relevant implementation and documentation files.
2. Compare user-facing wording and logs with the actual listen address.
3. In Go, `Addr: ":PORT"` or `ListenAndServe(":PORT", ...)` is a wildcard bind, not loopback-only. Equivalent wildcard forms exist in other runtimes (`0.0.0.0`, `::`, omitted host).
4. Check for authentication, Host/Origin validation, TLS, explicit remote-bind opt-in, and warnings.
5. Do not treat an explicitly documented remote bind as a vulnerability without a separate boundary failure.

## Runtime proof pattern

Use only a fake canary report or synthetic response body.

1. Confirm the intended loopback path returns the canary.
2. Enumerate one non-loopback address on the test host.
3. Request the same service through that address with proxies disabled.
4. Start an equivalent listener explicitly bound to `127.0.0.1` on another port and show that the non-loopback request fails.
5. Record status, body-canary presence, listener address, selected non-loopback address, and whether the negative control was reachable.
6. Stop the service, verify the port is closed, remove temporary source hooks, and confirm the upstream clone is clean.

For an in-package Go probe, an isolated single-file lint may report existing package symbols as undefined because it does not compile the whole package. Fix genuine syntax/import errors, then use a targeted `go test ./path/to/package -run '^TestName$' -count=1 -v` as the authoritative execution check.

The loopback-only negative control matters: it distinguishes wildcard binding from proxy behavior, generic host routing, or a flawed assumption about interface reachability.

## Impact and false-positive gate

Separate the primitive from reportability:

- Proven baseline: reachable peers can access the served content while the helper is running.
- Stronger stateful/API proof: if the peer can enumerate an app/agent, create an attacker-chosen user/session, read its marker back, and invoke the agent, prove that sequence. This removes dependence on guessing an existing victim session; treat existing-session, artifact, or debug-trace access as conditional secondary impact.
- CORS is not access control for a direct network peer. Browser CSRF is a separate branch and needs browser-generated request proof; an in-process `text/plain` request test alone is supporting evidence, not a browser-delivery result.
- Not automatically proven: public-internet exposure, firewall bypass, DNS-rebinding exploitation, browser-readable cross-origin access, secret theft, code execution, or universal tool execution.
- Preconditions: process active, port reachable, host routing/firewall permits access, and served content or actions have meaningful confidentiality/integrity value.
- Sensitivity examples: private dependency/package names, versions, source paths, vulnerability inventory, container composition, local project metadata, stateful session APIs, or privileged tool/API actions.
- For agent APIs, stop safely at deterministic no-tool invocation if that proves unauthorized execution of the agent path. Describe any configured-tool or ambient-credential consequence as conditional unless an inert tool proves it.
- Downgrade when the data is public/low-value, remote binding is explicit, authentication exists, realistic peers cannot reach the service, or the application author deliberately selected a remote bind.

Use external RAG for mitigation/reportability context, but treat local source and runtime evidence as proof. Cite retrieved URLs and avoid importing broad localhost/DNS-rebinding claims that were not exercised.

## Shared local/cloud launcher remediation

If the same launcher also serves Cloud Run, Agent Engine, containers, or orchestration, expect a triager to argue that wildcard binding is intentional. Separate deployment support from local defaults:

- add an explicit host/bind-address option;
- default local development to `127.0.0.1` (and deliberately handle IPv6 loopback if desired);
- make generated deployment commands pass `0.0.0.0` explicitly;
- require authentication or a clear warning/opt-in for non-loopback mode;
- make startup logs reflect the actual listener scope.

This preserves cloud deployment while fixing the localhost-described local boundary.

## Report framing

Prefer a balanced structure:

- **The problem:** documentation/logs promise localhost; implementation binds wildcard; handler lacks the relevant boundary control.
- **Impact analysis:** identify exactly what reachable peers can obtain or invoke, list process/network prerequisites, and state that public exposure was not tested unless it was.
- **Suggested remediation:** bind explicitly to `127.0.0.1` and optionally `[::1]`; require an explicit bind-address option for remote access; add authentication/TLS or recommend an SSH tunnel for remote use; add a regression test.

Do not assign high severity from wildcard binding alone. Preserve as a validated candidate when the technical proof is strong but program acceptance depends on variable content sensitivity or LAN reachability.

## Session examples

- A later ADK-style agent API review strengthened the class: the non-loopback client enumerated the safe agent, created and read an attacker-chosen in-memory session, and invoked a deterministic no-tool agent exactly once. Because no victim session identifier was needed, the candidate survived adversarial review while still avoiding Internet/RCE/tool-compromise claims.

For the stateful agent-API proof recipe, browser `text/plain` distinction, deployment-intent objection, and evidence bundle, see `local-agent-api-wildcard-bind-2026-07.md`.
