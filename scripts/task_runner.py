#!/usr/bin/env python3
"""CURSOR_TASKS.md 任务清单辅助工具（供本机轮询 + Cursor Agent 接力）。

默认读取仓库根目录的 CURSOR_TASKS.md（已纳入版本库，与 clone 同进退）。
本地副本可用 --file 指定。

用法:
    python scripts/task_runner.py next          # 输出下一项未完成任务
    python scripts/task_runner.py list          # 列出所有未完成子项
    python scripts/task_runner.py prompt        # 生成给 Cursor 的标准提示词
    python scripts/task_runner.py mark --line 42   # 将第 42 行勾选为 [x]
    python scripts/task_runner.py watch         # 监视文件，出现 [ ] 时提醒
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TASKS = REPO_ROOT / "CURSOR_TASKS.md"

CHECKBOX_RE = re.compile(r"^(\s*-\s+)\[([ xX])\](\s+.*)$")
TASK_HEAD_RE = re.compile(r"^###\s+Task\s+(\d+\.\d+)\s+[—\-]\s+(.*)$")
PHASE_HEAD_RE = re.compile(r"^##\s+Phase\s+(\d+):\s+(.*)$")


@dataclass
class TaskItem:
    line_no: int
    phase: str
    task_id: str
    task_title: str
    text: str
    done: bool


def load_lines(path: Path) -> list[str]:
    if not path.is_file():
        print(
            f"[ERROR] 任务文件不存在: {path}\n"
            f"  请确认已 clone 仓库且包含 CURSOR_TASKS.md，或使用 --file 指定路径。",
            file=sys.stderr,
        )
        sys.exit(1)
    return path.read_text(encoding="utf-8").splitlines()


def parse_items(lines: list[str]) -> list[TaskItem]:
    phase = ""
    task_id = ""
    task_title = ""
    items: list[TaskItem] = []

    for i, raw in enumerate(lines, start=1):
        phase_m = PHASE_HEAD_RE.match(raw)
        if phase_m:
            phase = f"Phase {phase_m.group(1)}: {phase_m.group(2).strip()}"
            continue

        task_m = TASK_HEAD_RE.match(raw)
        if task_m:
            task_id = task_m.group(1)
            task_title = task_m.group(2).strip()
            continue

        cb_m = CHECKBOX_RE.match(raw)
        if cb_m and task_id:
            items.append(
                TaskItem(
                    line_no=i,
                    phase=phase,
                    task_id=task_id,
                    task_title=task_title,
                    text=cb_m.group(3).strip(),
                    done=cb_m.group(2).lower() == "x",
                )
            )
    return items


def pending(items: list[TaskItem]) -> list[TaskItem]:
    return [x for x in items if not x.done]


def format_item(item: TaskItem) -> str:
    return (
        f"L{item.line_no} | {item.phase} | Task {item.task_id} {item.task_title}\n"
        f"  - [ ] {item.text}"
    )


def cmd_next(path: Path) -> int:
    items = parse_items(load_lines(path))
    todo = pending(items)
    if not todo:
        print("[task_runner] 全部子项已完成，无待办。")
        return 0
    print(format_item(todo[0]))
    print(f"\n（剩余 {len(todo)} 项未勾选）")
    return 0


def cmd_list(path: Path) -> int:
    todo = pending(parse_items(load_lines(path)))
    if not todo:
        print("[task_runner] 全部子项已完成。")
        return 0
    for item in todo:
        print(format_item(item))
        print()
    print(f"共 {len(todo)} 项未完成。")
    return 0


def cmd_prompt(path: Path) -> int:
    items = parse_items(load_lines(path))
    todo = pending(items)
    if not todo:
        print(
            "CURSOR_TASKS.md 中已无 `- [ ]` 子项。"
            "若总监新增 Phase，保存文件后重新运行本命令。"
        )
        return 0
    item = todo[0]
    rel = path.relative_to(REPO_ROOT) if path.is_relative_to(REPO_ROOT) else path
    print(
        f"""请继续 ModelingPaperKit 开发任务。

仓库: {REPO_ROOT}
任务清单: {rel}

下一项待办（请先完成此项，再勾选 `- [x]` 并按规定 commit）:
- {item.phase}
- Task {item.task_id}: {item.task_title}
- {item.text}

约束:
- 遵守 .cursorrules：core/ 与 templates/ 分 commit，单次 ≤5 文件
- 修改 core/*.sty 后运行: python scripts/verify_build.py
- 禁止 \\renewcommand 覆盖 LaTeX 内置命令
- 不确定处用 % TODO(director): 标记
"""
    )
    return 0


def cmd_mark(path: Path, line_no: int) -> int:
    lines = load_lines(path)
    if line_no < 1 or line_no > len(lines):
        print(f"[ERROR] 行号越界: {line_no}", file=sys.stderr)
        return 1
    raw = lines[line_no - 1]
    cb_m = CHECKBOX_RE.match(raw)
    if not cb_m:
        print(f"[ERROR] 第 {line_no} 行不是 checkbox 项: {raw!r}", file=sys.stderr)
        return 1
    if cb_m.group(2).lower() == "x":
        print(f"[task_runner] 第 {line_no} 行已是 [x]，跳过。")
        return 0
    lines[line_no - 1] = f"{cb_m.group(1)}[x]{cb_m.group(3)}"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[task_runner] 已勾选第 {line_no} 行。")
    return 0


def cmd_watch(path: Path, interval: float) -> int:
    print(f"[task_runner] 监视 {path}（每 {interval}s），Ctrl+C 退出。")
    last_count: int | None = None
    try:
        while True:
            todo = pending(parse_items(load_lines(path)))
            count = len(todo)
            if last_count is None:
                last_count = count
                if count:
                    print(f"[watch] 当前 {count} 项未完成，下一项:\n{format_item(todo[0])}")
                else:
                    print("[watch] 当前无待办。")
            elif count != last_count:
                last_count = count
                if count:
                    print(f"\n[watch] 检测到 {count} 项待办，下一项:\n{format_item(todo[0])}")
                else:
                    print("\n[watch] 全部子项已勾选完成。")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[watch] 已停止。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="CURSOR_TASKS.md 任务清单辅助")
    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_TASKS,
        help=f"任务文件路径 (default: {DEFAULT_TASKS.name})",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("next", help="显示下一项未勾选子任务")
    sub.add_parser("list", help="列出所有未勾选子任务")
    sub.add_parser("prompt", help="输出给 Cursor Agent 的标准提示词")

    mark_p = sub.add_parser("mark", help="将指定行勾选为 [x]")
    mark_p.add_argument("--line", type=int, required=True, help="checkbox 所在行号")

    watch_p = sub.add_parser("watch", help="轮询任务文件，待办变化时打印提醒")
    watch_p.add_argument(
        "--interval",
        type=float,
        default=30.0,
        help="轮询间隔秒数 (default: 30)",
    )

    args = parser.parse_args()
    path: Path = args.file.resolve()

    if args.command == "next":
        return cmd_next(path)
    if args.command == "list":
        return cmd_list(path)
    if args.command == "prompt":
        return cmd_prompt(path)
    if args.command == "mark":
        return cmd_mark(path, args.line)
    if args.command == "watch":
        return cmd_watch(path, args.interval)
    return 1


if __name__ == "__main__":
    sys.exit(main())
