# ModelingPaperKit

**数学建模论文排版工具包** — 核心引擎 + 多赛事插件架构

> 一套代码，三赛通用。核心引擎与赛事表层彻底分离。

## 架构

```
ModelingPaperKit/
├── core/                      # 核心排版引擎
│   ├── paperkit-base.sty      # 页面、字体、边距、图表底层逻辑
│   ├── paperkit-math.sty      # 数学公式、定理环境增强
│   └── paperkit-utils.sty     # 算法伪代码、代码块、实用宏
├── templates/                 # 赛事专属模板
│   ├── cumcm/                 # 国赛/高教杯 (CUMCM)
│   ├── mcm/                   # 美赛 (MCM/ICM)
│   └── wuyi/                  # 五一杯
├── scripts/                   # 构建与自动化
│   ├── build.py               # 一键编译
│   └── clean.py               # 清理缓存
└── examples/                  # 示例与脱敏数据
```

## 快速开始

### 编译模板

```bash
# 编译国赛模板
python scripts/build.py --target cumcm

# 编译美赛模板
python scripts/build.py --target mcm

# 编译五一杯模板
python scripts/build.py --target wuyi

# 清理后编译
python scripts/build.py --target cumcm --clean

# 一键编译全部
python scripts/build.py --target all
```

### 清理

```bash
# 清理所有编译缓存
python scripts/clean.py
```

### 使用模板

1. 复制对应 `templates/<赛事>/` 下的 `main_*.tex` 和 `sections/` 到你的工作目录
2. 修改论文标题 `\PaperTitle` 或 `\MCMTitle`
3. 在各 `sections/*.tex` 中填写你的内容
4. 运行 `python scripts/build.py --target <赛事>`

## 赛事说明

| 赛事 | 目录 | 文档类 | 语言 | 特殊要求 |
|------|------|--------|------|----------|
| 国赛/高教杯 | `templates/cumcm/` | ctexart | 中文 | 承诺书 + 编号页 |
| 美赛 | `templates/mcm/` | article | 英文 | Summary Sheet |
| 五一杯 | `templates/wuyi/` | ctexart | 中文 | 五一杯承诺书 |

> **关于"高教杯"与"国赛"**：全国大学生数学建模竞赛 (CUMCM) 的最高奖为"高教社杯"，两者是同一比赛。本工具包中 `cumcm` 即为该赛事的通用模板，适用于本/专科组别。

## 依赖

- TeX Live 2024+ 或 MiKTeX（需含 `xelatex`）
- 中文字体：SimSun（宋体）、SimHei（黑体）、FangSong（仿宋）
- Python 3.10+（仅构建脚本需要）

## 许可

MIT License
