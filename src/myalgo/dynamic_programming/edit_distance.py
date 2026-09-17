"""编辑距离 / Levenshtein 距离。

允许三种操作：插入一个字符、删除一个字符、替换一个字符。问把 word1
变成 word2 最少需要几步。

状态：dp[i][j] = word1 前 i 个字符变成 word2 前 j 个字符的最少操作数
边界：dp[i][0] = i（全删）、dp[0][j] = j（全插）
转移：
    w1[i-1] == w2[j-1] -> dp[i][j] = dp[i-1][j-1]                （不用动）
    否则 dp[i][j] = 1 + min(dp[i-1][j],      # 删
                            dp[i][j-1],      # 插
                            dp[i-1][j-1])    # 替换

时间复杂度：O(m * n)
空间复杂度：O(min(m, n))（滚动数组，只保留上一行）

应用：拼写纠错、模糊匹配、语音识别评估。
"""

from __future__ import annotations


def edit_distance(word1: str, word2: str) -> int:
    """返回 word1 变成 word2 的最少编辑操作次数。

    >>> edit_distance("kitten", "sitting")
    3
    >>> edit_distance("abc", "abc")
    0
    >>> edit_distance("", "abc")
    3
    >>> edit_distance("abc", "")
    3
    >>> edit_distance("flaw", "lawn")
    2
    """
    if word1 == word2:
        return 0
    if not word1:
        return len(word2)
    if not word2:
        return len(word1)

    # 让 word2 作为较短的维度，滚动数组只开 O(min(m, n))
    if len(word1) < len(word2):
        word1, word2 = word2, word1

    prev = list(range(len(word2) + 1))
    for i in range(1, len(word1) + 1):
        curr = [i] + [0] * len(word2)
        for j in range(1, len(word2) + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]
            else:
                curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
        prev = curr
    return prev[len(word2)]
