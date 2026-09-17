"""基数排序（Radix Sort, LSD）。

思路：从最低位（个位）开始，按当前位做一轮**稳定**的桶分配，
依次推进到最高位。因为每轮都稳定，低位排好的相对顺序会被保留，
最高位跑完整体就有序了。

时间复杂度：O(d * (n + k))，d 为最大位数、k 为基数（这里 10）
空间复杂度：O(n + k)

特点：非比较排序；负数处理方式是把符号位单独拿出来 —— 负数按绝对值排序后
反转并取负，再接上非负数部分。

注：官方 `sorts/radix_sort.py` 只处理非负整数，本实现补齐负数分支。
"""

from __future__ import annotations

from typing import Sequence


def _radix_sort_non_negative(data: list[int]) -> list[int]:
    """对非负整数列表做 LSD 基数排序（10 进制）。"""
    if not data:
        return []
    max_value = max(data)
    exp = 1
    out = list(data)
    while max_value // exp > 0:
        buckets: list[list[int]] = [[] for _ in range(10)]
        for x in out:
            buckets[(x // exp) % 10].append(x)
        out = [x for bucket in buckets for x in bucket]
        exp *= 10
    return out


def radix_sort(items: Sequence[int]) -> list[int]:
    """返回 items 升序排序后的**新列表**（不修改入参）。仅支持整数。

    >>> radix_sort([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    >>> radix_sort([])
    []
    >>> radix_sort([1])
    [1]
    >>> radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
    [2, 24, 45, 66, 75, 90, 170, 802]
    >>> radix_sort([-5, 3, -1, 0])
    [-5, -1, 0, 3]
    """
    data = list(items)
    if len(data) <= 1:
        return data

    negatives = [x for x in data if x < 0]
    non_negatives = [x for x in data if x >= 0]

    # 负数：按绝对值升序后反转取负，就得到升序的负数序列
    sorted_negatives = [-x for x in reversed(_radix_sort_non_negative([-x for x in negatives]))]
    return sorted_negatives + _radix_sort_non_negative(non_negatives)
