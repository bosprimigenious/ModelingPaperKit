# 国赛示例论文（简化 walkthrough）

本目录说明如何使用 ModelingPaperKit 完成一篇可编译的示例论文。

## 编译

在仓库根目录执行：

```bash
python scripts/generate_dummy_data.py
python scripts/build.py --target cumcm --clean
```

主模板位于 `templates/cumcm/`，已内置：

- `\figplot` 插图占位
- `listings` 代码清单（见 `sections/appendix.tex`）
- 合成数据说明见 `examples/dummy_data/README.md`

## 建模流程对应章节

| 步骤 | 章节文件 |
|------|----------|
| 问题重述 | `templates/cumcm/sections/problem.tex` |
| 模型建立 | `templates/cumcm/sections/model.tex` |
| 结果分析 | `templates/cumcm/sections/results.tex` |
| 附录代码 | `templates/cumcm/sections/appendix.tex` |
