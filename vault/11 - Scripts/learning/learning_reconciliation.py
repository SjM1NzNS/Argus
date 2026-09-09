#!/usr/bin/env python3
"""Deterministic run-coverage and source-health reconciliation for Argus learning."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from learning_registry import LearningRegistry, load_registry, select_sources
from learning_state import canonical_url, load_json_state, merge_json_state


DEGRADED_STATUSES = {
    "manual_review_required",
    "robots_blocked",
    "fetch_failed",
    "browser_failed",
    "skipped_run_budget_exceeded",
    "skipped_group_limit",
    "skipped_priority_filter",
    "skipped_backfill_source",
}
HEALTHY_ROOT_STATUSES = {
    "fetched_content",
    "fetched_index_metadata",
    "browser_fetched_content",
    "browser_fetched_index",
}


def reconcile_run(
    registry: LearningRegistry,
    records: list[dict],
    *,
    cadence: str,
    run_id: str | None = None,
    source_ids: set[str] | None = None,
) -> dict:
    expected = select_sources(registry, cadence=cadence, source_ids=source_ids)
    by_id = {source["id"]: source for source in expected}
    expected_ids = set(by_id)
    roots_by_source: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        if record.get("record_kind") == "root" and record.get("source_id") in expected_ids:
            roots_by_source[record["source_id"]].append(record)

    observed_ids = set(roots_by_source)
    duplicate_ids = sorted(source_id for source_id, roots in roots_by_source.items() if len(roots) != 1)
    provenance_mismatch: set[str] = set()
    degraded_ids: set[str] = set(duplicate_ids)
    root_statuses: dict[str, str] = {}
    for source_id, roots in roots_by_source.items():
        source = by_id[source_id]
        root = roots[-1]
        reasons = []
        if root.get("registry_schema_version") != registry.schema_version:
            reasons.append("registry_schema_mismatch")
        if root.get("registry_digest") != registry.digest:
            reasons.append("registry_digest_mismatch")
        if root.get("run_cadence") != cadence:
            reasons.append("run_cadence_mismatch")
        if run_id and root.get("run_id") != run_id:
            reasons.append("run_id_mismatch")
        if root.get("source_acquisition") != source.get("acquisition"):
            reasons.append("acquisition_mismatch")
        if reasons:
            provenance_mismatch.add(source_id)
            degraded_ids.add(source_id)
        status = str(root.get("local_processing_status") or "missing_status")
        root_statuses[source_id] = status
        if status not in HEALTHY_ROOT_STATUSES or status in DEGRADED_STATUSES or bool(root.get("fetch_error")):
            degraded_ids.add(source_id)

    missing = sorted(expected_ids - observed_ids)
    canonical_counts = Counter(
        canonical_url(record.get("effective_url") or record.get("url") or "")
        for record in records
        if record.get("record_kind") != "root" and (record.get("effective_url") or record.get("url"))
    )
    duplicate_candidate_url_count = sum(count - 1 for url, count in canonical_counts.items() if url and count > 1)
    per_source: dict[str, dict] = {}
    for source_id in sorted(expected_ids):
        source_records = [record for record in records if record.get("source_id") == source_id]
        per_source[source_id] = {
            "records": len(source_records),
            "root_status": root_statuses.get(source_id, "missing"),
            "discovered_records": sum(record.get("record_kind") != "root" for record in source_records),
            "actual_content_records": sum(record.get("content_quality") == "actual_content" for record in source_records),
            "seen_duplicates": sum(record.get("local_processing_status") == "skipped_seen_url" for record in source_records),
            "fetch_failures": sum(bool(record.get("fetch_error")) and record.get("local_processing_status") != "skipped_seen_url" for record in source_records),
        }

    degraded = sorted(degraded_ids)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run_id": run_id,
        "cadence": cadence,
        "registry_schema_version": registry.schema_version,
        "registry_digest": registry.digest,
        "expected_root_count": len(expected_ids),
        "expected_source_ids": sorted(expected_ids),
        "observed_root_count": len(observed_ids),
        "missing_source_ids": missing,
        "degraded_source_ids": degraded,
        "duplicate_root_source_ids": duplicate_ids,
        "provenance_mismatch_source_ids": sorted(provenance_mismatch),
        "record_count": len(records),
        "status_counts": dict(Counter(str(record.get("local_processing_status") or "unknown") for record in records)),
        "content_quality_counts": dict(Counter(str(record.get("content_quality") or "not_fetched") for record in records)),
        "candidate_url_count": len(canonical_counts),
        "duplicate_candidate_url_count": duplicate_candidate_url_count,
        "per_source": per_source,
        "complete": not missing and not degraded,
    }


def load_records(run_dir: Path) -> list[dict]:
    path = run_dir / "learning-candidates.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def update_health_state(path: Path, registry: LearningRegistry, report: dict) -> dict:
    state = load_json_state(path, default={"sources": {}}, warn=lambda message: print(message))
    now = report["generated_at"]
    run_id = report.get("run_id") or f"legacy-{now}"
    degraded = set(report["degraded_source_ids"])
    missing = set(report["missing_source_ids"])
    expected = set(report["expected_source_ids"])
    updates: dict = {
        "sources": {},
        "registry_digest": registry.digest,
        "last_runs": {
            report["cadence"]: {
                "run_id": run_id,
                "generated_at": now,
                "complete": report["complete"],
                "expected_roots": report["expected_root_count"],
                "observed_roots": report["observed_root_count"],
            }
        },
    }
    for source_id in expected:
        previous = state.get("sources", {}).get(source_id, {})
        if source_id in missing:
            status = "missing"
        elif source_id in degraded:
            status = "degraded"
        else:
            status = "healthy"
        entry = {
            "last_checked_at": now,
            "last_reconciled_at": now,
            "last_reconciled_run_id": run_id,
            "last_status": status,
            "last_cadence": report["cadence"],
            **report.get("per_source", {}).get(source_id, {}),
        }
        if status == "healthy":
            entry["last_success_at"] = now
            entry["consecutive_degraded_runs"] = 0
            if report["cadence"] == "weekly":
                entry["last_comprehensive_reconciliation_at"] = now
        else:
            entry["last_degraded_at"] = now
            if previous.get("last_reconciled_run_id") == run_id:
                entry["consecutive_degraded_runs"] = int(previous.get("consecutive_degraded_runs", 0))
            else:
                entry["consecutive_degraded_runs"] = int(previous.get("consecutive_degraded_runs", 0)) + 1
        updates["sources"][source_id] = entry
    return merge_json_state(path, updates, default={"sources": {}}, warn=lambda message: print(message))


def render_markdown(report: dict, registry: LearningRegistry) -> str:
    by_id = {s["id"]: s for s in registry.sources}
    lines = [
        f"# Learning {report['cadence']} reconciliation",
        "",
        f"- Generated: `{report['generated_at']}`",
        f"- Registry digest: `{report['registry_digest']}`",
        f"- Expected roots: `{report['expected_root_count']}`",
        f"- Observed roots: `{report['observed_root_count']}`",
        f"- Candidate URLs: `{report['candidate_url_count']}` (duplicates: `{report['duplicate_candidate_url_count']}`)",
        f"- Duplicate root IDs: `{len(report['duplicate_root_source_ids'])}`",
        f"- Provenance mismatches: `{len(report['provenance_mismatch_source_ids'])}`",
        f"- Complete: `{str(report['complete']).lower()}`",
        "",
        "## Missing roots",
        "",
    ]
    if report["missing_source_ids"]:
        for source_id in report["missing_source_ids"]:
            source = by_id[source_id]
            lines.append(f"- `{source_id}` — [{source['name']}]({source['url']})")
    else:
        lines.append("- None")
    lines.extend(["", "## Degraded roots", ""])
    if report["degraded_source_ids"]:
        for source_id in report["degraded_source_ids"]:
            source = by_id[source_id]
            lines.append(f"- `{source_id}` — [{source['name']}]({source['url']})")
    else:
        lines.append("- None")
    lines.extend(["", "## Per-source coverage and yield", "", "| Source ID | Root status | Records | Discovered | Actual content |", "|---|---:|---:|---:|---:|"])
    for source_id in report["expected_source_ids"]:
        item = report.get("per_source", {}).get(source_id, {})
        lines.append(
            f"| `{source_id}` | `{item.get('root_status', 'missing')}` | {item.get('records', 0)} | "
            f"{item.get('discovered_records', 0)} | {item.get('actual_content_records', 0)} |"
        )
    lines.extend(["", "## Status counts", ""])
    for status, count in sorted(report.get("status_counts", {}).items()):
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "> Reconciliation proves root traversal/health, not knowledge promotion. Ingestion remains proposal-only.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("registry_pos", nargs="?")
    parser.add_argument("run_dir_pos", nargs="?")
    parser.add_argument("--config", dest="registry_opt")
    parser.add_argument("--run-dir", dest="run_dir_opt")
    parser.add_argument("--cadence", default="weekly", choices=["daily", "weekly", "periodic", "backfill"])
    parser.add_argument("--source-ids", default="", help="Comma-separated exact source allowlist (required for targeted backfill reconciliation).")
    parser.add_argument("--health-state", default=str(Path.home() / ".config/argus/learning-source-health.json"))
    args = parser.parse_args()
    registry_path = args.registry_opt or args.registry_pos
    run_dir_value = args.run_dir_opt or args.run_dir_pos
    if not registry_path or not run_dir_value:
        parser.error("provide registry/run_dir positionally or with --config/--run-dir")
    registry = load_registry(registry_path)
    run_dir = Path(run_dir_value).expanduser()
    source_ids = {item.strip() for item in args.source_ids.split(",") if item.strip()} or None
    report = reconcile_run(
        registry,
        load_records(run_dir),
        cadence=args.cadence,
        run_id=run_dir.name,
        source_ids=source_ids,
    )
    json_path = run_dir / "learning-reconciliation.json"
    md_path = run_dir / "learning-reconciliation.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_markdown(report, registry), encoding="utf-8")
    update_health_state(Path(args.health_state).expanduser(), registry, report)
    print(json.dumps({**report, "json": str(json_path), "markdown": str(md_path)}, indent=2, sort_keys=True))
    return 0 if report["complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
