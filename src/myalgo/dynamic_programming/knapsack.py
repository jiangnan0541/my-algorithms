"""0/1 背包（0/1 Knapsack）。

思路：dp[j] 表示容量 j 下能装的最大价值。倒序遍历容量，
保证每件物品只被选一次。

状态转移：dp[j] = max(dp[j], dp[j - w] + v)

时间复杂度：O(n * capacity)
空间复杂度：O(capacity)（滚动数组优化）
"""

from __future__ import annotations


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """返回 0/1 背包在给定容量下的最大总价值。

    >>> knapsack_01([2, 3, 4], [3, 4, 5], 5)
    7
    >>> knapsack_01([], [], 10)
    0
    >>> knapsack_01([5], [10], 4)   # 装不下
    0
    """
    if len(weights) != len(values):
        raise ValueError("weights 与 values 长度必须一致")
    if capacity < 0:
        raise ValueError("capacity 不能为负")

    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for j in range(capacity, w - 1, -1):
            dp[j] = max(dp[j], dp[j - w] + v)
    return dp[capacity]
