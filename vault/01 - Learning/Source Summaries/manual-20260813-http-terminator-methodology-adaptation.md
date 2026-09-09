---
type: source-summary
status: reviewed
created: "2026-08-13"
promotion_status: implemented-methodology
---

# HTTP Terminator methodology adaptation for Argus

## Sources reviewed

- Full PortSwigger article: `https://portswigger.net/research/can-ai-do-novel-security-research`
- Source repository: `https://github.com/PortSwigger/http-terminator`
- Reviewed repository revision: `874682cdbdd176099f5a1ddadd647fe1e66b5940`
- Repository license: GNU AGPL; reviewed `LICENSE` SHA-256 `0d96a4ff68ad6d4b6f1f30f713b18d5184912ba8dd389f86aa7710db079abcb0`
- HTTP desync safety context: `https://portswigger.net/blog/http-desync-attacks-request-smuggling-reborn`

## Coverage

The review covered the article and repository documentation, Seeker Python source/prompts/storage/tests, Flamer Gradle/source/build path, Validator extension/target-source/filter/control behavior, Investigator methodology/dependencies/tests, local Burp/Java compatibility, and existing Argus learning, routing, HTTP request-smuggling, evidence, and research-cascade controls.

## Promoted methodology

Argus adopts:

- 1-3 sentence attributed micro-inspiration fragments;
- fresh-context ideation workers that receive no previous hypothesis history;
- strict source hash, fragment lineage, and prepared-artifact integrity binding;
- invariant/evaluator/expected-observation/negative-control hypothesis fields;
- deterministic normalization and deduplication;
- proposal-only hypothesis ledgers;
- externally pinned prepare and ingestion manifests, with same-buffer parse/hash, recursive schema/cardinality validation, controlled pathological-JSON failure, and no-symlink file admission;
- conservative model-visible secret scanning; canonical public-provenance/capability-path rejection (including empty userinfo/port authorities, alternate numeric/private hosts, C0/C1 controls, malformed or non-canonical escapes, semicolon parameters, arbitrary encoding depth, and IP-first public classification for canonical bracketed IPv6); canonical raw-and-normalized bounds across contract, worker, disposition, and evidence-path strings; invalid-Unicode containment; per-prompt plus prepared-artifact and emitted-ledger phase-size compatibility; environment-independent installed-launcher binding to the reviewed runtime; and unpredictable staging made owner-accessible despite restrictive caller umask before descriptor open, with atomic no-replace publication, descriptor-relative exact-inode rollback, and run/parent-path revalidation;
- full-SHA-256 hypothesis identities that preserve shared-prefix collisions;
- typed, hypothesis-bound reportable evidence manifests plus hash-bound evaluator-result verdicts, authenticated by an externally pinned post-review evidence index, with disjoint hashed evaluator inputs/outputs, hard-link/inode alias rejection, distinct passed controls, reproduced observation, non-empty timezone-bound human review, duplicate-reference rejection, and a 20,000,000-byte aggregate evidence ceiling;
- fresh-context replicate/minimize/falsify review;
- exhaustive one-row-per-hypothesis terminal disposition.

Implementation:

- `11 - Scripts/learning/research_cascade.py`
- `~/.local/bin/argus-research-cascade`
- `00 - System/offline-research-cascade.md`
- `08 - Templates/research-cascade-contract.json.template`
- `06 - Evals/Web2/offline-security-research-cascade-eval-scenarios.md`

## Deliberately not adopted

Argus does not adopt:

- Seeker's URL acquisition or duplicate SQLite source database;
- broad prompt-to-malformed-request generation as a default hunting step;
- Flamer's optional SCP upload path;
- Validator's ambient proxy-history/file targeting, persisted periodic operation, victim/OAST/response-queue behavior, or prebuilt dependency;
- Investigator's proprietary MCP/Organizer assumptions or approval/sandbox bypass paths.

These components do not currently improve the yield-to-risk/maintenance ratio. If a selected hypothesis needs dynamic evaluation, Argus will implement the smallest exact owned harness rather than porting the generic scanner first.

## Safety and evidence boundary

The implemented packager accepts only reviewed local UTF-8 artifacts; fails closed on hash drift, declared or detected secret-like model input, malformed/non-canonical/capability-like provenance (including empty authority credentials/ports and C0/C1 controls), pathological JSON, invalid Unicode scalar strings before path/syscall use, raw/normalized size violations across contract/worker/disposition/evidence-path data, unsafe output parents, run/parent pathname replacement, restrictive caller umask during staging, environment-based installed-launcher runtime substitution, per-prompt or emitted-artifact incompatibility with the next phase, malformed supplied external pins, evidence path/inode aliasing, and live-interaction contracts; performs no network/model/target action; emits private phase-compatible artifacts; and requires an operator-held evidence-index SHA-256 pin over deterministic evaluator evidence and human review before a `reportable` terminal disposition. It creates research proposals, never live authorization or finding proof. Rich capture/model metadata belongs in a separately reviewed outer research record; undeclared worker-result fields remain rejected by the strict packager schema.
