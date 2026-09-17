# my-algorithms — 经典算法手写实现（30 个）

> 复刻自官方仓库：<https://github.com/TheAlgorithms/Python>
> 路线：**读**源码 → **写** mini 版 → **证**对比 → **贡献** PR

手写实现经典算法，按 **排序 / 动态规划 / 图论** 三大类组织，
全部配 pytest 单元测试与 docstring doctest，覆盖率 99%。

## 我做了什么

- **读**：完整分析官方仓库（1539 个 `.py` / 49 个顶层目录 / 16 MB），
  对 `sorts` / `dynamic_programming` / `graphs` 三个目标目录做了 **177 个文件的
  AST 级依赖分析**，产出模块依赖图（见 `docs/architecture.md`）与精读笔记。
- **写**：从零手写 **30 个算法**（三类各 10 个）。
  统一约定：不改入参、返回新对象、每个函数标注时间与空间复杂度、
  统一图表示法。
- **证**：doctest 52 条 + 单元测试 290 个 = **342 条可执行断言**，
  825 条语句全覆盖，分支覆盖 431/432。
  另有 **9 组随机对拍**（与标准库、暴力枚举、以及另一套算法互相印证），
  详见 `docs/test-report.md`。
- **贡献**：已在官方 `CONTRIBUTING.md` 定位到 1 处拼写错误与 1 处重复段落，
  具体方案见 `docs/upstream-pr-plan.md`。

## 学到什么

读官方 177 个文件、再自己写 30 个之后，印象最深的五条：

1. **单文件自足 = 可贡献性。** 三个目标目录之间**零 import**（整仓唯一的模块内
   引用是一个基准测试脚本）。这就是它能让上千人各自独立提交的原因 ——
   复制一个文件出去就能跑。本项目同样坚持这条：连 Kruskal 需要的并查集
   都在文件内内联了一份最小实现。
2. **doctest 是"能跑的文档"。** 官方 88% 的文件把 `>>>` 示例写进 docstring。
   它同时回答"怎么用"和"还对吗"两个问题。代价是示例必须永远可运行 ——
   写完 52 条之后，我在 `lis_sequence` 上就被"等长解不唯一"卡过一次。
3. **教科书代码也会跑在版本前面。** 官方已迁到 Python **3.14t**（free-threaded），
   8% 的文件用了 PEP 695 泛型语法，2 个文件用了 PEP 758 ——
   后者连本机 3.13 都解析不了。所以对拍要对齐**算法语义**，不是 import 官方源码。
4. **"另一个 O(n log n)"和"这个 O(n log n)"差得很远。** 实测
   quick 2.79ms / heap 3.23ms / merge 4.28ms（n=2000，同一台机器）。
   归并慢在每层都要 new 一个列表，堆排慢在 sift-down 的缓存局部性。
   复杂度只定数量级，常数项得自己测。
5. **非比较排序的性能参数是值域，不是元素个数。** 值域 10 万、n 只有 2000 时，
   计数排序（4.44ms）比归并（4.28ms）还慢；换成全等值输入只要 0.15ms。
   "计数排序是 O(n+k)"里的 k 才是决定项。完整数据见
   `docs/benchmark-results.md`。

## 分类索引

复杂度一栏是**本实现**的实测标注（含常用的最好/最坏情况）。

### 排序 `src/myalgo/sorting/`

| 算法 | 文件 | 时间复杂度 | 空间 | 稳定 |
|---|---|---|---|---|
| 冒泡排序 | `bubble_sort.py` | O(n²)，已有序 O(n) | O(1) | 稳定 |
| 插入排序 | `insertion_sort.py` | O(n²)，已有序 O(n) | O(1) | 稳定 |
| 选择排序 | `selection_sort.py` | O(n²)，无最好情况 | O(1) | 不稳定 |
| 归并排序 | `merge_sort.py` | O(n log n) 恒定 | O(n) | 稳定 |
| 快速排序 | `quick_sort.py` | 平均 O(n log n)，最坏 O(n²) | O(log n) | 不稳定 |
| 堆排序 | `heap_sort.py` | O(n log n) 恒定 | O(1) | 不稳定 |
| 希尔排序 | `shell_sort.py` | 约 O(n^1.3)，最坏 O(n²) | O(1) | 不稳定 |
| 计数排序 | `counting_sort.py` | O(n + k)，k 为值域宽度 | O(n + k) | 稳定 |
| 基数排序 | `radix_sort.py` | O(d(n + k))，d 为位数 | O(n + k) | 稳定 |
| 桶排序 | `bucket_sort.py` | 平均 O(n + k)，最坏 O(n²) | O(n + k) | 稳定 |

### 动态规划 `src/myalgo/dynamic_programming/`

| 算法 | 文件 | 时间复杂度 | 空间 |
|---|---|---|---|
| 0/1 背包 | `knapsack.py` | O(nW) | O(W) |
| 最长公共子序列 | `longest_common_subsequence.py` | O(mn) | O(mn) |
| 编辑距离 | `edit_distance.py` | O(mn) | O(min(m, n)) |
| 零钱兑换 | `coin_change.py` | O(amount × 币种数) | O(amount) |
| 最长递增子序列 | `longest_increasing_subsequence.py` | O(n log n) / O(n²) | O(n) |
| 矩阵连乘 | `matrix_chain_order.py` | O(n³) | O(n²) |
| 最大子段和 | `max_subarray.py` | O(n) | O(1) |
| 斐波那契（迭代 DP） | `fibonacci_dp.py` | O(n) | O(1) |
| 子集和 | `subset_sum.py` | O(n × target) | O(target) |
| 钢条切割 | `rod_cutting.py` | O(n²) | O(n) |

### 图论 `src/myalgo/graph/`

| 算法 | 文件 | 时间复杂度 | 空间 |
|---|---|---|---|
| 广度优先搜索 | `bfs.py` | O(V + E) | O(V) |
| 深度优先搜索 | `dfs.py` | O(V + E) | O(V) |
| 拓扑排序 | `topological_sort.py` | O(V + E) | O(V) |
| 环检测（有向/无向） | `cycle_detect.py` | O(V + E) | O(V) |
| 并查集 | `union_find.py` | 近似 O(α(n)) | O(n) |
| Dijkstra 单源最短路 | `dijkstra.py` | O((V + E) log V) | O(V) |
| Bellman-Ford（含负环检测） | `bellman_ford.py` | O(V × E) | O(V) |
| Floyd-Warshall 多源最短路 | `floyd_warshall.py` | O(V³) | O(V²) |
| Kruskal 最小生成树 | `kruskal.py` | O(E log E) | O(V + E) |
| Prim 最小生成树 | `prim.py` | O(E log E) | O(V + E) |

## 基准实测

`python benchmarks/benchmark_sorting.py` 在 n=2000、值域 10 万下的结果（单位 ms）：

| 算法 | random | sorted | reversed | all-equal | nearly-sorted |
|---|---|---|---|---|---|
| bubble | 204.57 | 0.11 | 268.37 | 0.11 | 112.57 |
| insertion | 86.50 | 0.18 | 180.22 | 0.19 | 2.63 |
| selection | 103.93 | 94.83 | 91.86 | 96.85 | 95.05 |
| merge | 4.28 | 2.43 | 2.63 | 2.39 | 2.87 |
| quick | 2.79 | 1.92 | 2.04 | 0.18 | 2.05 |
| heap | 3.23 | 3.78 | 3.00 | 0.57 | 3.52 |
| shell | 2.83 | 1.43 | 2.09 | 1.50 | 2.10 |
| counting | 4.44 | 4.67 | 3.81 | 0.15 | 4.05 |
| radix | 0.88 | 0.80 | 0.83 | 0.23 | 0.82 |
| bucket | 0.73 | 0.69 | 0.76 | 0.035 | 0.70 |

完整分析（含 n=200 小规模档与逐条解读）见 `docs/benchmark-results.md`。

## 与官方对比（官方列为实测数据）

| 维度 | 官方 TheAlgorithms/Python | 我的 mini 版 |
|---|---|---|
| 定位 | 算法标本集，**不是**可安装的库 | 聚焦三类精选 |
| 规模 | 1539 个 `.py` / 49 个顶层目录 | **30 个**（三类各 10） |
| Python 版本 | `>= 3.14`（`.python-version` = `3.14t`） | **3.11**，语法通用性更好 |
| 目录耦合 | 零跨目录依赖（177 文件仅 1 处内部引用） | 同样坚持单文件自足 |
| 测试 | `pytest --doctest-modules`，88% 文件含 doctest | doctest + 独立 pytest 用例**双轨**，便于参数化对拍与覆盖率统计 |
| 测试规模 | — | 342 条断言，语句覆盖 100%、分支 431/432 |
| 复杂度标注 | 仅 14% 的文件标注 | **每个函数强制标注**时间 + 空间 |
| 风格 | 90% 遵循同一骨架，但图表示法（5 种以上）、注释密度不统一 | 统一骨架 + 统一图表示法（4 种，在 `graph/__init__.py` 里写明） |
| 性能数据 | 有 `sorts/benchmark_sorts.py` | 有 `benchmarks/benchmark_sorting.py`，含 5 种输入分布 |

## 目录结构

```
my-algorithms/
├── src/myalgo/
│   ├── sorting/               # 排序 10 个
│   ├── dynamic_programming/   # 动态规划 10 个
│   └── graph/                 # 图论 10 个
├── tests/
│   ├── test_sorting.py        # 125 个用例
│   ├── test_dp.py             #  85 个用例
│   ├── test_graph.py          #  68 个用例
│   └── test_cross_check.py    #  12 个用例（随机对拍，9 组算法互相印证）
├── benchmarks/
│   └── benchmark_sorting.py   # 10 个排序在 5 种分布上的横向基准
├── docs/
│   ├── architecture.md        # 官方源码模块依赖图（实测）
│   ├── m1-checklist.md        # 30 个算法清单（含官方对应文件）
│   ├── test-report.md         # 测试报告（覆盖率明细 + 对拍清单）
│   ├── benchmark-results.md   # 基准实测数据与分析
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
pytest -v tests/test_sorting.py                   # 只跑排序类
pytest tests/test_cross_check.py -v               # 只跑随机对拍
pytest --doctest-modules src/myalgo -q            # 单独验证 docstring 里的 doctest
pytest --cov=myalgo --cov-report=term-missing     # 覆盖率
python benchmarks/benchmark_sorting.py            # 排序基准（约 20 秒）
```

## 进度

| 里程碑 | 内容 | 状态 |
|--------|------|------|
| M0 | 环境 + 仓库骨架 + 方法论落地 | ✅ |
| M1 | 三类各手写 10 个，跑通 pytest | ✅ 30/30 |
| M2 | 补边界用例与随机对拍，覆盖率 >80% | ✅ 99% |
| M3 | README 分类索引 + 基准对比脚本 | ✅ |
| M4 | 往上游提 1 个 PR | ⬜ 候选已定位 |

## 参考

- 官方仓库：<https://github.com/TheAlgorithms/Python>（精读版本 `c6012e3`，2026-09-17）
- 模块依赖图与实测数据：`docs/architecture.md`
- 测试报告：`docs/test-report.md`
- 基准数据：`docs/benchmark-results.md`
- 读源码笔记：`docs/source-notes/002-thealgorithms-core.md`
- 上游贡献方案：`docs/upstream-pr-plan.md`
- 复刻方法论：`METHODOLOGY.md`
