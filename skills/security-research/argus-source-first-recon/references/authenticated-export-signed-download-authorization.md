# Authenticated export and signed-download authorization matrices

Use this workflow for authorized web applications that create asynchronous exports, archives, signed URLs, download components, or portability jobs. It is provider-agnostic: object stores, data-export portals, cloud consoles, and account data portability systems all fit.

## Objective

Test whether the current authenticated actor is authorized for the exact export job, archive, file component, or signer input while preserving a real same-account control. A source-mapped signer RPC or opaque download URL is a candidate, not proof.

## 1. Recover the supported object contract

From already-approved UI/source/runtime evidence, identify:

- export creation method/RPC and completion state;
- owner history/detail route;
- component-download or signer route;
- actor-routing fields (`authuser`, tenant/account route, profile index);
- object-selector fields (job/archive/component IDs, owner marker, part index);
- any signed-storage redirect reached only after server authorization.

Treat a selector as a tuple when multiple opaque fields jointly name the object. Do not change an owner marker separately and call it a non-selector field merely because its name looks like actor context. Preserve the current actor's route/session fields separately from the foreign object tuple.

Never synthesize an internal protobuf/RPC call merely because source exposes a descriptor. Capture the supported request first. If the supported route reaches reauthentication before the internal signer, do not direct-call the signer to bypass that gate.

## 2. Build minimal owned fixtures

Create one minimal non-sensitive fixture per owned account only after mutation approval:

- one product/data class;
- one dedicated folder/container;
- one tiny unique canary file/record;
- one export/job;
- no unrelated private data.

Record exact names and selectors privately; sanitized records keep hashes, byte counts, actor labels, route shapes, and selection counts only.

For complex product dialogs, anchor every query to the exact control or fixture—not the first visible `[role=dialog]`. Browser side sheets and transcript/help panels may also expose `role=dialog` and can cause an outside click that dismisses the real modal.

UI state often hydrates after the account/actor shell is ready. Separate waits for:

1. actor/host/path gate;
2. product-list controls;
3. selected-product state;
4. folder dialog and exact fixture row;
5. asynchronous checkbox counts;
6. create/export readiness.

Do not infer failure from `document.readyState=complete` while framework controls are still hydrating.

### Include-all checkbox pitfall

Folder-selection dialogs may disable **Deselect all** while a top-level **Include all files/folders** checkbox is checked. Use the supported sequence:

1. uncheck Include all;
2. wait until it is false and Deselect all is enabled;
3. click Deselect all;
4. wait for zero selected rows;
5. select the exact canary row;
6. wait for exactly one selected row;
7. confirm.

Verify state after every click; framework checkbox updates may be asynchronous.

## 3. Positive controls before the foreign probe

Required order:

1. Actor A -> A-owned component, through the supported route.
2. Actor B -> B-owned component, through the same route family.
3. Confirm each reaches the actual signer/download authorization boundary and, when permitted, the smallest archive-byte/canary identity proof.
4. Only then send one A-owned selector tuple under B while keeping B actor-routing/session fields fixed.

A pre-reauthentication HTTP 200 challenge page is not a successful owner control. A login/password/passkey page, generic shell, redirect, or “download” navigation is not signing or data access. If both owner routes stop at reauthentication, mark the matrix inconclusive and leave the one-shot foreign probe unspent.

Do not weaken this gate because the user is unavailable. Passwords, device PINs, TOTP/recovery values, and native passkey approvals remain user-handled. A single offered non-password path may be inspected without sending/resending codes; stop at native credential or permission UI. Do not use source knowledge to route around reauthentication.

## 4. Capture without preserving session material

Private evidence may retain the exact owned selector tuple/component URL when required for a later approved differential. It must be mode `0600` and never user-facing.

Sanitized evidence should retain only:

- actor label and verified route shape;
- method, host, path, and query-key names;
- request/response status;
- body byte count/hash when useful, never body content;
- selector hashes and lengths/character classes;
- selected product/folder counts;
- completion/reauth/download booleans;
- downloaded canary hash/size if a valid owner control reaches bytes.

Explicitly record false retention flags for cookies, headers, tokens, request bodies, response bodies, DOM text, and account identifiers. Do not store a raw batchexecute form body: it commonly contains CSRF/session values even when the interesting `f.req` field appears harmless.

## 5. Reauth-aware disposition

Use these states precisely:

- `owner_control_complete`: supported route reached signer/archive bytes and matched the owned canary.
- `reauth_blocked`: supported route stopped at password/passkey/device authorization before signer/archive bytes.
- `cross_account_probe_unspent`: negative control deliberately not sent because positive controls were incomplete.
- `denied`: foreign selector reached the same authorization layer as the owner control and produced a clean denial with no signed URL/bytes.
- `unexpected_success`: foreign selector yielded a usable signed URL or owned canary bytes; stop immediately.
- `inconclusive`: response families are not comparable or authorization layer was never reached.

Never call a reauth challenge a denial or authorization success.

## 6. Cleanup semantics

After an export reaches completion, deleting the source fixture generally does not delete the completed archive. This permits prompt cleanup of dedicated source canaries while retaining the server-side export for a later user-authenticated control, subject to program rules and expiry.

Cleanup requirements:

- select only the exact privately recorded fixture selector;
- move it to Trash and verify absence from the source view;
- permanently delete only when approved;
- verify absence from Trash and source view;
- remove disposable authenticated profile clones;
- close loopback CDP ports;
- remove transient screenshots and source files containing account markers;
- preserve only the minimum private selector/evidence records.

A native WebAuthn/passkey prompt may block navigation for the entire disposable browser. Do not interact with the native credential prompt. Stop and relaunch that disposable clone on the verified cleanup route, then resume from observed object state (for example, already moved to Trash) rather than repeating the mutation.

When terminating clone processes by command-line matching, avoid matching the wrapper shell containing the same profile-path string. Prefer the tracked process handle. If process discovery is necessary, exclude the current process and its wrapper/ancestor chain before signaling.

## 7. Evidence and manifest finalization order

Use this dependency order:

1. finish live actions and cleanup;
2. write private and sanitized evidence;
3. update candidate disposition, owned-account matrix, approval queue, hunt log, tested items, hypotheses, next steps, and finding hold;
4. rebuild evidence manifests for every changed document;
5. run the phase verifier;
6. run the full mission verifier;
7. inspect failed check names rather than only totals;
8. refresh any manifest entries whose governed documents changed;
9. rerun until fully green.

Do not build a manifest before final ledger edits and then report the resulting hash drift as harmless housekeeping. If a verifier reports only stale hashes for deliberately edited documents, regenerate those declared entries and rerun before declaring the mission complete.

## Reportability rule

No finding exists unless the foreign selector reaches a comparable post-reauth signer/download boundary and demonstrates unauthorized signed capability or canary access. Source descriptors, opaque selector recovery, completed exports, owner challenge pages, and pre-reauth HTTP 200 responses remain candidate evidence only.
