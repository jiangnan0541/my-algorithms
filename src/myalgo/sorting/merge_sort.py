"""归并排序（Merge Sort）。

思路：分治 —— 把数组对半切到底（单元素天然有序），再两两合并两个
有序数组（双指针取小）。

时间复杂度：O(n log n)（最好/平均/最坏都一样，这是它相对快排的稳定性优势）
空间复杂度：O(n)（合并需要额外数组）

特点：稳定排序；天然适合外部排序（数据放不下内存时按块归并）。
"""

from __future__ import annotations

from typing import Sequence


def _merge(left: list, right: list) -> list:
    """合并两个有序列表，返回新的有序列表。"""
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        # 用 <= 保证稳定性：相等时先取左半边的元素
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(items: Sequence) -> list:
    """返回 items 升序排序后的**新列表**（不修改入参）。

    >>> merge_sort([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    >>> merge_sort([])
    []
    >>> merge_sort([1])
    [1]
    >>> merge_sort([2, 2, 2])
    [2, 2, 2]
    >>> merge_sort([9, 8, 7, 6, 5])
    [5, 6, 7, 8, 9]
    """
    data = list(items)
    if len(data) <= 1:
        return data

    mid = len(data) // 2
    return _merge(merge_sort(data[:mid]), merge_sort(data[mid:]))
