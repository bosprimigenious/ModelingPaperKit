#!/usr/bin/env python3
"""ModelingPaperKit — 多赛事 LaTeX 编译工具

用法:
    python scripts/build.py --target cumcm
    python scripts/build.py --target all --clean
    python scripts/build.py --target cumcm --bibtex
    python scripts/build.py --target cumcm --engine "C:/texlive/bin/xelatex.exe"
    python scripts/build.py --target cumcm --watch
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import time
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
    "beijing": {
        "dir": "templates/beijing",
        "main": "main_beijing.tex",
        "description": "北京赛 (Beijing)",
    },
}

ERROR_LINE_RE = re.compile(r"^!\s*(.+)$", re.MULTILINE)
LATEX_ERROR_RE = re.compile(r"^! LaTeX Error:\s*(.+)$", re.MULTILINE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ModelingPaperKit 多赛事模板编译工具"
    )
    parser.add_argument(
        "--target",
        default="cumcm",
        choices=["cumcm", "mcm", "wuyi", "beijing", "all"],
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
    parser.add_argument(
        "--bibtex",
        action="store_true",
        help="启用 BibTeX 编译链 (xelatex -> bibtex -> xelatex x2)",
    )
    parser.add_argument(
        "--engine",
        default="xelatex",
        help="TeX 引擎可执行文件路径或命令名 (default: xelatex)",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="监视 .tex 文件变化并自动重编译",
    )
    parser.add_argument(
        "--watch-interval",
        type=float,
        default=2.0,
        help="--watch 轮询间隔秒数 (default: 2.0)",
    )
    return parser.parse_args()


def clean_aux(tex_dir: Path) -> None:
    """清理 LaTeX 编译产生的辅助文件."""
    patterns = [
        "*.aux", "*.log", "*.out", "*.toc", "*.bbl", "*.blg",
        "*.synctex.gz", "*.fdb_latexmk", "*.fls", "*.xdv",
    ]
    for pattern in patterns:
        for f in tex_dir.glob(pattern):
            f.unlink()
    out_dir = tex_dir / "out"
    if out_dir.exists():
        for pattern in patterns:
            for f in out_dir.glob(pattern):
                f.unlink()


def parse_log_errors(log_path: Path, max_lines: int = 12) -> list[str]:
    """从 .log 提取 LaTeX Error 行，返回友好提示."""
    if not log_path.exists():
        return []
    text = log_path.read_text(encoding="utf-8", errors="replace")
    errors = LATEX_ERROR_RE.findall(text)
    if not errors:
        errors = ERROR_LINE_RE.findall(text)
    return errors[:max_lines]


def print_log_hints(log_path: Path) -> None:
    errors = parse_log_errors(log_path)
    if errors:
        print("[HINT] 日志中的错误摘要:")
        for msg in errors:
            print(f"  - {msg.strip()}")
    else:
        print("[HINT] 未在日志中匹配到标准 Error 行，请打开日志全文排查。")


def run_engine(
    engine: str,
    args: list[str],
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [engine, *args],
        cwd=str(cwd),
        check=False,
        capture_output=False,
        text=True,
    )


def compile_target(
    target_key: str,
    *,
    clean: bool = False,
    use_bibtex: bool = False,
    engine: str = "xelatex",
    output_dir: str | None = None,
) -> bool:
    """编译单个赛事模板，返回是否成功."""
    target = TARGETS[target_key]
    tex_dir = REPO_ROOT / target["dir"]
    main_file = tex_dir / target["main"]
    main_stem = target["main"].replace(".tex", "")

    if not main_file.exists():
        print(f"[ERROR] 未找到主文件: {main_file}")
        return False

    if clean:
        print(f"[CLEAN] 清理 {target_key} 辅助文件")
        clean_aux(tex_dir)

    out_dir = Path(output_dir) if output_dir else tex_dir / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    if Path(engine).is_file():
        engine_cmd = str(Path(engine).resolve())
    elif shutil.which(engine):
        engine_cmd = engine
    else:
        print(f"[ERROR] 未找到 TeX 引擎: {engine}")
        return False

    xelatex_args = [
        "-interaction=nonstopmode",
        f"-output-directory={out_dir}",
        target["main"],
    ]

    print(f"[BUILD] 编译 {target['description']} ({target_key})")
    print(f"[BUILD] 工作目录: {tex_dir}")
    print(f"[BUILD] 引擎: {engine}")

    log_file = out_dir / f"{main_stem}.log"

    try:
        total_passes = 3
        for i in range(total_passes):
            print(f"[BUILD] xelatex ({i + 1}/{total_passes})")
            proc = run_engine(engine_cmd, xelatex_args, tex_dir)
            if proc.returncode != 0 and i == 0:
                print(f"[ERROR] xelatex 失败 (exit code {proc.returncode})")
                print_log_hints(log_file)
                return False
            if use_bibtex and i == 0:
                aux = out_dir / f"{main_stem}.aux"
                if aux.exists():
                    print("[BUILD] bibtex")
                    bib_name = aux.relative_to(tex_dir).with_suffix("").as_posix()
                    bib = run_engine("bibtex", [bib_name], tex_dir)
                    if bib.returncode != 0:
                        print(f"[WARN] bibtex 返回 {bib.returncode}，继续 xelatex")
                else:
                    print("[WARN] 未找到 .aux，跳过 bibtex")
            if i > 0 and proc.returncode != 0:
                print(f"[ERROR] xelatex 失败 (exit code {proc.returncode})")
                print_log_hints(log_file)
                return False

        pdf = out_dir / f"{main_stem}.pdf"
        if pdf.exists():
            print(f"[OK] PDF 已生成: {pdf}")
            return True
        print("[WARN] PDF 未生成，请检查 LaTeX 日志")
        print_log_hints(log_file)
        return False

    except FileNotFoundError:
        print(f"[ERROR] 未找到引擎可执行文件: {engine}")
        return False


def collect_tex_mtimes(tex_dir: Path) -> dict[Path, float]:
    mtimes: dict[Path, float] = {}
    for path in tex_dir.rglob("*.tex"):
        if "out" not in path.parts:
            mtimes[path] = path.stat().st_mtime
    return mtimes


def watch_and_build(
    target_key: str,
    compile_kwargs: dict,
    interval: float,
) -> None:
    tex_dir = REPO_ROOT / TARGETS[target_key]["dir"]
    print(f"[WATCH] 监视 {tex_dir} (*.tex)，Ctrl+C 退出")
    snapshot = collect_tex_mtimes(tex_dir)
    compile_target(target_key, **compile_kwargs)
    while True:
        time.sleep(interval)
        current = collect_tex_mtimes(tex_dir)
        if current != snapshot:
            changed = [p for p in current if snapshot.get(p) != current.get(p)]
            print(f"[WATCH] 检测到变更: {', '.join(p.name for p in changed[:5])}")
            snapshot = current
            compile_target(target_key, **compile_kwargs)


def main() -> None:
    args = parse_args()
    compile_kwargs = {
        "clean": args.clean,
        "use_bibtex": args.bibtex,
        "engine": args.engine,
        "output_dir": args.output_dir,
    }

    if args.watch:
        keys = list(TARGETS) if args.target == "all" else [args.target]
        if len(keys) > 1:
            print("[WARN] --watch 暂不支持 all，将仅监视 cumcm")
            keys = ["cumcm"]
        try:
            watch_and_build(keys[0], compile_kwargs, args.watch_interval)
        except KeyboardInterrupt:
            print("\n[WATCH] 已停止")
        return

    if args.target == "all":
        results = {key: compile_target(key, **compile_kwargs) for key in TARGETS}
        print("\n[SUMMARY]")
        for key, ok in results.items():
            print(f"  {key}: {'OK' if ok else 'FAILED'}")
        if not all(results.values()):
            sys.exit(1)
    else:
        if not compile_target(args.target, **compile_kwargs):
            sys.exit(1)


if __name__ == "__main__":
    main()
