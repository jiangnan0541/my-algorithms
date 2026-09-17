"""堆排序（Heap Sort）。

思路：先把数组整理成**大顶堆**（自底向上 sift-down 建堆），然后反复
把堆顶（当前最大值）换到数组末尾，堆规模减一，再对新堆顶做 sift-down。

时间复杂度：O(n log n)（建堆 O(n) + n 次 sift-down 各 O(log n)）
空间复杂度：O(1)（完全原地，在副本上做）

特点：不稳定；最坏情况仍 O(n log n)，且不需要归并排序那 O(n) 的额外空间。
数组下标从 0 开始，节点 i 的孩子为 2i+1 和 2i+2。
"""

from __future__ import annotations

from typing import Sequence


def _sift_down(data: list, start: int, end: int) -> None:
    """把 data[start] 下沉，使 data[start:end+1] 恢复大顶堆性质。"""
    root = start
    while True:
        child = 2 * root + 1
        if child > end:
            return
        # 选两个孩子里较大的那个
        if child + 1 <= end and data[child + 1] > data[child]:
            child += 1
        if data[root] >= data[child]:
            return
        data[root], data[child] = data[child], data[root]
        root = child


def heap_sort(items: Sequence) -> list:
    """返回 items 升序排序后的**新列表**（不修改入参）。

    >>> heap_sort([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    >>> heap_sort([])
    []
    >>> heap_sort([1])
    [1]
    >>> heap_sort([2, 2, 2])
    [2, 2, 2]
    >>> heap_sort([-1, -5, 3])
    [-5, -1, 3]
    """
    data = list(items)
    n = len(data)

    # 建堆：从最后一个非叶子节点开始下沉
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(data, i, n - 1)

    # 逐个把堆顶最大值换到末尾
    for end in range(n - 1, 0, -1):
        data[0], data[end] = data[end], data[0]
        _sift_down(data, 0, end - 1)
    return data
