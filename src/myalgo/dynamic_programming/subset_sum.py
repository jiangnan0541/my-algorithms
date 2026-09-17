"""子集和问题（Subset Sum）。

给定非负整数集合 nums 与目标 target，判断是否存在一个子集其和恰好为 target。

状态：dp[s] = 能否凑出和 s
转移：dp[s] = dp[s] or dp[s - x]（对每个 x，且 s >= x）
边界：dp[0] = True（空集和为 0）

时间复杂度：O(n * target)
空间复杂度：O(target)（滚动一维；注意内层必须**逆序**遍历，
        否则同一个数会被用多次，那就退化成「完全背包」了）

注：这是 0/1 背包的判定版（价值和重量相同），也是 Partition Equal
    Subset Sum 的核心子过程。
"""

from __future__ import annotations

from typing import Sequence


def subset_sum(nums: Sequence[int], target: int) -> bool:
    """判断 nums 中是否存在子集和为 target。

    >>> subset_sum([3, 34, 4, 12, 5, 2], 9)
    True
    >>> subset_sum([3, 34, 4, 12, 5, 2], 30)
    False
    >>> subset_sum([], 0)
    True
    >>> subset_sum([1], 0)
    True
    >>> subset_sum([], 5)
    False
    >>> subset_sum([2, 3], 5)
    True
    """
    if target < 0:
        return False

    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        if x < 0:
            continue  # 本题限定非负整数
        for s in range(target, x - 1, -1):  # 逆序，保证每个数只用一次
            if dp[s - x]:
                dp[s] = True
    return dp[target]


def partition_equal(nums: Sequence[int]) -> bool:
    """判断能否把 nums 分成两个和相等的子集。

    >>> partition_equal([1, 5, 11, 5])
    True
    >>> partition_equal([1, 2, 3, 5])
    False
    >>> partition_equal([])
    True
    """
    total = sum(nums)
    if total % 2:
        return False
    return subset_sum(nums, total // 2)
