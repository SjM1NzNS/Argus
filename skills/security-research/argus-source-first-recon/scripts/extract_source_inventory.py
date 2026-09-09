#!/usr/bin/env python3
"""Local-only deterministic JS/source artifact inventory for Argus.

No networking, code execution, dependency installation, or secret validation.
Candidate secret values are never emitted.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import stat
import sys
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qsl, quote, urlsplit, urlunsplit

VERSION = "1.1.2"
TEXT_EXTENSIONS = {
    ".html", ".htm", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx",
    ".json", ".map", ".css", ".txt", ".xml", ".yml", ".yaml",
}
URL_RE = re.compile(r"https?://[^\s\"'<>`\\)\]]+")
ROUTE_RE = re.compile(
    r"(?<![A-Za-z0-9])(/(?:api|v[0-9]+|graphql|auth|oauth|admin|internal|upload|"
    r"download|export|import|users?|accounts?|organizations?|projects?|sessions?|jobs?)"
    r"(?:/[A-Za-z0-9_{}:$.*+?=,@%~-]+)*)"
)
METHOD_ROUTE_RE = re.compile(
    r"\b(GET|POST|PUT|PATCH|DELETE|OPTIONS|HEAD)\b.{0,100}?"
    r"(/(?:[A-Za-z0-9_{}:$.*+?=,@%~-]+/?)+)", re.IGNORECASE
)
SOURCEMAP_RE = re.compile(r"sourceMappingURL\s*=\s*([^\s*]+)")
ASSET_REFERENCE_RE = re.compile(
    r'''(?P<quote>["'`])(?P<value>(?:(?:https?://[^/"'`\s]+)?/assets/|assets/|\./|\.\./)'''
    r'''[^"'`\s)]+?\.(?:js|mjs|cjs|css|json|wasm)(?:[?#][^"'`\s)]*)?)(?P=quote)''',
    re.IGNORECASE,
)
DYNAMIC_IMPORT_RE = re.compile(
    r'''\bimport\s*\(\s*(?P<quote>["'`])(?P<value>[^"'`\s)]+?\.(?:js|mjs|cjs|css|json|wasm)'''
    r'''(?:[?#][^"'`\s)]*)?)(?P=quote)\s*\)''',
    re.IGNORECASE,
)
AUTH_RE = re.compile(
    r"(?i)\b(authorization|bearer|cookie|set-cookie|csrf|xsrf|access[_-]?token|"
    r"refresh[_-]?token|id[_-]?token|session[_-]?(?:id|token)?|api[_-]?key|"
    r"credentials\s*:\s*['\"]include['\"]|localStorage|sessionStorage)\b"
)
SELECTOR_RE = re.compile(
    r"(?i)\b(user_?id|account_?id|tenant_?id|org(?:anization)?_?id|project_?id|"
    r"workspace_?id|session_?id|object_?id|resource_?id|owner_?id|role_?id|"
    r"team_?id|group_?id|customer_?id|file_?id|job_?id)\b"
)
WORKFLOW_RE = re.compile(
    r"(?i)\b(upload|download|export|import|invite|approve|reject|publish|unpublish|"
    r"delete|remove|create|update|submit|execute|run|trigger|cancel|reset|impersonate)\b"
)
FEATURE_RE = re.compile(
    r"(?i)\b(feature[_-]?flags?|experiments?|environment|env(?:ironment)?[_-]?name|"
    r"release[_-]?channel|debug|staging|production|development|beta|canary)\b"
)
SINK_RE = re.compile(
    r"(?i)\b(innerHTML|outerHTML|insertAdjacentHTML|document\.write|eval|Function|"
    r"setTimeout|setInterval|child_process|execFile|exec|spawn|system|shell|"
    r"dangerouslySetInnerHTML|postMessage|WebSocket|fetch|XMLHttpRequest)\b"
)
SECRET_PATTERNS = [
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,255}\b")),
    ("slack_token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,255}\b")),
    ("jwt_like", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")),
    ("named_secret", re.compile(
        r"(?i)(?:api[_-]?key|secret|password|passwd|token|client[_-]?secret)"
        r"\s*[=:]\s*['\"]([^'\"\r\n]{8,512})['\"]"
    )),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.name


def iter_files(input_path: Path, max_files: int) -> tuple[list[Path], list[str]]:
    skipped: list[str] = []
    if input_path.is_symlink():
        return [], [f"symlink_input:{input_path}"]
    if input_path.is_file():
        return [input_path], skipped
    files: list[Path] = []
    for path in sorted(input_path.rglob("*"), key=lambda p: p.as_posix()):
        if path.is_symlink():
            skipped.append(f"symlink:{safe_rel(path, input_path)}")
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            files.append(path)
            if len(files) >= max_files:
                skipped.append(f"max_files_reached:{max_files}")
                break
    return files, skipped


def line_number(text: str, start: int) -> int:
    return text.count("\n", 0, start) + 1


def add_matches(bucket: list[dict], regex: re.Pattern, text: str, source: str,
                value_group: int | None = None, transform=None) -> None:
    for match in regex.finditer(text):
        value = match.group(value_group) if value_group is not None else match.group(0)
        if transform:
            value = transform(value)
        bucket.append({"source": source, "line": line_number(text, match.start()), "value": value})


def sanitize_url(value: str) -> str:
    """Retain URL topology while removing userinfo and query/fragment capabilities.

    JavaScript bundles can contain URL-like strings with invalid bracket/port syntax.
    Treat those as opaque redacted candidates instead of aborting the entire inventory.
    """
    cleaned = html.unescape(value.rstrip(".,;:"))
    malformed = (
        f"<MALFORMED_URL len={len(cleaned)} "
        f"sha256={hashlib.sha256(cleaned.encode()).hexdigest()[:12]}>"
    )
    try:
        parts = urlsplit(cleaned)
        host = parts.hostname or ""
        port = parts.port
    except ValueError:
        return malformed
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    netloc = host
    if port:
        netloc = f"{host}:{port}"
    query = "&".join(
        f"{quote(key, safe='[]')}=<REDACTED>"
        for key, _ in parse_qsl(parts.query, keep_blank_values=True)
    )
    fragment = "<REDACTED>" if parts.fragment else ""
    return urlunsplit((parts.scheme, netloc, parts.path, query, fragment))


def scan_text(text: str, source: str) -> dict:
    result = {
        "urls": [], "routes": [], "method_routes": [], "source_map_references": [],
        "asset_references": [], "auth_signals": [], "object_selectors": [],
        "workflow_signals": [], "feature_signals": [], "sink_signals": [],
        "secret_candidates": [],
    }
    add_matches(result["urls"], URL_RE, text, source, transform=sanitize_url)
    add_matches(result["routes"], ROUTE_RE, text, source, value_group=1)
    for match in METHOD_ROUTE_RE.finditer(text):
        result["method_routes"].append({
            "source": source,
            "line": line_number(text, match.start()),
            "method": match.group(1).upper(),
            "route": match.group(2),
        })
    add_matches(result["source_map_references"], SOURCEMAP_RE, text, source, value_group=1)
    for kind, regex in (
        ("static_asset", ASSET_REFERENCE_RE),
        ("dynamic_import", DYNAMIC_IMPORT_RE),
    ):
        for match in regex.finditer(text):
            result["asset_references"].append({
                "source": source,
                "line": line_number(text, match.start()),
                "kind": kind,
                "value": match.group("value"),
            })
    for name, regex in (
        ("auth_signals", AUTH_RE), ("object_selectors", SELECTOR_RE),
        ("workflow_signals", WORKFLOW_RE), ("feature_signals", FEATURE_RE),
        ("sink_signals", SINK_RE),
    ):
        for match in regex.finditer(text):
            result[name].append({
                "source": source,
                "line": line_number(text, match.start()),
                "value": match.group(0),
            })
    for kind, regex in SECRET_PATTERNS:
        for match in regex.finditer(text):
            value = match.group(1) if match.lastindex else match.group(0)
            result["secret_candidates"].append({
                "source": source,
                "line": line_number(text, match.start()),
                "type": kind,
                "length": len(value),
                "sha256_prefix": sha256_bytes(value.encode("utf-8", "replace"))[:16],
                "value": "<REDACTED>",
            })
    return result


def valid_source_map(obj) -> bool:
    return (
        isinstance(obj, dict)
        and isinstance(obj.get("version"), int)
        and isinstance(obj.get("sources"), list)
        and (isinstance(obj.get("mappings"), str) or isinstance(obj.get("sourcesContent"), list))
    )


def dedupe(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for item in sorted(items, key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False)):
        key = json.dumps(item, sort_keys=True, ensure_ascii=False)
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-files", type=int, default=5000)
    parser.add_argument("--max-file-bytes", type=int, default=20 * 1024 * 1024)
    args = parser.parse_args()

    source = args.input.expanduser().resolve()
    if not source.exists():
        parser.error(f"input does not exist: {source}")
    files, skipped = iter_files(source, args.max_files)
    root = source if source.is_dir() else source.parent
    inventory = {
        "schema_version": 1,
        "tool": "extract_source_inventory.py",
        "tool_version": VERSION,
        "input_root": str(source),
        "network_performed": False,
        "files": [],
        "source_maps": [],
        "findings": {k: [] for k in scan_text("", "")},
        "skipped": skipped,
    }

    for path in files:
        rel = safe_rel(path, root)
        data = path.read_bytes()
        file_record = {"path": rel, "bytes": len(data), "sha256": sha256_bytes(data)}
        if len(data) > args.max_file_bytes:
            file_record["status"] = "skipped_too_large"
            inventory["files"].append(file_record)
            continue
        text = data.decode("utf-8", "replace")
        file_record["status"] = "scanned"
        inventory["files"].append(file_record)
        scanned = scan_text(text, rel)
        for key, values in scanned.items():
            inventory["findings"][key].extend(values)

        if path.suffix.lower() == ".map":
            map_record = {"path": rel, "valid": False, "sources": [], "embedded_sources": 0}
            try:
                obj = json.loads(text)
                map_record["valid"] = valid_source_map(obj)
                if map_record["valid"]:
                    sources = obj.get("sources", [])
                    contents = obj.get("sourcesContent", [])
                    map_record["sources"] = [str(s) for s in sources]
                    for idx, content in enumerate(contents if isinstance(contents, list) else []):
                        if not isinstance(content, str):
                            continue
                        map_record["embedded_sources"] += 1
                        label = f"{rel}::sourcesContent[{idx}]::{sources[idx] if idx < len(sources) else 'unknown'}"
                        embedded = scan_text(content, label)
                        for key, values in embedded.items():
                            inventory["findings"][key].extend(values)
                else:
                    map_record["reason"] = "missing_structural_source_map_fields"
            except json.JSONDecodeError as exc:
                map_record["reason"] = f"invalid_json:{exc.msg}"
            inventory["source_maps"].append(map_record)

    inventory["files"] = sorted(inventory["files"], key=lambda x: x["path"])
    inventory["source_maps"] = sorted(inventory["source_maps"], key=lambda x: x["path"])
    for key in inventory["findings"]:
        inventory["findings"][key] = dedupe(inventory["findings"][key])
    inventory["summary"] = {
        "files_seen": len(inventory["files"]),
        "files_scanned": sum(1 for x in inventory["files"] if x["status"] == "scanned"),
        "valid_source_maps": sum(1 for x in inventory["source_maps"] if x["valid"]),
        "candidate_counts": {k: len(v) for k, v in inventory["findings"].items()},
    }

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(inventory, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRUSR | stat.S_IWUSR)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(payload)
    os.chmod(output, 0o600)
    print(json.dumps({"output": str(output), **inventory["summary"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
