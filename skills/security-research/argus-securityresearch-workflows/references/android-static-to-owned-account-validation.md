# Android Static Recon to Bounded Authenticated Validation

Use this reference for scoped Android bug-bounty work that starts from an official app package and may later require researcher-owned accounts.

## 1. Establish official package provenance

1. Resolve the app from an official store listing and record app name, developer, package ID, store URL, update date, and version metadata.
2. Prefer first-party store acquisition. If accountless direct acquisition is unavailable and scope permits a mirror fallback, label it explicitly as mirror-derived.
3. For XAPK/split packages, record the container hash and every split hash.
4. Verify all APK splits share one signer certificate.
5. Check source-stamp/signing-scheme verification when available. A historical signer organization that differs from the current brand is not automatically suspicious when package identity, store ownership, uniform split signing, and source stamp align.
6. Preserve raw artifacts privately; never treat package availability or signer metadata alone as a finding.

## 2. Static-first extraction

Use two independent decoders when practical:

- `apktool` for authoritative manifest/resources/network-security configuration;
- `jadx` for supplementary Java/Kotlin route, auth, WebView, and telemetry analysis.

A partial JADX decompile can still be useful when apktool succeeds. Record decompiler error counts and avoid treating malformed decompiler output as authoritative.

Build reproducible inventories for:

- package/version/SDK/permissions/application flags;
- exported components, intent filters, app links, custom schemes, callbacks;
- network-security config, cleartext exceptions, user/debug CA behavior;
- first-party and third-party hosts;
- Retrofit/GraphQL routes, methods, auth requirements, object selectors, and mutation semantics;
- WebViews, JavaScript bridges, file/content access, URL-navigation policy, and added auth headers;
- candidate keys/tokens/client IDs with plaintext suppression;
- native libraries and split topology.

Classify every extracted host against the authoritative exact-scope list before any request. Third-party SDK/service URLs remain context only.

## 3. Redaction and false-positive gates

- Store candidate key/token values by resource name, length, and hash unless plaintext is operationally required in a private `0600` artifact.
- Public Auth0 client IDs, Firebase identifiers, Braze/Datazoom/Datadog client tokens, source maps, API bases, and codec/config lists are leads—not findings.
- Require a capability matrix or concrete boundary impact before reporting client-side values.
- Exported Android media/system components are not findings without an unprotected sensitive action or data boundary.
- Cleartext exceptions are not findings without sensitive traffic that actually uses them.
- Auth-required `{userId}` routes are BOLA candidates only; require two researcher-owned identities and positive/negative controls.

## 4. Resolve the complete live request before dispatch

Do not request a literal base URL merely because it appears in resources. Trace the base through its consumer interface and resolve appended child paths, query parameters, platform IDs, config suffixes, and client IDs locally first.

This avoids low-value empty directory/CDN objects and yields an exact app-equivalent request. If a bounded request returns an empty base object, do not guess children; return to static call-site tracing and queue the exact child route separately.

For each source-derived public configuration request:

1. Verify exact scope.
2. Fix the URL, method, headers, redirect policy, and maximum request count in the approval plan.
3. Save raw headers/body and hashes.
4. Parse locally with sensitive fields redacted.
5. Do not follow response-derived hosts or routes without a new gate.

## 5. Validate token/logging leads against production configuration

When code logs a URL, token, user ID, or credential object:

1. Identify the exact log call and priority (`VERBOSE`, `DEBUG`, `INFO`, `WARN`, `ERROR`).
2. Trace the logging facade to actual sinks (Logcat, files, Datadog, Crashlytics, etc.).
3. Determine whether trees/sinks are initialized in the release build.
4. Read production remote thresholds, sampling, developer-mode flags, and scrubbing hooks from source-derived public config when safely available.
5. Compare message priority to the production threshold.
6. Close or downgrade the lead when normal production excludes it. Treat internal/opt-in debug logging separately; do not claim default exfiltration from a conditional diagnostic state.

## 6. Researcher-owned account setup via OAuth device flow

Prefer a standard OAuth device-authorization flow when it lets the user handle login/signup in the provider browser and keeps passwords out of scripts.

One-account-at-a-time discipline:

1. Resolve the exact device-code endpoint, token endpoint, public client ID, audience, and scopes from the app.
2. Prepare a mission for **one device-code request only**.
3. Save the `device_code` in a private `0600` file; show only the verification URL and short user code to the user.
4. Do **not** automatically poll.
5. Wait for the user to explicitly confirm browser authorization is complete.
6. Use a separately approved token-exchange step; honor server interval/expiry and avoid resend/restart loops.
7. Store access/refresh/ID tokens privately; notes and chat contain only redacted hashes, expiry, subject/account role, and authorization state.
8. Complete Account A baseline before creating Account B. Use Account B only for two-sided authorization controls.

Stop on CAPTCHA, password, OTP/TOTP, consent, or unexpected notification boundaries. The user handles secrets and human verification.

## 7. Evidence and closure

Each mission should maintain:

- `plan.md` — exact action, limits, scope, stop conditions;
- `verification.md` — approval and completion gates;
- raw private artifacts and hashes;
- sanitized inventories;
- `completion.md` — tested behavior, negative controls, non-findings, remaining proof gate;
- synchronized approval queue, hypotheses, and checkpoint.

Do not report until the mobile lead produces concrete unauthorized data/action, cross-account behavior, credential capability, or another program-accepted impact. Public configuration and static architecture alone are normally reconnaissance evidence.
