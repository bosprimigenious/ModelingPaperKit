#!/usr/bin/env python3
"""从 examples/dummy_data 生成 walkthrough 插图（SVG + PDF）。"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "dummy_data"
FIG = ROOT / "figures"


def save_both(name: str) -> None:
    base = FIG / name
    plt.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    plt.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    plt.close()


def plot_workflow() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 2.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")
    labels = ["数据预处理", "特征构建", "模型训练", "结果验证"]
    xs = [0.6, 3.1, 5.6, 8.1]
    for x, text in zip(xs, labels):
        box = FancyBboxPatch(
            (x, 1.0),
            1.8,
            1.0,
            boxstyle="round,pad=0.05,rounding_size=0.08",
            linewidth=1.2,
            edgecolor="#2563eb",
            facecolor="#eff6ff",
        )
        ax.add_patch(box)
        ax.text(x + 0.9, 1.5, text, ha="center", va="center", fontsize=11)
    for x0, x1 in zip(xs[:-1], xs[1:]):
        ax.add_patch(
            FancyArrowPatch(
                (x0 + 1.85, 1.5),
                (x1 - 0.05, 1.5),
                arrowstyle="-|>",
                mutation_scale=12,
                linewidth=1.2,
                color="#64748b",
            )
        )
    ax.set_title("建模流程（示例）", fontsize=12, pad=8)
    save_both("fig_workflow")


def plot_timeseries() -> None:
    values: list[float] = []
    trends: list[float] = []
    with (DATA / "time_series.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            values.append(float(row["value"]))
            trends.append(float(row["trend"]))
    fig, ax = plt.subplots(figsize=(6.8, 3.2))
    ax.plot(range(len(values)), values, color="#2563eb", linewidth=1.8, label="观测值")
    ax.plot(range(len(trends)), trends, color="#94a3b8", linestyle="--", label="趋势项")
    ax.set_xlabel("周次序号")
    ax.set_ylabel("指标值")
    ax.set_title("合成时间序列（time_series.csv）")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(True, alpha=0.25)
    save_both("fig_timeseries")


def plot_classification() -> None:
    xs0, ys0, xs1, ys1 = [], [], [], []
    with (DATA / "classification.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            x, y, label = float(row["x1"]), float(row["x2"]), int(row["label"])
            (xs0 if label == 0 else xs1).append(x)
            (ys0 if label == 0 else ys1).append(y)
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    ax.scatter(xs0, ys0, s=18, alpha=0.65, label="类别 0", c="#3b82f6")
    ax.scatter(xs1, ys1, s=18, alpha=0.65, label="类别 1", c="#f97316")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_title("分类数据散点（classification.csv）")
    ax.legend()
    ax.grid(True, alpha=0.2)
    save_both("fig_classification")


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    plot_workflow()
    plot_timeseries()
    plot_classification()
    print(f"[OK] 已生成插图至 {FIG}")


if __name__ == "__main__":
    main()
