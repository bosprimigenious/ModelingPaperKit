# 国赛示例论文 Walkthrough

图文并茂的独立 LaTeX 示例，演示 ModelingPaperKit `core/` 宏包能力。

## 编译

在仓库根目录执行：

```bash
pip install matplotlib
python examples/cumcm_walkthrough/generate_figures.py
python scripts/build.py --target example --clean --bibtex
```

PDF 输出：`examples/cumcm_walkthrough/out/main.pdf`

全量验证（含四套模板 + 本示例）：

```bash
python scripts/verify_build.py
```

## 目录

| 路径 | 说明 |
|------|------|
| `main.tex` | 入口（`ctexart` + core 三件套） |
| `sections/` | 问题重述、模型、求解、算法 |
| `figures/` | SVG/PDF 插图（由脚本生成） |
| `references.bib` | 示例参考文献 |

## 演示特性

- `\figplot`、pgfplots 读 CSV、csvsimple 表格
- `\cref` / `\crefrange`、定理环境、算法伪代码
- `\keywords`、`\vb` / `\mat` / `\upcite`、`\todo`
