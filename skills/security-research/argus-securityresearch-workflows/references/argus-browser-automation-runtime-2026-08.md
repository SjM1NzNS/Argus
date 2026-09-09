# Argus browser automation runtime — durable operating pattern

Use this reference when changing scheduled browser acquisition, source triage, CDP control, or background GUI access. It complements the class-level source-first and learning-architecture rules; it does not authorize target testing.

## Retrieval/control router

1. Prefer static/feed acquisition when it is sufficient. Do not start a browser for an empty browser lane.
2. Use isolated headless Playwright for public dynamic roots and source-derived JavaScript/network mapping.
3. Use a dedicated localhost CDP profile for advanced Network/Runtime/Page control or persistent agent state. Never attach the user's normal Chrome profile implicitly.
4. Use `computer_use` only for visible/native interaction that browser-native control cannot satisfy. Require `hermes computer-use doctor` success and explicit authorization before touching a signed-in browser.

## Shared runtime and egress invariants

- Keep one shared browser policy/runtime module rather than separate Selenium/Playwright implementations.
- Create one fresh context per source or target/account boundary; disable downloads and service workers unless a task explicitly requires them.
- Keep sandboxing enabled by default. Any no-sandbox mode must be explicit, justified, and bounded.
- Do **not** treat a Python DNS pre-check plus `route.continue_()` as redirect-safe SSRF protection: Chromium can resolve again, Playwright routing may miss redirect hops, and ordinary context routing does not enforce WebSockets.
- Put learning Playwright and dedicated CDP Chrome behind a fail-closed localhost forward proxy. The proxy must reject the destination if **any** DNS answer is disallowed and connect to the exact validated IP while preserving HTTP `Host` and TLS SNI. Revalidate each proxy request so redirects and subresources cross the same gate.
- Use one shared **strict global-unicast** predicate in the Playwright/static URL guard and proxy. Do not rely on `ipaddress.is_global` alone: explicitly reject private, loopback, link-local, multicast, reserved, unspecified, deprecated IPv6 site-local, IPv4-mapped/compatible forms, unsafe NAT64 embeddings, and unsafe transition/tunnel forms. Add literal and mixed-answer tests for each special class.
- A caller timeout around `asyncio.to_thread(socket.getaddrinfo, ...)` is not a hard resolver bound because the libc resolver thread survives cancellation. Resolve in a killable worker subprocess (or a genuinely cancellable async resolver), cap output/answer count, kill and reap on timeout, apply one aggregate deadline across a capped set of connection attempts, and bound handler lifetime/stream idleness.
- Prevent browser bypass: remove implicit loopback proxy bypass, disable QUIC and non-proxied WebRTC UDP, and make the CDP service depend on the proxy. Verify with a temporary loopback server that CDP, redirect, and subresource attempts produce zero server hits.
- Disable all WebSockets in source-acquisition lanes with `route_web_socket` unless a specific workflow proves they are required. Record sanitized blocked attempts. A response-event `resource_type == websocket` branch is not enforcement.
- Keep a lightweight Playwright URL-policy layer for unsafe schemes, credentials, literal private destinations, top-level `data:`/`blob:`, and tracker suppression; the pinned proxy is the connection-level authority.
- Replace fixed sleeps with bounded lifecycle/content conditions. Wrap each page operation and the whole async lifecycle in hard timeouts and add a shell `timeout --kill-after` deadline.
- DOM item-count limits are not memory limits. Avoid full `innerText`, `Array.from(querySelectorAll(...))`, and unbounded performance-entry materialization. Walk text/elements incrementally, stop at scan and output limits, cap title/URL/attribute strings before browser-to-Python transfer, report lower-bound totals when traversal stops, and enforce per-event plus whole-evidence byte budgets before persistence.
- Bounded extraction must also preserve **semantic visibility**. Do not count text under `script`, `style`, `noscript`, `template`, SVG, hidden/inert, `aria-hidden`, or inline hidden-visibility ancestors as page/article content. Add a real-browser fixture where large serialized application state coexists with a small visible body; assert only visible text influences content quality. Separately inspect the semantic article container and platform lock/paywall state before labeling a capture `actual_content` or `full_text`.
- Bound the browser process tree as well as wall time. Run production wrappers in a transient user-systemd scope with `MemoryMax` and `TasksMax` (or an equivalent cgroup), and put persistent CDP Chrome under matching service bounds. Setup smoke must prove the cgroup mechanism is available.

## Safe evidence and failure pattern

For each isolated source context, persist a bounded private evidence directory containing a manifest and redacted network ledger:

- mode `0700` directories and `0600` files, including generated Markdown reports;
- browser/version, **confirmed** context policy, redirect/wait state, telemetry callback failures, and SHA-256 of the ledger;
- exact telemetry accounting: `blocked_request_total`, retained/recorded sample count, dropped blocked-sample count, event count/bytes, truncated-event count, dropped-event count, and dropped-event bytes;
- URL userinfo removed; all query/fragment values redacted; UUIDs, magic-link/reset capabilities, percent-encoded tokens, opaque path segments, sensitive path-key/value pairs, and opaque parameter names redacted;
- valid bracketed IPv6 reconstruction, normalized IDNs, and a final sanitized-URL byte cap;
- authorization, cookies, CSRF/XSRF, API keys, tokens, sessions, secrets, and unapproved response-header values redacted;
- JavaScript, source-map, and source-derived API/JSON inventory with ad/analytics noise suppressed; WebSockets are blocked rather than advertised as acquired surfaces.

Never persist raw exception text: browser errors can echo credentialed or capability URLs. Store controlled `error_stage`/`error_code` values. Do not assert context isolation, download policy, or service-worker state until context creation and policy attachment succeeded; use `not_created` for startup failures and still write an explicit failure manifest. Run-level Markdown/JSON must be derived from manifests and records, not policy intentions: distinguish `not_started`, `started`, and `failed`; report contexts requested/created, roots attempted/succeeded/failed, exact versus sampled telemetry counts, callback errors, and truncation. Label unexercised controls as **configured**, never observed.

Return nonzero for launch failure, any required-root failure, zero successful roots after a non-empty selection, or total-budget expiry. Preserve partial diagnostics, but suppress compilation/promotion and propagate the component failure through combined and weekly orchestrators. An empty selected lane must return before Playwright import/startup.

Use raw canonical URLs only in memory. Put URL identity in one shared static/browser helper and persist keyed HMAC identities so query variants do not collide after evidence sanitization and capability URLs are not stored reversibly. When introducing this to an existing seen-state file, migrate under the same exclusive lock: transform every legacy raw key, canonicalize before HMAC generation, normalize naive and aware legacy timestamps to UTC, let a valid timestamp outrank malformed values, deterministically merge collisions, atomically **replace** the `urls` bucket, remove raw keys, set a scheme marker, enforce mode `0600`, and assert that zero `http://`/`https://` keys or values remain **anywhere in the complete state document**. Audit top-level keys and legacy/metadata buckets as well as `state["urls"]`; a clean nested HMAC bucket does not compensate for stray raw top-level entries. An additive merge cannot perform this migration safely, and a browser-only HMAC implementation leaves the shared static state exposed. Test top-level and nested keys, canonical collisions, malformed/mixed-timezone timestamps, and bracketed IPv6 default/non-default ports.

When component runs are combined, copy the evidence directory into the combined run so every relative `browser_evidence_manifest` path still resolves. Verify the copied network ledger against the recorded SHA-256; a valid component artifact with a broken combined-run pointer is not a complete handoff.

## Reproducible Playwright environment

Use a dedicated venv with exact direct and transitive dependency pins. `uv pip sync` treats the input as the complete environment, so a direct-only requirements file can remove Playwright's transitive dependencies. Either use a fully resolved lock or use dependency-resolving installation.

Choose one launch strategy deliberately:

- install the pinned Playwright browser with the pinned interpreter; or
- select a validated system Chrome executable explicitly in every production wrapper.

A successful Python import is not proof that a driver and browser are launchable. Setup verification must import `playwright.async_api`, locate the driver/CLI, and perform a real bounded sandboxed launch/close with the same proxy and launch options production uses. Distro-patched Playwright may require `PLAYWRIGHT_NODEJS_PATH`, but prefer the package's bundled driver when present.

## Dedicated CDP service

- Bind the control endpoint only to `127.0.0.1` and use a dedicated private profile; never point it at the user's normal signed-in profile.
- `--remote-debugging-address=127.0.0.1` protects only the control listener, **not browser egress**. Require the exact-IP-pinning proxy service, configure Chrome to use it without loopback bypass, and disable non-proxied UDP channels.
- Use `--remote-allow-origins` scoped to the localhost endpoint and do not add `--no-sandbox` implicitly.
- Verify HTTP discovery, WebSocket CDP connection, `Network.enable`, `Page.navigate`, and `Runtime.evaluate`.
- Verify egress separately: navigate through CDP to a temporary loopback HTTP server and assert a browser error plus zero server hits. A public smoke alone does not prove private-network denial.
- Hermes CDP tools are registered from startup configuration; changing `browser.cdp_url` during a session normally benefits the next session.

## Background GUI environment

If the gateway lacks graphical environment variables, add a user-service drop-in for `DISPLAY`, `XAUTHORITY`, and `XDG_RUNTIME_DIR`, then run the doctor with those values. Do not restart the gateway from inside unfinished work; apply the restart after the active session is safely complete.

## Tests-first and verification checklist

1. Add failing tests for proxy destination parsing, credential rejection, mixed public/private DNS answers, exact validated-IP connection, private CONNECT denial before connection, WebSocket closure, URL/header/error redaction, HMAC URL identity, context truthfulness, bounded evidence/DOM extraction, timeout propagation, and combined-run evidence paths.
2. Run the focused red test, implement minimally, and rerun green.
3. Run the complete architecture suite, AST/byte compilation, shell syntax, systemd-unit verification, registry validation, and manifest-consumer schema tests **after the last edit**. A unit-green recorder can still break production if a consumer expects a renamed telemetry field; treat a real bounded lane run as a schema-contract test.
4. Exercise empty production and triage selections with an intentionally unusable browser path to prove no startup occurred.
5. Force launch failure and total-budget expiry. Require nonzero exits, controlled private failure records, truthful manifests and run summaries, preserved combined diagnostics, and compiler suppression.
6. Run one bounded public source through production ingestion and triage; verify permissions, hash binding, context isolation, exact/sample telemetry counters, byte/traversal truncation fields, and tracker handling. A tracker may legitimately appear in a sanitized blocked-request sample or bounded network ledger; it must not appear in the source-artifact or learning-candidate inventory.
7. Verify operational seen state after mixed static/browser execution: scheme marker present, mode `0600`, stable HMAC query identities, and zero raw URL keys/values under a recursive walk of the entire state document (including top-level and legacy buckets).
8. Exercise the two-lane combined orchestrator in isolated HOME/state paths and resolve every evidence pointer from the combined run.
9. Verify proxy public fetch, strict special-address and mixed-answer denial, private CONNECT denial, CDP loopback denial with zero sink hits, public-to-private redirect denial, and WebSocket denial. Use temporary owned sinks; never infer connection blocking from an error page alone.
10. Dispatch independent review after remediation. Do not claim closure until the result returns, every P1/P2 is resolved or explicitly accepted, and the full suite/live smoke is rerun after those fixes.
11. Do not modify mature playbooks/evals during runtime verification; use temporary roots and proposal-only staging.

## Review-discovered invariants and closure pitfalls

- Treat **every network acquisition lane** as an SSRF boundary. Static roots, `robots.txt`, and library-managed redirects must use the same mandatory loopback proxy as browser traffic. An explicit proxy that still honors `NO_PROXY` is not mandatory; tests must set hostile `NO_PROXY=*`/`no_proxy=*` and prove the request remains proxied. Build static openers from an HTTP(S)-only handler allowlist: urllib otherwise installs direct FTP/file/data handlers, so an HTTP redirect to FTP can escape the proxy.
- Static safety includes persistence. Keep operational discovery/redirect URLs in memory, sanitize every persisted root/effective/discovered URL with the shared evidence sanitizer, and replace urllib exception text with controlled error codes. Test short numeric codes, double-encoded path separators, and semicolon capability parameters as well as long opaque tokens.
- Validate the proxy setting once through a shared parser. Accept only credential-free `http://127.0.0.1:PORT` or `http://[::1]:PORT` with `1 <= PORT <= 65535`; reject `direct://`, remote hosts, userinfo, missing/zero/malformed ports, and non-empty path/query/fragment components. Shell launchers should call the shared validator rather than duplicate URL parsing, and persistent CDP units should pin the intended endpoint explicitly rather than inherit an arbitrary loopback proxy.
- Cancellation safety is broader than timeout handling. Resolver children must be killed and reaped on timeout, explicit task cancellation, and other failures; suppress the exit/kill race and shield reaping from repeated cancellation. Put semaphore acquisition inside the aggregate connection-lifetime deadline so queued accepted sockets cannot wait indefinitely. Context-close failures must not bypass recorder persistence: record a controlled cleanup error, write the manifest, and then propagate truthful fields.
- Producer/consumer schema checks are mandatory for bounded evidence. If extraction emits `*_lower_bound` fields, every ingest/triage record and summary must preserve that name or explicit semantics; never silently fall back to captured length and call it a total. Add an end-to-end consumer assertion, not only an extractor unit test.
- Track browser launch, context creation, and context-guard readiness as separate states. Aggregate retained/truncated/dropped event counts and bytes plus blocked total/recorded/dropped samples from manifests, not from intended policy.
- State migration must recursively audit the complete document. Legacy raw URL keys can sit at the top level even when `state["urls"]` is clean. Remove them under the same lock, atomically rewrite, and verify zero raw URL keys/values plus mode `0600` without printing the URLs.
- An explicit source allowlist is authoritative in **every cadence**, including compatibility/legacy modes. Never let a legacy branch silently ignore `ARGUS_SOURCE_FILTER`; test an exact valid source ID from the opposite lane and require a zero-source browser run with `not_started`, `0/0` context, and no network work.
- Run browser integration with the production browser interpreter/venv, not whichever system Python happens to import a distro Playwright shim. The durable check is a real system-Chrome launch using the same interpreter and launch options as production.
- Closure evidence must be from **after the final edit**. Adding a regression test after a green run invalidates the old suite count until that test is implemented and the complete suite is rerun. Do not summarize a prior green run as current status, and do not mark review complete while a follow-up independent verdict is still outstanding.

## Zone 0 corroboration

Preview.is retrieval on 2026-08-11 independently corroborated the redirect/rebinding threat model: [StackShield](https://stackshield.io/blog/laravel-ssrf-http-client-vulnerability) (`0.9945`) says every redirect target must be revalidated and validated addresses pinned; [IntruderLabs](https://intruderlabs.com.br/en/blog/ssrf-bypass-techniques) (`0.9759`) likewise recommends strict scheme/host policy, private/reserved-address rejection, exact-IP connection, redirect revalidation, and egress segmentation. These are external Zone 0 sources, not proof of the Argus implementation; local tests, live owned sinks, manifests, and independent review remain the acceptance evidence.
