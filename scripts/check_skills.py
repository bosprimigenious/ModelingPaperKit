#!/usr/bin/env python3
"""Lightweight Codex skill structure checker.

This intentionally avoids PyYAML so it can run in the base Python environment.
It checks only the conventions this repository needs for local skills.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9-]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check ModelingPaperKit skill folders")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["skills"],
        help="Skill folder or parent directory to check (default: skills)",
    )
    return parser.parse_args()


def discover_skill_dirs(paths: list[str]) -> list[Path]:
    dirs: list[Path] = []
    for raw in paths:
        path = (REPO_ROOT / raw).resolve() if not Path(raw).is_absolute() else Path(raw)
        if (path / "SKILL.md").exists():
            dirs.append(path)
        elif path.is_dir():
            dirs.extend(sorted(p for p in path.iterdir() if (p / "SKILL.md").exists()))
        else:
            print(f"[critical] path not found: {path}")
    return sorted(set(dirs))


def frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return {}


def check_skill(skill_dir: Path) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    meta = frontmatter(text)

    if not NAME_RE.match(name):
        findings.append(("critical", f"{name}: folder name must be lowercase hyphen-case"))
    if meta.get("name") != name:
        findings.append(("critical", f"{name}: frontmatter name does not match folder"))
    if not meta.get("description"):
        findings.append(("critical", f"{name}: missing description"))
    if "TODO" in text or "[TODO" in text:
        findings.append(("warning", f"{name}: SKILL.md still contains TODO text"))
    if not (skill_dir / "agents" / "openai.yaml").exists():
        findings.append(("warning", f"{name}: missing agents/openai.yaml"))

    refs = skill_dir / "references"
    if refs.exists():
        for ref in refs.glob("*.md"):
            ref_text = ref.read_text(encoding="utf-8")
            if "TODO" in ref_text or "[TODO" in ref_text:
                findings.append(("warning", f"{name}: {ref.name} contains TODO text"))
    return findings


def main() -> int:
    args = parse_args()
    skill_dirs = discover_skill_dirs(args.paths)
    if not skill_dirs:
        print("[critical] no skill folders found")
        return 1

    all_findings: list[tuple[str, str]] = []
    for skill_dir in skill_dirs:
        findings = check_skill(skill_dir)
        all_findings.extend(findings)
        if not findings:
            print(f"[ok] {skill_dir.relative_to(REPO_ROOT)}")

    for severity, message in all_findings:
        print(f"[{severity}] {message}")

    return 1 if any(sev == "critical" for sev, _ in all_findings) else 0


if __name__ == "__main__":
    sys.exit(main())
