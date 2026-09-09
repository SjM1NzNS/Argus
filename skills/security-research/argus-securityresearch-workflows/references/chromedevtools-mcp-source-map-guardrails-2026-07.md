# ChromeDevTools MCP source-map guardrails pattern (2026-07)

Use when hunting ChromeDevTools MCP browser-boundary issues involving page-controlled source maps and URL allow/block guardrails.

## Safe proof pattern

1. Keep proof local-only with a loopback HTTP server and isolated/headless Chrome.
2. Configure ChromeDevTools MCP with explicit `blocklist` or narrow `allowlist` values.
3. Add a page-controlled JavaScript `//# sourceMappingURL=...` comment pointing at a blocked or unallowlisted source map.
4. Use unique per-case markers in source-map `sources[]` to avoid cache ambiguity.
5. Compare normal runtime controls (`fetch`, image, worker, WebSocket, redirects) against DevTools/source-map behavior.
6. Include an absolute cross-origin source-map case when strengthening URL-guardrail findings: serve page/script from loopback server A, serve source map plus a normal-fetch control endpoint from loopback server B, then prove normal `fetch()` to B is blocked while `//# sourceMappingURL=http://127.0.0.1:<B>/...map` is still fetched by DevTools and reflected through MCP output.
7. Verify product output through `get_console_message`, not just server logs.
8. Add negative controls: roots/guardrail enabled, unique URL paths, normal runtime fetch blocked, and final redirect URL checks.

## Reportability gates

- Report conservatively as low severity unless arbitrary response-body disclosure, sensitive data access, or a common accepted client/default actor model is proven.
- Do not claim arbitrary file/response disclosure if only `sources[]` metadata is reflected.
- Before attempting to upgrade severity, run a field-reflection probe with unique markers in `sources[]`, `sourceRoot`, `file`, `names[]`, and `sourcesContent`; in the 2026-07-09 ChromeDevTools MCP run, only `sources[]` reached `get_console_message`, while `sourceRoot`, `file`, `names[]`, and `sourcesContent` did not.
- Do not claim the source-map fetch appears in `list_network_requests` unless product output proves it; in the 2026-07-09 check, it did **not** appear there.
- An absolute cross-origin source-map proof strengthens the request-capability argument, but it still does **not** upgrade the claim to arbitrary body disclosure or full SSRF unless response bytes beyond source-map metadata are reflected.
- DevTools internal workspace/source-map objects may be able to access blocked `sourcesContent` after the fetch. Treat that as a lead only: it is report-impactful only if an existing MCP-exposed product/tool response returns the workspace/search/UISourceCode content to the MCP client.
- In the 2026-07-09 upgrade pass, raw trace, Lighthouse reports, CSS source-map variant, and `get_console_message` did not expose source-map body content; only internal `embeddedContentByURL()` / `UISourceCode.searchInContent()` saw it.
- Quote or acknowledge project `SECURITY.md` language if it says URL guardrails are not a complete network sandbox.
- Avoid internal-network/metadata probing; loopback proof is enough to demonstrate guardrail inconsistency.

## Evidence to preserve

- Harness script.
- JSON result with blocklist/allowlist, observed server events, and MCP output booleans.
- Product output from `get_console_message` showing unique marker reflection.
- Product output from `list_network_requests` and `list_console_messages` when used as adversarial controls.
- Field-reflection downgrade JSON/log when severity depends on whether source-map body or non-`sources[]` fields are exposed.
- Adversarial validation explaining limitations and exact non-claims.
