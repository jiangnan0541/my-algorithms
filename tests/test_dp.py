"""动态规划算法测试（含与暴力枚举的随机对拍）。"""

import itertools
import random

import pytest

from myalgo import dynamic_programming as dp


# ------------------------------------------------------------ LCS

@pytest.mark.parametrize(
    "a, b, expected",
    [
        ("ABCBDAB", "BDCABA", 4),
        ("abc", "abc", 3),
        ("abc", "xyz", 0),
        ("", "abc", 0),
        ("a", "", 0),
        ("a", "a", 1),
        ("aa", "aaaa", 2),
    ],
)
def test_lcs_length(a, b, expected):
    assert dp.lcs_length(a, b) == expected


@pytest.mark.parametrize("a, b", [("", "abc"), ("abc", ""), ("abc", "xyz")])
def test_lcs_string_empty_results(a, b):
    assert dp.lcs_string(a, b) == ""


def test_lcs_string_is_a_valid_common_subsequence():
    """返回的串必须同时是 a 和 b 的子序列，且长度等于 lcs_length。"""
    a, b = "ABCBDAB", "BDCABA"
    result = dp.lcs_string(a, b)
    assert len(result) == dp.lcs_length(a, b)

    def is_subsequence(short: str, long: str) -> bool:
        it = iter(long)
        return all(ch in it for ch in short)

    assert is_subsequence(result, a)
    assert is_subsequence(result, b)


# --------------------------------------------------------- 编辑距离

@pytest.mark.parametrize(
    "w1, w2, expected",
    [
        ("kitten", "sitting", 3),
        ("abc", "abc", 0),
        ("", "", 0),
        ("", "abc", 3),
        ("abc", "", 3),
        ("flaw", "lawn", 2),
        ("a", "b", 1),
        ("intention", "execution", 5),
    ],
)
def test_edit_distance(w1, w2, expected):
    assert dp.edit_distance(w1, w2) == expected


def test_edit_distance_is_symmetric():
    assert dp.edit_distance("kitten", "abc") == dp.edit_distance("abc", "kitten")


# ---------------------------------------------------------- 零钱兑换

@pytest.mark.parametrize(
    "coins, amount, expected",
    [
        ([1, 2, 5], 11, 3),
        ([1, 3, 4], 6, 2),
        ([2], 3, -1),
        ([5], 0, 0),
        ([], 5, -1),
        ([7], -1, -1),
        ([1], 1, 1),
        ([186, 419, 83, 408], 6249, 20),
    ],
)
def test_coin_change(coins, amount, expected):
    assert dp.coin_change(coins, amount) == expected


def test_coin_change_beats_greedy():
    """贪心（先拿最大面额）在 [1,3,4]/6 上给 3 枚，正确答案是 2 枚。"""
    greedy = 6 // 4 + (6 % 4) // 3 + (6 % 4 % 3)
    assert greedy == 3
    assert dp.coin_change([1, 3, 4], 6) == 2


@pytest.mark.parametrize(
    "coins, amount, expected",
    [([1, 2, 5], 5, 4), ([2], 3, 0), ([1], 0, 1), ([2, 3], 6, 2)],
)
def test_coin_change_ways(coins, amount, expected):
    assert dp.coin_change_ways(coins, amount) == expected


def test_coin_change_ways_negative_amount():
    assert dp.coin_change_ways([1, 2], -1) == 0


# -------------------------------------------------- 最长递增子序列

@pytest.mark.parametrize(
    "nums, expected",
    [
        ([10, 9, 2, 5, 3, 7, 101, 18], 4),
        ([3, 3, 3], 1),
        ([], 0),
        ([1], 1),
        ([5, 4, 3, 2, 1], 1),
        ([1, 2, 3, 4, 5], 5),
        ([0, 1, 0, 3, 2, 3], 4),
    ],
)
def test_lis_length(nums, expected):
    assert dp.lis_length(nums) == expected


def test_lis_sequence_is_valid():
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    seq = dp.lis_sequence(nums)
    assert len(seq) == dp.lis_length(nums)
    assert all(x < y for x, y in zip(seq, seq[1:]))
    it = iter(nums)
    assert all(x in it for x in seq)


# ------------------------------------------------------------ 矩阵连乘

def test_matrix_chain_order_known_values():
    assert dp.matrix_chain_order([10, 30, 5, 60]) == (4500, "((A1A2)A3)")
    assert dp.matrix_chain_order([10]) == (0, "(A1)")


def test_matrix_chain_order_beats_naive_parenthesization():
    """[10,30,5,60] 上 (A1(A2A3)) 要 27000 次，最优只要 4500 次。"""
    naive = 30 * 5 * 60 + 10 * 30 * 60
    best, _ = dp.matrix_chain_order([10, 30, 5, 60])
    assert naive == 27000
    assert best == 4500


# ------------------------------------------------------------ 最大子段和

@pytest.mark.parametrize(
    "nums, expected",
    [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1, 2, 3, 4], 10),
        ([-1, -2, -3], -1),
        ([5], 5),
        ([], 0),
        ([0, -1], 0),
        ([-1, 0], 0),
    ],
)
def test_max_subarray(nums, expected):
    assert dp.max_subarray(nums) == expected


def test_max_subarray_range_points_at_the_max_sum():
    nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    total, start, end = dp.max_subarray_range(nums)
    assert total == 6
    assert nums[start : end + 1] == [4, -1, 2, 1]
    assert sum(nums[start : end + 1]) == total


def test_max_subarray_range_on_empty():
    assert dp.max_subarray_range([]) == (0, -1, -1)


# -------------------------------------------------------------- 斐波那契

@pytest.mark.parametrize(
    "n, expected",
    [(0, 0), (1, 1), (2, 1), (10, 55), (30, 832040), (50, 12586269025)],
)
def test_fibonacci_dp(n, expected):
    assert dp.fibonacci_dp(n) == expected


def test_fibonacci_dp_rejects_negative():
    with pytest.raises(ValueError):
        dp.fibonacci_dp(-1)


def test_fibonacci_sequence():
    assert dp.fibonacci_sequence(0) == []
    assert dp.fibonacci_sequence(1) == [0]
    assert dp.fibonacci_sequence(8) == [0, 1, 1, 2, 3, 5, 8, 13]
    with pytest.raises(ValueError):
        dp.fibonacci_sequence(-2)


# ---------------------------------------------------------------- 子集和

@pytest.mark.parametrize(
    "nums, target, expected",
    [
        ([3, 34, 4, 12, 5, 2], 9, True),
        ([3, 34, 4, 12, 5, 2], 30, False),
        ([], 0, True),
        ([1], 0, True),
        ([], 5, False),
        ([2, 3], 5, True),
        ([2, 3], 1, False),
        ([5], -1, False),
    ],
)
def test_subset_sum(nums, target, expected):
    assert dp.subset_sum(nums, target) == expected


def test_subset_sum_does_not_reuse_an_element():
    """一维滚动数组若写成顺序遍历，[3]/6 会被误判为 True（3 用了两次）。"""
    assert dp.subset_sum([3], 6) is False


def test_subset_sum_ignores_negative_numbers():
    """本题限定非负整数：负数元素被跳过，不会污染结果。"""
    assert dp.subset_sum([-1, 5], 5) is True
    assert dp.subset_sum([-5], 5) is False


def test_partition_equal():
    assert dp.partition_equal([1, 5, 11, 5]) is True
    assert dp.partition_equal([1, 2, 3, 5]) is False
    assert dp.partition_equal([]) is True
    assert dp.partition_equal([7]) is False


# -------------------------------------------------------------- 钢条切割

def test_rod_cutting_clrs_table():
    """CLRS 第 15 章标准表：长度 1..10 售价 1,5,8,9,10,17,17,20,24,30。"""
    prices = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]
    assert dp.rod_cutting(prices, 0) == 0
    assert [dp.rod_cutting(prices, n) for n in range(1, 11)] == [
        1, 5, 8, 10, 13, 17, 18, 22, 25, 30,
    ]


def test_rod_cutting_prefers_cutting_when_whole_piece_is_cheap():
    assert dp.rod_cutting([3, 4], 2) == 6  # 切成两段各卖 3，比整段卖 4 划算


def test_rod_cutting_rejects_out_of_range():
    with pytest.raises(ValueError):
        dp.rod_cutting([2], 3)
    with pytest.raises(ValueError):
        dp.rod_cutting([2, 3], -1)


def test_rod_cutting_with_plan_rejects_out_of_range():
    with pytest.raises(ValueError):
        dp.rod_cutting_with_plan([2], 3)
    with pytest.raises(ValueError):
        dp.rod_cutting_with_plan([2, 3], -1)


def test_rod_cutting_with_plan_sums_to_n():
    prices = [1, 5, 8, 9, 10, 17, 17, 20]
    total, plan = dp.rod_cutting_with_plan(prices, 8)
    assert total == dp.rod_cutting(prices, 8) == 22
    assert sum(plan) == 8
    assert total == sum(prices[length - 1] for length in plan)


# ------------------------------------------------------ 0/1 背包（样板回归）

def test_knapsack_basic():
    assert dp.knapsack_01([2, 3, 4], [3, 4, 5], 5) == 7


def test_knapsack_empty():
    assert dp.knapsack_01([], [], 10) == 0


def test_knapsack_item_too_heavy():
    assert dp.knapsack_01([5], [10], 4) == 0


def test_knapsack_exact_fit():
    """容量 5 有多个装满方案，取价值最大者：重量 2+3 两件，价值 3+5=8。"""
    assert dp.knapsack_01([2, 2, 3], [3, 3, 5], 5) == 8


def test_knapsack_zero_capacity():
    assert dp.knapsack_01([1, 2], [10, 20], 0) == 0


def test_knapsack_negative_capacity_rejected():
    with pytest.raises(ValueError):
        dp.knapsack_01([1], [1], -1)


def test_knapsack_length_mismatch():
    with pytest.raises(ValueError):
        dp.knapsack_01([1, 2], [1], 3)


def test_knapsack_matches_bruteforce():
    """小规模随机对拍：DP 结果必须等于暴力枚举。"""
    rnd = random.Random(7)
    for _ in range(30):
        n = rnd.randint(0, 8)
        weights = [rnd.randint(1, 10) for _ in range(n)]
        values = [rnd.randint(1, 20) for _ in range(n)]
        capacity = rnd.randint(0, 20)

        best = 0
        for r in range(n + 1):
            for combo in itertools.combinations(range(n), r):
                if sum(weights[i] for i in combo) <= capacity:
                    best = max(best, sum(values[i] for i in combo))

        assert dp.knapsack_01(weights, values, capacity) == best
