"""冒泡排序（Bubble Sort）。

思路：每轮从前往后两两比较相邻元素，逆序就交换，一轮结束最大的元素
"冒"到末尾。加一个 early-exit：某轮没有发生交换说明已有序，直接退出。

时间复杂度：平均/最坏 O(n^2)，最好 O(n)（已有序 + early-exit）
空间复杂度：O(1)（原地交换，在副本上做）

注：官方 `sorts/bubble_sort.py` 用的是双层 for 且无 early-exit，
本实现补上提前退出，已有序输入从 O(n^2) 降到 O(n)。
"""

from __future__ import annotations

from typing import Sequence


def bubble_sort(items: Sequence) -> list:
    """返回 items 升序排序后的**新列表**（不修改入参）。

    >>> bubble_sort([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    >>> bubble_sort([])
    []
    >>> bubble_sort([1])
    [1]
    >>> bubble_sort([2, 2, 2])
    [2, 2, 2]
    >>> bubble_sort([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    """
    data = list(items)
    n = len(data)
    for i in range(n - 1):
        swapped = False
        # 后 i 个元素已经就位，只需扫到 n-1-i
        for j in range(n - 1 - i):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
        if not swapped:
            break
    return data
