#!/usr/bin/env python3
"""一键清除编译缓存与敏感数据"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

AUX_PATTERNS = [
    "*.aux", "*.log", "*.out", "*.toc", "*.bbl", "*.blg",
    "*.synctex.gz", "*.fdb_latexmk", "*.fls", "*.xdv",
    "*.nav", "*.snm", "*.vrb",
]

PYCACHE_PATTERNS = ["__pycache__", "*.pyc", "*.pyo"]


def iter_aux_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in AUX_PATTERNS:
        files.extend(root.rglob(pattern))
    return files


def iter_pycache(root: Path) -> list[Path]:
    items: list[Path] = []
    for pattern in PYCACHE_PATTERNS:
        items.extend(root.rglob(pattern))
    return items


def iter_out_dirs(root: Path) -> list[Path]:
    return [
        out_dir
        for out_dir in root.rglob("out")
        if out_dir.is_dir() and ".git" not in out_dir.parts
    ]


def delete_paths(paths: list[Path], dry_run: bool) -> int:
    count = 0
    for path in paths:
        if dry_run:
            print(f"[DRY-RUN] 将删除: {path.relative_to(REPO_ROOT)}")
            count += 1
            continue
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
        count += 1
    return count


def confirm(prompt: str) -> bool:
    try:
        answer = input(f"{prompt} [y/N]: ").strip().lower()
    except EOFError:
        return False
    return answer in {"y", "yes"}


def main() -> None:
    parser = argparse.ArgumentParser(description="清理编译缓存与输出")
    parser.add_argument(
        "--all",
        action="store_true",
        default=True,
        help="清理所有 (默认)",
    )
    parser.add_argument("--aux-only", action="store_true", help="仅清理 LaTeX 辅助文件")
    parser.add_argument("--output-only", action="store_true", help="仅清理输出目录")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅列出将删除的文件，不实际删除",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="删除前交互式确认",
    )
    args = parser.parse_args()

    if args.aux_only:
        targets = iter_aux_files(REPO_ROOT)
        label = "LaTeX 辅助文件"
    elif args.output_only:
        targets = iter_out_dirs(REPO_ROOT)
        label = "输出目录"
    else:
        targets = (
            iter_aux_files(REPO_ROOT)
            + iter_pycache(REPO_ROOT)
            + iter_out_dirs(REPO_ROOT)
        )
        label = "缓存与输出"

    if not targets:
        print("[CLEAN] 无需清理")
        return

    if args.interactive and not args.dry_run:
        print(f"[CLEAN] 将删除 {len(targets)} 个{label}项")
        if not confirm("确认继续"):
            print("[CLEAN] 已取消")
            return

    n = delete_paths(targets, dry_run=args.dry_run)
    mode = "将删除" if args.dry_run else "已删除"
    print(f"[CLEAN] {mode} {n} 个{label}项")


if __name__ == "__main__":
    main()
