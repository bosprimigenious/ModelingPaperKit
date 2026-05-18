#!/usr/bin/env python3
"""一键创建新赛事模板脚手架.

用法:
    python scripts/new_contest.py --name apmcm --lang zh
    python scripts/new_contest.py --name icm --lang en
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_PY = REPO_ROOT / "scripts" / "build.py"
TEMPLATE_ZH = REPO_ROOT / "templates" / "cumcm"
TEMPLATE_EN = REPO_ROOT / "templates" / "mcm"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="创建新赛事 LaTeX 模板")
    parser.add_argument("--name", required=True, help="赛事标识 (小写英文，如 apmcm)")
    parser.add_argument(
        "--lang",
        choices=["zh", "en"],
        default="zh",
        help="模板语言 (default: zh)",
    )
    return parser.parse_args()


def validate_name(name: str) -> str:
    if not re.fullmatch(r"[a-z][a-z0-9_]*", name):
        raise ValueError("name 须为小写字母开头，仅含 a-z、0-9、下划线")
    return name


def register_target(name: str, lang: str) -> None:
    text = BUILD_PY.read_text(encoding="utf-8")
    if f'"{name}":' in text:
        print(f"[SKIP] TARGETS 已包含 {name}")
        return
    entry = (
        f'    "{name}": {{\n'
        f'        "dir": "templates/{name}",\n'
        f'        "main": "main_{name}.tex",\n'
        f'        "description": "{name.upper()} ({lang})",\n'
        f"    }},\n"
    )
    marker = "TARGETS = {"
    if marker not in text:
        raise RuntimeError("未在 build.py 中找到 TARGETS 字典")
    text = text.replace(marker, marker + "\n" + entry, 1)
    text = text.replace(
        'choices=["cumcm", "mcm", "wuyi", "all"]',
        f'choices=["cumcm", "mcm", "wuyi", "{name}", "all"]',
        1,
    )
    BUILD_PY.write_text(text, encoding="utf-8")
    print(f"[OK] 已注册到 scripts/build.py: {name}")


def create_template(name: str, lang: str) -> Path:
    src = TEMPLATE_ZH if lang == "zh" else TEMPLATE_EN
    dest = REPO_ROOT / "templates" / name
    if dest.exists():
        raise FileExistsError(f"目录已存在: {dest}")
    shutil.copytree(src, dest)
    mains = list(dest.glob("main_*.tex"))
    if not mains:
        raise FileNotFoundError(f"未在 {dest} 找到 main_*.tex")
    target_main = dest / f"main_{name}.tex"
    mains[0].rename(target_main)
    for extra in dest.glob("main_*.tex"):
        if extra != target_main:
            extra.unlink()
    print(f"[OK] 已创建模板: {dest}")
    return dest


def main() -> None:
    args = parse_args()
    name = validate_name(args.name)
    create_template(name, args.lang)
    register_target(name, args.lang)
    print(f"[NEXT] 编辑 templates/{name}/main_{name}.tex 并运行:")
    print(f"       python scripts/build.py --target {name}")


if __name__ == "__main__":
    main()
