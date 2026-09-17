"""Dijkstra 单源最短路（非负权）。

图用**加权**邻接表表示：``{节点: [(邻居, 权值), ...]}``。

思路（贪心 + 优先队列）：每次从"未确定"的节点中取出当前距离最小的那个，
它的距离就已经是最终答案（因为边权非负，绕路不可能更短），然后用它松弛邻居。

时间复杂度：O((V + E) log V)（二叉堆）
空间复杂度：O(V)

**限制**：边权必须非负。带负权要用 Bellman-Ford（见 `bellman_ford.py`）。
本实现会显式检查并抛 ValueError，而不是悄悄给出错误答案。

注：官方仓库里 dijkstra 有 5 个文件（`dijkstra.py` / `dijkstra_2.py` /
    `dijkstra_algorithm.py` / `dijkstra_alternate.py` / `bidirectional_dijkstra.py`），
    彼此没有交叉说明。本项目只保留一份。
"""

from __future__ import annotations

import heapq


def _check_non_negative(graph: dict) -> None:
    """边权非负性检查，负权直接报错。"""
    for node, neighbors in graph.items():
        for edge in neighbors:
            if edge[1] < 0:
                raise ValueError(f"边 {node} -> {edge[0]} 权值为负，请改用 Bellman-Ford")


def dijkstra(graph: dict, start) -> dict:
    """返回从 start 出发到各**可达**节点的最短距离 ``{节点: 距离}``。

    不可达节点不出现在结果里。图中不存在 start 时返回 {}。

    >>> g = {"A": [("B", 1), ("C", 4)], "B": [("C", 2), ("D", 5)], "C": [("D", 1)], "D": []}
    >>> dijkstra(g, "A")
    {'A': 0, 'B': 1, 'C': 3, 'D': 4}
    >>> dijkstra({"A": []}, "A")
    {'A': 0}
    >>> dijkstra(g, "Z")
    {}
    >>> dijkstra({"A": [("B", -1)], "B": []}, "A")
    Traceback (most recent call last):
        ...
    ValueError: 边 A -> B 权值为负，请改用 Bellman-Ford
    """
    if start not in graph:
        return {}
    _check_non_negative(graph)

    dist = {start: 0}
    heap = [(0, start)]

    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float("inf")):
            continue  # 过期堆项，跳过
        for nxt, weight in graph.get(node, []):
            nd = d + weight
            if nd < dist.get(nxt, float("inf")):
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return dist


def dijkstra_path(graph: dict, start, target) -> tuple[float, list]:
    """返回 (最短距离, 路径列表)；不可达时返回 (inf, [])。

    >>> g = {"A": [("B", 1), ("C", 4)], "B": [("C", 2), ("D", 5)], "C": [("D", 1)], "D": []}
    >>> dijkstra_path(g, "A", "D")
    (4, ['A', 'B', 'C', 'D'])
    >>> dijkstra_path(g, "D", "A")
    (inf, [])
    >>> dijkstra_path(g, "A", "A")
    (0, ['A'])
    """
    if start not in graph or target not in graph:
        return float("inf"), []
    _check_non_negative(graph)

    dist = {start: 0}
    prev: dict = {}
    heap = [(0, start)]

    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float("inf")):
            continue
        if node == target:
            break
        for nxt, weight in graph.get(node, []):
            nd = d + weight
            if nd < dist.get(nxt, float("inf")):
                dist[nxt] = nd
                prev[nxt] = node
                heapq.heappush(heap, (nd, nxt))

    if target not in dist:
        return float("inf"), []

    path = [target]
    while path[-1] != start:
        path.append(prev[path[-1]])
    return dist[target], path[::-1]
