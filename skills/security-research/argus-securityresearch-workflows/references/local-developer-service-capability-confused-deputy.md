# Local developer-service capability and confused-deputy validation

Use this reference for IDEs, debuggers, language servers, agent runtimes, developer dashboards, and tooling daemons that expose local HTTP/WebSocket APIs and retain stronger internal capabilities than their clients.

## High-signal chain

Look for the combination—not just one isolated unauthenticated endpoint:

1. A loopback API discloses or brokers a bearer capability, randomized WebSocket URI, session path, or daemon handle.
2. Another unauthenticated API accepts a caller-selected callback, VM/debug service, plugin, MCP server, proxy, or WebSocket URI.
3. The privileged process connects to that endpoint and treats protocol responses as trusted identity, path, workspace, project, or authorization input.
4. A validation failure falls back to lexical/path-string inference, guessed metadata, or permissive compatibility behavior.
5. The process uses a non-exported secret or victim-context privilege to expand access for the caller.
6. The caller reuses the exposed/brokered capability to exercise the newly authorized operation.

Treat loopback binding as a network-reachability restriction, not an operating-system user boundary. Prove the actual local actor instead of assuming it.

## Source-first map

Trace and preserve these edges:

- API dispatch and authentication/method/origin/capability checks;
- capability creation, storage, and exposure;
- caller-controlled endpoint normalization and outbound connection;
- exact protocol methods the privileged process invokes;
- attacker-controlled fields in returned protocol objects;
- path/root inference, canonicalization, existence checks, and fallbacks;
- where the privileged process supplies its private secret;
- final read/write/action service and containment rules;
- disconnect, revocation, and multi-client/root-merging behavior.

Build the fake peer from the observed protocol, implementing only the minimum read-only handshake methods. Log each received method and return deterministic synthetic values.

## Cross-user differential proof

Use two real OS identities where available:

- victim developer service UID;
- lower-privileged requester/fake-peer UID.

Create only synthetic canaries:

- victim root mode `0700`;
- victim private file mode `0600`;
- a sibling outside-root negative control;
- one exact attacker-chosen write canary.

Required gates:

### Before

- requester cannot traverse/read/write the victim root directly;
- privileged service is running normally;
- authorized root/capability state is captured;
- protected read/action is denied with the exact product error.

### Trigger

- capability retrieval is performed as the lower-privileged UID;
- registration/notification is performed as that same UID;
- fake peer logs the exact privileged handshake;
- its chosen path/root does not need to exist when testing a lexical fallback;
- retain raw HTTP status/body and protocol requests.

### After

- exact attacker-selected root/state appears;
- private canary is returned exactly;
- write returns the product's success object and exact bytes read back;
- outside-root control remains denied, proving a scoped authorization change rather than globally disabled containment;
- hashes establish which files changed and which controls did not.

### Revocation

- disconnect through the supported product flow;
- root/state returns to baseline;
- the same protected operation is denied again;
- verify temporary listeners, processes, symlinks, and disposable files are cleaned.

Do not claim persistence if disconnect removes authority. Bound impact to the filesystem/network/process privileges of the victim service.

## Current-source and release differential

Prefer both:

1. **Current source:** copy only relevant files into an isolated harness, preserve byte-identical hashes, and exercise the real handlers/helpers.
2. **Packaged release:** run the normal released launcher and prove the same before/trigger/after/revocation behavior.

Record both live Git pins with `git rev-parse HEAD` immediately before final reporting. Do not trust compressed-session summaries, stale notes, short hashes, or previously copied provenance values. Make the verifier assert both repository pins.

If a harness removes workspace-only metadata or otherwise adapts packaging, record that separately and hash every security-relevant product file against its source copy.

### Runtime assertions are not authorization checks

Inspect every `assert` on the path from attacker-controlled protocol data to root/path authorization. A Dart/Python/C/C++ assertion may reject the value in a debug or explicitly assertion-enabled run while disappearing in the released/default runtime. When this matters:

- record whether assertions were enabled in the exact exercised server process, not merely in a helper probe or fake peer;
- preserve the launch/compile arguments and the observed post-condition that proves the value passed the assertion site;
- phrase the report as an **assertions-disabled tested configuration** unless a packaged-release proof independently establishes the same behavior;
- state that an assertions-enabled debug build may stop earlier;
- remediate with an unconditional runtime validation before authorization state changes, never by strengthening the assertion alone.

Do not call a source-level assertion a production mitigation, and do not claim universal exploitability from an assertions-disabled harness without naming that prerequisite.

## Adversarial prior-art and report separation

Search issues, PRs, reviews, comments, and history for:

- trusted/untrusted local clients;
- API authentication tokens;
- capability/secret exposure;
- caller-selected debug/VM/plugin services;
- workspace-root authorization;
- filesystem service read/write;
- the exact confused-deputy chain.

Keep three verdicts separate:

1. **Technical validity:** did the complete cross-user differential pass?
2. **Novelty:** is the exact actor → fake peer → privileged authorization → impact chain public?
3. **Submission risk:** could a generic open trusted-client/authentication issue cause duplicate or known-issue closure anyway?

A generic public auth-hardening issue may not describe the demonstrated exploit chain, but it materially raises duplicate risk. Disclose it prominently rather than hiding it. Search review comments as carefully as issue bodies: a reviewer question that anticipates “any client can cause privileged root mutation” plus a reply proposing a trusted-client key is much closer prior art than a generic authentication issue, even when neither contains the final cross-user proof. Preserve exact comment URLs/IDs and distinguish:

- what the review already anticipated;
- what the follow-up issue actually tracks;
- what the new proof adds (actor boundary, fake-peer mechanics, runtime-mode prerequisite, concrete impact, and revocation controls).

For compact reviewer packages, prefer a focused quoted excerpt with comment IDs/URLs over a huge raw review JSON containing unrelated diffs, test fixtures, or capability-shaped sample strings. Keep the full saved response in the mission archive and hash it there.

Do not merge adjacent findings merely because they share the same unauthenticated local API. Keep reports separate when they have different sinks, impacts, controls, remediation, or prior-art posture. A technically stronger candidate can remain the second submission when a narrower candidate has cleaner novelty.

## Reporting boundaries

Use a clear `The problem` / `Impact analysis` split.

State facts:

- concrete lower-privileged local actor;
- victim service UID and requester UID;
- direct OS denial;
- exact before/after/revocation behavior;
- scope of read/write/action authority;
- victim privilege boundary;
- release/current-source provenance.

Explicitly reject unsupported claims such as remote-webpage reachability, non-loopback exposure, hosted-service compromise, persistence, code execution, or privilege beyond the victim process.

Recommended remediation layers:

- authenticate privileged local API clients with a per-launch capability;
- do not expose downstream bearer capabilities to unauthenticated callers;
- bind endpoint registration to an authenticated frontend/session or trusted channel;
- never promote lexical fallback output into authorization state;
- require existing canonical roots associated with a trusted project context;
- consider user-scoped IPC/peer credentials;
- add fake-peer regression tests preserving before/after denial controls.

## Evidence sealing

Maintain an independent verifier per candidate. It should assert:

- before/after/revocation invariants;
- UID boundary metadata;
- exact fake-peer methods;
- source/harness hashes;
- all live Git pins;
- validity of saved duplicate searches;
- preservation and state of material prior art.

Run pipelines with `set -o pipefail` when piping verifier output through `tee`; otherwise a verifier failure can be masked by a successful logging command.

Secret scanning must cover the **whole retained archive and review package**, not only the primary final proof. Older differential runs and HTTP transcripts may still contain inactive randomized WebSocket/capability URIs even when the latest evidence is redacted. Replace credential-like values with `[REDACTED]`, add a redaction log that does not preserve the removed value, rebuild affected manifests, and scan for bearer-shaped URI paths plus generic API-key/token/private-key patterns.

Generate a separate JSON verification result and SHA-256 artifact manifest. Build any review ZIP only after the final report/ledger edits, test it with a full archive integrity check, verify its checksum, and confirm no test listener/process remains.
