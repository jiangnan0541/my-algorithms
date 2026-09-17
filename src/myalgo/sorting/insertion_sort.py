"""插入排序（Insertion Sort）。

思路：把数组看成「已排序前缀 + 未排序后缀」，每次取后缀第一个元素，
在有序前缀里从后往前找到插入位置。等价于整理扑克牌。

时间复杂度：平均/最坏 O(n^2)，最好 O(n)（已有序）
空间复杂度：O(1)（原地，在副本上做）

特点：n 很小时常数极小，实践中是很多库对小数组的默认排序；
    稳定排序。
"""

from __future__ import annotations

from typing import Sequence


def insertion_sort(items: Sequence) -> list:
    """返回 items 升序排序后的**新列表**（不修改入参）。

    >>> insertion_sort([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    >>> insertion_sort([])
    []
    >>> insertion_sort([1])
    [1]
    >>> insertion_sort([2, 2, 2])
    [2, 2, 2]
    >>> insertion_sort([7, 6, 5, 4, 3])
    [3, 4, 5, 6, 7]
    """
    data = list(items)
    for i in range(1, len(data)):
        current = data[i]
        j = i - 1
        # 比 current 大的元素统一右移一格
        while j >= 0 and data[j] > current:
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = current
    return data
