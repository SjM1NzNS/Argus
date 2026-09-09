#!/usr/bin/env python3
"""Sanitize an already-exported HAR locally; no network activity."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

VERSION = "1.0.0"
REDACTED = "<REDACTED>"
SENSITIVE_NAME = re.compile(
    r"(?i)(authorization|proxy-authorization|cookie|set-cookie|api[-_]?key|token|"
    r"secret|password|passwd|csrf|xsrf|session|credential|private[-_]?key|client[-_]?secret)"
)
EMAIL_RE = re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![A-Za-z0-9.-])")
BEARER_RE = re.compile(r"(?i)\b(Bearer|Basic)\s+[A-Za-z0-9._~+/=-]{6,}")
JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
KEYLIKE_RE = re.compile(r"\b(?:AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|gh[pousr]_[A-Za-z0-9_]{20,255}|xox[baprs]-[0-9A-Za-z-]{10,255})\b")


def redact_text(value: str) -> str:
    value = BEARER_RE.sub(REDACTED, value)
    value = JWT_RE.sub(REDACTED, value)
    value = KEYLIKE_RE.sub(REDACTED, value)
    value = EMAIL_RE.sub("<REDACTED_EMAIL>", value)
    return value


def redact_url(value: str, captured: set[str]) -> str:
    try:
        parts = urlsplit(value)
        query = []
        for key, item in parse_qsl(parts.query, keep_blank_values=True):
            if SENSITIVE_NAME.search(key):
                if len(item) >= 6:
                    captured.add(item)
                item = REDACTED
            else:
                item = redact_text(item)
            query.append((key, item))
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
    except ValueError:
        return redact_text(value)


def scrub_named_value(name: str, value, captured: set[str]):
    if SENSITIVE_NAME.search(name):
        if isinstance(value, str) and len(value) >= 6:
            captured.add(value)
        return REDACTED
    return scrub_generic(value, captured)


def scrub_generic(value, captured: set[str]):
    if isinstance(value, dict):
        return {key: scrub_named_value(str(key), item, captured) for key, item in value.items()}
    if isinstance(value, list):
        return [scrub_generic(item, captured) for item in value]
    if isinstance(value, str):
        return redact_text(value)
    return value


def scrub_headers(headers, captured: set[str]):
    out = []
    for header in headers if isinstance(headers, list) else []:
        if not isinstance(header, dict):
            continue
        record = copy.deepcopy(header)
        name = str(record.get("name", ""))
        value = str(record.get("value", ""))
        if SENSITIVE_NAME.search(name):
            if len(value) >= 6:
                captured.add(value)
            record["value"] = REDACTED
        else:
            record["value"] = redact_text(value)
        out.append(record)
    return out


def scrub_cookies(cookies, captured: set[str]):
    out = []
    for cookie in cookies if isinstance(cookies, list) else []:
        if not isinstance(cookie, dict):
            continue
        record = copy.deepcopy(cookie)
        value = str(record.get("value", ""))
        if len(value) >= 6:
            captured.add(value)
        record["value"] = REDACTED
        out.append(record)
    return out


def scrub_params(params, captured: set[str]):
    out = []
    for param in params if isinstance(params, list) else []:
        if not isinstance(param, dict):
            continue
        record = copy.deepcopy(param)
        name = str(record.get("name", ""))
        value = str(record.get("value", ""))
        if SENSITIVE_NAME.search(name):
            if len(value) >= 6:
                captured.add(value)
            record["value"] = REDACTED
        else:
            record["value"] = redact_text(value)
        out.append(record)
    return out


def scrub_body_text(text: str, mime_type: str, captured: set[str]) -> str:
    if not isinstance(text, str):
        return text
    lower = (mime_type or "").lower()
    if "json" in lower or text.lstrip().startswith(("{", "[")):
        try:
            parsed = json.loads(text)
            return json.dumps(scrub_generic(parsed, captured), separators=(",", ":"), ensure_ascii=False)
        except json.JSONDecodeError:
            pass
    if "x-www-form-urlencoded" in lower:
        pairs = []
        for key, value in parse_qsl(text, keep_blank_values=True):
            if SENSITIVE_NAME.search(key):
                if len(value) >= 6:
                    captured.add(value)
                value = REDACTED
            else:
                value = redact_text(value)
            pairs.append((key, value))
        return urlencode(pairs)
    return redact_text(text)


def sanitize_entry(entry, captured: set[str]):
    out = copy.deepcopy(entry)
    request = out.get("request", {})
    if isinstance(request, dict):
        if isinstance(request.get("url"), str):
            request["url"] = redact_url(request["url"], captured)
        request["headers"] = scrub_headers(request.get("headers", []), captured)
        request["cookies"] = scrub_cookies(request.get("cookies", []), captured)
        request["queryString"] = scrub_params(request.get("queryString", []), captured)
        post = request.get("postData")
        if isinstance(post, dict):
            post["params"] = scrub_params(post.get("params", []), captured)
            if isinstance(post.get("text"), str):
                post["text"] = scrub_body_text(post["text"], str(post.get("mimeType", "")), captured)

    response = out.get("response", {})
    if isinstance(response, dict):
        response["headers"] = scrub_headers(response.get("headers", []), captured)
        response["cookies"] = scrub_cookies(response.get("cookies", []), captured)
        content = response.get("content")
        if isinstance(content, dict) and isinstance(content.get("text"), str):
            encoding = str(content.get("encoding", "")).lower()
            if encoding == "base64":
                raw = content["text"]
                if len(raw) >= 6:
                    captured.add(raw)
                content["text"] = REDACTED
                content["_argus_redaction"] = "base64_response_body_removed"
            else:
                content["text"] = scrub_body_text(content["text"], str(content.get("mimeType", "")), captured)

    messages = out.get("_webSocketMessages")
    if isinstance(messages, list):
        for message in messages:
            if isinstance(message, dict) and "data" in message:
                value = str(message.get("data", ""))
                if len(value) >= 6:
                    captured.add(value)
                message["data"] = REDACTED
                message["_argus_original_sha256"] = hashlib.sha256(value.encode("utf-8", "replace")).hexdigest()
                message["_argus_original_length"] = len(value)
    return out


def residual_scan(payload: str, captured: set[str]) -> list[str]:
    errors = []
    if BEARER_RE.search(payload):
        errors.append("bearer_or_basic_value")
    if JWT_RE.search(payload):
        errors.append("jwt_like_value")
    if KEYLIKE_RE.search(payload):
        errors.append("known_key_pattern")
    if EMAIL_RE.search(payload):
        errors.append("email_address")
    for value in sorted(captured, key=len, reverse=True):
        if value and value not in (REDACTED, "<REDACTED_EMAIL>") and value in payload:
            errors.append("captured_sensitive_value_remains")
            break
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    source = args.input.expanduser().resolve()
    if not source.is_file() or source.is_symlink():
        parser.error("input must be an existing non-symlink HAR file")
    raw = source.read_bytes()
    try:
        document = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: invalid HAR JSON: {exc}", file=sys.stderr)
        return 2
    entries = document.get("log", {}).get("entries") if isinstance(document, dict) else None
    if not isinstance(entries, list):
        print("ERROR: HAR has no log.entries array", file=sys.stderr)
        return 2

    captured: set[str] = set()
    sanitized = copy.deepcopy(document)
    sanitized["log"]["entries"] = [sanitize_entry(entry, captured) for entry in entries if isinstance(entry, dict)]
    sanitized["_argus_sanitization"] = {
        "tool": "sanitize_har.py",
        "tool_version": VERSION,
        "network_performed": False,
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "source_bytes": len(raw),
        "all_cookie_values_redacted": True,
        "websocket_payloads_removed": True,
    }
    payload = json.dumps(sanitized, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    errors = residual_scan(payload, captured)
    if errors:
        print(json.dumps({"status": "failed_closed", "residuals": errors}), file=sys.stderr)
        return 3

    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, stat.S_IRUSR | stat.S_IWUSR)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(payload)
    os.chmod(output, 0o600)
    print(json.dumps({
        "output": str(output),
        "entries": len(sanitized["log"]["entries"]),
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "sanitized_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "residual_errors": 0,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
