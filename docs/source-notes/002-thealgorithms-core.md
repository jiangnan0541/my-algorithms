# 读源码笔记 002 — TheAlgorithms/Python 核心三目录精读

> 这是 001 模板的**填实版**：记录 2026-09-18 对官方仓库 `sorts` / `dynamic_programming` /
> `graphs` 三个目录的完整精读。依赖图与实测数据见 [`../architecture.md`](../architecture.md)。

## 基本信息

| 项 | 值 |
|---|---|
| 官方仓库 | <https://github.com/TheAlgorithms/Python> |
| 精读 commit | `c6012e3`（2026-09-17，master 浅克隆） |
| 本地参考仓 | `D:\workbody\github\_reference\TheAlgorithms-Python` |
| 仓库规模 | 1539 个 `.py` / 16 MB / 49 个顶层目录 |
| 目标目录 | `sorts/` 59 文件、`dynamic_programming/` 52 文件、`graphs/` 63 文件（+4 测试） |
| 官方 Python 要求 | `>= 3.14`（`.python-version` = `3.14t`，free-threaded） |

## 这个仓库在解决什么问题

**用可运行的代码把"算法教科书"翻译成 Python，供人阅读和学习** —— 它不是给生产环境用的库。
README 自己写明了：

> "Implementations are for learning purposes only. They may be less efficient than the
> implementations in the Python standard library."

这个定位决定了它的全部设计取舍：**可读性 > 性能，自足性 > 复用**。

## 核心模块精读

### 模块 1：`sorts/`（59 个文件）

- **职责**：收录几乎全部排序算法，从教科书经典（冒泡 / 快排 / 归并 / 堆排）到冷门猎奇
  （斯大林排序、bogosort、slowsort、煎饼排序）。
- **关键数据结构**：几乎都是 Python 内建 `list`，没有自定义类型；少数用 `typing.Protocol`
  做"可比较"的约束。
- **主流程**：一个文件 = 一个排序函数，吃 `list` 吐排序后的 `list`。
- **我觉得设计得好的地方**：
  - 命名极规范：文件名就是算法名，函数名与文件名一致，想找什么直接找得到。
  - doctest 覆盖到位：正常值、空列表、负数、字符串、**甚至类型错误**都写成断言。
    例如 `heap_sort.py` 有 6 个 doctest，最后一个是预期抛异常：

    ```python
    >>> heap_sort([1, "two"])  # doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    TypeError: ...
    ```

  - `benchmark_sorts.py` 用 `timeit` 横向对比十几个排序的耗时 —— 这是很有价值的"可运行文档"。
- **我觉得可以改进的地方**：
  - 部分文件用了 Python 3.12+ 的 PEP 695 泛型语法（如 `heap_sort[T: Comparable]`），
    低版本解释器根本跑不起来 —— 让"拿下来就能跑"这个卖点打了折扣。
  - 注释密度不统一：有的文件逐行英文注释，有的只有一行 docstring。

### 模块 2：`dynamic_programming/`（52 个文件）

- **职责**：DP 经典问题集：0/1 背包、LCS、编辑距离、矩阵连乘、LIS、零钱兑换、Viterbi……
- **关键数据结构**：一维 / 二维 `list` 当状态表（自底向上为主），少数用 `@lru_cache`
  走自顶向下记忆化。
- **主流程**：典型三段式 —— 定义状态 → 写转移方程 → 处理边界。文件名即问题名。
- **值得注意的**：
  - `knapsack.py`（153 行）给了多条实现路径，注释里直接写了状态转移方程；
  - `viterbi.py`（376 行）是目录里最大的文件；
  - `catalan_numbers.py` 和 `egg_dropping.py` 用了 **PEP 758** 的 `except A, B:` 语法
    —— **Python 3.14 以下连解析都过不了**（本机 3.13 实测报
    `multiple exception types must be parenthesized`）。
- **我觉得可以改进的地方**：同族问题之间没有交叉引用。LIS 有 3 个文件、矩阵连乘有 2 个，
  读者不知道先看哪个、差异到底在哪 —— 明明是最适合做对比说明的地方。

### 模块 3：`graphs/`（63 个文件 + `tests/`）

- **职责**：图论全家桶：遍历（BFS / DFS）、最短路（Dijkstra / Bellman-Ford / Floyd / Johnson）、
  最小生成树（Kruskal / Prim / Boruvka）、拓扑排序、强连通分量、最大流、旅行商……
- **关键数据结构**：**没有统一的图类型**，各文件按需自选表示法：

  | 表示法 | 用在哪 |
  |---|---|
  | `dict[顶点, list[邻接顶点]]` | 最普遍（无权图） |
  | `dict[顶点, list[(邻接, 权)]]` | 带权图，如 `dijkstra.py` |
  | 邻接矩阵 | `graph_adjacency_matrix.py` |
  | 完整 `Graph` 类封装 | 仅 `graph_adjacency_list.py` / `graph_adjacency_matrix.py`（各约 600 行） |

- **主流程**：多数是「函数式」—— 传入图（字典）和起点/终点，返回值。
  `breadth_first_search.py` 是少数派，给了 `Graph` 类 + `bfs()` 方法。
- **我觉得设计得好的地方**：
  - 算法**变体**收录得很全（Dijkstra 5 个文件、BFS 6 个文件），说明社区在"同一问题的
    不同解法"上非常活跃 —— 这本身就是可以借鉴的组织方式。
  - `tests/` 下 4 个文件用 `unittest` 写显式测试，是少数不靠 doctest 的地方。
- **我觉得可以改进的地方**：
  - `dijkstra.py` 在**模块顶层**直接 `print()` 结果（第 107-114 行），
    **import 它就会打印 3 行** —— 与 CONTRIBUTING 明确要求的"最小副作用"相悖。
  - 图表示法在文件间五花八门，读者来回切换要不断重新适应。

## 我的 mini 版与官方的差异

| 点 | 官方 | 我的做法 | 为什么这么改 |
|---|---|---|---|
| Python 版本 | 3.14t（free-threaded） | **3.11** | 本机 `py311` 环境；语法通用性更好，不受 free-threading 限制 |
| 测试方式 | doctest 为主（88% 覆盖），由 `pytest --doctest-modules` 驱动 | **doctest + 独立 pytest 用例双轨** | 独立用例能参数化、能随机对拍、能统计覆盖率；doctest 保留作"能跑的文档" |
| 复杂度标注 | 仅 14% 的文件标了 | **每个函数必标**（时间 + 空间） | 学习目的，不标等于没学 |
| 函数签名 | 不统一（有的原地排序、有的返回新表） | 统一「**不改入参、返回新对象**」 | 减少副作用，测试友好；`quick_sort` 已按此写 |
| 目录命名 | `sorts` / `graphs`（复数） | `sorting` / `graph`（单数） | 个人习惯，不影响功能对齐 |
| 图表示法 | 五种以上混用 | 统一用 `dict[顶点, list[...]]` | 一种表示法贯穿 10 个图算法，便于横向对比 |
| 单文件自足 | 100% 遵守（实测零跨目录依赖） | ✅ 同样遵守 | 实测证明这是官方可维护性的关键，值得照搬 |
| 基准对比 | `benchmark_sorts.py` + `timeit` | M1 完成后照做 `benchmark_sorting.py` | 同一份数据跑自己 10 个排序，横向对比耗时 |

## 学到的三条方法论

1. **单文件自足 = 可贡献性。** 177 个文件里没有一条跨目录依赖（除基准脚本），
   任何人复制一个文件出去就能跑、能改、能提 PR —— 这是它积累上万贡献者的底层原因。
   本项目从一开始就遵循这条，实测证明方向是对的。
2. **doctest 是"能跑的文档"。** 它同时回答"这段代码怎么用"和"这段代码还对吗"两个问题，
   且天然适配算法这种纯函数场景。保留它是对的。
3. **教科书代码也要对齐版本节奏。** 官方已经跑到 3.14t，语法走在了大多数读者前面。
   我选 3.11 是务实取舍（本机环境 + 通用性），但要清楚这是取舍，不是标准。

## 可提 PR 的点（贡献阶段的备选）

- [x] **`CONTRIBUTING.md:199` 拼写错误**：`pslease` → `please`（★ 首选，零争议）
- [x] **`CONTRIBUTING.md:70-82` 重复段落**：`#### Pre-Commit Plugin` 标题下是前文的逐字重复
- [ ] `graphs/dijkstra.py:107-114` 模块级 `print()` 副作用（有讨论空间，暂缓）

详细方案见 [`../upstream-pr-plan.md`](../upstream-pr-plan.md)。
