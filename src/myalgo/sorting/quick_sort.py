"""快速排序（Quick Sort）。

思路：选一个基准值 pivot，把数组分成「小于 pivot」和「大于 pivot」两半，
递归排序两半后拼接。

时间复杂度：平均 O(n log n)，最坏 O(n^2)（数组已有序且基准取端点时）
空间复杂度：O(log n)（递归栈，原地分区版本）

本文件是「样板实现」——后续每加一个算法都按这个格式写：
模块 docstring 说明思路 + 复杂度，函数 docstring 用 doctest 写用例。
"""

from __future__ import annotations

from typing import Sequence


def quick_sort(items: Sequence) -> list:
    """返回 items 升序排序后的**新列表**（不修改入参）。

    >>> quick_sort([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    >>> quick_sort([])
    []
    >>> quick_sort([1])
    [1]
    >>> quick_sort([2, 2, 2])
    [2, 2, 2]
    """
    data = list(items)
    if len(data) <= 1:
        return data

    pivot = data[len(data) // 2]
    smaller = [x for x in data if x < pivot]
    equal = [x for x in data if x == pivot]
    larger = [x for x in data if x > pivot]
    return quick_sort(smaller) + equal + quick_sort(larger)
