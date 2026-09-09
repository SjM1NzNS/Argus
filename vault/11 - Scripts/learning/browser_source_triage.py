#!/usr/bin/env python3
"""One-context-per-source Playwright triage for the learning registry."""
from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from browser_runtime import (
    BrowserEvidenceRecorder,
    PublicURLPolicy,
    bounded_page_metrics,
    browser_launch_options,
    configure_playwright_node,
    controlled_error,
    create_isolated_page,
    extract_bounded_page,
    sanitize_url_for_evidence,
    wait_for_meaningful_page,
)
from learning_registry import load_registry
from learning_state import canonical_url

CONFIG = Path(
    sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / ".config/argus/learning-sources.yaml")
).expanduser()
OUT_DIR = Path(
    sys.argv[2]
    if len(sys.argv) > 2
    else str(Path.home() / "SecurityResearch/01 - Learning/Source Triage/browser-all-sources-")
    + datetime.now().strftime("%Y%m%d-%H%M%S")
).expanduser()
OUT_DIR.mkdir(parents=True, exist_ok=True)
os.chmod(OUT_DIR, 0o700)
PAGE_TIMEOUT_MS = int(float(os.environ.get("ARGUS_BROWSER_PAGE_TIMEOUT", "18")) * 1000)
MAX_SOURCES = int(os.environ.get("ARGUS_TRIAGE_MAX_SOURCES", "-1"))

SOURCE_FILTER = {
    value.strip()
    for value in os.environ.get("ARGUS_SOURCE_FILTER", "").split(",")
    if value.strip()
}
MAX_TOTAL_SECONDS = int(os.environ.get("ARGUS_BROWSER_MAX_TOTAL_SECONDS", "1800"))
MAX_BODY_TEXT_CHARS = int(os.environ.get("ARGUS_BROWSER_MAX_BODY_TEXT_CHARS", "200000"))
MAX_DOM_LINKS = int(os.environ.get("ARGUS_BROWSER_MAX_DOM_LINKS", "2000"))
PER_PAGE_BUDGET_SECONDS = max(5, int(PAGE_TIMEOUT_MS / 1000) + 12)
START_TIME = time.monotonic()
LEARNING_PAT = re.compile(
    r"(report|reports|issue|issues|blog|research|post|article|advis|cve|ghsa|vulnerab|security|audit|writeup|incident|hack|exploit|web-security|docs|guide|learn|taxonomy|prompt|llm|agent|solidity|scsvs|wstg|asvs|cheatsheet|competition|bounty|finding)",
    re.I,
)
NOISE_PAT = re.compile(
    r"(login|signup|sign_in|register|privacy|terms|contact|status|support|press|leaderboard|careers|pricing|product|enterprise|download|cookie|twitter|linkedin|discord|youtube|mailto:)",
    re.I,
)


def classify_link(href: str, text: str, base_host: str) -> str:
    value = (href or "").strip()
    if not value.startswith("http"):
        return "skip"
    same_site = urlparse(value).netloc.lower() == base_host.lower()
    blob = f"{value} {text or ''}"
    if NOISE_PAT.search(blob):
        return "noise"
    if LEARNING_PAT.search(blob):
        return "candidate_same_site" if same_site else "candidate_external"
    return "same_site" if same_site else "external"


def decision_for(row: dict) -> str:
    if row.get("error"):
        return "manual_review_or_drop"
    candidates = row["candidate_same_site"] + row["candidate_external"]
    if row["text_len"] < 300 and candidates < 3:
        return "manual_review_or_drop"
    if candidates >= 8:
        if row.get("configured_handling") == "browser_dom_required" or row["static_likely_dynamic"]:
            return "browser_dom_required"
        return "static_deep_link_ok"
    if candidates >= 3:
        return "keep_with_filtering"
    if row["text_len"] >= 2500 and row["same_site"] >= 5:
        return "single_page_or_index_keep"
    return "low_yield_review"


def _base_row(source: dict, browser_version: str) -> dict:
    return {
        "id": source["id"],
        "group": source.get("group"),
        "name": source.get("name"),
        "url": sanitize_url_for_evidence(source["url"]),
        "type": source.get("type", ""),
        "priority": source.get("priority", ""),
        "cadence": source.get("cadence", ""),
        "configured_handling": source.get("handling", ""),
        "title": "",
        "final_url": "",
        "text_len": 0,
        "links_total": 0,
        "candidate_same_site": 0,
        "candidate_external": 0,
        "same_site": 0,
        "external": 0,
        "noise": 0,
        "sample_candidates": [],
        "resource_hints": [],
        "source_artifacts": [],
        "blocked_requests": [],
        "browser_version": browser_version,
        "browser_context_isolated": False,
        "browser_evidence_manifest": f"browser-evidence/{source['id']}/manifest.json",
        "error": "",
        "error_stage": "",
        "static_likely_dynamic": False,
    }


async def scan(browser, source: dict, browser_version: str) -> dict:
    row = _base_row(source, browser_version)
    recorder = BrowserEvidenceRecorder(
        source_id=source["id"],
        output_root=OUT_DIR / "browser-evidence",
        max_events=int(os.environ.get("ARGUS_BROWSER_MAX_NETWORK_EVENTS", "2000")),
        browser_version=browser_version,
    )
    policy = PublicURLPolicy(resolve_public=False)
    context = None
    try:
        if time.monotonic() - START_TIME >= MAX_TOTAL_SECONDS:
            raise TimeoutError(f"browser triage total budget exceeded ({MAX_TOTAL_SECONDS}s)")
        allowed, reason = policy.check(source["url"])
        if not allowed:
            raise ValueError(f"browser navigation rejected URL ({reason})")
        context, page = await create_isolated_page(
            browser,
            user_agent="ArgusLearningBrowserTriage/2.0 (+isolated low-rate source triage)",
            policy=policy,
            recorder=recorder,
        )
        recorder.begin_navigation("root", source["url"])
        async with asyncio.timeout(PER_PAGE_BUDGET_SECONDS):
            response = await page.goto(
                source["url"],
                wait_until="domcontentloaded",
                timeout=PAGE_TIMEOUT_MS,
            )
            row["wait_state"] = await wait_for_meaningful_page(
                page,
                timeout_ms=PAGE_TIMEOUT_MS,
                minimum_text_chars=200,
            )
            final_url = page.url
            final_allowed, final_reason = policy.check(final_url)
            if not final_allowed:
                raise ValueError(f"browser redirect rejected URL ({final_reason})")
            data = await extract_bounded_page(
                page,
                text_limit=MAX_BODY_TEXT_CHARS,
                link_limit=MAX_DOM_LINKS,
                script_limit=200,
                resource_limit=2000,
                frame_limit=50,
            )
        metrics = bounded_page_metrics(data)
        row["title"] = data.get("title") or ""
        row["title_len_lower_bound"] = metrics["title_total_chars_lower_bound"]
        row["final_url"] = sanitize_url_for_evidence(final_url)
        row["http_status"] = response.status if response is not None else None
        row["text_len"] = metrics["text_total_chars_lower_bound"]
        row["text_len_lower_bound"] = metrics["text_total_chars_lower_bound"]
        row["links_total_lower_bound"] = metrics["totals_lower_bound"].get(
            "links", len(data.get("links") or [])
        )
        row["links_total"] = row["links_total_lower_bound"]
        row["dom_truncation"] = data.get("truncation") or {}
        row["dom_totals_lower_bound"] = metrics["totals_lower_bound"]
        row["dom_total_semantics"] = metrics["total_semantics"]
        base_host = urlparse(final_url).netloc.lower()
        seen: set[str] = set()
        for link in data.get("links") or []:
            raw_href = str(link.get("href") or "")
            raw_identity = canonical_url(raw_href)
            safe_href = sanitize_url_for_evidence(raw_href)
            if not raw_href or raw_identity in seen:
                continue
            seen.add(raw_identity)
            classification = classify_link(raw_href, str(link.get("text") or ""), base_host)
            if classification == "skip":
                continue
            row[classification] = row.get(classification, 0) + 1
            if classification.startswith("candidate") and len(row["sample_candidates"]) < 12:
                row["sample_candidates"].append(
                    {
                        "text": str(link.get("text") or "")[:220],
                        "href": safe_href,
                        "class": classification,
                    }
                )
        resources = []
        for item in data.get("resources") or []:
            safe_url = sanitize_url_for_evidence(str(item.get("name") or ""))
            if safe_url == "<REDACTED_INVALID_URL>":
                continue
            if re.search(r"graphql|api|_rsc|json|issues|reports|competitions|hacktivity|solodit|wp-json|feed|rss|\.js(?:\?|$)|\.map(?:\?|$)", safe_url, re.I):
                resources.append({"url": safe_url, "kind": str(item.get("initiatorType") or "other")[:40]})
        row["resource_hints"] = resources[:100]
        row["static_likely_dynamic"] = bool(row["resource_hints"]) or any(
            value in final_url
            for value in ["hackerone.com", "solodit.cyfrin.io", "cantina.xyz"]
        )
    except Exception as error:
        row.update(controlled_error(error, stage="source_scan"))
        row["error"] = row["error_code"]
    finally:
        cleanup_error = None
        if context is not None:
            try:
                await context.close()
            except Exception as error:
                cleanup_error = error
        if cleanup_error is not None:
            cleanup_fields = controlled_error(cleanup_error, stage="context_close")
            row["context_close_error"] = cleanup_fields["error_code"]
            if not row.get("error"):
                row.update(cleanup_fields)
                row["error"] = cleanup_fields["error_code"]
        manifest = recorder.write(
            failure_stage=row.get("error_stage") or None,
            error_code=row.get("error_code") or None,
        )
        row["browser_context_isolated"] = bool(manifest["context_isolated"])
        row["browser_context_guard_ready"] = bool(manifest["context_guard_ready"])
        row["source_artifacts"] = manifest["artifact_urls"]
        row["resource_hints"] = manifest["artifact_urls"]
        row["static_likely_dynamic"] = bool(row["resource_hints"]) or any(
            value in row.get("final_url", "")
            for value in ["hackerone.com", "solodit.cyfrin.io", "cantina.xyz"]
        )
        row["blocked_requests"] = manifest["blocked_requests"]
        row["blocked_request_total"] = manifest["blocked_request_total"]
        row["blocked_request_recorded"] = manifest["blocked_request_recorded"]
        row["dropped_blocked_request_count"] = manifest["dropped_blocked_request_count"]
        row["network_event_count"] = manifest["event_count"]
        row["network_event_bytes"] = manifest["event_bytes"]
        row["truncated_network_event_count"] = manifest["truncated_event_count"]
        row["dropped_network_event_count"] = manifest["dropped_event_count"]
        row["dropped_network_event_bytes"] = manifest["dropped_event_byte_count"]
        row["telemetry_callback_errors"] = manifest["telemetry_callback_errors"]
        row["network_sha256"] = manifest["network_sha256"]
    row["decision"] = decision_for(row)
    return row


async def _run_pipeline() -> int:
    registry = load_registry(CONFIG)
    sources = [dict(source) for source in registry.sources]
    if SOURCE_FILTER:
        unknown = SOURCE_FILTER - {source["id"] for source in sources}
        if unknown:
            raise SystemExit(f"Unknown source IDs: {', '.join(sorted(unknown))}")
        sources = [source for source in sources if source["id"] in SOURCE_FILTER]
    if MAX_SOURCES >= 0:
        sources = sources[:MAX_SOURCES]

    rows: list[dict] = []
    browser_version = "not_started"
    browser_started = False
    playwright = None
    browser = None
    try:
        if sources:
            configure_playwright_node()
            from playwright.async_api import async_playwright

            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(**browser_launch_options())
            browser_version = browser.version
            browser_started = True
        for index, source in enumerate(sources, 1):
            print(f"[{index}/{len(sources)}] {source.get('name')}", flush=True)
            rows.append(await scan(browser, source, browser_version))
    except Exception as error:
        observed = {row["id"] for row in rows}
        for source in sources:
            if source["id"] in observed:
                continue
            row = _base_row(source, browser_version)
            row.update(controlled_error(error, stage="browser_startup"))
            row["error"] = row["error_code"]
            recorder = BrowserEvidenceRecorder(
                source_id=source["id"],
                output_root=OUT_DIR / "browser-evidence",
                max_events=int(os.environ.get("ARGUS_BROWSER_MAX_NETWORK_EVENTS", "2000")),
                browser_version=browser_version,
            )
            manifest = recorder.write(
                failure_stage=row["error_stage"],
                error_code=row["error_code"],
            )
            row["source_artifacts"] = manifest["artifact_urls"]
            row["browser_context_isolated"] = bool(manifest["context_isolated"])
            row["browser_context_guard_ready"] = bool(manifest["context_guard_ready"])
            row["blocked_requests"] = manifest["blocked_requests"]
            row["blocked_request_total"] = manifest["blocked_request_total"]
            row["blocked_request_recorded"] = manifest["blocked_request_recorded"]
            row["dropped_blocked_request_count"] = manifest["dropped_blocked_request_count"]
            row["network_event_count"] = manifest["event_count"]
            row["network_event_bytes"] = manifest["event_bytes"]
            row["truncated_network_event_count"] = manifest["truncated_event_count"]
            row["dropped_network_event_count"] = manifest["dropped_event_count"]
            row["dropped_network_event_bytes"] = manifest["dropped_event_byte_count"]
            row["telemetry_callback_errors"] = manifest["telemetry_callback_errors"]
            row["network_sha256"] = manifest["network_sha256"]
            row["decision"] = decision_for(row)
            rows.append(row)
    finally:
        if browser is not None:
            await browser.close()
        if playwright is not None:
            await playwright.stop()

    json_path = OUT_DIR / "browser-source-triage.json"
    json_path.write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    os.chmod(json_path, 0o600)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["decision"]] = counts.get(row["decision"], 0) + 1
    contexts_created = sum(bool(row.get("browser_context_isolated")) for row in rows)
    context_guards_ready = sum(bool(row.get("browser_context_guard_ready")) for row in rows)
    successful_rows = sum(not bool(row.get("error")) for row in rows)
    failed_rows = len(rows) - successful_rows
    network_events = sum(int(row.get("network_event_count") or 0) for row in rows)
    network_bytes = sum(int(row.get("network_event_bytes") or 0) for row in rows)
    truncated_events = sum(int(row.get("truncated_network_event_count") or 0) for row in rows)
    dropped_events = sum(int(row.get("dropped_network_event_count") or 0) for row in rows)
    dropped_event_bytes = sum(int(row.get("dropped_network_event_bytes") or 0) for row in rows)
    blocked_total = sum(int(row.get("blocked_request_total") or 0) for row in rows)
    blocked_recorded = sum(int(row.get("blocked_request_recorded") or 0) for row in rows)
    blocked_dropped = sum(int(row.get("dropped_blocked_request_count") or 0) for row in rows)
    telemetry_errors = sum(int(row.get("telemetry_callback_errors") or 0) for row in rows)
    startup_state = "not_started" if not sources else ("started" if browser_started else "failed")
    lines = [
        "# Browser-rendered triage of learning sources",
        "",
        f"- Generated: {datetime.now(timezone.utc).isoformat()}",
        f"- Config: `{CONFIG}`",
        f"- Browser: Playwright Chromium `{browser_version}`",
        f"- Browser startup observed: {startup_state}",
        f"- Isolated contexts created/selected: {contexts_created}/{len(sources)}",
        f"- Context guards ready/selected: {context_guards_ready}/{len(sources)}",
        f"- Source scans succeeded/failed: {successful_rows}/{failed_rows}",
        "- Configured request policy: public HTTP(S), no credentials, strict global-unicast proxy validation",
        "- Configured WebSocket policy: disabled",
        f"- Network evidence: {network_events} retained events / {network_bytes} bytes; {truncated_events} truncated attempts; {dropped_events} dropped events / {dropped_event_bytes} bytes",
        f"- Observed blocked requests: {blocked_total} total; {blocked_recorded} retained; {blocked_dropped} dropped",
        f"- Observed telemetry callback errors: {telemetry_errors}",
        "- Evidence policy: bounded and value-redacted; exercised only where a context was created",
        f"- Sources scanned: {len(rows)}",
        "",
        "## Decision counts",
        "",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- {key}: {value}")
    lines += [
        "",
        "## Source decisions",
        "",
        "| Source | Group | Decision | Candidate links | Text chars (lower bound when truncated) | Artifacts | Notes |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        candidate_count = row["candidate_same_site"] + row["candidate_external"]
        notes = []
        if row.get("configured_handling"):
            notes.append(f"handling={row['configured_handling']}")
        if row.get("error"):
            notes.append(row["error"].replace("|", "/")[:90])
        if row.get("static_likely_dynamic"):
            notes.append("dynamic/browser hints")
        lines.append(
            f"| {row['name']} | {row['group']} | {row['decision']} | {candidate_count} | "
            f"{row['text_len']} | {len(row['source_artifacts'])} | {'; '.join(notes)} |"
        )
    lines += ["", "## Sample candidate links", ""]
    for row in rows:
        if not row["sample_candidates"]:
            continue
        lines += [f"### {row['name']}", ""]
        for candidate in row["sample_candidates"][:8]:
            text = (candidate["text"] or candidate["href"]).replace("[", "(").replace("]", ")")
            lines.append(f"- `{candidate['class']}` [{text}]({candidate['href']})")
        lines.append("")
    report_path = OUT_DIR / "browser-source-triage.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    os.chmod(report_path, 0o600)
    print(
        json.dumps(
            {
                "out_dir": str(OUT_DIR),
                "json": str(json_path),
                "report": str(report_path),
                "browser_version": browser_version,
                "browser_startup_observed": startup_state,
                "contexts_created": contexts_created,
                "context_guards_ready": context_guards_ready,
                "sources_succeeded": successful_rows,
                "sources_failed": failed_rows,
                "network_event_count": network_events,
                "network_event_bytes": network_bytes,
                "truncated_network_event_count": truncated_events,
                "dropped_network_event_count": dropped_events,
                "dropped_network_event_bytes": dropped_event_bytes,
                "blocked_request_total": blocked_total,
                "blocked_request_recorded": blocked_recorded,
                "dropped_blocked_request_count": blocked_dropped,
                "telemetry_callback_errors": telemetry_errors,
                "decision_counts": counts,
            },
            indent=2,
            sort_keys=True,
        )
    )
    failures = [row for row in rows if row.get("error")]
    successes = [row for row in rows if not row.get("error")]
    return 2 if failures or (sources and not successes) else 0


async def async_main() -> int:
    try:
        async with asyncio.timeout(MAX_TOTAL_SECONDS):
            return await _run_pipeline()
    except TimeoutError as error:
        failure = controlled_error(error, stage="run_budget")
        failure_path = OUT_DIR / "run-failure.json"
        failure_path.write_text(json.dumps(failure, sort_keys=True) + "\n", encoding="utf-8")
        os.chmod(failure_path, 0o600)
        return 124


def main() -> None:
    raise SystemExit(asyncio.run(async_main()))


if __name__ == "__main__":
    main()
