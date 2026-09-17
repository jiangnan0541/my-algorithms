"""矩阵连乘（Matrix Chain Order / 最优加括号）。

给定矩阵链 A1 A2 ... An 的维度序列 dims（Ai 的维度是 dims[i-1] x dims[i]），
矩阵乘法满足结合律但不满足交换律，不同的加括号方式计算量差别巨大。
求**最少标量乘法次数**以及对应的加括号方案。

状态：dp[i][j] = 计算 Ai..Aj 的最少乘法次数
转移：dp[i][j] = min over k in [i, j) of
          dp[i][k] + dp[k+1][j] + dims[i-1] * dims[k] * dims[j]
边界：dp[i][i] = 0

时间复杂度：O(n^3)
空间复杂度：O(n^2)

例：dims = [10, 30, 5, 60]
    ((A1A2)A3) = 10*30*5 + 10*5*60 = 1500 + 3000 = 4500
    (A1(A2A3)) = 30*5*60 + 10*30*60 = 9000 + 18000 = 27000
    最优 4500。
"""

from __future__ import annotations

from typing import Sequence

INF = float("inf")


def matrix_chain_order(dims: Sequence[int]) -> tuple[int, str]:
    """返回 (最少乘法次数, 加括号表达式)。

    >>> matrix_chain_order([10, 30, 5, 60])
    (4500, '((A1A2)A3)')
    >>> matrix_chain_order([40, 20, 30, 10, 30])
    (26000, '((A1(A2A3))A4)')
    >>> matrix_chain_order([10, 20])
    (0, '(A1)')
    >>> matrix_chain_order([10])
    (0, '(A1)')
    """
    n = len(dims) - 1  # 矩阵个数
    if n <= 1:
        return 0, "(A1)"

    # dp[i][j] 用 1-based 下标，对应 Ai..Aj
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    split = [[0] * (n + 1) for _ in range(n + 1)]

    # 按链长 len = 2..n 递推
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = INF
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

    def build(i: int, j: int) -> str:
        if i == j:
            return f"A{i}"
        k = split[i][j]
        return f"({build(i, k)}{build(k + 1, j)})"

    return dp[1][n], build(1, n)
