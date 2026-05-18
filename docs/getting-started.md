# 快速上手 (Getting Started)

> EN: Install TeX Live/MiKTeX with `xelatex`, pick a template under `templates/`, run `python scripts/build.py --target <name>`. See `docs/faq.md` for troubleshooting.

# 中文说明

## 环境准备

1. 安装 TeX Live 2024+ 或 MiKTeX
2. 确保 `xelatex` 在 PATH 中
3. 安装中文字体：SimSun (宋体)、SimHei (黑体)、FangSong (仿宋)、Microsoft YaHei
4. Python 3.10+ (仅构建脚本需要)

验证安装：
```bash
xelatex --version
python --version
```

## 三步开始

### 1. 选择模板

| 如果你的比赛是... | 使用模板 |
|------------------|---------|
| 全国大学生数学建模竞赛 (国赛/高教杯) | `templates/cumcm/` |
| 美国大学生数学建模竞赛 (MCM/ICM) | `templates/mcm/` |
| 五一数学建模竞赛 (五一杯) | `templates/wuyi/` |

### 2. 复制模板到工作目录

```bash
cp -r templates/cumcm/ my_paper/
cd my_paper/
```

### 3. 填写内容 + 编译

```bash
# 在 main_cumcm.tex 中修改论文标题
# 在 sections/ 各文件中填写你的内容

# 编译
python ../scripts/build.py --target cumcm
# 或在模板目录内直接:
cd .. && python scripts/build.py --target cumcm
```

PDF 生成在 `templates/cumcm/out/main_cumcm.pdf`。

## 核心文件说明

| 文件 | 作用 |
|------|------|
| `main_*.tex` | 主入口，控制整体结构 |
| `sections/cover.tex` | 承诺书 (国赛/五一杯) |
| `sections/summary_sheet.tex` | Summary Sheet (美赛) |
| `sections/problem.tex` | 问题重述 |
| `sections/analysis.tex` | 问题分析 |
| `sections/assumptions.tex` | 模型假设 |
| `sections/notation.tex` | 符号说明 |
| `sections/model.tex` | 模型建立与求解 |
| `sections/solution.tex` | 结果与分析 |
| `sections/validation.tex` | 模型检验 |
| `sections/evaluation.tex` | 模型评价与改进 |
| `sections/conclusion.tex` | 结论 |
| `sections/references.tex` | 参考文献 |
| `sections/appendix.tex` | 附录 |

## 常见问题

**Q: 编译报错 "font not found"**
A: 安装缺失的中文字体，或修改 `main_*.tex` 中的 `\setCJKmainfont`。

**Q: 参考文献显示 [?]**
A: 需要编译 2-3 次 xelatex，`build.py` 默认已处理。

**Q: 如何自定义页面边距？**
A: 修改 `core/paperkit-base.sty` 中的 `\geometry` 设置，或联系总监获取指导。
