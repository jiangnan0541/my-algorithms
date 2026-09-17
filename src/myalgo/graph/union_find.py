"""并查集（Disjoint Set Union / Union-Find）。

维护若干个互不相交的集合，支持近似 O(1) 的合并与查询：

- ``find(x)`` —— 找 x 所在集合的代表元（树根）
- ``union(a, b)`` —— 合并两个集合，返回是否真的发生了合并
- ``connected(a, b)`` —— 两者是否同属一个集合

两个关键优化：
1. **路径压缩**：find 时把沿途节点直接挂到根上，后续查询变成一步。
2. **按秩合并**（这里用按大小合并）：小树挂到大树上，避免长成链。

时间复杂度：单次操作近似 O(α(n))（α 是反阿克曼函数，n < 10^600 时 α <= 4，
        实际可视为常数）；不做优化最坏是 O(n)
空间复杂度：O(n)

应用：Kruskal 求最小生成树、动态连通性、判断无向图是否成环、
     图像处理里的连通区域标记。

注：官方对应文件在 `data_structures/disjoint_set/disjoint_set.py`，
    不在我们三个目标目录内 —— 但它是 Kruskal 的前置，所以一并手写。
"""

from __future__ import annotations


class UnionFind:
    """节点编号固定为 0..count-1 的并查集。

    >>> uf = UnionFind(5)
    >>> uf.component_count
    5
    >>> uf.union(0, 1)
    True
    >>> uf.connected(0, 1)
    True
    >>> uf.connected(0, 2)
    False
    >>> uf.union(0, 1)          # 已经连通，无事发生
    False
    >>> uf.union(2, 3)
    True
    >>> uf.union(0, 3)
    True
    >>> uf.component_count
    2
    >>> uf.size(3)
    4
    """

    def __init__(self, count: int) -> None:
        if count < 0:
            raise ValueError("count 必须是非负整数")
        self._parent = list(range(count))
        self._size = [1] * count
        self._count = count

    def __len__(self) -> int:
        return len(self._parent)

    @property
    def component_count(self) -> int:
        """当前连通分量个数。

        >>> UnionFind(3).component_count
        3
        """
        return self._count

    def find(self, x: int) -> int:
        """返回 x 的根节点，并顺路做路径压缩。

        >>> uf = UnionFind(4)
        >>> uf.union(0, 1)
        True
        >>> uf.union(1, 2)
        True
        >>> uf.find(2) == uf.find(0)
        True
        """
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        # 路径压缩：把 x 到根路径上的节点全部直接指向根
        while self._parent[x] != root:
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        """合并 a、b 所在集合；已在同一集合则返回 False。

        >>> uf = UnionFind(2)
        >>> uf.union(0, 1)
        True
        >>> uf.union(1, 0)
        False
        """
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # 按大小合并：小树挂到大树下面
        if self._size[ra] < self._size[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        self._size[ra] += self._size[rb]
        self._count -= 1
        return True

    def connected(self, a: int, b: int) -> bool:
        """判断 a、b 是否连通。

        >>> uf = UnionFind(3)
        >>> uf.connected(0, 2)
        False
        """
        return self.find(a) == self.find(b)

    def size(self, x: int) -> int:
        """返回 x 所在集合的元素个数。

        >>> uf = UnionFind(4)
        >>> uf.union(0, 1)
        True
        >>> uf.union(1, 2)
        True
        >>> uf.size(2)
        3
        """
        return self._size[self.find(x)]

    def groups(self) -> dict:
        """返回 ``{根节点: [成员, ...]}``。

        >>> UnionFind(3).groups()
        {0: [0], 1: [1], 2: [2]}
        """
        out: dict = {}
        for x in range(len(self._parent)):
            out.setdefault(self.find(x), []).append(x)
        return out
