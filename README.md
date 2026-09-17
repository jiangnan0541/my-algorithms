# my-algorithms — 经典算法手写实现

> 复刻自官方仓库：<https://github.com/TheAlgorithms/Python>
> 路线：**读**源码 → **写** mini 版 → **证**对比 → **贡献** PR

手写实现经典算法，按 **排序 / 动态规划 / 图论** 三大类组织，全部配 pytest 单元测试。

## 我做了什么

- **读**：完整分析官方仓库（1539 个 `.py` / 49 个顶层目录 / 16 MB），
  对 `sorts` / `dynamic_programming` / `graphs` 三个目标目录做了 **177 个文件的 AST 级
  依赖分析**，产出模块依赖图（见 `docs/architecture.md`）与精读笔记。
- **写**：从零手写 mini 版，目标 **三类各 10 个共 30 个**（当前完成 3 个样板）。
  统一风格：不改入参、返回新对象、每个函数标注时间/空间复杂度。
- **证**：doctest + 独立 pytest 用例双轨。样板阶段 23 个用例全过、覆盖率 99%，
  其中包含与标准库/暴力实现的随机对拍。
- **贡献**：已在官方 `CONTRIBUTING.md` 定位到 1 处拼写错误与 1 处重复段落，
  具体方案见 `docs/upstream-pr-plan.md`。

## 学到什么

读官方 177 个文件后的三条实测结论：

1. **单文件自足 = 可贡献性。** 三个目录之间**零 import**（整仓唯一的模块内引用是
   一个基准测试脚本）。这就是它能让上千人各自独立提交的原因 —— 复制一个文件出去就能跑。
2. **doctest 是"能跑的文档"。** 官方 88% 的文件把 `>>>` 示例写进 docstring，
   由 `pytest --doctest-modules` 统一驱动。它同时回答"怎么用"和"还对吗"两个问题。
3. **教科书代码也会跑在版本前面。** 官方已迁到 Python **3.14t**（free-threaded），
   8% 的文件用了 PEP 695 泛型语法，2 个文件用了 PEP 758 —— 后者连本机 3.13
   都解析不了。所以对拍要对齐**算法语义**，不是去 import 官方源码。

## 与官方对比（官方列为实测数据）

| 维度 | 官方 TheAlgorithms/Python | 我的 mini 版 |
|---|---|---|
| 定位 | 算法标本集，**不是**可安装的库 | 聚焦三类精选 |
| 规模 | 1539 个 `.py` / 49 个顶层目录 | 30 个（三类各 10） |
| Python 版本 | `>= 3.14`（`.python-version` = `3.14t`） | **3.11**，语法通用性更好 |
| 目录耦合 | 零跨目录依赖（177 文件仅 1 处内部引用） | 同样坚持单文件自足 |
| 测试 | `pytest --doctest-modules`，88% 文件含 doctest | doctest + 独立 pytest 用例**双轨**，便于参数化对拍与覆盖率统计 |
| 复杂度标注 | 仅 14% 的文件标注 | **每个函数强制标注**时间 + 空间 |
| 风格 | 90% 遵循同一骨架，但图表示法（5 种以上）、注释密度不统一 | 统一骨架 + 统一图表示法 |

## 目录结构

```
my-algorithms/
├── src/myalgo/
│   ├── sorting/               # 排序（目标 10 个，已完成 1）
│   ├── dynamic_programming/   # 动态规划（目标 10 个，已完成 1）
│   └── graph/                 # 图论（目标 10 个，已完成 1）
├── tests/                     # pytest 单元测试（23 个用例）
├── docs/
│   ├── architecture.md        # 官方源码模块依赖图（实测）
│   ├── m1-checklist.md        # 30 个算法清单（含官方对应文件）
│   ├── upstream-pr-plan.md    # 上游 PR 计划
│   └── source-notes/          # 读源码笔记（001 模板 / 002 精读）
├── requirements.txt
└── pyproject.toml             # pytest 配置（pythonpath=src，免安装直接跑）
```

## 环境

- Python 3.11（Anaconda3 环境：`conda activate py311`）
- 依赖：`pip install -r requirements.txt`（走清华镜像）

## 运行

```bash
conda activate py311
cd D:\workbody\github\my-algorithms

pytest -q                                        # 跑全部测试
pytest -v tests/test_sorting.py                  # 只跑排序类
pytest --doctest-modules src/myalgo -q           # 单独验证 docstring 里的 doctest
pytest --cov=myalgo --cov-report=term-missing    # 覆盖率
```

## 进度

| 里程碑 | 内容 | 状态 |
|--------|------|------|
| M0 | 环境 + 仓库骨架 + 方法论落地 | ✅ |
| M1 | 三类各手写 10 个，跑通 pytest | 🔄 3/30 |
| M2 | 补边界用例与随机对拍，覆盖率 >80% | ⬜ |
| M3 | README 分类索引 + 基准对比脚本 | ⬜ |
| M4 | 往上游提 1 个 PR | ⬜ 候选已定位 |

### 分类索引

| 分类 | 目录 | 已完成 | 目标 | 官方目录规模 |
|------|------|--------|------|--------------|
| 排序 | `src/myalgo/sorting/` | 1 | 10 | `sorts/` 59 个 |
| 动态规划 | `src/myalgo/dynamic_programming/` | 1 | 10 | `dynamic_programming/` 52 个 |
| 图论 | `src/myalgo/graph/` | 1 | 10 | `graphs/` 63 个 |

## 参考

- 官方仓库：<https://github.com/TheAlgorithms/Python>（精读版本 `c6012e3`，2026-09-17）
- 模块依赖图与实测数据：`docs/architecture.md`
- 读源码笔记：`docs/source-notes/002-thealgorithms-core.md`
- 上游贡献方案：`docs/upstream-pr-plan.md`
- 复刻方法论：`METHODOLOGY.md`
