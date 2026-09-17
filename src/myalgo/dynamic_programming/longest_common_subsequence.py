"""最长公共子序列（Longest Common Subsequence, LCS）。

注意区分「子序列」（可不连续）与「子串」（必须连续）—— 本题是子序列。

状态：dp[i][j] = a 的前 i 个字符与 b 的前 j 个字符的 LCS 长度
转移：
    a[i-1] == b[j-1] -> dp[i][j] = dp[i-1][j-1] + 1
    否则             -> dp[i][j] = max(dp[i-1][j], dp[i][j-1])

时间复杂度：O(m * n)
空间复杂度：O(m * n)（要还原具体序列必须留整表；只要长度可滚动数组降到 O(min(m,n))）

经典应用：git diff、DNA 序列比对、拼写纠错。
"""

from __future__ import annotations


def _dp_table(a: str, b: str) -> list[list[int]]:
    """构造 LCS 长度表，dp[i][j] 含义见模块 docstring。"""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def lcs_length(a: str, b: str) -> int:
    """返回 a 与 b 的最长公共子序列长度。

    >>> lcs_length("ABCBDAB", "BDCABA")
    4
    >>> lcs_length("abc", "abc")
    3
    >>> lcs_length("abc", "xyz")
    0
    >>> lcs_length("", "abc")
    0
    """
    if not a or not b:
        return 0
    return _dp_table(a, b)[len(a)][len(b)]


def lcs_string(a: str, b: str) -> str:
    """返回 a 与 b 的**一个**最长公共子序列（存在多个时按回溯规则取其一）。

    >>> lcs_string("ABCBDAB", "BDCABA")
    'BCBA'
    >>> lcs_string("abc", "xyz")
    ''
    >>> lcs_string("", "abc")
    ''
    """
    if not a or not b:
        return ""

    dp = _dp_table(a, b)
    i, j = len(a), len(b)
    chars: list[str] = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(chars))
