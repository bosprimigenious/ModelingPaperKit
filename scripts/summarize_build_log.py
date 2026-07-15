#!/usr/bin/env python3
"""Summarize LaTeX build logs for ModelingPaperKit."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TARGETS = {
    "cumcm": Path("templates/cumcm/out/main_cumcm.log"),
    "mcm": Path("templates/mcm/out/main_mcm.log"),
    "wuyi": Path("templates/wuyi/out/main_wuyi.log"),
    "beijing": Path("templates/beijing/out/main_beijing.log"),
    "example": Path("examples/cumcm_walkthrough/out/main.log"),
}

PATTERNS = [
    ("critical", "latex_error", re.compile(r"^! LaTeX Error:\s*(.+)$", re.MULTILINE)),
    ("critical", "tex_error", re.compile(r"^!\s+(.+)$", re.MULTILINE)),
    ("critical", "emergency_stop", re.compile(r"Emergency stop", re.IGNORECASE)),
    ("critical", "fatal_error", re.compile(r"Fatal error occurred", re.IGNORECASE)),
    ("warning", "missing_file", re.compile(r"LaTeX Warning: File `([^']+)' not found")),
    ("warning", "undefined_reference", re.compile(r"LaTeX Warning: Reference `([^']+)' .*undefined")),
    ("warning", "undefined_citation", re.compile(r"LaTeX Warning: Citation `([^']+)' .*undefined")),
    ("warning", "rerun_needed", re.compile(r"Rerun to get (cross-references|outlines) right")),
    ("warning", "overfull_hbox", re.compile(r"Overfull \\hbox .+")),
    ("info", "underfull_hbox", re.compile(r"Underfull \\hbox .+")),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize LaTeX build logs")
    parser.add_argument("--target", choices=sorted(TARGETS), default=None)
    parser.add_argument("--log", default=None, help="Explicit .log path")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--max-findings", type=int, default=40)
    return parser.parse_args()


def resolve_log(args: argparse.Namespace) -> tuple[str | None, Path]:
    if args.log:
        path = Path(args.log)
        return args.target, path if path.is_absolute() else REPO_ROOT / path
    target = args.target or "cumcm"
    return target, REPO_ROOT / TARGETS[target]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def add_finding(
    findings: list[dict[str, object]],
    severity: str,
    code: str,
    message: str,
    path: Path,
    line: int | None,
) -> None:
    findings.append(
        {
            "severity": severity,
            "code": code,
            "message": message.strip(),
            "path": display_path(path),
            "line": line,
        }
    )


def summarize(findings: list[dict[str, object]]) -> dict[str, int]:
    return {
        "critical": sum(1 for f in findings if f["severity"] == "critical"),
        "warning": sum(1 for f in findings if f["severity"] == "warning"),
        "info": sum(1 for f in findings if f["severity"] == "info"),
    }


def parse_log(path: Path, max_findings: int) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    findings: list[dict[str, object]] = []
    seen: set[tuple[str, str, int]] = set()
    for severity, code, pattern in PATTERNS:
        for match in pattern.finditer(text):
            line = line_for_offset(text, match.start())
            message = match.group(1) if match.groups() else match.group(0)
            key = (code, message, line)
            if key in seen:
                continue
            seen.add(key)
            add_finding(findings, severity, code, message, path, line)
            if len(findings) >= max_findings:
                return findings
    return findings


def main() -> int:
    args = parse_args()
    target, log_path = resolve_log(args)
    findings: list[dict[str, object]] = []

    if not log_path.exists():
        add_finding(findings, "info", "missing_log", "Build log was not found", log_path, None)
    else:
        findings.extend(parse_log(log_path, args.max_findings))

    summary = summarize(findings)
    result = {
        "tool": "summarize_build_log",
        "target": target,
        "status": "critical" if summary["critical"] else "warning" if summary["warning"] else "ok",
        "summary": summary,
        "findings": findings,
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"summarize_build_log {target or display_path(log_path)}: {result['status']}")
        for finding in findings:
            location = f" ({finding['path']}:{finding['line']})" if finding["line"] else f" ({finding['path']})"
            print(f"[{finding['severity']}] {finding['code']}: {finding['message']}{location}")
    return 1 if summary["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
