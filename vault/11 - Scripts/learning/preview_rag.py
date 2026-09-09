#!/usr/bin/env python3
"""Argus wrapper for preview.is RAG Search API.

Usage:
  argus-preview-rag --health
  argus-preview-rag "CSP strict-dynamic bypass real bug bounty writeup" --save

Reads PREVIEW_IS_API_KEY or PREVIEW_RAG_API_KEY from the environment or ~/.config/argus/preview-is.env.
Never prints the API key.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import sys
import textwrap
import urllib.error
import urllib.request

API_BASE = "https://api.preview.is"
DEFAULT_ENV = Path(os.environ.get("ARGUS_PREVIEW_ENV", str(Path.home() / ".config/argus/preview-is.env"))).expanduser()
VAULT = Path(os.environ.get("ARGUS_VAULT", str(Path.home() / "SecurityResearch"))).expanduser()
DEFAULT_INBOX_ROOT = VAULT / "01 - Learning" / "Inbox"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def api_key(env_path: Path) -> str | None:
    load_env_file(env_path)
    # preview.is site/Codex setup uses PREVIEW_RAG_API_KEY; the original
    # Argus wrapper used PREVIEW_IS_API_KEY. Accept both for compatibility,
    # preferring the wrapper-specific name when both are present.
    for name in ("PREVIEW_IS_API_KEY", "PREVIEW_RAG_API_KEY"):
        key = os.environ.get(name)
        if key:
            return key.strip()
    return None


def request_json(url: str, method: str = "GET", body: dict | None = None, key: str | None = None) -> tuple[int, dict, dict]:
    data = None
    headers = {"User-Agent": "Argus preview-rag/1.0"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if key:
        headers["X-API-Key"] = key
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8", "replace")
            parsed = json.loads(raw) if raw else {}
            return resp.status, dict(resp.headers), parsed
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            parsed = json.loads(raw) if raw else {"detail": raw}
        except json.JSONDecodeError:
            parsed = {"detail": raw}
        return e.code, dict(e.headers), parsed


def summarize_result(result: dict, max_chars: int = 700) -> str:
    title = result.get("title") or "(untitled)"
    url = result.get("url") or ""
    score = result.get("score")
    sections = result.get("matched_sections") or []
    lines = [f"## {title}"]
    if url:
        lines.append(f"Source: {url}")
    if score is not None:
        lines.append(f"Score: {score}")
    for sec in sections[:3]:
        heading = sec.get("heading") or "Matched section"
        text = (sec.get("text") or "").strip().replace("\r", "")
        if len(text) > max_chars:
            text = text[:max_chars].rstrip() + "…"
        lines.append(f"\n### {heading}\n{text}")
    return "\n".join(lines).strip()


def save_results(query: str, payload: dict, inbox_root: Path = DEFAULT_INBOX_ROOT) -> Path:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("manual-preview-is-%Y%m%d-%H%M%S")
    out = inbox_root / stamp
    out.mkdir(parents=True, exist_ok=True)
    safe_payload = json.loads(json.dumps(payload))
    (out / "preview-is-results.json").write_text(json.dumps(safe_payload, indent=2, ensure_ascii=False))
    md = ["---", "type: external-rag-results", "source: preview.is", f"fetched_at: \"{dt.datetime.now(dt.timezone.utc).isoformat()}\"", "---", "", f"# preview.is results — {query}", "", "Policy: `00 - System/external-rag-source-policy.md`", ""]
    for result in payload.get("results", []):
        md.append(summarize_result(result))
        md.append("")
    (out / "preview-is-results.md").write_text("\n".join(md).rstrip() + "\n")
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Query preview.is RAG Search API safely for Argus learning/reference.")
    p.add_argument("query", nargs="?", help="Natural-language security technique query")
    p.add_argument("--k", type=int, default=5, help="Number of parent articles to return (default: 5)")
    p.add_argument("--candidates", type=int, default=80, help="Chunks retrieved before ranking (default: 80)")
    p.add_argument("--min-score", type=float, default=0.1, help="Minimum relevance score (default: 0.1)")
    p.add_argument("--full-content", action="store_true", help="Request full markdown content where enabled")
    p.add_argument("--save", action="store_true", help="Save JSON and markdown result summary into the learning inbox")
    p.add_argument("--json", action="store_true", help="Print raw JSON response")
    p.add_argument("--health", action="store_true", help="Check API health; does not require an API key")
    p.add_argument("--env", default=str(DEFAULT_ENV), help=f"Env file path (default: {DEFAULT_ENV})")
    args = p.parse_args()

    if args.health:
        status, headers, payload = request_json(f"{API_BASE}/health")
        print(json.dumps({"status_code": status, "response": payload}, indent=2))
        return 0 if status == 200 else 1

    if not args.query:
        p.error("query is required unless --health is used")

    key = api_key(Path(args.env))
    if not key:
        print(textwrap.dedent(f"""
        Missing preview.is API key.

        Add it to the environment or to:
          {args.env}

        Example file content:
          PREVIEW_RAG_API_KEY=rk_your_key

        Backward-compatible alias also supported:
          PREVIEW_IS_API_KEY=rk_your_key

        Then secure it:
          chmod 600 {args.env}
        """).strip(), file=sys.stderr)
        return 2

    body = {
        "query": args.query,
        "k": args.k,
        "candidates": args.candidates,
        "min_score": args.min_score,
        "full_content": bool(args.full_content),
    }
    status, headers, payload = request_json(f"{API_BASE}/search", method="POST", body=body, key=key)
    if status != 200:
        print(json.dumps({"status_code": status, "response": payload}, indent=2), file=sys.stderr)
        return 1

    if args.save:
        out = save_results(args.query, payload)
        print(f"Saved results to: {out}")

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"Query: {payload.get('query', args.query)}")
        print(f"Count: {payload.get('count', len(payload.get('results', [])))}")
        print()
        for i, result in enumerate(payload.get("results", []), 1):
            print(summarize_result(result))
            if i != len(payload.get("results", [])):
                print("\n" + "-" * 80 + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
