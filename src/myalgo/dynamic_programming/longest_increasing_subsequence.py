"""最长递增子序列（Longest Increasing Subsequence, LIS）。

子序列不要求连续。提供两种解法：

1. ``lis_length`` —— **贪心 + 二分**，O(n log n)。
   维护 tails[k] = 所有长度为 k+1 的递增子序列中，**结尾最小值**。
   tails 本身单调递增，所以可以二分查找插入位置。
   注意 tails 不是某条真实的 LIS，只是"结束元素的最小值"这个记账表。

2. ``lis_sequence`` —— O(n^2) 标准 DP + 前驱指针，用来还原具体序列。
   两种实现在 ``tests/`` 里互相随机对拍（长度必须一致）。

时间复杂度：lis_length O(n log n)；lis_sequence O(n^2)
空间复杂度：lis_length O(n)；lis_sequence O(n)

严格递增：相等元素不算递增。
"""

from __future__ import annotations

from bisect import bisect_left
from typing import Sequence


def lis_length(nums: Sequence[int]) -> int:
    """返回最长**严格**递增子序列的长度。

    >>> lis_length([10, 9, 2, 5, 3, 7, 101, 18])
    4
    >>> lis_length([3, 3, 3])
    1
    >>> lis_length([])
    0
    >>> lis_length([1])
    1
    >>> lis_length([5, 4, 3, 2, 1])
    1
    """
    tails: list[int] = []
    for x in nums:
        pos = bisect_left(tails, x)  # 严格递增 => 找第一个 >= x 的位置
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x
    return len(tails)


def lis_sequence(nums: Sequence[int]) -> list[int]:
    """返回一个最长**严格**递增子序列本身。

    等长解可能不止一个，本实现按下标扫描顺序取到哪一个就返回哪一个，
    不保证是字典序最小或元素和最小的那个。例如下面这个输入长度为 4 的
    解至少有 [2, 3, 7, 18] 和 [2, 5, 7, 101] 两个，本实现返回后者。
    测试里断言的是「长度正确 + 确实递增 + 确实是 nums 的子序列」，
    而不是硬编码某一个具体答案。

    >>> lis_sequence([10, 9, 2, 5, 3, 7, 101, 18])
    [2, 5, 7, 101]
    >>> lis_sequence([3, 3, 3])
    [3]
    >>> lis_sequence([])
    []
    """
    if not nums:
        return []

    n = len(nums)
    dp = [1] * n
    prev = [-1] * n
    best = 0

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
        if dp[i] > dp[best]:
            best = i

    # 沿前驱指针回溯
    out: list[int] = []
    node: int | None = best
    while node is not None and node >= 0:
        out.append(nums[node])
        node = prev[node]
    return out[::-1]
