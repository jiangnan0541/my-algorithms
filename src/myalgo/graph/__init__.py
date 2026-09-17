"""图论算法（10 个）。

图表示法约定（全目录统一，避免官方那种"5 种图表示法混用"）：
- 无权图：``{节点: [邻居, ...]}``
- 加权图：``{节点: [(邻居, 权值), ...]}``
- 边表：``[(u, v, w), ...]``
- 邻接矩阵：``matrix[i][j]``，无边用 ``float("inf")``
"""

from .bellman_ford import bellman_ford, bellman_ford_path
from .bfs import bfs_order, shortest_path_length
from .cycle_detect import (
    find_cycle_directed,
    has_cycle_directed,
    has_cycle_undirected,
)
from .dfs import connected_components, dfs_order, dfs_order_recursive
from .dijkstra import dijkstra, dijkstra_path
from .floyd_warshall import floyd_warshall, has_negative_cycle
from .kruskal import kruskal
from .prim import prim
from .topological_sort import topological_sort, topological_sort_dfs
from .union_find import UnionFind

__all__ = [
    "UnionFind",
    "bellman_ford",
    "bellman_ford_path",
    "bfs_order",
    "connected_components",
    "dfs_order",
    "dfs_order_recursive",
    "dijkstra",
    "dijkstra_path",
    "find_cycle_directed",
    "floyd_warshall",
    "has_cycle_directed",
    "has_cycle_undirected",
    "has_negative_cycle",
    "kruskal",
    "prim",
    "shortest_path_length",
    "topological_sort",
    "topological_sort_dfs",
]
