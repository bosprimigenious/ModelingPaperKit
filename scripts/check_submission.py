#!/usr/bin/env python3
"""Submission-oriented checks for ModelingPaperKit templates.

The first version intentionally uses only the Python standard library.  It is a
fast preflight check, not a substitute for official contest rules or PDF review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TARGETS = {
    "cumcm": {
        "dir": Path("templates/cumcm"),
        "main": "main_cumcm.tex",
        "pdf": Path("templates/cumcm/out/main_cumcm.pdf"),
        "log": Path("templates/cumcm/out/main_cumcm.log"),
    }
}

IDENTITY_HINT_RE = re.compile(
    r"学校|学院|导师|指导教师|姓名|学号|队员|手机号|电话|邮箱|email|/Users/|C:\\Users\\|/home/",
    re.IGNORECASE,
)
CACHE_SUFFIXES = {".aux", ".log", ".out", ".toc", ".synctex.gz", ".xdv", ".fls", ".fdb_latexmk"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check CUMCM submission readiness")
    parser.add_argument("--target", default="cumcm", choices=sorted(TARGETS))
    parser.add_argument("--support-dir", default=None, help="Optional supporting material directory")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser.parse_args()


def add_finding(
    findings: list[dict[str, object]],
    severity: str,
    code: str,
    message: str,
    path: Path | None = None,
) -> None:
    findings.append(
        {
            "severity": severity,
            "code": code,
            "message": message,
            "path": str(path.relative_to(REPO_ROOT)) if path and path.is_absolute() else str(path) if path else None,
        }
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def check_cumcm_template(findings: list[dict[str, object]], main_path: Path) -> None:
    text = read_text(main_path)
    if r"\cumcmPaperSubmissionfalse" not in text:
        add_finding(
            findings,
            "warning",
            "submission_mode_unclear",
            "CUMCM electronic-safe default was not found",
            main_path,
        )
    if re.search(r"^[^%]*\\cumcmPaperSubmissiontrue", text, re.MULTILINE):
        add_finding(
            findings,
            "critical",
            "paper_mode_enabled",
            "Paper submission mode appears enabled; electronic PDF may include paper-only pages",
            main_path,
        )
    if re.search(r"^[^%]*\\input\{sections/ai_declaration", text, re.MULTILINE):
        add_finding(
            findings,
            "critical",
            "ai_details_in_paper",
            "AI-use details are included in the main paper; keep them in supporting materials when required",
            main_path,
        )


def check_build_artifacts(findings: list[dict[str, object]], target: dict[str, Path]) -> None:
    pdf = REPO_ROOT / target["pdf"]
    log = REPO_ROOT / target["log"]
    if not pdf.exists():
        add_finding(findings, "warning", "missing_pdf", "Final PDF was not found", pdf)
    if not log.exists():
        add_finding(findings, "info", "missing_log", "Build log was not found", log)


def suspicious_cache_file(path: Path) -> bool:
    name = path.name
    return any(name.endswith(suffix) for suffix in CACHE_SUFFIXES)


def check_support_dir(findings: list[dict[str, object]], support_dir: Path) -> None:
    if not support_dir.exists():
        add_finding(findings, "warning", "missing_support_dir", "Supporting material directory was not found", support_dir)
        return
    for path in support_dir.rglob("*"):
        if path.is_dir():
            continue
        rel = path.relative_to(REPO_ROOT) if path.is_absolute() and path.is_relative_to(REPO_ROOT) else path
        if suspicious_cache_file(path):
            add_finding(findings, "warning", "build_cache_in_support", "Build cache file appears in supporting materials", rel)
        if IDENTITY_HINT_RE.search(str(path)):
            add_finding(findings, "warning", "identity_hint_in_filename", "Filename may contain identity-related text", rel)


def summarize(findings: list[dict[str, object]]) -> dict[str, int]:
    return {
        "critical": sum(1 for f in findings if f["severity"] == "critical"),
        "warning": sum(1 for f in findings if f["severity"] == "warning"),
        "info": sum(1 for f in findings if f["severity"] == "info"),
    }


def main() -> int:
    args = parse_args()
    target = TARGETS[args.target]
    main_path = REPO_ROOT / target["dir"] / target["main"]
    findings: list[dict[str, object]] = []

    if not main_path.exists():
        add_finding(findings, "critical", "missing_main", "Template main file was not found", main_path)
    else:
        check_cumcm_template(findings, main_path)
        check_build_artifacts(findings, target)

    if args.support_dir:
        support_dir = Path(args.support_dir)
        if not support_dir.is_absolute():
            support_dir = REPO_ROOT / support_dir
        check_support_dir(findings, support_dir)

    summary = summarize(findings)
    result = {
        "tool": "check_submission",
        "target": args.target,
        "status": "critical" if summary["critical"] else "warning" if summary["warning"] else "ok",
        "summary": summary,
        "findings": findings,
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"check_submission {args.target}: {result['status']}")
        for finding in findings:
            path = f" ({finding['path']})" if finding["path"] else ""
            print(f"[{finding['severity']}] {finding['code']}: {finding['message']}{path}")

    return 1 if summary["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
