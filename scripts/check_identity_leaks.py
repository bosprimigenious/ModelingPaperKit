#!/usr/bin/env python3
"""Scan text files for likely CUMCM electronic-submission identity leaks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_INCLUDE_SUFFIXES = {
    ".tex",
    ".bib",
    ".md",
    ".py",
    ".m",
    ".r",
    ".csv",
    ".tsv",
    ".txt",
    ".log",
    ".json",
    ".yaml",
    ".yml",
}
DEFAULT_EXCLUDE_PARTS = {
    ".git",
    "__pycache__",
    "out",
    "node_modules",
    ".venv",
    "venv",
}
DEFAULT_EXCLUDE_FILES = {
    "templates/cumcm/sections/ai_declaration.tex",
    "templates/cumcm/sections/cover.tex",
    "templates/cumcm/sections/numbering_page.tex",
}

PATTERNS = [
    ("email", re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")),
    ("phone_cn", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("absolute_path", re.compile(r"(/Users/[^\\s,;:]+|/home/[^\\s,;:]+|[A-Za-z]:\\\\Users\\\\[^\\s,;:]+)")),
    ("student_id_context", re.compile(r"(学号|student\\s*id|student_id).{0,12}\d{6,14}", re.IGNORECASE)),
    ("school_context", re.compile(r"(学校|学院|大学|校区|实验室|导师|指导教师|队员|姓名).{0,16}")),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan files for likely identity leaks")
    parser.add_argument("paths", nargs="*", default=["templates/cumcm", "skills", "docs"])
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--include-paper-pages",
        action="store_true",
        help="Also scan CUMCM paper-only commitment and numbering pages",
    )
    return parser.parse_args()


def resolve_path(raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else REPO_ROOT / path


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def should_skip(path: Path, include_paper_pages: bool) -> bool:
    rel = display_path(path)
    if not include_paper_pages and rel in DEFAULT_EXCLUDE_FILES:
        return True
    if any(part in DEFAULT_EXCLUDE_PARTS for part in path.parts):
        return True
    return path.suffix.lower() not in DEFAULT_INCLUDE_SUFFIXES


def iter_files(paths: list[str], include_paper_pages: bool) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = resolve_path(raw)
        if path.is_file() and not should_skip(path, include_paper_pages):
            files.append(path)
        elif path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and not should_skip(child, include_paper_pages):
                    files.append(child)
    return sorted(set(files))


def scan_file(path: Path) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        for code, pattern in PATTERNS:
            match = pattern.search(line)
            if match:
                findings.append(
                    {
                        "severity": "warning",
                        "code": code,
                        "message": "Possible identity-related text found",
                        "path": display_path(path),
                        "line": line_no,
                        "excerpt": match.group(0)[:80],
                    }
                )
    return findings


def summarize(findings: list[dict[str, object]]) -> dict[str, int]:
    return {
        "critical": 0,
        "warning": len(findings),
        "info": 0,
    }


def main() -> int:
    args = parse_args()
    findings: list[dict[str, object]] = []
    for path in iter_files(args.paths, args.include_paper_pages):
        findings.extend(scan_file(path))

    summary = summarize(findings)
    result = {
        "tool": "check_identity_leaks",
        "status": "warning" if findings else "ok",
        "summary": summary,
        "findings": findings,
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"check_identity_leaks: {result['status']}")
        for finding in findings:
            print(
                f"[{finding['severity']}] {finding['code']}: "
                f"{finding['path']}:{finding['line']} {finding['excerpt']}"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
