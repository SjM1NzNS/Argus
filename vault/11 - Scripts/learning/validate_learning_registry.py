#!/usr/bin/env python3
"""Validate and summarize the canonical Argus learning source registry."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from learning_registry import RegistryValidationError, load_registry


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="~/.config/argus/learning-sources.yaml")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        registry = load_registry(Path(args.config).expanduser())
    except RegistryValidationError as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, indent=2))
        return 1
    payload = {
        "valid": True,
        "schema_version": registry.schema_version,
        "digest": registry.digest,
        "sources": len(registry.sources),
        "cadences": dict(Counter(s["cadence"] for s in registry.sources)),
        "roles": dict(Counter(s["role"] for s in registry.sources)),
        "acquisitions": dict(Counter(s["acquisition"] for s in registry.sources)),
        "trust": dict(Counter(s["trust"] for s in registry.sources)),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
