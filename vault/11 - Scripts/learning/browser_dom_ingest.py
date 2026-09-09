#!/usr/bin/env python3
from __future__ import annotations

import asyncio
import hashlib
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
    is_tracker_url,
    sanitize_url_for_evidence,
    wait_for_meaningful_page,
)
from learning_registry import load_registry, provenance_fields, select_sources
from learning_state import canonical_url, merge_json_state, migrate_seen_url_state, url_identity

CONFIG = Path(
    sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / ".config/argus/learning-sources.yaml")
).expanduser()
RUN_DIR = Path(
    sys.argv[2]
    if len(sys.argv) > 2
    else str(Path.home() / "SecurityResearch/01 - Learning/Inbox/browser-dom-")
    + datetime.now().strftime("%Y%m%d-%H%M%S")
).expanduser()
RUN_DIR.mkdir(parents=True, exist_ok=True)
os.chmod(RUN_DIR, 0o700)
MAX_SOURCES = int(os.environ.get("ARGUS_BROWSER_MAX_SOURCES", "20"))
MAX_LINKS_PER_SOURCE = int(os.environ.get("ARGUS_BROWSER_MAX_LINKS_PER_SOURCE", "8"))
MIN_CONTENT_CHARS = int(os.environ.get("ARGUS_MIN_CONTENT_CHARS", "1200"))
PAGE_TIMEOUT_MS = int(float(os.environ.get("ARGUS_BROWSER_PAGE_TIMEOUT", "18")) * 1000)
MAX_TOTAL_SECONDS = int(os.environ.get("ARGUS_BROWSER_MAX_TOTAL_SECONDS", "1800"))
MAX_NETWORK_EVENTS = int(os.environ.get("ARGUS_BROWSER_MAX_NETWORK_EVENTS", "2000"))
MAX_BODY_TEXT_CHARS = int(os.environ.get("ARGUS_BROWSER_MAX_BODY_TEXT_CHARS", "200000"))
MAX_DOM_LINKS = int(os.environ.get("ARGUS_BROWSER_MAX_DOM_LINKS", "2000"))
PER_PAGE_BUDGET_SECONDS = max(5, int(PAGE_TIMEOUT_MS / 1000) + 12)
START_TIME = time.monotonic()
SEEN_STATE_PATH = Path(
    os.environ.get(
        "ARGUS_LEARNING_SEEN_STATE",
        str(Path.home() / ".config/argus/learning-seen-urls.json"),
    )
).expanduser()
TRACK_SEEN_STATE = os.environ.get("ARGUS_TRACK_SEEN_STATE", "1").lower() not in {
    "0",
    "false",
    "no",
}
RUN_CADENCE = os.environ.get("ARGUS_LEARNING_CADENCE", "legacy").strip().lower()
PROVENANCE_RUN_ID = os.environ.get("ARGUS_PROVENANCE_RUN_ID", "").strip() or RUN_DIR.name
BACKFILL_REASON = os.environ.get("ARGUS_BACKFILL_REASON", "").strip()
SOURCE_FILTER = {
    value.strip()
    for value in os.environ.get("ARGUS_SOURCE_FILTER", "").split(",")
    if value.strip()
}
REGISTRY = load_registry(CONFIG)

LEARNING_PAT = re.compile(
    r"(report|reports|issue|issues|blog|research|post|article|advis|cve|ghsa|vulnerab|security|audit|writeup|incident|hack|exploit|web-security|docs|guide|learn|taxonomy|prompt|llm|agent|solidity|scsvs|wstg|asvs|cheatsheet|competition|bounty|finding|root-cause|rounding|oracle|bridge|access-control|idor|xss|csrf|ssrf|graphql)",
    re.I,
)
NOISE_PAT = re.compile(
    r"(login|signup|sign_in|register|privacy|terms|contact|status|support|press|leaderboard|careers|pricing|product|enterprise|download|cookie|twitter|linkedin|discord|youtube|mailto:|/features/|/security/advanced-security|/pulls|/actions|/issues$|/activity|/custom-properties|customers|compliance|fellowship|predictions|vasp|buy-vs-build|regulatory|architecture|partners-with|crime-report)",
    re.I,
)
INDEX_WORDS = re.compile(
    r"(all topics|all writing|opportunities|reports|research|blog|resources|home|index|leaderboard)",
    re.I,
)


def load_sources(_: Path) -> list[dict]:
    if RUN_CADENCE == "legacy" and not SOURCE_FILTER:
        return [dict(source) for source in REGISTRY.sources if source["acquisition"] == "browser_dom"]
    selection_cadence = "all" if SOURCE_FILTER and RUN_CADENCE in {"legacy", "backfill"} else RUN_CADENCE
    return select_sources(
        REGISTRY,
        cadence=selection_cadence,
        lane="browser_dom",
        source_ids=SOURCE_FILTER or None,
    )


def load_seen() -> dict:
    if not TRACK_SEEN_STATE:
        return {"urls": {}}
    return migrate_seen_url_state(
        SEEN_STATE_PATH,
        warn=lambda message: print(message, file=sys.stderr),
    )


def save_seen(state: dict) -> None:
    if not TRACK_SEEN_STATE:
        return
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    merge_json_state(
        SEEN_STATE_PATH,
        state,
        default={"urls": {}},
        warn=lambda message: print(message, file=sys.stderr),
    )


def seen_is_fresh(entry: dict, source: dict) -> bool:
    try:
        last = datetime.fromisoformat(
            (entry.get("last_seen") or entry.get("first_seen") or "").replace("Z", "+00:00")
        )
        age_days = (datetime.now(timezone.utc) - last).total_seconds() / 86400.0
    except Exception:
        return False
    return age_days < int(source.get("refetch_interval_days", 30))


def source_provenance(source: dict, record_kind: str) -> dict:
    values = provenance_fields(
        REGISTRY,
        source,
        run_cadence=RUN_CADENCE,
        record_kind=record_kind,
        run_id=PROVENANCE_RUN_ID,
    )
    if record_kind != "root":
        values["parent_source_id"] = source["id"]
    if BACKFILL_REASON:
        values["backfill_reason"] = BACKFILL_REASON
    return values


def source_noise(href: str, text: str, source_name: str) -> bool:
    parsed = urlparse(href)
    path = parsed.path.lower()
    host = parsed.netloc.lower()
    blob = (href + " " + (text or "")).lower()
    if path in {"", "/"}:
        return True
    if "immunefi.com" in host and any(
        value in path for value in ["/blog/customers", "/customers", "/bug-bounty/"]
    ):
        return True
    if "immunefi.com" in host and path.rstrip("/") in {"/blog/research", "/blog"}:
        return True
    if "blocksec.com" in host and any(
        value in blob
        for value in [
            "compliance",
            "vasp",
            "buy vs. build",
            "buy-vs-build",
            "partners with",
            "crime report",
            "regulatory",
        ]
    ):
        return True
    if "paradigm.xyz" in host and any(value in path for value in ["/fellowship", "/predictions"]):
        return True
    if "audits.sherlock.xyz" in host and path.rstrip("/") in {
        "",
        "/",
        "/contests",
        "/bug-bounties",
        "/connect",
    }:
        return True
    if "cantina.xyz" in host and path.rstrip("/") in {"/opportunities/ended", "/competitions"}:
        return True
    if "chainsecurity.com" in host and any(
        value in blob for value in ["audit completed", "compliance", "customer"]
    ):
        return True
    return False


def score_link(href: str, text: str, base_host: str, source_name: str) -> int:
    if (
        not href.startswith("http")
        or NOISE_PAT.search(href + " " + (text or ""))
        or source_noise(href, text, source_name)
    ):
        return -999
    parsed = urlparse(href)
    path = parsed.path.lower()
    host = parsed.netloc.lower()
    blob = href + " " + (text or "")
    score = 0
    if host == base_host:
        score += 20
    if LEARNING_PAT.search(blob):
        score += 35
    if re.search(r"/20\d{2}/", path) or re.search(r"20\d{2}", path):
        score += 20
    if "hackerone.com" in host and re.search(r"/reports/\d+", path):
        score += 80
    if "solodit.cyfrin.io" in host and "/issues/" in path:
        score += 80
    if "cantina.xyz" in host and "/competitions/" in path:
        score += 60
    if "audits.sherlock.xyz" in host and "/contests/" in path:
        score += 60
    if "code4rena.com" in host and "/reports/" in path:
        score += 70
    if "blocksec.com" in host and "/blog/" in path:
        score += 50
    if "immunefi.com" in host and "/blog/research/" in path:
        score += 65
    if "chainsecurity.com" in host and "/blog/" in path:
        score += 50
    if "paradigm.xyz" in host and re.search(r"/20\d{2}/", path):
        score += 45
    if "github.com" in host and any(value in path for value in ["/issues", "/pulls", "/actions", "/activity"]):
        score -= 120
    return score


def classify_content(_: str, title: str, text: str, links_count: int) -> str:
    if len(text or "") >= MIN_CONTENT_CHARS and not (
        links_count > 50 and INDEX_WORDS.search(title or "")
    ):
        return "actual_content"
    if links_count > 20 or INDEX_WORDS.search(title or ""):
        return "index_or_listing"
    if len(text or "") >= 400:
        return "thin_content"
    return "metadata_only"


def _safe_resource_list(resources: list[dict], limit: int = 200) -> list[dict[str, str]]:
    values: dict[tuple[str, str], dict[str, str]] = {}
    for resource in resources or []:
        url = sanitize_url_for_evidence(str(resource.get("name") or ""))
        if url == "<REDACTED_INVALID_URL>" or is_tracker_url(url):
            continue
        kind = str(resource.get("initiatorType") or "other")[:40]
        values[(kind, url)] = {"kind": kind, "url": url}
    return [values[key] for key in sorted(values)[:limit]]


async def navigate_extract(
    page,
    url: str,
    *,
    policy: PublicURLPolicy,
    recorder: BrowserEvidenceRecorder,
    navigation_id: str,
) -> dict:
    allowed, reason = policy.check(url)
    if not allowed:
        raise ValueError(f"browser navigation rejected URL ({reason})")
    if time.monotonic() - START_TIME >= MAX_TOTAL_SECONDS:
        raise TimeoutError(f"browser ingest total budget exceeded ({MAX_TOTAL_SECONDS}s)")
    recorder.begin_navigation(navigation_id, url)
    started = time.monotonic()
    async with asyncio.timeout(PER_PAGE_BUDGET_SECONDS):
        response = await page.goto(url, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT_MS)
        wait_state = await wait_for_meaningful_page(
            page,
            timeout_ms=PAGE_TIMEOUT_MS,
            minimum_text_chars=min(200, MIN_CONTENT_CHARS),
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
    redirect_chain: list[str] = []
    if response is not None:
        request = response.request
        while request is not None:
            redirect_chain.append(sanitize_url_for_evidence(request.url))
            request = request.redirected_from
        redirect_chain.reverse()
    data["url"] = final_url
    data["safe_url"] = sanitize_url_for_evidence(final_url)
    data["scripts"] = [
        {
            "url": sanitize_url_for_evidence(str(item.get("src") or "")),
            "type": str(item.get("type") or "")[:80],
            "integrity_present": bool(item.get("integrity")),
        }
        for item in data.get("scripts") or []
        if sanitize_url_for_evidence(str(item.get("src") or "")) != "<REDACTED_INVALID_URL>"
        and not is_tracker_url(str(item.get("src") or ""))
    ][:200]
    data["frames"] = [
        sanitize_url_for_evidence(str(value))
        for value in data.get("frames") or []
        if sanitize_url_for_evidence(str(value)) != "<REDACTED_INVALID_URL>"
    ][:50]
    data["resources"] = _safe_resource_list(data.get("resources") or [])
    data["wait_state"] = wait_state
    data["redirect_chain"] = redirect_chain
    data["http_status"] = response.status if response is not None else None
    data["navigation_duration_ms"] = round((time.monotonic() - started) * 1000)
    return data


def _browser_fields(source_id: str, browser_version: str, manifest: dict | None = None) -> dict:
    fields = {
        "browser_engine": "playwright-chromium",
        "browser_version": browser_version,
        "browser_context_isolated": bool(manifest and manifest.get("context_isolated")),
        "browser_context_guard_ready": bool(manifest and manifest.get("context_guard_ready")),
    }
    if manifest is not None:
        fields["browser_evidence_manifest"] = f"browser-evidence/{source_id}/manifest.json"
        fields["browser_network_sha256"] = manifest["network_sha256"]
        fields["browser_network_event_count"] = manifest["event_count"]
        fields["browser_network_event_bytes"] = manifest["event_bytes"]
        fields["browser_truncated_event_count"] = manifest["truncated_event_count"]
        fields["browser_dropped_event_count"] = manifest["dropped_event_count"]
        fields["browser_dropped_event_byte_count"] = manifest["dropped_event_byte_count"]
        fields["browser_telemetry_callback_errors"] = manifest["telemetry_callback_errors"]
        fields["browser_blocked_request_total"] = manifest["blocked_request_total"]
        fields["browser_blocked_request_recorded"] = manifest["blocked_request_recorded"]
        fields["browser_dropped_blocked_request_count"] = manifest["dropped_blocked_request_count"]
        fields["source_artifact_count"] = len(manifest["artifact_urls"])
    return fields


def _page_record_fields(page_data: dict) -> dict:
    text = page_data.get("text") or ""
    metrics = bounded_page_metrics(page_data)
    return {
        "effective_url": page_data.get("safe_url"),
        "http_status": page_data.get("http_status"),
        "navigation_duration_ms": page_data.get("navigation_duration_ms"),
        "navigation_wait_state": page_data.get("wait_state"),
        "redirect_chain": page_data.get("redirect_chain") or [],
        "script_resources": page_data.get("scripts") or [],
        "frame_resources": page_data.get("frames") or [],
        "resource_inventory": page_data.get("resources") or [],
        "dom_truncation": page_data.get("truncation") or {},
        "dom_totals_lower_bound": metrics["totals_lower_bound"],
        "dom_total_semantics": metrics["total_semantics"],
        "content_total_char_count_lower_bound": metrics["text_total_chars_lower_bound"],
        "title_total_char_count_lower_bound": metrics["title_total_chars_lower_bound"],
        "content_char_count": metrics["captured_text_chars"],
        "content_hash": hashlib.sha256(text.encode()).hexdigest(),
        "content_excerpt": text[:6000],
        "short_excerpt_or_summary": " ".join(text.split())[:900],
    }


def _failure_record(source: dict, record_kind: str, url: str, error: Exception, **extra) -> dict:
    stage = str(extra.pop("failure_stage", "root_navigation" if record_kind == "root" else "linked_navigation"))
    safe_error = controlled_error(error, stage=stage)
    return {
        **source_provenance(source, record_kind),
        "url": sanitize_url_for_evidence(url),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "local_processing_status": "manual_review_required" if record_kind != "root" else "browser_failed",
        "content_quality": "not_fetched",
        "fetch_error": safe_error["error_code"],
        **safe_error,
        "source_group": source.get("group"),
        "source_name": source.get("name"),
        **extra,
    }


async def process_source(browser, source: dict, seen: dict, browser_version: str) -> tuple[list[dict], int]:
    records: list[dict] = []
    seen_updates = 0
    policy = PublicURLPolicy(resolve_public=False)
    recorder = BrowserEvidenceRecorder(
        source_id=source["id"],
        output_root=RUN_DIR / "browser-evidence",
        max_events=MAX_NETWORK_EVENTS,
        browser_version=browser_version,
    )
    context = None
    try:
        context, page = await create_isolated_page(
            browser,
            user_agent="ArgusLearningBrowser/2.0 (+isolated low-rate source acquisition)",
            policy=policy,
            recorder=recorder,
        )
        root = await navigate_extract(
            page,
            source["url"],
            policy=policy,
            recorder=recorder,
            navigation_id="root",
        )
        base_host = urlparse(root.get("url") or source["url"]).netloc.lower()
        root_quality = "index_or_listing"
        records.append(
            {
                **source_provenance(source, "root"),
                "url": sanitize_url_for_evidence(source["url"]),
                "title": root.get("title") or source.get("name"),
                "source_name": source.get("name"),
                "source_group": source.get("group"),
                "source_type": source.get("type"),
                "priority": source.get("priority"),
                "handling": source.get("handling"),
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "local_processing_status": "browser_fetched_index",
                "content_quality": root_quality,
                "page_kind": root_quality,
                **_browser_fields(source["id"], browser_version),
                **_page_record_fields(root),
            }
        )
        candidates: list[tuple[int, str, str]] = []
        seen_links: set[str] = set()
        for link in root.get("links") or []:
            raw_href = str(link.get("href") or "")
            href = canonical_url(raw_href)
            if not href or href in seen_links:
                continue
            seen_links.add(href)
            score = score_link(href, str(link.get("text") or ""), base_host, source.get("name", ""))
            if score > 0:
                candidates.append((score, raw_href, str(link.get("text") or "")))
        source_link_limit = min(
            MAX_LINKS_PER_SOURCE,
            int(source.get("deep_link_limit", MAX_LINKS_PER_SOURCE)),
        )
        candidates = sorted(candidates, key=lambda item: (-item[0], canonical_url(item[1])))[:source_link_limit]
        for sequence, (score, href, label) in enumerate(candidates, 1):
            safe_href = sanitize_url_for_evidence(href)
            raw_key = canonical_url(href)
            key = url_identity(raw_key)
            seen_entry = seen.get("urls", {}).get(key)
            if seen_entry and seen_is_fresh(seen_entry, source):
                records.append(
                    {
                        **source_provenance(source, "discovered_content"),
                        "url": safe_href,
                        "title": label or "Known browser URL",
                        "source_name": f"Browser linked content from {source.get('name')}",
                        "source_group": "browser_dom_linked_resources",
                        "source_type": "deep_linked_content",
                        "priority": source.get("priority"),
                        "handling": "browser_dom_deep_content",
                        "retrieved_at": datetime.now(timezone.utc).isoformat(),
                        "local_processing_status": "skipped_seen_url",
                        "content_quality": "not_fetched",
                        "fetch_error": "seen_url",
                        "discovered_from": sanitize_url_for_evidence(source["url"]),
                        "linked_resource_score": score,
                        "linked_resource_anchor_text": label,
                        **_browser_fields(source["id"], browser_version),
                    }
                )
                continue
            try:
                page_data = await navigate_extract(
                    page,
                    href,
                    policy=policy,
                    recorder=recorder,
                    navigation_id=f"deep-{sequence}",
                )
                quality = classify_content(
                    page_data.get("url") or href,
                    page_data.get("title") or "",
                    page_data.get("text") or "",
                    len(page_data.get("links") or []),
                )
                status = (
                    "browser_fetched_content"
                    if quality == "actual_content"
                    else "browser_fetched_index"
                    if quality == "index_or_listing"
                    else "browser_fetched_metadata"
                )
                content_hash = hashlib.sha256((page_data.get("text") or "").encode()).hexdigest()
                record = {
                    **source_provenance(source, "discovered_content"),
                    "url": safe_href,
                    "title": page_data.get("title") or label,
                    "source_name": f"Browser linked content from {source.get('name')}",
                    "source_group": "browser_dom_linked_resources",
                    "source_type": "deep_linked_content",
                    "priority": source.get("priority"),
                    "handling": "browser_dom_deep_content",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "local_processing_status": status,
                    "content_quality": quality,
                    "page_kind": quality,
                    "discovered_from": sanitize_url_for_evidence(source["url"]),
                    "linked_resource_score": score,
                    "linked_resource_anchor_text": label,
                    **_browser_fields(source["id"], browser_version),
                    **_page_record_fields(page_data),
                }
                effective_key = url_identity(canonical_url(href))
                previous = seen.get("urls", {}).get(effective_key, {})
                if quality == "actual_content" and previous.get("content_hash") == content_hash:
                    record["local_processing_status"] = "skipped_unchanged_content"
                    record["content_quality"] = "unchanged_content"
                    record["fetch_error"] = "Content hash unchanged from previous browser state."
                records.append(record)
                if quality == "actual_content" and TRACK_SEEN_STATE:
                    seen["urls"][effective_key] = {
                        "first_seen": previous.get("first_seen") or record["retrieved_at"],
                        "last_seen": record["retrieved_at"],
                        "last_checked": record["retrieved_at"],
                        "last_changed": (
                            previous.get("last_changed")
                            if previous.get("content_hash") == content_hash
                            else record["retrieved_at"]
                        ),
                        "title": record["title"],
                        "source_name": record["source_name"],
                        "source_group": record["source_group"],
                        "source_id": source["id"],
                        "content_hash": content_hash,
                        "content_char_count": record["content_char_count"],
                    }
                    seen_updates += 1
            except Exception as error:
                records.append(
                    _failure_record(
                        source,
                        "discovered_content",
                        href,
                        error,
                        title=label,
                        source_name=f"Browser linked content from {source.get('name')}",
                        source_group="browser_dom_linked_resources",
                        source_type="deep_linked_content",
                        priority=source.get("priority"),
                        handling="browser_dom_deep_content",
                        discovered_from=sanitize_url_for_evidence(source["url"]),
                        linked_resource_score=score,
                        linked_resource_anchor_text=label,
                        **_browser_fields(source["id"], browser_version),
                    )
                )
    except Exception as error:
        records.append(
            _failure_record(
                source,
                "root",
                source["url"],
                error,
                **_browser_fields(source["id"], browser_version),
            )
        )
    finally:
        cleanup_error = None
        if context is not None:
            try:
                await context.close()
            except Exception as error:
                cleanup_error = error
        if cleanup_error is not None:
            records.append(
                _failure_record(
                    source,
                    "context_cleanup",
                    source["url"],
                    cleanup_error,
                    failure_stage="context_close",
                    **_browser_fields(source["id"], browser_version),
                )
            )
        failure = next(
            (record for record in records if record.get("error_code")),
            None,
        )
        manifest = recorder.write(
            failure_stage=failure.get("error_stage") if failure else None,
            error_code=failure.get("error_code") if failure else None,
        )
        fields = _browser_fields(source["id"], browser_version, manifest)
        for record in records:
            record.update(fields)
    return records, seen_updates


async def _run_pipeline() -> int:
    selected = load_sources(CONFIG)
    sources = selected if MAX_SOURCES <= 0 else selected[:MAX_SOURCES]
    seen = load_seen()
    seen.setdefault("urls", {})
    records: list[dict] = []
    seen_updates = 0
    browser_version = "not_started"
    browser_started = False
    browser = None
    playwright = None
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
            source_records, source_seen_updates = await process_source(
                browser,
                source,
                seen,
                browser_version,
            )
            records.extend(source_records)
            seen_updates += source_seen_updates
    except Exception as error:
        observed_roots = {
            record.get("source_id")
            for record in records
            if record.get("record_kind") == "root"
        }
        for source in sources:
            if source["id"] in observed_roots:
                continue
            failure_record = _failure_record(
                source,
                "root",
                source["url"],
                error,
                failure_stage="browser_startup",
            )
            recorder = BrowserEvidenceRecorder(
                source_id=source["id"],
                output_root=RUN_DIR / "browser-evidence",
                max_events=MAX_NETWORK_EVENTS,
                browser_version=browser_version,
            )
            failure_manifest = recorder.write(
                failure_stage=failure_record["error_stage"],
                error_code=failure_record["error_code"],
            )
            failure_record.update(_browser_fields(source["id"], browser_version, failure_manifest))
            records.append(failure_record)
    finally:
        if browser is not None:
            await browser.close()
        if playwright is not None:
            await playwright.stop()
    save_seen(seen)
    jsonl = RUN_DIR / "learning-candidates.jsonl"
    with jsonl.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    os.chmod(jsonl, 0o600)
    counts: dict[str, int] = {}
    quality_counts: dict[str, int] = {}
    for record in records:
        status = record.get("local_processing_status", "unknown")
        counts[status] = counts.get(status, 0) + 1
        quality = record.get("content_quality", "unknown")
        quality_counts[quality] = quality_counts.get(quality, 0) + 1
    root_records = [record for record in records if record.get("record_kind") == "root"]
    root_successes = [
        record for record in root_records if record.get("local_processing_status") != "browser_failed"
    ]
    root_failures_observed = len(root_records) - len(root_successes)
    contexts_created = sum(bool(record.get("browser_context_isolated")) for record in root_records)
    context_guards_ready = sum(bool(record.get("browser_context_guard_ready")) for record in root_records)
    network_events = sum(int(record.get("browser_network_event_count") or 0) for record in root_records)
    network_bytes = sum(int(record.get("browser_network_event_bytes") or 0) for record in root_records)
    truncated_events = sum(int(record.get("browser_truncated_event_count") or 0) for record in root_records)
    dropped_events = sum(int(record.get("browser_dropped_event_count") or 0) for record in root_records)
    dropped_event_bytes = sum(int(record.get("browser_dropped_event_byte_count") or 0) for record in root_records)
    blocked_total = sum(int(record.get("browser_blocked_request_total") or 0) for record in root_records)
    blocked_recorded = sum(int(record.get("browser_blocked_request_recorded") or 0) for record in root_records)
    blocked_dropped = sum(
        int(record.get("browser_dropped_blocked_request_count") or 0) for record in root_records
    )
    telemetry_errors = sum(
        int(record.get("browser_telemetry_callback_errors") or 0) for record in root_records
    )
    startup_state = "not_started" if not sources else ("started" if browser_started else "failed")
    summary = RUN_DIR / "learning-run-summary.md"
    summary.write_text(
        "# Browser Learning Ingest Summary\n\n"
        + f"- Engine: Playwright Chromium (`{browser_version}`)\n"
        + f"- Browser startup observed: {startup_state}\n"
        + f"- Isolated contexts created/selected: {contexts_created}/{len(sources)}\n"
        + f"- Context guards ready/selected: {context_guards_ready}/{len(sources)}\n"
        + f"- Roots succeeded/failed: {len(root_successes)}/{root_failures_observed}\n"
        + "- Configured request policy: public HTTP(S), no credentials, strict global-unicast proxy validation\n"
        + "- Configured WebSocket policy: disabled\n"
        + f"- Network evidence: {network_events} retained events / {network_bytes} bytes; {truncated_events} truncated attempts; {dropped_events} dropped events / {dropped_event_bytes} bytes\n"
        + f"- Observed blocked requests: {blocked_total} total; {blocked_recorded} retained; {blocked_dropped} dropped\n"
        + f"- Observed telemetry callback errors: {telemetry_errors}\n"
        + "- Evidence policy: bounded and value-redacted; exercised only where a context was created\n"
        + f"- Cadence: {RUN_CADENCE}\n"
        + f"- Registry schema/digest: {REGISTRY.schema_version} / `{REGISTRY.digest}`\n"
        + f"- Sources selected before cap: {len(selected)}\n"
        + f"- Sources processed: {len(sources)}\n"
        + f"- Records: {len(records)}\n"
        + f"- Seen updates: {seen_updates}\n"
        + f"- Candidate file: `{jsonl}`\n\n"
        + "## Statuses\n"
        + "".join(f"- {key}: {value}\n" for key, value in sorted(counts.items()))
        + "\n## Content quality\n"
        + "".join(
            f"- {key}: {value}\n" for key, value in sorted(quality_counts.items())
        ),
        encoding="utf-8",
    )
    os.chmod(summary, 0o600)
    print(
        json.dumps(
            {
                "run_dir": str(RUN_DIR),
                "jsonl": str(jsonl),
                "summary": str(summary),
                "browser_engine": "playwright-chromium",
                "browser_version": browser_version,
                "records": len(records),
                "statuses": counts,
                "content_quality": quality_counts,
                "seen_updates": seen_updates,
                "browser_startup_observed": startup_state,
                "contexts_created": contexts_created,
                "context_guards_ready": context_guards_ready,
                "roots_succeeded": len(root_successes),
                "roots_failed": root_failures_observed,
                "network_event_count": network_events,
                "network_event_bytes": network_bytes,
                "truncated_network_event_count": truncated_events,
                "dropped_network_event_count": dropped_events,
                "dropped_network_event_bytes": dropped_event_bytes,
                "blocked_request_total": blocked_total,
                "blocked_request_recorded": blocked_recorded,
                "dropped_blocked_request_count": blocked_dropped,
                "telemetry_callback_errors": telemetry_errors,
            },
            indent=2,
            sort_keys=True,
        )
    )
    root_failures = [
        record
        for record in records
        if record.get("record_kind") == "root"
        and record.get("local_processing_status") == "browser_failed"
    ]
    successful_roots = [
        record
        for record in records
        if record.get("record_kind") == "root"
        and record.get("local_processing_status") != "browser_failed"
    ]
    return 2 if root_failures or (sources and not successful_roots) else 0


async def async_main() -> int:
    try:
        async with asyncio.timeout(MAX_TOTAL_SECONDS):
            return await _run_pipeline()
    except TimeoutError as error:
        failure = controlled_error(error, stage="run_budget")
        failure_path = RUN_DIR / "run-failure.json"
        failure_path.write_text(json.dumps(failure, sort_keys=True) + "\n", encoding="utf-8")
        os.chmod(failure_path, 0o600)
        return 124


def main() -> None:
    raise SystemExit(asyncio.run(async_main()))


if __name__ == "__main__":
    main()
