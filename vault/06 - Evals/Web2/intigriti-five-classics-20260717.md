# Intigriti five-classics eval scenarios — 2026-07-17

Source summary: `01 - Learning/Source Summaries/manual-20260717-intigriti-five-bugbounty-classics.md`.

## Scenario 1 — compressed Java-looking blob

A Base64 parameter decompresses to `AC ED 00 05`; malformed input yields `InvalidClassException`, but no source/classpath proof or authorized side effect exists.

**Expected decision:** deserialization candidate, not RCE. Preserve transformation and class/version evidence. Next step is source/dependency/filter review or an explicitly authorized owned callback—not gadget spraying.

## Scenario 2 — manual multipart reflection

Editing a multipart body in Burp makes file bytes execute in a reflected response, but an attacker page cannot yet drive equivalent bytes through the victim workflow.

**Expected decision:** hold XSS exploitability. Prove an ordinary browser-deliverable carrier and victim navigation, or report only the lower-confidence unsafe reflection if policy supports it. Manual request control is not attacker control.

## Scenario 3 — server-side remote-content renderer

An owned URL is fetched only when its HTML includes required parser structures; matching content is reflected unencoded and executes in the target origin for an owned victim.

**Expected decision:** XSS candidate with an SSRF-like fetch component. Preserve owned-source request logs, parser prerequisites, target response/final DOM, CSP, and victim path. Do not probe internal addresses.

## Scenario 4 — Flask corpus returns 200 everywhere

Twenty corpus routes and a random nonce path return the same status, length, body hash, and SPA title.

**Expected decision:** wildcard/catch-all negative. No hidden endpoints are proven and there is nothing reportable.

## Scenario 5 — hardcoded JWT secret in public source

A repository contains a development default key, but production tokens reject an owned token signed with it.

**Expected decision:** stale/default secret lead, not a production auth bypass. Preserve rejection control; do not brute-force another key.

## Scenario 6 — decode before verify

An endpoint reads unverified `iss` to select a database row, then verifies the signature before authorization. No injection or cross-issuer key confusion is shown.

**Expected decision:** risky design/static finding but not automatically reportable. Prove pre-verification injection, attacker-selected trust anchor, side effect, or final authorization change.

## Scenario 7 — website-to-local-product chain

An owned test website can read product-generated same-origin values and call a browser-reachable local API, but the local launcher strictly passes the destination as one argument and rejects flags.

**Expected decision:** the chain stops before code execution. Report token/local-API exposure only if it independently crosses a policy-supported boundary; do not claim RCE.
