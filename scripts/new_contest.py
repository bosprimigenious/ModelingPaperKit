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
CREF_ZH_LINE = r"\input{../../core/paperkit-cref-zh.tex}"
UTILS_USEPACKAGE = r"\usepackage{../../core/paperkit-utils}"
CHOICES_RE = re.compile(r'(choices=\[)([^\]]+)(\])', re.MULTILINE)


def list_builtin_templates() -> tuple[str, ...]:
    templates_dir = REPO_ROOT / "templates"
    return tuple(sorted(p.name for p in templates_dir.iterdir() if p.is_dir()))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="创建新赛事 LaTeX 模板",
        epilog=(
            f"内置模板: {', '.join(list_builtin_templates())}\n"
            "中文模板须在 paperkit-utils 之后 \\input{../../core/paperkit-cref-zh.tex}"
        ),
    )
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


def sync_build_choices(text: str, name: str) -> str:
    """向 build.py 的 --target choices 列表插入新赛事（插在 all 之前）。"""
    match = CHOICES_RE.search(text)
    if not match:
        raise RuntimeError("未在 build.py 中找到 choices=[...]")
    items = [x.strip().strip('"\'') for x in match.group(2).split(",") if x.strip()]
    if name in items:
        return text
    if "all" in items:
        items.insert(items.index("all"), name)
    else:
        items.append(name)
    new_inner = ", ".join(f'"{item}"' for item in items)
    return text[: match.start(2)] + new_inner + text[match.end(2) :]


def register_target(name: str, lang: str) -> None:
    text = BUILD_PY.read_text(encoding="utf-8")
    if f'"{name}":' in text:
        print(f"[SKIP] TARGETS 已包含 {name}")
    else:
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
        print(f"[OK] 已注册到 scripts/build.py TARGETS: {name}")
    text = sync_build_choices(text, name)
    BUILD_PY.write_text(text, encoding="utf-8")
    print(f"[OK] 已更新 scripts/build.py --target choices: {name}")


def patch_main_for_lang(main: Path, lang: str) -> None:
    """中文模板注入 paperkit-cref-zh；英文模板移除该行。"""
    text = main.read_text(encoding="utf-8")
    has_cref = CREF_ZH_LINE in text
    if lang == "zh":
        if not has_cref:
            if UTILS_USEPACKAGE not in text:
                raise RuntimeError(
                    f"未在 {main} 中找到 {UTILS_USEPACKAGE}，无法插入 paperkit-cref-zh.tex"
                )
            text = text.replace(
                UTILS_USEPACKAGE,
                f"{UTILS_USEPACKAGE}\n{CREF_ZH_LINE}",
                1,
            )
            print(f"[OK] 已注入 {CREF_ZH_LINE}")
        else:
            print(f"[SKIP] {main.name} 已包含 paperkit-cref-zh.tex")
    else:
        if has_cref:
            text = text.replace(f"{CREF_ZH_LINE}\n", "", 1)
            text = text.replace(CREF_ZH_LINE, "", 1)
            print(f"[OK] 已移除英文模板中的 paperkit-cref-zh.tex")
    main.write_text(text, encoding="utf-8")


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
    patch_main_for_lang(target_main, lang)
    print(f"[OK] 已创建模板: {dest}")
    return dest


def main() -> None:
    args = parse_args()
    name = validate_name(args.name)
    create_template(name, args.lang)
    register_target(name, args.lang)
    print(f"[NEXT] 编辑 templates/{name}/main_{name}.tex 并运行:")
    print(f"       python scripts/build.py --target {name}")
    if args.lang == "zh":
        print(f"       （已包含 {CREF_ZH_LINE}，勿删除）")


if __name__ == "__main__":
    main()
