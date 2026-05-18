# 常见问题 (FAQ)

## 找不到 xelatex

安装 [TeX Live](https://tug.org/texlive/) 或 MiKTeX，并将 `bin` 目录加入 PATH。也可用：

```bash
python scripts/build.py --engine "C:/texlive/2024/bin/windows/xelatex.exe"
```

## 中文字体缺失

国赛/五一杯模板需要 SimSun、SimHei 等。Windows 一般已内置；Linux 请安装 `fonts-noto-cjk` 或改用 `fontset=fandol`（需改 `main_*.tex`）。

## 编译报错如何排查

```bash
python scripts/build.py --target cumcm
```

脚本会解析 `out/*.log` 中的 `! LaTeX Error` 行并打印摘要。

## `\figplot` 只显示占位框

将图片放入 `figures/` 或 `../02_figures/`，文件名与 `\figplot` 第 5 个参数一致。

## BibTeX 参考文献

```bash
python scripts/build.py --target cumcm --bibtex
```

并在正文中使用 `\cite{}`。
