#!/usr/bin/env python3
"""Check artifacts/model_fitness.md structure and optional PASS-all gate."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

ROW_RE = re.compile(r"^\|(.+)\|$")
HOLLOW_RE = re.compile(r"根据.{0,40}(?:可)?知|由此(?:可)?见")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check model fitness report artifact")
    parser.add_argument("--artifacts", default="artifacts")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--require",
        action="store_true",
        help="Missing model_fitness.md is critical",
    )
    parser.add_argument(
        "--require-pass",
        action="store_true",
        help="Every Qi verdict must be PASS",
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
            continue
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


def main() -> int:
    args = parse_args()
    art = resolve(args.artifacts)
    path = art / "model_fitness.md"
    findings: list[dict[str, object]] = []

    if not path.exists():
        findings.append(
            {
                "severity": "critical" if args.require or args.require_pass else "warning",
                "code": "missing_model_fitness",
                "message": f"missing {display(path)}; copy skills/cumcm-model-fitness/references/fitness-report-template.md",
                "path": str(path),
                "line": None,
            }
        )
    else:
        text = path.read_text(encoding="utf-8")
        # Prefer the markdown table whose headers include Verdict (per-Qi table)
        headers, rows = [], []
        best: tuple[list[str], list[list[str]]] | None = None
        # Scan sliding windows by rebuilding tables from line groups
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            if not ROW_RE.match(lines[i].strip()):
                i += 1
                continue
            block = []
            while i < len(lines) and ROW_RE.match(lines[i].strip()):
                block.append(lines[i])
                i += 1
            h, r = parse_md_table("\n".join(block))
            if h and r and col_index(h, "verdict", "结论", "判定") is not None:
                # Prefer tables that also look like Qi rows
                if col_index(h, "qi", "sub", "问") is not None or col_index(h, "required form", "form") is not None:
                    best = (h, r)
                    break
                if best is None:
                    best = (h, r)
        if best:
            headers, rows = best
        else:
            headers, rows = parse_md_table(text)
        if not rows:
            findings.append(
                {
                    "severity": "critical",
                    "code": "empty_fitness_table",
                    "message": "model_fitness.md has no data rows in a markdown table",
                    "path": display(path),
                    "line": None,
                }
            )
        else:
            qi_i = col_index(headers, "qi", "sub", "问")
            form_i = col_index(headers, "required form", "form", "形态", "deliverable")
            art_i = col_index(headers, "output", "artifact", "产物")
            verd_i = col_index(headers, "verdict", "结论", "判定")
            match_i = col_index(headers, "form match", "match")

            if verd_i is None:
                findings.append(
                    {
                        "severity": "critical",
                        "code": "no_verdict_column",
                        "message": "fitness table needs a Verdict column (PASS/REFINE/REJECT)",
                        "path": display(path),
                        "line": None,
                    }
                )

            for n, row in enumerate(rows, start=1):
                label = row[qi_i] if qi_i is not None else f"row{n}"
                if not str(label).strip() or set(str(label).strip()) <= set("-"):
                    continue

                if form_i is not None:
                    form = row[form_i].strip()
                    if not form or form in {"-", "TBD", "待定"}:
                        findings.append(
                            {
                                "severity": "critical",
                                "code": "missing_required_form",
                                "message": f"{label}: Required form empty",
                                "path": display(path),
                                "line": None,
                            }
                        )

                verdict = row[verd_i].strip().upper() if verd_i is not None else ""
                # normalize
                if "PASS" in verdict:
                    vnorm = "PASS"
                elif "REJECT" in verdict:
                    vnorm = "REJECT"
                elif "REFINE" in verdict:
                    vnorm = "REFINE"
                else:
                    vnorm = verdict or "MISSING"

                if vnorm == "MISSING":
                    findings.append(
                        {
                            "severity": "critical",
                            "code": "missing_verdict",
                            "message": f"{label}: Verdict must be PASS/REFINE/REJECT",
                            "path": display(path),
                            "line": None,
                        }
                    )
                elif args.require_pass and vnorm != "PASS":
                    findings.append(
                        {
                            "severity": "critical",
                            "code": "verdict_not_pass",
                            "message": f"{label}: verdict is {vnorm}, --require-pass set",
                            "path": display(path),
                            "line": None,
                        }
                    )

                if vnorm == "PASS" and art_i is not None:
                    out = row[art_i].strip().strip("`")
                    if not out or out in {"-", "TBD", "待定", "N/A"}:
                        findings.append(
                            {
                                "severity": "critical",
                                "code": "pass_without_artifact",
                                "message": f"{label}: PASS requires Output artifact path",
                                "path": display(path),
                                "line": None,
                            }
                        )
                    else:
                        for piece in re.split(r"[,;，；]", out):
                            piece = piece.strip()
                            if not piece:
                                continue
                            cand = Path(piece)
                            if not cand.is_absolute():
                                c1 = (art / piece).resolve()
                                c2 = (REPO_ROOT / piece).resolve()
                            else:
                                c1 = c2 = cand
                            if not c1.exists() and not c2.exists():
                                findings.append(
                                    {
                                        "severity": "warning",
                                        "code": "artifact_missing",
                                        "message": f"{label}: artifact not found: {piece}",
                                        "path": display(path),
                                        "line": None,
                                    }
                                )

                if match_i is not None:
                    m = row[match_i].strip().lower()
                    if vnorm == "PASS" and m in {"n", "no", "否", "false"}:
                        findings.append(
                            {
                                "severity": "critical",
                                "code": "pass_but_form_mismatch",
                                "message": f"{label}: PASS but Form match is No",
                                "path": display(path),
                                "line": None,
                            }
                        )

        # Direct answers section hollow check
        for i, line in enumerate(text.splitlines(), start=1):
            if HOLLOW_RE.search(line) and "模板" not in line:
                findings.append(
                    {
                        "severity": "warning",
                        "code": "hollow_in_fitness_report",
                        "message": f"hollow phrasing in fitness report: {line.strip()[:100]}",
                        "path": display(path),
                        "line": i,
                    }
                )

    summary = {"critical": 0, "warning": 0, "info": 0}
    for f in findings:
        sev = str(f.get("severity", "info"))
        if sev in summary:
            summary[sev] += 1

    status = "critical" if summary["critical"] else "warning" if summary["warning"] else "ok"
    result = {
        "tool": "check_model_fitness",
        "status": status,
        "summary": summary,
        "findings": findings,
        "artifacts": display(art) if art.exists() else str(art),
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"check_model_fitness: {status}")
        print(
            f"summary: critical={summary['critical']} "
            f"warning={summary['warning']} info={summary['info']}"
        )
        for f in findings:
            path = f.get("path")
            line = f.get("line")
            loc = f" ({path}:{line})" if path and line else f" ({path})" if path else ""
            print(f"[{f['severity']}] {f['code']}: {f['message']}{loc}")
        if not findings:
            print("[ok] model fitness artifact looks structured")

    return 1 if summary["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
