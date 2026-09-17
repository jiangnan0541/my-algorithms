"""Floyd-Warshall 多源最短路。

输入是 n x n 的**邻接矩阵** ``graph[i][j]`` 表示 i 到 j 的直接边权，
无边用 ``float("inf")``，``graph[i][i] = 0``。

思路（区间 DP）：枚举中转点 k，看"走 k 中转"是否比当前更短：
    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
k 必须放最外层 —— 这样第 k 轮结束时，dist[i][j] 已经考虑了
「中转点只取自 {0..k}」的最优解。

时间复杂度：O(V^3)
空间复杂度：O(V^2)（原地更新，但本实现先复制一份，不改入参）

特点：一次性算出**所有点对**的最短距离，边权可以为负（但不能有负环）。
代码只有三重循环，是 DP 里"最优子结构"最直白的例子。
"""

from __future__ import annotations

INF = float("inf")


def floyd_warshall(graph: list[list[float]]) -> list[list[float]]:
    """返回全源最短路矩阵（新对象，不修改入参）。

    >>> inf = float("inf")
    >>> g = [[0, 5, inf, 10], [inf, 0, 3, inf], [inf, inf, 0, 1], [inf, inf, inf, 0]]
    >>> floyd_warshall(g)
    [[0, 5, 8, 9], [inf, 0, 3, 4], [inf, inf, 0, 1], [inf, inf, inf, 0]]
    >>> floyd_warshall([[0]])
    [[0]]
    """
    n = len(graph)
    dist = [row[:] for row in graph]  # 深一层拷贝，避免染指入参

    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue  # i 到不了 k，这一轮不用试
            for j in range(n):
                through_k = dist[i][k] + dist[k][j]
                if through_k < dist[i][j]:
                    dist[i][j] = through_k
    return dist


def has_negative_cycle(graph: list[list[float]]) -> bool:
    """判断图中是否存在**负权环**。

    原理：若存在负环，绕环会让某点到自己的距离变成负数，
    即 Floyd 跑完后对角线上出现负值。

    >>> inf = float("inf")
    >>> has_negative_cycle([[0, 1], [1, 0]])
    False
    >>> has_negative_cycle([[0, 1], [-2, 0]])
    True
    >>> has_negative_cycle([[0, 2], [2, 0]])
    False
    """
    dist = floyd_warshall(graph)
    return any(dist[i][i] < 0 for i in range(len(dist)))
