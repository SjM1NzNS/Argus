from __future__ import annotations

import hashlib
import json
import os
import stat
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

from compile_learning_inbox import candidate_id_for_record, classify, provenance_admission
from learning_promotion import classify_knowledge_types, promotion_requirements
from learning_reconciliation import reconcile_run, render_markdown
from learning_registry import (
    RegistryValidationError,
    load_registry,
    provenance_fields,
    select_sources,
)
from learning_safety import scope_disposition
from learning_state import (
    canonical_url,
    load_json_state,
    merge_json_state,
    migrate_seen_url_state,
    url_identity,
)
from mandatory_proxy import build_mandatory_proxy_opener
from network_policy import is_strict_public_ip, validate_loopback_http_proxy_url
from publish_learning_run import build_manifest


FIXTURE = """
registry:
  schema_version: 2
  promotion_status_default: proposal_only
source_group_policies:
  monitoring:
    role: practitioner_commentary
    domain: web2
    acquisition: static
    cadence: weekly
    trust: curated_secondary
    promotion_policy: corroboration_required
    original_source_required: false
    independent_corroboration: required
    refetch_interval_days: 14
    expected_content_type: article
    deep_link_limit: 4
  references:
    role: foundational_reference
    domain: cross_domain
    acquisition: static
    cadence: on_demand
    trust: authority
    promotion_policy: review_required
    original_source_required: false
    independent_corroboration: conditional
    refetch_interval_days: 180
    expected_content_type: documentation
monitoring:
  - id: daily-primary
    name: Daily Primary
    url: https://example.test/daily
    type: research_blog
    cadence: daily
    trust: primary
    promotion_policy: review_required
    independent_corroboration: conditional
    priority: high
  - id: weekly-static
    name: Weekly Static
    url: https://example.test/weekly
    type: research_blog
    priority: medium
  - id: weekly-browser-index
    name: Weekly Browser Index
    url: https://browser.example.test/reports
    type: report_index
    role: discovery_index
    acquisition: browser_dom
    trust: discovery_only
    promotion_policy: original_source_required
    original_source_required: true
    independent_corroboration: required
    expected_content_type: index
    priority: high
references:
  - id: foundational-reference
    name: Foundational Reference
    url: https://reference.example.test/
    type: official_standard
    priority: high
"""


class RegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "sources.yaml"
        self.path.write_text(FIXTURE, encoding="utf-8")
        self.registry = load_registry(self.path)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_group_defaults_are_materialized_and_registry_is_hashed(self) -> None:
        source = next(s for s in self.registry.sources if s["id"] == "weekly-static")
        self.assertEqual(source["role"], "practitioner_commentary")
        self.assertEqual(source["cadence"], "weekly")
        self.assertEqual(source["refetch_interval_days"], 14)
        self.assertRegex(self.registry.digest, r"^[0-9a-f]{64}$")

    def test_cadence_and_lane_selection_are_explicit(self) -> None:
        self.assertEqual(
            [s["id"] for s in select_sources(self.registry, cadence="daily")],
            ["daily-primary"],
        )
        self.assertEqual(
            {s["id"] for s in select_sources(self.registry, cadence="weekly")},
            {"daily-primary", "weekly-static", "weekly-browser-index"},
        )
        self.assertEqual(
            [s["id"] for s in select_sources(self.registry, cadence="weekly", lane="browser_dom")],
            ["weekly-browser-index"],
        )
        self.assertEqual(
            [s["id"] for s in select_sources(self.registry, cadence="backfill")],
            ["foundational-reference"],
        )

    def test_targeted_backfill_is_an_exact_allowlist(self) -> None:
        selected = select_sources(
            self.registry,
            cadence="backfill",
            source_ids={"foundational-reference"},
        )
        self.assertEqual({s["id"] for s in selected}, {"foundational-reference"})

        daily_refresh = select_sources(
            self.registry,
            cadence="backfill",
            source_ids={"daily-primary"},
        )
        self.assertEqual({s["id"] for s in daily_refresh}, {"daily-primary"})

        with self.assertRaises(RegistryValidationError):
            select_sources(
                self.registry,
                cadence="backfill",
                source_ids={"not-present"},
            )

    def test_required_semantics_are_rejected_when_missing(self) -> None:
        bad = Path(self.tmp.name) / "bad.yaml"
        bad.write_text(
            """
registry: {schema_version: 2}
source_group_policies:
  broken:
    domain: web2
broken:
  - id: broken
    name: Broken
    url: https://example.test/
    type: blog
    priority: high
""",
            encoding="utf-8",
        )
        with self.assertRaises(RegistryValidationError) as ctx:
            load_registry(bad)
        self.assertIn("role", str(ctx.exception))
        self.assertIn("cadence", str(ctx.exception))

    def test_empty_allowlist_selects_nothing(self) -> None:
        self.assertEqual(
            select_sources(self.registry, cadence="backfill", source_ids=set()),
            [],
        )

    def test_duplicate_yaml_keys_and_non_scalar_fields_fail_closed(self) -> None:
        duplicate = Path(self.tmp.name) / "duplicate.yaml"
        duplicate.write_text(FIXTURE + "\nregistry:\n  schema_version: 2\n", encoding="utf-8")
        with self.assertRaises(RegistryValidationError):
            load_registry(duplicate)

        malformed = Path(self.tmp.name) / "malformed.yaml"
        malformed.write_text(FIXTURE.replace("id: daily-primary", "id: [daily-primary]", 1), encoding="utf-8")
        with self.assertRaises(RegistryValidationError):
            load_registry(malformed)

    def test_provenance_fields_bind_record_to_registry_policy(self) -> None:
        source = next(s for s in self.registry.sources if s["id"] == "weekly-browser-index")
        provenance = provenance_fields(self.registry, source, run_cadence="weekly", record_kind="root")
        self.assertEqual(provenance["source_id"], "weekly-browser-index")
        self.assertEqual(provenance["source_role"], "discovery_index")
        self.assertEqual(provenance["source_trust"], "discovery_only")
        self.assertEqual(provenance["promotion_policy"], "original_source_required")
        self.assertTrue(provenance["original_source_required"])
        self.assertEqual(provenance["registry_schema_version"], 2)
        self.assertEqual(provenance["registry_digest"], self.registry.digest)
        self.assertEqual(provenance["record_kind"], "root")


class ReconciliationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        path = Path(self.tmp.name) / "sources.yaml"
        path.write_text(FIXTURE, encoding="utf-8")
        self.registry = load_registry(path)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_weekly_reconciliation_reports_missing_and_degraded_roots(self) -> None:
        by_id = {source["id"]: source for source in self.registry.sources}
        records = [
            {
                **provenance_fields(self.registry, by_id["daily-primary"], run_cadence="weekly", record_kind="root", run_id="weekly-test"),
                "local_processing_status": "fetched_content",
                "content_quality": "actual_content",
            },
            {
                **provenance_fields(self.registry, by_id["weekly-static"], run_cadence="weekly", record_kind="root", run_id="weekly-test"),
                "local_processing_status": "manual_review_required",
                "content_quality": "not_fetched",
                "fetch_error": "TimeoutError",
            },
        ]
        report = reconcile_run(self.registry, records, cadence="weekly", run_id="weekly-test")
        self.assertEqual(report["expected_root_count"], 3)
        self.assertEqual(report["observed_root_count"], 2)
        self.assertEqual(report["missing_source_ids"], ["weekly-browser-index"])
        self.assertEqual(report["degraded_source_ids"], ["weekly-static"])
        self.assertFalse(report["complete"])
        rendered = render_markdown(report, self.registry)
        self.assertIn("Per-source coverage and yield", rendered)
        self.assertIn("weekly-browser-index", rendered)

    def test_reconciliation_rejects_stale_duplicate_and_budget_skipped_roots(self) -> None:
        by_id = {source["id"]: source for source in self.registry.sources}
        good = provenance_fields(self.registry, by_id["daily-primary"], run_cadence="weekly", record_kind="root", run_id="weekly-test")
        stale = provenance_fields(self.registry, by_id["weekly-static"], run_cadence="weekly", record_kind="root", run_id="weekly-test")
        stale["registry_digest"] = "0" * 64
        records = [
            {**good, "local_processing_status": "fetched_content", "content_quality": "actual_content"},
            {**good, "local_processing_status": "fetched_content", "content_quality": "actual_content"},
            {**stale, "local_processing_status": "skipped_group_limit", "content_quality": "not_fetched"},
        ]
        report = reconcile_run(self.registry, records, cadence="weekly", run_id="weekly-test")
        self.assertIn("daily-primary", report["duplicate_root_source_ids"])
        self.assertIn("weekly-static", report["degraded_source_ids"])
        self.assertIn("weekly-static", report["provenance_mismatch_source_ids"])
        self.assertFalse(report["complete"])

    def test_published_manifest_counts_reconciliation_provenance_mismatches(self) -> None:
        run_dir = Path(self.tmp.name) / "weekly-test"
        run_dir.mkdir()
        (run_dir / "learning-reconciliation.json").write_text(
            json.dumps(
                {
                    "complete": False,
                    "missing_source_ids": [],
                    "degraded_source_ids": ["daily-primary", "weekly-static"],
                    "provenance_mismatch_source_ids": ["daily-primary", "weekly-static"],
                }
            ),
            encoding="utf-8",
        )
        manifest = build_manifest(
            registry_path=Path(self.tmp.name) / "sources.yaml",
            run_dir=run_dir,
            cadence="weekly",
            reconciliation_exit=2,
        )
        self.assertEqual(manifest["reconciliation"]["provenance_error_count"], 2)


class StateAndSafetyTests(unittest.TestCase):
    def test_strict_public_ip_rejects_special_and_transition_destinations(self) -> None:
        for address in (
            "127.0.0.1",
            "224.0.0.1",
            "fec0::1",
            "ff02::1",
            "64:ff9b::7f00:1",
            "64:ff9b:1::cb00:7101",
            "::ffff:127.0.0.1",
            "2002:7f00:1::",
        ):
            with self.subTest(address=address):
                self.assertFalse(is_strict_public_ip(address))
        self.assertTrue(is_strict_public_ip("93.184.216.34"))
        self.assertTrue(is_strict_public_ip("2606:4700:4700::1111"))
        self.assertFalse(is_strict_public_ip("64:ff9b::5db8:d822"))

    def test_canonical_url_drops_tracking_and_normalizes_origin(self) -> None:
        self.assertEqual(
            canonical_url("HTTPS://Example.COM:443/a/?utm_source=x&b=2&a=1#frag"),
            "https://example.com/a?a=1&b=2",
        )
        ipv6 = canonical_url("https://[2606:4700:4700::1111]:8443/a")
        self.assertEqual(ipv6, "https://[2606:4700:4700::1111]:8443/a")
        self.assertEqual(urlsplit(ipv6).port, 8443)

    def test_loopback_proxy_validation_is_shared_and_fail_closed(self) -> None:
        self.assertEqual(
            validate_loopback_http_proxy_url("http://127.0.0.1:9219"),
            "http://127.0.0.1:9219",
        )
        for value in (
            "direct://",
            "http://proxy.example:8080",
            "http://user:pass@127.0.0.1:9219",
            "http://127.0.0.1:9219/path",
            "http://127.0.0.1:9219/?query=1",
            "http://127.0.0.1:9219/#fragment",
            "http://127.0.0.1:0",
            "http://127.0.0.1",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_loopback_http_proxy_url(value)

    def test_mandatory_proxy_handler_cannot_honor_no_proxy_bypass(self) -> None:
        opener = build_mandatory_proxy_opener("http://127.0.0.1:9219")
        handler = next(
            item for item in opener.handlers if item.__class__.__name__ == "MandatoryProxyHandler"
        )
        with mock.patch.dict(os.environ, {"NO_PROXY": "*", "no_proxy": "*"}):
            http_request = handler.http_request(Request("http://example.com/a"))
            https_request = handler.https_request(Request("https://example.com/a"))
        self.assertEqual(http_request.host, "127.0.0.1:9219")
        self.assertEqual(http_request.selector, "http://example.com/a")
        self.assertEqual(https_request.host, "127.0.0.1:9219")
        self.assertEqual(https_request._tunnel_host, "example.com")
        self.assertNotIn("FTPHandler", {item.__class__.__name__ for item in opener.handlers})
        redirect = next(item for item in opener.handlers if item.__class__.__name__ == "HTTPOnlyRedirectHandler")
        with self.assertRaises(HTTPError):
            redirect.redirect_request(
                Request("https://example.com/start"), None, 302, "Found", {}, "ftp://127.0.0.1/private"
            )

    def test_mandatory_proxy_reprocesses_http_redirects_and_blocks_ftp_redirects(self) -> None:
        class SyntheticProxy(BaseHTTPRequestHandler):
            mode = "http"
            requests: list[str] = []

            def do_GET(self) -> None:
                self.__class__.requests.append(self.path)
                if self.path.endswith("/start"):
                    self.send_response(302)
                    target = (
                        "http://redirect.example/next"
                        if self.__class__.mode == "http"
                        else "ftp://127.0.0.1/private"
                    )
                    self.send_header("Location", target)
                    self.end_headers()
                    return
                self.send_response(204)
                self.end_headers()

            def log_message(self, *_: object) -> None:
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), SyntheticProxy)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            proxy_url = f"http://127.0.0.1:{server.server_address[1]}"
            with mock.patch.dict(os.environ, {"NO_PROXY": "*", "no_proxy": "*"}):
                with build_mandatory_proxy_opener(proxy_url).open(
                    Request("http://origin.example/start"), timeout=2
                ) as response:
                    self.assertEqual(response.status, 204)
                self.assertEqual(
                    SyntheticProxy.requests,
                    ["http://origin.example/start", "http://redirect.example/next"],
                )
                SyntheticProxy.mode = "ftp"
                SyntheticProxy.requests.clear()
                with self.assertRaises(HTTPError):
                    build_mandatory_proxy_opener(proxy_url).open(
                        Request("http://origin.example/start"), timeout=2
                    )
                self.assertEqual(SyntheticProxy.requests, ["http://origin.example/start"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_corrupt_state_is_quarantined_and_merge_is_atomic(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "state.json"
            path.write_text("{broken", encoding="utf-8")
            warnings: list[str] = []
            self.assertEqual(load_json_state(path, default={"urls": {}}, warn=warnings.append), {"urls": {}})
            self.assertTrue(warnings)
            self.assertTrue(list(path.parent.glob("state.json.corrupt-*")))
            merged = merge_json_state(path, {"urls": {"https://example.com/a": {"last_seen": "2026-01-01T00:00:00+00:00"}}})
            self.assertIn("https://example.com/a", merged["urls"])

    def test_source_health_merge_prefers_newer_last_checked_at(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "health.json"
            path.write_text(
                json.dumps(
                    {
                        "sources": {
                            "source-a": {
                                "last_checked_at": "2026-08-11T05:03:52+00:00",
                                "last_success_at": "2026-08-11T05:03:52+00:00",
                                "last_status": "healthy",
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )
            merged = merge_json_state(
                path,
                {
                    "sources": {
                        "source-a": {
                            "last_checked_at": "2026-08-18T05:00:24+00:00",
                            "last_status": "degraded",
                            "last_reconciled_run_id": "weekly-reconciliation-20260818-070001",
                        }
                    }
                },
            )
            self.assertEqual(merged["sources"]["source-a"]["last_status"], "degraded")
            self.assertEqual(
                merged["sources"]["source-a"]["last_checked_at"],
                "2026-08-18T05:00:24+00:00",
            )

    def test_seen_url_state_migration_atomically_removes_raw_keys(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "seen.json"
            raw_one = "https://example.com/magic/AbCdEfGhIjKlMnOpQrStUvWx?page=1"
            raw_two = "https://example.com/magic/AbCdEfGhIjKlMnOpQrStUvWx?page=2"
            path.write_text(
                json.dumps(
                    {
                        "urls": {
                            raw_one: {"last_seen": "2026-01-01T00:00:00+00:00"},
                            raw_two: {"last_seen": "2026-01-02T00:00:00+00:00"},
                        }
                    }
                ),
                encoding="utf-8",
            )
            migrated = migrate_seen_url_state(path, key=b"m" * 32)
            self.assertEqual(set(migrated["urls"]), {url_identity(raw_one, key=b"m" * 32), url_identity(raw_two, key=b"m" * 32)})
            rendered = path.read_text(encoding="utf-8")
            self.assertNotIn("https://", rendered)
            self.assertNotIn("AbCdEf", rendered)
            self.assertEqual(migrated["url_identity_scheme"], "hmac-sha256")
            self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

    def test_seen_url_state_migration_absorbs_legacy_top_level_raw_url_keys(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "seen.json"
            raw = "https://example.com/reset/abcdefghijklmnopqrstuvwxyz123456"
            path.write_text(
                json.dumps({raw: {"last_seen": "2025-01-01T00:00:00+00:00"}, "urls": {}}),
                encoding="utf-8",
            )
            migrated = migrate_seen_url_state(path, key=b"m" * 32)
            self.assertNotIn(raw, migrated)
            self.assertIn(url_identity(raw, key=b"m" * 32), migrated["urls"])
            self.assertNotIn("https://", path.read_text(encoding="utf-8"))

    def test_seen_url_state_migration_canonicalizes_and_merges_collisions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "seen.json"
            older = "HTTPS://[2606:4700:4700::1111]:443/a/"
            newer = "https://[2606:4700:4700::1111]/a"
            path.write_text(json.dumps({
                older: {"last_seen": "2025-01-01T00:00:00+00:00", "old": True},
                "urls": {newer: {"last_seen": "2026-01-01T00:00:00+00:00", "new": True}},
            }), encoding="utf-8")
            migrated = migrate_seen_url_state(path, key=b"m" * 32)
            identity = url_identity(canonical_url(newer), key=b"m" * 32)
            self.assertEqual(set(migrated["urls"]), {identity})
            self.assertTrue(migrated["urls"][identity]["new"])
            self.assertEqual(migrated["urls"][identity]["last_seen"], "2026-01-01T00:00:00+00:00")

    def test_seen_url_state_migration_normalizes_mixed_timestamps_and_ignores_malformed_for_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "seen.json"
            naive = "HTTPS://EXAMPLE.COM:443/a/?utm_source=legacy"
            aware = "https://example.com/a"
            malformed = "https://example.com/a?utm_campaign=broken"
            path.write_text(json.dumps({"urls": {
                naive: {"last_seen": "2026-01-01T00:00:00", "winner": "naive"},
                aware: {"last_seen": "2026-01-02T00:00:00+00:00", "winner": "aware"},
                malformed: {"last_seen": "not-a-timestamp", "winner": "malformed"},
            }}), encoding="utf-8")
            migrated = migrate_seen_url_state(path, key=b"m" * 32)
            identity = url_identity("https://example.com/a", key=b"m" * 32)
            self.assertEqual(set(migrated["urls"]), {identity})
            self.assertEqual(migrated["urls"][identity]["winner"], "aware")
            self.assertEqual(
                migrated["urls"][identity]["last_seen"],
                "2026-01-02T00:00:00+00:00",
            )

    def test_scope_review_blocks_explicit_abuse_workflows_without_blocking_defense(self) -> None:
        self.assertEqual(scope_disposition("turnkey credential harvester and phishing workflow"), "scope_review_required")
        self.assertEqual(scope_disposition("how to detect and mitigate phishing safely"), "staged_untrusted")


class CompilerProvenanceTests(unittest.TestCase):
    def test_neutral_content_remains_unclassified_and_does_not_match_ai_substrings(self) -> None:
        category, vuln_class, _ = classify({
            "title": "WordPress maintenance release availability notice",
            "url": "https://wordpress.org/news/maintenance-release/",
            "content_excerpt": "A routine maintenance release is available with compatibility fixes.",
            "source_group": "wordpress_official_security_intelligence",
        })
        self.assertEqual(category, "unclassified_candidate")
        self.assertNotEqual(vuln_class, "AI / LLM Security")

    def test_compiler_requires_current_bound_provenance_and_stable_candidate_id(self) -> None:
        record = {
            "source_id": "daily-primary",
            "registry_schema_version": 2,
            "registry_digest": "a" * 64,
            "run_id": "daily-1",
            "run_cadence": "daily",
            "record_kind": "discovered_content",
            "source_role": "primary_research",
            "source_trust": "primary",
            "promotion_policy": "review_required",
            "original_source_required": False,
            "independent_corroboration": "conditional",
            "url": "https://example.test/article",
            "effective_url": "https://example.test/article",
            "content_hash": "b" * 64,
        }
        ok, reasons = provenance_admission(record, expected_registry_digest="a" * 64)
        self.assertTrue(ok, reasons)
        first = candidate_id_for_record(record)
        self.assertEqual(first, candidate_id_for_record(dict(record)))
        self.assertRegex(first, r"^candidate-[0-9a-f]{20}$")
        record["registry_digest"] = "c" * 64
        ok, reasons = provenance_admission(record, expected_registry_digest="a" * 64)
        self.assertFalse(ok)
        self.assertIn("registry_digest_mismatch", reasons)


class PromotionSemanticsTests(unittest.TestCase):
    def test_candidate_classes_are_multi_label_and_bounded(self) -> None:
        text = (
            "A trust-boundary mismatch creates an authorization bypass. "
            "Validation must replay an owned control and preserve response evidence. "
            "Reject the false positive when both roles resolve to the same tenant. "
            "The reusable hunting workflow also improves the parser tool."
        )
        labels = classify_knowledge_types(text)
        self.assertIn("vulnerability_pattern", labels)
        self.assertIn("validation_technique", labels)
        self.assertIn("architecture_trust_boundary", labels)
        self.assertIn("false_positive_condition", labels)
        self.assertIn("evidence_requirement", labels)
        self.assertIn("hunting_methodology", labels)
        self.assertIn("tooling_procedure", labels)

    def test_discovery_material_cannot_bypass_original_source_and_corroboration(self) -> None:
        source = {
            "role": "discovery_index",
            "trust": "discovery_only",
            "promotion_policy": "original_source_required",
            "original_source_required": True,
            "independent_corroboration": "required",
        }
        gate = promotion_requirements(source)
        self.assertEqual(gate["promotion_status"], "proposal_only")
        self.assertTrue(gate["original_source_resolution_required"])
        self.assertEqual(gate["corroboration_required"], "required")
        self.assertTrue(gate["manual_review_required"])

    def test_authority_is_still_reviewed_not_auto_promoted(self) -> None:
        source = {
            "role": "authority",
            "trust": "authority",
            "promotion_policy": "review_required",
            "original_source_required": False,
            "independent_corroboration": "conditional",
        }
        gate = promotion_requirements(source)
        self.assertEqual(gate["promotion_status"], "proposal_only")
        self.assertTrue(gate["manual_review_required"])
        self.assertFalse(gate["original_source_resolution_required"])


if __name__ == "__main__":
    unittest.main()
