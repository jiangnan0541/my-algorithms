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

- [x] `quick_sort` — 快速排序　→ 官方 `sorts/quick_sort.py`　★样板
- [ ] `bubble_sort` — 冒泡排序　→ 官方 `sorts/bubble_sort.py`
- [ ] `insertion_sort` — 插入排序　→ 官方 `sorts/insertion_sort.py`
- [ ] `selection_sort` — 选择排序　→ 官方 `sorts/selection_sort.py`
- [ ] `merge_sort` — 归并排序　→ 官方 `sorts/merge_sort.py`
- [ ] `heap_sort` — 堆排序　→ 官方 `sorts/heap_sort.py`
- [ ] `counting_sort` — 计数排序　→ 官方 `sorts/counting_sort.py`
- [ ] `radix_sort` — 基数排序　→ 官方 `sorts/radix_sort.py`
- [ ] `shell_sort` — 希尔排序　→ 官方 `sorts/shell_sort.py`
- [ ] `bucket_sort` — 桶排序　→ 官方 `sorts/bucket_sort.py`

## 动态规划 `src/myalgo/dynamic_programming/`　（官方 `dynamic_programming/`）

- [x] `knapsack_01` — 0/1 背包　→ 官方 `dynamic_programming/knapsack.py`　★样板
- [ ] `longest_common_subsequence` — 最长公共子序列　→ 官方 `dynamic_programming/longest_common_subsequence.py`
- [ ] `edit_distance` — 编辑距离　→ 官方 `dynamic_programming/edit_distance.py`
- [ ] `coin_change` — 零钱兑换　→ 官方 `dynamic_programming/minimum_coin_change.py`
- [ ] `longest_increasing_subsequence` — 最长递增子序列　→ 官方 `dynamic_programming/longest_increasing_subsequence.py`
- [ ] `matrix_chain_order` — 矩阵连乘　→ 官方 `dynamic_programming/matrix_chain_order.py`
- [ ] `max_subarray` — 最大子段和（Kadane）　→ 官方 `dynamic_programming/max_subarray_sum.py`
- [ ] `fibonacci_dp` — 斐波那契（迭代 DP）　→ 官方 `dynamic_programming/fibonacci.py`
- [ ] `subset_sum` — 子集和　→ 官方 `dynamic_programming/sum_of_subset.py`
- [ ] `rod_cutting` — 钢条切割　→ 官方 `dynamic_programming/rod_cutting.py`

## 图论 `src/myalgo/graph/`　（官方 `graphs/`）

- [x] `bfs` — 广度优先搜索 + 无权最短路　→ 官方 `graphs/breadth_first_search.py`　★样板
- [ ] `dfs` — 深度优先搜索　→ 官方 `graphs/depth_first_search.py`
- [ ] `topological_sort` — 拓扑排序　→ 官方 `graphs/g_topological_sort.py`（Kahn 版见 `kahns_algorithm_topo.py`）
- [ ] `dijkstra` — 单源最短路（非负权）　→ 官方 `graphs/dijkstra.py`
- [ ] `bellman_ford` — 单源最短路（含负权 + 负环检测）　→ 官方 `graphs/bellman_ford.py`
- [ ] `floyd_warshall` — 多源最短路　→ 官方 `graphs/graphs_floyd_warshall.py`（`dynamic_programming/` 下另有一版）
- [ ] `union_find` — 并查集　→ 官方 `data_structures/disjoint_set/disjoint_set.py`（**不在三目标目录内**）
- [ ] `kruskal` — 最小生成树　→ 官方 `graphs/minimum_spanning_tree_kruskal.py`
- [ ] `prim` — 最小生成树　→ 官方 `graphs/minimum_spanning_tree_prims.py`
- [ ] `cycle_detect` — 有向图环检测　→ 官方 `graphs/check_cycle.py`

---

## 读源码时记下的两个官方瑕疵（顺手记，别踩）

1. `sorts/topological_sort.py` —— **拓扑排序被放在了 `sorts/` 目录里**。
   它本质是图算法（基于 DFS 后序），放在排序分类下属于归类不严谨。
   我们自己的 `topological_sort` 放在 `src/myalgo/graph/`，是对的。
2. 官方同名算法常有多份实现（Dijkstra 5 个文件、LIS 3 个、矩阵连乘 2 个），
   文件之间没有任何交叉说明。**本项目每个算法只写一份**，用注释说明清楚，
   避免同样的混乱。

## 进度

| 分类 | 已完成 | 目标 |
|---|---|---|
| 排序 | 1 | 10 |
| 动态规划 | 1 | 10 |
| 图论 | 1 | 10 |
| **合计** | **3** | **30** |

## M2 补充要求

- [ ] 每个算法补边界用例：空输入、单元素、全等值、逆序、含负数
- [ ] 至少 3 个算法加「与朴素实现 / 标准库对拍」的随机测试
- [ ] `pytest --cov=myalgo` 覆盖率 > 80%（当前样板阶段：99%）
- [ ] 照官方 `sorts/benchmark_sorts.py` 写一个 `benchmark_sorting.py`，
      用 `timeit` 横向对比自己 10 个排序的耗时
