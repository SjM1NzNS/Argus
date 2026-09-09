#!/usr/bin/env python3
"""Deprecated compatibility entrypoint for the unified Playwright triage lane."""
from __future__ import annotations

import os
import sys
from pathlib import Path

TARGET = Path(__file__).with_name("browser_source_triage.py")


def main() -> None:
    print(
        "browser_source_triage_selenium.py is deprecated; using browser_source_triage.py",
        file=sys.stderr,
    )
    browser_python = Path(
        os.environ.get(
            "ARGUS_BROWSER_PYTHON",
            str(Path.home() / ".local/share/argus-browser/venv/bin/python"),
        )
    )
    if not browser_python.is_file():
        raise SystemExit(f"Argus browser Python is missing: {browser_python}")
    os.execv(str(browser_python), [str(browser_python), str(TARGET), *sys.argv[1:]])


if __name__ == "__main__":
    main()
