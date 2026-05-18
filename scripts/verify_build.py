#!/usr/bin/env python3
"""Phase 6.1 编译验证：三套模板全量编译并检查 PDF / 日志."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TARGETS = ("cumcm", "mcm", "wuyi", "beijing")
MAIN = {
    "cumcm": "main_cumcm",
    "mcm": "main_mcm",
    "wuyi": "main_wuyi",
    "beijing": "main_beijing",
}


def run_build() -> int:
    cmd = [sys.executable, str(REPO_ROOT / "scripts" / "build.py"), "--target", "all", "--clean"]
    print("[VERIFY] " + " ".join(cmd))
    return subprocess.call(cmd, cwd=str(REPO_ROOT))


def check_target(name: str) -> list[str]:
    issues: list[str] = []
    stem = MAIN[name]
    out = REPO_ROOT / "templates" / name / "out"
    pdf = out / f"{stem}.pdf"
    log = out / f"{stem}.log"

    if not pdf.is_file() or pdf.stat().st_size < 1024:
        issues.append(f"{name}: PDF 缺失或过小 ({pdf})")
    if not log.is_file():
        issues.append(f"{name}: 日志缺失 ({log})")
        return issues

    text = log.read_text(encoding="utf-8", errors="replace")
    if re.search(r"^! LaTeX Error:", text, re.MULTILINE):
        issues.append(f"{name}: 存在 LaTeX Error（见 {log}）")
    overfull = len(re.findall(r"Overfull \\hbox", text))
    underfull = len(re.findall(r"Underfull \\hbox", text))
    if overfull:
        issues.append(f"{name}: Overfull \\hbox × {overfull}")
    if underfull:
        issues.append(f"{name}: Underfull \\hbox × {underfull}")
    if "Rerun to get cross-references right" in text:
        # 三次编译后仍出现则提示
        if "Label(s) may have changed" in text:
            issues.append(f"{name}: 交叉引用可能未稳定（见 {log}）")

    print(f"[VERIFY] {name}: PDF OK ({pdf.stat().st_size // 1024} KB), "
          f"errors=0, overfull={overfull}, underfull={underfull}")
    return issues


def main() -> None:
    code = run_build()
    if code != 0:
        print("[VERIFY] build.py 失败")
        sys.exit(code)

    all_issues: list[str] = []
    for name in TARGETS:
        all_issues.extend(check_target(name))

    if all_issues:
        print("\n[VERIFY] FAILED")
        for item in all_issues:
            print(f"  - {item}")
        sys.exit(1)

    print("\n[VERIFY] PASSED — 三套模板编译通过")
    sys.exit(0)


if __name__ == "__main__":
    main()
