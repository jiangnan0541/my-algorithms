"""Bellman-Ford 单源最短路（支持负权 + 负环检测）。

输入是**边表**：``[(起点, 终点, 权值), ...]`` 加节点个数，节点编号 0..n-1。

思路（逐轮松弛）：对所有边做 V-1 轮松弛。因为一条最短路最多含 V-1 条边，
所以 V-1 轮之后一定收敛。第 V 轮还能继续松弛 => 存在从起点可达的负权环，
此时最短路无意义（可以无限绕圈把距离压到 -inf）。

时间复杂度：O(V * E)
空间复杂度：O(V)

与 Dijkstra 的关系：Dijkstra 用优先队列把每轮"取最小"压到 log 级，所以更快，
但要求边权非负；Bellman-Ford 慢，但能处理负权，还能检测负环。
"""

from __future__ import annotations

INF = float("inf")


def bellman_ford(edges: list, num_vertices: int, start: int) -> list:
    """返回长度为 num_vertices 的距离数组，不可达节点为 inf。

    存在从 start 可达的负权环时抛 ValueError。

    >>> bellman_ford([(0, 1, 4), (0, 2, 5), (1, 2, -3), (2, 3, 2)], 4, 0)
    [0, 4, 1, 3]
    >>> bellman_ford([(0, 1, 1)], 3, 0)
    [0, 1, inf]
    >>> bellman_ford([(0, 1, 1), (1, 2, -2), (2, 1, -2)], 3, 0)
    Traceback (most recent call last):
        ...
    ValueError: 图中存在从起点可达的负权环，最短路无定义
    """
    if not 0 <= start < num_vertices:
        raise ValueError(f"起点 {start} 超出 0..{num_vertices - 1} 范围")

    dist = [INF] * num_vertices
    dist[start] = 0

    for _ in range(num_vertices - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break  # 提前收敛，剩下的轮次没必要跑

    # 第 V 轮：若还能松弛，说明有负环
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            raise ValueError("图中存在从起点可达的负权环，最短路无定义")

    return dist


def bellman_ford_path(edges: list, num_vertices: int, start: int, target: int) -> tuple[float, list]:
    """返回 (最短距离, 路径)；不可达时返回 (inf, [])。

    >>> edges = [(0, 1, 4), (0, 2, 5), (1, 2, -3), (2, 3, 2)]
    >>> bellman_ford_path(edges, 4, 0, 3)
    (3, [0, 1, 2, 3])
    >>> bellman_ford_path(edges, 4, 3, 0)
    (inf, [])
    """
    dist = bellman_ford(edges, num_vertices, start)
    if target < 0 or target >= num_vertices or dist[target] == INF:
        return INF, []

    # 反向推一条路径：从 target 出发找满足 d[u] + w == d[v] 的前驱
    path = [target]
    cur = target
    while cur != start:
        for u, v, w in edges:
            if v == cur and dist[u] != INF and dist[u] + w == dist[v]:
                path.append(u)
                cur = u
                break
        else:  # pragma: no cover - 距离表正确时不会走到这里
            return INF, []
    return dist[target], path[::-1]
