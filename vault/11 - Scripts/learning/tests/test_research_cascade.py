from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_DIR))

import research_cascade
from research_cascade import CascadeError, ingest_results, prepare_run, verify_dispositions


class PrepareRunTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / "source.txt"
        self.source.write_text(
            "A front end and back end can interpret the same message differently. "
            "A useful evaluator observes invariant violations rather than one expected exploit. "
            "A negative control uses an unambiguous message.\n\n"
            "Fresh context reduces anchoring on already-known techniques. "
            "Every hypothesis must retain its inspiration lineage. "
            "Unexpected output belongs in a bounded anomaly queue.",
            encoding="utf-8",
        )
        digest = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.contract = self.root / "contract.json"
        self.contract.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "run_id": "unit-cascade",
                    "objective": "Generate testable parser-disagreement hypotheses.",
                    "novelty_definition": "A distinct trigger or evaluator-observable pattern.",
                    "authorization": {
                        "zone": 0,
                        "live_target_interaction": False,
                        "model_input_approved": True,
                        "source_contains_secrets": False,
                    },
                    "source": {
                        "path": str(self.source),
                        "url": "https://example.test/research",
                        "title": "Synthetic research",
                        "sha256": digest,
                        "access_state": "full_article",
                        "sanitization_status": "not_required",
                    },
                    "ideation": {
                        "prohibited_families": ["timeout-only claims"],
                        "hypotheses_per_fragment": 3,
                        "max_fragments": 10,
                        "max_source_bytes": 10000,
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_prepare_rejects_non_private_run_parent(self) -> None:
        public_parent = self.root / "public-parent"
        public_parent.mkdir(mode=0o755)
        public_parent.chmod(0o755)

        with self.assertRaisesRegex(CascadeError, "parent.*mode-private"):
            prepare_run(self.contract, public_parent / "run")
        self.assertFalse((public_parent / "run").exists())

    def test_prepare_collision_rollback_preserves_concurrent_same_name_file(self) -> None:
        run_dir = self.root / "run-concurrent-collision"
        real_write = research_cascade._write_private
        calls = 0

        def insert_same_name_collision(path: Path, content: str, **kwargs: object):
            nonlocal calls
            calls += 1
            if calls == 2:
                run_fd = kwargs["dir_fd"]
                fd = os.open(
                    "fragments.jsonl",
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                    0o600,
                    dir_fd=run_fd,
                )
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write("concurrent sentinel\n")
            return real_write(path, content, **kwargs)

        with mock.patch.object(research_cascade, "_write_private", side_effect=insert_same_name_collision):
            with self.assertRaises(FileExistsError):
                prepare_run(self.contract, run_dir)

        self.assertFalse(run_dir.exists())
        stage_dirs = [path for path in self.root.iterdir() if path.name.startswith(".argus-cascade-stage-")]
        self.assertEqual(len(stage_dirs), 1)
        self.assertEqual((stage_dirs[0] / "fragments.jsonl").read_text(), "concurrent sentinel\n")
        self.assertFalse((stage_dirs[0] / "contract.json").exists())

    def test_prepare_atomic_publication_rejects_concurrent_run_entry(self) -> None:
        run_dir = self.root / "run-publication-race"
        real_write = research_cascade._write_private
        inserted = False

        def insert_concurrent_run(path: Path, content: str, **kwargs: object) -> tuple[int, int]:
            nonlocal inserted
            identity = real_write(path, content, **kwargs)
            if not inserted:
                run_dir.mkdir(mode=0o700)
                sentinel = run_dir / "sentinel.txt"
                sentinel.write_text("preserve\n", encoding="utf-8")
                sentinel.chmod(0o600)
                inserted = True
            return identity

        with mock.patch.object(research_cascade, "_write_private", side_effect=insert_concurrent_run):
            with self.assertRaisesRegex(CascadeError, "already exists"):
                prepare_run(self.contract, run_dir)

        self.assertEqual((run_dir / "sentinel.txt").read_text(encoding="utf-8"), "preserve\n")
        self.assertFalse((run_dir / "contract.json").exists())
        self.assertEqual(
            [path.name for path in self.root.iterdir() if path.name.startswith(".argus-cascade-stage-")],
            [],
        )

    def test_prepare_rejects_nonempty_staging_inode_substitution(self) -> None:
        run_dir = self.root / "run-stage-substitution"
        displaced_stage: Path | None = None
        replacement_stage: Path | None = None
        real_mkdir = os.mkdir

        def replace_staging_after_mkdir(path: object, *args: object, **kwargs: object) -> None:
            nonlocal displaced_stage, replacement_stage
            real_mkdir(path, *args, **kwargs)
            stage_name = os.fspath(path)
            dir_fd = kwargs.get("dir_fd")
            if not isinstance(dir_fd, int) or not stage_name.startswith(".argus-cascade-stage-"):
                return
            parent = Path(os.readlink(f"/proc/self/fd/{dir_fd}"))
            replacement_stage = parent / stage_name
            displaced_stage = parent / f"{stage_name}-original"
            replacement_stage.rename(displaced_stage)
            replacement_stage.mkdir(mode=0o700)
            sentinel = replacement_stage / "sentinel.txt"
            sentinel.write_text("preserve\n", encoding="utf-8")
            sentinel.chmod(0o600)

        try:
            with mock.patch.object(research_cascade.os, "mkdir", side_effect=replace_staging_after_mkdir):
                with self.assertRaisesRegex(CascadeError, "staging directory is not empty"):
                    prepare_run(self.contract, run_dir)

            self.assertFalse(run_dir.exists())
            self.assertIsNotNone(replacement_stage)
            assert replacement_stage is not None
            self.assertEqual((replacement_stage / "sentinel.txt").read_text(), "preserve\n")
            self.assertEqual([path.name for path in replacement_stage.iterdir()], ["sentinel.txt"])
        finally:
            if replacement_stage is not None and replacement_stage.exists():
                shutil.rmtree(replacement_stage)
            if displaced_stage is not None and displaced_stage.exists():
                shutil.rmtree(displaced_stage)

    def test_prepare_staging_is_private_and_rollback_safe_under_restrictive_umask(self) -> None:
        run_dir = self.root / "run-restrictive-umask"
        previous_umask = os.umask(0o777)
        try:
            summary = prepare_run(self.contract, run_dir)
        finally:
            os.umask(previous_umask)

        self.assertEqual(summary["run_id"], "unit-cascade")
        self.assertEqual(stat.S_IMODE(run_dir.stat().st_mode), 0o700)
        self.assertEqual(
            [path.name for path in self.root.iterdir() if path.name.startswith(".argus-cascade-stage-")],
            [],
        )

    def test_prepare_detects_replaced_run_path_before_success(self) -> None:
        run_dir = self.root / "run-success-race"
        displaced = self.root / "displaced-success-run"
        victim = self.root / "success-victim"
        victim.mkdir()
        sentinel = victim / "sentinel.txt"
        sentinel.write_text("must survive\n", encoding="utf-8")
        real_verify = research_cascade._verify_run_identity

        def replace_after_publication(parent_fd: int, run_name: str, run_identity: tuple[int, int]) -> None:
            run_dir.rename(displaced)
            run_dir.symlink_to(victim, target_is_directory=True)
            real_verify(parent_fd, run_name, run_identity)

        try:
            with mock.patch.object(research_cascade, "_verify_run_identity", side_effect=replace_after_publication):
                with self.assertRaisesRegex(CascadeError, "identity changed"):
                    prepare_run(self.contract, run_dir)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "must survive\n")
            self.assertEqual(list(displaced.iterdir()), [])
        finally:
            if run_dir.is_symlink():
                run_dir.unlink()
            if displaced.exists():
                shutil.rmtree(displaced)

    def test_prepare_rejects_parent_path_rebinding_and_rolls_back_published_run(self) -> None:
        private_parent = self.root / "prepare-parent"
        private_parent.mkdir(mode=0o700)
        run_dir = private_parent / "run"
        displaced_parent = self.root / "prepare-parent-displaced"
        real_verify = research_cascade._verify_run_identity
        rebound = False

        def rebind_parent_after_publication(
            parent_fd: int,
            run_name: str,
            run_identity: tuple[int, int],
        ) -> None:
            nonlocal rebound
            real_verify(parent_fd, run_name, run_identity)
            if not rebound:
                private_parent.rename(displaced_parent)
                private_parent.mkdir(mode=0o700)
                rebound = True

        with mock.patch.object(
            research_cascade,
            "_verify_run_identity",
            side_effect=rebind_parent_after_publication,
        ):
            with self.assertRaisesRegex(CascadeError, "parent identity changed"):
                prepare_run(self.contract, run_dir)

        self.assertFalse((displaced_parent / "run").exists())
        self.assertFalse(run_dir.exists())

    def test_prepare_cleanup_does_not_follow_replaced_run_path(self) -> None:
        run_dir = self.root / "run-race"
        displaced = self.root / "displaced-run"
        victim = self.root / "victim"
        victim.mkdir()
        sentinel = victim / "sentinel.txt"
        sentinel.write_text("must survive\n", encoding="utf-8")
        def replace_after_publication(*_args: object, **_kwargs: object) -> None:
            run_dir.rename(displaced)
            run_dir.symlink_to(victim, target_is_directory=True)
            raise OSError("injected post-publication failure")

        with mock.patch.object(research_cascade, "_verify_run_identity", side_effect=replace_after_publication):
            with self.assertRaisesRegex(OSError, "injected"):
                prepare_run(self.contract, run_dir)

        self.assertEqual(sentinel.read_text(encoding="utf-8"), "must survive\n")
        self.assertEqual(list(displaced.iterdir()), [])
        self.assertTrue(run_dir.is_symlink())
        run_dir.unlink()
        shutil.rmtree(displaced)

    def test_prepare_emits_private_attributed_micro_inspiration_packets(self) -> None:
        run_dir = self.root / "run"

        summary = prepare_run(self.contract, run_dir)

        self.assertEqual(summary["run_id"], "unit-cascade")
        self.assertGreaterEqual(summary["fragment_count"], 2)
        self.assertEqual(stat.S_IMODE(run_dir.stat().st_mode), 0o700)
        for path in run_dir.iterdir():
            if path.is_file():
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)

        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        packets = [json.loads(line) for line in (run_dir / "task-packets.jsonl").read_text().splitlines()]
        self.assertEqual(len(fragments), len(packets))
        self.assertEqual({row["fragment_id"] for row in fragments}, {row["fragment_id"] for row in packets})
        self.assertTrue(all(1 <= row["sentence_count"] <= 3 for row in fragments))
        self.assertTrue(all(row["source_sha256"] == hashlib.sha256(self.source.read_bytes()).hexdigest() for row in fragments))
        self.assertTrue(all(row["promotion_status"] == "proposal_only" for row in packets))
        self.assertTrue(all("Return JSON only" in row["prompt"] for row in packets))
        self.assertTrue(all("A front end" not in row["prompt"] or "Fresh context" not in row["prompt"] for row in packets))

        manifest = json.loads((run_dir / "run-manifest.json").read_text())
        self.assertEqual(manifest["source"]["sha256"], hashlib.sha256(self.source.read_bytes()).hexdigest())
        self.assertEqual(manifest["network_calls"], 0)
        self.assertEqual(manifest["target_interactions"], 0)
        for name, digest in manifest["prepared_artifacts_sha256"].items():
            self.assertEqual(digest, hashlib.sha256((run_dir / name).read_bytes()).hexdigest())

    def test_prepare_rejects_live_target_contract(self) -> None:
        contract = json.loads(self.contract.read_text())
        contract["authorization"]["live_target_interaction"] = True
        self.contract.write_text(json.dumps(contract), encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "live_target_interaction"):
            prepare_run(self.contract, self.root / "run")

    def test_prepare_rejects_source_hash_mismatch(self) -> None:
        self.source.write_text("changed", encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "sha256"):
            prepare_run(self.contract, self.root / "run")

    def test_prepare_rejects_secret_material_despite_false_declaration(self) -> None:
        self.source.write_text(
            "Synthetic credential fixture " + "AKIA" + "A" * 16 + " must not reach model input.\n",
            encoding="utf-8",
        )
        contract = json.loads(self.contract.read_text())
        contract["source"]["sha256"] = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.contract.write_text(json.dumps(contract), encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "secret"):
            prepare_run(self.contract, self.root / "run-secret")
        self.assertFalse((self.root / "run-secret").exists())

    def test_prepare_rejects_symlinked_contract_and_source(self) -> None:
        contract_link = self.root / "contract-link.json"
        contract_link.symlink_to(self.contract)
        with self.assertRaisesRegex(CascadeError, "symlink"):
            prepare_run(contract_link, self.root / "run-contract-link")

        source_link = self.root / "source-link.txt"
        source_link.symlink_to(self.source)
        contract = json.loads(self.contract.read_text())
        contract["source"]["path"] = str(source_link)
        self.contract.write_text(json.dumps(contract), encoding="utf-8")
        with self.assertRaisesRegex(CascadeError, "symlink"):
            prepare_run(self.contract, self.root / "run-source-link")

    def test_prepare_emits_canonical_validated_contract_values(self) -> None:
        contract = json.loads(self.contract.read_text())
        contract["run_id"] = "  canonical-run  "
        contract["objective"] = "  Narrow objective.  "
        contract["novelty_definition"] = "  Distinct boundary.  "
        contract["source"]["path"] = f"  {self.source}  "
        contract["source"]["url"] = "  https://example.test/research  "
        contract["source"]["title"] = "  Reviewed source  "
        contract["ideation"]["prohibited_families"] = ["  duplicate family  "]
        self.contract.write_text(json.dumps(contract), encoding="utf-8")

        summary = prepare_run(self.contract, self.root / "canonical-run")
        emitted = json.loads((self.root / "canonical-run" / "contract.json").read_text())

        self.assertEqual(summary["run_id"], "canonical-run")
        self.assertEqual(emitted["objective"], "Narrow objective.")
        self.assertEqual(emitted["novelty_definition"], "Distinct boundary.")
        self.assertEqual(emitted["source"]["path"], str(self.source))
        self.assertEqual(emitted["source"]["url"], "https://example.test/research")
        self.assertEqual(emitted["source"]["title"], "Reviewed source")
        self.assertEqual(emitted["ideation"]["prohibited_families"], ["duplicate family"])

    def test_prepare_rejects_oversized_raw_prohibited_family(self) -> None:
        contract = json.loads(self.contract.read_text())
        contract["ideation"]["prohibited_families"] = [" " * 2_000 + "x"]
        self.contract.write_text(json.dumps(contract), encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "prohibited_families"):
            prepare_run(self.contract, self.root / "run-raw-prohibited")

        self.assertFalse((self.root / "run-raw-prohibited").exists())

    def test_prepare_maximum_task_packet_set_is_ingest_compatible(self) -> None:
        sentence = "A" * 7_998 + "."
        self.source.write_text("\n\n".join(sentence for _ in range(100)), encoding="utf-8")
        contract = json.loads(self.contract.read_text())
        contract["objective"] = "O" * 4_000
        contract["novelty_definition"] = "N" * 4_000
        contract["source"]["title"] = "T" * 1_000
        contract["source"]["sha256"] = hashlib.sha256(self.source.read_bytes()).hexdigest()
        contract["ideation"].update(
            {
                "prohibited_families": ["P" * 1_000 for _ in range(3)],
                "hypotheses_per_fragment": 5,
                "max_fragments": 100,
                "max_source_bytes": 5_000_000,
            }
        )
        self.contract.write_text(json.dumps(contract), encoding="utf-8")
        run_dir = self.root / "run-maximum-compatible-artifact"

        prepared = prepare_run(self.contract, run_dir)
        task_packet_bytes = (run_dir / "task-packets.jsonl").read_bytes()
        packets = [json.loads(line) for line in task_packet_bytes.splitlines()]
        self.assertEqual(len(packets), 100)
        self.assertTrue(all(len(packet["prompt"]) <= 20_000 for packet in packets))
        self.assertLessEqual(len(task_packet_bytes), research_cascade._MAX_RESULTS_BYTES)

        results_path = self.root / "maximum-compatible-results.jsonl"
        results_path.write_text(
            "".join(json.dumps(self._valid_result(packet["fragment_id"])) + "\n" for packet in packets),
            encoding="utf-8",
        )
        ingested = ingest_results(run_dir, results_path, prepared["manifest_sha256"])
        self.assertEqual(ingested["result_count"], 100)

    def test_prepare_rejects_raw_text_that_exceeds_emission_bound(self) -> None:
        cases = (
            ("objective", " " * 4_000 + "x", "objective exceeds 4000"),
            ("run_id", " " * 80 + "x", "run_id exceeds 80"),
            ("source.sha256", " " * 64 + ("0" * 64), "sha256 exceeds 64"),
        )
        for index, (field, value, message) in enumerate(cases):
            with self.subTest(field=field):
                contract = json.loads(self.contract.read_text())
                if field == "source.sha256":
                    contract["source"]["sha256"] = value
                else:
                    contract[field] = value
                self.contract.write_text(json.dumps(contract), encoding="utf-8")
                run_dir = self.root / f"run-raw-bound-{index}"

                with self.assertRaisesRegex(CascadeError, message):
                    prepare_run(self.contract, run_dir)

                self.assertFalse(run_dir.exists())
                self.contract.unlink(missing_ok=True)
                self.setUp_contract()

    def test_prepare_rejects_capability_style_source_url(self) -> None:
        capability_urls = (
            "https://example.test/research?token=secret",
            "https://example.test/share/A7qP9mK2vX8cR4tN6wY1zB3dF5hJ0sL",
            "https://example.test/download/%41%37%71%50%39%6d%4b%32%76%58%38%63%52%34%74%4e%36%77%59%31%7a%42%33%64%46%35%68%4a%30%73%4c",
            "https://example.test/reset/123456",
            "https://example.test/research/550e8400-e29b-41d4-a716-446655440000",
            "https://example.test/research/0123456789abcdef01234567",
            "https://example.test/research/0123456789abcdef01234567;ignored",
            "https://example.test/research/A7qP9mK2vX8cR4tN6wY1zB3dF5hJ0sL%zz",
            "https://example.test/%72esearch",
            "https://example.test/research/%ZZ",
            "https://example.test/magic%252F654321",
            "https://example.test/magic%2525252F654321",
            "http://127.0.0.1/research",
            "http://127.1/research",
            "http://2130706433/research",
            "http://localhost/research",
            "https://intranet/research",
            "http://169.254.169.254/latest",
            "https://example.test/%2e%2e/private",
            "https://example.test/a%5cb",
            "https://example.test/a%253fb",
        )
        for index, source_url in enumerate(capability_urls):
            with self.subTest(source_url=source_url):
                contract = json.loads(self.contract.read_text())
                contract["source"]["url"] = source_url
                self.contract.write_text(json.dumps(contract), encoding="utf-8")
                with self.assertRaisesRegex(CascadeError, "source.url"):
                    prepare_run(self.contract, self.root / f"run-capability-{index}")
                self.contract.unlink(missing_ok=True)
                self.setUp_contract()

    def test_prepare_rejects_malformed_urls_with_controlled_error(self) -> None:
        malformed_urls = (
            "https://[invalid/research",
            "https://example.test:bad/research",
            "https://@example.test/research",
            "https://:@example.test/research",
            "https://example.test:/research",
            "https://example.test/research\x7ftrail",
            "https://example.test/research%7Ftrail",
            "https://[2606:4700:4700::1111%25eth0]/research",
        )
        for index, source_url in enumerate(malformed_urls):
            with self.subTest(source_url=source_url):
                contract = json.loads(self.contract.read_text())
                contract["source"]["url"] = source_url
                self.contract.write_text(json.dumps(contract), encoding="utf-8")
                with self.assertRaisesRegex(CascadeError, "source.url"):
                    prepare_run(self.contract, self.root / f"malformed-url-{index}")
                self.contract.unlink(missing_ok=True)
                self.setUp_contract()

    def test_prepare_accepts_canonical_global_ipv6_provenance_literal(self) -> None:
        contract = json.loads(self.contract.read_text())
        contract["source"]["url"] = "https://[2606:4700:4700::1111]/research"
        self.contract.write_text(json.dumps(contract), encoding="utf-8")

        summary = prepare_run(self.contract, self.root / "global-ipv6")

        self.assertEqual(summary["run_id"], "unit-cascade")

    def setUp_contract(self) -> None:
        digest = hashlib.sha256(self.source.read_bytes()).hexdigest()
        self.contract.write_text(json.dumps({
            "schema_version": 1,
            "run_id": "unit-cascade",
            "objective": "Generate testable parser-disagreement hypotheses.",
            "novelty_definition": "A distinct trigger or evaluator-observable pattern.",
            "authorization": {"zone": 0, "live_target_interaction": False, "model_input_approved": True, "source_contains_secrets": False},
            "source": {"path": str(self.source), "url": "https://example.test/research", "title": "Synthetic research", "sha256": digest, "access_state": "full_article", "sanitization_status": "not_required"},
            "ideation": {"prohibited_families": ["timeout-only claims"], "hypotheses_per_fragment": 3, "max_fragments": 10, "max_source_bytes": 10000},
        }), encoding="utf-8")

    def test_prepare_rejects_boolean_schema_version_and_zone(self) -> None:
        contract = json.loads(self.contract.read_text())
        contract["schema_version"] = True
        self.contract.write_text(json.dumps(contract), encoding="utf-8")
        with self.assertRaisesRegex(CascadeError, "schema_version"):
            prepare_run(self.contract, self.root / "run")

        self.setUp_contract()
        contract = json.loads(self.contract.read_text())
        contract["authorization"]["zone"] = False
        self.contract.write_text(json.dumps(contract), encoding="utf-8")
        with self.assertRaisesRegex(CascadeError, "zone"):
            prepare_run(self.contract, self.root / "run")

    def test_prepare_rejects_oversized_single_sentence_fragment(self) -> None:
        self.source.write_text("A" * 12001, encoding="utf-8")
        contract = json.loads(self.contract.read_text())
        contract["source"]["sha256"] = hashlib.sha256(self.source.read_bytes()).hexdigest()
        contract["ideation"]["max_source_bytes"] = 20000
        self.contract.write_text(json.dumps(contract), encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "fragment exceeds"):
            prepare_run(self.contract, self.root / "run")

    def test_prepare_rejects_oversized_contract_text(self) -> None:
        contract = json.loads(self.contract.read_text())
        contract["objective"] = "O" * 5000
        self.contract.write_text(json.dumps(contract), encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "objective exceeds"):
            prepare_run(self.contract, self.root / "run")

    def test_prepare_rejects_task_packet_prompt_incompatible_with_ingest(self) -> None:
        contract = json.loads(self.contract.read_text())
        contract["objective"] = "O" * 4_000
        contract["novelty_definition"] = "N" * 4_000
        contract["ideation"]["prohibited_families"] = [f"P{index}-" + ("x" * 995) for index in range(20)]
        self.contract.write_text(json.dumps(contract), encoding="utf-8")
        run_dir = self.root / "prompt-incompatible"

        with self.assertRaisesRegex(CascadeError, "prompt exceeds 20000 characters"):
            prepare_run(self.contract, run_dir)

        self.assertFalse(run_dir.exists())
        self.assertEqual(
            [path.name for path in self.root.iterdir() if path.name.startswith(".argus-cascade-stage-")],
            [],
        )

    def test_prepare_rejects_undeclared_contract_fields(self) -> None:
        contract = json.loads(self.contract.read_text())
        contract["private_note"] = "must not be retained silently"
        self.contract.write_text(json.dumps(contract), encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "unexpected fields"):
            prepare_run(self.contract, self.root / "run")

    def test_prepare_rejects_oversized_contract_file_before_parsing(self) -> None:
        self.contract.write_text("{" + (" " * 1_000_001) + "}", encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "contract JSON exceeds"):
            prepare_run(self.contract, self.root / "run")

    def _prepare(self, name: str = "run") -> Path:
        run_dir = self.root / name
        summary = prepare_run(self.contract, run_dir)
        self.manifest_sha256 = summary["manifest_sha256"]
        return run_dir

    def _valid_result(self, fragment_id: str, *, title: str = "Parser differential") -> dict:
        return {
            "fragment_id": fragment_id,
            "hypotheses": [
                {
                    "title": title,
                    "mechanism": "Two supported components normalize one field differently.",
                    "invariant": "Both components must agree on the message boundary.",
                    "safe_evaluator": "Use an owned fixed-source parser fixture with a benign canary.",
                    "expected_observation": "The fixture records different parsed boundaries.",
                    "negative_control": "An unambiguous message yields identical boundaries.",
                    "assumptions": ["Both components are present in the fixture."],
                    "prior_art_queries": ["parser boundary differential prior art"],
                }
            ],
        }

    def _repin_run_manifest(self, run_dir: Path, manifest: dict) -> str:
        manifest_path = run_dir / "run-manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return hashlib.sha256(manifest_path.read_bytes()).hexdigest()

    def _repin_prepared_artifact(self, run_dir: Path, name: str, content: str) -> str:
        artifact = run_dir / name
        artifact.write_text(content, encoding="utf-8")
        manifest = json.loads((run_dir / "run-manifest.json").read_text())
        manifest["prepared_artifacts_sha256"][name] = hashlib.sha256(artifact.read_bytes()).hexdigest()
        return self._repin_run_manifest(run_dir, manifest)

    def test_ingest_rejects_recursively_malformed_run_manifest_fields(self) -> None:
        mutations = (
            ("created_at", lambda manifest: manifest.__setitem__("created_at", False)),
            ("objective", lambda manifest: manifest.__setitem__("objective", [])),
            ("novelty_definition", lambda manifest: manifest.__setitem__("novelty_definition", "x" * 5000)),
            ("source.path", lambda manifest: manifest["source"].__setitem__("path", {})),
            ("source.url", lambda manifest: manifest["source"].__setitem__("url", "https://example.test/research?token=x")),
            ("source.title", lambda manifest: manifest["source"].__setitem__("title", False)),
            ("source.access_state", lambda manifest: manifest["source"].__setitem__("access_state", "summary")),
            ("source.sanitization_status", lambda manifest: manifest["source"].__setitem__("sanitization_status", 1)),
            ("prohibited_families", lambda manifest: manifest["ideation"].__setitem__("prohibited_families", [False])),
            ("prepared digest", lambda manifest: manifest["prepared_artifacts_sha256"].__setitem__("README.md", False)),
        )
        for index, (label, mutate) in enumerate(mutations):
            with self.subTest(label=label):
                run_dir = self._prepare(f"malformed-manifest-{index}")
                manifest = json.loads((run_dir / "run-manifest.json").read_text())
                mutate(manifest)
                manifest_sha256 = self._repin_run_manifest(run_dir, manifest)
                fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
                results_path = self.root / f"malformed-manifest-{index}.jsonl"
                results_path.write_text(
                    "".join(json.dumps(self._valid_result(row["fragment_id"])) + "\n" for row in fragments),
                    encoding="utf-8",
                )
                with self.assertRaises(CascadeError):
                    ingest_results(run_dir, results_path, manifest_sha256)

    def test_ingest_rejects_recursively_malformed_fragment_fields(self) -> None:
        mutations = (
            ("schema_version", lambda row: row.__setitem__("schema_version", True)),
            ("fragment_id", lambda row: row.__setitem__("fragment_id", "fragment-invalid")),
            ("text", lambda row: row.__setitem__("text", False)),
            ("sentence_count", lambda row: row.__setitem__("sentence_count", True)),
            ("source_path", lambda row: row.__setitem__("source_path", [])),
            ("source_url", lambda row: row.__setitem__("source_url", "https://other.test/research")),
            ("source_title", lambda row: row.__setitem__("source_title", {})),
            ("source_sha256", lambda row: row.__setitem__("source_sha256", "0" * 64)),
            ("access_state", lambda row: row.__setitem__("access_state", "summary")),
            ("sanitization_status", lambda row: row.__setitem__("sanitization_status", 1)),
        )
        for index, (label, mutate) in enumerate(mutations):
            with self.subTest(label=label):
                run_dir = self._prepare(f"malformed-fragment-{index}")
                fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
                mutate(fragments[0])
                manifest_sha256 = self._repin_prepared_artifact(
                    run_dir,
                    "fragments.jsonl",
                    "".join(json.dumps(row, sort_keys=True) + "\n" for row in fragments),
                )
                results_path = self.root / f"malformed-fragment-{index}.jsonl"
                results_path.write_text(
                    "".join(json.dumps(self._valid_result(row["fragment_id"])) + "\n" for row in fragments),
                    encoding="utf-8",
                )
                with self.assertRaises(CascadeError):
                    ingest_results(run_dir, results_path, manifest_sha256)

    def test_ingest_rejects_recursively_malformed_task_packets(self) -> None:
        mutations = (
            ("schema_version", lambda row: row.__setitem__("schema_version", True)),
            ("run_id", lambda row: row.__setitem__("run_id", "other-run")),
            ("task_id", lambda row: row.__setitem__("task_id", False)),
            ("fragment_id", lambda row: row.__setitem__("fragment_id", "fragment-9999-deadbeefdead")),
            ("phase", lambda row: row.__setitem__("phase", "evaluation")),
            ("toolsets", lambda row: row.__setitem__("toolsets", ["web"])),
            ("network_allowed", lambda row: row.__setitem__("network_allowed", 0)),
            ("target_interaction_allowed", lambda row: row.__setitem__("target_interaction_allowed", 0)),
            ("promotion_status", lambda row: row.__setitem__("promotion_status", "promoted")),
            ("prompt", lambda row: row.__setitem__("prompt", [])),
        )
        for index, (label, mutate) in enumerate(mutations):
            with self.subTest(label=label):
                run_dir = self._prepare(f"malformed-packet-{index}")
                packets = [json.loads(line) for line in (run_dir / "task-packets.jsonl").read_text().splitlines()]
                mutate(packets[0])
                manifest_sha256 = self._repin_prepared_artifact(
                    run_dir,
                    "task-packets.jsonl",
                    "".join(json.dumps(row, sort_keys=True) + "\n" for row in packets),
                )
                fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
                results_path = self.root / f"malformed-packet-{index}.jsonl"
                results_path.write_text(
                    "".join(json.dumps(self._valid_result(row["fragment_id"])) + "\n" for row in fragments),
                    encoding="utf-8",
                )
                with self.assertRaises(CascadeError):
                    ingest_results(run_dir, results_path, manifest_sha256)

    def test_verify_dispositions_rejects_malformed_ingestion_metadata(self) -> None:
        mutations = (
            ("ingested_at", False),
            ("result_count", True),
            ("normalized_hypothesis_count", False),
        )
        for index, (field, value) in enumerate(mutations):
            with self.subTest(field=field):
                run_dir, hypothesis = self._ingested_run(f"malformed-ingestion-{index}")
                ingestion_path = run_dir / "ingestion-manifest.json"
                ingestion = json.loads(ingestion_path.read_text())
                ingestion[field] = value
                ingestion_path.write_text(json.dumps(ingestion, indent=2, sort_keys=True) + "\n", encoding="utf-8")
                ingestion_sha256 = hashlib.sha256(ingestion_path.read_bytes()).hexdigest()
                dispositions = self.root / f"malformed-ingestion-{index}.jsonl"
                dispositions.write_text(json.dumps({
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "coverage_gap",
                    "reason": "The evaluator remains unavailable.",
                    "evidence_refs": [],
                    "next_safe_action": "Build the owned deterministic evaluator.",
                }) + "\n", encoding="utf-8")
                with self.assertRaises(CascadeError):
                    verify_dispositions(
                        run_dir,
                        dispositions,
                        self.manifest_sha256,
                        ingestion_sha256,
                    )

    def test_ingest_rejects_parent_path_rebinding_and_rolls_back_outputs(self) -> None:
        private_parent = self.root / "ingest-parent"
        private_parent.mkdir(mode=0o700)
        run_dir = private_parent / "run"
        summary = prepare_run(self.contract, run_dir)
        self.manifest_sha256 = summary["manifest_sha256"]
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        results_path = self.root / "ingest-parent-results.jsonl"
        results_path.write_text(
            "".join(json.dumps(self._valid_result(fragment["fragment_id"])) + "\n" for fragment in fragments),
            encoding="utf-8",
        )
        displaced_parent = self.root / "ingest-parent-displaced"
        real_write = research_cascade._write_private
        rebound = False

        def rebind_parent_before_ledger(path: Path, content: str, **kwargs: object) -> tuple[int, int]:
            nonlocal rebound
            if not rebound and Path(path).name == "hypothesis-ledger.jsonl":
                private_parent.rename(displaced_parent)
                private_parent.mkdir(mode=0o700)
                rebound = True
            return real_write(path, content, **kwargs)

        with mock.patch.object(research_cascade, "_write_private", side_effect=rebind_parent_before_ledger):
            with self.assertRaisesRegex(CascadeError, "parent identity changed"):
                ingest_results(run_dir, results_path, self.manifest_sha256)

        self.assertFalse((displaced_parent / "run" / "hypothesis-ledger.jsonl").exists())
        self.assertFalse((displaced_parent / "run" / "ingestion-manifest.json").exists())
        self.assertFalse(run_dir.exists())

    def test_ingest_rejects_run_path_replacement_without_touching_replacement(self) -> None:
        run_dir = self._prepare("ingest-race")
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        results_path = self.root / "ingest-race-results.jsonl"
        results_path.write_text(
            "".join(json.dumps(self._valid_result(fragment["fragment_id"])) + "\n" for fragment in fragments),
            encoding="utf-8",
        )
        displaced = self.root / "ingest-race-displaced"
        replacement = self.root / "ingest-race-replacement"
        replacement.mkdir(mode=0o700)
        sentinel = replacement / "sentinel.txt"
        sentinel.write_text("preserve", encoding="utf-8")
        sentinel.chmod(0o600)
        real_write = research_cascade._write_private
        replaced = False

        def replace_before_write(path: Path, content: str, **kwargs: object) -> None:
            nonlocal replaced
            if not replaced and Path(path).name == "hypothesis-ledger.jsonl":
                run_dir.rename(displaced)
                replacement.rename(run_dir)
                replaced = True
            real_write(path, content, **kwargs)

        with mock.patch.object(research_cascade, "_write_private", side_effect=replace_before_write):
            with self.assertRaisesRegex(CascadeError, "identity changed"):
                ingest_results(run_dir, results_path, self.manifest_sha256)

        self.assertEqual((run_dir / "sentinel.txt").read_text(), "preserve")
        self.assertFalse((run_dir / "hypothesis-ledger.jsonl").exists())
        self.assertFalse((run_dir / "ingestion-manifest.json").exists())
        self.assertFalse((displaced / "hypothesis-ledger.jsonl").exists())
        self.assertFalse((displaced / "ingestion-manifest.json").exists())

    def test_ingest_normalizes_and_deduplicates_hypotheses(self) -> None:
        run_dir = self._prepare()
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        results_path = self.root / "results.jsonl"
        rows = [
            self._valid_result(fragments[0]["fragment_id"]),
            self._valid_result(fragments[1]["fragment_id"], title="  parser   differential  "),
        ]
        results_path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")

        summary = ingest_results(run_dir, results_path, self.manifest_sha256)

        self.assertEqual(summary["result_count"], 2)
        self.assertEqual(summary["normalized_hypothesis_count"], 1)
        ledger = [json.loads(line) for line in (run_dir / "hypothesis-ledger.jsonl").read_text().splitlines()]
        self.assertEqual(len(ledger), 1)
        self.assertEqual(len(ledger[0]["lineage"]), 2)
        self.assertEqual(ledger[0]["state"], "hypothesis")
        self.assertEqual(ledger[0]["promotion_status"], "proposal_only")
        self.assertEqual(stat.S_IMODE((run_dir / "hypothesis-ledger.jsonl").stat().st_mode), 0o600)

    def test_ingest_preserves_distinct_hypotheses_with_shared_legacy_id_prefix(self) -> None:
        run_dir = self._prepare("identity-prefix-collision")
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        rows = [self._valid_result(fragment["fragment_id"], title=f"Distinct title {index}") for index, fragment in enumerate(fragments)]
        results_path = self.root / "identity-prefix-collision-results.jsonl"
        results_path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")
        shared_prefix = "a" * 20
        identities = iter((shared_prefix + "1" * 44, shared_prefix + "2" * 44))

        with mock.patch.object(research_cascade, "_hypothesis_identity", side_effect=lambda _row: next(identities)):
            summary = ingest_results(run_dir, results_path, self.manifest_sha256)

        ledger = [json.loads(line) for line in (run_dir / "hypothesis-ledger.jsonl").read_text().splitlines()]
        self.assertEqual(summary["normalized_hypothesis_count"], 2)
        self.assertEqual(
            {row["hypothesis_id"] for row in ledger},
            {f"hypothesis-{shared_prefix}{'1' * 44}", f"hypothesis-{shared_prefix}{'2' * 44}"},
        )

    def test_ingest_rejects_unknown_fragment_and_extra_fields(self) -> None:
        run_dir = self._prepare()
        unknown = self._valid_result("fragment-9999-deadbeefdead")
        unknown["hypotheses"][0]["payload"] = "not part of the contract"
        results_path = self.root / "results.jsonl"
        results_path.write_text(json.dumps(unknown) + "\n", encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "unknown fragment|unexpected fields"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

    def test_ingest_requires_exactly_one_result_per_fragment(self) -> None:
        run_dir = self._prepare()
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        results_path = self.root / "results.jsonl"
        one = self._valid_result(fragments[0]["fragment_id"])
        results_path.write_text(json.dumps(one) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(CascadeError, "missing results"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

        results_path.write_text(json.dumps(one) + "\n" + json.dumps(one) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(CascadeError, "duplicate result"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

    def test_ingest_rejects_oversized_raw_hypothesis_text_and_list_items(self) -> None:
        cases = (
            ("mechanism", " " * 10_000 + "x", "mechanism exceeds"),
            ("assumptions", [" " * 2_000 + "x"], "assumptions item exceeds"),
        )
        for index, (field, value, message) in enumerate(cases):
            with self.subTest(field=field):
                run_dir = self._prepare(f"raw-hypothesis-bound-{index}")
                fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
                rows = [self._valid_result(fragment["fragment_id"]) for fragment in fragments]
                rows[0]["hypotheses"][0][field] = value
                results_path = self.root / f"raw-hypothesis-bound-{index}.jsonl"
                results_path.write_text(
                    "".join(json.dumps(row) + "\n" for row in rows),
                    encoding="utf-8",
                )

                with self.assertRaisesRegex(CascadeError, message):
                    ingest_results(run_dir, results_path, self.manifest_sha256)

                self.assertFalse((run_dir / "hypothesis-ledger.jsonl").exists())
                self.assertFalse((run_dir / "ingestion-manifest.json").exists())

    def test_ingest_rejects_ledger_larger_than_closure_admission_ceiling(self) -> None:
        self.source.write_text(
            "\n\n".join(f"Distinct parser boundary sentence {index}." for index in range(100)),
            encoding="utf-8",
        )
        contract = json.loads(self.contract.read_text())
        contract["source"]["sha256"] = hashlib.sha256(self.source.read_bytes()).hexdigest()
        contract["ideation"].update(
            {"hypotheses_per_fragment": 5, "max_fragments": 100, "max_source_bytes": 100_000}
        )
        self.contract.write_text(json.dumps(contract), encoding="utf-8")
        run_dir = self._prepare("oversized-ledger")
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        rows = []
        for fragment_index, fragment in enumerate(fragments):
            hypotheses = []
            for hypothesis_index in range(5):
                hypothesis = self._valid_result(fragment["fragment_id"], title=f"Distinct {fragment_index}-{hypothesis_index}")["hypotheses"][0]
                hypothesis["mechanism"] = "M" * 4_000
                hypothesis["invariant"] = "I" * 4_000
                hypothesis["safe_evaluator"] = "E" * 1_600
                hypotheses.append(hypothesis)
            rows.append({"fragment_id": fragment["fragment_id"], "hypotheses": hypotheses})
        results_path = self.root / "oversized-ledger-results.jsonl"
        results_path.write_text(
            "".join(json.dumps(row) + "\n" for row in rows),
            encoding="utf-8",
        )
        self.assertLess(results_path.stat().st_size, research_cascade._MAX_RESULTS_BYTES)

        with self.assertRaisesRegex(CascadeError, "hypothesis ledger JSONL exceeds 5000000 bytes"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

        self.assertFalse((run_dir / "hypothesis-ledger.jsonl").exists())
        self.assertFalse((run_dir / "ingestion-manifest.json").exists())

    def test_ingest_rejects_json_escaped_lone_surrogate_without_traceback(self) -> None:
        cases = (("title", "\ud800"), ("assumptions", ["\ud800"]))
        for index, (field, value) in enumerate(cases):
            with self.subTest(field=field):
                run_dir = self._prepare(f"surrogate-result-{index}")
                fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
                rows = [self._valid_result(fragment["fragment_id"]) for fragment in fragments]
                rows[0]["hypotheses"][0][field] = value
                results_path = self.root / f"surrogate-result-{index}.jsonl"
                results_path.write_text(
                    "".join(json.dumps(row) + "\n" for row in rows),
                    encoding="utf-8",
                )

                with self.assertRaisesRegex(CascadeError, "valid Unicode text"):
                    ingest_results(run_dir, results_path, self.manifest_sha256)

                self.assertFalse((run_dir / "hypothesis-ledger.jsonl").exists())
                self.assertFalse((run_dir / "ingestion-manifest.json").exists())

    def test_ingest_rejects_malformed_fragment_identifier_types(self) -> None:
        for index, malformed in enumerate(([], {}, 1, True, None)):
            with self.subTest(malformed=malformed):
                run_dir = self.root / f"malformed-id-run-{index}"
                summary = prepare_run(self.contract, run_dir)
                fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
                rows = [self._valid_result(fragment["fragment_id"]) for fragment in fragments]
                rows[0]["fragment_id"] = malformed
                results_path = self.root / f"malformed-id-{index}.jsonl"
                results_path.write_text(
                    "".join(json.dumps(row) + "\n" for row in rows),
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(CascadeError, "fragment_id"):
                    ingest_results(run_dir, results_path, summary["manifest_sha256"])

    def test_ingest_contains_pathological_json_decoder_failures(self) -> None:
        cases = {
            "oversized-integer": "9" * 10_000,
            "deeply-nested": "[" * 10_000 + "0" + "]" * 10_000,
        }
        for index, (label, malformed_id) in enumerate(cases.items()):
            with self.subTest(label=label):
                run_dir = self._prepare(f"decoder-{index}")
                results_path = self.root / f"decoder-{index}.jsonl"
                results_path.write_text(
                    '{"fragment_id":' + malformed_id + ',"hypotheses":[]}\n',
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(CascadeError, "invalid hypothesis results JSONL"):
                    ingest_results(run_dir, results_path, self.manifest_sha256)
                self.assertFalse((run_dir / "hypothesis-ledger.jsonl").exists())
                self.assertFalse((run_dir / "ingestion-manifest.json").exists())

    def test_ingest_rejects_duplicate_json_keys(self) -> None:
        run_dir = self._prepare()
        fragment = json.loads((run_dir / "fragments.jsonl").read_text().splitlines()[0])
        results_path = self.root / "results.jsonl"
        results_path.write_text(
            '{"fragment_id":"' + fragment["fragment_id"] + '","fragment_id":"other","hypotheses":[]}\n',
            encoding="utf-8",
        )
        with self.assertRaisesRegex(CascadeError, "duplicate JSON key"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

    def test_ingest_refuses_to_overwrite_existing_ledger(self) -> None:
        run_dir = self._prepare()
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        results_path = self.root / "results.jsonl"
        results_path.write_text(
            "".join(json.dumps(self._valid_result(fragment["fragment_id"])) + "\n" for fragment in fragments),
            encoding="utf-8",
        )
        ingest_results(run_dir, results_path, self.manifest_sha256)

        with self.assertRaisesRegex(CascadeError, "already exists"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

    def test_failed_ingest_preserves_preexisting_ingestion_manifest(self) -> None:
        run_dir = self._prepare()
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        results_path = self.root / "results.jsonl"
        results_path.write_text(
            "".join(json.dumps(self._valid_result(fragment["fragment_id"])) + "\n" for fragment in fragments),
            encoding="utf-8",
        )
        preexisting = run_dir / "ingestion-manifest.json"
        preexisting.write_text('{"sentinel":true}\n', encoding="utf-8")
        preexisting.chmod(0o600)

        with self.assertRaisesRegex(CascadeError, "already exists"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

        self.assertEqual(preexisting.read_text(encoding="utf-8"), '{"sentinel":true}\n')
        self.assertFalse((run_dir / "hypothesis-ledger.jsonl").exists())

    def test_ingest_rejects_oversized_hypothesis_field(self) -> None:
        run_dir = self._prepare()
        fragment = json.loads((run_dir / "fragments.jsonl").read_text().splitlines()[0])
        result = self._valid_result(fragment["fragment_id"])
        result["hypotheses"][0]["mechanism"] = "M" * 9000
        results_path = self.root / "results.jsonl"
        results_path.write_text(json.dumps(result) + "\n", encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "exceeds"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

    def test_ingest_rejects_non_private_run_directory(self) -> None:
        run_dir = self._prepare()
        run_dir.chmod(0o755)
        fragment = json.loads((run_dir / "fragments.jsonl").read_text().splitlines()[0])
        results_path = self.root / "results.jsonl"
        results_path.write_text(json.dumps(self._valid_result(fragment["fragment_id"])) + "\n", encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "group or other"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

    def test_ingest_rejects_modified_prepared_artifact(self) -> None:
        run_dir = self._prepare()
        fragments_path = run_dir / "fragments.jsonl"
        fragments_path.write_text(fragments_path.read_text() + "\n", encoding="utf-8")
        results_path = self.root / "results.jsonl"
        results_path.write_text("", encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "integrity"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

    def test_ingest_rejects_coordinated_manifest_and_provenance_tamper_against_pin(self) -> None:
        run_dir = self._prepare()
        fragments_path = run_dir / "fragments.jsonl"
        rows = [json.loads(line) for line in fragments_path.read_text().splitlines()]
        for row in rows:
            row["source_url"] = "https://tampered.invalid/provenance"
        fragments_path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
        manifest_path = run_dir / "run-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["source"]["url"] = "https://tampered.invalid/provenance"
        manifest["prepared_artifacts_sha256"]["fragments.jsonl"] = hashlib.sha256(fragments_path.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        results_path = self.root / "results.jsonl"
        results_path.write_text("", encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "operator-supplied SHA-256 pin"):
            ingest_results(run_dir, results_path, self.manifest_sha256)

    def test_ingest_hashes_the_exact_results_bytes_it_parses(self) -> None:
        run_dir = self._prepare()
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        original = "".join(json.dumps(self._valid_result(fragment["fragment_id"])) + "\n" for fragment in fragments).encode()
        results_path = self.root / "results.jsonl"
        results_path.write_bytes(original)
        original_reader = research_cascade._read_regular_bytes

        def read_then_replace(path: Path, *, max_bytes: int, label: str):
            data, digest = original_reader(path, max_bytes=max_bytes, label=label)
            if label == "hypothesis results JSONL":
                results_path.write_text('{"replaced":true}\n', encoding="utf-8")
            return data, digest

        with mock.patch.object(research_cascade, "_read_regular_bytes", side_effect=read_then_replace):
            ingest_results(run_dir, results_path, self.manifest_sha256)

        ingestion_manifest = json.loads((run_dir / "ingestion-manifest.json").read_text())
        self.assertEqual(ingestion_manifest["results_sha256"], hashlib.sha256(original).hexdigest())
        self.assertNotEqual(ingestion_manifest["results_sha256"], hashlib.sha256(results_path.read_bytes()).hexdigest())

    def _ingested_run(self, name: str = "run") -> tuple[Path, dict]:
        run_dir = self._prepare(name)
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        results_path = self.root / f"results-{name}.jsonl"
        results_path.write_text(
            "".join(json.dumps(self._valid_result(fragment["fragment_id"])) + "\n" for fragment in fragments),
            encoding="utf-8",
        )
        summary = ingest_results(run_dir, results_path, self.manifest_sha256)
        self.ingestion_manifest_sha256 = summary["ingestion_manifest_sha256"]
        hypothesis = json.loads((run_dir / "hypothesis-ledger.jsonl").read_text().splitlines()[0])
        return run_dir, hypothesis

    def test_verify_rejects_run_path_replacement_without_touching_replacement(self) -> None:
        run_dir, hypothesis = self._ingested_run("closure-race")
        dispositions = self.root / "closure-race-dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "coverage_gap",
                    "reason": "The owned evaluator has not been built.",
                    "evidence_refs": [],
                    "next_safe_action": "Build a deterministic local fixture.",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        displaced = self.root / "closure-race-displaced"
        replacement = self.root / "closure-race-replacement"
        replacement.mkdir(mode=0o700)
        sentinel = replacement / "sentinel.txt"
        sentinel.write_text("preserve", encoding="utf-8")
        sentinel.chmod(0o600)
        real_write = research_cascade._write_private
        replaced = False

        def replace_before_write(path: Path, content: str, **kwargs: object) -> None:
            nonlocal replaced
            if not replaced and Path(path).name == "closure-manifest.json":
                run_dir.rename(displaced)
                replacement.rename(run_dir)
                replaced = True
            real_write(path, content, **kwargs)

        with mock.patch.object(research_cascade, "_write_private", side_effect=replace_before_write):
            with self.assertRaisesRegex(CascadeError, "identity changed"):
                verify_dispositions(
                    run_dir,
                    dispositions,
                    self.manifest_sha256,
                    self.ingestion_manifest_sha256,
                )

        self.assertEqual((run_dir / "sentinel.txt").read_text(), "preserve")
        self.assertFalse((run_dir / "closure-manifest.json").exists())
        self.assertFalse((displaced / "closure-manifest.json").exists())

    def test_verify_rejects_parent_path_rebinding_and_rolls_back_output(self) -> None:
        private_parent = self.root / "closure-parent"
        private_parent.mkdir(mode=0o700)
        run_dir = private_parent / "run"
        summary = prepare_run(self.contract, run_dir)
        self.manifest_sha256 = summary["manifest_sha256"]
        fragments = [json.loads(line) for line in (run_dir / "fragments.jsonl").read_text().splitlines()]
        results_path = self.root / "closure-parent-results.jsonl"
        results_path.write_text(
            "".join(json.dumps(self._valid_result(fragment["fragment_id"])) + "\n" for fragment in fragments),
            encoding="utf-8",
        )
        ingestion = ingest_results(run_dir, results_path, self.manifest_sha256)
        self.ingestion_manifest_sha256 = ingestion["ingestion_manifest_sha256"]
        hypothesis = json.loads((run_dir / "hypothesis-ledger.jsonl").read_text().splitlines()[0])
        dispositions = self.root / "closure-parent-dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "coverage_gap",
                    "reason": "The owned evaluator has not been built.",
                    "evidence_refs": [],
                    "next_safe_action": "Build a deterministic local fixture.",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        displaced_parent = self.root / "closure-parent-displaced"
        real_write = research_cascade._write_private
        rebound = False

        def rebind_parent_before_closure(path: Path, content: str, **kwargs: object) -> tuple[int, int]:
            nonlocal rebound
            if not rebound and Path(path).name == "closure-manifest.json":
                private_parent.rename(displaced_parent)
                private_parent.mkdir(mode=0o700)
                rebound = True
            return real_write(path, content, **kwargs)

        with mock.patch.object(research_cascade, "_write_private", side_effect=rebind_parent_before_closure):
            with self.assertRaisesRegex(CascadeError, "parent identity changed"):
                verify_dispositions(
                    run_dir,
                    dispositions,
                    self.manifest_sha256,
                    self.ingestion_manifest_sha256,
                )

        self.assertFalse((displaced_parent / "run" / "closure-manifest.json").exists())
        self.assertFalse(run_dir.exists())

    def test_verify_dispositions_requires_exactly_one_terminal_row(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "coverage_gap",
                    "reason": "The owned evaluator fixture has not been implemented.",
                    "evidence_refs": [],
                    "next_safe_action": "Build a deterministic local fixture.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        summary = verify_dispositions(
            run_dir,
            dispositions,
            self.manifest_sha256,
            self.ingestion_manifest_sha256,
        )

        self.assertTrue(summary["complete"])
        self.assertEqual(summary["counts"], {"coverage_gap": 1})
        self.assertEqual(stat.S_IMODE((run_dir / "closure-manifest.json").stat().st_mode), 0o600)

    def test_verify_dispositions_rejects_oversized_or_invalid_unicode_evidence_refs(self) -> None:
        malformed_refs = (
            (" " * research_cascade._MAX_SOURCE_PATH_CHARS) + "\ud800",
            "evidence/control.json\x00suffix",
        )
        for index, malformed_ref in enumerate(malformed_refs):
            with self.subTest(malformed_ref=repr(malformed_ref)):
                run_dir, hypothesis = self._ingested_run(f"invalid-evidence-ref-{index}")
                dispositions = self.root / f"invalid-evidence-ref-{index}-dispositions.jsonl"
                dispositions.write_text(
                    json.dumps(
                        {
                            "hypothesis_id": hypothesis["hypothesis_id"],
                            "disposition": "coverage_gap",
                            "reason": "The evaluator has not been built.",
                            "evidence_refs": [malformed_ref],
                            "next_safe_action": "Build a deterministic owned fixture.",
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )

                with self.assertRaisesRegex(CascadeError, "evidence_refs must be a bounded text list"):
                    verify_dispositions(
                        run_dir,
                        dispositions,
                        self.manifest_sha256,
                        self.ingestion_manifest_sha256,
                    )

                self.assertFalse((run_dir / "closure-manifest.json").exists())

    def test_verify_dispositions_rejects_malformed_optional_evidence_index_pin(self) -> None:
        run_dir, hypothesis = self._ingested_run("malformed-optional-pin")
        dispositions = self.root / "malformed-optional-pin-dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "coverage_gap",
                    "reason": "The evaluator has not been built.",
                    "evidence_refs": [],
                    "next_safe_action": "Build a deterministic owned fixture.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(CascadeError, "evidence index SHA-256"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                "not-a-sha256",
            )

        self.assertFalse((run_dir / "closure-manifest.json").exists())

    def test_verify_dispositions_rejects_malformed_hypothesis_identifier_types(self) -> None:
        for index, malformed in enumerate(([], {}, 1, True, None)):
            with self.subTest(malformed=malformed):
                run_dir, hypothesis = self._ingested_run(f"malformed-disposition-{index}")
                dispositions = self.root / f"malformed-disposition-{index}.jsonl"
                dispositions.write_text(
                    json.dumps(
                        {
                            "hypothesis_id": malformed,
                            "disposition": "coverage_gap",
                            "reason": "The evaluator has not been built.",
                            "evidence_refs": [],
                            "next_safe_action": "Build a deterministic owned fixture.",
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )
                with self.assertRaisesRegex(CascadeError, "hypothesis_id"):
                    verify_dispositions(
                        run_dir,
                        dispositions,
                        self.manifest_sha256,
                        self.ingestion_manifest_sha256,
                    )

    def test_verify_dispositions_rejects_missing_and_duplicate_rows(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text("", encoding="utf-8")
        with self.assertRaisesRegex(CascadeError, "missing dispositions"):
            verify_dispositions(run_dir, dispositions, self.manifest_sha256, self.ingestion_manifest_sha256)

        row = {
            "hypothesis_id": hypothesis["hypothesis_id"],
            "disposition": "disproved",
            "reason": "A matched control explains the observation.",
            "evidence_refs": ["owned-fixture-log.json"],
            "next_safe_action": "none",
        }
        dispositions.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(CascadeError, "duplicate disposition"):
            verify_dispositions(run_dir, dispositions, self.manifest_sha256, self.ingestion_manifest_sha256)

    def _write_valid_evidence_manifest(self, run_dir: Path, hypothesis_id: str) -> str:
        evidence_dir = run_dir / "evidence"
        evidence_dir.mkdir(mode=0o700, exist_ok=True)
        input_path = evidence_dir / "input.json"
        positive_path = evidence_dir / "positive.json"
        negative_path = evidence_dir / "negative.json"
        input_path.write_text('{"fixture":"owned"}\n', encoding="utf-8")
        positive_path.write_text('{"candidate":"different"}\n', encoding="utf-8")
        negative_path.write_text('{"control":"same"}\n', encoding="utf-8")
        input_path.chmod(0o600)
        positive_path.chmod(0o600)
        negative_path.chmod(0o600)
        manifest = {
            "schema_version": 1,
            "hypothesis_id": hypothesis_id,
            "evaluator": {"identity": "owned-parser-fixture", "version": "1.0.0"},
            "input_artifacts": {"evidence/input.json": hashlib.sha256(input_path.read_bytes()).hexdigest()},
            "output_artifacts": {
                "evidence/positive.json": hashlib.sha256(positive_path.read_bytes()).hexdigest(),
                "evidence/negative.json": hashlib.sha256(negative_path.read_bytes()).hexdigest(),
            },
            "positive_control": {"status": "passed", "evidence_ref": "evidence/positive.json"},
            "negative_control": {"status": "passed", "evidence_ref": "evidence/negative.json"},
            "observation_status": "reproduced",
            "independent_review": {
                "decision": "approved",
                "reviewer": "human:unit-reviewer",
                "reviewed_at": "2026-08-13T00:00:00+00:00",
            },
        }
        manifest_path = evidence_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
        manifest_path.chmod(0o600)
        return "evidence/manifest.json"

    def _write_test_evidence_index(
        self,
        run_dir: Path,
        hypothesis_id: str,
        evidence_refs: list[str],
    ) -> str:
        entries = [
            {
                "hypothesis_id": hypothesis_id,
                "evidence_manifest": reference,
                "evidence_manifest_sha256": "0" * 64,
                "evaluator_result": "evidence/evaluator-result.json",
                "evaluator_result_sha256": "0" * 64,
                "independent_review": {
                    "decision": "approved",
                    "reviewer": "human:unit-reviewer",
                    "reviewed_at": "2026-08-13T00:00:00+00:00",
                },
            }
            for reference in evidence_refs
        ]
        index_path = run_dir / "evidence-index.json"
        index_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "run_id": "unit-cascade",
                    "run_manifest_sha256": self.manifest_sha256,
                    "ingestion_manifest_sha256": self.ingestion_manifest_sha256,
                    "entries": entries,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        index_path.chmod(0o600)
        return hashlib.sha256(index_path.read_bytes()).hexdigest()

    def _rehash_indexed_bundle(self, run_dir: Path, evidence_ref: str) -> str:
        manifest_path = run_dir / evidence_ref
        manifest = json.loads(manifest_path.read_text())
        result_ref = manifest["evaluator_result"]
        index_path = run_dir / "evidence-index.json"
        evidence_index = json.loads(index_path.read_text())
        evidence_index["entries"][0]["evidence_manifest_sha256"] = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
        evidence_index["entries"][0]["evaluator_result_sha256"] = hashlib.sha256((run_dir / result_ref).read_bytes()).hexdigest()
        index_path.write_text(json.dumps(evidence_index) + "\n", encoding="utf-8")
        return hashlib.sha256(index_path.read_bytes()).hexdigest()

    def _write_valid_indexed_evidence_bundle(
        self,
        run_dir: Path,
        hypothesis_id: str,
    ) -> tuple[str, str]:
        evidence_dir = run_dir / "evidence"
        evidence_dir.mkdir(mode=0o700, exist_ok=True)
        input_path = evidence_dir / "input.json"
        positive_path = evidence_dir / "positive.json"
        negative_path = evidence_dir / "negative.json"
        result_path = evidence_dir / "evaluator-result.json"
        for path, content in (
            (input_path, '{"fixture":"owned"}\n'),
            (positive_path, '{"candidate":"different"}\n'),
            (negative_path, '{"control":"same"}\n'),
        ):
            path.write_text(content, encoding="utf-8")
            path.chmod(0o600)
        evaluator = {"identity": "owned-parser-fixture", "version": "1.0.0"}
        result = {
            "schema_version": 1,
            "run_id": "unit-cascade",
            "hypothesis_id": hypothesis_id,
            "evaluator": evaluator,
            "positive_control": {"status": "passed", "evidence_ref": "evidence/positive.json"},
            "negative_control": {"status": "passed", "evidence_ref": "evidence/negative.json"},
            "observation_status": "reproduced",
        }
        result_path.write_text(json.dumps(result) + "\n", encoding="utf-8")
        result_path.chmod(0o600)
        manifest = {
            "schema_version": 1,
            "hypothesis_id": hypothesis_id,
            "evaluator": evaluator,
            "input_artifacts": {"evidence/input.json": hashlib.sha256(input_path.read_bytes()).hexdigest()},
            "output_artifacts": {
                "evidence/positive.json": hashlib.sha256(positive_path.read_bytes()).hexdigest(),
                "evidence/negative.json": hashlib.sha256(negative_path.read_bytes()).hexdigest(),
                "evidence/evaluator-result.json": hashlib.sha256(result_path.read_bytes()).hexdigest(),
            },
            "evaluator_result": "evidence/evaluator-result.json",
        }
        manifest_ref = "evidence/manifest.json"
        manifest_path = run_dir / manifest_ref
        manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
        manifest_path.chmod(0o600)
        evidence_index = {
            "schema_version": 1,
            "run_id": "unit-cascade",
            "run_manifest_sha256": self.manifest_sha256,
            "ingestion_manifest_sha256": self.ingestion_manifest_sha256,
            "entries": [
                {
                    "hypothesis_id": hypothesis_id,
                    "evidence_manifest": manifest_ref,
                    "evidence_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                    "evaluator_result": "evidence/evaluator-result.json",
                    "evaluator_result_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(),
                    "independent_review": {
                        "decision": "approved",
                        "reviewer": "human:unit-reviewer",
                        "reviewed_at": "2026-08-13T00:00:00+00:00",
                    },
                }
            ],
        }
        index_path = run_dir / "evidence-index.json"
        index_path.write_text(json.dumps(evidence_index) + "\n", encoding="utf-8")
        index_path.chmod(0o600)
        return manifest_ref, hashlib.sha256(index_path.read_bytes()).hexdigest()

    def test_cli_accepts_external_evidence_index_pin(self) -> None:
        digest = "a" * 64
        args = research_cascade._build_parser().parse_args(
            [
                "verify-dispositions",
                "--run-dir",
                "/tmp/run",
                "--dispositions",
                "/tmp/dispositions.jsonl",
                "--manifest-sha256",
                "b" * 64,
                "--ingestion-manifest-sha256",
                "c" * 64,
                "--evidence-index-sha256",
                digest,
            ]
        )

        self.assertEqual(args.evidence_index_sha256, digest)

    def test_installed_launcher_ignores_home_runtime_substitution(self) -> None:
        fake_home = self.root / "fake-home"
        fake_runtime = fake_home / "SecurityResearch" / "11 - Scripts" / "learning" / "research_cascade.py"
        fake_runtime.parent.mkdir(parents=True)
        fake_runtime.write_text('print("UNSEALED_HOME_RUNTIME_EXECUTED")\n', encoding="utf-8")
        user_site = fake_home / ".local" / "lib" / "python3.13" / "site-packages"
        user_site.mkdir(parents=True)
        user_site_marker = fake_home / "usercustomize-used"
        (user_site / "usercustomize.py").write_text(
            f'from pathlib import Path\nPath({str(user_site_marker)!r}).write_text("used")\n',
            encoding="utf-8",
        )
        fake_bin = self.root / "fake-bin"
        fake_bin.mkdir()
        fake_interpreter_marker = fake_home / "path-python-used"
        fake_python = fake_bin / "python3"
        fake_python.write_text(
            f'#!/bin/sh\nprintf used > {str(fake_interpreter_marker)!r}\nexit 77\n',
            encoding="utf-8",
        )
        fake_python.chmod(0o700)
        fake_pythonpath = self.root / "fake-pythonpath"
        fake_pythonpath.mkdir()
        sitecustomize_marker = fake_home / "sitecustomize-used"
        (fake_pythonpath / "sitecustomize.py").write_text(
            f'from pathlib import Path\nPath({str(sitecustomize_marker)!r}).write_text("used")\n',
            encoding="utf-8",
        )
        process = subprocess.run(
            [str(Path.home() / ".local/bin/argus-research-cascade"), "--help"],
            capture_output=True,
            text=True,
            timeout=30,
            env={
                **os.environ,
                "HOME": str(fake_home),
                "PATH": f"{fake_bin}:{os.environ.get('PATH', '')}",
                "PYTHONPATH": str(fake_pythonpath),
                "PYTHONDONTWRITEBYTECODE": "1",
            },
        )

        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertNotIn("UNSEALED_HOME_RUNTIME_EXECUTED", process.stdout)
        self.assertFalse(user_site_marker.exists())
        self.assertFalse(fake_interpreter_marker.exists())
        self.assertFalse(sitecustomize_marker.exists())
        self.assertIn("verify-dispositions", process.stdout)

    def test_verify_dispositions_accepts_externally_pinned_evaluator_result(self) -> None:
        run_dir, hypothesis = self._ingested_run("indexed-evidence")
        evidence_ref, evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        dispositions = self.root / "indexed-evidence-dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "The externally pinned evaluator result reproduces the invariant.",
                    "evidence_refs": [evidence_ref],
                    "next_safe_action": "Perform final reportability review.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        closure = verify_dispositions(
            run_dir,
            dispositions,
            self.manifest_sha256,
            self.ingestion_manifest_sha256,
            evidence_index_sha256,
        )

        self.assertEqual(closure["counts"], {"reportable": 1})
        self.assertEqual(closure["evidence_index_sha256"], evidence_index_sha256)
        self.assertIn("evidence/evaluator-result.json", closure["evidence_sha256"])

    def test_verify_dispositions_rejects_wrong_evidence_index_pin(self) -> None:
        run_dir, hypothesis = self._ingested_run("wrong-evidence-index-pin")
        evidence_ref, evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        evidence_index = run_dir / "evidence-index.json"
        evidence_index.write_text('{"schema_version":1}\n', encoding="utf-8")
        evidence_index.chmod(0o600)
        dispositions = self.root / "wrong-evidence-index-pin-dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "The fixture appears to reproduce the observation.",
                    "evidence_refs": [evidence_ref],
                    "next_safe_action": "Reject the wrong external pin.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(CascadeError, "evidence index.*operator-supplied"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                "0" * 64,
            )

    def test_verify_dispositions_requires_external_evidence_index_pin_for_reportable(self) -> None:
        run_dir, hypothesis = self._ingested_run("missing-evidence-index-pin")
        evidence_ref, evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        dispositions = self.root / "missing-evidence-index-pin-dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "The fixture appears to reproduce the observation.",
                    "evidence_refs": [evidence_ref],
                    "next_safe_action": "Obtain operator-held evidence approval.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(CascadeError, "evidence index.*pin"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
            )

    def test_verify_dispositions_rejects_reportable_without_evidence(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "Claimed by a model.",
                    "evidence_refs": [],
                    "next_safe_action": "none",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(CascadeError, "evidence"):
            verify_dispositions(run_dir, dispositions, self.manifest_sha256, self.ingestion_manifest_sha256)

    def test_verify_dispositions_rejects_modified_ledger(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        ledger = run_dir / "hypothesis-ledger.jsonl"
        ledger.write_text(ledger.read_text() + "\n", encoding="utf-8")
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text("", encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "integrity"):
            verify_dispositions(run_dir, dispositions, self.manifest_sha256, self.ingestion_manifest_sha256)

    def test_verify_dispositions_rejects_wrong_ingestion_manifest_pin(self) -> None:
        run_dir, _hypothesis = self._ingested_run()
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text("", encoding="utf-8")
        with self.assertRaisesRegex(CascadeError, "operator-supplied SHA-256 pin"):
            verify_dispositions(run_dir, dispositions, self.manifest_sha256, "0" * 64)

    def test_verify_dispositions_hashes_the_exact_bytes_it_parses(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        row = {
            "hypothesis_id": hypothesis["hypothesis_id"],
            "disposition": "coverage_gap",
            "reason": "Evaluator not yet implemented.",
            "evidence_refs": [],
            "next_safe_action": "Build the owned fixture.",
        }
        original = (json.dumps(row) + "\n").encode()
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_bytes(original)
        original_reader = research_cascade._read_regular_bytes

        def read_then_replace(path: Path, *, max_bytes: int, label: str):
            data, digest = original_reader(path, max_bytes=max_bytes, label=label)
            if label == "dispositions JSONL":
                dispositions.write_text('{"replaced":true}\n', encoding="utf-8")
            return data, digest

        with mock.patch.object(research_cascade, "_read_regular_bytes", side_effect=read_then_replace):
            closure = verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
            )

        self.assertEqual(closure["dispositions_sha256"], hashlib.sha256(original).hexdigest())
        self.assertNotEqual(closure["dispositions_sha256"], hashlib.sha256(dispositions.read_bytes()).hexdigest())

    def test_verify_dispositions_rejects_model_claim_file_as_reportable_evidence(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        evidence = run_dir / "evidence" / "claim.txt"
        evidence.parent.mkdir(mode=0o700)
        evidence.write_text("The model says this is proven.\n", encoding="utf-8")
        evidence.chmod(0o600)
        dispositions = self.root / "dispositions.jsonl"
        row = {
            "hypothesis_id": hypothesis["hypothesis_id"],
            "disposition": "reportable",
            "reason": "Claimed by a model.",
            "evidence_refs": ["evidence/claim.txt"],
            "next_safe_action": "none",
        }
        dispositions.write_text(json.dumps(row) + "\n", encoding="utf-8")
        evidence_index_sha256 = self._write_test_evidence_index(
            run_dir,
            hypothesis["hypothesis_id"],
            ["evidence/claim.txt"],
        )

        with self.assertRaisesRegex(CascadeError, "evidence manifest"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                evidence_index_sha256,
            )

    def test_verify_dispositions_rejects_missing_or_external_reportable_evidence(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        dispositions = self.root / "dispositions.jsonl"
        base = {
            "hypothesis_id": hypothesis["hypothesis_id"],
            "disposition": "reportable",
            "reason": "Deterministic owned fixture demonstrates the invariant violation.",
            "evidence_refs": ["evidence/missing.json"],
            "next_safe_action": "Run reportability review.",
        }
        dispositions.write_text(json.dumps(base) + "\n", encoding="utf-8")
        evidence_index_sha256 = self._write_test_evidence_index(
            run_dir,
            hypothesis["hypothesis_id"],
            base["evidence_refs"],
        )
        with self.assertRaisesRegex(CascadeError, "evidence"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                evidence_index_sha256,
            )

        outside = self.root / "outside.json"
        outside.write_text("{}\n", encoding="utf-8")
        base["evidence_refs"] = [str(outside)]
        dispositions.write_text(json.dumps(base) + "\n", encoding="utf-8")
        evidence_index_sha256 = self._write_test_evidence_index(
            run_dir,
            hypothesis["hypothesis_id"],
            base["evidence_refs"],
        )
        with self.assertRaisesRegex(CascadeError, "relative"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                evidence_index_sha256,
            )

    def test_verify_dispositions_hashes_existing_reportable_evidence(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        evidence_ref, evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        evidence = run_dir / evidence_ref
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "Deterministic owned fixture demonstrates the invariant violation.",
                    "evidence_refs": [evidence_ref],
                    "next_safe_action": "Run reportability review.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        summary = verify_dispositions(
            run_dir,
            dispositions,
            self.manifest_sha256,
            self.ingestion_manifest_sha256,
            evidence_index_sha256,
        )

        self.assertIn(evidence_ref, summary["evidence_sha256"])
        self.assertEqual(summary["evidence_sha256"][evidence_ref], hashlib.sha256(evidence.read_bytes()).hexdigest())
        self.assertEqual(summary["counts"], {"reportable": 1})

    def test_verify_dispositions_enforces_aggregate_evidence_byte_limit(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        evidence_ref, evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "Deterministic owned fixture demonstrates the invariant violation.",
                    "evidence_refs": [evidence_ref],
                    "next_safe_action": "Run reportability review.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        with mock.patch.object(research_cascade, "_MAX_TOTAL_EVIDENCE_BYTES", 50, create=True):
            with self.assertRaisesRegex(CascadeError, "aggregate evidence"):
                verify_dispositions(
                    run_dir,
                    dispositions,
                    self.manifest_sha256,
                    self.ingestion_manifest_sha256,
                    evidence_index_sha256,
                )

    def test_verify_dispositions_rejects_overlapping_input_and_output_artifacts(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        evidence_ref, evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        evidence_manifest = run_dir / evidence_ref
        manifest = json.loads(evidence_manifest.read_text())
        manifest["input_artifacts"] = {
            "evidence/positive.json": manifest["output_artifacts"]["evidence/positive.json"]
        }
        evidence_manifest.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
        evidence_index_sha256 = self._rehash_indexed_bundle(run_dir, evidence_ref)
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "Input and output must remain causally distinct.",
                    "evidence_refs": [evidence_ref],
                    "next_safe_action": "Rebuild the evidence manifest.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(CascadeError, "disjoint"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                evidence_index_sha256,
            )

    def test_verify_dispositions_contains_invalid_unicode_artifact_map_key(self) -> None:
        run_dir, hypothesis = self._ingested_run("surrogate-artifact-key")
        evidence_ref, _evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        evidence_manifest = run_dir / evidence_ref
        manifest = json.loads(evidence_manifest.read_text())
        manifest["input_artifacts"]["\ud800"] = manifest["input_artifacts"].pop("evidence/input.json")
        evidence_manifest.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
        evidence_index_sha256 = self._rehash_indexed_bundle(run_dir, evidence_ref)
        dispositions = self.root / "surrogate-artifact-key-dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "Invalid Unicode must fail closed.",
                    "evidence_refs": [evidence_ref],
                    "next_safe_action": "Repair the evidence manifest.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(CascadeError, "path must be valid Unicode text"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                evidence_index_sha256,
            )

        self.assertFalse((run_dir / "closure-manifest.json").exists())

    def test_verify_dispositions_rejects_duplicate_evidence_manifest_references(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        evidence_ref, evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "Duplicate references must not cause repeated hashing.",
                    "evidence_refs": [evidence_ref, evidence_ref],
                    "next_safe_action": "Deduplicate evidence references.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(CascadeError, "duplicate evidence"):
            verify_dispositions(run_dir, dispositions, self.manifest_sha256, self.ingestion_manifest_sha256)

    def test_verify_dispositions_rejects_hard_linked_evidence_aliases(self) -> None:
        run_dir, hypothesis = self._ingested_run("hard-linked-evidence")
        evidence_ref, _evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        manifest_path = run_dir / evidence_ref
        manifest = json.loads(manifest_path.read_text())
        input_ref = next(iter(manifest["input_artifacts"]))
        positive_ref = "evidence/positive.json"
        input_path = run_dir / input_ref
        input_path.unlink()
        os.link(run_dir / positive_ref, input_path)
        manifest["input_artifacts"][input_ref] = hashlib.sha256(input_path.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
        evidence_index_sha256 = self._rehash_indexed_bundle(run_dir, evidence_ref)
        dispositions = self.root / "hard-linked-evidence-dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "Distinct paths must not alias one evidence inode.",
                    "evidence_refs": [evidence_ref],
                    "next_safe_action": "Rebuild evidence without hard links.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(CascadeError, "hard-link|inode alias"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                evidence_index_sha256,
            )

    def test_verify_dispositions_rejects_controls_with_identical_content(self) -> None:
        run_dir, hypothesis = self._ingested_run("identical-controls")
        evidence_ref, evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        manifest_path = run_dir / evidence_ref
        manifest = json.loads(manifest_path.read_text())
        negative = run_dir / "evidence/negative.json"
        positive = run_dir / "evidence/positive.json"
        negative.write_bytes(positive.read_bytes())
        manifest["output_artifacts"]["evidence/negative.json"] = hashlib.sha256(negative.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
        evidence_index_sha256 = self._rehash_indexed_bundle(run_dir, evidence_ref)
        dispositions = self.root / "identical-controls-dispositions.jsonl"
        dispositions.write_text(
            json.dumps(
                {
                    "hypothesis_id": hypothesis["hypothesis_id"],
                    "disposition": "reportable",
                    "reason": "The evaluator claims both controls passed.",
                    "evidence_refs": [evidence_ref],
                    "next_safe_action": "Review the controls.",
                }
            )
            + "\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(CascadeError, "distinct content"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                evidence_index_sha256,
            )

    def test_verify_dispositions_rejects_same_artifact_for_both_controls(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        evidence_ref, evidence_index_sha256 = self._write_valid_indexed_evidence_bundle(
            run_dir,
            hypothesis["hypothesis_id"],
        )
        evidence_manifest = run_dir / evidence_ref
        manifest = json.loads(evidence_manifest.read_text())
        evaluator_result_path = run_dir / manifest["evaluator_result"]
        evaluator_result = json.loads(evaluator_result_path.read_text())
        evaluator_result["negative_control"]["evidence_ref"] = evaluator_result["positive_control"]["evidence_ref"]
        evaluator_result_path.write_text(json.dumps(evaluator_result) + "\n", encoding="utf-8")
        manifest["output_artifacts"][manifest["evaluator_result"]] = hashlib.sha256(
            evaluator_result_path.read_bytes()
        ).hexdigest()
        evidence_manifest.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
        evidence_index_sha256 = self._rehash_indexed_bundle(run_dir, evidence_ref)
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text(json.dumps({
            "hypothesis_id": hypothesis["hypothesis_id"],
            "disposition": "reportable",
            "reason": "Controls are incorrectly aliased.",
            "evidence_refs": [evidence_ref],
            "next_safe_action": "none",
        }) + "\n", encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "distinct output artifacts"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                evidence_index_sha256,
            )

    def test_verify_dispositions_rejects_symlinked_evidence_component(self) -> None:
        run_dir, hypothesis = self._ingested_run()
        outside = self.root / "outside-evidence"
        outside.mkdir()
        (outside / "manifest.json").write_text("{}\n", encoding="utf-8")
        (run_dir / "evidence").symlink_to(outside, target_is_directory=True)
        dispositions = self.root / "dispositions.jsonl"
        dispositions.write_text(json.dumps({
            "hypothesis_id": hypothesis["hypothesis_id"],
            "disposition": "reportable",
            "reason": "Must not follow evidence directory symlinks.",
            "evidence_refs": ["evidence/manifest.json"],
            "next_safe_action": "none",
        }) + "\n", encoding="utf-8")
        evidence_index_sha256 = self._write_test_evidence_index(
            run_dir,
            hypothesis["hypothesis_id"],
            ["evidence/manifest.json"],
        )

        with self.assertRaisesRegex(CascadeError, "symlink"):
            verify_dispositions(
                run_dir,
                dispositions,
                self.manifest_sha256,
                self.ingestion_manifest_sha256,
                evidence_index_sha256,
            )

    def test_prepare_rejects_url_as_source_path(self) -> None:
        contract = json.loads(self.contract.read_text())
        contract["source"]["path"] = "https://example.test/research"
        self.contract.write_text(json.dumps(contract), encoding="utf-8")

        with self.assertRaisesRegex(CascadeError, "local regular file"):
            prepare_run(self.contract, self.root / "run")

    def test_prepare_rejects_embedded_nul_source_path_with_controlled_error(self) -> None:
        contract = json.loads(self.contract.read_text())
        contract["source"]["path"] = f"{self.source}\x00suffix"
        self.contract.write_text(json.dumps(contract), encoding="utf-8")
        run_dir = self.root / "nul-source-path"

        process = subprocess.run(
            [
                str(Path.home() / ".local/bin/argus-research-cascade"),
                "prepare",
                "--contract",
                str(self.contract),
                "--run-dir",
                str(run_dir),
            ],
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

        self.assertEqual(process.returncode, 2)
        self.assertIn("error: path must not contain NUL characters", process.stderr)
        self.assertNotIn("Traceback", process.stderr)
        self.assertFalse(run_dir.exists())

    def test_phase_entry_rejects_embedded_nul_path_arguments(self) -> None:
        with self.subTest(argument="contract path"):
            with self.assertRaisesRegex(CascadeError, "contract path must not contain NUL"):
                prepare_run(f"{self.contract}\x00suffix", self.root / "nul-contract-argument")

        with self.subTest(argument="run directory"):
            with self.assertRaisesRegex(CascadeError, "run directory must not contain NUL"):
                prepare_run(self.contract, f"{self.root / 'nul-run-argument'}\x00suffix")

        prepared_run = self.root / "nul-results-argument"
        prepared_summary = prepare_run(self.contract, prepared_run)
        with self.subTest(argument="results path"):
            with self.assertRaisesRegex(CascadeError, "results path must not contain NUL"):
                ingest_results(
                    prepared_run,
                    f"{self.root / 'results.jsonl'}\x00suffix",
                    prepared_summary["manifest_sha256"],
                )

        ingested_run, _hypothesis = self._ingested_run("nul-dispositions-argument")
        with self.subTest(argument="dispositions path"):
            with self.assertRaisesRegex(CascadeError, "dispositions path must not contain NUL"):
                verify_dispositions(
                    ingested_run,
                    f"{self.root / 'dispositions.jsonl'}\x00suffix",
                    self.manifest_sha256,
                    self.ingestion_manifest_sha256,
                )

        with self.subTest(argument="existing run directory"):
            with self.assertRaisesRegex(CascadeError, "run directory must not contain NUL"):
                ingest_results(
                    f"{ingested_run}\x00suffix",
                    self.root / "unused-results.jsonl",
                    self.manifest_sha256,
                )


if __name__ == "__main__":
    unittest.main()
