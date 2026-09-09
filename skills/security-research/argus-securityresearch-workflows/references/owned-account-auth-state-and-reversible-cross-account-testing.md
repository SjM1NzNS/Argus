# Owned-account auth-state and reversible cross-account testing

Use this reference when an authorized hunt moves from public/source mapping into manually authenticated validation with one or more controlled accounts.

## 1. Model authentication state in separate layers

Do not call an account “verified” or “unverified” from one signal alone. Record these independently:

1. **Identity-provider state** — session present, primary factor types, provider-side email verification, linked OAuth identities.
2. **Target backend state** — target-owned verification/status endpoints and their normalization behavior.
3. **Application enforcement state** — SSR props, UI gates, protected API responses, and actions actually allowed.

A mismatch is a hypothesis, not impact. For example, a target endpoint returning `false` while the identity provider reports `verified` may be stale state or a canonicalization defect rather than a verification bypass.

## 2. Run a bounded identifier-normalization matrix

For an owned identifier only, compare the smallest relevant variants before interpreting status:

- exact configured representation;
- lowercase canonical form;
- uppercase form;
- trim/whitespace only when source indicates it may reach the backend.

Record booleans/statuses without printing the raw identifier. If exact/lower/upper differ, trace which representation each later component uses. Then test whether the mismatch changes an authenticated security boundary—not merely which screen or recovery UX appears.

Reportability requires one of: unauthorized data/action, durable account confusion, bypass of an ownership proof, recovery against the wrong principal, or a controlled cross-account effect. Enumeration or self-service flow confusion alone usually does not satisfy the Argus impact gate.

## 3. Bridge manual authentication without handling secrets

- Let the user type passwords, OTPs, recovery codes, and OAuth credentials.
- Never request or transcribe those values.
- After login, collect only sanitized state such as `session=yes`, factor types, verification booleans, provider names, and array counts.
- Match the active account to a controlled slot using a local hash comparison; output only `PRIMARY_ACCOUNT` / `SECONDARY_ACCOUNT`, never the identifier or hash unless required for private evidence.
- Use an existing browser session in place; do not export bearer tokens or cookies when a same-origin browser request can perform the validation.
- If temporary screenshots may contain PII, capture only the target window, redact in any retained artifact, and delete raw temporary captures after extracting the necessary state.

## 4. Reversible two-account authorization matrix

When no owned object exists, obtain explicit approval before creating one.

1. Create one benign object in account A and one in account B.
2. Disable notifications or external side effects where possible.
3. Give objects unmistakable control names.
4. Store exact object IDs only in private evidence or temporary same-origin storage. Do not assume same-origin storage survives logout: identity-provider sign-out may clear application `localStorage`. Before switching accounts, move only the owned object ID—not cookies or tokens—to a mode-0600 temporary local file, and remove it immediately after cleanup.
5. Keep authentication one account at a time when that is the user’s operating constraint; log out/switch rather than collecting reusable session secrets. If the exact runtime route is needed, an in-page `fetch`/`XMLHttpRequest` observer may record only method, sanitized path, and owned object ID; never print or persist request authorization headers.
6. Establish same-owner controls first: A→A and B→B positives.
7. Attempt only the minimal cross-owner mutation/read: A-session→B-object and B-session→A-object.
8. Re-authenticate as the owner to verify whether state actually changed; never infer success from HTTP status alone.
9. Restore the original state immediately.
10. Delete both control objects and verify cleanup before closing the branch.

For alert/search objects, prefer notification frequency `Never` and avoid actions that email agents, subscribe users, create leads, or contact partners.

## 5. Source and UI false-positive gates

- A client route rendering does not prove the backend authorized private data.
- A reset-password form reachable by query parameter is not a reset bypass without a valid recovery state and controlled password change.
- `verify_at_sign_up=false` plus an active session is only a pre-hijacking signal. Prove durable factor retention or automatic linking across a legitimate owner event using owned controls.
- Automatic OAuth linking is not a finding unless an attacker-established factor/session remains usable after the owner links or verifies the account.
- A case-sensitive verification lookup is not enough by itself; prove principal confusion or boundary impact.
- Empty owned pages demonstrate route access, not cross-account exposure.

## 6. Evidence checklist

Retain:

- sanitized per-layer auth state;
- exact normalization variants and results without raw identifiers;
- source excerpts showing where the status controls flow;
- object A/B ownership map;
- pre/post state for every mutation;
- cleanup verification;
- a clear distinction between confirmed implementation defect, exploitable finding, and closed false positive.
