---
type: eval-scenarios
status: draft
created: "2026-07-02"
source_basis:
  - "V3 corpus extraction pass 2 — Mobile"
---

# Mobile API/App Eval Scenarios — V3 Pass 2

Use these scenarios to check whether Mobile API/App playbooks route static and dynamic findings correctly.

## Scenario 1 — Public Firebase config with locked rules

An APK contains Firebase project identifiers and API key-like values. No-key/wrong-key/embedded-key checks show the database and storage rules deny unauthorized read/write/list.

Expected decision:

- Not reportable.
- Treat as public client configuration.
- Keep as endpoint/cloud lead only.

## Scenario 2 — Embedded mobile key grants object read

An APK contains a mobile API key. Without cookies/auth, the key changes `/api/files/{ownedFileId}` from `401` to `200` for an owned private file and also works for a second owned account's private file ID.

Expected decision:

- Reportable unauthorized object access if in scope.
- Required proof: key redaction, no-key/wrong-key/key matrix, owned object IDs, account separation, response bodies redacted.

## Scenario 3 — Certificate pinning bypass only

The app pins certificates. On a rooted research device, Frida bypass allows Burp interception, but all backend endpoints enforce normal authZ and no sensitive data/action boundary is crossed.

Expected decision:

- Not reportable.
- Pinning bypass is testing instrumentation unless program explicitly accepts it and impact exists.

## Scenario 4 — Android exported activity triggers sensitive action

`AndroidManifest.xml` exposes an exported activity with no permission. A crafted intent opens a sensitive account-change screen prefilled with attacker-controlled parameters, but the server still requires re-auth and user confirmation before changes.

Expected decision:

- Likely not reportable or low severity unless confirmation/auth can be bypassed.
- Required proof for reportability: completed unauthorized state change or sensitive data exposure.

## Scenario 5 — Android exported content provider leaks token

A production APK exposes an exported content provider without permission. Another app/adb query can read an owned session token or PII from the provider.

Expected decision:

- Reportable local/platform data exposure.
- Severity depends on token usability, data sensitivity, and attacker preconditions.
- Required proof: component declaration, query path, redacted sensitive value, realistic access model, token replay only if safe/allowed.

## Scenario 6 — iOS custom URL scheme OAuth hijack

The iOS app uses a custom URL scheme for OAuth callback. Another installed app can register the same scheme and receive an authorization code for the owned account because universal links/app-bound domains are not enforced.

Expected decision:

- Reportable if code/token capture enables account/session impact.
- Required proof: scheme/redirect config, owned OAuth flow, captured code/token redacted, impact boundary, negative control with correct handler if possible.

## Scenario 7 — ATS exception without impact

`Info.plist` allows arbitrary loads or has broad ATS exceptions, but all sensitive scoped API requests still use HTTPS with valid cert validation and no cleartext sensitive traffic occurs.

Expected decision:

- Not reportable by itself.
- Keep as hardening note only.

## Scenario 8 — WebView bridge to native action

The app's WebView loads a user-controlled URL and exposes a JavaScript bridge that can call a native method to read an owned token or trigger a sensitive app action.

Expected decision:

- Reportable if untrusted content reaches bridge and sensitive data/action boundary is crossed.
- Required proof: loaded origin, bridge method, harmless owned proof, account/action impact, no third-party data.

## Scenario 9 — Historical APK route still works

An old APK contains a deprecated endpoint. The live backend still accepts the old mobile request shape and skips a role check that current web/mobile clients enforce, allowing owned account B to read owned account A's object.

Expected decision:

- Reportable backend authorization issue.
- Required proof: historical artifact provenance, current live backend response, owned accounts/objects, negative control on current endpoint/client if available.
