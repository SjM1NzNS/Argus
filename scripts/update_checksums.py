#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

# README.md is intentionally mutable on GitHub and remains covered by the
# public-release content scanner. Excluding it here prevents documentation-only
# edits from invalidating the integrity manifest for the packaged artifacts.
EXCLUDED = {"CHECKSUMS.sha256", "README.md"}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rendered(root: Path) -> str:
    rows = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if not path.is_file() or ".git" in path.parts or relative in EXCLUDED:
            continue
        rows.append(f"{digest(path)}  {relative}")
    return "\n".join(rows) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or verify the Argus public-backup checksum file.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    target = root / "CHECKSUMS.sha256"
    expected = rendered(root)
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != expected:
            print("CHECKSUM VERIFICATION FAILED")
            return 1
        print("CHECKSUM VERIFICATION PASSED")
        return 0
    target.write_text(expected, encoding="utf-8")
    print(f"Wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
