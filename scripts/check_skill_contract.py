#!/usr/bin/env python3
"""Verify each skill has an operable contract (trigger, outputs, acceptance)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_HEADINGS = (
    "When to use",
    "Required inputs",
    "Required outputs",
    "Must not",
    "Acceptance",
)

# High-leverage skills that must also ship a fixture or example reference.
FIXTURE_REQUIRED = {
    "cumcm-problem-reading",
    "cumcm-modeling-plan",
    "cumcm-result-consistency",
    "cumcm-sentence-polish",
    "cumcm-final-review",
    "cumcm-submission-pack",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check skill contracts / acceptance files")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["skills"],
        help="Skill folder or parent directory (default: skills)",
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--require-fixtures",
        action="store_true",
        help="Require fixtures/ or acceptance examples for high-leverage skills",
    )
    return parser.parse_args()


def discover_skill_dirs(paths: list[str]) -> list[Path]:
    dirs: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = REPO_ROOT / path
        path = path.resolve()
        if (path / "SKILL.md").exists():
            dirs.append(path)
        elif path.is_dir():
            dirs.extend(sorted(p for p in path.iterdir() if (p / "SKILL.md").exists()))
        else:
            # missing path reported later as finding via empty dirs
            pass
    return sorted(set(dirs))


def contract_text(skill_dir: Path) -> tuple[str, str | None]:
    """Return (text, source_label). Prefer acceptance.md, else SKILL.md Contract section."""
    acceptance = skill_dir / "acceptance.md"
    if acceptance.exists():
        return acceptance.read_text(encoding="utf-8"), "acceptance.md"
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    # Optional ## Contract block inside SKILL.md
    match = re.search(r"^##\s+Contract\s*$", text, re.MULTILINE)
    if match:
        return text[match.start() :], "SKILL.md#Contract"
    return text, "SKILL.md"


def has_heading(text: str, heading: str) -> bool:
    patterns = [
        rf"^##\s+{re.escape(heading)}\s*$",
        rf"^###\s+{re.escape(heading)}\s*$",
        rf"^\*\*{re.escape(heading)}\*\*",
        rf"^{re.escape(heading)}\s*:",
    ]
    return any(re.search(p, text, re.MULTILINE | re.IGNORECASE) for p in patterns)


def check_skill(skill_dir: Path, require_fixtures: bool) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    name = skill_dir.name
    rel = str(skill_dir.relative_to(REPO_ROOT))

    if not (skill_dir / "SKILL.md").exists():
        findings.append(
            {
                "severity": "critical",
                "code": "missing_skill_md",
                "message": f"{name}: missing SKILL.md",
                "path": rel,
                "line": None,
            }
        )
        return findings

    text, source = contract_text(skill_dir)
    if source == "SKILL.md" and not (skill_dir / "acceptance.md").exists():
        # Full SKILL.md may still satisfy headings; warn if contract file missing for cumcm-*.
        if name.startswith("cumcm-") or name in {"modeling-paperkit", "cumcm-sentence-polish"}:
            # Only critical if headings also missing; warning for missing dedicated file.
            missing = [h for h in REQUIRED_HEADINGS if not has_heading(text, h)]
            if missing:
                findings.append(
                    {
                        "severity": "critical",
                        "code": "missing_acceptance",
                        "message": (
                            f"{name}: missing acceptance.md and SKILL.md lacks contract "
                            f"headings: {', '.join(missing)}"
                        ),
                        "path": rel,
                        "line": None,
                    }
                )
            else:
                findings.append(
                    {
                        "severity": "warning",
                        "code": "acceptance_in_skill_only",
                        "message": f"{name}: contract lives only in SKILL.md; prefer acceptance.md",
                        "path": rel,
                        "line": None,
                    }
                )
    else:
        missing = [h for h in REQUIRED_HEADINGS if not has_heading(text, h)]
        for heading in missing:
            findings.append(
                {
                    "severity": "critical",
                    "code": "missing_contract_heading",
                    "message": f"{name}: {source} missing heading '{heading}'",
                    "path": f"{rel}/{source.split('#')[0]}",
                    "line": None,
                }
            )

    # Referenced reference files mentioned as `references/foo.md` should exist.
    for match in re.finditer(r"references/([a-zA-Z0-9_./-]+\.md)", text):
        ref = skill_dir / "references" / match.group(1).split("/")[-1]
        # Also allow nested path under references/
        nested = skill_dir / "references" / match.group(1)
        if not ref.exists() and not nested.exists():
            # Try path as written relative to skill dir
            alt = skill_dir / "references" / match.group(1)
            if not alt.exists():
                findings.append(
                    {
                        "severity": "warning",
                        "code": "missing_reference",
                        "message": f"{name}: referenced references/{match.group(1)} not found",
                        "path": rel,
                        "line": None,
                    }
                )

    if require_fixtures and name in FIXTURE_REQUIRED:
        fixtures = skill_dir / "fixtures"
        has_fix = fixtures.is_dir() and any(fixtures.iterdir())
        has_examples = (skill_dir / "references" / "examples.md").exists()
        if not has_fix and not has_examples:
            findings.append(
                {
                    "severity": "warning",
                    "code": "missing_fixture",
                    "message": (
                        f"{name}: high-leverage skill should have fixtures/ or references/examples.md"
                    ),
                    "path": rel,
                    "line": None,
                }
            )

    return findings


def main() -> int:
    args = parse_args()
    skill_dirs = discover_skill_dirs(args.paths)
    findings: list[dict[str, object]] = []

    if not skill_dirs:
        findings.append(
            {
                "severity": "critical",
                "code": "no_skills",
                "message": "no skill folders found",
                "path": None,
                "line": None,
            }
        )
    else:
        for skill_dir in skill_dirs:
            findings.extend(check_skill(skill_dir, args.require_fixtures))

    summary = {"critical": 0, "warning": 0, "info": 0}
    for finding in findings:
        sev = str(finding.get("severity", "info"))
        if sev in summary:
            summary[sev] += 1

    status = "critical" if summary["critical"] else "warning" if summary["warning"] else "ok"
    result = {
        "tool": "check_skill_contract",
        "status": status,
        "summary": summary,
        "findings": findings,
        "skills_checked": len(skill_dirs),
    }

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"check_skill_contract: {status} (skills={len(skill_dirs)})")
        print(
            f"summary: critical={summary['critical']} "
            f"warning={summary['warning']} info={summary['info']}"
        )
        for finding in findings:
            path = finding.get("path")
            loc = f" ({path})" if path else ""
            print(f"[{finding['severity']}] {finding['code']}: {finding['message']}{loc}")
        if not findings:
            print("[ok] all skill contracts present")

    return 1 if summary["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
