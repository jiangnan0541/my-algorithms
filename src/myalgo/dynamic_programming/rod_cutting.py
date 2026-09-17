"""钢条切割（Rod Cutting）。

一根长 n 的钢条，长度 i 的整段售价为 prices[i-1]（i = 1..len(prices)）。
可以任意切成整数段出售，求最大收益。

状态：dp[i] = 长度 i 的钢条能获得的最大收益
转移：dp[i] = max over 1 <= j <= i of (prices[j-1] + dp[i-j])
边界：dp[0] = 0

时间复杂度：O(n^2)
空间复杂度：O(n)

这是「完全背包」的另一种写法：把钢条看作容量 n 的背包，
每段长度 j 是重量、售价是价值，每种长度可取无限次。
"""

from __future__ import annotations

from typing import Sequence


def _cut_plan(prices: Sequence[int], n: int, dp: list[int]) -> list[int]:
    """根据 dp 表回溯出一个取得最大收益的切割方案（各段长度）。"""
    plan: list[int] = []
    rest = n
    while rest > 0:
        for j in range(1, rest + 1):
            if prices[j - 1] + dp[rest - j] == dp[rest]:
                plan.append(j)
                rest -= j
                break
    return plan


def rod_cutting(prices: Sequence[int], n: int) -> int:
    """返回长度 n 的钢条能获得的最大收益。n 超出 prices 覆盖范围时抛 ValueError。

    >>> rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 8)
    22
    >>> rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 4)
    10
    >>> rod_cutting([1, 5, 8, 9, 10, 17, 17, 20], 0)
    0
    >>> rod_cutting([3, 4], 2)
    6
    >>> rod_cutting([1, 5, 8, 9, 10, 17, 17, 20, 24, 30], 10)
    30
    >>> rod_cutting([2], 3)
    Traceback (most recent call last):
        ...
    ValueError: prices 只覆盖到长度 1，无法处理 n=3
    """
    if n < 0:
        raise ValueError("n 必须是非负整数")
    if n > len(prices):
        raise ValueError(f"prices 只覆盖到长度 {len(prices)}，无法处理 n={n}")

    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        best = 0
        for j in range(1, i + 1):
            candidate = prices[j - 1] + dp[i - j]
            if candidate > best:
                best = candidate
        dp[i] = best
    return dp[n]


def rod_cutting_with_plan(prices: Sequence[int], n: int) -> tuple[int, list[int]]:
    """返回 (最大收益, 切割方案)。方案里各段长度之和为 n。

    >>> rod_cutting_with_plan([1, 5, 8, 9, 10, 17, 17, 20], 8)
    (22, [2, 6])
    >>> rod_cutting_with_plan([1, 5, 8], 0)
    (0, [])
    """
    if n < 0:
        raise ValueError("n 必须是非负整数")
    if n > len(prices):
        raise ValueError(f"prices 只覆盖到长度 {len(prices)}，无法处理 n={n}")

    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = max(prices[j - 1] + dp[i - j] for j in range(1, i + 1))
    return dp[n], _cut_plan(prices, n, dp)
