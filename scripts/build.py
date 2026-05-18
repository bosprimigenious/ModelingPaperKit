#!/usr/bin/env python3
"""ModelingPaperKit — 多赛事 LaTeX 编译工具

用法:
    python scripts/build.py --target cumcm            # 编译国赛模板
    python scripts/build.py --target mcm              # 编译美赛模板
    python scripts/build.py --target wuyi             # 编译五一杯模板
    python scripts/build.py --target cumcm --clean    # 清理后编译
    python scripts/build.py --target all              # 编译全部模板
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TARGETS = {
    "cumcm": {
        "dir": "templates/cumcm",
        "main": "main_cumcm.tex",
        "description": "国赛/高教杯 (CUMCM)",
    },
    "mcm": {
        "dir": "templates/mcm",
        "main": "main_mcm.tex",
        "description": "美赛 (MCM/ICM)",
    },
    "wuyi": {
        "dir": "templates/wuyi",
        "main": "main_wuyi.tex",
        "description": "五一杯 (Wuyi Cup)",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ModelingPaperKit 多赛事模板编译工具"
    )
    parser.add_argument(
        "--target",
        default="cumcm",
        choices=["cumcm", "mcm", "wuyi", "all"],
        help="选择目标赛事模板 (default: cumcm)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="编译前清理辅助文件",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="PDF 输出目录 (默认: <template_dir>/out/)",
    )
    return parser.parse_args()


def clean_aux(tex_dir: Path) -> None:
    """清理 LaTeX 编译产生的辅助文件."""
    patterns = ["*.aux", "*.log", "*.out", "*.toc", "*.bbl", "*.blg",
                "*.synctex.gz", "*.fdb_latexmk", "*.fls", "*.xdv"]
    for pattern in patterns:
        for f in tex_dir.glob(pattern):
            f.unlink()
    out_dir = tex_dir / "out"
    if out_dir.exists():
        for pattern in patterns:
            for f in out_dir.glob(pattern):
                f.unlink()


def compile_target(target_key: str, clean: bool = False) -> bool:
    """编译单个赛事模板，返回是否成功."""
    target = TARGETS[target_key]
    tex_dir = REPO_ROOT / target["dir"]
    main_file = tex_dir / target["main"]

    if not main_file.exists():
        print(f"[ERROR] 未找到主文件: {main_file}")
        return False

    if clean:
        print(f"[CLEAN] 清理 {target_key} 辅助文件")
        clean_aux(tex_dir)

    out_dir = tex_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    xelatex_args = [
        "xelatex",
        "-interaction=nonstopmode",
        f"-output-directory={out_dir}",
        target["main"],
    ]

    print(f"[BUILD] 编译 {target['description']} ({target_key})")
    print(f"[BUILD] 工作目录: {tex_dir}")

    try:
        # xelatex × 3 (三次编译确保交叉引用正确)
        for i in range(3):
            print(f"[BUILD] xelatex ({i+1}/3)")
            subprocess.run(xelatex_args, check=True, cwd=str(tex_dir))

        # 将 PDF 复制到 out 目录
        pdf = out_dir / target["main"].replace(".tex", ".pdf")
        if pdf.exists():
            print(f"[OK] PDF 已生成: {pdf}")
            return True
        else:
            print(f"[WARN] PDF 未生成，请检查 LaTeX 日志")
            return False

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 编译失败 (exit code {e.returncode})")
        log_file = out_dir / target["main"].replace(".tex", ".log")
        if log_file.exists():
            print(f"[INFO] 查看日志: {log_file}")
        return False
    except FileNotFoundError:
        print("[ERROR] 未找到 xelatex，请确认已安装 TeX Live 或 MiKTeX")
        return False


def main() -> None:
    args = parse_args()

    if args.target == "all":
        results = {}
        for key in TARGETS:
            results[key] = compile_target(key, clean=args.clean)
        print("\n[SUMMARY]")
        for key, ok in results.items():
            status = "OK" if ok else "FAILED"
            print(f"  {key}: {status}")
        if not all(results.values()):
            sys.exit(1)
    else:
        ok = compile_target(args.target, clean=args.clean)
        if not ok:
            sys.exit(1)


if __name__ == "__main__":
    main()
