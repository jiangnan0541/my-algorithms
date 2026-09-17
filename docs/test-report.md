# 测试报告

> 生成时间：2026-09-18
> 环境：Windows 11 / Python 3.11.16 (Anaconda `py311` / pytest 8.x / pytest-cov)
> 复现命令见文末。

## 一、总览

| 指标 | 数值 |
|---|---|
| 算法模块 | **30**（排序 10 / 动态规划 10 / 图论 10） |
| 单元测试用例 | **290** 个 |
| docstring doctest | **52** 条 |
| 可执行断言合计 | **342** 条 |
| 语句覆盖率 | **825 / 825 = 100%** |
| 分支覆盖率 | **431 / 432 = 99.8%** |
| 综合覆盖率 | **99%** |
| 测试结果 | 全部通过，0 失败 0 跳过 |

覆盖率要求是 M2 的「> 80%」，实际做到 99%（分支覆盖已开启）。

## 二、三层验证策略

单靠硬编码的已知答案只能证明"这几个用例对"。本项目用三层交叉：

**第 1 层 — doctest（52 条）**
每个公开函数都带 `>>>` 示例，由 `pytest --doctest-modules` 驱动。
好处是文档示例必须永远可运行，改了实现忘了改文档会直接测试失败。

**第 2 层 — 参数化单元测试（290 个）**
`tests/` 下按分类组织，统一覆盖五类边界：
空输入、单元素、全等值、逆序、含负数。
排序类的 10 个函数用同一批边界参数化，任意一个行为不一致都会暴露。

**第 3 层 — 随机对拍（`tests/test_cross_check.py`）**
用**独立实现**互相印证，共 9 组：

| 被测算法 | 对拍对象 | 对拍方式 |
|---|---|---|
| LIS（贪心+二分 O(n log n)） | `lis_sequence`（O(n²) DP）＋ 全子序列暴力枚举 | 长度必须三者一致 |
| 零钱兑换（DP） | 金额空间 BFS | 最少枚数一致 |
| 子集和（DP） | `itertools.combinations` 暴力枚举 | 布尔值一致 |
| 最大子段和（Kadane O(n)） | O(n²) 双层求和 | 最大值一致 |
| 编辑距离（滚动数组） | 无记忆化朴素递归 | 距离一致 |
| 矩阵连乘（区间 DP） | 无记忆化朴素递归 | 最少次数一致 |
| Dijkstra（堆） | Floyd-Warshall（区间 DP） | 随机图上一整行距离表逐点一致 |
| Kruskal（边贪心） | Prim（点贪心） | MST 总权值与边数一致 |
| 10 个排序互相对拍 | `sorted()` | 同一批输入上 10 个输出完全相同 |

其中 Dijkstra ↔ Floyd-Warshall、Kruskal ↔ Prim 这两组用的是**完全不同**
的算法范式（堆贪心 vs 区间 DP、边贪心 vs 点贪心），能同时通过说明
不是实现里某个共同的错误在自洽。

## 三、覆盖率明细

按模块统计（`branch = true`，即分支覆盖已开启）：

| 模块 | 语句 | 分支 | 覆盖率 |
|---|---|---|---|
| `myalgo/__init__.py` | 1 | 0 | 100% |
| `sorting/`（10 个算法 + `__init__`） | 187 | 76 | **100%** |
| └ `bubble_sort` / `insertion_sort` / `selection_sort` | 39 | 20 | 100% |
| └ `merge_sort` / `quick_sort` / `heap_sort` / `shell_sort` | 70 | 24 | 100% |
| └ `counting_sort` / `radix_sort` / `bucket_sort` | 67 | 32 | 100% |
| `dynamic_programming/`（10 个算法 + `__init__`） | 248 | 140 | **99.3%** |
| └ `rod_cutting` | 35 | 22 | 98%（仅 1 处不可达分支） |
| └ 其余 9 个算法 | 202 | 118 | 100% |
| `graph/`（10 个算法 + `__init__`） | 389 | 216 | **100%** |
| **合计** | **825** | **432** | **99%** |

### 唯一未覆盖的分支

`src/myalgo/dynamic_programming/rod_cutting.py:27 -> 26`

```python
for j in range(1, rest + 1):
    if prices[j - 1] + dp[rest - j] == dp[rest]:
        plan.append(j)
        ...
        break          # ← 行 27
```

`dp[rest]` 的定义就是「所有切法里的最大值」，所以**必然**存在至少一个 `j`
使等式成立，内层循环一定会在第一处命中就 `break`，「循环自然结束」这条路径
结构上不可达。保留 `for` 写法是为了和上方 DP 递推形式保持一致、便于对照，
不为了刷覆盖率把它改写成 `next()`。

## 四、复现命令

```bash
conda activate py311
cd D:\workbody\github\my-algorithms

# 单元测试 + 覆盖率
pytest --cov=myalgo --cov-report=term-missing

# 只看 doctest（docstring 里的示例）
pytest --doctest-modules src/myalgo -q

# 只跑随机对拍
pytest tests/test_cross_check.py -v

# 生成 HTML 覆盖率报告（打开 htmlcov/index.html）
pytest --cov=myalgo --cov-report=html
```

## 五、还没做的

- 没有做性能回归（每次提交跑基准并比对历史）。当前 `benchmarks/` 只能手动跑。
- 没有接 CI（GitHub Actions）。本机到 GitHub 只有 SSH 22 端口连通，
  Actions 的运行环境与此无关，但推送后的首次构建还没验证过。
- 图论类里 `has_cycle_undirected` 对**平行边**（同一对节点两条边）会判为有环，
  语义上可争议，目前只在 docstring 里写明了「每条边两个方向都要出现」这条前提。
