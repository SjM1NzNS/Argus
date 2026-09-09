#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".txt", ".py", ".sh", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".csv", ".html", ".css", ".js"}
TEXT_FILENAMES = {".env.example", "preview-is.env.example", ".gitignore", "CHECKSUMS.sha256"}
FORBIDDEN_PATH_PARTS = {".env", ".obsidian", "tool-output", "__pycache__"}
FORBIDDEN_SUFFIXES = {".har", ".pcap", ".pcapng", ".sqlite", ".db", ".pem", ".p12", ".pfx", ".key", ".pyc", ".log"}
private_program_terms = "|".join(
    (
        "Google " + "Bug" + " Hunters",
        "bug" + "hunters" + r"\.google\.com",
        "Google " + "V" + "RP",
        "Red" + r"[-\s]*" + "Bull",
        "red" + "bull" + r"\.com",
        "Civi" + "tatis",
        "Engel" + r"\s*(?:&|and)\s*V[öo]lkers",
        "Porta" + "ltoro",
        r"\b" + "Or" + "bit" + r"\b",
    )
)
FORBIDDEN_PATTERNS = {
    "source home path": re.compile(re.escape("/home/" + "argus") + r"(?:/|\b)", re.I),
    "private program identifier": re.compile(private_program_terms, re.I),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "Stripe live key": re.compile(r"\b(?:sk|rk)_live_[0-9A-Za-z]{16,}\b"),
    "JWT": re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
}
EMAIL_RE = re.compile(r"(?<![A-Za-z0-9._%+-])([A-Za-z0-9._%+-]+)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})(?![A-Za-z0-9.-])")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SKILL_ASSET_RE = re.compile(
    r"(?<![A-Za-z0-9_./-])((?:references|scripts)/[A-Za-z0-9_./-]+\.(?:md|py|sh|json|yaml|yml))"
)


def is_allowed_email(value: str) -> bool:
    domain = value.rsplit("@", 1)[1].lower()
    return domain.endswith(("example.com", "example.org", "example.net", "example.invalid"))


def validate_skill(path: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append(f"invalid skill frontmatter start: {path}")
        return
    end = text.find("\n---\n", 4)
    if end < 0 or not text[end + 5 :].strip():
        errors.append(f"invalid/empty skill body: {path}")
        return
    frontmatter = text[4:end]
    name = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", frontmatter)
    description = re.search(r"(?m)^description:\s*(.+)$", frontmatter)
    if not name or not re.fullmatch(r"[a-z0-9_-]{1,64}", name.group(1).strip()):
        errors.append(f"invalid skill name: {path}")
    if not description or len(description.group(1).strip().strip("\"'")) > 1024:
        errors.append(f"invalid skill description: {path}")
    if len(text) > 100_000:
        errors.append(f"skill exceeds 100,000 characters: {path}")


def validate_links(path: Path, text: str, root: Path, errors: list[str]) -> None:
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip().split()[0].strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0]
        if not target:
            continue
        # Do not mistake array/function syntax inside extracted source snippets
        # for Markdown. Validate only path-shaped or file-shaped targets.
        if "/" not in target and Path(target).suffix.lower() not in {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh"}:
            continue
        candidate = (path.parent / target).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            errors.append(f"relative link escapes repository: {path}: {target}")
            continue
        if not candidate.exists():
            errors.append(f"broken relative link: {path}: {target}")


def validate_skill_assets(skill_root: Path, errors: list[str]) -> None:
    """Resolve linked reference/script paths anywhere in a packaged skill."""
    for markdown in skill_root.rglob("*.md"):
        text = markdown.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for match in SKILL_ASSET_RE.finditer(text):
            target = match.group(1)
            local = skill_root / target
            cross_skill = any(skill_root.parent.glob(f"*/{target}"))
            if not local.is_file() and not cross_skill:
                errors.append(
                    f"missing skill asset: {markdown.relative_to(skill_root)}: {target}"
                )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed privacy and structure gate for the public Argus backup.")
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []
    scanned = 0

    for path in sorted(root.rglob("*")):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(root)
        if path.is_dir():
            continue
        scanned += 1
        if any(part in FORBIDDEN_PATH_PARTS for part in relative.parts) and relative.name != ".env.example":
            errors.append(f"forbidden path component: {relative}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden file type: {relative}")
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in TEXT_FILENAMES:
            errors.append(f"opaque/unapproved file type: {relative}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"non-UTF-8 file: {relative}")
            continue
        for label, pattern in FORBIDDEN_PATTERNS.items():
            for m in pattern.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                errors.append(f"{label}: {relative}:{line}")
        for m in EMAIL_RE.finditer(text):
            if not is_allowed_email(m.group(0)):
                line = text.count("\n", 0, m.start()) + 1
                errors.append(f"non-reserved email address: {relative}:{line}")
        if path.name == "SKILL.md" and "skills/security-research" in relative.as_posix():
            validate_skill(path, errors)
        if path.suffix.lower() == ".md":
            validate_links(path, text, root, errors)

    required = [
        root / "README.md",
        root / "PRIVACY.md",
        root / "AGENTS.md",
        root / "SOURCE-MANIFEST.json",
        root / "CHECKSUMS.sha256",
        root / "vault/00 - System/web2-skill-index.md",
        root / "vault/00 - System/web3-skill-index.md",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"required file missing: {path.relative_to(root)}")

    skills_root = root / "skills/security-research"
    if skills_root.is_dir():
        for skill_root in sorted(p for p in skills_root.iterdir() if p.is_dir()):
            validate_skill_assets(skill_root, errors)

    if errors:
        print(f"PUBLIC RELEASE VERIFICATION FAILED ({len(errors)} issue(s), {scanned} files scanned)")
        for error in errors[:200]:
            print(f"- {error}")
        if len(errors) > 200:
            print(f"- ... {len(errors) - 200} more")
        return 1
    print(f"PUBLIC RELEASE VERIFICATION PASSED ({scanned} files scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
