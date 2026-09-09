#!/usr/bin/env python3
"""Argus learning ingest: fetch actual learning content, not just indexes.

Design goals:
- Daily cron: prioritize deep content from AppSec.fyi linked resources and blog/report
  landing pages. Treat roots/topic pages as discovery only.
- One-time/backfill mode: include heavyweight roots (PortSwigger/HackTricks/OWASP)
  and deep links from them when ARGUS_INCLUDE_BACKFILL=1.
- Every record carries content quality so compiler can ignore listing metadata.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urljoin, urlparse
from urllib.request import Request
from urllib.robotparser import RobotFileParser

from browser_runtime import controlled_error, sanitize_persisted_url_fields
from learning_registry import grouped_sources, load_registry, provenance_fields, select_sources
from learning_state import canonical_url, merge_json_state, migrate_seen_url_state, url_identity
from mandatory_proxy import build_mandatory_proxy_opener

CONFIG = Path(sys.argv[1]).expanduser()
RUN_DIR = Path(sys.argv[2]).expanduser()
DRY = os.environ.get("ARGUS_DRY_RUN", "").lower() in {"1", "true", "yes"}
TIMEOUT = float(os.environ.get("ARGUS_FETCH_TIMEOUT", "8"))
MAX_BYTES = int(os.environ.get("ARGUS_FETCH_MAX_BYTES", "600000"))
USER_AGENT = os.environ.get(
    "ARGUS_USER_AGENT",
    "ArgusLearningIngest/1.1 (+local security research methodology compiler; low-rate)",
)
EGRESS_PROXY = os.environ.get(
    "ARGUS_BROWSER_EGRESS_PROXY",
    "http://127.0.0.1:9219",
)
HTTP_OPENER = build_mandatory_proxy_opener(EGRESS_PROXY)
MAX_TOTAL_SECONDS = float(os.environ.get("ARGUS_MAX_TOTAL_SECONDS", "300"))
MAX_SOURCES_PER_GROUP = int(os.environ.get("ARGUS_MAX_SOURCES_PER_GROUP", "6"))
PRIORITY_ONLY = os.environ.get("ARGUS_PRIORITY_ONLY", "").lower() in {"1", "true", "yes"}
INCLUDE_BACKFILL = os.environ.get("ARGUS_INCLUDE_BACKFILL", "").lower() in {"1", "true", "yes"}
MAX_APPSEC_LINK_FETCHES = int(os.environ.get("ARGUS_MAX_APPSEC_LINK_FETCHES", "20"))
MAX_APPSEC_LINK_RECORDS = int(os.environ.get("ARGUS_MAX_APPSEC_LINK_RECORDS", "60"))
MAX_DAILY_DEEP_LINK_FETCHES = int(os.environ.get("ARGUS_MAX_DAILY_DEEP_LINK_FETCHES", "20"))
MAX_DEEP_LINKS_PER_SOURCE = int(os.environ.get("ARGUS_MAX_DEEP_LINKS_PER_SOURCE", "5"))
MAX_BACKFILL_DEEP_LINK_FETCHES = int(os.environ.get("ARGUS_MAX_BACKFILL_DEEP_LINK_FETCHES", "300"))
MAX_BACKFILL_LINKS_PER_SOURCE = int(os.environ.get("ARGUS_MAX_BACKFILL_LINKS_PER_SOURCE", "75"))
MAX_BACKFILL_CRAWL_DEPTH = int(os.environ.get("ARGUS_MAX_BACKFILL_CRAWL_DEPTH", "4"))
MIN_CONTENT_CHARS = int(os.environ.get("ARGUS_MIN_CONTENT_CHARS", "1200"))
MAX_CONTENT_EXCERPT = int(os.environ.get("ARGUS_MAX_CONTENT_EXCERPT", "6000"))
START_TIME = time.monotonic()
SEEN_STATE_PATH = Path(os.environ.get("ARGUS_LEARNING_SEEN_STATE", str(Path.home() / ".config/argus/learning-seen-urls.json"))).expanduser()
REFETCH_SEEN_AFTER_DAYS = int(os.environ.get("ARGUS_REFETCH_SEEN_AFTER_DAYS", "30"))
TRACK_SEEN_STATE = os.environ.get("ARGUS_TRACK_SEEN_STATE", "1").lower() not in {"0", "false", "no"}
RUN_CADENCE = os.environ.get("ARGUS_LEARNING_CADENCE", "legacy").strip().lower()
PROVENANCE_RUN_ID = os.environ.get("ARGUS_PROVENANCE_RUN_ID", "").strip() or RUN_DIR.name
BACKFILL_REASON = os.environ.get("ARGUS_BACKFILL_REASON", "").strip()
SOURCE_FILTER = {
    value.strip()
    for value in os.environ.get("ARGUS_SOURCE_FILTER", "").split(",")
    if value.strip()
}
RUN_DIR.mkdir(parents=True, exist_ok=True)


def remaining_seconds() -> float:
    return MAX_TOTAL_SECONDS - (time.monotonic() - START_TIME)


def budget_ok(min_remaining: float = 2.0) -> bool:
    return remaining_seconds() > min_remaining


def budget_status() -> str:
    return f"remaining={remaining_seconds():.1f}s max_total={MAX_TOTAL_SECONDS:.1f}s"


def load_seen_state() -> dict:
    if not TRACK_SEEN_STATE or DRY:
        return {"urls": {}}
    return migrate_seen_url_state(
        SEEN_STATE_PATH,
        warn=lambda message: print(message, file=sys.stderr),
    )


def save_seen_state(state: dict) -> None:
    if not TRACK_SEEN_STATE or DRY:
        return
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    merge_json_state(SEEN_STATE_PATH, state, default={"urls": {}}, warn=lambda message: print(message, file=sys.stderr))


def iso_age_days(ts: str) -> float | None:
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).total_seconds() / 86400.0
    except Exception:
        return None


class ContentParser(HTMLParser):
    CONTENT_TAGS = {"article", "main", "section", "p", "li", "h1", "h2", "h3", "h4", "pre", "code", "blockquote", "td", "th"}
    SKIP_TAGS = {"script", "style", "noscript", "svg", "canvas"}

    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title: list[str] = []
        self.meta_desc: list[str] = []
        self.links: list[str] = []
        self.link_records: list[dict] = []
        self.tag_stack: list[str] = []
        self.text_chunks: list[str] = []
        self.current_href: str | None = None
        self.current_link_text: list[str] = []
        self.skip_depth = 0
        self.article_count = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        d = dict(attrs)
        if tag == "article":
            self.article_count += 1
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
        self.tag_stack.append(tag)
        if tag == "title":
            self.in_title = True
        if tag == "a" and d.get("href"):
            self.current_href = d["href"]
            self.current_link_text = []
            self.links.append(d["href"])
        if tag == "meta":
            name = (d.get("name") or d.get("property") or "").lower()
            if name in {"description", "og:description", "twitter:description"} and d.get("content"):
                self.meta_desc.append(d["content"])

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        if tag == "a" and self.current_href:
            label = " ".join(" ".join(self.current_link_text).split())[:240]
            self.link_records.append({"href": self.current_href, "text": label})
            self.current_href = None
            self.current_link_text = []
        if tag in self.SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
        for i in range(len(self.tag_stack) - 1, -1, -1):
            if self.tag_stack[i] == tag:
                del self.tag_stack[i:]
                break

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title.append(data)
        if self.current_href is not None:
            self.current_link_text.append(data)
        if self.skip_depth:
            return
        if any(t in self.CONTENT_TAGS for t in self.tag_stack):
            cleaned = " ".join(data.split())
            if cleaned:
                self.text_chunks.append(cleaned)


def parse_scalar(v: str):
    v = v.strip()
    if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
        return v[1:-1]
    if v in {"true", "false"}:
        return v == "true"
    if re.fullmatch(r"\d+", v):
        return int(v)
    return v


def load_simple_yaml(path: Path):
    data = {}
    current_group = None
    current_item = None
    current_key = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if indent == 0 and line.endswith(":"):
            current_group = line[:-1]
            data[current_group] = [] if current_group not in {"appsec_fyi_discovery_rule"} else {}
            current_item = None
            current_key = None
            continue
        if current_group is None:
            continue
        if line.startswith("- ") and indent <= 2:
            rest = line[2:].strip()
            current_item = {}
            data.setdefault(current_group, []).append(current_item)
            current_key = None
            if rest and ":" in rest:
                k, v = rest.split(":", 1)
                current_item[k.strip()] = parse_scalar(v)
            continue
        if current_group == "appsec_fyi_discovery_rule":
            if indent == 2 and ":" in line:
                k, v = line.split(":", 1)
                k = k.strip(); v = v.strip()
                if v:
                    data[current_group][k] = parse_scalar(v); current_key = k
                else:
                    data[current_group][k] = []; current_key = k
            elif indent >= 4 and line.startswith("- ") and current_key:
                data[current_group][current_key].append(parse_scalar(line[2:]))
            continue
        if isinstance(data.get(current_group), list) and current_item is not None and ":" in line:
            k, v = line.split(":", 1)
            current_item[k.strip()] = parse_scalar(v)
    return data


robots_cache = {}


def robots_allowed(url: str) -> tuple[bool, str]:
    try:
        p = urlparse(url)
        if p.scheme not in {"http", "https"} or not p.netloc:
            return False, "non_http_url"
        base = f"{p.scheme}://{p.netloc}"
        if base not in robots_cache:
            rp = RobotFileParser()
            robots_url = base + "/robots.txt"
            rp.set_url(robots_url)
            try:
                req = Request(robots_url, headers={"User-Agent": USER_AGENT})
                with HTTP_OPENER.open(
                    req,
                    timeout=min(TIMEOUT, max(1.0, remaining_seconds())),
                ) as response:
                    limit = min(MAX_BYTES, 256_000)
                    body = response.read(limit + 1)
                    if len(body) > limit:
                        return False, "robots_too_large"
                    encoding = response.headers.get_content_charset() or "utf-8"
                    rp.parse(body.decode(encoding, "replace").splitlines())
            except HTTPError as error:
                if error.code in {401, 403}:
                    rp.disallow_all = True
                    rp.modified()
                elif 400 <= error.code < 500:
                    rp.allow_all = True
                    rp.modified()
                else:
                    return False, f"robots_http_error:{error.code}"
            except Exception as error:
                return False, f"robots_fetch_failed:{type(error).__name__}"
            robots_cache[base] = rp
        return robots_cache[base].can_fetch(USER_AGENT, url), "robots_checked_via_pinned_proxy"
    except Exception as error:
        return False, f"robots_error:{type(error).__name__}"


INDEX_PATH_TOKENS = {
    "index", "all-topics", "topics", "resources", "reports", "blog", "research", "learn", "category", "tag",
    "archive", "changelog", "overview", "feed", "home", "timeline", "sources", "tools"
}
INDEX_TITLE_PHRASES = ["all topics", "resources", "reports", "audit reports", "security audit reports", "blog", "research papers", "home", "resource library"]


def is_index_like_url(url: str, title: str = "", link_count: int = 0) -> bool:
    p = urlparse(url); path = (p.path or "/").lower(); host = p.netloc.lower(); title = (title or "").lower()
    if host in {"github.com", "www.github.com"} and path.count("/") <= 2:
        return True
    if host == "appsec.fyi" and (path in {"/", "/index.html"} or path.endswith(".html")):
        return True
    if "code4rena.com" in host and path.rstrip("/") == "/reports":
        return True
    if path in {"", "/"} and link_count > 20:
        return True
    if any(tok in path for tok in INDEX_PATH_TOKENS) and link_count > 25:
        return True
    if any(phrase in title for phrase in INDEX_TITLE_PHRASES) and link_count > 20:
        return True
    return False


def is_wayback_dated_article_url(url: str) -> bool:
    """Return True for fixed Wayback snapshots of dated article paths.

    Wayback wraps the original page with high-link-count navigation. A dated
    original path is a stronger signal than that wrapper, while archive roots,
    categories, tags, and undated indexes remain subject to normal heuristics.
    """
    parsed = urlparse(url)
    if parsed.netloc.lower() != "web.archive.org":
        return False
    match = re.match(r"^/web/\d+(?:[a-z_]+)?/(https?://.+)$", parsed.path, re.IGNORECASE)
    if not match:
        return False
    original = urlparse(match.group(1))
    segments = [segment for segment in original.path.split("/") if segment]
    for index in range(len(segments) - 2):
        if re.fullmatch(r"20\d{2}", segments[index]) and re.fullmatch(r"(?:0?[1-9]|1[0-2])", segments[index + 1]):
            slug = segments[index + 2]
            return slug not in {"index", "index.html", "archive", "category", "tag"}
    return False


def content_quality(url: str, title: str, text: str, link_count: int, article_signal: bool = False) -> str:
    chars = len(text or "")
    # Deep articles often live below /blog/ and include normal site navigation.
    # A single semantic <article> or Article JSON-LD is stronger than the
    # broad URL/link-count listing heuristic.
    if article_signal and chars >= MIN_CONTENT_CHARS:
        return "actual_content"
    if is_index_like_url(url, title, link_count):
        return "index_or_listing"
    if chars >= MIN_CONTENT_CHARS:
        return "actual_content"
    if chars >= 400:
        return "thin_content"
    return "metadata_only"


def fetch(url: str) -> dict:
    if DRY:
        return {"status": "dry_run_not_fetched", "title": "", "excerpt": "", "links": [], "link_records": [], "error": ""}
    if not budget_ok(TIMEOUT + 1.0):
        return {"status": "skipped_run_budget_exceeded", "title": "", "excerpt": "", "links": [], "link_records": [], "error": budget_status()}
    allowed, robots_note = robots_allowed(url)
    if not allowed:
        return {"status": "blocked_by_robots_txt", "title": "", "excerpt": "", "links": [], "link_records": [], "error": robots_note}
    try:
        req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.5"})
        effective_timeout = max(1.0, min(TIMEOUT, remaining_seconds() - 1.0))
        with HTTP_OPENER.open(req, timeout=effective_timeout) as r:
            ct = r.headers.get("content-type", "")
            body = r.read(MAX_BYTES)
            final_url = r.geturl()
        text = body.decode("utf-8", "replace")
        parser = ContentParser(); parser.feed(text)
        title = html.unescape(" ".join(" ".join(parser.title).split()))[:240]
        extracted_text = " ".join(" ".join(parser.text_chunks).split())
        fallback_text = " ".join(re.sub(r"<[^>]+>", " ", text[:40000]).split())
        content_text = extracted_text if len(extracted_text) >= 300 else fallback_text
        article_signal = parser.article_count == 1 or is_wayback_dated_article_url(final_url or url) or bool(
            re.search(r'["\']@type["\']\s*:\s*["\']Article["\']', text, re.IGNORECASE)
        )
        q = content_quality(final_url or url, title, content_text, len(parser.links), article_signal)
        content_hash = hashlib.sha256(content_text.encode("utf-8", "replace")).hexdigest() if content_text else ""
        status = "fetched_content" if q == "actual_content" else "fetched_index_metadata" if q == "index_or_listing" else "fetched_metadata"
        excerpt_source = content_text[:MAX_CONTENT_EXCERPT]
        if q != "actual_content" and parser.meta_desc:
            excerpt_source = parser.meta_desc[0]
        return {
            "status": status,
            "title": title,
            "excerpt": " ".join(excerpt_source.split())[:900],
            "content_excerpt": content_text[:MAX_CONTENT_EXCERPT],
            "content_char_count": len(content_text),
            "content_quality": q,
            "content_hash": content_hash,
            "page_kind": q,
            "links": parser.links[:700],
            "link_records": parser.link_records[:700],
            "content_type": ct,
            "effective_url": final_url,
            "error": "",
        }
    except Exception as error:
        safe_error = controlled_error(error, stage="static_fetch")
        return {
            "status": "manual_review_required",
            "title": "",
            "excerpt": "",
            "links": [],
            "link_records": [],
            "error": safe_error["error_code"],
            **safe_error,
        }


def classify_linked_resource(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if any(x in host for x in ["owasp.org", "github.com/owasp"]): return "official docs"
    if "portswigger.net" in host: return "academy/research"
    if any(x in host for x in ["github.com", "gitlab.com"]): return "repository/advisory/tool"
    if any(x in host for x in ["youtube.com", "youtu.be", "slideshare"]): return "talk"
    if any(x in host for x in ["medium.com", "substack.com", "blog"]): return "blog/research"
    return "writeup/resource"


def source_quality_default(item: dict, group: str) -> int:
    if "source_quality_default" in item: return int(item["source_quality_default"])
    trust_score = {"authority": 10, "primary": 9, "curated_secondary": 7, "discovery_only": 4, "contextual": 5}
    if item.get("trust") in trust_score: return trust_score[item["trust"]]
    typ = item.get("type", "")
    if typ in {"official_docs", "official_standard", "official_testing_guide", "official_cheat_sheets"}: return 10
    if typ in {"contest_reports", "judging_guidelines", "severity_standard"}: return 9
    if typ in {"research_blog", "web3_security_research", "academy", "bounty_learning"}: return 8
    if typ in {"topic_page", "topic_index", "training"}: return 6
    if typ in {"blog_feed", "researcher_blog", "podcast_notes"}: return 6
    return 5


def candidate_record(group: str, item: dict, status_data: dict, extra: dict | None = None) -> dict:
    rec = {
        "url": item.get("url"),
        "effective_url": status_data.get("effective_url", item.get("url")),
        "title": status_data.get("title") or item.get("name"),
        "source_name": item.get("name"),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "source_group": group,
        "source_type": item.get("type"),
        "priority": item.get("priority"),
        "source_quality_default": source_quality_default(item, group),
        "short_excerpt_or_summary": status_data.get("excerpt", ""),
        "content_excerpt": status_data.get("content_excerpt", ""),
        "content_char_count": status_data.get("content_char_count", 0),
        "content_quality": status_data.get("content_quality", ""),
        "content_hash": status_data.get("content_hash", ""),
        "page_kind": status_data.get("page_kind", ""),
        "local_processing_status": status_data.get("status"),
        "fetch_error": status_data.get("error", ""),
        "handling": item.get("handling", ""),
        "topic": item.get("topic", ""),
        "notes": item.get("notes", ""),
    }
    if extra: rec.update(extra)
    source = item if item.get("id") else REGISTRY_BY_ID.get(rec.get("parent_source_id", ""))
    if source:
        rec.update(provenance_fields(
            REGISTRY,
            source,
            run_cadence=RUN_CADENCE,
            record_kind=item.get("_record_kind", "root" if item.get("url") == source.get("url") else "discovered_content"),
            run_id=PROVENANCE_RUN_ID,
        ))
        if rec.get("record_kind") != "root":
            rec.setdefault("parent_source_id", source["id"])
    if BACKFILL_REASON:
        rec["backfill_reason"] = BACKFILL_REASON
    return sanitize_persisted_url_fields(rec)


def allowed_appsec_topic(url: str, rule: dict) -> bool:
    if not url.startswith("https://appsec.fyi/") or not url.endswith(".html"): return False
    for ex in rule.get("exclude", []):
        pat = "^" + re.escape(ex).replace("\\*", ".*") + "$"
        if re.match(pat, url): return False
    return True


def is_low_signal_share_url(url: str) -> bool:
    p = urlparse(url); host = p.netloc.lower(); path = p.path.lower()
    if host in {"x.com", "twitter.com"} and ("/intent/" in path or "/share" in path): return True
    if host.endswith("linkedin.com") and ("/sharing/" in path or "share-offsite" in path): return True
    if host in {"www.facebook.com", "facebook.com"} and "/sharer" in path: return True
    if host in {"reddit.com", "www.reddit.com"} and "/submit" in path: return True
    if host == "news.ycombinator.com" and "submitlink" in path: return True
    return False


def score_linked_resource(url: str, link_text: str = "") -> int:
    p = urlparse(url); host = p.netloc.lower(); path = p.path.lower(); text = (link_text or "").lower()
    score = 0
    if any(x in host for x in ["portswigger.net", "developer.mozilla.org", "escape.tech", "advisories.gitlab.com", "github.com", "gitlab.com", "projectdiscovery.io", "hackerone.com", "intigriti.com", "yeswehack.com", "embracethered.com", "simonwillison.net", "arcanum-sec.github.io"]): score += 25
    if any(tok in path for tok in ["cve-", "ghsa-", "advisories", "advisory", "vulnerab", "idor", "bola", "broken-object", "authorization", "access-control", "graphql", "api-security", "writeup", "report", "blog", "post", "article", "docs", "cheatsheet", "research", "labs", "prompt", "injection", "llm", "ai", "taxonomy"]): score += 35
    if re.search(r"/20\d{2}/(0?[1-9]|1[0-2])/", path) or re.search(r"/20\d{2}[-/]", path): score += 35
    if "rekt.news" in host and path.endswith("-rekt"): score += 35
    if "code4rena.com" in host and re.search(r"/reports/20\d{2}", path): score += 35
    if any(tok in text for tok in ["idor", "bola", "broken object", "authorization", "access control", "case study", "writeup", "report", "cve", "advisory", "how to", "guide", "research", "vulnerability", "exploit", "root cause", "prompt injection", "llm", "ai security", "agent"]): score += 20
    # Penalize navigation/product/policy links that are content-heavy but poor learning inputs.
    if any(tok in path for tok in ["privacy", "terms", "policy", "transparency", "disclosure-policy", "vulnerability-scanner", "product", "pricing", "downloads", "support", "login", "register"]): score -= 70
    if path.lower().endswith((".pdf", ".png", ".jpg", ".jpeg", ".svg", ".zip")): score -= 30
    if path in {"", "/"}: score -= 30
    if any(tok in path for tok in ["awesome", "scanner", "tool", "github.com/search"]): score -= 15
    if any(x in host for x in ["youtube.com", "youtu.be", "x.com", "twitter.com", "linkedin.com"]): score -= 50
    return score


def appsec_topic_priority(url: str):
    slug = url.rsplit("/", 1)[-1].lower()
    preferred = ["idor.html", "authz.html", "apisec.html", "authn.html", "oauth.html", "jwt.html", "file-upload.html", "upload.html", "s3.html", "secrets.html", "ssrf.html", "graphql.html", "xss.html", "csrf.html", "deser.html", "rce.html"]
    try: return (preferred.index(slug), slug)
    except ValueError: return (100, slug)


def is_backfill_source(group: str, item: dict) -> bool:
    cadence = str(item.get("cadence", "")).lower()
    if cadence in {"one_time", "one-time", "backfill", "one_time_full", "less_frequent", "periodic", "on_demand"}: return True
    if group in {"web2_core_theory", "web3_core_theory"}: return True
    return False


def should_process_item(group: str, item: dict) -> tuple[bool, str]:
    if PRIORITY_ONLY and item.get("priority") != "high":
        return False, "skipped_priority_filter"
    if RUN_CADENCE == "legacy" and is_backfill_source(group, item) and not INCLUDE_BACKFILL:
        return False, "skipped_backfill_source"
    return True, ""


def apply_source_native_gate(item: dict, url: str, meta: dict) -> dict:
    """Prevent long application shells from being compiled as learning content."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    source_type = str(item.get("type", "")).lower()
    reason = ""
    if "repository" in source_type and host in {"github.com", "www.github.com", "gitlab.com", "www.gitlab.com"}:
        reason = "repository_clone_required"
    elif host in {"youtube.com", "www.youtube.com", "m.youtube.com"} and parsed.path.rstrip("/") == "/playlist":
        reason = "youtube_playlist_metadata_and_transcripts_required"
    if not reason:
        return meta
    gated = dict(meta)
    gated.update({
        "status": "source_native_required",
        "content_quality": "source_native_required",
        "page_kind": "application_shell_or_index",
        "excerpt": f"Generic HTML is not authoritative learning content for this source ({reason}). Use the source-native handler.",
        "content_excerpt": "",
        "content_char_count": 0,
        "content_hash": "",
        "error": reason,
    })
    return gated


def is_unwanted_learning_link(url: str, root_url: str = "") -> bool:
    p=urlparse(url); path=(p.path or "/").lower(); host=p.netloc.lower()
    # HackTricks mirrors create duplicate non-English pages; keep /en/ and root paths only.
    if "hacktricks.wiki" in host:
        m=re.match(r"^/([a-z]{2})(/|$)", path)
        if m and m.group(1) != "en":
            return True
        if any(x in path for x in ["/welcome/", "values-and-faq"]):
            return True
    # For PortSwigger, keep Academy/Research methodology pages; reject product/company/commerce pages
    # that are long enough to look like content but are poor learning inputs.
    if "portswigger.net" in host:
        if path.startswith("/web-security/"):
            if any(x in path for x in ["/certification", "/all-labs", "/users", "/dashboard", "/hall-of-fame", "/mystery-lab-challenge"]):
                return True
        elif path.startswith("/research/"):
            return False
        else:
            return True
    # GitHub project chrome is extremely noisy during OWASP backfill. Prefer raw/known docs over
    # issues, PRs, actions, settings, generated repo pages, and administrative markdown.
    if host in {"github.com", "www.github.com"}:
        noisy_segments = ["/issues", "/pulls", "/actions", "/activity", "/discussions", "/security", "/pulse", "/graphs", "/network", "/settings", "/custom-properties", "/releases", "/contribute"]
        if any(seg in path for seg in noisy_segments):
            return True
        noisy_files = ("/.gitignore", "/.gitattributes", "/.editorconfig", "/license", "/license.md", "/contributing.md", "/code_of_conduct.md", "/makefile", "/security.md", "/readme.md")
        if path.endswith(noisy_files):
            return True
        if "/blob/" not in path and "/raw/" not in path:
            return True
    # Generic product/navigation/policy pages are poor learning inputs.
    if any(x in path for x in ["/pricing", "/product", "/enterprise", "/downloads", "/support", "/login", "/register", "/privacy", "/terms", "/about", "/contact", "/careers", "/legal", "/solutions", "/customers"]):
        return True
    return False


def ranked_links(base_url: str, meta: dict, same_domain_preferred: bool = False) -> list[tuple[int, str, str]]:
    out = []
    base_host = urlparse(base_url).netloc.lower()
    for lr in meta.get("link_records") or [{"href": h, "text": ""} for h in meta.get("links", [])]:
        full = urljoin(base_url, lr.get("href", "")).split("#")[0]
        if not full.startswith("http") or is_low_signal_share_url(full) or is_unwanted_learning_link(full, base_url):
            continue
        if full == base_url:
            continue
        score = score_linked_resource(full, lr.get("text", ""))
        if same_domain_preferred and urlparse(full).netloc.lower() == base_host:
            score += 15
        out.append((score, full, lr.get("text", "")))
    ranked = []
    seen = set()
    for score, full, label in sorted(out, key=lambda x: (-x[0], x[1])):
        if full in seen:
            continue
        seen.add(full); ranked.append((score, full, label))
    return ranked


def same_site(url: str, root_url: str) -> bool:
    a=urlparse(url); b=urlparse(root_url)
    return a.scheme.startswith('http') and a.netloc.lower() == b.netloc.lower()


def crawl_backfill_source(root_url: str, item: dict, root_meta: dict) -> int:
    """Bounded same-site crawl for one-time/reference sources.

    Fetches topic/article pages discovered from index roots. Index pages are
    recorded but not compiled; actual content pages become compiler inputs.
    """
    fetched = 0
    visited = {root_url}
    queue = []
    for score, linked, label in ranked_links(root_url, root_meta, same_domain_preferred=True):
        if same_site(linked, root_url):
            queue.append((linked, label, score, 1))
    while queue and fetched < MAX_BACKFILL_LINKS_PER_SOURCE and budget_ok(TIMEOUT + 1.0):
        linked, label, score, depth = queue.pop(0)
        if linked in visited or not same_site(linked, root_url):
            continue
        visited.add(linked)
        linked_item = {
            **item,
            "name": f"Backfill crawled content from {item.get('name')}",
            "url": linked,
            "type": "deep_linked_content",
            "priority": item.get("priority", "high"),
            "handling": "backfill_crawled_content",
            "_record_kind": "discovered_content",
        }
        linked_meta = fetch(linked)
        add_record(candidate_record("backfill_deep_content", linked_item, linked_meta, {
            "discovered_from": root_url,
            "crawl_depth": depth,
            "linked_resource_score": score,
            "linked_resource_anchor_text": label,
            "linked_resource_classification": classify_linked_resource(linked),
        }))
        fetched += 1
        if linked_meta.get("content_quality") == "index_or_listing" and depth < MAX_BACKFILL_CRAWL_DEPTH:
            for child_score, child, child_label in ranked_links(linked, linked_meta, same_domain_preferred=True):
                if child not in visited and same_site(child, root_url):
                    queue.append((child, child_label, child_score, depth + 1))
        time.sleep(0.2 if not DRY else 0)
    return fetched


REGISTRY = load_registry(CONFIG)
REGISTRY_BY_ID = {source["id"]: source for source in REGISTRY.sources}
if RUN_CADENCE == "legacy" and not SOURCE_FILTER:
    selected_sources = [dict(source) for source in REGISTRY.sources]
else:
    selection_cadence = "all" if SOURCE_FILTER and RUN_CADENCE in {"legacy", "backfill"} else RUN_CADENCE
    selected_sources = select_sources(
        REGISTRY,
        cadence=selection_cadence,
        lane="static",
        source_ids=SOURCE_FILTER or None,
        priorities={"high"} if PRIORITY_ONLY else None,
    )
data = grouped_sources(REGISTRY, selected_sources)
data["appsec_fyi_discovery_rule"] = REGISTRY.discovery_rules
records: list[dict] = []
seen: set[tuple] = set()
seen_learning_urls: set[str] = set()
seen_state = load_seen_state()
seen_state.setdefault("urls", {})
seen_state_updates = 0


def should_skip_known_url(url: str, source: dict | None = None) -> tuple[bool, str]:
    """Skip known content until the source-specific categorical refresh interval is due."""
    if INCLUDE_BACKFILL or DRY or not TRACK_SEEN_STATE:
        return False, ""
    entry = seen_state.get("urls", {}).get(url_identity(canonical_url(url)))
    if not entry:
        return False, ""
    refetch_days = int((source or {}).get("refetch_interval_days", REFETCH_SEEN_AFTER_DAYS))
    if refetch_days <= 0:
        return True, "seen_url"
    age = iso_age_days(entry.get("last_seen") or entry.get("first_seen") or "")
    if age is None or age < refetch_days:
        return True, f"seen_url_recent:{age:.1f}d" if age is not None else "seen_url_recent"
    return False, "due_periodic_refetch"


def mark_unchanged_if_seen(rec: dict) -> dict:
    if INCLUDE_BACKFILL or DRY or not TRACK_SEEN_STATE:
        return rec
    if rec.get("local_processing_status") != "fetched_content" or rec.get("content_quality") != "actual_content":
        return rec
    key = url_identity(canonical_url(rec.get("effective_url") or rec.get("url") or ""))
    old = seen_state.get("urls", {}).get(key)
    if old and old.get("content_hash") and old.get("content_hash") == rec.get("content_hash"):
        rec = dict(rec)
        rec["local_processing_status"] = "skipped_unchanged_content"
        rec["content_quality"] = "unchanged_content"
        rec["fetch_error"] = "Content hash unchanged from previous learning ingest state."
    return rec


def update_seen_state_from_record(rec: dict) -> None:
    global seen_state_updates
    if DRY or not TRACK_SEEN_STATE:
        return
    if rec.get("local_processing_status") not in {"fetched_content", "skipped_unchanged_content"}:
        return
    if (rec.get("page_kind") or rec.get("content_quality")) not in {"actual_content", "unchanged_content"}:
        return
    if rec.get("source_type") not in {"linked_resource", "deep_linked_content"}:
        return
    canonical = canonical_url(rec.get("effective_url") or rec.get("url") or "")
    if not canonical:
        return
    key = url_identity(canonical)
    urls = seen_state.setdefault("urls", {})
    now = datetime.now(timezone.utc).isoformat()
    prev = urls.get(key, {})
    urls[key] = {
        "first_seen": prev.get("first_seen") or now,
        "last_seen": now,
        "title": rec.get("title") or prev.get("title", ""),
        "source_name": rec.get("source_name") or prev.get("source_name", ""),
        "source_group": rec.get("source_group") or prev.get("source_group", ""),
        "content_hash": rec.get("content_hash") or prev.get("content_hash", ""),
        "content_char_count": rec.get("content_char_count") or prev.get("content_char_count", 0),
    }
    seen_state_updates += 1
appsec_topic_pages: list[str] = []
daily_deep_fetches = 0
backfill_deep_fetches = 0


def add_record(rec: dict) -> bool:
    rec = mark_unchanged_if_seen(rec)
    url = rec.get("url")
    key = (url, rec.get("source_group"), rec.get("appsec_topic_source", ""), rec.get("discovered_from", ""))
    if not url or key in seen:
        return False
    # Avoid compiling the same deep article/advisory twice when it is discovered
    # from both AppSec.fyi root and a topic page. Keep index/topic pages separate.
    if rec.get("source_type") in {"linked_resource", "deep_linked_content"} and rec.get("local_processing_status") == "fetched_content":
        if url in seen_learning_urls:
            return False
        seen_learning_urls.add(url)
    seen.add(key); records.append(rec); update_seen_state_from_record(rec); return True


# Process configured sources. In daily mode, backfill roots are skipped instead of being compiled as learning.
for group, items in data.items():
    if group == "appsec_fyi_discovery_rule" or not isinstance(items, list):
        continue
    processed_in_group = 0
    for item in items:
        url = item.get("url")
        if not url: continue
        ok, skip_status = should_process_item(group, item)
        if not ok:
            add_record(candidate_record(group, item, {"status": skip_status, "title": item.get("name"), "excerpt": f"Skipped in daily mode: {skip_status}.", "links": [], "error": ""}))
            continue
        if MAX_SOURCES_PER_GROUP > 0 and processed_in_group >= MAX_SOURCES_PER_GROUP:
            add_record(candidate_record(group, item, {"status": "skipped_group_limit", "title": item.get("name"), "excerpt": f"Skipped because ARGUS_MAX_SOURCES_PER_GROUP={MAX_SOURCES_PER_GROUP}.", "links": [], "error": ""}))
            continue
        if not budget_ok(TIMEOUT + 1.0):
            add_record(candidate_record(group, item, {"status": "skipped_run_budget_exceeded", "title": item.get("name"), "excerpt": "Skipped because total run budget was exhausted.", "links": [], "error": budget_status()}))
            continue
        processed_in_group += 1
        dynamic = "solodit.cyfrin.io" in url or "hackerone.com/hacktivity" in url or item.get("handling") == "browser_dom_required"
        meta = {"status": "manual_review_required", "title": item.get("name"), "excerpt": "Browser DOM extraction required. Static fetch skipped so this source can be handled by run_browser_dom_ingest.sh.", "links": [], "link_records": [], "error": "browser_dom_required"} if dynamic else fetch(url)
        meta = apply_source_native_gate(item, url, meta)
        add_record(candidate_record(group, item, meta))
        time.sleep(0.2 if not DRY else 0)
        if item.get("name") == "AppSec.fyi Root Topic Index" and meta.get("links"):
            rule = data.get("appsec_fyi_discovery_rule", {})
            for href in meta["links"]:
                full = urljoin(url, href)
                if allowed_appsec_topic(full, rule):
                    appsec_topic_pages.append(full)
        # Blog/report roots are discovery-only. Fetch top deep links from them.
        if group != "web2_topic_indexes" and meta.get("content_quality") == "index_or_listing":
            if is_backfill_source(group, item) and INCLUDE_BACKFILL:
                if backfill_deep_fetches < MAX_BACKFILL_DEEP_LINK_FETCHES:
                    before = backfill_deep_fetches
                    fetched_now = crawl_backfill_source(url, item, meta)
                    backfill_deep_fetches = min(MAX_BACKFILL_DEEP_LINK_FETCHES, before + fetched_now)
            elif (not is_backfill_source(group, item)) and daily_deep_fetches < MAX_DAILY_DEEP_LINK_FETCHES:
                source_limit = min(MAX_DEEP_LINKS_PER_SOURCE, int(item.get("deep_link_limit", MAX_DEEP_LINKS_PER_SOURCE)))
                for score, linked, label in ranked_links(url, meta, same_domain_preferred=True)[:source_limit]:
                    if daily_deep_fetches >= MAX_DAILY_DEEP_LINK_FETCHES or not budget_ok(TIMEOUT + 1.0):
                        break
                    linked_item = {**item, "name": f"Deep linked content from {item.get('name')}", "url": linked, "type": "deep_linked_content", "priority": item.get("priority", "high"), "handling": "daily_deep_content", "_record_kind": "discovered_content"}
                    skip_known, skip_reason = should_skip_known_url(linked, item)
                    if skip_known:
                        add_record(candidate_record("daily_deep_content", linked_item, {"status": "skipped_seen_url", "title": "Known daily URL", "excerpt": f"Skipped because URL is already in seen-state ({skip_reason}).", "links": [], "error": skip_reason}, {"discovered_from": url, "linked_resource_score": score, "linked_resource_anchor_text": label, "linked_resource_classification": classify_linked_resource(linked)}))
                        continue
                    linked_meta = fetch(linked)
                    add_record(candidate_record("daily_deep_content", linked_item, linked_meta, {"discovered_from": url, "linked_resource_score": score, "linked_resource_anchor_text": label, "linked_resource_classification": classify_linked_resource(linked)}))
                    daily_deep_fetches += 1
                    time.sleep(0.2 if not DRY else 0)

# AppSec root discovery: topic pages are discovery-only, linked resources are the learning content.
rule = data.get("appsec_fyi_discovery_rule", {})
appsec_root_source = REGISTRY_BY_ID.get("appsec-fyi-root-topic-index", {})
max_topics = int(rule.get("max_topic_pages_per_run", 10) or 10)
for topic_url in sorted(set(appsec_topic_pages), key=appsec_topic_priority)[:max_topics]:
    if not budget_ok(TIMEOUT + 1.0): break
    item = {**appsec_root_source, "name": f"AppSec.fyi discovered topic: {topic_url.rsplit('/',1)[-1]}", "url": topic_url, "type": "topic_page", "priority": "medium", "handling": "extract_linked_resources_as_learning_candidates", "_record_kind": "discovery_page"}
    meta = fetch(topic_url)
    add_record(candidate_record("web2_topic_indexes", item, meta, {"discovered_from": "https://appsec.fyi"}))
    time.sleep(0.2 if not DRY else 0)

max_links = int(rule.get("max_linked_resources_per_topic_per_run", 25) or 25)
linked_fetches = 0
linked_records = 0
if MAX_APPSEC_LINK_FETCHES == 0 and MAX_APPSEC_LINK_RECORDS == 0:
    pass
else:
    for rec in list(records):
        if not (rec.get("source_group") == "web2_topic_indexes" and rec.get("source_type") == "topic_page" and rec.get("url", "").startswith("https://appsec.fyi/")):
            continue
        if not budget_ok(TIMEOUT + 1.0): break
        topic_url = rec["url"]; topic_name = rec.get("topic") or rec.get("title") or topic_url
        meta = fetch(topic_url)
        for score, linked, link_label in ranked_links(topic_url, meta)[:max_links]:
            if MAX_APPSEC_LINK_RECORDS > 0 and linked_records >= MAX_APPSEC_LINK_RECORDS: break
            linked_item = {**appsec_root_source, "name": f"Linked resource from {topic_name}", "url": linked, "type": "linked_resource", "priority": "medium", "handling": "learning_candidate", "_record_kind": "discovered_content"}
            if MAX_APPSEC_LINK_FETCHES > 0 and linked_fetches >= MAX_APPSEC_LINK_FETCHES:
                add_record(candidate_record("appsec_fyi_linked_resources", linked_item, {"status": "skipped_appsec_link_fetch_limit", "title": "AppSec linked resource fetch deferred", "excerpt": f"Skipped because ARGUS_MAX_APPSEC_LINK_FETCHES={MAX_APPSEC_LINK_FETCHES}.", "links": [], "error": ""}, {"appsec_topic_source": topic_url, "appsec_topic": topic_name, "linked_resource_classification": classify_linked_resource(linked), "linked_resource_score": score, "linked_resource_anchor_text": link_label, "compiler_instruction": "Score original source independently; do not treat AppSec.fyi as authority."}))
                linked_records += 1
                continue
            if not budget_ok(TIMEOUT + 1.0): break
            skip_known, skip_reason = should_skip_known_url(linked, appsec_root_source)
            if skip_known:
                add_record(candidate_record("appsec_fyi_linked_resources", linked_item, {"status": "skipped_seen_url", "title": "Known AppSec linked resource", "excerpt": f"Skipped because URL is already in seen-state ({skip_reason}).", "links": [], "error": skip_reason}, {"appsec_topic_source": topic_url, "appsec_topic": topic_name, "linked_resource_classification": classify_linked_resource(linked), "linked_resource_score": score, "linked_resource_anchor_text": link_label, "compiler_instruction": "Score original source independently; do not treat AppSec.fyi as authority."}))
                linked_records += 1
                continue
            linked_meta = fetch(linked)
            linked_fetches += 1
            add_record(candidate_record("appsec_fyi_linked_resources", linked_item, linked_meta, {"appsec_topic_source": topic_url, "appsec_topic": topic_name, "linked_resource_classification": classify_linked_resource(linked), "linked_resource_score": score, "linked_resource_anchor_text": link_label, "compiler_instruction": "Score original source independently; do not treat AppSec.fyi as authority."}))
            linked_records += 1
            time.sleep(0.2 if not DRY else 0)

for rec in records:
    if rec.get("source_group") == "web3_continuous_monitoring" and any(x in (rec.get("source_name") or "") for x in ["Rekt", "Immunefi", "Solodit"]):
        rec["web3_extraction_required"] = {
            "protocol_type": ["bridge", "lending", "staking", "vault", "AMM", "oracle", "governance", "account abstraction", "cross-chain messaging", "key management", "supply chain", "other"],
            "root_cause_category": ["access control", "missing validation", "oracle manipulation", "share accounting", "rounding/precision", "signature replay", "reentrancy", "upgradeability/proxy issue", "bridge proof/message validation", "admin/private key compromise", "dependency/supply chain", "economic design flaw", "other"],
            "attacker_path": ["required permissions", "transaction sequence", "external dependencies", "assumptions"],
            "impact": ["stolen funds", "frozen funds", "minted unbacked assets", "governance/control compromise", "insolvency", "data/key compromise", "gas/efficiency only", "unclear"],
            "lesson_outputs": ["invariant", "code pattern", "Foundry/Slither/Echidna test", "false positives", "reportability proof", "severity/downgrade", "skill patch recommendation"],
        }

save_seen_state(seen_state)

jsonl = RUN_DIR / "learning-candidates.jsonl"
with jsonl.open("w", encoding="utf-8") as f:
    for rec in records:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

by_group: dict[str, int] = {}; statuses: dict[str, int] = {}; content_quality_counts: dict[str, int] = {}
for r in records:
    by_group[r.get("source_group", "unknown")] = by_group.get(r.get("source_group", "unknown"), 0) + 1
    statuses[r.get("local_processing_status", "unknown")] = statuses.get(r.get("local_processing_status", "unknown"), 0) + 1
    cq = r.get("content_quality") or ("not_fetched" if r.get("local_processing_status") != "fetched_content" else "unknown")
    content_quality_counts[cq] = content_quality_counts.get(cq, 0) + 1

summary = RUN_DIR / "learning-run-summary.md"
actual = content_quality_counts.get("actual_content", 0)
indexish = content_quality_counts.get("index_or_listing", 0)
summary.write_text(
    "# Argus Learning Ingestion Run Summary\n\n"
    f"- Run date: {datetime.now(timezone.utc).isoformat()}\n"
    f"- Config: `{CONFIG}`\n"
    f"- Registry schema/digest: `{REGISTRY.schema_version}` / `{REGISTRY.digest}`\n"
    f"- Operational cadence: `{RUN_CADENCE}`\n"
    f"- Selected static roots: `{len(selected_sources)}`\n"
    f"- Explicit source filter: `{','.join(sorted(SOURCE_FILTER)) if SOURCE_FILTER else 'none'}`\n"
    f"- Dry run: `{DRY}`\n"
    f"- Priority-only mode: `{PRIORITY_ONLY}`\n"
    f"- Include backfill / one-time sources: `{INCLUDE_BACKFILL}`\n"
    f"- Seen-state tracking: `{TRACK_SEEN_STATE}` (`{SEEN_STATE_PATH}`)\n"
    f"- Refetch seen URLs after days: `{REFETCH_SEEN_AFTER_DAYS}`\n"
    f"- Seen-state updates this run: `{seen_state_updates}`\n"
    f"- Max total seconds: `{MAX_TOTAL_SECONDS}`\n"
    f"- Max sources per group: `{MAX_SOURCES_PER_GROUP}`\n"
    f"- Max AppSec linked-resource fetches: `{MAX_APPSEC_LINK_FETCHES}`\n"
    f"- Max AppSec linked-resource records: `{MAX_APPSEC_LINK_RECORDS}`\n"
    f"- Max daily deep-link fetches: `{MAX_DAILY_DEEP_LINK_FETCHES}`\n"
    f"- Max backfill deep-link fetches: `{MAX_BACKFILL_DEEP_LINK_FETCHES}`\n"
    f"- Max backfill links per source: `{MAX_BACKFILL_LINKS_PER_SOURCE}`\n"
    f"- Max backfill crawl depth: `{MAX_BACKFILL_CRAWL_DEPTH}`\n"
    f"- Candidate file: `{jsonl}`\n"
    f"- Total candidate records: {len(records)}\n"
    f"- Actual content records: {actual}\n"
    f"- Index/listing metadata records: {indexish}\n\n"
    "## Source groups configured / processed\n\n" + "".join(f"- {k}: {v}\n" for k, v in sorted(by_group.items())) + "\n"
    "## Processing statuses\n\n" + "".join(f"- {k}: {v}\n" for k, v in sorted(statuses.items())) + "\n"
    "## Content quality\n\n" + "".join(f"- {k}: {v}\n" for k, v in sorted(content_quality_counts.items())) + "\n"
    "## Handling note\n\n"
    "- `daily` selects only explicitly daily roots; `weekly` reconciles daily+weekly roots; `backfill` selects only periodic/on-demand roots.\n"
    "- Source-specific refetch intervals and promotion policy come from registry schema v2; every compiler output remains proposal-only.\n"
    "- AppSec.fyi and blog/report roots are discovery sources; the compiler should learn from `fetched_content` deep pages, not topic/listing records.\n\n"
    "## Next step\n\n"
    "Run the learning compiler against `fetched_content` records only, then review `fetched_index_metadata` records for discovery gaps.\n",
    encoding="utf-8",
)

print(json.dumps({"records": len(records), "by_group": by_group, "statuses": statuses, "content_quality": content_quality_counts, "run_dir": str(RUN_DIR), "summary": str(summary), "jsonl": str(jsonl), "seen_state": str(SEEN_STATE_PATH), "seen_state_updates": seen_state_updates}, indent=2, sort_keys=True))
