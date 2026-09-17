"""Kruskal 最小生成树（MST）。

输入：节点数 num_vertices + 无向边表 ``[(u, v, w), ...]``。

思路（贪心 + 并查集）：
1. 所有边按权值升序排序。
2. 依次考察每条边，若它连接的两个端点**尚不连通**就选入（并查集判环），
   否则丢弃（选它会成环）。
3. 选够 V-1 条边时结束。

正确性来自"割性质"：全局最小的可安全加入的边一定属于某棵 MST。

时间复杂度：O(E log E)（排序主导；并查集操作近似 O(1)）
空间复杂度：O(V + E)

注：图不连通时返回的是**最小生成森林**，总权值是各连通分量 MST 之和。
    本文件内联了一份最小并查集，保证单文件复制出去即可运行；
    完整版（带 sizes/groups 等接口）见同目录 `union_find.py`。
"""

from __future__ import annotations


class _DisjointSet:
    """Kruskal 内部用的极简并查集（路径压缩 + 按大小合并）。"""

    def __init__(self, count: int) -> None:
        self._parent = list(range(count))
        self._size = [1] * count

    def find(self, x: int) -> int:
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self._size[ra] < self._size[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        self._size[ra] += self._size[rb]
        return True


def kruskal(num_vertices: int, edges: list) -> tuple[int, list]:
    """返回 (最小生成森林总权值, 选中的边列表)。

    选中的边按被接受的先后顺序排列。节点编号需落在 0..num_vertices-1。

    >>> edges = [(0, 1, 1), (0, 2, 4), (0, 3, 3), (1, 2, 2), (2, 3, 5)]
    >>> kruskal(4, edges)
    (6, [(0, 1, 1), (1, 2, 2), (0, 3, 3)])
    >>> kruskal(1, [])
    (0, [])
    >>> kruskal(3, [(0, 1, 2)])      # 不连通：只连通了 0-1
    (2, [(0, 1, 2)])
    >>> kruskal(4, [(0, 1, 1), (0, 1, 1), (1, 2, 1), (0, 2, 5)])
    (2, [(0, 1, 1), (1, 2, 1)])
    """
    dsu = _DisjointSet(num_vertices)
    total = 0
    chosen: list = []

    # 按权值升序；相等时按 (u, v) 兜底，保证结果可复现
    for u, v, w in sorted(edges, key=lambda e: (e[2], e[0], e[1])):
        if dsu.union(u, v):
            total += w
            chosen.append((u, v, w))
            if len(chosen) == num_vertices - 1:
                break
    return total, chosen
