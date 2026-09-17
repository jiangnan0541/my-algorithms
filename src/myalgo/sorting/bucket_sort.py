"""桶排序（Bucket Sort）。

思路：把值域 [min, max] 均分成 k 个桶，元素按值落进对应桶；
每个桶内部单独排序（这里用插入排序，桶小所以很快）；最后按桶序拼接。

时间复杂度：平均 O(n + k)（元素均匀分布时），最坏 O(n^2)
        （全部元素挤进同一个桶，退化成桶内插入排序）
空间复杂度：O(n + k)

特点：稳定（前提是桶内排序稳定，本实现的插入排序稳定）。
    和计数排序的区别：计数排序每格只存计数，桶排序每格存元素列表，
    因此能处理浮点数。

注：桶内排序内联了插入排序的几行，避免跨文件 import，
    保持"单个文件复制出去就能跑"的官方风格。
"""

from __future__ import annotations

from typing import Sequence


def bucket_sort(items: Sequence[float], bucket_count: int | None = None) -> list:
    """返回 items 升序排序后的**新列表**（不修改入参）。支持整数与浮点数。

    bucket_count 缺省取元素个数；传 1 可强制退化成"全塞一个桶"。

    >>> bucket_sort([0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51])
    [0.32, 0.33, 0.37, 0.42, 0.47, 0.51, 0.52]
    >>> bucket_sort([])
    []
    >>> bucket_sort([1])
    [1]
    >>> bucket_sort([2, 2, 2])
    [2, 2, 2]
    >>> bucket_sort([-5, 3, -1, 0])
    [-5, -1, 0, 3]
    """
    data = list(items)
    if len(data) <= 1:
        return data

    low, high = min(data), max(data)
    if low == high:
        return data

    if bucket_count is None:
        bucket_count = len(data)
    width = (high - low) / bucket_count

    buckets: list[list] = [[] for _ in range(bucket_count)]
    for x in data:
        idx = int((x - low) / width)
        if idx >= bucket_count:  # 最大值正好落在右边界
            idx = bucket_count - 1
        buckets[idx].append(x)

    out: list = []
    for bucket in buckets:
        # 桶内插入排序（内联版本）
        for i in range(1, len(bucket)):
            current = bucket[i]
            j = i - 1
            while j >= 0 and bucket[j] > current:
                bucket[j + 1] = bucket[j]
                j -= 1
            bucket[j + 1] = current
        out.extend(bucket)
    return out
