#!/usr/bin/env python3
"""Argus WordPress CVE intelligence digest.

Local adaptation of the wp-cve-intel workflow:
- Pull Patchstack's public WordPress high/critical database listing.
- Prefer plugin, non-admin/low-priv, high-impact classes.
- Write a local Argus Markdown + JSON digest.
- Do NOT run scanners, PoCs, Nuclei templates, or touch live targets.

This script intentionally uses only Python stdlib.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

PATCHSTACK_LISTING = "https://patchstack.com/database?severity=7,10&platform=wordpress"
UA = "ArgusWordPressCVEIntel/1.0 (+local digest; no scanning)"
VAULT = Path(os.environ.get("ARGUS_VAULT", str(Path.home() / "SecurityResearch"))).expanduser()
DEFAULT_OUT_ROOT = VAULT / "01 - Learning" / "Inbox"

HIGH_IMPACT_TERMS = {
    "account takeover": 35,
    "privilege escalation": 35,
    "authentication bypass": 35,
    "auth bypass": 35,
    "remote code execution": 35,
    "code execution": 35,
    "rce": 35,
    "object injection": 30,
    "sql injection": 30,
    "arbitrary file upload": 30,
    "arbitrary file read": 28,
    "arbitrary file deletion": 28,
    "path traversal": 25,
    "directory traversal": 25,
    "local file inclusion": 25,
    "server-side request forgery": 25,
    "ssrf": 25,
    "stored cross-site scripting": 18,
    "stored xss": 18,
    "broken access control": 18,
    "cross-site scripting": 10,
    "xss": 10,
}

LOW_PRIV_TERMS = [
    "unauthenticated",
    "subscriber",
    "contributor",
    "customer",
    "author",
    "low-priv",
    "low privilege",
]
ADMIN_ONLY_TERMS = ["administrator", "admin+", "admin only", "admin-only"]


@dataclass
class Candidate:
    title: str
    url: str
    component_type: str
    slug: str | None
    relative_time: str | None
    score: int
    reasons: list[str]
    cve: str | None = None
    cvss: str | None = None
    detail_title: str | None = None
    vuln_class: str | None = None
    action: str = "watch"


def fetch(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def strip_tags(s: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def unique(iterable: Iterable[str]) -> list[str]:
    seen = set()
    out = []
    for x in iterable:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def parse_listing(listing_html: str, base: str = "https://patchstack.com") -> list[Candidate]:
    hrefs = unique(re.findall(r'href="(/database/wordpress/(?:plugin|theme)/[^"]+/vulnerability/[^"]+)"', listing_html))
    candidates: list[Candidate] = []
    for href in hrefs:
        m = re.search(r"/database/wordpress/(plugin|theme)/([^/]+)/vulnerability/([^/?#]+)", href)
        if not m:
            continue
        component_type, slug, slug_title = m.groups()
        # Nearby table row text contains relative disclosure time + title.
        pos = listing_html.find(f'href="{href}"')
        start = max(0, pos - 900)
        end = min(len(listing_html), pos + 1800)
        snippet = strip_tags(listing_html[start:end])
        title = title_from_snippet(snippet, slug_title)
        relative_time = relative_time_from_snippet(snippet)
        score, reasons, vuln_class = score_candidate(title, component_type)
        url = urllib.parse.urljoin(base, href)
        candidates.append(
            Candidate(
                title=title,
                url=url,
                component_type=component_type,
                slug=slug,
                relative_time=relative_time,
                score=score,
                reasons=reasons,
                vuln_class=vuln_class,
            )
        )
    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates


def title_from_snippet(snippet: str, fallback_slug_title: str) -> str:
    # Prefer text after the relative-time marker: "2 minutes ago Backstage <=... vulnerability".
    rel = re.search(r"(?:Disclosed|\b\d+\s+(?:minute|minutes|hour|hours|day|days)\s+ago)\s+(.+? vulnerability)", snippet, re.I)
    if rel:
        title = rel.group(1).strip()
        # Cut off accidental table/control text after title.
        title = re.split(r"\s+(?:Details|Patchstack|CVSS|Risks|This vulnerability|Get started)\b", title, maxsplit=1)[0].strip()
        return title
    title = fallback_slug_title.replace("-", " ").strip()
    return title[:1].upper() + title[1:]


def relative_time_from_snippet(snippet: str) -> str | None:
    m = re.search(r"\b(\d+\s+(?:minute|minutes|hour|hours|day|days)\s+ago)\b", snippet, re.I)
    if m:
        return m.group(1)
    if "Disclosed" in snippet:
        return "Disclosed"
    return None


def score_candidate(title: str, component_type: str) -> tuple[int, list[str], str | None]:
    t = title.lower()
    score = 0
    reasons = []
    vuln_class = None
    if component_type == "plugin":
        score += 15
        reasons.append("plugin")
    else:
        score -= 10
        reasons.append("theme/deprioritized")
    if any(term in t for term in LOW_PRIV_TERMS):
        score += 30
        reasons.append("unauth/low-priv wording")
    if any(term in t for term in ADMIN_ONLY_TERMS) and not any(term in t for term in ["subscriber", "contributor", "unauthenticated", "customer"]):
        score -= 25
        reasons.append("admin-only wording risk")
    for term, value in HIGH_IMPACT_TERMS.items():
        if term in t:
            score += value
            reasons.append(term)
            vuln_class = term
            break
    if "vulnerability" in t:
        score += 5
    if score >= 75:
        action = "reverse-first"
    elif score >= 45:
        action = "review"
    else:
        action = "watch"
    return score, reasons + [f"action:{action}"], vuln_class


def enrich_detail(candidate: Candidate, delay: float = 0.5) -> Candidate:
    time.sleep(delay)
    try:
        body = fetch(candidate.url, timeout=20)
    except Exception as exc:  # noqa: BLE001
        candidate.reasons.append(f"detail_fetch_failed:{type(exc).__name__}")
        return candidate
    title_m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
    if title_m:
        candidate.detail_title = html.unescape(strip_tags(title_m.group(1)))
    cve = re.search(r"\bCVE-\d{4}-\d{4,7}\b", body)
    if cve:
        candidate.cve = cve.group(0)
    cvss = re.search(r"\bCVSS\s+([0-9](?:\.\d)?)\b", strip_tags(body), re.I)
    if cvss:
        candidate.cvss = cvss.group(1)
    return candidate


def action_from_score(score: int) -> str:
    if score >= 75:
        return "reverse-first"
    if score >= 45:
        return "review"
    return "watch"


def write_outputs(candidates: list[Candidate], out_dir: Path, source_url: str, dry_run: bool = False) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now().astimezone()
    for c in candidates:
        c.action = action_from_score(c.score)
    data = {
        "generated_at": now.isoformat(),
        "source_url": source_url,
        "mode": "dry_run" if dry_run else "live_public_listing_fetch",
        "safety": {
            "target_contact": False,
            "scanner_execution": False,
            "poc_execution": False,
            "upstream_writes": False,
        },
        "candidates": [asdict(c) for c in candidates],
    }
    json_path = out_dir / "wordpress-cve-intel-digest.json"
    md_path = out_dir / "wordpress-cve-intel-digest.md"
    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    md_path.write_text(render_markdown(data), encoding="utf-8")
    return md_path, json_path


def render_markdown(data: dict) -> str:
    rows = data["candidates"]
    lines = [
        "---",
        "type: wordpress-cve-intel-digest",
        f"generated_at: \"{data['generated_at']}\"",
        f"source: \"{data['source_url']}\"",
        f"mode: \"{data['mode']}\"",
        "---",
        "",
        "# WordPress CVE Intelligence Digest",
        "",
        "Local Argus adaptation of `nahamsec/wp-cve-intel`. This digest is lead generation only.",
        "",
        "Safety invariants: no target contact, no scanner execution, no PoC execution, no upstream writes.",
        "",
        "## Priority candidates",
        "",
        "| Rank | Action | Score | Candidate | CVE | CVSS | Age | Reasons |",
        "|---:|---|---:|---|---|---|---|---|",
    ]
    for i, c in enumerate(rows, 1):
        title = c["title"].replace("|", "\\|")
        link = f"[{title}]({c['url']})"
        reasons = ", ".join(c.get("reasons") or []).replace("|", "\\|")
        lines.append(
            f"| {i} | {c['action']} | {c['score']} | {link} | {c.get('cve') or ''} | {c.get('cvss') or ''} | {c.get('relative_time') or ''} | {reasons} |"
        )
    lines += [
        "",
        "## Handling rules",
        "",
        "- `reverse-first`: worth manual advisory/detail review and local-lab reproduction planning.",
        "- `review`: keep as a watch item; promote only if an active in-scope WordPress surface intersects.",
        "- `watch`: low priority unless target inventory later matches the plugin/theme.",
        "- Do not run Nuclei/WPScan/public PoCs from this digest against live targets without explicit approval and scope contract review.",
        "- Route any intersecting target lead through `02 - Vulnerability Playbooks/Web2/WordPress CVE Intelligence/overview.md` plus the relevant primitive playbook.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--url", default=PATCHSTACK_LISTING)
    ap.add_argument("--max-candidates", type=int, default=int(os.environ.get("ARGUS_WP_CVE_MAX", "10")))
    ap.add_argument("--enrich", type=int, default=int(os.environ.get("ARGUS_WP_CVE_ENRICH", "5")), help="fetch detail pages for top N")
    ap.add_argument("--run-label", default=os.environ.get("ARGUS_RUN_LABEL"))
    ap.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    run_label = args.run_label or "wordpress-cve-intel-" + dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = Path(args.out_root) / run_label

    if args.dry_run:
        sample = """
        <a href="/database/wordpress/plugin/example/vulnerability/wordpress-example-plugin-1-0-unauthenticated-sql-injection-vulnerability">1 minute ago Example <= 1.0 Unauthenticated SQL Injection vulnerability</a>
        <a href="/database/wordpress/theme/theme/vulnerability/wordpress-theme-1-0-reflected-cross-site-scripting-xss-vulnerability">2 days ago Theme <= 1.0 Reflected Cross-Site Scripting XSS vulnerability</a>
        """
        candidates = parse_listing(sample)
    else:
        listing = fetch(args.url)
        candidates = parse_listing(listing)

    candidates = candidates[: max(1, args.max_candidates)]
    enrich_n = 0 if args.dry_run else max(0, min(args.enrich, len(candidates)))
    for i in range(enrich_n):
        candidates[i] = enrich_detail(candidates[i])

    md, js = write_outputs(candidates, out_dir, args.url, args.dry_run)
    print(json.dumps({"ok": True, "count": len(candidates), "markdown": str(md), "json": str(js)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
