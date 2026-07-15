# ModelingPaperKit

**数学建模论文排版工具包** — 核心引擎 + 多赛事插件（Core + Plugins）

> 一套 `core/`，四套赛事模板；公共排版进引擎，赛规差异进 `templates/`。

<!-- 待配置 GitHub Actions 后取消注释
![Build](https://github.com/<owner>/ModelingPaperKit/actions/workflows/verify.yml/badge.svg)
![License](https://img.shields.io/github/license/<owner>/ModelingPaperKit)
-->

## 项目简介

ModelingPaperKit 面向数学建模竞赛论文的 **XeLaTeX 排版工作流**：共享 `paperkit-*.sty` 引擎，按赛事提供独立 `templates/<赛事>/` 插件。复制模板目录、填写 `sections/`、一键编译即可出 PDF。

<p align="center">
  <img src="docs/assets/architecture.svg" alt="Core + Plugins 架构：core 引擎连接 cumcm、mcm、wuyi、beijing 四套模板" width="720" />
</p>

## 赛事覆盖

| 赛事 | 年份 | 目录 | `--target` | 语言 | 文档类 | 特殊页 |
|------|------|------|------------|------|--------|--------|
| 全国大学生数学建模竞赛 (CUMCM) | 2026 | `templates/cumcm/` | `cumcm` | 中文 | `ctexart` | 电子版默认无封面；纸质版可启用承诺书 + 编号专用页 |
| 美国大学生数学建模竞赛 (MCM/ICM) | 2026 | `templates/mcm/` | `mcm` | 英文 | `article` | Summary Sheet |
| 五一杯数学建模竞赛 | 2026 | `templates/wuyi/` | `wuyi` | 中文 | `ctexart` | 五一杯承诺书 + AI Declaration |
| 北京大学生数学建模与计算机应用竞赛 | 2026 | `templates/beijing/` | `beijing` | 中文 | `ctexart` | 承诺书 + AI Declaration |

> **国赛与高教杯**：CUMCM 最高奖为「高教社杯」，为同一赛事；`cumcm` 模板适用于本科/专科组别。  
> **电子版提交**：CUMCM 电子版论文默认从摘要页开始；纸质版可在 `main_cumcm.tex` 中启用 `\cumcmPaperSubmissiontrue` 生成承诺书和编号专用页。AI 工具使用信息按赛规在参考文献后声明或放入支撑材料，不作为论文正文的独立声明页。

## 快速开始

1. **克隆仓库**（需 Git、Python 3.10+、TeX Live / MiKTeX 且含 `xelatex`）
2. **选择赛事**：进入 `templates/<赛事>/`，编辑 `main_*.tex` 与各 `sections/*.tex`（标题、摘要、正文；勿提交真实姓名/学号/电话）
3. **编译**：在仓库根目录执行下方命令，PDF 输出至 `templates/<赛事>/out/`

```bash
git clone <repository-url>
cd ModelingPaperKit
python scripts/build.py --target cumcm
```

## 编译命令

| 命令 | 说明 |
|------|------|
| `python scripts/build.py --target cumcm` | 国赛/高教杯 (CUMCM) |
| `python scripts/build.py --target mcm` | 美赛 (MCM/ICM) |
| `python scripts/build.py --target wuyi` | 五一杯 |
| `python scripts/build.py --target beijing` | 北京赛 |
| `python scripts/build.py --target example` | 图文并茂示例论文（需先运行 `generate_figures.py`） |
| `python scripts/build.py --target all` | 编译全部模板与示例（5 个 PDF） |
| `python scripts/build.py --target cumcm --clean` | 编译前清理辅助文件 |
| `python scripts/build.py --target cumcm --bibtex` | 启用 BibTeX 链（xelatex → bibtex → xelatex ×2） |
| `python scripts/build.py --target cumcm --watch` | 监视 `.tex` 变更并自动重编译 |
| `python scripts/clean.py` | 清理各模板下的编译缓存 |
| `python scripts/verify_build.py` | 全量编译并检查 PDF / 日志（0 Error、Overfull 统计） |
| `python scripts/check_skills.py skills/cumcm-final-review` | 检查 Codex skill frontmatter、TODO 和基础结构 |
| `python scripts/check_submission.py --target cumcm` | 检查国赛电子版默认模式、构建产物和支撑材料基础风险 |

指定 TeX 引擎路径（可选）：

```bash
python scripts/build.py --target cumcm --engine "C:/texlive/2024/bin/windows/xelatex.exe"
```

## 脚手架：新建赛事模板

从中文或英文基准模板复制目录，并自动注册到 `build.py`：

```bash
python scripts/new_contest.py --name apmcm --lang zh
python scripts/new_contest.py --name icm --lang en
```

内置可参考模板：`cumcm`、`mcm`、`wuyi`、`beijing`（见 `scripts/new_contest.py` 中 `BUILTIN_TEMPLATES`）。

## 依赖

| 类型 | 要求 |
|------|------|
| TeX | TeX Live 2024+ 或 MiKTeX，**必须**支持 `xelatex` |
| 中文字体（中文模板） | SimSun（宋体）、SimHei（黑体）、FangSong（仿宋）；部分模板使用 Microsoft YaHei |
| 英文字体（MCM） | Times New Roman、Arial |
| Python | 3.10+（仅 `scripts/` 构建与工具脚本） |

## 项目结构

```
ModelingPaperKit/
├── core/                          # 共享排版引擎（禁止写入赛事专属内容）
│   ├── paperkit-base.sty          # 页面、边距、图表、列表、中文 caption
│   ├── paperkit-math.sty          # 数学符号、定理环境、矩阵快捷命令
│   └── paperkit-utils.sty         # 算法、代码块、hyperref/cleveref、\keywords 等
├── templates/
│   ├── cumcm/                     # 2025 国赛 — main_cumcm.tex + sections/
│   ├── mcm/                       # 2026 美赛 — main_mcm.tex + Summary Sheet
│   ├── wuyi/                      # 2026 五一杯 — main_wuyi.tex
│   └── beijing/                   # 2026 北京赛 — main_beijing.tex
├── scripts/
│   ├── build.py                   # 多赛事一键编译
│   ├── clean.py                   # 清理缓存
│   ├── verify_build.py            # 全量编译验证
│   ├── new_contest.py             # 新赛事脚手架
│   └── generate_dummy_data.py     # 合成示例数据
├── examples/
│   ├── cumcm_walkthrough/         # 图文并茂示例论文（main.tex + figures/）
│   └── dummy_data/                # 脱敏 CSV（非真实赛题数据）
├── docs/
│   ├── assets/
│   │   └── architecture.svg       # README 架构图
│   ├── getting-started.md
│   ├── template-guide.md
│   └── faq.md
├── README.md
```

## 架构说明（Core + Plugins）

- **`core/`**：三份 `.sty` 供所有模板 `\usepackage{../../core/...}`；不含学校名、队号、赛规封面文案。
- **`templates/<赛事>/`**：仅保留该赛差异（承诺书、编号页、Summary Sheet、AI 使用说明、章节骨架）。
- **禁止**在模板中重复实现已在 `core/` 中的逻辑；**禁止** `\renewcommand` 覆盖 LaTeX 内置命令（自定义命令请用新名，如 `\vb`）。
- 中文模板统一 `ctexart` + `xelatex`；MCM 使用 `article` + `[en]` 选项加载核心包。

各模板主文件均引用：

```latex
\usepackage{../../core/paperkit-base}
\usepackage{../../core/paperkit-math}      % MCM: \usepackage[en]{...}
\usepackage{../../core/paperkit-utils}   % MCM: \usepackage[en]{...}
```

## 文档

- [快速上手](docs/getting-started.md)
- [模板编写指南](docs/template-guide.md)
- [常见问题](docs/faq.md)
- [2026 国赛 GitHub 开源生态与 Skill 建设调研](docs/2026-cumcm-github-skill-research.md)
- [2026 国赛 Skill 索引](docs/2026-cumcm-skill-index.md)
- [ModelingPaperKit Skill](skills/modeling-paperkit/SKILL.md)

## 许可

MIT License
