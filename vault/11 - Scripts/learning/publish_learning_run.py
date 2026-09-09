#!/usr/bin/env python3
"""Publish a deterministic learning-run manifest and exact-cadence pointer."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from learning_registry import load_registry, select_sources
from learning_state import canonical_url, write_json_atomic


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_records(run_dir: Path) -> list[dict]:
    path = run_dir / "learning-candidates.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_manifest(
    *,
    registry_path: Path,
    run_dir: Path,
    cadence: str,
    reconciliation_exit: int,
    source_ids: set[str] | None = None,
) -> dict:
    registry = load_registry(registry_path)
    selected = select_sources(registry, cadence=cadence, source_ids=source_ids)
    records = load_records(run_dir)
    reconciliation_path = run_dir / "learning-reconciliation.json"
    reconciliation = load_json(reconciliation_path) if reconciliation_path.exists() else {}
    compiler_report = run_dir / "learning-compiler-run.md"
    provenance_path = Path.home() / "SecurityResearch" / "01 - Learning" / "Provenance Manifests" / f"{run_dir.name}.jsonl"
    dispositions: list[dict] = []
    if provenance_path.exists():
        dispositions = [json.loads(line) for line in provenance_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    urls = [canonical_url(record.get("effective_url") or record.get("url") or "") for record in records if record.get("url")]
    duplicate_count = len(urls) - len(set(urls))
    compiled_count = sum(1 for item in dispositions if item.get("disposition") == "draft_compiled_pending_review")
    complete = bool(reconciliation.get("complete")) and reconciliation_exit == 0
    ready_for_review = complete and compiler_report.exists()
    generated_at = datetime.now(timezone.utc).isoformat()
    manifest = {
        "manifest_schema_version": 1,
        "run_id": run_dir.name,
        "cadence": cadence,
        "generated_at": generated_at,
        "run_dir": str(run_dir),
        "registry_path": str(registry_path),
        "registry_schema_version": registry.schema_version,
        "registry_digest": registry.digest,
        "source_filter": sorted(source_ids) if source_ids is not None else None,
        "selected_source_ids": [source["id"] for source in selected],
        "selected_source_count": len(selected),
        "record_count": len(records),
        "root_record_count": sum(1 for record in records if record.get("record_kind") == "root"),
        "candidate_url_count": len(urls),
        "duplicate_candidate_url_count": duplicate_count,
        "status_counts": dict(Counter(record.get("local_processing_status") or "unknown" for record in records)),
        "content_quality_counts": dict(Counter(record.get("content_quality") or "unknown" for record in records)),
        "disposition_counts": dict(Counter(item.get("disposition") or "unknown" for item in dispositions)),
        "draft_compiled_count": compiled_count,
        "reconciliation": {
            "path": str(reconciliation_path),
            "exit_code": reconciliation_exit,
            "complete": bool(reconciliation.get("complete")),
            "missing_source_ids": reconciliation.get("missing_source_ids", []),
            "degraded_source_ids": reconciliation.get("degraded_source_ids", []),
            "provenance_error_count": len(reconciliation.get("provenance_mismatch_source_ids", [])),
        },
        "compiler": {
            "report": str(compiler_report),
            "completed": compiler_report.exists(),
            "provenance_manifest": str(provenance_path),
            "provenance_manifest_sha256": hashlib.sha256(provenance_path.read_bytes()).hexdigest() if provenance_path.exists() else None,
        },
        "ready_for_review": ready_for_review,
        "review_contract": "Consume this exact run_id only. Promotion remains manual/proposal-only and requires source-specific review/corroboration/eval/changelog linkage.",
    }
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--cadence", required=True, choices=["daily", "weekly", "periodic", "backfill"])
    parser.add_argument("--reconciliation-exit", required=True, type=int)
    parser.add_argument("--source-ids", default="")
    parser.add_argument("--pointer-dir", default=str(Path.home() / ".config/argus"))
    args = parser.parse_args()
    source_ids = {item.strip() for item in args.source_ids.split(",") if item.strip()} or None
    manifest = build_manifest(
        registry_path=Path(args.config).expanduser(),
        run_dir=Path(args.run_dir).expanduser(),
        cadence=args.cadence,
        reconciliation_exit=args.reconciliation_exit,
        source_ids=source_ids,
    )
    manifest_path = Path(args.run_dir).expanduser() / "learning-run-manifest.json"
    pointer_path = Path(args.pointer_dir).expanduser() / f"latest-{args.cadence}-learning-run.json"
    write_json_atomic(manifest_path, manifest)
    write_json_atomic(pointer_path, manifest)
    print(json.dumps({"manifest": str(manifest_path), "pointer": str(pointer_path), "ready_for_review": manifest["ready_for_review"]}, sort_keys=True))


if __name__ == "__main__":
    main()
