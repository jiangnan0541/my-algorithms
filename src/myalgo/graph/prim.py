"""Prim 最小生成树（MST）。

图用**加权无向**邻接表表示：``{节点: [(邻居, 权值), ...]}``。

思路（贪心 + 优先队列）：从任意起点开始，把"已选集合"到"未选节点"的所有
边丢进最小堆，每次取出权值最小且另一端还没选中的边，把新节点拉进集合。

时间复杂度：O(E log E)（二叉堆；斐波那契堆可到 O(E + V log V)）
空间复杂度：O(V + E)

与 Kruskal 的区别：
- Kruskal 从**边**出发，全局排序 + 并查集，适合边稀疏、边表已给好的场景。
- Prim 从**点**出发，不断扩展已选集合，适合邻接表在手的稠密图。
两者都得同一个答案（MST 权值唯一，但具体选边可能不同）。

注：图不连通时返回最小生成森林（从 start 可达部分 + 其余分量的 MST）。
"""

from __future__ import annotations

import heapq


def prim(graph: dict, start=None) -> tuple[int, list]:
    """返回 (最小生成森林总权值, 选中的边列表 ``[(u, v, w), ...]``)。

    start 缺省取图中第一个节点。图里所有节点都会覆盖到（不连通则各分量各跑一棵）。

    >>> g = {0: [(1, 1), (2, 4), (3, 3)],
    ...      1: [(0, 1), (2, 2)],
    ...      2: [(0, 4), (1, 2), (3, 5)],
    ...      3: [(0, 3), (2, 5)]}
    >>> prim(g)
    (6, [(0, 1, 1), (1, 2, 2), (0, 3, 3)])
    >>> prim({0: []})
    (0, [])
    >>> prim({0: [(1, 2)], 1: [(0, 2)], 2: [(3, 7)], 3: [(2, 7)]})
    (9, [(0, 1, 2), (2, 3, 7)])
    """
    if not graph:
        return 0, []

    visited: set = set()
    total = 0
    chosen: list = []

    # 依次以每个尚未访问的节点为新分量起点，保证不连通图也全覆盖
    for seed in graph:
        if seed in visited:
            continue
        visited.add(seed)
        heap = [(w, seed, nxt) for nxt, w in graph.get(seed, [])]
        heapq.heapify(heap)

        while heap:
            w, u, v = heapq.heappop(heap)
            if v in visited:
                continue  # 会成环，丢弃
            visited.add(v)
            total += w
            chosen.append((u, v, w))
            for nxt, nw in graph.get(v, []):
                if nxt not in visited:
                    heapq.heappush(heap, (nw, v, nxt))
    return total, chosen
