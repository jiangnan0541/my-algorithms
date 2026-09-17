"""动态规划测试（含与暴力枚举的对拍）。"""

import itertools
import random

import pytest

from myalgo.dynamic_programming import knapsack_01


def test_knapsack_basic():
    assert knapsack_01([2, 3, 4], [3, 4, 5], 5) == 7


def test_knapsack_empty():
    assert knapsack_01([], [], 10) == 0


def test_knapsack_item_too_heavy():
    assert knapsack_01([5], [10], 4) == 0


def test_knapsack_exact_fit():
    """容量 5 时有多个装满方案，取价值最大者：2+3 两件，价值 3+5=8。"""
    assert knapsack_01([2, 2, 3], [3, 3, 5], 5) == 8


def test_knapsack_zero_capacity():
    assert knapsack_01([1, 2], [10, 20], 0) == 0


def test_knapsack_negative_capacity_rejected():
    with pytest.raises(ValueError):
        knapsack_01([1], [1], -1)


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

        assert knapsack_01(weights, values, capacity) == best


def test_knapsack_length_mismatch():
    with pytest.raises(ValueError):
        knapsack_01([1, 2], [1], 3)
