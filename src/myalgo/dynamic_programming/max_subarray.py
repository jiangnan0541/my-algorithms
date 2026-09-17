"""最大子段和（Kadane 算法）。

给定整数数组，求**连续**子数组的最大和（子数组至少含一个元素）。

思路（Kadane）：
    cur = 以当前元素结尾的最大子段和
    cur = max(x, cur + x)   —— 要么另起一段，要么接上前一段
    best = max(best, cur)

时间复杂度：O(n)
空间复杂度：O(1)（只需两个变量）

关键点：全是负数时答案不是 0，而是最大的那个负数（子数组不能为空）。
"""

from __future__ import annotations

from typing import Sequence


def max_subarray(nums: Sequence[int]) -> int:
    """返回连续子数组的最大和；空数组返回 0。

    >>> max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    >>> max_subarray([1, 2, 3, 4])
    10
    >>> max_subarray([-1, -2, -3])
    -1
    >>> max_subarray([5])
    5
    >>> max_subarray([])
    0
    """
    if not nums:
        return 0

    best = cur = nums[0]
    for x in nums[1:]:
        cur = x if cur + x < x else cur + x
        if cur > best:
            best = cur
    return best


def max_subarray_range(nums: Sequence[int]) -> tuple[int, int, int]:
    """返回 (最大和, 起始下标, 结束下标) —— 左闭右闭；空数组返回 (0, -1, -1)。

    >>> max_subarray_range([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    (6, 3, 6)
    >>> max_subarray_range([-1, -2, -3])
    (-1, 0, 0)
    >>> max_subarray_range([])
    (0, -1, -1)
    """
    if not nums:
        return 0, -1, -1

    best = cur = nums[0]
    best_start = best_end = 0
    start = 0

    for i in range(1, len(nums)):
        if nums[i] > cur + nums[i]:
            cur = nums[i]
            start = i
        else:
            cur += nums[i]
        if cur > best:
            best = cur
            best_start, best_end = start, i
    return best, best_start, best_end
