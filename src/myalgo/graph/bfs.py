"""广度优先搜索（Breadth-First Search, BFS）。

图用邻接表表示：``{节点: [邻居, ...]}``。

思路：从起点开始层层扩散，用队列（FIFO）维护待访问节点，
用 visited 集合避免重复入队。

时间复杂度：O(V + E)
空间复杂度：O(V)
"""

from __future__ import annotations

from collections import deque


def bfs_order(graph: dict, start) -> list:
    """返回从 start 出发的 BFS 访问顺序。图中不存在 start 时返回 []。

    >>> g = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    >>> bfs_order(g, "A")
    ['A', 'B', 'C', 'D']
    >>> bfs_order(g, "Z")
    []
    """
    if start not in graph:
        return []

    visited = {start}
    order = []
    queue = deque([start])

    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph.get(node, []):
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
    return order


def shortest_path_length(graph: dict, start, target) -> int:
    """返回无权图中 start 到 target 的最短跳数；不可达返回 -1。

    >>> g = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    >>> shortest_path_length(g, "A", "D")
    2
    >>> shortest_path_length(g, "D", "A")
    -1
    """
    if start not in graph:
        return -1
    if start == target:
        return 0

    visited = {start}
    queue = deque([(start, 0)])

    while queue:
        node, dist = queue.popleft()
        for nxt in graph.get(node, []):
            if nxt == target:
                return dist + 1
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, dist + 1))
    return -1
