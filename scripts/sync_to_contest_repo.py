#!/usr/bin/env python3
"""Sync ModelingPaperKit tool layer into a contest workspace repo."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Paths relative to PaperKit root to copy.
SYNC_PATHS = [
    "core",
    "templates",
    "scripts/check_identity_leaks.py",
    "scripts/check_skills.py",
    "scripts/check_submission.py",
    "scripts/check_tex_links.py",
    "scripts/check_skill_contract.py",
    "scripts/check_prose_style.py",
    "scripts/prose_rules.json",
    "scripts/check_claim_coverage.py",
    "scripts/check_model_fitness.py",
    "scripts/preflight.py",
    "scripts/inspect_template.py",
    "scripts/summarize_build_log.py",
    "scripts/build.py",
    "scripts/clean.py",
    "scripts/new_contest.py",
    "scripts/generate_dummy_data.py",
    "scripts/verify_build.py",
    "scripts/sync_to_contest_repo.py",
    "docs/repo-sync.md",
    "AGENTS.md",
    "docs/2026-cumcm-skill-index.md",
    "docs/2026-cumcm-official-rules-snapshot.md",
    "docs/getting-started.md",
    "docs/template-guide.md",
    "docs/faq.md",
    "tests/test_preflight.py",
    "tests/fixtures",
    "examples",
    "reference",
]

SKILL_GLOBS = (
    "skills/cumcm-*",
    "skills/modeling-paperkit",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync PaperKit tool layer to contest repo")
    parser.add_argument(
        "--dest",
        required=True,
        help="Destination contest repo root (e.g. ../math_modeling2026)",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def expand_sync_list() -> list[Path]:
    items: list[Path] = []
    for rel in SYNC_PATHS:
        path = REPO_ROOT / rel
        if path.exists():
            items.append(path)
    skills_root = REPO_ROOT / "skills"
    if skills_root.is_dir():
        for child in sorted(skills_root.iterdir()):
            if not child.is_dir():
                continue
            if child.name.startswith("cumcm-") or child.name == "modeling-paperkit":
                items.append(child)
    return items


def copy_item(src: Path, dest_root: Path, dry_run: bool) -> str:
    rel = src.relative_to(REPO_ROOT)
    dest = dest_root / rel
    action = "UPDATE" if dest.exists() else "ADD"
    if dry_run:
        return f"{action} {rel}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
    return f"{action} {rel}"


def main() -> int:
    args = parse_args()
    dest_root = Path(args.dest)
    if not dest_root.is_absolute():
        dest_root = (Path.cwd() / dest_root).resolve()
    if not dest_root.is_dir():
        print(f"[critical] dest not a directory: {dest_root}", file=sys.stderr)
        return 1

    items = expand_sync_list()
    print(f"sync PaperKit → {dest_root} ({'dry-run' if args.dry_run else 'write'})")
    for src in items:
        print(copy_item(src, dest_root, args.dry_run))
    print(f"done: {len(items)} paths")
    return 0


if __name__ == "__main__":
    sys.exit(main())
