#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the public Argus skills and configuration safely.")
    parser.add_argument("--mode", choices=("copy", "symlink"), default="copy", help="Install skill directories by copying or symlinking them.")
    parser.add_argument("--hermes-home", type=Path, default=Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")))
    parser.add_argument("--argus-config", type=Path, default=Path(os.environ.get("ARGUS_CONFIG", Path.home() / ".config/argus")))
    parser.add_argument("--skip-skills", action="store_true")
    parser.add_argument("--skip-config", action="store_true")
    parser.add_argument("--force", action="store_true", help="Allow overwriting an existing destination. Review local changes first.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def fail_if_exists(path: Path, force: bool) -> None:
    if path.exists() or path.is_symlink():
        if not force:
            raise SystemExit(f"Refusing to overwrite existing path: {path}\nRe-run with --force only after reviewing local modifications.")


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    source_skills = root / "skills/security-research"
    skill_dest_root = args.hermes_home.expanduser() / "skills/security-research"
    source_registry = root / "config/learning-sources.yaml"
    registry_dest = args.argus_config.expanduser() / "learning-sources.yaml"

    actions: list[tuple[str, Path, Path]] = []
    if not args.skip_skills:
        for source in sorted(source_skills.iterdir()):
            if (source / "SKILL.md").is_file():
                actions.append((args.mode, source, skill_dest_root / source.name))
    if not args.skip_config:
        actions.append(("copy-file", source_registry, registry_dest))

    for action, source, destination in actions:
        fail_if_exists(destination, args.force)
        print(f"{action}: {source} -> {destination}")

    if args.dry_run:
        print("Dry run complete; no files changed.")
        return 0

    for action, source, destination in actions:
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() or destination.is_symlink():
            if destination.is_dir() and not destination.is_symlink():
                shutil.rmtree(destination)
            else:
                destination.unlink()
        if action == "symlink":
            destination.symlink_to(source.resolve(), target_is_directory=True)
        elif action == "copy":
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

    print("Installation complete. Start a new Hermes session to reload skills.")
    print(f"Open the Obsidian vault at: {root / 'vault'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
