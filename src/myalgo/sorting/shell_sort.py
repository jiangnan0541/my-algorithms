"""希尔排序（Shell Sort）。

思路：插入排序的改进版。先用较大步长 gap 把数组分成分散的子序列做
插入排序，让元素能"大步跳"到大致位置；gap 逐步折半直到 1，
最后退化成一次普通插入排序 —— 但此时数组已**基本有序**，
插入排序在近似有序输入上是 O(n) 的。

时间复杂度：取决于增量序列。折半序列（n/2, n/4, ..., 1）最坏 O(n^2)，
        平均约 O(n^1.3)；Hibbard / Sedgewick 序列可到 O(n^1.5) 以下
空间复杂度：O(1)

特点：不稳定；代码改动量小（插入排序加一个 gap 循环），实战中中等规模
    数据上常比 O(n log n) 的算法还快，因为无递归、常数小。
"""

from __future__ import annotations

from typing import Sequence


def shell_sort(items: Sequence) -> list:
    """返回 items 升序排序后的**新列表**（不修改入参）。

    >>> shell_sort([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    >>> shell_sort([])
    []
    >>> shell_sort([1])
    [1]
    >>> shell_sort([2, 2, 2])
    [2, 2, 2]
    >>> shell_sort([9, 8, 7, 6, 5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    data = list(items)
    n = len(data)
    gap = n // 2
    while gap > 0:
        # 对每个步长为 gap 的子序列做插入排序
        for i in range(gap, n):
            current = data[i]
            j = i
            while j >= gap and data[j - gap] > current:
                data[j] = data[j - gap]
                j -= gap
            data[j] = current
        gap //= 2
    return data
