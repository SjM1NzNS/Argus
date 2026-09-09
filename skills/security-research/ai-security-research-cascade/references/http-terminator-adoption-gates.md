# HTTP Terminator Adoption Gates

Source repository: `https://github.com/PortSwigger/http-terminator`

Use this reference when adapting the HTTP Terminator research pipeline to a scope-aware security workspace. It records class-level integration boundaries, not permission to scan live systems.

## Stage disposition

| Stage | Safe role | Required adaptation |
|---|---|---|
| Seeker | Extract desync hypotheses from public research and RFCs | Feed sanitized local artifacts rather than arbitrary URLs; preserve source hash and provenance; keep output proposal-only. |
| Flamer | Generate and deduplicate malformed-request candidates offline | Pin dependencies; use reviewed inspiration; begin with dry-run/local persistence; prohibit optional remote upload; keep generated corpora private. |
| Validator | Deterministically evaluate selected candidates in an owned two-hop harness | Safety-fork before use: strict destination allowlist, bounded concurrency and volume, no ambient proxy-history targeting, no restored periodic scans, no victim/OAST actions by default. |
| Investigator | Replicate, minimise, falsify, cascade, and report | Port the workflow to fresh-context Hermes tasks and immutable evaluators; do not assume proprietary MCP or organizer components exist. |

## Source-review findings that must inform adaptation

- Seeker's fetcher follows redirects and accepts supplied URLs. A hardened workspace should retain acquisition authority and pass sanitized local artifacts into extraction.
- Seeker stores source URLs, prompts, extracted sections, and raw model responses. Keep credentials, authenticated material, capability URLs, private briefs, and target data out of its model inputs and databases.
- Flamer generates malformed HTTP requests and has an optional upload path. Local generation is the safe default; remote transfer must remain disabled unless separately designed and approved.
- Validator can derive targets from Burp proxy history or large URL files. Proxy history is not a scope contract and must never serve as an implicit allowlist.
- A denylist with placeholder entries is not a safety boundary. Enforce an exact scope-derived allowlist immediately before every send, including host, scheme, port, and destination-address policy.
- A filter that logs a disallowed request but returns a continue action does not block egress. Verify blocking behavior with an owned sink and zero received requests.
- Persisted periodic-validation preferences can silently resume active traffic. Production-safe forks must default to stopped on every load and require an explicit per-run approval artifact.
- Victim-request, response-queue, Collaborator/OAST, and generated-corpus operations can affect unrelated users. Keep them disabled outside an owned simulator unless a human approves a narrowly documented Zone 3 action.
- Passive anomaly collection is a lead source, not proof. Preserve response lineage and feed anomalies through deterministic controls and independent falsification.
- Prebuilt binary dependencies need provenance, hash, license, and source correspondence review before loading into Burp.
- The published Investigator is partly a methodology reference and relies on external components. Reimplement its phase contracts rather than claiming the repository runs end to end.

## Implemented Argus subset

The operational Argus adaptation is documented in `$HOME/SecurityResearch/00 - System/offline-research-cascade.md` and exposed as `argus-research-cascade`.

It intentionally implements only:

- offline hash-bound local source admission, no-symlink bounded reads, conservative scanning of every model-visible field, canonical public-provenance checks that reject empty userinfo/port authorities, alternate numeric/private/single-label hosts, C0/C1 controls, malformed/non-canonical escapes, path parameters, and arbitrarily encoded capability-like paths while classifying canonical global bracketed IPv6 by public-address semantics; unpredictable staging made owner-accessible despite restrictive caller umask before descriptor open, atomic no-replace run publication, descriptor-relative exact-inode rollback, run/parent pathname revalidation, an installed launcher bound to the reviewed absolute runtime rather than mutable `HOME`, and externally pinned prepared-artifact manifests;
- attributed 1–3 sentence micro-inspiration;
- fresh-context no-tool task packets that prepare validates with ingest's complete packet contract and refuses to emit above the 20,000-character per-prompt or 5,000,000-byte per-artifact admission ceilings. If the packet-count and per-prompt ceilings mathematically make aggregate overflow unreachable, verify the boundary with a maximum-cardinality positive producer→consumer test rather than retaining an impossible aggregate-negative fixture;
- strict, recursively bounded JSON admission with raw-and-normalized string/list bounds across contract, worker, disposition, and evidence-path data; invalid-Unicode containment before path/syscall use; controlled decoder failures; exact identifier and supplied-pin typing/format; exactly one result per fragment; task-packet/fragment/count/provenance cross-bindings; lineage-preserving deduplication; and an emitted-ledger ceiling compatible with closure;
- proposal-only hypothesis ledgers using full-SHA-256 `hypothesis-<64 lowercase hex>` IDs with externally pinned, run-manifest-bound ingestion manifests;
- one terminal disposition per normalized hypothesis, with a typed hypothesis-bound evidence manifest and hash-bound evaluator result, authenticated by an externally pinned post-review evidence index, disjoint hashed evaluator input/output paths, hard-link/inode alias rejection, distinct passed positive/negative controls, reproduced observation, non-empty timezone-aware human review, duplicate-reference rejection, and a 20,000,000-byte aggregate evidence ceiling required for `reportable` closure.

Use `08 - Templates/research-cascade-contract.json.template`, then:

```bash
RUN_PARENT="$HOME/.local/share/argus-research-cascade/runs"
RUN_DIR="$RUN_PARENT/new-run"
install -d -m 0700 "$RUN_PARENT"

argus-research-cascade prepare \
  --contract /absolute/path/to/contract.json \
  --run-dir "$RUN_DIR"

argus-research-cascade ingest \
  --run-dir "$RUN_DIR" \
  --results /absolute/path/to/hypothesis-results.jsonl \
  --manifest-sha256 "$MANIFEST_SHA256"

argus-research-cascade verify-dispositions \
  --run-dir "$RUN_DIR" \
  --dispositions /absolute/path/to/dispositions.jsonl \
  --manifest-sha256 "$MANIFEST_SHA256" \
  --ingestion-manifest-sha256 "$INGESTION_MANIFEST_SHA256" \
  --evidence-index-sha256 "$EVIDENCE_INDEX_SHA256"
```

The immediate run parent must already exist, be owned by the current effective user, and be mode-private. Descriptor/inode checks are fail-closed phase transaction controls, not sandbox isolation from a mutually hostile process sharing that UID; claims bind the identities observed at publication/write/final-check gates. A false `source_contains_secrets` declaration does not bypass secret-pattern admission checks over exact source bytes and other model-visible fields. URL provenance must be public and canonical enough to exclude credentials, queries/fragments, non-default ports, malformed hosts/escapes, encoded unreserved characters, path parameters, and opaque high-entropy capabilities. Heuristics do not prove content public; the operator remains responsible for source review and sanitization.

Capture `manifest_sha256` from `prepare` and `ingestion_manifest_sha256` from `ingest` outside the mutable run directory. For a reportable row, create and review `evidence-index.json`, capture its SHA-256 outside the run, and pass it as `--evidence-index-sha256`; non-reportable closure may omit this third pin. Never regenerate an expected digest from the artifact it is meant to authenticate.

The packager performs no acquisition, model, payload-generation, Burp, or target calls. Build a narrow owned evaluator only after a selected hypothesis establishes the need; do not port the generic Flamer/Validator first.

## Recommended architecture

```text
public research/RFC
  -> hardened acquisition and sanitization
  -> local attributed artifact
  -> hypothesis extraction
  -> proposal-only review gate
  -> offline candidate generation
  -> human-selected candidate
  -> owned two-hop parser harness
  -> deterministic evaluation
  -> fresh-context replicate/minimise/falsify cascade
  -> evidence and reportability review
```

## Live-target gates

1. Load the HTTP request-smuggling/desynchronization playbook and exact target scope contract.
2. Confirm that the program permits this class and the exact proposed action.
3. Prefer an owned local front-end/back-end harness.
4. If live work is permitted, begin with one direction-specific, non-poisoning discriminator and a matched benign control.
5. Set destination, request-count, concurrency, retry, timing, response-capture, and stop budgets in deterministic code.
6. Use only owned canaries. Never collect another user's response or data.
7. Treat a timeout, error status, connection close, or scanner label as a lead until two-hop parser disagreement and connection reuse are causally bound.
8. Require separate approval before victim requests, response-queue poisoning, cache/routing effects, OAST, repeated ambiguity, or corpus-scale testing.
9. Stop at minimum sufficient evidence and run fresh-connection, unambiguous-framing, and patched/configured controls.

## Release-freeze and independent-review gate

Apply this ordering whenever the cascade runtime, schemas, integrity controls, or operator documentation change:

1. Finish all implementation and hardening edits before requesting independent review.
2. Declare a release freeze: after this point, do not add “one last guard” while verification or review is running.
3. Run the focused cascade tests, then test discovery with an explicit tests directory/pattern, compilation/static checks, and a fresh installed-CLI `prepare -> ingest -> verify-dispositions` smoke run. Set `PYTHONDONTWRITEBYTECODE=1` for read-only verification. A discovery command that reports `Ran 0 tests` is a failed gate; if browser-bound tests are opt-in, force their documented integration flag and require a zero-skip final run.
4. Build the smoke fixture from the live parser constants and a known-good current test helper, not from remembered or stale documentation. Exercise it with the digests returned by `prepare` and `ingest`, including one valid typed-`reportable` evidence manifest, evaluator result, externally pinned evidence index, and installed CLI option. Assert exact summary/manifest field names, all three cross-bindings, full identifier length, cardinality, private modes, proposal-only status, and zero packager interactions. Also verify fail-closed behavior with an invalid contract and confirm that no partial run directory remains. A temporary harness assertion that uses the wrong live field name is a harness defect, not evidence of a product blocker; inspect the live schema and rerun cleanly.
5. Before sealing, do one final blocker-focused self-review of newly introduced security-sensitive helpers. Distinguish local parsers such as `socket.inet_aton()` from DNS/network resolution; prove the actual call path before invalidating a release. Optional syscall tracing is extra evidence only when the tracer is present and produces a checked result—an unavailable tracer or empty compound-command output is not a pass.
6. Freeze an explicit artifact list. In a Git worktree, bind review to the reviewed diff/revision. In a non-Git vault, write a SHA-256 manifest outside the artifact tree and require `sha256sum -c` before and after review. Include runtime, tests, the exact installed wrapper target resolved by `readlink -f "$(command -v argus-research-cascade)"`, operator docs, template, evals, routing, changelog, and skill references that make release claims. Hash the seal file itself and retain that digest as the reviewer-visible seal identity.
7. Dispatch fresh-context, read-only reviewers only against that frozen set. Separate security/logic, requirement/documentation/test completeness, and adversarial release-gate review when practical. Require machine-parseable verdicts, seal-file digest plus entry confirmation before and after review, exact absolute file/line references and reproduction for blockers, and fail-closed semantics when the response cannot be parsed.
8. While review runs, perform read-only checks only. If any frozen file changes after review dispatch, treat every outstanding verdict as stale, regenerate the checksum manifest, rerun affected gates, and request a fresh review. A self-raised concern does not invalidate the seal until reproduced; document the read-only probe and preserve the seal when the concern is disproved.
9. Do not report final independent approval until every required reviewer result is actually available, parsed, checksum-valid, and blocker-free. Dispatch acknowledgement is not approval. If execution limits interrupt the gate, identify the exact frozen checksum set and leave the task in verification-incomplete state.

This prevents a strong earlier test run from being incorrectly presented as covering later hardening edits, and prevents an independent review from silently becoming stale.

## Verification checklist

- Implementation is frozen before final tests and independent review.
- A non-Git release has an external frozen-file SHA-256 manifest; all reviewers verify it before reading.
- Test discovery names the tests directory/pattern explicitly and runs a non-zero test count.
- Installed-CLI smoke covers both returned pins, typed reportable evidence, private modes, and invalid-contract rollback.
- No post-review-dispatch edits exist; otherwise checksums, tests, and review were rerun.
- Source revision and license recorded.
- Dependencies pinned or independently verified.
- Acquisition accepts sanitized local artifacts.
- Model inputs exclude secrets and target/private data.
- Generated corpora are private and local.
- Destination enforcement is default-deny and tested with an owned sink.
- Ambient Burp history cannot become a target source.
- Periodic, victim, OAST, and upload behavior is disabled by default.
- Local two-hop positive and negative controls pass.
- Every candidate has provenance, request budget, disposition, and independent falsification.

## Primary references

- `https://portswigger.net/research/can-ai-do-novel-security-research`
- `https://github.com/PortSwigger/http-terminator`
- `https://portswigger.net/blog/http-desync-attacks-request-smuggling-reborn`
