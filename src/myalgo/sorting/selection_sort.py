"""选择排序（Selection Sort）。

思路：每轮在未排序区间里找最小值，与区间首位交换。交换次数固定为
最多 n-1 次（这是它相对冒泡的唯一优势：写操作少）。

时间复杂度：O(n^2)（无论输入如何，比较次数恒定）
空间复杂度：O(1)（原地，在副本上做）

注：不稳定。例如 [2, 2, 1]，第一轮把 1 与首个 2 交换后，
两个 2 的相对顺序被打乱。
"""

from __future__ import annotations

from typing import Sequence


def selection_sort(items: Sequence) -> list:
    """返回 items 升序排序后的**新列表**（不修改入参）。

    >>> selection_sort([3, 1, 4, 1, 5, 9, 2, 6])
    [1, 1, 2, 3, 4, 5, 6, 9]
    >>> selection_sort([])
    []
    >>> selection_sort([1])
    [1]
    >>> selection_sort([2, 2, 2])
    [2, 2, 2]
    >>> selection_sort([-3, 0, -7])
    [-7, -3, 0]
    """
    data = list(items)
    n = len(data)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
    return data
