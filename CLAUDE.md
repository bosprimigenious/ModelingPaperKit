# ModelingPaperKit — Claude 项目指南

## 项目定位
数学建模论文排版工具包。核心引擎 (`core/`) 与赛事模板 (`templates/`) 彻底分离。
架构原则：**Core + Plugins** — 公共逻辑入 core，赛事差异入 template。

## 目录约定
```
core/           # 共享排版引擎 (不可包含赛事特定内容)
templates/      # 赛事模板 (cumcm/mcm/wuyi)
scripts/        # 构建工具
examples/       # 示例与脱敏数据
docs/           # 文档
```

## 关键约束
- 编译引擎：必须用 `xelatex`（支持中文字体）
- 中文模板：`\documentclass{ctexart}` + `\usepackage{../../core/paperkit-base}`
- 英文模板：`\documentclass{article}` + `\usepackage{../../core/paperkit-base}`
- 严禁在模板中硬编码个人信息（姓名、学号、电话、邮箱、学校名）
- 严禁提交真实竞赛数据 — 只能用合成 dummy 数据
- 新功能优先考虑是否应进入 `core/`，而非直接写入模板

## 构建命令
```bash
python scripts/build.py --target cumcm    # 国赛
python scripts/build.py --target mcm      # 美赛
python scripts/build.py --target wuyi     # 五一杯
python scripts/build.py --target all      # 全部
python scripts/clean.py                   # 清理
```

## Cursor 协作模式
- 总监 (Bosprimigenious) 负责架构设计与代码审查
- Cursor 按 `CURSOR_TASKS.md` 逐项执行实现任务
- 每个 Task 完成后需 commit，格式：`feat:` / `fix:` / `refactor:` / `docs:`
- TODO 标记格式：`% TODO(director): <问题描述>`
