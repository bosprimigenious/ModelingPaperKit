#!/usr/bin/env python3
"""Inspect ModelingPaperKit template structure and drafting status."""

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
        "out_dir": Path("templates/cumcm/out"),
        "expected_sections": [
            "problem.tex",
            "analysis.tex",
            "assumptions.tex",
            "notation.tex",
            "model.tex",
            "solution.tex",
            "results.tex",
            "validation.tex",
            "evaluation.tex",
            "conclusion.tex",
            "references.tex",
            "appendix.tex",
        ],
        "special_pages": ["cover.tex", "numbering_page.tex", "ai_declaration.tex"],
    }
}

INPUT_RE = re.compile(r"\\input\{([^{}]+)\}")
SECTION_RE = re.compile(r"\\(?:section|subsection|subsubsection)\*?\{([^{}]+)\}")
PLACEHOLDER_RE = re.compile(r"在此|\[在此|关键词一|问题一|问题二|示例|TODO|占位", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect template structure")
    parser.add_argument("--target", default="cumcm", choices=sorted(TARGETS))
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser.parse_args()


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def strip_comment(line: str) -> str:
    escaped = False
    out: list[str] = []
    for char in line:
        if char == "%" and not escaped:
            break
        out.append(char)
        escaped = char == "\\" and not escaped
        if char != "\\":
            escaped = False
    return "".join(out)


def active_text(text: str) -> str:
    return "\n".join(strip_comment(line) for line in text.splitlines())


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
            "path": display_path(path) if path else None,
        }
    )


def resolve_input(template_dir: Path, raw: str) -> Path:
    path = template_dir / raw
    if path.suffix:
        return path
    return path.with_suffix(".tex")


def count_placeholders(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    return len(PLACEHOLDER_RE.findall(text))


def extract_headings(path: Path) -> list[str]:
    text = active_text(path.read_text(encoding="utf-8", errors="replace"))
    return [match.group(1) for match in SECTION_RE.finditer(text)]


def inspect_target(target_key: str) -> dict[str, object]:
    target = TARGETS[target_key]
    template_dir = REPO_ROOT / target["dir"]
    main_path = template_dir / target["main"]
    out_dir = REPO_ROOT / target["out_dir"]
    findings: list[dict[str, object]] = []

    sections_present: list[str] = []
    sections_missing: list[str] = []
    included_files: list[str] = []
    section_status: list[dict[str, object]] = []
    special_pages: dict[str, bool] = {}

    if not main_path.exists():
        add_finding(findings, "critical", "missing_main", "Template main file is missing", main_path)
    else:
        main_text = active_text(main_path.read_text(encoding="utf-8", errors="replace"))
        for match in INPUT_RE.finditer(main_text):
            raw = match.group(1)
            included = resolve_input(template_dir, raw)
            included_files.append(display_path(included))
        for section_name in target["expected_sections"]:
            path = template_dir / "sections" / section_name
            if path.exists():
                sections_present.append(section_name)
                placeholders = count_placeholders(path)
                section_status.append(
                    {
                        "file": display_path(path),
                        "placeholders": placeholders,
                        "headings": extract_headings(path),
                    }
                )
                if placeholders > 0:
                    add_finding(findings, "info", "section_placeholders", f"Section still contains placeholders: {section_name}", path)
            else:
                sections_missing.append(section_name)
                add_finding(findings, "critical", "missing_section", f"Expected section is missing: {section_name}", path)

        for page in target["special_pages"]:
            path = template_dir / "sections" / page
            special_pages[page] = path.exists()
            if not path.exists():
                add_finding(findings, "warning", "missing_special_page", f"Special page template is missing: {page}", path)

        if r"\cumcmPaperSubmissionfalse" not in main_text:
            add_finding(findings, "warning", "submission_mode_unclear", "Electronic-safe default marker was not found", main_path)

    pdf = out_dir / target["main"].replace(".tex", ".pdf")
    log = out_dir / target["main"].replace(".tex", ".log")
    artifacts = {
        "pdf": display_path(pdf) if pdf.exists() else None,
        "log": display_path(log) if log.exists() else None,
    }
    if not pdf.exists():
        add_finding(findings, "warning", "missing_pdf", "Compiled PDF was not found", pdf)
    if not log.exists():
        add_finding(findings, "info", "missing_log", "Build log was not found", log)

    summary = {
        "critical": sum(1 for f in findings if f["severity"] == "critical"),
        "warning": sum(1 for f in findings if f["severity"] == "warning"),
        "info": sum(1 for f in findings if f["severity"] == "info"),
    }
    return {
        "tool": "inspect_template",
        "target": target_key,
        "status": "critical" if summary["critical"] else "warning" if summary["warning"] else "ok",
        "summary": summary,
        "template": {
            "dir": display_path(template_dir),
            "main": target["main"],
            "out_dir": display_path(out_dir),
        },
        "sections": {
            "present": sections_present,
            "missing": sections_missing,
            "included": included_files,
            "status": section_status,
        },
        "special_pages": special_pages,
        "artifacts": artifacts,
        "findings": findings,
    }


def main() -> int:
    args = parse_args()
    result = inspect_target(args.target)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"inspect_template {args.target}: {result['status']}")
        for finding in result["findings"]:
            path = f" ({finding['path']})" if finding["path"] else ""
            print(f"[{finding['severity']}] {finding['code']}: {finding['message']}{path}")
    return 1 if result["summary"]["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
