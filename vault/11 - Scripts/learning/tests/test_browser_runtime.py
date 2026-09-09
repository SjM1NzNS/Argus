from __future__ import annotations

import asyncio
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from browser_runtime import (
    BrowserEvidenceRecorder,
    PublicURLPolicy,
    browser_context_options,
    browser_launch_options,
    bounded_page_metrics,
    configure_playwright_node,
    controlled_error,
    create_isolated_page,
    extract_bounded_page,
    redact_headers,
    sanitize_persisted_url_fields,
    sanitize_url_for_evidence,
    url_identity,
    wait_for_meaningful_page,
)


class BrowserRuntimeSafetyTests(unittest.TestCase):
    def test_evidence_url_strips_userinfo_values_and_fragment(self) -> None:
        sanitized = sanitize_url_for_evidence(
            "https://user:pass@Example.COM/path?token=secret&next=%2Fhome#opaque-state"
        )
        self.assertEqual(
            sanitized,
            "https://example.com/path?next=%3CREDACTED%3E&token=%3CREDACTED%3E#%3CREDACTED%3E",
        )
        self.assertNotIn("user", sanitized)
        self.assertNotIn("pass", sanitized)
        self.assertNotIn("secret", sanitized)
        self.assertNotIn("opaque-state", sanitized)

    def test_capability_path_segments_and_opaque_parameter_names_are_redacted(self) -> None:
        raw = (
            "https://example.com/download/"
            + "sk_live_"
            + "A" * 24
            + "?"
            + "eyJ"
            + "hbGciOiJIUzI1NiJ9"
            + "=secret"
        )
        sanitized = sanitize_url_for_evidence(raw)
        self.assertNotIn("sk_live", sanitized)
        self.assertNotIn("eyJhbGci", sanitized)
        self.assertNotIn("secret", sanitized)
        self.assertIn("%3CREDACTED%3E", sanitized)

    def test_uuid_magic_link_percent_encoded_ipv6_and_oversized_urls_are_safe(self) -> None:
        raw = (
            "https://[2606:4700:4700::1111]/reset/"
            "550e8400-e29b-41d4-a716-446655440000/magic/AbCdEfGhIjKlMnOpQrStUvWx/"
            "%41%42%43%44%45%46%47%48%49%4A%4B%4C%4D%4E%4F%50%51%52%53%54%55%56%57%58"
            "?AbCdEfGhIjKlMnOpQrStUvWx"
        )
        sanitized = sanitize_url_for_evidence(raw)
        self.assertTrue(sanitized.startswith("https://[2606:4700:4700::1111]/"))
        self.assertNotIn("550e8400", sanitized)
        self.assertNotIn("AbCdEf", sanitized)
        self.assertGreaterEqual(sanitized.count("%3CREDACTED%3E"), 3)
        oversized = sanitize_url_for_evidence("https://example.com/" + "a" * 20_000)
        self.assertNotIn("a" * 100, oversized)
        self.assertIn("REDACTED", oversized)
        self.assertLessEqual(len(oversized.encode("utf-8")), 4096)

    def test_single_class_capability_segments_and_request_ids_are_redacted(self) -> None:
        for label, token in (
            ("reset", "abcdefghijklmnopqrstuvwxyz123456"),
            ("magic", "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"),
            ("invite", "abcdefghijklmnopqrstuvwxyz"),
            ("auth", "123456789012345678901234"),
        ):
            with self.subTest(label=label):
                rendered = sanitize_url_for_evidence(f"https://example.com/{label}/{token}")
                self.assertNotIn(token, rendered)
                self.assertIn("%3CREDACTED%3E", rendered)
        headers = redact_headers(
            {
                "X-Request-ID": "550e8400-e29b-41d4-a716-446655440000",
                "X-Correlation-ID": "abcdefghijklmnopqrstuvwxyz123456",
            }
        )
        self.assertEqual(headers["x-request-id"], "<REDACTED>")
        self.assertEqual(headers["x-correlation-id"], "<REDACTED>")

    def test_short_and_encoded_capability_path_credentials_are_redacted(self) -> None:
        cases = (
            ("https://example.com/reset/123456", "123456"),
            ("https://example.com/magic%252F654321", "654321"),
            ("https://example.com/password/abcd", "abcd"),
            ("https://example.com/invite;token=7788", "7788"),
        )
        for raw, secret in cases:
            with self.subTest(raw=raw):
                rendered = sanitize_url_for_evidence(raw)
                self.assertNotIn(secret, rendered)
                self.assertIn("REDACTED", rendered)

    def test_static_candidate_url_fields_are_sanitized(self) -> None:
        record = sanitize_persisted_url_fields({
            "url": "https://example.com/reset/123456?token=secret",
            "effective_url": "https://example.com/magic%252F654321",
            "discovered_from": "https://example.com/invite;token=7788",
            "title": "unchanged",
        })
        payload = json.dumps(record)
        for secret in ("123456", "secret", "654321", "7788"):
            self.assertNotIn(secret, payload)
        self.assertEqual(record["title"], "unchanged")

    def test_bounded_page_metrics_preserve_lower_bound_semantics(self) -> None:
        metrics = bounded_page_metrics(
            {
                "text": "captured",
                "title": "short",
                "text_total_chars_lower_bound": 50_000,
                "title_total_chars_lower_bound": 77,
                "totals_lower_bound": {"links": 201, "elements_scanned": 10_000},
                "total_semantics": "lower_bound_when_truncated",
            }
        )
        self.assertEqual(metrics["text_total_chars_lower_bound"], 50_000)
        self.assertEqual(metrics["title_total_chars_lower_bound"], 77)
        self.assertEqual(metrics["totals_lower_bound"]["links"], 201)
        self.assertEqual(metrics["total_semantics"], "lower_bound_when_truncated")

    def test_controlled_errors_never_persist_exception_text_or_urls(self) -> None:
        error = RuntimeError(
            "failed https://user:pass@example.com/private/token-abcdef?session=secret"
        )
        rendered = controlled_error(error, stage="navigation")
        self.assertEqual(rendered["error_stage"], "navigation")
        self.assertEqual(rendered["error_code"], "navigation_runtime_error")
        self.assertNotIn("example.com", json.dumps(rendered))
        self.assertNotIn("secret", json.dumps(rendered))

    def test_raw_url_identity_is_stable_distinct_and_not_reversible_in_state(self) -> None:
        key = b"k" * 32
        first = url_identity("https://example.com/items?page=1&token=secret", key=key)
        same = url_identity("https://example.com/items?page=1&token=secret", key=key)
        second = url_identity("https://example.com/items?page=2&token=secret", key=key)
        self.assertEqual(first, same)
        self.assertNotEqual(first, second)
        self.assertNotIn("example.com", first)
        self.assertNotIn("secret", first)

    def test_request_policy_blocks_unsafe_schemes_credentials_and_private_literals(self) -> None:
        policy = PublicURLPolicy(resolve_public=False)
        for url in [
            "file:///etc/passwd",
            "javascript:alert(1)",
            "data:text/html,hello",
            "http://127.0.0.1/admin",
            "http://169.254.169.254/latest/meta-data/",
            "https://user:pass@example.com/private",
        ]:
            with self.subTest(url=url):
                allowed, _ = policy.check(url)
                self.assertFalse(allowed)
        self.assertEqual(policy.check("https://example.com/app"), (True, "public_http_url"))
        self.assertEqual(
            policy.check("data:image/png;base64,AAAA", allow_embedded=True),
            (True, "embedded_resource"),
        )
        self.assertEqual(
            policy.check("https://www.googletagmanager.com/gtm.js?id=G-1"),
            (False, "third_party_tracker"),
        )

    def test_public_destinations_are_re_resolved_for_each_request(self) -> None:
        policy = PublicURLPolicy(resolve_public=True)
        with mock.patch("browser_runtime.is_public_http_url", return_value=True) as check:
            self.assertEqual(policy.check("https://example.com/a"), (True, "public_http_url"))
            self.assertEqual(policy.check("https://example.com/a"), (True, "public_http_url"))
        self.assertEqual(check.call_count, 2)

    def test_sensitive_header_values_are_never_retained(self) -> None:
        redacted = redact_headers(
            {
                "Authorization": "Bearer top-secret",
                "Cookie": "session=abc",
                "X-CSRF-Token": "csrf-secret",
                "Content-Type": "application/json",
                "Referer": "https://example.com/app?token=also-secret#private",
            }
        )
        self.assertEqual(redacted["authorization"], "<REDACTED>")
        self.assertEqual(redacted["cookie"], "<REDACTED>")
        self.assertEqual(redacted["x-csrf-token"], "<REDACTED>")
        self.assertEqual(redacted["content-type"], "application/json")
        self.assertNotIn("also-secret", redacted["referer"])
        self.assertIn("token=%3CREDACTED%3E", redacted["referer"])

        self.assertNotIn("top-secret", json.dumps(redacted))
        self.assertNotIn("session=abc", json.dumps(redacted))

    def test_playwright_uses_the_available_node_binary(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            selected = configure_playwright_node("/opt/node/bin/node")
            self.assertEqual(selected, "/opt/node/bin/node")
            self.assertEqual(os.environ["PLAYWRIGHT_NODEJS_PATH"], "/opt/node/bin/node")

    def test_context_policy_is_isolated_and_downloads_are_disabled(self) -> None:
        options = browser_context_options("ArgusTest/1.0")
        self.assertFalse(options["accept_downloads"])
        self.assertEqual(options["service_workers"], "block")
        self.assertNotIn("storage_state", options)
        self.assertEqual(options["user_agent"], "ArgusTest/1.0")

    def test_launch_policy_uses_system_chrome_and_fail_closed_proxy(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True):
            options = browser_launch_options()
        self.assertEqual(options["executable_path"], "/usr/bin/google-chrome")
        self.assertEqual(options["proxy"]["server"], "http://127.0.0.1:9219")
        self.assertTrue(options["chromium_sandbox"])
        args = options["args"]
        self.assertIn("--disable-quic", args)
        self.assertIn("--proxy-bypass-list=<-loopback>", args)
        self.assertNotIn("--no-sandbox", args)


class BrowserEvidenceTests(unittest.TestCase):
    def test_network_evidence_is_bounded_sanitized_hashed_and_private(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            recorder = BrowserEvidenceRecorder(
                source_id="source-one",
                output_root=Path(td),
                max_events=2,
                browser_version="Chrome Test",
            )
            recorder.begin_navigation("root", "https://example.com/?session=secret")
            recorder.record_request(
                method="GET",
                url="https://example.com/app.js?token=secret",
                resource_type="script",
                headers={"Authorization": "Bearer secret", "Accept": "*/*"},
            )
            recorder.record_response(
                status=200,
                url="https://example.com/app.js?token=secret",
                resource_type="script",
                headers={"Content-Type": "application/javascript", "Set-Cookie": "sid=secret"},
            )
            recorder.record_request(
                method="GET",
                url="https://example.com/overflow",
                resource_type="document",
                headers={},
            )
            manifest = recorder.write()

            self.assertFalse(manifest["context_isolated"])
            self.assertEqual(manifest["downloads_allowed"], "not_created")
            self.assertEqual(manifest["service_workers"], "not_created")
            self.assertEqual(manifest["event_count"], 2)
            self.assertEqual(manifest["dropped_event_count"], 1)
            self.assertLessEqual(manifest["event_bytes"], manifest["max_evidence_bytes"])
            self.assertEqual(manifest["blocked_request_total"], 0)
            self.assertRegex(manifest["network_sha256"], r"^[0-9a-f]{64}$")
            network_path = Path(td) / "source-one" / "network.jsonl"
            payload = network_path.read_text(encoding="utf-8")
            self.assertNotIn("secret", payload)
            self.assertIn("%3CREDACTED%3E", payload)
            self.assertEqual(stat.S_IMODE(network_path.stat().st_mode), 0o600)
            self.assertEqual(
                stat.S_IMODE((Path(td) / "source-one" / "manifest.json").stat().st_mode),
                0o600,
            )
    def test_blocked_counts_and_serialized_evidence_bytes_are_truthfully_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            recorder = BrowserEvidenceRecorder(
                source_id="bounded",
                output_root=Path(td),
                max_events=500,
                max_event_bytes=256,
                max_evidence_bytes=1024,
            )
            for index in range(205):
                recorder.record_blocked_request(
                    "https://example.com/" + ("x" * 5000) + f"?token={index}",
                    "websocket_disabled",
                )
                recorder.record_request(
                    method="GET",
                    url=f"https://example.com/resource/{index}",
                    resource_type="fetch",
                    headers={"content-type": "y" * 5000},
                )
            manifest = recorder.write()
            self.assertEqual(manifest["blocked_request_total"], 205)
            self.assertEqual(manifest["blocked_request_recorded"], 200)
            self.assertEqual(manifest["dropped_blocked_request_count"], 5)
            self.assertLessEqual(manifest["event_bytes"], 1024)
            self.assertGreater(manifest["dropped_event_count"], 0)
            self.assertGreater(manifest["truncated_event_count"], 0)
            network_path = Path(td) / "bounded" / "network.jsonl"
            for line in network_path.read_text(encoding="utf-8").splitlines():
                self.assertLessEqual(len(line.encode("utf-8")), 256)

    def test_artifact_inventory_suppresses_trackers_and_keeps_source_derived_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            recorder = BrowserEvidenceRecorder(source_id="source-one", output_root=Path(td), max_events=10)
            recorder.begin_navigation("root", "https://app.example.com/")
            recorder.record_response(
                status=200,
                url="https://app.example.com/api/config?key=secret",
                resource_type="fetch",
                headers={"Content-Type": "application/json"},
            )
            recorder.record_response(
                status=200,
                url="https://www.googletagmanager.com/collect?id=secret",
                resource_type="fetch",
                headers={"Content-Type": "application/json"},
            )
            recorder.record_response(
                status=200,
                url="https://cdn.example.net/assets/app.js.map?v=secret",
                resource_type="script",
                headers={"Content-Type": "application/json"},
            )
            recorder.record_response(
                status=200,
                url="https://plausible.io/js/script.js",
                resource_type="script",
                headers={"Content-Type": "application/javascript"},
            )
            artifacts = recorder.artifact_urls()
            rendered = json.dumps(artifacts)
            self.assertIn("app.example.com/api/config", rendered)
            self.assertIn("source_map_reference", rendered)
            self.assertNotIn("googletagmanager", rendered)
            self.assertNotIn("plausible", rendered)
            self.assertNotIn("secret", rendered)


class BrowserLaneSourceTests(unittest.TestCase):
    def test_browser_lanes_share_playwright_runtime_and_do_not_use_fixed_sleeps(self) -> None:
        for name in ("browser_dom_ingest.py", "browser_source_triage.py"):
            text = (SCRIPT_DIR / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertIn("from browser_runtime import", text)
                self.assertNotIn("time.sleep(", text)
        self.assertNotIn("selenium", (SCRIPT_DIR / "browser_dom_ingest.py").read_text(encoding="utf-8").lower())

    def test_browser_consumers_use_lower_bound_dom_metrics(self) -> None:
        for name in ("browser_dom_ingest.py", "browser_source_triage.py"):
            text = (SCRIPT_DIR / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertIn("bounded_page_metrics", text)
                self.assertNotIn('data.get("text_total_chars")', text)
                self.assertNotIn('data.get("totals")', text)

    def test_summaries_distinguish_startup_context_guard_and_evidence_saturation(self) -> None:
        for name in ("browser_dom_ingest.py", "browser_source_triage.py"):
            text = (SCRIPT_DIR / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertIn("browser_started", text)
                self.assertIn("context_guards_ready", text)
                self.assertIn("truncated_network_event_count", text)
                self.assertIn("dropped_network_event_bytes", text)
                self.assertIn("blocked_request_recorded", text)

    def test_static_ingest_forces_robots_content_and_redirects_through_proxy_opener(self) -> None:
        text = (SCRIPT_DIR / "learning_ingest.py").read_text(encoding="utf-8")
        self.assertIn("build_mandatory_proxy_opener", text)
        self.assertGreaterEqual(text.count("HTTP_OPENER.open("), 2)
        self.assertNotIn("urlopen(", text)
        self.assertNotIn("rp.read()", text)
        self.assertIn("return False, f\"robots_error:", text)

    def test_legacy_browser_lane_does_not_ignore_an_explicit_source_filter(self) -> None:
        text = (SCRIPT_DIR / "browser_dom_ingest.py").read_text(encoding="utf-8")
        self.assertIn('RUN_CADENCE == "legacy" and not SOURCE_FILTER', text)

    def test_cdp_launcher_rejects_non_loopback_or_bypass_proxy_values(self) -> None:
        launcher = SCRIPT_DIR.parent / "browser" / "launch_argus_chrome_cdp.sh"
        for proxy in (
            "direct://",
            "http://proxy.example:8080",
            "http://user:pass@127.0.0.1:9219",
            "http://127.0.0.1:9219/extra",
            "http://127.0.0.1:9219/?q=1",
        ):
            with self.subTest(proxy=proxy), tempfile.TemporaryDirectory() as td:
                env = {
                    **os.environ,
                    "ARGUS_BROWSER_EGRESS_PROXY": proxy,
                    "ARGUS_CHROME_BINARY": "/bin/true",
                    "ARGUS_CHROME_CDP_PROFILE": td,
                }
                result = subprocess.run(
                    [str(launcher)], env=env, text=True, capture_output=True, timeout=5
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("credential-free loopback HTTP proxy", result.stderr)

    def test_browser_wrappers_enforce_process_cgroup_memory_and_task_bounds(self) -> None:
        for name in ("run_browser_dom_ingest.sh", "run_browser_source_triage.sh"):
            text = (SCRIPT_DIR / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertIn("systemd-run --user --scope", text)
                self.assertIn("MemoryMax=", text)
                self.assertIn("TasksMax=", text)
                self.assertIn("timeout --signal=TERM --kill-after=15s", text)

    def test_browser_ingest_wrapper_reaches_user_manager_from_cron_like_environment(self) -> None:
        wrapper = SCRIPT_DIR / "run_browser_dom_ingest.sh"
        with tempfile.TemporaryDirectory() as td:
            env = {
                "HOME": str(Path.home()),
                "PATH": "/usr/local/bin:/usr/bin:/bin",
                "ARGUS_SECURITY_RESEARCH": td,
                "ARGUS_BROWSER_PYTHON": "/bin/true",
                "ARGUS_BROWSER_MAX_TOTAL_SECONDS": "1",
            }
            result = subprocess.run(
                ["bash", str(wrapper)],
                env=env,
                text=True,
                capture_output=True,
                timeout=10,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_combined_orchestrator_preserves_browser_evidence_paths(self) -> None:
        text = (SCRIPT_DIR / "run_daily_learning_ingest.sh").read_text(encoding="utf-8")
        self.assertIn('BROWSER_DIR/browser-evidence', text)
        self.assertIn('RUN_DIR/browser-evidence', text)
        self.assertIn('cp -a', text)

    def test_combined_orchestrator_binds_both_lanes_to_parent_run_id(self) -> None:
        orchestrator = (SCRIPT_DIR / "run_daily_learning_ingest.sh").read_text(encoding="utf-8")
        self.assertEqual(orchestrator.count('ARGUS_PROVENANCE_RUN_ID="$RUN_LABEL"'), 2)
        for name in ("learning_ingest.py", "browser_dom_ingest.py"):
            text = (SCRIPT_DIR / name).read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertIn("ARGUS_PROVENANCE_RUN_ID", text)
                self.assertIn("run_id=PROVENANCE_RUN_ID", text)

    def test_legacy_selenium_triage_is_a_deprecation_wrapper(self) -> None:
        text = (SCRIPT_DIR / "browser_source_triage_selenium.py").read_text(encoding="utf-8")
        self.assertIn("deprecated", text.lower())
        self.assertNotIn("from selenium", text.lower())


class _FakeEventPage:
    def __init__(self) -> None:
        self.handlers: dict[str, object] = {}

    def on(self, event: str, handler: object) -> None:
        self.handlers[event] = handler


class _FakeContext:
    def __init__(self) -> None:
        self.route_pattern = ""
        self.route_handler = None
        self.websocket_pattern = ""
        self.websocket_handler = None
        self.page = _FakeEventPage()

    async def route(self, pattern: str, handler: object) -> None:
        self.route_pattern = pattern
        self.route_handler = handler

    async def route_web_socket(self, pattern: str, handler: object) -> None:
        self.websocket_pattern = pattern
        self.websocket_handler = handler

    async def new_page(self) -> _FakeEventPage:
        return self.page


class _FakeBrowser:
    def __init__(self) -> None:
        self.contexts: list[_FakeContext] = []
        self.options: list[dict[str, object]] = []

    async def new_context(self, **options: object) -> _FakeContext:
        self.options.append(options)
        context = _FakeContext()
        self.contexts.append(context)
        return context


class BrowserIsolationTests(unittest.IsolatedAsyncioTestCase):
    async def test_each_source_gets_a_fresh_guarded_context(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            browser = _FakeBrowser()
            policy = PublicURLPolicy(resolve_public=False)
            first_recorder = BrowserEvidenceRecorder(source_id="one", output_root=Path(td))
            second_recorder = BrowserEvidenceRecorder(source_id="two", output_root=Path(td))
            first, first_page = await create_isolated_page(
                browser,
                user_agent="ArgusTest/1.0",
                policy=policy,
                recorder=first_recorder,
            )
            second, second_page = await create_isolated_page(
                browser,
                user_agent="ArgusTest/1.0",
                policy=policy,
                recorder=second_recorder,
            )
            self.assertIsNot(first, second)
            self.assertIsNot(first_page, second_page)
            self.assertEqual(first.route_pattern, "**/*")
            self.assertIsNotNone(first.route_handler)
            self.assertEqual(first.websocket_pattern, "**/*")
            self.assertIsNotNone(first.websocket_handler)
            self.assertEqual(set(first_page.handlers), {"request", "response"})
            self.assertFalse(browser.options[0]["accept_downloads"])
            self.assertEqual(browser.options[0]["service_workers"], "block")

            class Request:
                url = "http://127.0.0.1/private"

                @staticmethod
                def is_navigation_request() -> bool:
                    return True

            class Route:
                request = Request()

                def __init__(self) -> None:
                    self.aborted = ""
                    self.continued = False

                async def abort(self, reason: str) -> None:
                    self.aborted = reason

                async def continue_(self) -> None:
                    self.continued = True

            route = Route()
            assert first.route_handler is not None
            await first.route_handler(route)
            self.assertEqual(route.aborted, "blockedbyclient")
            self.assertFalse(route.continued)
            self.assertEqual(first_recorder.blocked_requests[0]["reason"], "non_public_destination")

            class WebSocketRoute:
                url = "wss://echo.example/socket?token=secret"

                def __init__(self) -> None:
                    self.closed = False

                async def close(self) -> None:
                    self.closed = True

            websocket = WebSocketRoute()
            assert first.websocket_handler is not None
            await first.websocket_handler(websocket)
            self.assertTrue(websocket.closed)
            self.assertEqual(first_recorder.blocked_requests[-1]["reason"], "websocket_disabled")
            self.assertNotIn("secret", first_recorder.blocked_requests[-1]["url"])
            self.assertTrue(first_recorder.context_created)


class _FakePage:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    async def wait_for_load_state(self, state: str, timeout: int) -> None:
        self.calls.append(("state", state))
        if state == "networkidle":
            raise TimeoutError("busy page")

    async def wait_for_function(self, expression: str, timeout: int) -> None:
        self.calls.append(("function", expression))


class BrowserWaitTests(unittest.IsolatedAsyncioTestCase):
    async def test_bounded_extraction_passes_hard_dom_limits(self) -> None:
        class EvaluatePage:
            def __init__(self) -> None:
                self.limits = None

            async def evaluate(self, expression: str, limits: dict) -> dict:
                self.limits = limits
                return {"text": "x", "links": [], "scripts": [], "resources": [], "frames": []}

        page = EvaluatePage()
        await extract_bounded_page(
            page,
            text_limit=1234,
            link_limit=22,
            script_limit=33,
            resource_limit=44,
            frame_limit=5,
        )
        self.assertEqual(
            page.limits,
            {
                "text": 1234,
                "links": 22,
                "scripts": 33,
                "resources": 44,
                "frames": 5,
                "elementScan": 10000,
                "textNodeScan": 10000,
                "titleChars": 512,
                "urlChars": 4096,
            },
        )

    async def test_wait_is_state_aware_and_tolerates_busy_pages(self) -> None:
        page = _FakePage()
        result = await wait_for_meaningful_page(page, timeout_ms=5000, minimum_text_chars=200)
        self.assertEqual(result["domcontentloaded"], "observed")
        self.assertEqual(result["networkidle"], "timeout_or_busy")
        self.assertEqual(result["meaningful_content"], "observed")
        self.assertEqual([kind for kind, _ in page.calls], ["state", "state", "function"])

    async def test_wait_propagates_programming_and_transport_errors(self) -> None:
        class BrokenPage(_FakePage):
            async def wait_for_load_state(self, state: str, timeout: int) -> None:
                raise RuntimeError("transport failed")

        with self.assertRaisesRegex(RuntimeError, "transport failed"):
            await wait_for_meaningful_page(BrokenPage(), timeout_ms=5000)


class RealBrowserBoundTests(unittest.IsolatedAsyncioTestCase):
    @unittest.skipUnless(
        os.environ.get("ARGUS_RUN_BROWSER_INTEGRATION") == "1",
        "set ARGUS_RUN_BROWSER_INTEGRATION=1 for the real system-Chrome bound probe",
    )
    async def test_extracted_text_excludes_script_style_template_and_hidden_content(self) -> None:
        configure_playwright_node()
        from playwright.async_api import async_playwright

        document = """
          <body>
            <p>VISIBLE_ALPHA</p>
            <script>{"opaque":"SCRIPT_ONLY_TOKEN"}</script>
            <style>.x::before { content: 'STYLE_ONLY_TOKEN'; }</style>
            <noscript>NOSCRIPT_ONLY_TOKEN</noscript>
            <template>TEMPLATE_ONLY_TOKEN</template>
            <div hidden>HIDDEN_ONLY_TOKEN</div>
            <div aria-hidden="true">ARIA_HIDDEN_ONLY_TOKEN</div>
            <div style="display:none">DISPLAY_NONE_ONLY_TOKEN</div>
            <p>VISIBLE_OMEGA</p>
          </body>
        """
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(**browser_launch_options())
            try:
                page = await browser.new_page()
                await page.goto("data:text/html," + quote(document), wait_until="domcontentloaded")
                data = await extract_bounded_page(page, text_limit=10_000)
            finally:
                await browser.close()
        self.assertIn("VISIBLE_ALPHA", data["text"])
        self.assertIn("VISIBLE_OMEGA", data["text"])
        for hidden in (
            "SCRIPT_ONLY_TOKEN",
            "STYLE_ONLY_TOKEN",
            "NOSCRIPT_ONLY_TOKEN",
            "TEMPLATE_ONLY_TOKEN",
            "HIDDEN_ONLY_TOKEN",
            "ARIA_HIDDEN_ONLY_TOKEN",
            "DISPLAY_NONE_ONLY_TOKEN",
        ):
            self.assertNotIn(hidden, data["text"])

    @unittest.skipUnless(
        os.environ.get("ARGUS_RUN_BROWSER_INTEGRATION") == "1",
        "set ARGUS_RUN_BROWSER_INTEGRATION=1 for the real system-Chrome bound probe",
    )
    async def test_oversized_dom_attributes_and_title_are_bounded_before_python_transfer(self) -> None:
        configure_playwright_node()
        from playwright.async_api import async_playwright

        title = "T" * 250_000
        href = "https://example.com/" + ("a" * 250_000)
        nodes = "".join(f"<div>node-{index}</div>" for index in range(20_000))
        document = f"<title>{title}</title><a href='{href}'>label</a>{nodes}"
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(**browser_launch_options())
            try:
                page = await browser.new_page()
                await page.goto("data:text/html," + quote(document), wait_until="domcontentloaded")
                data = await extract_bounded_page(
                    page,
                    text_limit=10,
                    link_limit=1,
                    script_limit=1,
                    resource_limit=1,
                    frame_limit=1,
                    element_scan_limit=100,
                    text_node_scan_limit=100,
                )
            finally:
                await browser.close()
        self.assertLessEqual(len(data["title"]), 512)
        self.assertLessEqual(len(data["links"][0]["href"]), 4096)
        self.assertLessEqual(len(data["text"]), 10)
        self.assertTrue(data["truncation"]["element_scan"])
        self.assertEqual(data["total_semantics"], "lower_bound_when_truncated")


if __name__ == "__main__":
    unittest.main()
