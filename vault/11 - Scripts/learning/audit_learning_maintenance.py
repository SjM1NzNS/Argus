#!/usr/bin/env python3
"""Read-only periodic maintenance audit for the Argus learning knowledge base."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from learning_registry import load_registry


def age_days(path: Path, now: datetime) -> float:
    return (now.timestamp() - path.stat().st_mtime) / 86400.0


def indexed_paths(root: Path) -> tuple[list[str], list[str]]:
    found, missing = [], []
    for index in (root / "00 - System" / "web2-skill-index.md", root / "00 - System" / "web3-skill-index.md"):
        if not index.exists():
            missing.append(str(index))
            continue
        for value in re.findall(r"`([^`]+\.md)`", index.read_text(encoding="utf-8", errors="replace")):
            candidate = Path(value).expanduser()
            if not candidate.is_absolute():
                candidate = root / value
            found.append(str(candidate))
            if not candidate.exists():
                missing.append(str(candidate))
    return sorted(set(found)), sorted(set(missing))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="~/.config/argus/learning-sources.yaml")
    parser.add_argument("--root", default="~/SecurityResearch")
    parser.add_argument("--health-state", default="~/.config/argus/learning-source-health.json")
    parser.add_argument("--stale-playbook-days", type=int, default=180)
    parser.add_argument("--stale-proposal-days", type=int, default=30)
    parser.add_argument("--output")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    root = Path(args.root).expanduser()
    registry = load_registry(Path(args.config).expanduser())
    playbook_root = root / "02 - Vulnerability Playbooks"
    proposal_roots = [root / "01 - Learning" / "Skill Patch Proposals", root / "06 - Evals" / "Learning Proposals"]
    playbooks = [p for p in playbook_root.rglob("*.md") if p.is_file()]
    stale_playbooks = sorted(str(p) for p in playbooks if age_days(p, now) >= args.stale_playbook_days)
    proposals = [p for base in proposal_roots if base.exists() for p in base.rglob("*.md") if p.is_file()]
    stale_proposals = sorted(str(p) for p in proposals if age_days(p, now) >= args.stale_proposal_days)
    indexed, missing_index_targets = indexed_paths(root)

    health_path = Path(args.health_state).expanduser()
    health = json.loads(health_path.read_text(encoding="utf-8")) if health_path.exists() else {"sources": {}}
    degraded = sorted(
        ({"source_id": sid, **entry}
         for sid, entry in health.get("sources", {}).items()
         if int(entry.get("consecutive_degraded_runs", 0)) >= 2),
        key=lambda item: item["source_id"],
    )
    health_sources = health.get("sources", {})
    never_checked = sorted(source["id"] for source in registry.sources if source["id"] not in health_sources)
    overdue = []
    for source in registry.sources:
        if source["cadence"] not in {"daily", "weekly"}:
            continue
        last = health_sources.get(source["id"], {}).get("last_success_at")
        try:
            age = (now - datetime.fromisoformat(last.replace("Z", "+00:00"))).total_seconds() / 86400.0
        except (AttributeError, TypeError, ValueError):
            age = float("inf")
        allowed = 2 if source["cadence"] == "daily" else 9
        if age > allowed:
            overdue.append({"source_id": source["id"], "cadence": source["cadence"], "days_since_success": None if age == float("inf") else round(age, 1)})

    decision_root = root / "01 - Learning" / "Promotion Decisions"
    decision_files = list(decision_root.rglob("*.md")) if decision_root.exists() else []
    decision_counts: Counter[str] = Counter()
    for decision in decision_files:
        match = re.search(r"^disposition:\s*([^\n]+)", decision.read_text(encoding="utf-8", errors="replace"), re.MULTILINE)
        decision_counts[(match.group(1).strip() if match else "unstructured")] += 1
    provenance_root = root / "01 - Learning" / "Provenance Manifests"
    provenance_manifests = list(provenance_root.glob("*.jsonl")) if provenance_root.exists() else []

    payload = {
        "generated_at": now.isoformat(),
        "registry": {
            "schema_version": registry.schema_version,
            "digest": registry.digest,
            "sources": len(registry.sources),
            "cadences": dict(Counter(s["cadence"] for s in registry.sources)),
            "roles": dict(Counter(s["role"] for s in registry.sources)),
        },
        "playbooks": {"total": len(playbooks), "stale": stale_playbooks},
        "proposals": {"total": len(proposals), "stale_unresolved": stale_proposals},
        "indexes": {"referenced_markdown": len(indexed), "missing_targets": missing_index_targets},
        "source_health": {
            "repeatedly_degraded": degraded,
            "never_reconciled": never_checked,
            "overdue_daily_or_weekly": overdue,
        },
        "learning_history": {
            "durable_provenance_manifests": len(provenance_manifests),
            "promotion_decisions": len(decision_files),
            "decision_counts": dict(decision_counts),
        },
        "eval_coverage": {
            "web2_eval_files": len(list((root / "06 - Evals" / "Web2").rglob("*.md"))),
            "web3_eval_files": len(list((root / "06 - Evals" / "Web3").rglob("*.md"))),
            "note": "Counts are an audit cue; promotion still requires class-specific eval review rather than filename heuristics.",
        },
    }
    output = Path(args.output).expanduser() if args.output else root / "12 - Logs" / "learning" / f"maintenance-audit-{now.strftime('%Y%m%d-%H%M%S')}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Argus Learning Maintenance Audit", "",
        f"- Generated: `{payload['generated_at']}`",
        f"- Registry: schema `{registry.schema_version}`, digest `{registry.digest}`, sources `{len(registry.sources)}`",
        f"- Cadence counts: `{payload['registry']['cadences']}`",
        f"- Playbooks: `{len(playbooks)}` total, `{len(stale_playbooks)}` older than {args.stale_playbook_days} days",
        f"- Outstanding proposals: `{len(proposals)}` total, `{len(stale_proposals)}` older than {args.stale_proposal_days} days",
        f"- Index references missing: `{len(missing_index_targets)}`",
        f"- Sources degraded in at least two reconciliations: `{len(degraded)}`",
        f"- Sources never represented in health state: `{len(never_checked)}`; overdue daily/weekly: `{len(overdue)}`",
        f"- Durable provenance manifests: `{len(provenance_manifests)}`; structured promotion decisions: `{len(decision_files)}` (`{dict(decision_counts)}`)",
        f"- Eval files: Web2 `{payload['eval_coverage']['web2_eval_files']}`, Web3 `{payload['eval_coverage']['web3_eval_files']}`", "",
        "## Maintenance queues", "",
        "### Stale playbook review", *([f"- `{p}`" for p in stale_playbooks] or ["- None."]), "",
        "### Stale proposal review", *([f"- `{p}`" for p in stale_proposals] or ["- None."]), "",
        "### Missing taxonomy/index targets", *([f"- `{p}`" for p in missing_index_targets] or ["- None."]), "",
        "### Repeatedly degraded sources", *([f"- `{d['source_id']}` — status `{d.get('last_status')}`, consecutive `{d.get('consecutive_degraded_runs')}`" for d in degraded] or ["- None."]), "",
        "### Overdue daily/weekly coverage", *([f"- `{d['source_id']}` — cadence `{d['cadence']}`, days since success `{d['days_since_success']}`" for d in overdue] or ["- None."]), "",
        "### Never reconciled (includes intentional periodic/on-demand sources)", *([f"- `{source_id}`" for source_id in never_checked] or ["- None."]), "",
        "## Policy", "",
        "- This audit is read-only. Staleness is a review signal, not evidence that content is wrong.",
        "- Foundational sources are refreshed only through an explicit targeted backfill with a recorded reason.",
        "- Taxonomy/index and eval changes remain review-gated and must be recorded in the skill changelog.",
    ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({**payload, "output": str(output)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
