#!/usr/bin/env python3
"""Argus learning compiler.

Consumes learning-candidates.jsonl and compiles only substantial deep content into
source summaries, skill patch proposals, rejected/discovery audits, and eval proposals.
Index/listing records are discovery context only.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from learning_promotion import classify_knowledge_types, promotion_requirements
from learning_registry import load_registry
from learning_safety import scope_disposition
from learning_state import canonical_url

ROOT = Path.home() / "SecurityResearch"
INBOX_ROOT = ROOT / "01 - Learning" / "Inbox"
SOURCE_SUMMARIES = ROOT / "01 - Learning" / "Source Summaries"
PATCH_PROPOSALS = ROOT / "01 - Learning" / "Skill Patch Proposals"
REJECTED = ROOT / "01 - Learning" / "Rejected Lessons"
EVALS = ROOT / "06 - Evals"
CHANGELOG_DIR = ROOT / "07 - Skill Changelog"
PROVENANCE_MANIFESTS = ROOT / "01 - Learning" / "Provenance Manifests"
REGISTRY_PATH = Path(__import__("os").environ.get("ARGUS_LEARNING_CONFIG", str(Path.home() / ".config/argus/learning-sources.yaml"))).expanduser()
ALLOW_LEGACY = __import__("os").environ.get("ARGUS_COMPILER_ALLOW_LEGACY", "").lower() in {"1", "true", "yes"}

MIN_COMPILE_CHARS = int(__import__("os").environ.get("ARGUS_COMPILER_MIN_CONTENT_CHARS", "1200"))
MAX_RECORDS = int(__import__("os").environ.get("ARGUS_COMPILER_MAX_RECORDS", "40"))

WEB2_CLASSES = [
    ("IDOR / BOLA / Access Control", ["idor", "bola", "object reference", "access control", "authorization", "cross-tenant", "tenant"]),
    ("Authentication / Session", ["oauth", "saml", "mfa", "session", "login", "password reset", "passkey", "token"]),
    ("API Security", ["api", "graphql", "rest", "endpoint", "object level", "rate limit"]),
    ("AI / LLM Security", ["prompt injection", "llm", "ai security", "agent", "model", "tool call", "indirect prompt", "jailbreak"]),
    ("File Upload / Media Processing", ["upload", "file", "media", "image", "audio", "decoder", "attachment"]),
    ("Race Conditions / TOCTOU", ["race", "toctou", "time-of-check", "time of check"]),
    ("Client-Side / XSS", ["xss", "cross-site scripting", "dom", "script"]),
]
WEB3_CLASSES = [
    ("Bridge / Proof Validation", ["bridge", "zk proof", "proof", "settlement", "rollup"]),
    ("Access Control / Admin Key", ["admin key", "owner", "privilege", "ownership", "admin privileges"]),
    ("Accounting / Invariants", ["accounting", "invariant", "withdraw", "drain", "locked", "liquidity"]),
    ("Oracle / Economic", ["oracle", "price", "liquidation", "manipulation"]),
]


def latest_inbox() -> Path:
    raise SystemExit(
        "Explicit inbox path required; do not infer latest by lexical directory order. "
        "Use a cadence pointer in ~/.config/argus/latest-<cadence>-learning-run.json."
    )


def slugify(s: str, limit: int = 90) -> str:
    s = re.sub(r"https?://", "", s.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return (s[:limit].strip("-") or "source")


REQUIRED_PROVENANCE_FIELDS = {
    "source_id",
    "registry_schema_version",
    "registry_digest",
    "run_id",
    "run_cadence",
    "record_kind",
    "source_role",
    "source_trust",
    "promotion_policy",
    "original_source_required",
    "independent_corroboration",
}


def candidate_id_for_record(record: dict) -> str:
    identity = "\n".join([
        str(record.get("source_id") or "unbound"),
        canonical_url(record.get("effective_url") or record.get("url") or ""),
        str(record.get("content_hash") or "no-content-hash"),
    ])
    return "candidate-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20]


def provenance_admission(record: dict, *, expected_registry_digest: str) -> tuple[bool, list[str]]:
    reasons = [f"missing_{field}" for field in sorted(REQUIRED_PROVENANCE_FIELDS) if field not in record]
    if record.get("registry_digest") and record.get("registry_digest") != expected_registry_digest:
        reasons.append("registry_digest_mismatch")
    if record.get("record_kind") not in {"discovered_content", "source_native_content"}:
        reasons.append("record_kind_not_compilable")
    return not reasons, reasons


def sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text or "").strip()
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9$])", text)
    return [p.strip() for p in parts if len(p.strip()) > 40]


def choose_sentences(text: str, keywords: list[str], n: int = 4) -> list[str]:
    sents = sentences(text)
    scored = []
    for i, s in enumerate(sents):
        low = s.lower()
        score = sum(3 for k in keywords if k in low)
        score += sum(1 for k in ["attacker", "exploit", "bypass", "access", "modify", "delete", "drain", "proof", "impact", "vulnerability", "fix", "mitigation"] if k in low)
        if score:
            scored.append((score, -i, s))
    return [x[2] for x in sorted(scored, reverse=True)[:n]] or sents[:n]


def classify(rec: dict) -> tuple[str, str, list[str]]:
    title = (rec.get("title") or "").lower()
    url = (rec.get("url") or "").lower()
    topic = (rec.get("topic") or "").lower()
    content = (rec.get("content_excerpt") or rec.get("short_excerpt_or_summary") or "").lower()
    # Weight title/URL/topic heavily; extracted page text often contains navigation
    # terms (XSS/API/etc.) unrelated to the specific article.
    primary = " ".join([title, url, topic])
    text = " ".join([primary, primary, primary, content])
    is_web3 = rec.get("source_group") == "web3_continuous_monitoring" or any(x in url for x in ["rekt.news", "code4rena", "solodit", "immunefi", "openzeppelin", "trailofbits"])

    # High-confidence overrides first.
    if any(x in primary for x in ["idor", "bola", "broken-object", "object-reference", "access-control", "cross-tenant"]):
        best_name, kws = "IDOR / BOLA / Access Control", ["idor", "bola", "object reference", "access control", "authorization", "cross-tenant", "tenant"]
    elif any(x in primary for x in ["race", "toctou", "time-of-check", "path-lookup"]):
        best_name, kws = "Race Conditions / TOCTOU", ["race", "toctou", "time-of-check", "time of check", "path lookup"]
    elif re.search(r"\b(prompt injection|llm|ai security|ai model|agentic|agent|jailbreak|model poisoning)\b", primary):
        best_name, kws = "AI / LLM Security", ["prompt injection", "llm", "ai security", "agent", "model", "tool call", "indirect prompt", "jailbreak"]
    elif any(x in primary for x in ["dolby", "dng", "image", "imessage", "zero-click", "0-click", "decoder", "media"]):
        best_name, kws = "File Upload / Media Processing", ["upload", "file", "media", "image", "audio", "decoder", "attachment", "zero-click"]
    elif any(x in primary for x in ["aztec", "bridge", "rollup", "zk"]):
        best_name, kws = "Bridge / Proof Validation", ["bridge", "zk proof", "proof", "settlement", "rollup"]
    elif any(x in primary for x in ["dxsale", "admin", "owner", "ownership"]):
        best_name, kws = "Access Control / Admin Key", ["admin key", "owner", "privilege", "ownership", "admin privileges"]
    else:
        classes = WEB3_CLASSES if is_web3 else WEB2_CLASSES
        best = (0, "Web3 General" if is_web3 else "Web2 General", [])
        for name, class_kws in classes:
            score = sum(2 for k in class_kws if k in primary) + sum(1 for k in class_kws if k in content)
            if score > best[0]:
                best = (score, name, class_kws)
        best_name, kws = best[1], best[2]

    category = "unclassified_candidate"
    if "false positive" in text or "not vulnerable" in text:
        category = "false-positive pattern"
    elif any(x in text for x in ["severity", "cvss", "critical", "high severity"]):
        category = "severity rule"
    elif any(x in primary for x in ["how to", "testing for", "guide", "workflow"]):
        category = "technique"
    elif any(x in primary for x in ["cve-", "ghsa-", "advisory", "exploit", "vulnerability", "rekt"]):
        category = "vulnerability pattern"
    return category, best_name, kws


def source_quality(rec: dict) -> int:
    """Legacy display value derived only from categorical registry trust.

    It is never a promotion decision and must not increase because content is long or
    hosted on a familiar domain.
    """
    return int(rec.get("source_quality_default") or 0)


def compile_record(rec: dict, out_dir: Path) -> dict:
    category, vuln_class, kws = classify(rec)
    text = rec.get("content_excerpt") or rec.get("short_excerpt_or_summary") or ""
    key_sents = choose_sentences(text, kws)
    quality = source_quality(rec)
    knowledge_types = classify_knowledge_types(" ".join([rec.get("title") or "", text]))
    gate = promotion_requirements({
        "role": rec.get("source_role"),
        "trust": rec.get("source_trust"),
        "promotion_policy": rec.get("promotion_policy"),
        "original_source_required": rec.get("original_source_required", False),
        "independent_corroboration": rec.get("independent_corroboration", "required"),
    })
    title = rec.get("title") or rec.get("source_name") or rec.get("url")
    url = rec.get("url")
    effective_url = rec.get("effective_url") or url
    candidate_id = candidate_id_for_record(rec)
    scope = scope_disposition(" ".join([title or "", text]))
    affected_surface = "Web3 protocol / smart contract" if rec.get("source_domain") == "web3" else "Web/API/application surface"
    if "File Upload" in vuln_class: affected_surface = "File upload / media parser / async processing surface"
    if "Access Control" in vuln_class or "IDOR" in vuln_class: affected_surface = "Object, tenant, account, or authorization boundary"
    if "Bridge" in vuln_class: affected_surface = "Bridge, rollup, proof verification, or settlement boundary"

    summary_path = out_dir / f"{candidate_id}-{slugify(title or url, limit=60)}.md"
    md = [
        "---",
        "type: learning-source-summary",
        f"candidate_id: {candidate_id}",
        "generator_kind: deterministic-heuristic-draft",
        "review_status: pending",
        "promotion_target: vault_playbook",
        f"safety_scope: {scope}",
        f"compiled_at: {datetime.now(timezone.utc).isoformat()}",
        f"source_quality: {quality}",
        f"source_id: {rec.get('source_id') or 'legacy-unbound'}",
        f"source_role: {rec.get('source_role') or 'unknown'}",
        f"source_trust: {rec.get('source_trust') or 'contextual'}",
        f"promotion_policy: {gate['promotion_policy']}",
        f"promotion_status: {gate['promotion_status']}",
        f"knowledge_types: [{', '.join(knowledge_types)}]",
        f"classification: {category}",
        f"vulnerability_class: {vuln_class}",
        "---",
        "",
        f"# {title}",
        "",
        f"- Candidate ID: `{candidate_id}`",
        f"- Original URL: `{url}`",
        f"- Effective URL: `{effective_url}`",
        f"- Retrieved at / content SHA-256: `{rec.get('retrieved_at') or 'unknown'}` / `{rec.get('content_hash') or 'unavailable'}`",
        f"- Source ID / role / trust: `{rec.get('source_id') or 'legacy-unbound'}` / `{rec.get('source_role') or 'unknown'}` / `{rec.get('source_trust') or 'contextual'}`",
        f"- Parent source / discovery root: `{rec.get('parent_source_id') or rec.get('source_id') or 'unknown'}` / `{rec.get('discovered_from') or 'direct root'}`",
        f"- Acquisition provenance: run=`{rec.get('run_id') or 'legacy'}`, cadence=`{rec.get('run_cadence') or 'legacy'}`, method=`{rec.get('source_acquisition') or 'unknown'}`",
        f"- Registry schema/digest: `{rec.get('registry_schema_version') or 'legacy'}` / `{rec.get('registry_digest') or 'unavailable'}`",
        f"- Source group: `{rec.get('source_group')}`",
        f"- Content chars: `{rec.get('content_char_count')}`",
        f"- Classification: **{category}**",
        f"- Vulnerability class: **{vuln_class}**",
        "",
        "## Source summary",
        "",
    ]
    for s in key_sents[:3]: md.append(f"- {s}")
    md += [
        "",
        "## Heuristic review prompts (not extracted facts)",
        "",
        f"- Possible affected surface: {affected_surface}",
        "- Reviewer must identify source-specific preconditions, validation steps, evidence requirements, false-positive gates, and reportability implications from the cited material.",
        "- Do not copy generic compiler text into a mature playbook. If the source does not establish a novel, concrete rule, reject or defer this candidate.",
        f"- Safety scope: `{scope}`. A `scope_review_required` candidate is quarantined from proposal generation pending explicit authorized-scope review.",
        "",
        "## Knowledge and promotion semantics",
        "",
        f"- Candidate knowledge types: `{', '.join(knowledge_types) if knowledge_types else 'unclassified'}`",
        f"- Promotion status: `{gate['promotion_status']}`; manual review required: `{str(gate['manual_review_required']).lower()}`",
        f"- Original-source resolution required: `{str(gate['original_source_resolution_required']).lower()}`",
        f"- Independent corroboration: `{gate['corroboration_required']}`",
        "- Promotion must record the exact playbook/eval/index/changelog changes or an explicit rejection reason.",
        "",
        "## Compiler decision",
        "",
        "- This deterministic artifact is a heuristic draft for semantic review, not a claim that source-specific methodology was extracted.",
        "- Use it as proposal input only after scope, original-source, corroboration, evidence, eval, and changelog gates are satisfied.",
    ]
    summary_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    return {
        "candidate_id": candidate_id,
        "title": title,
        "url": url,
        "effective_url": effective_url,
        "quality": quality,
        "classification": category,
        "vuln_class": vuln_class,
        "knowledge_types": knowledge_types,
        "promotion_gate": gate,
        "promotion_target": "vault_playbook",
        "safety_scope": scope,
        "source_id": rec.get("source_id") or "legacy-unbound",
        "summary_path": str(summary_path),
        "content_hash": rec.get("content_hash"),
        "key_sentences": key_sents[:3],
    }


def main() -> None:
    inbox = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else latest_inbox()
    jsonl = inbox / "learning-candidates.jsonl"
    if not jsonl.exists():
        raise SystemExit(f"Missing {jsonl}")
    records = [json.loads(l) for l in jsonl.read_text(encoding="utf-8").splitlines() if l.strip()]
    registry = load_registry(REGISTRY_PATH)
    eligible: list[dict] = []
    dispositions: list[dict] = []
    seen_urls: dict[str, str] = {}
    accepted_statuses = {"fetched_content", "browser_fetched_content"}
    for record in records:
        candidate_id = candidate_id_for_record(record)
        canonical = canonical_url(record.get("effective_url") or record.get("url") or "")
        base = {
            "candidate_id": candidate_id,
            "run_id": record.get("run_id"),
            "source_id": record.get("source_id"),
            "parent_source_id": record.get("parent_source_id"),
            "original_url": record.get("url"),
            "effective_url": record.get("effective_url") or record.get("url"),
            "retrieved_at": record.get("retrieved_at"),
            "content_sha256": record.get("content_hash"),
            "content_char_count": record.get("content_char_count"),
            "acquisition_lane": record.get("source_acquisition"),
            "discovered_from": record.get("discovered_from"),
            "registry_schema_version": record.get("registry_schema_version"),
            "registry_digest": record.get("registry_digest"),
            "promotion_policy": record.get("promotion_policy"),
            "review_status": "pending",
            "promotion_target": "vault_playbook",
        }
        if record.get("local_processing_status") not in accepted_statuses or record.get("content_quality") != "actual_content":
            dispositions.append({**base, "disposition": "discovery_context_or_not_fetched", "reason": record.get("local_processing_status") or record.get("content_quality")})
            continue
        if int(record.get("content_char_count") or 0) < MIN_COMPILE_CHARS:
            dispositions.append({**base, "disposition": "deferred_thin_content", "reason": f"below_{MIN_COMPILE_CHARS}_chars"})
            continue
        admitted, reasons = provenance_admission(record, expected_registry_digest=registry.digest)
        if not admitted and not ALLOW_LEGACY:
            dispositions.append({**base, "disposition": "quarantined_unbound_or_stale_provenance", "reason": ",".join(reasons)})
            continue
        safety = scope_disposition(" ".join([record.get("title") or "", record.get("content_excerpt") or record.get("short_excerpt_or_summary") or ""]))
        if safety == "scope_review_required":
            dispositions.append({**base, "disposition": "quarantined_scope_review", "reason": "explicit operational-abuse workflow terms require authorized-scope review"})
            continue
        if canonical in seen_urls:
            dispositions.append({**base, "disposition": "duplicate", "duplicate_of": seen_urls[canonical]})
            continue
        seen_urls[canonical] = candidate_id
        eligible.append(record)
        dispositions.append({**base, "disposition": "eligible_heuristic_draft"})

    actual = eligible[:MAX_RECORDS]
    compiled_ids = {candidate_id_for_record(record) for record in actual}
    for disposition in dispositions:
        if disposition["disposition"] == "eligible_heuristic_draft" and disposition["candidate_id"] not in compiled_ids:
            disposition["disposition"] = "deferred_compiler_cap"
            disposition["reason"] = f"ARGUS_COMPILER_MAX_RECORDS={MAX_RECORDS}"

    run_name = inbox.name
    summary_dir = SOURCE_SUMMARIES / run_name
    summary_dir.mkdir(parents=True, exist_ok=True)
    PATCH_PROPOSALS.mkdir(parents=True, exist_ok=True)
    REJECTED.mkdir(parents=True, exist_ok=True)
    (EVALS / "Learning Proposals").mkdir(parents=True, exist_ok=True)
    PROVENANCE_MANIFESTS.mkdir(parents=True, exist_ok=True)

    compiled = [compile_record(r, summary_dir) for r in actual]
    compiled_by_id = {item["candidate_id"]: item for item in compiled}
    for disposition in dispositions:
        if disposition["candidate_id"] in compiled_by_id:
            disposition["source_summary"] = compiled_by_id[disposition["candidate_id"]]["summary_path"]
            disposition["disposition"] = "draft_compiled_pending_review"
    provenance_path = PROVENANCE_MANIFESTS / f"{run_name}.jsonl"
    provenance_path.write_text(
        "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in dispositions),
        encoding="utf-8",
    )
    provenance_sha256 = hashlib.sha256(provenance_path.read_bytes()).hexdigest()
    skipped_counts = Counter(item["disposition"] for item in dispositions if item["disposition"] != "draft_compiled_pending_review")
    content_counts = Counter(r.get("content_quality") or "not_fetched" for r in records)

    proposal_path = PATCH_PROPOSALS / f"{run_name}-compiler-proposals.md"
    by_class = defaultdict(list)
    for c in compiled: by_class[c["vuln_class"]].append(c)
    lines = [
        f"# Learning Compiler Proposals — {run_name}", "",
        "## Compiler gate", "",
        f"- Input inbox: `{inbox}`",
        f"- Records total: `{len(records)}`",
        f"- Compiled actual-content records: `{len(compiled)}`",
        f"- Durable provenance manifest: `{provenance_path}` (`sha256:{provenance_sha256}`)",
        "- Generator kind: deterministic heuristic draft; semantic novelty and source-specific methodology are not asserted.",
        "- Gate: only current registry-bound `fetched_content`/`browser_fetched_content` records with `content_quality=actual_content` were compiled.",
        "- Every compiler output has `promotion_status=proposal_only`; no source role permits automatic promotion.",
        "- Discovery-index material requires resolution to the original source before promotion; categorical corroboration policy travels with each record.",
        "- Index/listing/topic pages were treated as discovery context only.", "",
        "## Content quality counts", "",
    ]
    for k, v in content_counts.most_common(): lines.append(f"- {k}: {v}")
    lines += ["", "## Proposed playbook updates", ""]
    for cls, items in sorted(by_class.items()):
        lines += [f"### {cls}", ""]
        for item in items:
            gate = item["promotion_gate"]
            lines.append(
                f"- `{item['candidate_id']}` — `{item['title']}` ({item['quality']}/10 display only): {item['url']} — "
                f"summary=`{item['summary_path']}`, source=`{item['source_id']}`, knowledge=`{','.join(item['knowledge_types']) or 'unclassified'}`, "
                f"original-source-required=`{str(gate['original_source_resolution_required']).lower()}`, "
                f"corroboration=`{gate['corroboration_required']}`, status=`{gate['promotion_status']}`"
            )
        lines += [
            "",
            "Reviewer action: extract a source-specific novel rule or reject/defer; complete the vault patch template, eval linkage, and changelog only after evidence gates pass.",
            "",
        ]
    proposal_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    rejected_path = REJECTED / f"{run_name}-discovery-only-and-skipped.md"
    rlines = [
        f"# Non-compiled learning dispositions — {run_name}",
        "",
        "This audit distinguishes discovery context, fetch failures, duplicates, provenance quarantine, safety-scope review, thin content, and compiler-cap deferrals. It is not a blanket rejection record.",
        "",
    ]
    for k, v in skipped_counts.most_common(): rlines.append(f"- {k}: {v}")
    rlines += ["", "## Index/listing examples", ""]
    for r in records:
        if r.get("content_quality") == "index_or_listing":
            rlines.append(f"- `{r.get('source_group')}` — {r.get('title')} — {r.get('url')}")
    rejected_path.write_text("\n".join(rlines) + "\n", encoding="utf-8")

    eval_path = EVALS / "Learning Proposals" / f"{run_name}-compiler-eval-proposals.md"
    eval_lines = [
        f"# Eval linkage candidates from learning compiler — {run_name}",
        "",
        "These are linkage placeholders, not generated behavioral claims or mature evals. A reviewer must identify a concrete source-specific rule before creating/updating an eval.",
        "",
    ]
    for candidate in compiled:
        eval_lines += [
            f"## {candidate['candidate_id']} — {candidate['title']}",
            "",
            f"- Source summary: `{candidate['summary_path']}`",
            f"- Heuristic class: `{candidate['vuln_class']}`",
            "- Required reviewer decision: `reject | defer | no-eval-needed | create-eval | update-eval`",
            "- Required linkage if promoted: playbook path, eval path/ID, review decision record, and changelog anchor.",
            "",
        ]
    eval_path.write_text("\n".join(eval_lines) + "\n", encoding="utf-8")

    run_report = inbox / "learning-compiler-run.md"
    run_report.write_text("\n".join([
        f"# Learning Compiler Run — {run_name}", "",
        f"- Input: `{jsonl}`",
        f"- Actual-content heuristic drafts compiled: `{len(compiled)}`",
        f"- Durable provenance/disposition manifest: `{provenance_path}`",
        f"- Provenance manifest SHA-256: `{provenance_sha256}`",
        f"- Source summaries: `{summary_dir}`",
        f"- Skill patch proposals: `{proposal_path}`",
        f"- Discovery/skipped audit: `{rejected_path}`",
        f"- Eval proposals: `{eval_path}`",
        "", "## Compiled sources", "",
        *[f"- {c['vuln_class']} — {c['title']} — `{c['summary_path']}`" for c in compiled],
    ]) + "\n", encoding="utf-8")

    print(json.dumps({
        "inbox": str(inbox),
        "records": len(records),
        "compiled": len(compiled),
        "summary_dir": str(summary_dir),
        "proposal_path": str(proposal_path),
        "rejected_path": str(rejected_path),
        "eval_path": str(eval_path),
        "run_report": str(run_report),
        "provenance_manifest": str(provenance_path),
        "provenance_manifest_sha256": provenance_sha256,
        "disposition_counts": dict(Counter(item["disposition"] for item in dispositions)),
        "content_counts": dict(content_counts),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
