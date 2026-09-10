#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import update_checksums


class UpdateChecksumsTests(unittest.TestCase):
    def test_rendered_excludes_mutable_top_level_readme(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("mutable documentation\n", encoding="utf-8")
            (root / "stable.txt").write_text("stable artifact\n", encoding="utf-8")

            manifest = update_checksums.rendered(root)

            self.assertNotIn("README.md", manifest)
            self.assertIn("stable.txt", manifest)

    def test_rendered_keeps_nested_readmes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / "docs"
            nested.mkdir()
            (nested / "README.md").write_text("packaged documentation\n", encoding="utf-8")

            manifest = update_checksums.rendered(root)

            self.assertIn("docs/README.md", manifest)


if __name__ == "__main__":
    unittest.main()
