"""斐波那契数列（迭代 DP 版）。

定义：F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2)

朴素递归是 O(2^n)（同一子问题被反复重算）。这里用**自底向上**的迭代：
只保留最近两个值，就把时间和空间都压到最优。

时间复杂度：O(n)
空间复杂度：O(1)

注：本模块演示 DP 里「滚动变量」的典型手法 —— 当状态转移只依赖前 k 项时，
    不需要开长度为 n 的数组。大 n 结果会溢出普通浮点，Python 整数不受限。
"""

from __future__ import annotations


def fibonacci_dp(n: int) -> int:
    """返回第 n 个斐波那契数（F(0) = 0）。n 为负时抛 ValueError。

    >>> fibonacci_dp(0)
    0
    >>> fibonacci_dp(1)
    1
    >>> fibonacci_dp(10)
    55
    >>> fibonacci_dp(30)
    832040
    """
    if n < 0:
        raise ValueError("n 必须是非负整数")
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def fibonacci_sequence(count: int) -> list[int]:
    """返回前 count 个斐波那契数。count 为负时抛 ValueError。

    >>> fibonacci_sequence(0)
    []
    >>> fibonacci_sequence(1)
    [0]
    >>> fibonacci_sequence(8)
    [0, 1, 1, 2, 3, 5, 8, 13]
    """
    if count < 0:
        raise ValueError("count 必须是非负整数")
    out = []
    a, b = 0, 1
    for _ in range(count):
        out.append(a)
        a, b = b, a + b
    return out
