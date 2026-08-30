#!/usr/bin/env python3
"""Lightweight coverage check for task_matrix.md and claim_map.md artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ROW_RE = re.compile(r"^\|(.+)\|$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check task matrix / claim map coverage")
    parser.add_argument(
        "--artifacts",
        default="artifacts",
        help="Directory containing task_matrix.md and/or claim_map.md",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--require",
        action="store_true",
        help="Treat missing artifact files as critical instead of warning",
    )
    return parser.parse_args()


def resolve(path: str | Path) -> Path:
    p = Path(path)
    return p if p.is_absolute() else REPO_ROOT / p


def display(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def parse_md_table(text: str) -> tuple[list[str], list[list[str]]]:
    headers: list[str] = []
    rows: list[list[str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= set("-: ") and c for c in cells):
            continue  # separator
        if not headers:
            headers = cells
            continue
        if len(cells) < len(headers):
            cells = cells + [""] * (len(headers) - len(cells))
        rows.append(cells[: len(headers)])
    return headers, rows


def col_index(headers: list[str], *names: str) -> int | None:
    lowered = [h.lower() for h in headers]
    for name in names:
        for i, h in enumerate(lowered):
            if name.lower() in h:
                return i
    return None


def check_task_matrix(path: Path, require: bool) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    if not path.exists():
        findings.append(
            {
                "severity": "critical" if require else "warning",
                "code": "missing_task_matrix",
                "message": f"missing {display(path)}",
                "path": display(path) if path.exists() else str(path),
                "line": None,
            }
        )
        return findings

    text = path.read_text(encoding="utf-8")
    headers, rows = parse_md_table(text)
    if not headers or not rows:
        findings.append(
            {
                "severity": "critical",
                "code": "empty_task_matrix",
                "message": "task_matrix.md has no data rows",
                "path": display(path),
                "line": None,
            }
        )
        return findings

    out_i = col_index(headers, "output", "artifact", "产物")
    sub_i = col_index(headers, "subproblem", "子问", "question")
    base = path.parent

    for n, row in enumerate(rows, start=1):
        label = row[sub_i] if sub_i is not None else f"row {n}"
        if out_i is None:
            findings.append(
                {
                    "severity": "warning",
                    "code": "no_output_column",
                    "message": "task_matrix missing Output artifact column",
                    "path": display(path),
                    "line": None,
                }
            )
            break
        artifact = row[out_i].strip()
        if not artifact or artifact in {"-", "TBD", "待定", "N/A"}:
            findings.append(
                {
                    "severity": "critical",
                    "code": "missing_output_artifact",
                    "message": f"subproblem '{label}' has empty output artifact",
                    "path": display(path),
                    "line": None,
                }
            )
            continue
        # Allow comma-separated paths
        for piece in re.split(r"[,;，；]", artifact):
            piece = piece.strip().strip("`")
            if not piece:
                continue
            candidate = Path(piece)
            if not candidate.is_absolute():
                candidate = (base / piece).resolve()
                alt = (REPO_ROOT / piece).resolve()
            else:
                alt = candidate
            if not candidate.exists() and not alt.exists():
                findings.append(
                    {
                        "severity": "warning",
                        "code": "artifact_path_missing",
                        "message": f"subproblem '{label}': artifact not found: {piece}",
                        "path": display(path),
                        "line": None,
                    }
                )
    return findings


def check_claim_map(path: Path, require: bool) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    if not path.exists():
        findings.append(
            {
                "severity": "critical" if require else "warning",
                "code": "missing_claim_map",
                "message": f"missing {display(path)}",
                "path": str(path),
                "line": None,
            }
        )
        return findings

    text = path.read_text(encoding="utf-8")
    headers, rows = parse_md_table(text)
    if not headers or not rows:
        findings.append(
            {
                "severity": "critical",
                "code": "empty_claim_map",
                "message": "claim_map.md has no data rows",
                "path": display(path),
                "line": None,
            }
        )
        return findings

    claim_i = col_index(headers, "claim", "主张")
    src_i = col_index(headers, "source", "artifact", "来源", "产物")
    base = path.parent

    for n, row in enumerate(rows, start=1):
        claim = row[claim_i] if claim_i is not None else f"row {n}"
        if src_i is None:
            findings.append(
                {
                    "severity": "warning",
                    "code": "no_source_column",
                    "message": "claim_map missing Source artifact column",
                    "path": display(path),
                    "line": None,
                }
            )
            break
        src = row[src_i].strip().strip("`")
        if not src or src in {"-", "TBD", "待定", "N/A"}:
            findings.append(
                {
                    "severity": "critical",
                    "code": "claim_without_source",
                    "message": f"claim has no source artifact: {claim[:80]}",
                    "path": display(path),
                    "line": None,
                }
            )
            continue
        candidate = Path(src)
        if not candidate.is_absolute():
            candidate = (base / src).resolve()
            alt = (REPO_ROOT / src).resolve()
        else:
            alt = candidate
        if not candidate.exists() and not alt.exists():
            findings.append(
                {
                    "severity": "warning",
                    "code": "claim_source_missing",
                    "message": f"claim source not found: {src} (claim: {claim[:60]})",
                    "path": display(path),
                    "line": None,
                }
            )
    return findings


def main() -> int:
    args = parse_args()
    art = resolve(args.artifacts)
    findings: list[dict[str, object]] = []
    findings.extend(check_task_matrix(art / "task_matrix.md", args.require))
    findings.extend(check_claim_map(art / "claim_map.md", args.require))

    summary = {"critical": 0, "warning": 0, "info": 0}
    for finding in findings:
        sev = str(finding.get("severity", "info"))
        if sev in summary:
            summary[sev] += 1

    status = "critical" if summary["critical"] else "warning" if summary["warning"] else "ok"
    result = {
        "tool": "check_claim_coverage",
        "status": status,
        "summary": summary,
        "findings": findings,
        "artifacts": display(art) if art.exists() else str(art),
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"check_claim_coverage: {status}")
        print(
            f"summary: critical={summary['critical']} "
            f"warning={summary['warning']} info={summary['info']}"
        )
        for finding in findings:
            path = finding.get("path")
            loc = f" ({path})" if path else ""
            print(f"[{finding['severity']}] {finding['code']}: {finding['message']}{loc}")
        if not findings:
            print("[ok] coverage artifacts look complete")

    return 1 if summary["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
