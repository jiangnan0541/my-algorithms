"""随机对拍 —— 用**独立实现**互相印证，而不是只比对硬编码答案。

对拍思路分三类：
1. 与标准库 / 暴力枚举比：sorted()、itertools.combinations、枚举全部子序列
2. 与另一种算法比：Dijkstra ↔ Floyd-Warshall、Kruskal ↔ Prim、BFS ↔ 单位权 Dijkstra
3. 与朴素递归比：编辑距离、矩阵连乘

硬编码的已知答案只能证明"这几个用例对"，对拍才能证明"这一整类输入都对"。
"""

import itertools
import random

from myalgo import dynamic_programming as dp
from myalgo import graph as G
from myalgo import sorting

INF = float("inf")


# ------------------------------------------------------------ 排序

def test_all_sorts_agree_on_the_same_random_input():
    """10 个排序互相印证：同一批随机输入上结果必须完全一致（都等于 sorted）。"""
    rnd = random.Random(314159)
    for _ in range(10):
        data = [rnd.randint(-50, 50) for _ in range(rnd.randint(0, 30))]
        outputs = [
            sorting.bubble_sort(data),
            sorting.insertion_sort(data),
            sorting.selection_sort(data),
            sorting.merge_sort(data),
            sorting.quick_sort(data),
            sorting.heap_sort(data),
            sorting.shell_sort(data),
            sorting.counting_sort(data),
            sorting.radix_sort(data),
            sorting.bucket_sort(data),
        ]
        assert all(out == sorted(data) for out in outputs)


# ------------------------------------------------------ 最长递增子序列

def brute_lis(nums: list) -> int:
    """枚举所有 2^n 个子序列，取最长的严格递增者。"""
    n = len(nums)
    best = 0
    for mask in range(1 << n):
        seq = [nums[i] for i in range(n) if mask >> i & 1]
        if all(x < y for x, y in zip(seq, seq[1:])):
            best = max(best, len(seq))
    return best


def test_lis_matches_bruteforce():
    rnd = random.Random(2718)
    for _ in range(40):
        nums = [rnd.randint(0, 12) for _ in range(rnd.randint(0, 9))]
        assert dp.lis_length(nums) == brute_lis(nums)
        assert len(dp.lis_sequence(nums)) == brute_lis(nums)


# ------------------------------------------------------------ 零钱兑换

def bfs_coin_change(coins: list, amount: int) -> int:
    """独立实现：在「金额空间」上做 BFS，首次到达 amount 的层数即最少枚数。"""
    if amount == 0:
        return 0
    if not coins:
        return -1
    seen = {0}
    frontier = [0]
    steps = 0
    while frontier:
        steps += 1
        nxt = []
        for base in frontier:
            for c in coins:
                value = base + c
                if value == amount:
                    return steps
                if value < amount and value not in seen:
                    seen.add(value)
                    nxt.append(value)
        frontier = nxt
    return -1


def test_coin_change_matches_bfs():
    rnd = random.Random(1618)
    for _ in range(40):
        coins = rnd.sample(range(1, 12), rnd.randint(1, 4))
        amount = rnd.randint(0, 60)
        assert dp.coin_change(coins, amount) == bfs_coin_change(coins, amount)


# -------------------------------------------------------------- 子集和

def test_subset_sum_matches_bruteforce():
    rnd = random.Random(1414)
    for _ in range(60):
        nums = [rnd.randint(1, 12) for _ in range(rnd.randint(0, 7))]
        target = rnd.randint(0, 30)
        expected = any(
            sum(combo) == target
            for r in range(len(nums) + 1)
            for combo in itertools.combinations(nums, r)
        )
        assert dp.subset_sum(nums, target) is expected


# ------------------------------------------------------------ 最大子段和

def brute_max_subarray(nums: list) -> int:
    if not nums:
        return 0
    return max(
        sum(nums[i : j + 1])
        for i in range(len(nums))
        for j in range(i, len(nums))
    )


def test_max_subarray_matches_bruteforce():
    rnd = random.Random(1732)
    for _ in range(50):
        nums = [rnd.randint(-10, 10) for _ in range(rnd.randint(0, 12))]
        assert dp.max_subarray(nums) == brute_max_subarray(nums)


# -------------------------------------------------------------- 编辑距离

def naive_edit_distance(a: str, b: str) -> int:
    """朴素递归（无记忆化）—— 指数级，只用于短字符串对拍。"""
    if not a:
        return len(b)
    if not b:
        return len(a)
    if a[-1] == b[-1]:
        return naive_edit_distance(a[:-1], b[:-1])
    return 1 + min(
        naive_edit_distance(a[:-1], b),
        naive_edit_distance(a, b[:-1]),
        naive_edit_distance(a[:-1], b[:-1]),
    )


def test_edit_distance_matches_naive_recursion():
    rnd = random.Random(2236)
    alphabet = "abc"
    for _ in range(30):
        a = "".join(rnd.choice(alphabet) for _ in range(rnd.randint(0, 5)))
        b = "".join(rnd.choice(alphabet) for _ in range(rnd.randint(0, 5)))
        assert dp.edit_distance(a, b) == naive_edit_distance(a, b)


# -------------------------------------------------------------- 矩阵连乘

def naive_chain_order(dims: list, i: int, j: int) -> int:
    """朴素递归枚举所有加括号方式（无记忆化）。"""
    if i == j:
        return 0
    return min(
        naive_chain_order(dims, i, k)
        + naive_chain_order(dims, k + 1, j)
        + dims[i - 1] * dims[k] * dims[j]
        for k in range(i, j)
    )


def test_matrix_chain_matches_naive_recursion():
    rnd = random.Random(8281)
    for _ in range(25):
        n = rnd.randint(1, 5)
        dims = [rnd.randint(1, 20) for _ in range(n + 1)]
        best, _ = dp.matrix_chain_order(dims)
        assert best == naive_chain_order(dims, 1, n)


# ---------------------------------------------------------------- 最短路

def random_weighted_graph(rnd: random.Random, n: int, edge_prob: float = 0.35) -> dict:
    """随机**有向**加权图（权值 1..9，非负）。"""
    graph = {i: [] for i in range(n)}
    for u in range(n):
        for v in range(n):
            if u != v and rnd.random() < edge_prob:
                graph[u].append((v, rnd.randint(1, 9)))
    return graph


def to_matrix(graph: dict, n: int) -> list:
    matrix = [[INF] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0
    for u, edges in graph.items():
        for v, w in edges:
            matrix[u][v] = min(matrix[u][v], w)
    return matrix


def test_dijkstra_matches_floyd_warshall():
    """单源（堆）与全源（DP）两套完全不同的思路，距离表必须一致。"""
    rnd = random.Random(9182)
    for _ in range(30):
        n = rnd.randint(1, 7)
        graph = random_weighted_graph(rnd, n)
        dist = G.dijkstra(graph, 0)
        row0 = G.floyd_warshall(to_matrix(graph, n))[0]

        for v in range(n):
            if row0[v] == INF:
                assert v not in dist, f"节点 {v} 被判定为不可达，Dijkstra 却给了距离"
            else:
                assert dist.get(v) == row0[v]

        for v, d in dist.items():
            assert d == row0[v]


def test_bfs_shortest_path_matches_unit_weight_dijkstra():
    """无权图 BFS 与「所有边权为 1」的 Dijkstra 必须给同一个最短路长度。"""
    unweighted = {
        "A": ["B", "C"],
        "B": ["D", "E"],
        "C": ["E"],
        "D": ["F"],
        "E": ["F"],
        "F": [],
    }
    weighted = {u: [(v, 1) for v in nbrs] for u, nbrs in unweighted.items()}
    distances = G.dijkstra(weighted, "A")

    for target in unweighted:
        assert G.shortest_path_length(unweighted, "A", target) == distances[target]


# ------------------------------------------------------------ 最小生成树

def random_connected_graph(rnd: random.Random, n: int, extra_edges: int = 6):
    """先随机生成一棵生成树保证连通，再补若干条随机边制造环。"""
    graph = {i: [] for i in range(n)}
    edges = []

    def add(u, v, w):
        graph[u].append((v, w))
        graph[v].append((u, w))
        edges.append((u, v, w))

    for v in range(1, n):
        add(rnd.randrange(v), v, rnd.randint(1, 9))
    for _ in range(extra_edges):
        u, v = rnd.randrange(n), rnd.randrange(n)
        if u != v:
            add(u, v, rnd.randint(1, 9))
    return graph, edges


def test_kruskal_matches_prim():
    """边贪心（排序 + 并查集）与点贪心（优先队列）必须给出同一个 MST 权值。"""
    rnd = random.Random(5772)
    for _ in range(30):
        n = rnd.randint(1, 8)
        graph, edges = random_connected_graph(rnd, n)
        total_k, chosen_k = G.kruskal(n, edges)
        total_p, chosen_p = G.prim(graph)

        assert total_k == total_p
        assert len(chosen_k) == len(chosen_p) == n - 1


def test_mst_weight_is_at_most_any_other_spanning_tree():
    """MST 是下界：随机取别的生成树，权值不会更小。"""
    rnd = random.Random(6060)
    for _ in range(20):
        n = rnd.randint(2, 8)
        graph, edges = random_connected_graph(rnd, n, extra_edges=8)
        total, _ = G.kruskal(n, edges)

        # 用 Prim 从不同起点各跑一次，权值应始终相同
        for start in list(graph)[:3]:
            other_total, _ = G.prim(graph, start)
            assert other_total == total


# ------------------------------------------------------------ 拓扑排序

def test_topological_sorts_agree_on_validity():
    rnd = random.Random(3366)
    for _ in range(30):
        n = rnd.randint(1, 7)
        dag = {i: [] for i in range(n)}
        for u in range(n):
            for v in range(u + 1, n):  # 只连向后继，天然无环
                if rnd.random() < 0.4:
                    dag[u].append(v)

        for order in (G.topological_sort(dag), G.topological_sort_dfs(dag)):
            assert sorted(order) == sorted(dag)
            position = {node: i for i, node in enumerate(order)}
            for u, successors in dag.items():
                for v in successors:
                    assert position[u] < position[v]
