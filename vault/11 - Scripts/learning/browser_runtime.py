#!/usr/bin/env python3
"""Shared safety, isolation, waiting, and evidence primitives for Argus browsers.

The module intentionally keeps Playwright imports lazy. Pure policy and evidence
helpers can therefore be tested without launching a browser, while production
callers use the same URL and redaction boundaries.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import parse_qsl, quote, unquote, urlencode, urlsplit, urlunsplit

from learning_state import is_public_http_url, url_identity
from network_policy import validate_loopback_http_proxy_url

SENSITIVE_HEADER_RE = re.compile(
    r"(?:authorization|proxy-authorization|cookie|set-cookie|csrf|xsrf|api[-_]?key|token|secret|session)",
    re.I,
)
TRACKER_HOST_RE = re.compile(
    r"(?:^|\.)(?:doubleclick\.net|googletagmanager\.com|google-analytics\.com|analytics\.google\.com|hotjar\.com|plausible\.io|matomo\.cloud|licdn\.com|linkedin\.com|redditstatic\.com|reddit\.com|ads-twitter\.com|facebook\.net|facebook\.com)$",
    re.I,
)
SOURCE_ARTIFACT_PATH_RE = re.compile(
    r"(?:^|/)(?:api|graphql|rest|wp-json)(?:/|$)|(?:config|manifest|routes?|endpoints?)\.(?:json|js)$|\.(?:json|map)$",
    re.I,
)
OPAQUE_VALUE_RE = re.compile(
    r"^(?:sk_(?:live|test)_[A-Za-z0-9_-]{12,}|AKIA[A-Z0-9]{16}|eyJ[A-Za-z0-9_-]{12,}|[0-9a-fA-F]{24,}|[A-Za-z0-9_-]{40,})$"
)
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")
CAPABILITY_PATH_LABELS = {
    "activate",
    "activation",
    "auth",
    "confirm",
    "invite",
    "magic",
    "mfa",
    "otp",
    "password",
    "recovery",
    "reset",
    "token",
    "verify",
}
CAPABILITY_SEGMENT_RE = re.compile(r"^[A-Za-z0-9._~-]{16,}$")
MAX_EVIDENCE_URL_BYTES = 4096
MAX_HEADER_COUNT = 64
MAX_HEADER_NAME_CHARS = 128
MAX_HEADER_VALUE_CHARS = 1024
MAX_EVENT_BYTES = 16 * 1024
MAX_EVIDENCE_BYTES = 2 * 1024 * 1024
MAX_BLOCKED_REQUESTS = 200
SAFE_HEADER_VALUES = {
    "accept",
    "accept-language",
    "cache-control",
    "content-length",
    "content-type",
    "origin",
    "referer",
    "sec-fetch-dest",
    "sec-fetch-mode",
    "sec-fetch-site",
    "user-agent",
    "x-request-id",
    "x-correlation-id",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_tracker_url(url: str) -> bool:
    try:
        return bool(TRACKER_HOST_RE.search((urlsplit(url).hostname or "").lower()))
    except (TypeError, ValueError):
        return False


def _fully_unquote(value: str, rounds: int = 3) -> str:
    decoded = value or ""
    for _ in range(max(1, rounds)):
        candidate = unquote(decoded)
        if candidate == decoded:
            break
        decoded = candidate
    return decoded


def _redact_opaque(value: str, *, capability_context: bool = False) -> str:
    decoded = _fully_unquote(value or "")
    if OPAQUE_VALUE_RE.fullmatch(decoded) or UUID_RE.fullmatch(decoded):
        return "<REDACTED>"
    if capability_context and decoded:
        return "<REDACTED>"
    if len(decoded) >= 20:
        classes = sum(
            bool(pattern.search(decoded))
            for pattern in (re.compile(r"[a-z]"), re.compile(r"[A-Z]"), re.compile(r"[0-9]"), re.compile(r"[-_~.]"))
        )
        if classes >= 2 and " " not in decoded:
            return "<REDACTED>"
    return value


def _bounded_evidence_url(value: str, *, scheme: str, netloc: str) -> str:
    if len(value.encode("utf-8", "replace")) <= MAX_EVIDENCE_URL_BYTES:
        return value
    return urlunsplit((scheme, netloc, "/<REDACTED_OVERSIZED_URL>", "", ""))


def sanitize_url_for_evidence(url: str) -> str:
    """Remove capability material and return a bounded, syntactically valid URL."""
    try:
        parts = urlsplit(html.unescape((url or "").strip()))
        scheme = parts.scheme.lower()
        host = (parts.hostname or "").encode("idna").decode("ascii").lower()
        if scheme not in {"http", "https", "ws", "wss"} or not host:
            return "<REDACTED_INVALID_URL>"
        port = parts.port
        rendered_host = f"[{host}]" if ":" in host else host
        netloc = rendered_host
        if port and not (
            (scheme in {"https", "wss"} and port == 443)
            or (scheme in {"http", "ws"} and port == 80)
        ):
            netloc = f"{rendered_host}:{port}"
        raw_segments = _fully_unquote(parts.path or "/").split("/")
        safe_segments: list[str] = []
        previous_label = ""
        for segment in raw_segments:
            decoded_segment = _fully_unquote(segment)
            base_label = decoded_segment.split(";", 1)[0].lower()
            if previous_label in CAPABILITY_PATH_LABELS:
                safe_value = "<REDACTED>" if decoded_segment else ""
            elif base_label in CAPABILITY_PATH_LABELS and ";" in decoded_segment:
                safe_value = f"{decoded_segment.split(';', 1)[0]};<REDACTED>"
            else:
                safe_value = _redact_opaque(decoded_segment)
            safe_segments.append(quote(safe_value, safe="-._~!$&'()*+,;=:@"))
            previous_label = base_label
        path = "/".join(safe_segments)
        query_names = sorted(
            _redact_opaque(key)
            for key, _ in parse_qsl(parts.query, keep_blank_values=True, max_num_fields=128)
        )
        query = urlencode([(key, "<REDACTED>") for key in query_names], doseq=True)
        fragment = quote("<REDACTED>", safe="") if parts.fragment else ""
        rendered = urlunsplit((scheme, netloc, path or "/", query, fragment))
        return _bounded_evidence_url(rendered, scheme=scheme, netloc=netloc)
    except (TypeError, UnicodeError, ValueError):
        return "<REDACTED_INVALID_URL>"


def sanitize_persisted_url_fields(record: Mapping[str, Any]) -> dict[str, Any]:
    """Copy a record while sanitizing URL-bearing fields before persistence."""
    rendered = dict(record)
    for key, value in list(rendered.items()):
        is_url_field = key == "url" or key.endswith("_url") or key in {"discovered_from", "redirect_chain"}
        if not is_url_field:
            continue
        if isinstance(value, str):
            rendered[key] = sanitize_url_for_evidence(value)
        elif isinstance(value, (list, tuple)):
            rendered[key] = [
                sanitize_url_for_evidence(item) if isinstance(item, str) else item
                for item in value
            ]
    return rendered


def controlled_error(error: Exception, *, stage: str) -> dict[str, str]:
    """Return diagnostic identifiers without persisting attacker-controlled exception text."""
    error_name = re.sub(r"(?<!^)(?=[A-Z])", "_", type(error).__name__).lower()
    safe_stage = re.sub(r"[^a-z0-9_]+", "_", stage.lower()).strip("_") or "unknown"
    return {
        "error_stage": safe_stage,
        "error_code": f"{safe_stage}_{error_name}",
    }


def redact_headers(headers: Mapping[str, Any] | None) -> dict[str, str]:
    """Retain useful protocol metadata without retaining credential values."""
    result: dict[str, str] = {}
    items = sorted((headers or {}).items(), key=lambda item: str(item[0]).lower())[:MAX_HEADER_COUNT]
    for raw_name, raw_value in items:
        name = str(raw_name).lower()[:MAX_HEADER_NAME_CHARS]
        value = str(raw_value)
        if SENSITIVE_HEADER_RE.search(name):
            result[name] = "<REDACTED>"
        elif name in {"origin", "referer"}:
            result[name] = sanitize_url_for_evidence(value)
        elif name in {"x-request-id", "x-correlation-id"}:
            result[name] = "<REDACTED>"
        elif name in SAFE_HEADER_VALUES:
            result[name] = value[:MAX_HEADER_VALUE_CHARS]
        else:
            # Preserve the existence of uncommon headers, not arbitrary values.
            result[name] = "<PRESENT>"
    return result


class PublicURLPolicy:
    """Public-HTTP(S) policy that re-resolves every network request."""

    def __init__(self, *, resolve_public: bool = True) -> None:
        self.resolve_public = resolve_public

    def check(self, url: str, *, allow_embedded: bool = False) -> tuple[bool, str]:
        try:
            parts = urlsplit(url)
            scheme = parts.scheme.lower()
            if scheme in {"data", "blob"}:
                if allow_embedded:
                    return True, "embedded_resource"
                return False, "embedded_scheme_navigation"

            if scheme not in {"http", "https"}:
                return False, "unsupported_scheme"
            if parts.username or parts.password:
                return False, "credentialed_url"
            host = (parts.hostname or "").lower()
            if not host:
                return False, "missing_host"
            if is_tracker_url(url):
                return False, "third_party_tracker"
            allowed = is_public_http_url(url, resolve=self.resolve_public)
            return (True, "public_http_url") if allowed else (False, "non_public_destination")
        except (TypeError, ValueError):
            return False, "invalid_url"


def configure_playwright_node(node_path: str | None = None) -> str:
    """Point distro-patched Playwright at an available Node.js binary."""
    selected = (
        node_path
        or os.environ.get("PLAYWRIGHT_NODEJS_PATH")
        or shutil.which("node")
    )
    if not selected:
        raise RuntimeError("Playwright requires Node.js; no node executable was found")
    os.environ["PLAYWRIGHT_NODEJS_PATH"] = selected
    return selected


def browser_context_options(user_agent: str) -> dict[str, Any]:
    """Return a fresh-context policy; callers create one context per source."""
    return {
        "user_agent": user_agent,
        "viewport": {"width": 1365, "height": 900},
        "accept_downloads": False,
        "service_workers": "block",
        "ignore_https_errors": False,
    }


def browser_launch_options() -> dict[str, Any]:
    """Return fail-closed Chromium launch options shared by all browser lanes."""
    try:
        proxy_url = validate_loopback_http_proxy_url(
            os.environ.get(
                "ARGUS_BROWSER_EGRESS_PROXY",
                "http://127.0.0.1:9219",
            )
        )
    except ValueError as error:
        raise RuntimeError("ARGUS_BROWSER_EGRESS_PROXY must be a credential-free loopback HTTP proxy") from error

    chrome_binary = os.environ.get("ARGUS_CHROME_BINARY", "/usr/bin/google-chrome").strip()
    if not chrome_binary or not os.access(chrome_binary, os.X_OK):
        raise RuntimeError(f"Chrome binary is not executable: {chrome_binary or '<unset>'}")
    sandbox_enabled = os.environ.get("ARGUS_BROWSER_NO_SANDBOX", "").lower() not in {
        "1",
        "true",
        "yes",
    }
    return {
        "headless": True,
        "chromium_sandbox": sandbox_enabled,
        "executable_path": chrome_binary,
        "proxy": {"server": proxy_url},
        "args": [
            "--disable-dev-shm-usage",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-sync",
            "--disable-quic",
            "--disable-crash-reporter",
            "--disable-breakpad",
            "--disable-features=AsyncDns",
            "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
            "--proxy-bypass-list=<-loopback>",
        ],
    }


async def create_isolated_page(
    browser: Any,
    *,
    user_agent: str,
    policy: PublicURLPolicy,
    recorder: "BrowserEvidenceRecorder",
) -> tuple[Any, Any]:
    """Create one guarded browser context/page and attach redacted telemetry."""
    context = await browser.new_context(**browser_context_options(user_agent))
    recorder.mark_context_created()

    async def guard(route: Any) -> None:
        request = route.request
        navigation_check = getattr(request, "is_navigation_request", None)
        is_navigation = bool(navigation_check()) if callable(navigation_check) else False
        allowed, reason = policy.check(request.url, allow_embedded=not is_navigation)
        if allowed:
            await route.continue_()
            return
        recorder.record_blocked_request(request.url, reason)
        await route.abort("blockedbyclient")

    await context.route("**/*", guard)

    async def block_websocket(websocket: Any) -> None:
        recorder.record_blocked_request(websocket.url, "websocket_disabled")
        await websocket.close()

    await context.route_web_socket("**/*", block_websocket)
    page = await context.new_page()

    def on_request(request: Any) -> None:
        try:
            recorder.record_request(
                method=request.method,
                url=request.url,
                resource_type=request.resource_type,
                headers=request.headers,
            )
        except Exception:
            recorder.record_telemetry_error()
            return

    def on_response(response: Any) -> None:
        try:
            recorder.record_response(
                status=response.status,
                url=response.url,
                resource_type=response.request.resource_type,
                headers=response.headers,
            )
        except Exception:
            recorder.record_telemetry_error()
            return

    page.on("request", on_request)
    page.on("response", on_response)
    recorder.mark_context_guard_ready()
    return context, page


def _is_timeout_error(error: Exception) -> bool:
    return any(cls.__name__ == "TimeoutError" for cls in type(error).__mro__)


async def wait_for_meaningful_page(page: Any, *, timeout_ms: int, minimum_text_chars: int = 200) -> dict[str, str]:
    """Use bounded lifecycle/content conditions instead of fixed sleeps."""
    result: dict[str, str] = {}
    try:
        await page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
        result["domcontentloaded"] = "observed"
    except Exception as error:
        if not _is_timeout_error(error):
            raise
        result["domcontentloaded"] = "timeout_or_busy"
    try:
        await page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 5000))
        result["networkidle"] = "observed"
    except Exception as error:
        if not _is_timeout_error(error):
            raise
        result["networkidle"] = "timeout_or_busy"
    threshold = max(0, int(minimum_text_chars))
    expression = f"""() => {{
      if (!document.body) return false;
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      let total = 0, scanned = 0, node;
      while ((node = walker.nextNode()) && scanned < 2000) {{
        total += String(node.nodeValue || '').length;
        if (total >= {threshold}) return true;
        scanned += 1;
      }}
      return false;
    }}"""
    try:
        await page.wait_for_function(expression, timeout=min(timeout_ms, 5000))
        result["meaningful_content"] = "observed"
    except Exception as error:
        if not _is_timeout_error(error):
            raise
        result["meaningful_content"] = "timeout_or_thin"
    return result


async def extract_bounded_page(
    page: Any,
    *,
    text_limit: int = 200_000,
    link_limit: int = 2_000,
    script_limit: int = 500,
    resource_limit: int = 2_000,
    frame_limit: int = 100,
    element_scan_limit: int = 10_000,
    text_node_scan_limit: int = 10_000,
    url_char_limit: int = MAX_EVIDENCE_URL_BYTES,
    title_char_limit: int = 512,
) -> dict[str, Any]:
    """Serialize a hard-bounded DOM snapshot without materializing full collections."""
    limits = {
        "text": max(0, int(text_limit)),
        "links": max(0, int(link_limit)),
        "scripts": max(0, int(script_limit)),
        "resources": max(0, int(resource_limit)),
        "frames": max(0, int(frame_limit)),
        "elementScan": max(1, int(element_scan_limit)),
        "textNodeScan": max(1, int(text_node_scan_limit)),
        "urlChars": max(64, int(url_char_limit)),
        "titleChars": max(32, int(title_char_limit)),
    }
    return await page.evaluate(
        r"""limits => {
          const cap = (value, limit) => String(value || '').slice(0, limit);
          const root = document.documentElement || document;

          const textParts = [];
          let textChars = 0;
          let capturedTextChars = 0;
          let textNodesScanned = 0;
          let textTruncated = false;
          const excludedTextTags = new Set(['script', 'style', 'noscript', 'template', 'svg']);
          const isRenderableTextNode = textNode => {
            let parent = textNode.parentElement;
            while (parent) {
              const tag = String(parent.tagName || '').toLowerCase();
              const inlineStyle = String(parent.getAttribute('style') || '');
              if (
                excludedTextTags.has(tag)
                || parent.hidden
                || parent.hasAttribute('inert')
                || String(parent.getAttribute('aria-hidden') || '').toLowerCase() === 'true'
                || /(?:^|;)\s*display\s*:\s*none\s*(?:;|$)/i.test(inlineStyle)
                || /(?:^|;)\s*visibility\s*:\s*(?:hidden|collapse)\s*(?:;|$)/i.test(inlineStyle)
              ) return false;
              if (parent === document.body) break;
              parent = parent.parentElement;
            }
            return true;
          };
          if (document.body && limits.text > 0) {
            const textWalker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
            let textNode;
            while ((textNode = textWalker.nextNode())) {
              textNodesScanned += 1;
              if (isRenderableTextNode(textNode)) {
                const value = String(textNode.nodeValue || '');
                textChars += value.length;
                const remaining = limits.text - capturedTextChars;
                if (remaining > 0) {
                  const captured = value.slice(0, remaining);
                  textParts.push(captured);
                  capturedTextChars += captured.length;
                }
              }
              if (textChars > limits.text || textNodesScanned >= limits.textNodeScan) {
                textTruncated = Boolean(textWalker.nextNode()) || textChars > limits.text;
                break;
              }
            }
          }

          const links = [];
          const scripts = [];
          const frames = [];
          const counts = {links: 0, scripts: 0, frames: 0};
          let elementsScanned = 0;
          let elementScanTruncated = false;
          const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
          let node;
          while ((node = walker.nextNode())) {
            elementsScanned += 1;
            const tag = String(node.tagName || '').toLowerCase();
            if (tag === 'a') {
              counts.links += 1;
              if (links.length < limits.links) {
                links.push({
                  text: cap(node.getAttribute('aria-label') || node.getAttribute('title') || node.firstChild?.nodeValue || '', 240).trim().replace(/\s+/g, ' '),
                  href: cap(node.href, limits.urlChars)
                });
              }
            } else if (tag === 'script' && node.src) {
              counts.scripts += 1;
              if (scripts.length < limits.scripts) {
                scripts.push({
                  src: cap(node.src, limits.urlChars),
                  type: cap(node.type || 'classic', 80),
                  integrity: cap(node.integrity || '', 256)
                });
              }
            } else if (tag === 'iframe' && node.src) {
              counts.frames += 1;
              if (frames.length < limits.frames) frames.push(cap(node.src, limits.urlChars));
            }
            if (elementsScanned >= limits.elementScan) {
              elementScanTruncated = Boolean(walker.nextNode());
              break;
            }
          }

          const title = cap(document.title, limits.titleChars);
          const currentUrl = cap(location.href, limits.urlChars);
          return {
            title,
            title_total_chars_lower_bound: String(document.title || '').length,
            url: currentUrl,
            text: textParts.join(''),
            text_total_chars_lower_bound: textChars,
            links,
            scripts,
            resources: [],
            frames,
            resources_source: 'bounded_network_evidence',
            total_semantics: 'lower_bound_when_truncated',
            truncation: {
              title: String(document.title || '').length > limits.titleChars,
              url: String(location.href || '').length > limits.urlChars,
              text: textTruncated,
              links: counts.links > limits.links || elementScanTruncated,
              scripts: counts.scripts > limits.scripts || elementScanTruncated,
              resources: false,
              frames: counts.frames > limits.frames || elementScanTruncated,
              element_scan: elementScanTruncated,
              text_node_scan: textNodesScanned >= limits.textNodeScan
            },
            totals_lower_bound: {
              links: counts.links,
              scripts: counts.scripts,
              resources: 0,
              frames: counts.frames,
              elements_scanned: elementsScanned,
              text_nodes_scanned: textNodesScanned
            }
          };
        }""",
        limits,
    )


def bounded_page_metrics(page_data: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize bounded DOM counters without converting lower bounds to exact totals."""
    captured_text_chars = len(str(page_data.get("text") or ""))
    captured_title_chars = len(str(page_data.get("title") or ""))
    try:
        text_lower_bound = int(
            page_data.get("text_total_chars_lower_bound", captured_text_chars)
        )
    except (TypeError, ValueError):
        text_lower_bound = captured_text_chars
    try:
        title_lower_bound = int(
            page_data.get("title_total_chars_lower_bound", captured_title_chars)
        )
    except (TypeError, ValueError):
        title_lower_bound = captured_title_chars
    raw_totals = page_data.get("totals_lower_bound")
    totals = dict(raw_totals) if isinstance(raw_totals, Mapping) else {}
    return {
        "captured_text_chars": captured_text_chars,
        "captured_title_chars": captured_title_chars,
        "text_total_chars_lower_bound": max(captured_text_chars, text_lower_bound),
        "title_total_chars_lower_bound": max(captured_title_chars, title_lower_bound),
        "totals_lower_bound": totals,
        "total_semantics": str(
            page_data.get("total_semantics") or "lower_bound_when_truncated"
        ),
    }


def _private_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    os.chmod(path, 0o700)


def _write_private_text(path: Path, content: str) -> None:
    _private_directory(path.parent)
    tmp = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with tmp.open("w", encoding="utf-8") as handle:
        handle.write(content)
    os.chmod(tmp, 0o600)
    os.replace(tmp, path)
    os.chmod(path, 0o600)


class BrowserEvidenceRecorder:
    """Bounded, value-redacted network evidence for one isolated source context."""

    def __init__(
        self,
        *,
        source_id: str,
        output_root: Path,
        max_events: int = 2000,
        max_evidence_bytes: int = MAX_EVIDENCE_BYTES,
        max_event_bytes: int = MAX_EVENT_BYTES,
        browser_version: str = "unknown",
    ) -> None:
        self.source_id = source_id
        self.output_dir = Path(output_root) / source_id
        self.max_events = max(1, int(max_events))
        self.max_evidence_bytes = max(1024, int(max_evidence_bytes))
        self.max_event_bytes = max(256, int(max_event_bytes))
        self.browser_version = browser_version

        self.events: list[dict[str, Any]] = []
        self.event_bytes = 0
        self.dropped_event_count = 0
        self.dropped_event_byte_count = 0
        self.truncated_event_count = 0
        self.navigation_id = "unbound"
        self.navigation_url = ""
        self.root_host = ""
        self.started_at = utc_now()
        self.blocked_requests: list[dict[str, str]] = []
        self.blocked_request_total = 0
        self.dropped_blocked_request_count = 0
        self.context_created = False
        self.context_guard_ready = False
        self.telemetry_error_count = 0

    def mark_context_created(self) -> None:
        self.context_created = True

    def mark_context_guard_ready(self) -> None:
        self.context_guard_ready = True

    def record_telemetry_error(self) -> None:
        self.telemetry_error_count += 1

    def begin_navigation(self, navigation_id: str, url: str) -> None:
        self.navigation_id = str(navigation_id)
        self.navigation_url = sanitize_url_for_evidence(url)
        if not self.root_host:
            self.root_host = (urlsplit(url).hostname or "").lower()

    @staticmethod
    def _encoded_event_size(event: Mapping[str, Any]) -> int:
        return len((json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))

    def _append(self, event: dict[str, Any]) -> None:
        event["captured_at"] = utc_now()
        event["navigation_id"] = self.navigation_id[:128]
        size = self._encoded_event_size(event)
        if size > self.max_event_bytes:
            event = {
                "kind": str(event.get("kind") or "unknown")[:32],
                "captured_at": event["captured_at"],
                "event_truncated": True,
            }
            size = self._encoded_event_size(event)
            self.truncated_event_count += 1
        if len(self.events) >= self.max_events or self.event_bytes + size > self.max_evidence_bytes:
            self.dropped_event_count += 1
            self.dropped_event_byte_count += size
            return
        self.events.append(event)
        self.event_bytes += size

    def record_blocked_request(self, url: str, reason: str) -> None:
        self.blocked_request_total += 1
        if len(self.blocked_requests) < MAX_BLOCKED_REQUESTS:
            self.blocked_requests.append(
                {"url": sanitize_url_for_evidence(url), "reason": str(reason)[:128]}
            )
        else:
            self.dropped_blocked_request_count += 1

    def record_request(
        self,
        *,
        method: str,
        url: str,
        resource_type: str,
        headers: Mapping[str, Any] | None,
    ) -> None:
        self._append(
            {
                "kind": "request",
                "method": str(method).upper()[:16],
                "url": sanitize_url_for_evidence(url),
                "resource_type": str(resource_type)[:64],
                "headers": redact_headers(headers),
            }
        )

    def record_response(
        self,
        *,
        status: int,
        url: str,
        resource_type: str,
        headers: Mapping[str, Any] | None,
    ) -> None:
        self._append(
            {
                "kind": "response",
                "status": int(status),
                "url": sanitize_url_for_evidence(url),
                "resource_type": str(resource_type)[:64],
                "headers": redact_headers(headers),
            }
        )

    def artifact_urls(self) -> list[dict[str, str]]:
        artifacts: dict[tuple[str, str], dict[str, str]] = {}
        for event in self.events:
            if event.get("kind") != "response":
                continue
            resource_type = str(event.get("resource_type") or "")
            content_type = str((event.get("headers") or {}).get("content-type") or "")
            url = str(event.get("url") or "")
            try:
                parts = urlsplit(url)
                host = (parts.hostname or "").lower()
                path = parts.path.lower()
            except ValueError:
                continue
            if is_tracker_url(url):
                continue
            same_source = host == self.root_host or host.endswith(f".{self.root_host}")
            artifact_kind = ""
            if path.endswith(".map"):
                artifact_kind = "source_map_reference"
            elif resource_type == "script" or "javascript" in content_type or path.endswith((".js", ".mjs")):
                artifact_kind = "javascript"
            elif resource_type == "websocket":
                artifact_kind = "websocket"
            elif (
                (resource_type in {"xhr", "fetch"} or "json" in content_type)
                and (same_source or SOURCE_ARTIFACT_PATH_RE.search(path))
            ):
                artifact_kind = "api_or_json"
            if artifact_kind:
                artifacts[(artifact_kind, url)] = {"kind": artifact_kind, "url": url}
        return [artifacts[key] for key in sorted(artifacts)]

    def write(
        self,
        *,
        failure_stage: str | None = None,
        error_code: str | None = None,
    ) -> dict[str, Any]:
        _private_directory(self.output_dir)
        network_text = "".join(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n" for event in self.events)
        network_path = self.output_dir / "network.jsonl"
        _write_private_text(network_path, network_text)
        network_hash = hashlib.sha256(network_text.encode("utf-8")).hexdigest()
        manifest = {
            "schema_version": 2,
            "source_id": self.source_id,
            "started_at": self.started_at,
            "completed_at": utc_now(),
            "browser_version": self.browser_version,
            "context_isolated": self.context_created,
            "context_guard_ready": self.context_guard_ready,
            "downloads_allowed": False if self.context_created else "not_created",
            "service_workers": "blocked" if self.context_created else "not_created",
            "telemetry_callback_errors": self.telemetry_error_count,
            "failure_stage": failure_stage,
            "error_code": error_code,
            "event_count": len(self.events),
            "event_bytes": self.event_bytes,
            "max_event_bytes": self.max_event_bytes,
            "max_evidence_bytes": self.max_evidence_bytes,
            "truncated_event_count": self.truncated_event_count,
            "dropped_event_count": self.dropped_event_count,
            "dropped_event_byte_count": self.dropped_event_byte_count,
            "blocked_request_total": self.blocked_request_total,
            "blocked_request_recorded": len(self.blocked_requests),
            "dropped_blocked_request_count": self.dropped_blocked_request_count,
            "blocked_requests": self.blocked_requests,
            "artifact_urls": self.artifact_urls(),
            "network_file": "network.jsonl",
            "network_sha256": network_hash,
        }
        _write_private_text(
            self.output_dir / "manifest.json",
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        )
        return manifest
