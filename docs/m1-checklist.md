# M1 清单 — 三类各手写 10 个

> 路线图阶段 1 的 M1 目标：**排序 / 动态规划 / 图论各手写 10 个，跑通 pytest**。
>
> 「官方对应」是 2026-09-18 实测核对过的路径，30 个目标文件**全部存在**于
> `_reference/TheAlgorithms-Python`（commit `c6012e3`）。
> 官方目录规模：`sorts/` 59 个、`dynamic_programming/` 52 个、`graphs/` 63 个 ——
> 我们各取 10 个最有代表性的，不对齐数量，对齐**质量与规范**。
>
> **单项完成标准**：① 实现 + 时间/空间复杂度标注 ② docstring 含 doctest
> ③ `tests/` 补边界用例 ④ 勾掉这里。

## 排序 `src/myalgo/sorting/`　（官方 `sorts/`）

- [x] `quick_sort` — 快速排序　→ 官方 `sorts/quick_sort.py`
- [x] `bubble_sort` — 冒泡排序　→ 官方 `sorts/bubble_sort.py`
- [x] `insertion_sort` — 插入排序　→ 官方 `sorts/insertion_sort.py`
- [x] `selection_sort` — 选择排序　→ 官方 `sorts/selection_sort.py`
- [x] `merge_sort` — 归并排序　→ 官方 `sorts/merge_sort.py`
- [x] `heap_sort` — 堆排序　→ 官方 `sorts/heap_sort.py`
- [x] `counting_sort` — 计数排序　→ 官方 `sorts/counting_sort.py`
- [x] `radix_sort` — 基数排序　→ 官方 `sorts/radix_sort.py`
- [x] `shell_sort` — 希尔排序　→ 官方 `sorts/shell_sort.py`
- [x] `bucket_sort` — 桶排序　→ 官方 `sorts/bucket_sort.py`

## 动态规划 `src/myalgo/dynamic_programming/`　（官方 `dynamic_programming/`）

- [x] `knapsack_01` — 0/1 背包　→ 官方 `dynamic_programming/knapsack.py`
- [x] `longest_common_subsequence` — 最长公共子序列　→ 官方 `dynamic_programming/longest_common_subsequence.py`
- [x] `edit_distance` — 编辑距离　→ 官方 `dynamic_programming/edit_distance.py`
- [x] `coin_change` — 零钱兑换　→ 官方 `dynamic_programming/minimum_coin_change.py`
- [x] `longest_increasing_subsequence` — 最长递增子序列　→ 官方 `dynamic_programming/longest_increasing_subsequence.py`
- [x] `matrix_chain_order` — 矩阵连乘　→ 官方 `dynamic_programming/matrix_chain_order.py`
- [x] `max_subarray` — 最大子段和（Kadane）　→ 官方 `dynamic_programming/max_subarray_sum.py`
- [x] `fibonacci_dp` — 斐波那契（迭代 DP）　→ 官方 `dynamic_programming/fibonacci.py`
- [x] `subset_sum` — 子集和　→ 官方 `dynamic_programming/sum_of_subset.py`
- [x] `rod_cutting` — 钢条切割　→ 官方 `dynamic_programming/rod_cutting.py`

## 图论 `src/myalgo/graph/`　（官方 `graphs/`）

- [x] `bfs` — 广度优先搜索 + 无权最短路　→ 官方 `graphs/breadth_first_search.py`
- [x] `dfs` — 深度优先搜索（迭代 + 递归两版）　→ 官方 `graphs/depth_first_search.py`
- [x] `topological_sort` — 拓扑排序（Kahn + DFS 两版）　→ 官方 `graphs/g_topological_sort.py`
- [x] `dijkstra` — 单源最短路（非负权）　→ 官方 `graphs/dijkstra.py`
- [x] `bellman_ford` — 单源最短路（含负权 + 负环检测）　→ 官方 `graphs/bellman_ford.py`
- [x] `floyd_warshall` — 多源最短路　→ 官方 `graphs/graphs_floyd_warshall.py`
- [x] `union_find` — 并查集　→ 官方 `data_structures/disjoint_set/disjoint_set.py`（**不在三目标目录内**）
- [x] `kruskal` — 最小生成树　→ 官方 `graphs/minimum_spanning_tree_kruskal.py`
- [x] `prim` — 最小生成树　→ 官方 `graphs/minimum_spanning_tree_prims.py`
- [x] `cycle_detect` — 环检测（有向三色 / 无向父节点法）　→ 官方 `graphs/check_cycle.py`

---

## 读源码时记下的两个官方瑕疵（顺手记，别踩）

1. `sorts/topological_sort.py` —— **拓扑排序被放在了 `sorts/` 目录里**。
   它本质是图算法（基于 DFS 后序），放在排序分类下属于归类不严谨。
   我们自己的 `topological_sort` 放在 `src/myalgo/graph/`，是对的。
2. 官方同名算法常有多份实现（Dijkstra 5 个文件、LIS 3 个、矩阵连乘 2 个），
   文件之间没有任何交叉说明。**本项目每个算法只写一份**，用注释说明清楚，
   避免同样的混乱。

## 自己写的时候踩到的三个坑（写下来，下次不用再想一遍）

1. **`lis_sequence` 的等长解不唯一。** `[10,9,2,5,3,7,101,18]` 长度为 4 的解
   至少有 `[2,3,7,18]` 和 `[2,5,7,101]` 两个。最初把教科书答案硬编码进 doctest，
   测试直接挂。正确做法是在 docstring 里说明"返回其中一个"，测试改成断言
   "长度正确 + 严格递增 + 确实是原序列的子序列"。
2. **无向图的邻接表里，一条边会以两个方向各出现一次。**
   所以父节点必须排除，否则 `A-B` 这一条边会被判成 `A->B->A` 的环。
   反过来，如果误用有向图的三色 DFS 去跑无向图，全图都会被判有环 ——
   `tests/test_graph.py` 里专门留了一个测试记录这个反例。
3. **子集和的一维滚动数组必须逆序。** 顺序遍历会让 `[3]`、目标 6 判成 True
   （同一个 3 被用了两次），也就是把 0/1 背包写成了完全背包。
   也留了一个测试盯着这条。

## 进度

| 分类 | 已完成 | 目标 |
|---|---|---|
| 排序 | 10 | 10 |
| 动态规划 | 10 | 10 |
| 图论 | 10 | 10 |
| **合计** | **30** | **30** |

## M2 补充要求

- [x] 每个算法补边界用例：空输入、单元素、全等值、逆序、含负数
- [x] 至少 3 个算法加「与朴素实现 / 标准库对拍」的随机测试
      —— 实际做了 **9 组**，见 `tests/test_cross_check.py`
- [x] `pytest --cov=myalgo` 覆盖率 > 80%
      —— 实际 **99%**（825 条语句 0 未覆盖，432 个分支仅 1 处结构性不可达）
- [x] 照官方 `sorts/benchmark_sorts.py` 写一个基准脚本
      —— `benchmarks/benchmark_sorting.py`，结果记在 `docs/benchmark-results.md`
