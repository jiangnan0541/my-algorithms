"""排序算法测试。"""

import random

import pytest

from myalgo.sorting import quick_sort

CASES = [
    [],
    [1],
    [2, 2, 2],
    [3, 1, 4, 1, 5, 9, 2, 6],
    list(range(10)),
    list(range(10, 0, -1)),
    [-5, 0, 3, -1],
]


@pytest.mark.parametrize("data", CASES)
def test_quick_sort_matches_builtin(data):
    assert quick_sort(data) == sorted(data)


def test_quick_sort_does_not_mutate_input():
    data = [3, 1, 2]
    quick_sort(data)
    assert data == [3, 1, 2]


def test_quick_sort_randomized():
    rnd = random.Random(42)
    for _ in range(20):
        data = [rnd.randint(-100, 100) for _ in range(rnd.randint(0, 50))]
        assert quick_sort(data) == sorted(data)
