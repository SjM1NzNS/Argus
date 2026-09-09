#!/usr/bin/env python3
"""Shared canonicalization and locked/atomic JSON state helpers for Argus learning."""
from __future__ import annotations

import copy
import fcntl
import hashlib
import hmac
import json
import os
import socket
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Iterator
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from network_policy import is_strict_public_ip

TRACKING_KEYS = {"fbclid", "gclid", "dclid", "msclkid", "mc_cid", "mc_eid"}


def canonical_url(url: str) -> str:
    value = (url or "").strip()
    if not value:
        return ""
    parts = urlsplit(value)
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").lower()
    port = parts.port
    rendered_host = f"[{host}]" if ":" in host else host
    if port and not ((scheme == "https" and port == 443) or (scheme == "http" and port == 80)):
        netloc = f"{rendered_host}:{port}"
    else:
        netloc = rendered_host
    if parts.username or parts.password:
        # Preserve the original authority for validation to reject; canonicalization
        # is not a credential-stripping security boundary.
        netloc = parts.netloc.lower()
    path = parts.path or "/"
    if path != "/":
        path = path.rstrip("/")
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in TRACKING_KEYS
    ]
    query.sort()
    return urlunsplit((scheme, netloc, path, urlencode(query, doseq=True), ""))


def url_identity_key(path: str | Path | None = None) -> bytes:
    target = Path(
        path
        or os.environ.get("ARGUS_URL_IDENTITY_KEY")
        or os.environ.get("ARGUS_BROWSER_URL_IDENTITY_KEY")
        or (Path.home() / ".config/argus/url-identity.key")
    ).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    os.chmod(target.parent, 0o700)
    try:
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        pass
    else:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(os.urandom(32))
    os.chmod(target, 0o600)
    key = target.read_bytes()
    if len(key) < 32:
        raise RuntimeError("learning URL identity key is invalid")
    return key


def url_identity(url: str, *, key: bytes | None = None) -> str:
    digest = hmac.new(key or url_identity_key(), url.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"hmac-sha256:{digest}"


def is_public_http_url(url: str, *, resolve: bool = False) -> bool:
    """Reject credentialed, localhost, and non-global IP destinations.

    With ``resolve=True`` every current A/AAAA answer must be globally routable.
    This is an egress guard for browser navigation, not an authorization decision.
    """
    try:
        parts = urlsplit(url)
        if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
            return False
        if parts.username or parts.password:
            return False
        host = parts.hostname.lower()
        if host in {"localhost", "localhost.localdomain"} or host.endswith(".localhost"):
            return False
        try:
            literal = socket.inet_pton(socket.AF_INET, host)
            if not is_strict_public_ip(socket.inet_ntop(socket.AF_INET, literal)):
                return False
        except OSError:
            try:
                literal = socket.inet_pton(socket.AF_INET6, host)
                if not is_strict_public_ip(socket.inet_ntop(socket.AF_INET6, literal)):
                    return False
            except OSError:
                if resolve:
                    answers = socket.getaddrinfo(
                        host,
                        parts.port or (443 if parts.scheme.lower() == "https" else 80),
                        type=socket.SOCK_STREAM,
                    )
                    addresses = {answer[4][0] for answer in answers}
                    if not addresses or any(not is_strict_public_ip(address) for address in addresses):
                        return False
        return True
    except (ValueError, OSError, socket.gaierror):
        return False


@contextmanager
def _locked(path: Path) -> Iterator[None]:
    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _read_or_quarantine(path: Path, default: dict, warn: Callable[[str], None] | None) -> dict:
    if not path.exists():
        return copy.deepcopy(default)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("state root must be a mapping")
        return value
    except Exception as exc:
        quarantine = path.with_name(f"{path.name}.corrupt-{time.time_ns()}")
        path.replace(quarantine)
        if warn:
            warn(f"Quarantined corrupt learning state {path} as {quarantine}: {type(exc).__name__}: {exc}")
        return copy.deepcopy(default)


def load_json_state(path: str | Path, *, default: dict, warn: Callable[[str], None] | None = print) -> dict:
    target = Path(path).expanduser()
    with _locked(target):
        return _read_or_quarantine(target, default, warn)


def _timestamp(entry: dict) -> datetime | None:
    for key in (
        "last_checked_at",
        "last_checked",
        "last_seen",
        "last_success_at",
        "updated_at",
        "retrieved_at",
    ):
        raw = entry.get(key)
        if not raw:
            continue
        try:
            parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            if parsed.tzinfo is None or parsed.utcoffset() is None:
                return parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except Exception:
            continue
    return None


def migrate_seen_url_state(
    path: str | Path,
    *,
    key: bytes | None = None,
    warn: Callable[[str], None] | None = print,
) -> dict:
    """Atomically replace legacy raw URL keys with shared HMAC identities."""
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    with _locked(target):
        current = _read_or_quarantine(target, {"urls": {}}, warn)
        urls = current.get("urls") if isinstance(current.get("urls"), dict) else {}
        raw_keys = [item for item in urls if not str(item).startswith("hmac-sha256:")]
        top_level_raw_keys = [
            item
            for item in current
            if str(item).lower().startswith(("http://", "https://"))
        ]
        if not raw_keys and not top_level_raw_keys:
            current["url_identity_scheme"] = "hmac-sha256"
            return current

        identity_key = key or url_identity_key()
        migrated: dict[str, dict] = {}
        all_entries = list(urls.items()) + [
            (raw_key, current[raw_key]) for raw_key in top_level_raw_keys
        ]
        for raw_key, value in all_entries:
            identity = str(raw_key)
            if not identity.startswith("hmac-sha256:"):
                canonical_identity_url = canonical_url(identity)
                identity = url_identity(canonical_identity_url or identity, key=identity_key)
            incoming = copy.deepcopy(value) if isinstance(value, dict) else {"legacy_value_present": True}
            previous = migrated.get(identity)
            if previous is None:
                migrated[identity] = incoming
            else:
                old_ts, new_ts = _timestamp(previous), _timestamp(incoming)
                migrated[identity] = (
                    {**incoming, **previous}
                    if old_ts is not None and (new_ts is None or old_ts > new_ts)
                    else {**previous, **incoming}
                )

        for raw_key in top_level_raw_keys:
            current.pop(raw_key, None)
        current["urls"] = migrated
        current["url_identity_scheme"] = "hmac-sha256"
        current["url_identity_migrated_count"] = len(raw_keys) + len(top_level_raw_keys)
        current["url_identity_migrated_at"] = datetime.now().astimezone().isoformat()
        current["updated_at"] = current["url_identity_migrated_at"]
        fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(current, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, target)
            os.chmod(target, 0o600)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
        return current


def _merge_mapping(current: dict, incoming: dict) -> dict:
    result = copy.deepcopy(current)
    for key, value in incoming.items():
        if key in {"urls", "sources"} and isinstance(value, dict):
            bucket = result.setdefault(key, {})
            if not isinstance(bucket, dict):
                bucket = result[key] = {}
            for item_key, item_value in value.items():
                if not isinstance(item_value, dict) or not isinstance(bucket.get(item_key), dict):
                    bucket[item_key] = copy.deepcopy(item_value)
                    continue
                old = bucket[item_key]
                old_ts, new_ts = _timestamp(old), _timestamp(item_value)
                if old_ts is not None and (new_ts is None or old_ts > new_ts):
                    bucket[item_key] = {**item_value, **old}
                else:
                    bucket[item_key] = {**old, **item_value}
        elif isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge_mapping(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def write_json_atomic(path: str | Path, data: dict) -> None:
    """Replace a JSON document under an exclusive lock using a unique temp file."""
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    with _locked(target):
        fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(data, handle, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, target)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)


def merge_json_state(
    path: str | Path,
    updates: dict,
    *,
    default: dict | None = None,
    warn: Callable[[str], None] | None = print,
) -> dict:
    """Lock, re-read, merge, and atomically replace JSON state.

    This prevents static/browser/manual runs from overwriting each other's URL or
    source-health updates when they overlap.
    """
    target = Path(path).expanduser()
    target.parent.mkdir(parents=True, exist_ok=True)
    with _locked(target):
        current = _read_or_quarantine(target, default or {}, warn)
        merged = _merge_mapping(current, updates)
        merged["updated_at"] = datetime.now().astimezone().isoformat()
        fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(merged, handle, ensure_ascii=False, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, target)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)
        return merged
