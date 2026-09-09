# Third-party security tool adoption hardening

Use this reference after a tool-share triage produces an “add” or “pilot” decision. It captures a class-level installation and proof pattern; exact versions and paths remain session artifacts in the vault/tool registry.

## 1. Establish the claim ladder

Track each state separately:

1. canonical source identified;
2. code/dependencies reviewed;
3. immutable version selected;
4. artifact checksum or commit verified;
5. isolated install completed;
6. no-target/help/import smoke passed;
7. local inert fixture exercised the useful behavior;
8. host application loaded the plugin without error;
9. expected UI/feature was observed.

Never collapse stages 5–7 into stages 8–9. For GUI plugins, “runtime staged and imports pass” is not “extension loaded.”

## 2. Reproducible acquisition

Prefer, in order:

- release asset plus publisher checksum/signature;
- immutable Git tag verified against its commit;
- immutable commit when the project has no tags;
- source build pinned to an exact revision.

Record the canonical repository, tag, commit, checksum, install root, launcher, and any local patch. Avoid unpinned `latest`, remote pipe-to-shell installers, and mutable branch-only installs when a stronger option exists.

## 3. Isolation and dependency review

- Python CLI: use a dedicated `uv venv` or `uv tool` environment, not system Python.
- Burp/browser/IDE extension: use a dedicated first-use profile and separate data directory.
- Hosted tool: create a bookmark/launcher only; do not preload or submit target data during installation.
- Review transitive dependencies, not only the top-level requirements file.
- When upstream pins stale packages, test whether current compatible versions work in isolation; document deviations.

Inspect code/config for:

- `verify=False`, globally suppressed TLS warnings, or trust-all certificate handlers;
- automatic redirects that can cross hosts or scope;
- update checks, telemetry, remote UI/help/logo assets, and cloud APIs;
- filesystem writes and process execution;
- default stress, batching, alias-overload, brute-force, or DoS-style tests;
- generated reproduction commands that may print secrets.

## 4. Safe wrapper pattern

When a useful tool has risky defaults but a narrow local correction is auditable:

1. keep the upstream tree pinned and record its commit;
2. apply the smallest local patch;
3. expose a wrapper that defaults to low-impact tests;
4. require an explicit option such as `--include-stress` for excluded risky tests;
5. preserve the upstream behavior only behind that explicit gate;
6. assert the wrapper contains every excluded test name and that insecure options are absent from the installed source;
7. document that the wrapper is a local Argus variant, not upstream behavior.

Do not silently patch findings or output semantics in a way that makes results incomparable to upstream.

## 5. Local inert-fixture verification

A useful smoke test exercises behavior without contacting a target:

- URL collector: empty stdin/list should exit cleanly and emit no surprise network/error output.
- JS endpoint extractor: local fixture containing two known endpoint forms; assert both are returned.
- HTTP/API checker: local loopback server records method, path, headers, and payload classes; assert bounded request count and absence of batch/stress shapes.
- Plugin runtime: compile/import under the exact interpreter and load every optional dependency.
- Desktop link: validate the `.desktop` file and separately check the canonical hosted URL.

Help/version output alone proves launchability, not core behavior.

## 6. Legacy Jython/Burp extensions

Legacy Python extensions need extra gates:

1. use a checksum-verified Jython standalone JAR;
2. compile the extension under that exact Jython version;
3. install modules into a dedicated module directory;
4. import all required modules under Jython, not CPython;
5. expect modern transitive packages to advertise Python-2 compatibility incorrectly—pin the last syntax-compatible release when imports prove the latest is invalid;
6. launch Burp with a dedicated `--data-dir` to avoid touching the primary profile;
7. set Jython JAR, module folder, and extension path in the isolated profile;
8. observe both “no extension error” and the expected tab/UI before claiming load success.

Java deprecation/native-access warnings are compatibility signals to document, not proof of extension failure. Do not preserve a transient GUI-driver failure as a durable limitation; preserve the staged-vs-observed claim boundary and the manual verification gate.

## 7. Hosted-tool disclosure boundary

A hosted query generator, URL analyzer, schema visualizer, or scanner can receive:

- private hostnames and paths;
- search intent;
- DOM/schema contents;
- screenshots, cookies, headers, or traffic;
- program-identifying context.

A launcher/bookmark is acceptable without opening it automatically. Before submitting target material, evaluate program policy and disclosure risk; prefer local tools for private bounty data.

## 8. Reconnaissance and enumeration tool gates

For subdomain, DNS, HTTP-enrichment, screenshot, and monitoring tools, add these checks before adoption:

1. **Measure incremental value.** Compare source/module coverage against already installed enumerators. If nearly all providers overlap, adopt only the unique sources or delta-monitoring logic rather than another full pipeline.
2. **Trace actual network behavior by flag.** A command labeled `passive` may become active when status, title, technology, alive-only, screenshot, browser-render, IP-resolution, or deep-detection options are enabled. Classify each flag separately.
3. **Unit-test scope matching with adversarial names.** For target `example.com`, accept only `example.com` or names ending in `.example.com`; explicitly reject `notexample.com` and `example.com.evil.org`. Substring membership is never an adequate scope boundary.
4. **Reconcile program policy per target.** A tool approved for one program is not globally approved. Hard-block programs that prohibit domain enumeration or automated scanners; explicit asset-list programs should consume only that list rather than discover adjacent names.
5. **Review transport and secret handling.** Require TLS verification by default, bounded redirects, private `0600` provider-key config, redacted logs, and no remote report/UI exposure.
6. **Separate discovery from enrichment.** Passive candidates should flow through strict normalization, suffix/ownership/scope filtering, deduplication, and new-versus-known classification before any DNS/HTTP/browser contact.
7. **Prefer a pinned wrapper or selective source extraction.** If the useful portion is three unique providers or monitoring logic, do not install a broad upstream CLI unchanged. Pin the reviewed commit, apply minimal auditable fixes, cap concurrency/rate, reject active flags, and write mission-local provenance.
8. **Treat outputs as leads.** New names create scope/ownership review items and source-first mapping candidates, never findings or automatic scanner queues.

Use local inert fixtures to verify the wrapper rejects out-of-bound names and active options before any target-specific use.

## 9. Final verification report

Report a compact matrix:

| Tool | Pin/checksum | Isolation | Behavioral test | Remaining gate |
|---|---|---|---|---|

Also state:

- whether any live target was contacted;
- every local safety patch;
- upstream/local version mismatches;
- hosted-data disclosure caveats;
- exact manual gate for any GUI plugin not yet observed.

A consolidated verification should fail closed on missing launchers, wrong commits, checksum mismatch, invalid config, missing safety patch, failing fixture, or invalid desktop files.
