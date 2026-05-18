#!/usr/bin/env python3
"""生成 README 用 Core+Plugins 架构图（UTF-8 SVG）。"""

from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).resolve().parent / "architecture.svg"

SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 400" role="img"
     aria-label="ModelingPaperKit Core + Plugins 架构">
  <defs>
    <linearGradient id="coreGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="100%" stop-color="#2563eb"/>
    </linearGradient>
    <filter id="shadow" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.12"/>
    </filter>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#64748b"/>
    </marker>
  </defs>

  <rect width="820" height="400" fill="#f8fafc" rx="12"/>

  <g filter="url(#shadow)">
    <rect x="210" y="28" width="400" height="88" rx="10" fill="url(#coreGrad)"/>
    <text x="410" y="54" text-anchor="middle" fill="#ffffff"
          font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="18" font-weight="700">core/ 核心引擎</text>
    <text x="410" y="84" text-anchor="middle" fill="#dbeafe"
          font-family="Consolas,monospace" font-size="13">paperkit-base · paperkit-math · paperkit-utils</text>
  </g>

  <g stroke="#94a3b8" stroke-width="2" fill="none" marker-end="url(#arrow)">
    <path d="M280 116 L140 168"/>
    <path d="M350 116 L290 168"/>
    <path d="M470 116 L530 168"/>
    <path d="M540 116 L680 168"/>
  </g>

  <g filter="url(#shadow)">
    <rect x="40" y="168" width="170" height="118" rx="10" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
    <rect x="230" y="168" width="170" height="118" rx="10" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
    <rect x="420" y="168" width="170" height="118" rx="10" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
    <rect x="610" y="168" width="170" height="118" rx="10" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
  </g>

  <text x="125" y="196" text-anchor="middle" fill="#64748b"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="11" font-weight="600">templates/ 赛事模板</text>
  <text x="125" y="220" text-anchor="middle" fill="#0f172a"
        font-family="Consolas,monospace" font-size="16" font-weight="700">cumcm</text>
  <text x="125" y="244" text-anchor="middle" fill="#3b82f6"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="13" font-weight="600">2025 · 中文</text>
  <text x="125" y="266" text-anchor="middle" fill="#475569"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="12">国赛 CUMCM</text>

  <text x="315" y="196" text-anchor="middle" fill="#64748b"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="11" font-weight="600">templates/ 赛事模板</text>
  <text x="315" y="220" text-anchor="middle" fill="#0f172a"
        font-family="Consolas,monospace" font-size="16" font-weight="700">mcm</text>
  <text x="315" y="244" text-anchor="middle" fill="#8b5cf6"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="13" font-weight="600">2026 · 英文</text>
  <text x="315" y="266" text-anchor="middle" fill="#475569"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="12">美赛 MCM/ICM</text>

  <text x="505" y="196" text-anchor="middle" fill="#64748b"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="11" font-weight="600">templates/ 赛事模板</text>
  <text x="505" y="220" text-anchor="middle" fill="#0f172a"
        font-family="Consolas,monospace" font-size="16" font-weight="700">wuyi</text>
  <text x="505" y="244" text-anchor="middle" fill="#059669"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="13" font-weight="600">2026 · 中文</text>
  <text x="505" y="266" text-anchor="middle" fill="#475569"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="12">五一杯</text>

  <text x="695" y="196" text-anchor="middle" fill="#64748b"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="11" font-weight="600">templates/ 赛事模板</text>
  <text x="695" y="220" text-anchor="middle" fill="#0f172a"
        font-family="Consolas,monospace" font-size="16" font-weight="700">beijing</text>
  <text x="695" y="244" text-anchor="middle" fill="#d97706"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="13" font-weight="600">2026 · 中文</text>
  <text x="695" y="266" text-anchor="middle" fill="#475569"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="12">北京赛</text>

  <text x="410" y="328" text-anchor="middle" fill="#64748b"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="13">复制 templates/ → 填写 sections/ → python scripts/build.py --target &lt;赛事&gt;</text>
  <text x="410" y="356" text-anchor="middle" fill="#94a3b8"
        font-family="'Microsoft YaHei','SimHei',sans-serif" font-size="12">Core + Plugins · XeLaTeX</text>
</svg>
"""


def main() -> None:
    OUT.write_text(SVG.strip() + "\n", encoding="utf-8", newline="\n")
    text = OUT.read_text(encoding="utf-8")
    if "核心引擎" not in text or "\ufffd" in text:
        raise SystemExit("[ERROR] SVG 中文校验失败")
    print(f"[OK] 已写入 UTF-8 SVG: {OUT}")


if __name__ == "__main__":
    main()
