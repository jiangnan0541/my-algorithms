"""零钱兑换（最少硬币数）。

给定硬币面额集合 coins（每种数量无限）与目标金额 amount，求凑出该金额
所需的**最少硬币枚数**；凑不出返回 -1。

状态：dp[a] = 凑出金额 a 的最少枚数
转移：dp[a] = min(dp[a - c] + 1)，对所有 c in coins 且 c <= a
边界：dp[0] = 0，其余初始化为 amount + 1 作为「不可达」哨兵

时间复杂度：O(amount * len(coins))
空间复杂度：O(amount)

注：这是「完全背包」型。贪心（每次拿最大面额）是错的 ——
    例如 coins=[1, 3, 4]、amount=6，贪心给 4+1+1=3 枚，最优是 3+3=2 枚。
"""

from __future__ import annotations

from typing import Sequence


def coin_change(coins: Sequence[int], amount: int) -> int:
    """返回凑出 amount 的最少硬币数，无法凑出返回 -1。

    >>> coin_change([1, 2, 5], 11)
    3
    >>> coin_change([1, 3, 4], 6)
    2
    >>> coin_change([2], 3)
    -1
    >>> coin_change([5], 0)
    0
    >>> coin_change([], 5)
    -1
    """
    if amount < 0:
        return -1
    if amount == 0:
        return 0
    if not coins:
        return -1

    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for c in coins:
            if 0 < c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1

    return -1 if dp[amount] == unreachable else dp[amount]


def coin_change_ways(coins: Sequence[int], amount: int) -> int:
    """返回凑出 amount 的**组合数**（不同顺序算同一种，即组合不是排列）。

    >>> coin_change_ways([1, 2, 5], 5)
    4
    >>> coin_change_ways([2], 3)
    0
    >>> coin_change_ways([1], 0)
    1
    """
    if amount < 0:
        return 0

    dp = [0] * (amount + 1)
    dp[0] = 1
    # 外层遍历硬币、内层遍历金额 => 天然按组合计数，不会重复算排列
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]
