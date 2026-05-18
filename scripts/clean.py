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


def clean_aux_files(root: Path) -> int:
    """递归删除 LaTeX 辅助文件，返回删除数."""
    count = 0
    for pattern in AUX_PATTERNS:
        for f in root.rglob(pattern):
            f.unlink()
            count += 1
    return count


def clean_pycache(root: Path) -> int:
    """递归删除 Python 缓存，返回删除数."""
    count = 0
    for pattern in PYCACHE_PATTERNS:
        for item in root.rglob(pattern):
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
            count += 1
    return count


def clean_out_dirs(root: Path) -> int:
    """删除所有 out/ 输出目录，返回删除数."""
    count = 0
    for out_dir in root.rglob("out"):
        if out_dir.is_dir() and ".git" not in out_dir.parts:
            shutil.rmtree(out_dir)
            count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="清理编译缓存与输出")
    parser.add_argument("--all", action="store_true", default=True,
                       help="清理所有 (默认)")
    parser.add_argument("--aux-only", action="store_true",
                       help="仅清理 LaTeX 辅助文件")
    parser.add_argument("--output-only", action="store_true",
                       help="仅清理输出目录")
    args = parser.parse_args()

    if args.aux_only:
        n = clean_aux_files(REPO_ROOT)
        print(f"[CLEAN] 删除 {n} 个 LaTeX 辅助文件")
    elif args.output_only:
        n = clean_out_dirs(REPO_ROOT)
        print(f"[CLEAN] 删除 {n} 个输出目录")
    else:
        n1 = clean_aux_files(REPO_ROOT)
        n2 = clean_pycache(REPO_ROOT)
        n3 = clean_out_dirs(REPO_ROOT)
        print(f"[CLEAN] 删除 {n1} 个辅助文件, {n2} 个缓存, {n3} 个输出目录")


if __name__ == "__main__":
    main()
