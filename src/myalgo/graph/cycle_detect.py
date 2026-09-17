"""环检测（有向图 / 无向图）。

**有向图**用三色标记 DFS：
- WHITE 未访问，GRAY 在当前 DFS 路径上，BLACK 已完成
- 顺着边走到一个 GRAY 节点 => 撞回自己的路径 => 有环
- 走到 BLACK 节点是安全的（那是另一条已探完的路径）

**无向图**只需记录父节点：DFS 时遇到已访问且**不是父亲**的邻居即有环。
（无向图里每条边会被看到两次，不排掉父节点会把正常的往返边误判成环。）

时间复杂度：O(V + E)
空间复杂度：O(V)

为什么不能用有向图那套跑无向图：无向图中 A-B 一条边双向可见，
会被当成 A->B->A 的环，全图都会被判有环。
"""

from __future__ import annotations

WHITE, GRAY, BLACK = 0, 1, 2


def _build_colors(graph: dict) -> dict:
    """所有出现过的节点都初始化为 WHITE（包括只作为邻居出现、没有出边的）。"""
    color = {node: WHITE for node in graph}
    for neighbors in graph.values():
        for nxt in neighbors:
            color.setdefault(nxt, WHITE)
    return color


def has_cycle_directed(graph: dict) -> bool:
    """判断有向图是否有环。邻接表 ``{节点: [后继, ...]}``。

    >>> has_cycle_directed({"A": ["B"], "B": ["C"], "C": []})
    False
    >>> has_cycle_directed({"A": ["B"], "B": ["A"]})
    True
    >>> has_cycle_directed({"A": ["A"]})
    True
    >>> has_cycle_directed({})
    False
    >>> has_cycle_directed({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []})
    False
    """
    color = _build_colors(graph)

    def visit(node) -> bool:
        color[node] = GRAY
        for nxt in graph.get(node, []):
            if color[nxt] == GRAY:
                return True
            if color[nxt] == WHITE and visit(nxt):
                return True
        color[node] = BLACK
        return False

    return any(color[node] == WHITE and visit(node) for node in list(color))


def find_cycle_directed(graph: dict) -> list | None:
    """返回有向图中的**一个**环（形如 ['A', 'B', 'C', 'A']）；无环返回 None。

    >>> find_cycle_directed({"A": ["B"], "B": ["C"], "C": ["A"]})
    ['A', 'B', 'C', 'A']
    >>> find_cycle_directed({"A": ["B", "C"], "B": [], "C": []}) is None
    True
    """
    color = _build_colors(graph)
    path: list = []

    def visit(node) -> list | None:
        color[node] = GRAY
        path.append(node)
        for nxt in graph.get(node, []):
            if color[nxt] == GRAY:
                # 从路径中 nxt 第一次出现的位置截到当前，再补上 nxt 闭环
                return path[path.index(nxt):] + [nxt]
            if color[nxt] == WHITE:
                found = visit(nxt)
                if found is not None:
                    return found
        color[node] = BLACK
        path.pop()
        return None

    for node in list(color):
        if color[node] == WHITE:
            found = visit(node)
            if found is not None:
                return found
    return None


def has_cycle_undirected(graph: dict) -> bool:
    """判断无向图是否有环。

    邻接表必须按无向图的规矩写：**每条边两个方向都要出现**。
    因此 ``{"B": ["C"], "C": ["B"]}`` 只是同一条边 B-C，不构成环。

    >>> has_cycle_undirected({"A": ["B", "C"], "B": ["A"], "C": ["A"]})
    False
    >>> has_cycle_undirected({"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]})
    True
    >>> has_cycle_undirected({"A": []})
    False
    >>> has_cycle_undirected({"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"]})
    False
    """
    visited: set = set()

    def visit(node, parent) -> bool:
        visited.add(node)
        for nxt in graph.get(node, []):
            if nxt not in visited:
                if visit(nxt, node):
                    return True
            elif nxt != parent:
                # 已访问、又不是来的方向 => 撞上另一条路径 => 有环
                return True
        return False

    for node in graph:
        if node not in visited and visit(node, None):
            return True
    return False
