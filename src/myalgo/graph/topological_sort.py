"""拓扑排序（Topological Sort）。

对**有向无环图（DAG）**给出一个线性排序，使每条边 u -> v 中 u 都排在 v 前。
典型用途：构建系统的依赖顺序、课程先修表、任务调度。

图用邻接表表示：``{节点: [后继节点, ...]}``。

两种实现：
- ``topological_sort`` —— **Kahn 算法**（BFS 版）。统计入度，先把入度为 0 的
  节点入队，逐个出队并把它后继的入度减一，减到 0 就入队。天然能检测环。
- ``topological_sort_dfs`` —— DFS 后序反转版，遇到环返回 None。

时间复杂度：O(V + E)
空间复杂度：O(V)

注：拓扑序通常不唯一。官方把 `topological_sort.py` 放在 `sorts/` 目录下，
    归类不严谨 —— 它是图算法，本项目放在 `graph/`。
"""

from __future__ import annotations

from collections import deque


def topological_sort(graph: dict) -> list:
    """返回一个拓扑序；图中存在环时抛 ValueError。

    >>> dag = {"A": ["C"], "B": ["C", "D"], "C": ["E"], "D": ["E"], "E": []}
    >>> topological_sort(dag)
    ['A', 'B', 'C', 'D', 'E']
    >>> topological_sort({})
    []
    >>> topological_sort({"A": ["B"], "B": ["A"]})
    Traceback (most recent call last):
        ...
    ValueError: 图中存在环，不存在拓扑序
    """
    indegree = {node: 0 for node in graph}
    for neighbors in graph.values():
        for nxt in neighbors:
            # 后继节点可能没在自己的键上出现（出度为 0 的节点）
            indegree[nxt] = indegree.get(nxt, 0) + 1

    queue = deque(node for node in graph if indegree[node] == 0)
    order: list = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph.get(node, []):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(order) != len(indegree):
        raise ValueError("图中存在环，不存在拓扑序")
    return order


def topological_sort_dfs(graph: dict) -> list | None:
    """DFS 后序反转求拓扑序；存在环时返回 None。

    >>> dag = {"A": ["C"], "B": ["C", "D"], "C": ["E"], "D": ["E"], "E": []}
    >>> topological_sort_dfs(dag)
    ['B', 'D', 'A', 'C', 'E']
    >>> topological_sort_dfs({"A": ["B"], "B": ["A"]}) is None
    True
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    for neighbors in graph.values():
        for nxt in neighbors:
            color.setdefault(nxt, WHITE)

    order: list = []
    has_cycle = False

    def visit(node) -> None:
        nonlocal has_cycle
        color[node] = GRAY  # 进入：在当前 DFS 路径上
        for nxt in graph.get(node, []):
            if color[nxt] == GRAY:  # 撞到路径上的节点 => 有环
                has_cycle = True
                return
            if color[nxt] == WHITE:
                visit(nxt)
                if has_cycle:
                    return
        color[node] = BLACK  # 离开：彻底完成
        order.append(node)

    for node in graph:
        if color[node] == WHITE:
            visit(node)
            if has_cycle:
                return None
    return order[::-1]  # 后序反转即为拓扑序
