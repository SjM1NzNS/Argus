# OIDC and Keycloak Source-First Validation

Use this reference when an in-scope web application delegates login to Keycloak or another OIDC provider and the public source/redirect chain exposes the client, realm/issuer, callback, PKCE parameters, registration, recovery, or theme resources.

## 1. Preserve the exact application transaction

Acquire the application entry point without automatic redirects, then parse the exact authorization URL from `Location`. Preserve private raw headers/body with restrictive permissions, but promote only:

- authorization origin and path;
- query-key names, never opaque values;
- client ID when it is a public client identifier;
- callback origin/path;
- response type, scope names, and PKCE method;
- lengths and uniqueness verdicts for `state`, `nonce`, and `code_challenge`, not their values.

Capture at least two independently initiated normal transactions before claiming uniqueness. Distinguish the three controls: `state` binds the browser transaction, `nonce` binds the ID token, and PKCE binds code redemption. Presence of one does not substitute for another.

## 2. Run a bounded no-follow redirect validator

Create a fresh normal authorization URL, change only `redirect_uri`, and use no-follow requests. A minimal matrix is:

1. exact registered callback positive control;
2. same-origin alternate path;
3. HTTP downgrade of the legitimate callback;
4. reserved external origin such as `https://redirect-test.invalid/cb`;
5. userinfo confusion such as `https://researcher@example.invalid/cb`;
6. suffix confusion such as `https://legitimate.example.redirect-test.invalid/cb`.

Never follow an accepted external redirect. Record status, sanitized `Location` origin/path/query keys, and a bounded visible error summary. Do not print state, nonce, code challenge, session code, execution ID, tab ID, or opaque action URL values.

An accepted same-origin alternate path is not code theft by itself. Before promotion, prove a separate same-origin read/exfiltration primitive and account for PKCE. Test callback normalization with an invalid code/state plus a reserved external `redirect` value; if the application starts a fresh transaction and canonicalizes `redirect_uri` back to the fixed callback, disposition the wildcard as non-impactful absent another chain.

## 3. Callback controls

Use only inert controls before an owned account exists:

- callback with no parameters;
- callback with deliberately invalid code/state;
- invalid code/state plus a reserved external redirect parameter.

Expected secure behavior is return to the application or a fresh OIDC transaction with new state/nonce/PKCE. Never replay a real authorization code, intercept another user's flow, or redeem a code without its owned verifier.

## 4. Browser User-Agent gate

When a program mandates an exact User-Agent, verify it from the browser runtime before target navigation:

```js
navigator.userAgent
```

For a dedicated CDP browser, also verify `/json/version`. If the existing process uses the wrong UA, first prove it uses the isolated agent profile, restart only that process with the required `--user-agent`, then recheck. Do not assume a curl UA carries over to browser traffic. Do not repurpose or terminate the user's normal browser profile.

If desktop capture is unavailable, CDP may navigate and inspect the rendered DOM, but it must not become CAPTCHA automation or credential handling. Passwords, TOTP, recovery codes, and CAPTCHA completion remain manual even when the user provides a value in chat.

## 5. Registration and recovery gates

Registration/recovery GETs may be mapped from rendered links. Record form method, action origin/path, field names/types/autocomplete, CAPTCHA provider origin, and password-policy text without values.

Do not:

- type, retain, echo, or submit passwords;
- automate or bypass CAPTCHA;
- send enumeration probes when the program excludes account/email enumeration;
- trigger repeated reset or verification messages;
- register more than the approved owned account.

Park the dedicated browser at the form and record zero-length password/confirmation/CAPTCHA controls. Resume only after the user manually completes the gate.

## 6. Static-resource version fingerprinting

A public Keycloak theme script can establish a version floor or range:

1. hash the exact served bytes;
2. locate the canonical upstream path in the public repository;
3. fetch a small, relevant tag range;
4. compare byte length and SHA-256;
5. report all matching tags and the nearest non-matching predecessor.

An unchanged file across several releases does **not** identify the deployed patch level. Phrase the result as “served file matches upstream versions X–Y,” not “server runs version X.” Use it to exclude clearly old CVEs only when every plausible matching release is beyond the fixed version.

For a CVE lead, require the primary advisory or an equivalent high-confidence source, exact affected/fixed range, privilege prerequisite, deployed feature prerequisite, and a safe proof path. Search snippets and advisory-package aggregate pages are discovery only. If applicability remains ambiguous, do not send the payload.

## 7. Capability and action disposition

Standard OIDC discovery is protocol-derived rather than endpoint guessing, but an edge error or HTML maintenance page is not a capability document. Preserve the response and record discovery as blocked; do not infer supported grants or registration behavior.

For exact source-embedded portal actions (for example a personal-bar render URL), use a fresh guest session and a read-only request only when state semantics are clear. An empty redirect to a fresh OIDC challenge closes guest disclosure for that action; it does not prove every authenticated authorization path safe.

## 8. Evidence and verifier hygiene

- Set tool-output directories to `0700` and files to `0600`.
- Validate secret redaction specifically inside `findings.secret_candidates`; route and object records may legitimately contain a `value` key.
- A candidate is safe only when its secret value is `<REDACTED>` and no `sample`, `literal`, `raw`, or equivalent plaintext field exists.
- Inspect a script's real `--help` before invoking it. If `extract_source_inventory.py` accepts only `--input` and `--output`, keep provenance in an adjacent evidence manifest; do not invent unsupported CLI flags.
- Re-run permission, JSON, redaction, and browser-field-length checks after the final note/log write.

## 9. Disposition language

Use precise outcomes:

- `rejected_cross_origin` — provider rejected the redirect variant;
- `same_origin_only_no_chain` — alternate path accepted but no code/verifier exfiltration primitive;
- `callback_canonicalized` — attacker redirect input did not survive into the fresh transaction;
- `blocked_on_manual_account_gate` — password/CAPTCHA required;
- `version_range_only` — static file matches multiple upstream releases;
- `version_infeasible` — all plausible releases postdate the fix;
- `configuration_unproven` — CVE requires Policy Enforcer, UMA, client-registration privilege, or another feature not evidenced by source/runtime.

Do not convert a blocked authenticated branch into “safe.” Preserve it for resume.
