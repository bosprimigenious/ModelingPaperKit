#!/usr/bin/env python3
"""Check basic TeX links, labels, citations, inputs, and figure assets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TARGETS = {
    "cumcm": {
        "dir": Path("templates/cumcm"),
        "main": "main_cumcm.tex",
        "graphics_paths": [Path("figures"), Path("../02_figures")],
    }
}

INPUT_RE = re.compile(r"\\input\{([^{}]+)\}")
LABEL_RE = re.compile(r"\\label\{([^{}]+)\}")
REF_RE = re.compile(r"\\(?:ref|eqref|cref|Cref)\{([^{}]+)\}")
CITE_RE = re.compile(r"\\(?:cite|upcite|supercite)\{([^{}]+)\}")
BIBITEM_RE = re.compile(r"\\bibitem(?:\[[^\]]*\])?\{([^{}]+)\}")
INCLUDEGRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^{}]+)\}")
FIGPLOT_RE = re.compile(r"\\figplot\b")
GRAPHICSPATH_RE = re.compile(r"\\graphicspath\{(.+)\}")
PATH_IN_BRACES_RE = re.compile(r"\{([^{}]+)\}")
TEX_EXTENSIONS = ["", ".tex"]
GRAPHIC_EXTENSIONS = ["", ".pdf", ".png", ".jpg", ".jpeg", ".eps"]


@dataclass(frozen=True)
class SourceFile:
    path: Path
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check TeX links and assets")
    parser.add_argument("--target", default="cumcm", choices=sorted(TARGETS))
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument(
        "--strict-placeholders",
        action="store_true",
        help="Treat missing figplot placeholder assets as warnings instead of info",
    )
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


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def add_finding(
    findings: list[dict[str, object]],
    severity: str,
    code: str,
    message: str,
    path: Path | None = None,
    line: int | None = None,
) -> None:
    findings.append(
        {
            "severity": severity,
            "code": code,
            "message": message,
            "path": display_path(path) if path else None,
            "line": line,
        }
    )


def resolve_input(base_dir: Path, raw: str) -> Path | None:
    candidate = Path(raw)
    for ext in TEX_EXTENSIONS:
        path = base_dir / f"{candidate}{ext}"
        if path.exists():
            return path.resolve()
    return None


def collect_sources(main_path: Path, findings: list[dict[str, object]]) -> list[SourceFile]:
    sources: list[SourceFile] = []
    seen: set[Path] = set()

    def visit(path: Path) -> None:
        resolved = path.resolve()
        if resolved in seen:
            return
        seen.add(resolved)
        text = path.read_text(encoding="utf-8", errors="replace")
        sources.append(SourceFile(resolved, text))
        clean = active_text(text)
        for match in INPUT_RE.finditer(clean):
            raw = match.group(1)
            child = resolve_input(path.parent, raw)
            if child:
                visit(child)
            else:
                add_finding(
                    findings,
                    "critical",
                    "missing_input",
                    f"Input file was not found: {raw}",
                    resolved,
                    line_for_offset(clean, match.start()),
                )

    visit(main_path)
    return sources


def split_csv_values(raw: str) -> list[str]:
    values: list[str] = []
    for value in raw.split(","):
        value = value.strip()
        if value:
            values.append(value)
    return values


def parse_graphics_paths(source: SourceFile, template_dir: Path) -> list[Path]:
    paths: list[Path] = []
    clean = active_text(source.text)
    for match in GRAPHICSPATH_RE.finditer(clean):
        for raw in PATH_IN_BRACES_RE.findall(match.group(1)):
            paths.append((source.path.parent / raw).resolve())
    if source.path.parent == template_dir.resolve():
        target = TARGETS["cumcm"]
        for raw in target["graphics_paths"]:
            paths.append((template_dir / raw).resolve())
    return paths


def find_graphic(source_dir: Path, graphics_paths: list[Path], raw: str) -> bool:
    candidate = Path(raw)
    search_dirs = [source_dir, *graphics_paths]
    for directory in search_dirs:
        for ext in GRAPHIC_EXTENSIONS:
            path = directory / f"{candidate}{ext}"
            if path.exists():
                return True
    return False


def extract_figplot_file(text: str, start: int) -> tuple[str | None, int]:
    args: list[str] = []
    pos = start
    while len(args) < 5 and pos < len(text):
        brace = text.find("{", pos)
        if brace == -1:
            return None, pos
        depth = 0
        for idx in range(brace, len(text)):
            if text[idx] == "{":
                depth += 1
            elif text[idx] == "}":
                depth -= 1
                if depth == 0:
                    args.append(text[brace + 1 : idx])
                    pos = idx + 1
                    break
        else:
            return None, pos
    return (args[4].strip() if len(args) >= 5 else None), pos


def check_sources(
    sources: list[SourceFile],
    template_dir: Path,
    findings: list[dict[str, object]],
    *,
    strict_placeholders: bool,
) -> None:
    labels: dict[str, tuple[Path, int]] = {}
    refs: list[tuple[str, Path, int]] = []
    cites: list[tuple[str, Path, int]] = []
    bibitems: set[str] = set()
    graphics_paths: list[Path] = []

    for source in sources:
        graphics_paths.extend(parse_graphics_paths(source, template_dir))
    graphics_paths = sorted(set(graphics_paths))

    for source in sources:
        clean = active_text(source.text)
        for match in LABEL_RE.finditer(clean):
            label = match.group(1)
            line = line_for_offset(clean, match.start())
            if label in labels:
                first_path, first_line = labels[label]
                add_finding(
                    findings,
                    "warning",
                    "duplicate_label",
                    f"Duplicate label '{label}', first defined at {display_path(first_path)}:{first_line}",
                    source.path,
                    line,
                )
            else:
                labels[label] = (source.path, line)
        for match in REF_RE.finditer(clean):
            for label in split_csv_values(match.group(1)):
                refs.append((label, source.path, line_for_offset(clean, match.start())))
        for match in CITE_RE.finditer(clean):
            for key in split_csv_values(match.group(1)):
                cites.append((key, source.path, line_for_offset(clean, match.start())))
        for match in BIBITEM_RE.finditer(clean):
            bibitems.add(match.group(1))
        for match in INCLUDEGRAPHICS_RE.finditer(clean):
            raw = match.group(1).strip()
            if not find_graphic(source.path.parent, graphics_paths, raw):
                add_finding(
                    findings,
                    "warning",
                    "missing_figure",
                    f"Figure file was not found: {raw}",
                    source.path,
                    line_for_offset(clean, match.start()),
                )
        for match in FIGPLOT_RE.finditer(clean):
            raw, _ = extract_figplot_file(clean, match.end())
            if raw and not find_graphic(source.path.parent, graphics_paths, raw):
                severity = "warning" if strict_placeholders else "info"
                code = "missing_figplot_asset" if strict_placeholders else "placeholder_figplot_asset"
                add_finding(
                    findings,
                    severity,
                    code,
                    f"figplot asset was not found and will render as a placeholder: {raw}",
                    source.path,
                    line_for_offset(clean, match.start()),
                )

    for label, path, line in refs:
        if label not in labels:
            add_finding(findings, "warning", "undefined_ref", f"Reference target was not found: {label}", path, line)
    for key, path, line in cites:
        if key not in bibitems:
            add_finding(findings, "warning", "undefined_cite", f"Citation key was not found: {key}", path, line)


def summarize(findings: list[dict[str, object]]) -> dict[str, int]:
    return {
        "critical": sum(1 for f in findings if f["severity"] == "critical"),
        "warning": sum(1 for f in findings if f["severity"] == "warning"),
        "info": sum(1 for f in findings if f["severity"] == "info"),
    }


def main() -> int:
    args = parse_args()
    target = TARGETS[args.target]
    template_dir = REPO_ROOT / target["dir"]
    main_path = template_dir / target["main"]
    findings: list[dict[str, object]] = []

    if not main_path.exists():
        add_finding(findings, "critical", "missing_main", "Main TeX file was not found", main_path)
    else:
        sources = collect_sources(main_path, findings)
        check_sources(sources, template_dir, findings, strict_placeholders=args.strict_placeholders)

    summary = summarize(findings)
    result = {
        "tool": "check_tex_links",
        "target": args.target,
        "status": "critical" if summary["critical"] else "warning" if summary["warning"] else "ok",
        "summary": summary,
        "findings": findings,
    }
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"check_tex_links {args.target}: {result['status']}")
        for finding in findings:
            location = f" ({finding['path']}:{finding['line']})" if finding["path"] else ""
            print(f"[{finding['severity']}] {finding['code']}: {finding['message']}{location}")
    return 1 if summary["critical"] else 0


if __name__ == "__main__":
    sys.exit(main())
