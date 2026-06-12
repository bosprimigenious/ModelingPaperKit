# LaTeX Patterns

Use these repository conventions instead of inventing new local styles.

## Core Packages

Templates load:

```latex
\usepackage{../../core/paperkit-base}
\usepackage{../../core/paperkit-math}
\usepackage{../../core/paperkit-utils}
```

MCM uses English options:

```latex
\usepackage[en]{../../core/paperkit-math}
\usepackage[en]{../../core/paperkit-utils}
```

Chinese templates also input:

```latex
\input{../../core/paperkit-cref-zh.tex}
```

## Figures

Prefer `\figplot` when a figure may be missing or needs a consistent note:

```latex
\figplot{题注}{0.32\textheight}{fig:workflow}{占位说明}{fig_workflow.pdf}{制图说明}
```

The fifth argument is the file name. The macro searches common figure paths such as `figures/` and `../02_figures/`.

## References

Use labels and `\cref`:

```latex
\label{fig:workflow}
如 \cref{fig:workflow} 所示，...
```

Use `\upcite{key}` for superscript-style citation where appropriate.

## Math

Use local shortcuts:

```latex
\vb{x}
\mat{A}
\trans
\R
\argmin
\argmax
```

Do not redefine built-in LaTeX commands such as `\vec`.

## Tables

Use booktabs-style macros:

```latex
\begin{table}[H]
  \centering
  \caption{结果对比}
  \begin{tabular}{lcc}
    \topline
    方法 & 指标一 & 指标二 \\
    \midline
    Baseline & 0.82 & 0.71 \\
    Ours & 0.89 & 0.76 \\
    \bottomline
  \end{tabular}
  \label{tab:results}
\end{table}
```

## Algorithms

Use `algorithm` and `algpseudocode` from `paperkit-utils`.

## Keywords

Use:

```latex
\keywords{关键词一；关键词二；关键词三}
```

## Anonymization Helpers

Use:

```latex
\email{...}
\phone{...}
```

These are intentionally anonymized in output.

