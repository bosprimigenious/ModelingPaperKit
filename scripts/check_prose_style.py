#!/usr/bin/env python3
"""Scan paper TeX for AI filler, hollow inference, and meta-language leakage.

Rules live in scripts/prose_rules.json so skills and the checker share one source.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = Path(__file__).resolve().parent / "prose_rules.json"

TARGET_DIRS = {
    "cumcm": REPO_ROOT / "templates" / "cumcm",
    "wuyi": REPO_ROOT / "templates" / "wuyi",
    "beijing": REPO_ROOT / "templates" / "beijing",
}

ALLOW_MARKER = re.compile(r"prose:allow")
COMMENT_RE = re.compile(r"(?<!\\)%.*$")


def load_rules() -> dict[str, list[tuple[str, re.Pattern[str]]]]:
    data = json.loads(RULES_PATH.read_text(encoding="utf-8"))

    def compile_group(key: str) -> list[tuple[str, re.Pattern[str]]]:
        out: list[tuple[str, re.Pattern[str]]] = []
        for item in data.get(key, []):
            flags = 0
            for f in item.get("flags") or []:
                if f.upper() == "I":
                    flags |= re.IGNORECASE
            out.append((item["code"], re.compile(item["pattern"], flags)))
        return out

    return {
        "ai_filler": compile_group("ai_filler"),
        "hollow_inference": compile_group("hollow_inference"),
        "meta": compile_group("meta"),
        "weak": compile_group("weak"),
    }


RULES = load_rules()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan TeX prose for banned AI / hollow patterns")
    parser.add_argument("--target", choices=sorted(TARGET_DIRS), default="cumcm")
    parser.add_argument(
        "--path",
        action="append",
        default=[],
        help="Extra file or directory to scan (repeatable)",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--strict-prose",
        action="store_true",
        help="Promote AI filler and hollow-inference warnings to critical",
    )
    parser.add_argument(
        "--include-main",
        action="store_true",
        default=True,
        help="Include main_*.tex (default true)",
    )
    return parser.parse_args()


def resolve_scan_paths(args: argparse.Namespace) -> list[Path]:
    paths: list[Path] = []
    if args.path:
        for raw in args.path:
            p = Path(raw)
            if not p.is_absolute():
                p = REPO_ROOT / p
            paths.append(p)
    else:
        root = TARGET_DIRS[args.target]
        sections = root / "sections"
        if sections.is_dir():
            paths.append(sections)
        if args.include_main:
            for main in root.glob("main_*.tex"):
                paths.append(main)
    return paths


def iter_tex_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file() and path.suffix == ".tex":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.tex")))
    skip_names = {"cover.tex", "numbering_page.tex", "ai_declaration.tex"}
    return [f for f in files if f.name not in skip_names]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def strip_comment(line: str) -> str:
    return COMMENT_RE.sub("", line)


def scan_file(path: Path, strict_prose: bool) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [
            {
                "severity": "warning",
                "code": "read_failed",
                "message": str(exc),
                "path": display_path(path),
                "line": None,
            }
        ]

    for i, raw in enumerate(lines, start=1):
        if ALLOW_MARKER.search(raw):
            continue
        line = strip_comment(raw)
        if not line.strip():
            continue

        for code, pattern in RULES["meta"]:
            if pattern.search(line):
                findings.append(
                    {
                        "severity": "critical",
                        "code": code,
                        "message": f"instructional/meta-language in paper body: {line.strip()[:120]}",
                        "path": display_path(path),
                        "line": i,
                    }
                )

        # Hollow inference: critical under strict, else warning (still blocks final with --strict-prose)
        for code, pattern in RULES["hollow_inference"]:
            if pattern.search(line):
                sev = "critical" if strict_prose else "warning"
                findings.append(
                    {
                        "severity": sev,
                        "code": code,
                        "message": f"hollow inference / empty connector: {line.strip()[:120]}",
                        "path": display_path(path),
                        "line": i,
                    }
                )

        for code, pattern in RULES["ai_filler"]:
            if pattern.search(line):
                sev = "critical" if strict_prose else "warning"
                findings.append(
                    {
                        "severity": sev,
                        "code": code,
                        "message": f"AI-filler / empty praise: {line.strip()[:120]}",
                        "path": display_path(path),
                        "line": i,
                    }
                )

        for code, pattern in RULES["weak"]:
            if pattern.search(line):
                findings.append(
                    {
                        "severity": "info",
                        "code": code,
                        "message": f"weak professional phrasing: {line.strip()[:120]}",
                        "path": display_path(path),
                        "line": i,
                    }
                )

    return findings


def main() -> int:
    args = parse_args()
    scan_roots = resolve_scan_paths(args)
    files = iter_tex_files(scan_roots)
    findings: list[dict[str, object]] = []

    if not files:
        findings.append(
            {
                "severity": "warning",
                "code": "no_tex",
                "message": "no .tex files found to scan",
                "path": None,
                "line": None,
            }
        )
    else:
        for path in files:
            findings.extend(scan_file(path, args.strict_prose))

    summary = {"critical": 0, "warning": 0, "info": 0}
    for finding in findings:
        sev = str(finding.get("severity", "info"))
        if sev in summary:
            summary[sev] += 1

    status = "critical" if summary["critical"] else "warning" if summary["warning"] else "ok"
    result = {
        "tool": "check_prose_style",
        "status": status,
        "summary": summary,
        "findings": findings,
        "files_scanned": len(files),
        "strict_prose": bool(args.strict_prose),
        "rules_file": str(RULES_PATH.relative_to(REPO_ROOT)),
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"check_prose_style: {status} (files={len(files)})")
        print(
            f"summary: critical={summary['critical']} "
            f"warning={summary['warning']} info={summary['info']}"
        )
        for finding in findings:
            if finding.get("severity") == "info":
                continue
            path = finding.get("path")
            line = finding.get("line")
            loc = f" ({path}:{line})" if path and line else f" ({path})" if path else ""
            print(f"[{finding['severity']}] {finding['code']}: {finding['message']}{loc}")
        if summary["info"]:
            print(f"info findings hidden: {summary['info']}")
        if not findings:
            print("[ok] no prose style issues")

    return 1 if summary["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
