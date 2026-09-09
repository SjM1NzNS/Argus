# Official CLI Package Provenance and Symlink Fixtures

Use this reference when an authorized frontend, documentation bundle, or fixed source artifact exposes an exact first-party CLI/package name and registry. It extends source-first recon from package provenance through static review and, only under a separate authorization, owned local validation of filesystem-boundary candidates.

## Phase separation is mandatory

Treat these as three distinct actions:

1. **Registry metadata only** — identify the exact version, archive URL, integrity fields, and publication metadata.
2. **Archive-only static review** — download the fixed archive, verify its published hashes, apply archive-safety gates, and inspect source without installing or executing it.
3. **Owned local execution fixture** — only if separately authorized, execute the smallest exact source module needed to validate a static hypothesis, with network/UI/dependencies mocked and a disposable fake home.

A request to perform static review "without installation or execution" authorizes phases 1–2 only. Do not silently promote to phase 3. Record a new plan/approval before any package/module code runs, even when the fixture is local and harmless.

## 1. Registry metadata without ambient credentials

- Derive the package name and registry from exact first-party source.
- Confirm the registry host is explicitly in scope or document tight functional attribution.
- Use disposable empty user/global package-manager configuration and cache.
- Disable redirects and retries where the client permits it.
- Request metadata only; do not resolve dependencies, install, invoke `npx`, run lifecycle scripts, or execute the package.
- Preserve only sanitized metadata, command outcome, timestamps, and a request ledger.

Metadata being publicly readable is not a vulnerability by itself. Record intent signals such as frontend instructions that deliberately use an empty user config.

## 2. Fixed archive static review

Use a separate approval once metadata exposes an exact archive URL and hashes.

Before source review:

1. Download the exact archive once with redirects disabled and a byte cap.
2. Verify every published integrity value available (for npm, normally SRI SHA-512 and SHA-1 shasum).
3. Reject before extraction if the archive has:
   - absolute or traversal names;
   - symlink, hardlink, device, FIFO, or other special members;
   - duplicate or abnormal names;
   - implausible member counts or unpacked size;
   - hash mismatch.
4. Prefer in-place archive reads. If extraction is necessary, manually write only validated regular members into a disposable directory.
5. Inspect `package.json` for lifecycle scripts, binaries, engines, dependencies, registry hooks, update paths, and fixed versus floating versions.
6. Trace source-to-sink paths for:
   - filesystem writes, recursive deletion, rename, and staging;
   - path normalization and containment;
   - process spawning and `shell` use;
   - network clients, redirects, and authorization forwarding;
   - token/cache permissions;
   - package self-update behavior;
   - remote bundle/archive member validation.

Do not equate a clean archive with a clean CLI. Archive traversal and runtime filesystem traversal are separate classes.

## 3. Adjacent supply-chain and API leads

An official package can expose new, tightly attributed boundaries:

- a distinct production API, tenant, audience, or client configuration;
- a private-registry install command plus a registry-less `npx` fallback;
- self-update commands or package-manager invocation;
- agent Skill/MCP installation destinations.

Gate each lead independently:

- A distinct API receives its own exact-route, read-only plan and request budget.
- A registry-less `npx --package=@scope/name` fallback may justify one public-registry metadata lookup. A `404` proves only that the package does not currently resolve there; it does **not** prove namespace/scope claimability or dependency confusion. Never claim or publish to test it.
- Generic health/version `500` responses are not reportable without stack, secret, data, or security-boundary impact.

## 4. Symlink-aware filesystem analysis

Lexical checks such as:

```js
const candidate = path.resolve(base, userPart);
if (!candidate.startsWith(path.resolve(base) + path.sep)) fail();
```

reject `..` but do not constrain existing symlink components. Search the whole package and wrappers for:

- `lstat`, `realpath`, `readlink`;
- `isSymbolicLink`;
- `O_NOFOLLOW` or platform-equivalent no-follow primitives;
- revalidation immediately before `rm`, write, rename, or recursive copy.

Follow callers from the helper to the supported CLI command. Preserve whether the mutation uses a target directory, its parent, a staging directory, and recursive deletion.

### Owned differential fixture

Only under separate authorization:

1. Reverify the exact package hash.
2. Create a mode-`0700` temporary fake home and project.
3. Keep actual `HOME`, SSH, agent, and config directories out of the fixture.
4. Disable network and replace the package's fetch/UI dependencies with inert deterministic mocks.
5. Execute the smallest exact signed modules, not a reimplementation.
6. Run a causal pair:
   - **negative:** real project directory; mutation must remain beneath the project;
   - **positive:** same project path with one repository-controlled symlink component; all other inputs identical.
7. Use inert canary contents and compare pre/post existence, hashes, and canonical destinations.
8. Destroy the temporary fixture and verify no process or temp directory remains.

Useful impact controls in a fake home include:

- project install redirected to a modeled global agent Skill directory;
- replacement of a pre-existing modeled global Skill;
- project remove redirected to an owned fake config file whose basename satisfies the CLI slug grammar.

For a repository-delivery claim, do more than inspect the source worktree. Create an owned local origin, commit the link, perform a normal local clone into the modeled victim layout, and retain all of:

- origin and clone `git ls-files -s` mode `120000`;
- clone-time `lstat`/`readlink` proof that the checkout materialized a real symlink;
- the exact relative target and checkout-depth assumptions;
- OS, Git, and runtime versions;
- confirmation that no remote repository or victim was involved.

Do not publish a malicious repository or involve a victim.

### Natural-workflow control

A synthetic basename such as `config` is useful for proving the deletion sink, but reportability also depends on a plausible supported workflow. Add a second owned control when possible:

1. choose a real source-declared or bundled Skill slug;
2. pre-create the corresponding modeled global Skill with an inert trusted marker;
3. clone the owned repository so its project `.agents` or `.agents/skills` ancestor link resolves to that modeled global directory;
4. invoke the exact remove/install module with `location=project` and the plausible slug;
5. verify the lexical path is inside the clone while the real parent is outside, and record the global Skill's before/after hash or existence;
6. keep network disabled and destroy the fixture.

This closes the objection that the proof depends only on an implausible synthetic command. It still does not prove automatic execution, attacker-controlled approved content, or an installed CLI entry point.

## Evidence and reportability

Retain:

- exact artifact URL/version and published/observed hashes;
- archive member/safety summary;
- exact source excerpts with file and line provenance;
- fixture runner and result JSON;
- real-directory negative and symlink positive;
- canonical destination, pre/post hash/existence, external-request count;
- cleanup and restrictive-mode verification;
- explicit non-claims.

Lead with content-independent impact when available. For example, an exact `remove` path that deletes an owned fake config file is stronger than a mocked malicious Skill bundle.

Downgrade clearly for:

- victim interaction and a malicious/untrusted repository;
- symlink-supporting checkout/platform requirements;
- victim-user permissions only;
- basename/slug restrictions;
- mocked bundle content rather than live attacker-controlled approved content;
- no automatic agent execution, confidentiality, privilege escalation, or server-side impact.

Treat first-party CLI/package eligibility as a separate scope question even when its registry hostname is explicitly listed. Do not inflate a local user-assisted primitive to High merely because an agent-Skill destination is imaginable.

### Separate four verdicts

Do not collapse these decisions:

1. **Technical validity** — exact source and owned controls prove the filesystem primitive.
2. **Impact validity** — the supported workflow creates a concrete integrity/availability effect independent of mocked attacker content.
3. **Asset eligibility** — the program covers the downloadable CLI/package itself, not merely the registry hostname.
4. **Submission readiness** — exploitability prerequisites and proof fidelity make acceptance more likely than Informative/N/A/OOS.

Run independent Skeptic and Impact reviews against the frozen artifact/evidence set. Preserve disagreement rather than averaging it away. A valid CWE-59 can remain **HOLD** when:

- the scope is domain/mobile-centric and does not explicitly include local CLI artifacts;
- exploitation requires an untrusted repository, symlink-supporting checkout, exact victim command, project-location selection, path-depth assumptions, and a slug/basename collision;
- only exact internal modules were exercised while the installed CLI entry point was not;
- the effect remains within the victim user's permissions and shows no confidentiality, privilege, RCE, or server impact.

Use CVSS metrics that reflect the demonstrated chain rather than the primitive in isolation. High attack complexity can be appropriate when checkout behavior, path placement, basename, and explicit command conditions all must align. Keep a Low/HOLD verdict when the strongest invalidity argument remains stronger than the severity argument; do not draft merely because the primitive is real.

If an installed-entrypoint replay would violate the user's static-only/no-execution constraint, stop and record it as missing proof. Do not silently broaden authorization to improve reportability.

## Mitigation review

A durable fix should:

- create or identify the intended base, then canonicalize it;
- inspect every existing component with `lstat`/`realpath` and reject symlinks in trusted path segments;
- ensure the real parent remains beneath the real base;
- reject symlink targets before recursive removal or replacement;
- revalidate immediately before destructive operations to reduce TOCTOU exposure;
- use no-follow/openat-style primitives where available;
- apply identical checks to add/install and remove/uninstall paths;
- include real-directory, intermediate-symlink, dangling-symlink, replacement, deletion, and race-aware regression tests.

Reference: <https://developer.android.com/privacy-and-security/risks/zip-path-traversal>

## Common false positives

- Public package metadata or source exposure without unintended capability.
- Published package hash/integrity fields treated as a security weakness.
- Public-registry `404` treated as proof that an organization scope is claimable.
- Client-side selectable API base URL treated as token exfiltration without an attacker-controlled configuration path.
- `path.resolve()` assumed to neutralize symlinks.
- A mocked local bundle treated as proof of live contributor/reviewer bypass.
- A source-level primitive promoted without a supported command path, exact-module fixture, and negative control.
- Module execution described as "static review." Keep the static and dynamic phases explicit in evidence and final reporting.
