"""排序算法测试。

统一的验收口径（对 10 个排序一视同仁）：
1. 结果 == ``sorted(data)``
2. 不修改入参
3. 随机数据也成立
4. 边界：空 / 单元素 / 全等值 / 逆序 / 含负数 / 已有序
"""

import random

import pytest

from myalgo import sorting

SORTS = [
    sorting.bubble_sort,
    sorting.insertion_sort,
    sorting.selection_sort,
    sorting.merge_sort,
    sorting.quick_sort,
    sorting.heap_sort,
    sorting.shell_sort,
    sorting.counting_sort,
    sorting.radix_sort,
    sorting.bucket_sort,
]
SORT_IDS = [func.__name__ for func in SORTS]

EDGE_CASES = [
    pytest.param([], id="empty"),
    pytest.param([1], id="single"),
    pytest.param([2, 2, 2], id="all-equal"),
    pytest.param(list(range(10)), id="sorted"),
    pytest.param(list(range(10, 0, -1)), id="reversed"),
    pytest.param([-5, 0, 3, -1], id="with-negatives"),
    pytest.param([-3, -3, -1, -7], id="all-negative"),
    pytest.param([0, 0, -1, 0], id="with-zero-dup"),
]


@pytest.mark.parametrize("func", SORTS, ids=SORT_IDS)
@pytest.mark.parametrize("data", EDGE_CASES)
def test_matches_builtin_sorted(func, data):
    assert func(data) == sorted(data)


@pytest.mark.parametrize("func", SORTS, ids=SORT_IDS)
def test_does_not_mutate_input(func):
    data = [3, 1, 2]
    func(data)
    assert data == [3, 1, 2]


@pytest.mark.parametrize("func", SORTS, ids=SORT_IDS)
def test_returns_new_list(func):
    data = [2, 1]
    assert func(data) is not data


@pytest.mark.parametrize("func", SORTS, ids=SORT_IDS)
def test_randomized(func):
    """随机对拍：以标准库 sorted() 为基准。"""
    rnd = random.Random(20260918)
    for _ in range(20):
        data = [rnd.randint(-100, 100) for _ in range(rnd.randint(0, 40))]
        assert func(data) == sorted(data)


@pytest.mark.parametrize("func", SORTS, ids=SORT_IDS)
def test_accepts_tuple_and_range(func):
    """入参是任意序列（不只是 list）。"""
    assert func((3, 1, 2)) == [1, 2, 3]
    assert func(range(5, 0, -1)) == [1, 2, 3, 4, 5]


def test_merge_sort_is_stable():
    """归并排序稳定：相等元素保持原有相对顺序。"""
    data = [(1, "a"), (0, "b"), (1, "c"), (0, "d")]
    assert sorting.merge_sort(data) == [(0, "b"), (0, "d"), (1, "a"), (1, "c")]


def test_bucket_sort_handles_floats():
    assert sorting.bucket_sort([0.5, 0.1, 0.9, 0.3]) == [0.1, 0.3, 0.5, 0.9]


def test_bucket_sort_single_bucket_degenerates_gracefully():
    """只有 1 个桶时退化成桶内插入排序，结果仍然正确。"""
    data = [4, 2, 9, 1, 7]
    assert sorting.bucket_sort(data, bucket_count=1) == [1, 2, 4, 7, 9]


def test_counting_sort_rejects_non_integers():
    with pytest.raises(TypeError):
        sorting.counting_sort([1.5, 2.5])


def test_radix_sort_rejects_non_integers():
    with pytest.raises(TypeError):
        sorting.radix_sort([1.5, 2.5])
