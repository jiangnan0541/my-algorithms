"""深度优先搜索（Depth-First Search, DFS）。

图用邻接表表示：``{节点: [邻居, ...]}``（与 `bfs.py` 保持同一套表示法）。

两种写法：
- ``dfs_order`` —— 显式栈迭代版，不会触发递归深度上限，工程上更可取。
  为保证"先左后右"的访问顺序，入栈时要**逆序**压入邻居。
- ``dfs_order_recursive`` —— 递归版，直观但不适用于深图
  （Python 默认递归上限 1000）。

时间复杂度：O(V + E)
空间复杂度：O(V)

DFS 与 BFS 的区别：BFS 按层扩散、天然给出无权最短路；DFS 沿一条路走到底，
适合判连通性、判环、拓扑排序、求强连通分量。
"""

from __future__ import annotations


def dfs_order(graph: dict, start) -> list:
    """返回从 start 出发的 DFS 访问顺序。图中不存在 start 时返回 []。

    >>> g = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    >>> dfs_order(g, "A")
    ['A', 'B', 'D', 'C']
    >>> dfs_order(g, "Z")
    []
    >>> dfs_order({"A": []}, "A")
    ['A']
    """
    if start not in graph:
        return []

    visited = {start}
    order = []
    stack = [start]

    while stack:
        node = stack.pop()
        order.append(node)
        # 逆序压栈，弹出时才是原顺序
        for nxt in reversed(list(graph.get(node, []))):
            if nxt not in visited:
                visited.add(nxt)
                stack.append(nxt)
    return order


def dfs_order_recursive(graph: dict, start) -> list:
    """递归版 DFS 访问顺序，结果与 ``dfs_order`` 一致。

    >>> g = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    >>> dfs_order_recursive(g, "A")
    ['A', 'B', 'D', 'C']
    >>> dfs_order_recursive(g, "Z")
    []
    """
    if start not in graph:
        return []

    visited = set()
    order = []

    def visit(node) -> None:
        visited.add(node)
        order.append(node)
        for nxt in graph.get(node, []):
            if nxt not in visited:
                visit(nxt)

    visit(start)
    return order


def connected_components(graph: dict) -> list[list]:
    """返回无向图的连通分量，每个分量是排序后的节点列表。

    图按**无向**处理：`u -> v` 与 `v -> u` 等价（邻接表不对称也会被补全）。
    节点需要可排序（int / str 均可，混合类型会 TypeError）。

    >>> connected_components({"A": ["B"], "B": [], "C": [], "D": ["C"]})
    [['A', 'B'], ['C', 'D']]
    >>> connected_components({})
    []
    """
    # 先补全反向边，构造无向邻接表
    adj: dict = {node: set() for node in graph}
    for node, neighbors in graph.items():
        for nxt in neighbors:
            adj[node].add(nxt)
            adj.setdefault(nxt, set()).add(node)

    seen: set = set()
    components: list[list] = []
    for node in adj:
        if node in seen:
            continue
        stack = [node]
        seen.add(node)
        group = []
        while stack:
            cur = stack.pop()
            group.append(cur)
            for nxt in adj[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        components.append(sorted(group))
    return components
