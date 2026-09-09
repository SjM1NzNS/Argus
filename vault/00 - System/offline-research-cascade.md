---
type: workflow
status: active
created_utc: "2026-08-13"
source_basis:
  - "https://portswigger.net/research/can-ai-do-novel-security-research"
  - "https://github.com/PortSwigger/http-terminator"
---

# Offline Source-to-Hypothesis Research Cascade

This workflow adapts only the parts of HTTP Terminator that improve Argus now: attributed micro-inspiration, fresh-context hypothesis generation, invariant-oriented evaluation contracts, deduplication, and exhaustive terminal disposition. It performs no acquisition, model call, payload generation, Burp loading, or target request by itself.

## When to use it

Use it when all of the following are true:

- a full public paper, RFC, advisory, or reviewed source artifact is already available locally;
- the source is sanitized or contains no secrets, authenticated captures, private briefs, capability URLs, target data, or personal data;
- the objective is one narrow mechanism class;
- fresh-context ideation could produce testable hypotheses that a static checklist would miss;
- hypotheses can later be evaluated in deterministic source review, fixed local fixtures, or an owned simulator.

Do not use it for routine daily learning, generic summarization, broad payload generation, or live-target automation.

## Phase contract

```text
reviewed local source
  -> prepare attributed 1-3 sentence fragments
  -> dispatch one fresh-context worker per task packet
  -> ingest strict JSON results
  -> deduplicate into proposal-only hypothesis ledger
  -> prior-art + deterministic evaluator + fresh-context falsification
  -> one terminal disposition per hypothesis
```

### 1. Prepare the source

1. Acquire and review the full source through the existing Argus source-first or learning workflow.
2. Save only the substantive, sanitized text to a local file.
3. Hash the exact file:

```bash
sha256sum /absolute/path/to/source.txt
```

4. Copy `08 - Templates/research-cascade-contract.json.template` and complete it. Keep:
   - `zone: 0`;
   - `live_target_interaction: false`;
   - `source_contains_secrets: false`;
   - one objective and explicit prohibited/duplicate families.

### 2. Prepare task packets

Create the immediate parent first and make it private. It must already exist, be owned by the current effective user, and have no group/other permission bits:

```bash
RUN_PARENT="$HOME/.local/share/argus-research-cascade/runs"
RUN_DIR="$RUN_PARENT/new-run"
install -d -m 0700 "$RUN_PARENT"

argus-research-cascade prepare \
  --contract /absolute/path/to/contract.json \
  --run-dir "$RUN_DIR"
```

The command fails closed on URL input paths; symlinked or non-regular input components; source hash drift; undeclared contract fields; non-Zone-0 contracts; unapproved model input; secret-like material detected in the source or any model-visible contract text even when `source_contains_secrets` is false; malformed, single-label, legacy-numeric/private-address, non-default-port, query/fragment-bearing, credential-delimited (including empty userinfo), empty-explicit-port, control-bearing, non-canonical encoded, or opaque capability-like provenance URLs; excessive raw or normalized contract-controlled prompt fields; any prepared task packet whose prompt exceeds ingest's 20,000-character field ceiling; prepared artifacts larger than the ingester's 5,000,000-byte per-artifact ceiling; a non-private/unowned immediate run parent; or an existing run directory. Canonical globally routable IPv4 and bracketed IPv6 provenance literals are classified by public-address semantics. Validated text/list fields are normalized before the canonical contract is hashed and emitted. Secret detection is a conservative admission guard, not a guarantee that arbitrary private material can be classified perfectly—operators must still sanitize and review the exact source bytes.

Run creation stages mode-private artifacts through an unpredictable directory beneath the already-open private parent. It records that entry's no-follow inode identity, forces that exact entry to `0700` despite caller `umask`, opens it descriptor-relatively, requires descriptor identity to match, and only then writes artifacts. It publishes the completed run with Linux atomic no-replace rename and never writes through the caller-declared run name before publication. Prepare, ingest, and closure revalidate both the run entry and the parent pathname device/inode before success; detected replacement cannot redirect a successful phase. Every phase tracks invocation-owned output by `(device, inode)` and removes it on failure only while that exact inode remains at the descriptor-relative name, preserving concurrent replacements and pre-existing files. These controls are fail-closed transaction checks, not isolation between mutually hostile processes sharing the effective UID; such processes already have equivalent authority over the user-owned private tree and can race after any final check. The packager writes mode-`0600` files under a mode-`0700` run directory, hashes every prepared artifact in `run-manifest.json`, returns that manifest's SHA-256 as the operator-held integrity pin, and records zero network/target interactions. The installed launcher is bound to the reviewed absolute runtime path and does not derive executable code from mutable `HOME`.

Record the returned `manifest_sha256` **outside the mutable run directory**. Do not recover or replace this pin by re-hashing `run-manifest.json` after ideation; the external pin is what detects coordinated manifest/provenance tampering.

### 3. Dispatch fresh-context ideation

Read `task-packets.jsonl`. Dispatch each packet independently with `delegate_task` and **no toolsets**. Each worker receives one fragment rather than the full paper or prior hypotheses. This preserves creative isolation and prevents anchoring.

Save exact worker JSON objects, one per line, to `hypothesis-results.jsonl`. Do not repair malformed output silently; rerun that worker or keep the ideation phase explicitly incomplete. Ingestion cannot create a ledger until every prepared fragment has exactly one valid result object.

### 4. Normalize and deduplicate

```bash
argus-research-cascade ingest \
  --run-dir "$RUN_DIR" \
  --results /absolute/path/to/hypothesis-results.jsonl \
  --manifest-sha256 "$MANIFEST_SHA256"
```

The ingester:

- accepts only the declared schema;
- requires exactly one result object per prepared fragment and rejects incomplete or duplicate worker coverage;
- re-verifies all prepared artifact hashes before trusting fragment or contract state;
- rejects unknown fragment IDs and undeclared payload-like fields;
- rejects duplicate JSON keys, pathological decoder depth/integer inputs, invalid Unicode scalar strings, and oversized raw or normalized output fields/lists through bounded `CascadeError`;
- recursively validates the run manifest, fragments, task packets, result rows, ingestion manifest, and all count/cardinality/provenance relationships;
- refuses to publish an emitted hypothesis ledger above closure's 5,000,000-byte admission ceiling;
- normalizes whitespace;
- deduplicates by title + mechanism + invariant;
- persists the complete SHA-256 identity as `hypothesis-<64 lowercase hex>` so distinct hypotheses cannot alias through a truncated display ID;
- preserves every source-fragment lineage;
- emits `hypothesis-ledger.jsonl` with `proposal_only` and `target_interaction_allowed: false`.

The command returns `ingestion_manifest_sha256`. Preserve it outside the run directory alongside `manifest_sha256`; closure requires both independent pins. The ledger is a research queue, not evidence.

### 5. Evaluate safely

For each hypothesis:

1. Search prior art before implementation.
2. State the boundary invariant and expected observation.
3. Prefer source inspection, parser/library unit tests, fixed-source replay, or an owned local simulator.
4. Build the smallest deterministic evaluator; keep the source fixed while changing the candidate variable.
5. Include a matched negative control and known-positive control where available.
6. Preserve exact artifact hashes and evaluator versions.
7. Delegate replicate/minimize/falsify reviews in fresh contexts.
8. Stop on unsupported topology, ambiguous observation, nondeterminism, source drift, or missing authorization.

Target-specific work still requires the exact program contract, relevant playbooks, and separate action approval. This workflow never grants live-target authorization.

### 6. Close every hypothesis

Create JSONL with exactly these fields:

```json
{"hypothesis_id":"hypothesis-<64-lowercase-hex>","disposition":"coverage_gap","reason":"...","evidence_refs":[],"next_safe_action":"..."}
```

Allowed terminal dispositions:

- `reportable`
- `disproved`
- `blocked`
- `coverage_gap`
- `duplicate`

Then run:

```bash
argus-research-cascade verify-dispositions \
  --run-dir "$RUN_DIR" \
  --dispositions /absolute/path/to/dispositions.jsonl \
  --manifest-sha256 "$MANIFEST_SHA256" \
  --ingestion-manifest-sha256 "$INGESTION_MANIFEST_SHA256" \
  --evidence-index-sha256 "$EVIDENCE_INDEX_SHA256"
```

Omit `--evidence-index-sha256` only when no disposition is `reportable`. For any reportable row, create `evidence-index.json`, review its exact content, compute its SHA-256 externally, and retain that third pin outside the mutable run directory before closure.

Closure opens untrusted files once without following symlinks, bounds raw strings and validates UTF-8 scalar text before any path/syscall use, parses and hashes the same bounded bytes, syntax-checks every supplied external digest even when an optional evidence-index pin is unnecessary for non-reportable closure, re-verifies the externally pinned run, ingestion, and (when reportable) evidence-index manifests, prepared artifacts, ledger schema/count/hash, typed identifier formats, and disposition cardinality, then writes `closure-manifest.json`. It fails if a hypothesis is missing, duplicated, unknown, malformed, non-terminal, or called `reportable` without an externally pinned evidence-index entry and valid typed evidence bundle.

For `reportable`, each `evidence_refs` entry must name a run-local evidence-manifest JSON file with exactly this shape (`hypothesis_id` contains 64 lowercase hex characters after `hypothesis-`):

```json
{
  "schema_version": 1,
  "hypothesis_id": "hypothesis-<64-lowercase-hex>",
  "evaluator": {"identity": "owned-fixture-name", "version": "immutable-version"},
  "input_artifacts": {"evidence/input.json": "<sha256>"},
  "output_artifacts": {
    "evidence/positive.json": "<sha256>",
    "evidence/negative.json": "<sha256>",
    "evidence/evaluator-result.json": "<sha256>"
  },
  "evaluator_result": "evidence/evaluator-result.json"
}
```

The hash-bound evaluator result owns the verdict fields:

```json
{
  "schema_version": 1,
  "run_id": "<run-id>",
  "hypothesis_id": "hypothesis-<64-lowercase-hex>",
  "evaluator": {"identity": "owned-fixture-name", "version": "immutable-version"},
  "positive_control": {"status": "passed", "evidence_ref": "evidence/positive.json"},
  "negative_control": {"status": "passed", "evidence_ref": "evidence/negative.json"},
  "observation_status": "reproduced"
}
```

`evidence-index.json` is the externally authenticated post-review trust anchor:

```json
{
  "schema_version": 1,
  "run_id": "<run-id>",
  "run_manifest_sha256": "<operator-held-prepare-pin>",
  "ingestion_manifest_sha256": "<operator-held-ingest-pin>",
  "entries": [{
    "hypothesis_id": "hypothesis-<64-lowercase-hex>",
    "evidence_manifest": "evidence/manifest.json",
    "evidence_manifest_sha256": "<sha256>",
    "evaluator_result": "evidence/evaluator-result.json",
    "evaluator_result_sha256": "<sha256>",
    "independent_review": {
      "decision": "approved",
      "reviewer": "human:<non-empty-reviewer-identity>",
      "reviewed_at": "2026-08-13T00:00:00Z"
    }
  }]
}
```

Every declared input/output digest is rechecked. Every evidence reference and artifact-map key is raw-bounded and validated as UTF-8 scalar text before normalization or filesystem use. Input and output path sets must be disjoint; positive and negative controls must pass and reference distinct hashed output artifacts with distinct content; the observation must be reproduced; and the externally pinned index must record explicit approval by a non-empty human-bound reviewer at a timezone-aware timestamp. Evidence-manifest references and artifact paths cannot be duplicated, symlink-aliased, or hard-link/inode-aliased across reportable rows. Individual manifests/artifacts retain their per-file bounds, and the exact admitted bytes across all unique reportable manifests and artifacts cannot exceed 20,000,000 bytes. Absolute paths, traversal, invalid Unicode, symlinked path components, model-claim files, hash drift, control aliasing, stale, malformed, or missing external pins, or budget exhaustion fail closed. The closure manifest binds all supplied operator pins, the exact dispositions bytes, and all validated evidence-manifest/artifact hashes.

## Non-adopted HTTP Terminator components

Leave these out until their benefit exceeds their safety and maintenance cost:

- arbitrary URL fetching or duplicate acquisition/database layers;
- general LLM-generated malformed-request corpora;
- SCP/remote corpus upload;
- ambient Burp proxy-history target discovery;
- periodic validation restored from preferences;
- victim-request, response-queue, Collaborator/OAST, or production connection-poisoning automation;
- prebuilt Burp dependencies without source/provenance correspondence;
- proprietary Investigator MCP assumptions or bypassed approval/sandbox modes.

If a deterministic owned parser harness becomes necessary, implement only the exact evaluator required by a selected hypothesis. Do not first port the generic Validator.

## Acceptance criteria

A cascade improved the workflow only if it produces at least one of:

- a novel testable invariant;
- a lower-noise deterministic evaluator;
- a useful negative-control or false-positive rule;
- a concrete coverage gap worth fixing;
- a well-supported playbook/eval improvement after review.

If it produces generic restatements, payload churn, duplicate ideas, or hypotheses that cannot be safely evaluated, close them and do not expand the system.
