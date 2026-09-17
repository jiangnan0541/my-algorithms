"""计数排序（Counting Sort）。

思路：**不是比较排序**。统计每个值出现的次数，再按值域从小到大回填。
下标从 0 开始，所以先减去最小值 offset 把值域平移成非负。

时间复杂度：O(n + k)，k 为值域宽度 max - min
空间复杂度：O(n + k)

特点：稳定（本实现按原顺序回填）；适合值域窄的整数集合
（比如年龄、成绩），值域极大时 k 会爆炸，反而不如 O(n log n) 的比较排序。
"""

from __future__ import annotations

from typing import Sequence


def counting_sort(items: Sequence[int]) -> list[int]:
    """返回 items 升序排序后的**新列表**（不修改入参）。仅支持整数。

    >>> counting_sort([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    >>> counting_sort([])
    []
    >>> counting_sort([1])
    [1]
    >>> counting_sort([2, 2, 2])
    [2, 2, 2]
    >>> counting_sort([-3, 5, -3, 0])
    [-3, -3, 0, 5]
    """
    data = list(items)
    if len(data) <= 1:
        return data

    offset = min(data)
    counts = [0] * (max(data) - offset + 1)
    for x in data:
        counts[x - offset] += 1

    out = []
    for i, count in enumerate(counts):
        if count:
            out.extend([i + offset] * count)
    return out
