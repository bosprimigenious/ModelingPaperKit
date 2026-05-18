#!/usr/bin/env python3
"""生成 examples/dummy_data 下的合成 CSV."""

from __future__ import annotations

from pathlib import Path

import random

OUT = Path(__file__).resolve().parent.parent / "examples" / "dummy_data"
random.seed(42)


def write_time_series() -> None:
    rows = ["date,value,trend"]
    for i in range(1, 49):
        rows.append(f"2024-W{i:02d},{100 + i * 1.2 + random.gauss(0, 3):.2f},{i * 0.8:.2f}")
    (OUT / "time_series.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")


def write_classification() -> None:
    rows = ["x1,x2,label"]
    for i in range(120):
        label = i % 2
        x1 = random.gauss(2 if label else -2, 1)
        x2 = random.gauss(1 if label else -1, 1)
        rows.append(f"{x1:.3f},{x2:.3f},{label}")
    (OUT / "classification.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")


def write_regression() -> None:
    rows = ["feature,strength,noise,target"]
    for i in range(80):
        f = random.uniform(0, 10)
        s = 1.5 * f + random.gauss(0, 2)
        n = random.gauss(0, 1)
        rows.append(f"{f:.3f},{s:.3f},{n:.3f},{s + n:.3f}")
    (OUT / "regression.csv").write_text("\n".join(rows) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_time_series()
    write_classification()
    write_regression()
    print(f"[OK] 已写入 {OUT}")


if __name__ == "__main__":
    main()
