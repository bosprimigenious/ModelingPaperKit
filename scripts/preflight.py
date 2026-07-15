#!/usr/bin/env python3
"""Run ModelingPaperKit preflight checks as one command."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ModelingPaperKit preflight checks")
    parser.add_argument("--target", default="cumcm", choices=["cumcm"])
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--strict-placeholders", action="store_true")
    parser.add_argument("--skip-skills", action="store_true")
    parser.add_argument("--skip-git-diff-check", action="store_true")
    return parser.parse_args()


def run_json_tool(name: str, args: list[str]) -> dict[str, object]:
    proc = subprocess.run(
        [sys.executable, *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        return {
            "tool": name,
            "status": "warning",
            "summary": {"critical": 0, "warning": 1, "info": 0},
            "findings": [
                {
                    "severity": "warning",
                    "code": "tool_failed",
                    "message": proc.stderr.strip() or f"{name} failed",
                    "path": None,
                    "line": None,
                }
            ],
        }
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {
            "tool": name,
            "status": "warning",
            "summary": {"critical": 0, "warning": 1, "info": 0},
            "findings": [
                {
                    "severity": "warning",
                    "code": "bad_json",
                    "message": f"{name} did not produce valid JSON",
                    "path": None,
                    "line": None,
                }
            ],
        }


def run_text_check(name: str, args: list[str]) -> dict[str, object]:
    proc = subprocess.run(args, cwd=REPO_ROOT, check=False, capture_output=True, text=True)
    if proc.returncode == 0:
        return {
            "tool": name,
            "status": "ok",
            "summary": {"critical": 0, "warning": 0, "info": 0},
            "findings": [],
        }
    return {
        "tool": name,
        "status": "critical",
        "summary": {"critical": 1, "warning": 0, "info": 0},
        "findings": [
            {
                "severity": "critical",
                "code": "check_failed",
                "message": (proc.stdout + proc.stderr).strip() or f"{name} failed",
                "path": None,
                "line": None,
            }
        ],
    }


def combine(results: list[dict[str, object]], target: str) -> dict[str, object]:
    summary = {"critical": 0, "warning": 0, "info": 0}
    findings: list[dict[str, object]] = []
    for result in results:
        result_summary = result.get("summary", {})
        for key in summary:
            summary[key] += int(result_summary.get(key, 0))  # type: ignore[union-attr]
        for finding in result.get("findings", []):
            if isinstance(finding, dict):
                item = dict(finding)
                item["source_tool"] = result.get("tool")
                findings.append(item)
    return {
        "tool": "preflight",
        "target": target,
        "status": "critical" if summary["critical"] else "warning" if summary["warning"] else "ok",
        "summary": summary,
        "checks": results,
        "findings": findings,
    }


def main() -> int:
    args = parse_args()
    results: list[dict[str, object]] = []

    results.append(run_json_tool("inspect_template", ["scripts/inspect_template.py", "--target", args.target, "--format", "json"]))
    results.append(run_json_tool("check_identity_leaks", ["scripts/check_identity_leaks.py", "templates/cumcm", "--format", "json"]))

    tex_args = ["scripts/check_tex_links.py", "--target", args.target, "--format", "json"]
    if args.strict_placeholders:
        tex_args.append("--strict-placeholders")
    results.append(run_json_tool("check_tex_links", tex_args))

    submission_args = ["scripts/check_submission.py", "--target", args.target, "--format", "json"]
    results.append(run_json_tool("check_submission", submission_args))
    results.append(run_json_tool("summarize_build_log", ["scripts/summarize_build_log.py", "--target", args.target, "--format", "json"]))

    if not args.skip_skills:
        results.append(run_text_check("check_skills", [sys.executable, "scripts/check_skills.py", "skills"]))
    if not args.skip_git_diff_check:
        results.append(run_text_check("git_diff_check", ["git", "diff", "--check"]))

    result = combine(results, args.target)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"preflight {args.target}: {result['status']}")
        print(
            f"summary: critical={result['summary']['critical']} "
            f"warning={result['summary']['warning']} info={result['summary']['info']}"
        )
        for finding in result["findings"]:
            path = finding.get("path")
            line = finding.get("line")
            loc = f" ({path}:{line})" if path and line else f" ({path})" if path else ""
            print(
                f"[{finding.get('severity')}] {finding.get('source_tool')}/"
                f"{finding.get('code')}: {finding.get('message')}{loc}"
            )
    return 1 if result["summary"]["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
