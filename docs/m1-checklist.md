# M1 清单 — 三类各手写 10 个

> 路线图阶段 1 的 M1 目标：**排序 / 动态规划 / 图论各手写 10 个，跑通 pytest**。
> 每写完一个：勾掉 → 补 docstring → 在 `tests/` 加对拍用例。

## 排序 `src/myalgo/sorting/`

- [x] `quick_sort` — 快速排序（样板，含 doctest + pytest）
- [ ] `bubble_sort` — 冒泡排序
- [ ] `insertion_sort` — 插入排序
- [ ] `selection_sort` — 选择排序
- [ ] `merge_sort` — 归并排序
- [ ] `heap_sort` — 堆排序
- [ ] `counting_sort` — 计数排序
- [ ] `radix_sort` — 基数排序
- [ ] `shell_sort` — 希尔排序
- [ ] `bucket_sort` — 桶排序

## 动态规划 `src/myalgo/dynamic_programming/`

- [x] `knapsack_01` — 0/1 背包（样板，含暴力对拍）
- [ ] `longest_common_subsequence` — 最长公共子序列
- [ ] `edit_distance` — 编辑距离
- [ ] `coin_change` — 零钱兑换
- [ ] `longest_increasing_subsequence` — 最长递增子序列
- [ ] `matrix_chain_order` — 矩阵连乘
- [ ] `max_subarray` — 最大子段和（Kadane）
- [ ] `fibonacci_dp` — 斐波那契（迭代 DP）
- [ ] `subset_sum` — 子集和
- [ ] `rod_cutting` — 钢条切割

## 图论 `src/myalgo/graph/`

- [x] `bfs` — 广度优先搜索 + 无权最短路（样板）
- [ ] `dfs` — 深度优先搜索
- [ ] `topological_sort` — 拓扑排序
- [ ] `dijkstra` — 单源最短路（非负权）
- [ ] `bellman_ford` — 单源最短路（含负权 + 负环检测）
- [ ] `floyd_warshall` — 多源最短路
- [ ] `union_find` — 并查集
- [ ] `kruskal` — 最小生成树
- [ ] `prim` — 最小生成树
- [ ] `cycle_detect` — 有向图环检测

## M2 补充要求

- [ ] 每个算法补边界用例：空输入、单元素、全等值、逆序、含负数
- [ ] 至少 3 个算法加「与朴素实现/标准库对拍」的随机测试
- [ ] `pytest --cov=myalgo` 覆盖率 > 80%
