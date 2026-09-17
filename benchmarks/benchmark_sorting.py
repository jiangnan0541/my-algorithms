"""排序算法横向基准（对照官方 `sorts/benchmark_sorts.py` 的思路）。

用法：
    python benchmarks/benchmark_sorting.py
    python benchmarks/benchmark_sorting.py --sizes 200,1000,3000

对比 10 个自定义排序在 5 种输入分布上的耗时，用 `timeit` 取多次运行的最小值
（最小值比平均值更能反映真实性能，因为不受偶发系统调度干扰）。

观察点（跑一遍就能验证教科书结论）：
- O(n^2) 的三个（冒泡/插入/选择）在 n 变大后崩得最快
- 插入排序在「已有序」输入上是 O(n)，跟 O(n log n) 的差距不大
- 计数/基数排序与值域有关，值域窄时反而比比较排序快
- 快排在「已有序」输入上（本实现取中位数基准）没有出现最坏情况，
  而三数取端点的实现在这个分布上会退化到 O(n^2)
"""

from __future__ import annotations

import argparse
import random
import sys
import timeit
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from myalgo import sorting  # noqa: E402

SORTS = [
    ("bubble", sorting.bubble_sort),
    ("insertion", sorting.insertion_sort),
    ("selection", sorting.selection_sort),
    ("merge", sorting.merge_sort),
    ("quick", sorting.quick_sort),
    ("heap", sorting.heap_sort),
    ("shell", sorting.shell_sort),
    ("counting", sorting.counting_sort),
    ("radix", sorting.radix_sort),
    ("bucket", sorting.bucket_sort),
]

# 值域必须收窄，counting_sort / radix_sort 直接按值大小开数组
VALUE_POOL = 100_000


def make_datasets(size: int, seed: int = 20260918) -> dict:
    """构造 5 种典型分布。"""
    rnd = random.Random(seed)
    base = [rnd.randrange(1, VALUE_POOL) for _ in range(size)]
    ordered = sorted(base)
    return {
        "random": base,
        "sorted": ordered,
        "reversed": ordered[::-1],
        "all-equal": [7] * size,
        "nearly-sorted": [
            ordered[i] if rnd.random() > 0.02 else rnd.randrange(1, VALUE_POOL)
            for i in range(size)
        ],
    }


def time_one(func, data: list, repeat: int = 3) -> float:
    """返回单次调用的最快耗时（秒）。"""
    timer = timeit.Timer(lambda: func(data))
    return min(timer.repeat(repeat=repeat, number=1))


def run(sizes: list[int], repeat: int) -> None:
    print(f"值域 1..{VALUE_POOL}，每个测量取 {repeat} 次最小值\n")
    for size in sizes:
        datasets = make_datasets(size)
        print(f"=== n = {size} ===")
        header = f"{'算法':<10}" + "".join(f"{name:>14}" for name in datasets)
        print(header)
        print("-" * len(header))
        for label, func in SORTS:
            cells = []
            for data in datasets.values():
                elapsed = time_one(func, data, repeat)
                cells.append(f"{elapsed * 1000:>12.2f}ms" if elapsed >= 1e-4 else f"{elapsed * 1e6:>12.0f}us")
            print(f"{label:<10}" + "".join(cells))
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="排序算法横向基准")
    parser.add_argument(
        "--sizes",
        default="200,1000,2000",
        help="逗号分隔的规模列表（默认 200,1000,2000）",
    )
    parser.add_argument("--repeat", type=int, default=3, help="每个测量重复次数")
    args = parser.parse_args()

    sizes = [int(x) for x in args.sizes.split(",") if x.strip()]
    run(sizes, args.repeat)


if __name__ == "__main__":
    main()
