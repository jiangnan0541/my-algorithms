"""图论算法测试。

图表示法沿用 `myalgo.graph` 的约定：
无权 `{节点: [邻居]}`、加权 `{节点: [(邻居, 权值)]}`、边表 `[(u, v, w)]`。
"""

import pytest

from myalgo import graph as G

INF = float("inf")

DIAMOND = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}

DAG = {"A": ["C"], "B": ["C", "D"], "C": ["E"], "D": ["E"], "E": []}

WEIGHTED = {
    "A": [("B", 1), ("C", 4)],
    "B": [("C", 2), ("D", 5)],
    "C": [("D", 1)],
    "D": [],
}


# ------------------------------------------------------------------ BFS

def test_bfs_order():
    assert G.bfs_order(DIAMOND, "A") == ["A", "B", "C", "D"]


def test_bfs_unknown_start():
    assert G.bfs_order(DIAMOND, "Z") == []


def test_bfs_single_node():
    assert G.bfs_order({"X": []}, "X") == ["X"]


def test_bfs_cycle_terminates():
    assert G.bfs_order({"A": ["B"], "B": ["C"], "C": ["A"]}, "A") == ["A", "B", "C"]


def test_shortest_path_length():
    assert G.shortest_path_length(DIAMOND, "A", "D") == 2
    assert G.shortest_path_length(DIAMOND, "A", "A") == 0
    assert G.shortest_path_length(DIAMOND, "D", "A") == -1
    assert G.shortest_path_length(DIAMOND, "Z", "A") == -1


# ------------------------------------------------------------------ DFS

def test_dfs_order():
    assert G.dfs_order(DIAMOND, "A") == ["A", "B", "D", "C"]


def test_dfs_and_recursive_agree():
    for start in ("A", "B", "D"):
        assert G.dfs_order(DIAMOND, start) == G.dfs_order_recursive(DIAMOND, start)


@pytest.mark.parametrize("start", ["Z", "a"])
def test_dfs_unknown_start(start):
    assert G.dfs_order(DIAMOND, start) == []
    assert G.dfs_order_recursive(DIAMOND, start) == []


def test_dfs_handles_cycles_and_self_loops():
    assert G.dfs_order({"A": ["A"]}, "A") == ["A"]
    cyclic = {"A": ["B"], "B": ["C"], "C": ["A"]}
    assert sorted(G.dfs_order(cyclic, "A")) == ["A", "B", "C"]


def test_connected_components():
    g = {"A": ["B"], "B": [], "C": [], "D": ["C"]}
    assert G.connected_components(g) == [["A", "B"], ["C", "D"]]


def test_connected_components_empty_graph():
    assert G.connected_components({}) == []


def test_connected_components_one_way_edges_are_treated_as_undirected():
    """只写了 A->B，没有 B->A，仍应算同一个连通分量。"""
    assert G.connected_components({"A": ["B"], "B": []}) == [["A", "B"]]


# ----------------------------------------------------------- 拓扑排序

def test_topological_sort_kahn():
    assert G.topological_sort(DAG) == ["A", "B", "C", "D", "E"]


def test_topological_sort_empty_graph():
    assert G.topological_sort({}) == []


def test_topological_sort_detects_cycle():
    with pytest.raises(ValueError, match="环"):
        G.topological_sort({"A": ["B"], "B": ["A"]})
    with pytest.raises(ValueError, match="环"):
        G.topological_sort({"A": ["A"]})


def test_topological_sort_dfs_returns_none_on_cycle():
    assert G.topological_sort_dfs({"A": ["B"], "B": ["A"]}) is None


def test_both_topological_sorts_respect_every_edge():
    """不比较具体顺序（拓扑序不唯一），只验证约束成立。"""
    for order in (G.topological_sort(DAG), G.topological_sort_dfs(DAG)):
        assert sorted(order) == sorted(DAG)
        position = {node: i for i, node in enumerate(order)}
        for u, successors in DAG.items():
            for v in successors:
                assert position[u] < position[v]


# --------------------------------------------------------------- Dijkstra

def test_dijkstra_known_distances():
    assert G.dijkstra(WEIGHTED, "A") == {"A": 0, "B": 1, "C": 3, "D": 4}


def test_dijkstra_unknown_start():
    assert G.dijkstra(WEIGHTED, "Z") == {}


def test_dijkstra_unreachable_nodes_are_omitted():
    assert G.dijkstra({"A": [("B", 1)], "B": [], "Z": []}, "A") == {"A": 0, "B": 1}


def test_dijkstra_path():
    assert G.dijkstra_path(WEIGHTED, "A", "D") == (4, ["A", "B", "C", "D"])
    assert G.dijkstra_path(WEIGHTED, "A", "A") == (0, ["A"])
    assert G.dijkstra_path(WEIGHTED, "D", "A") == (INF, [])


def test_dijkstra_path_rejects_a_worse_alternative_route():
    """A->C 直达 1；绕 A->B->C 要 6，这次松弛必须被拒绝。"""
    g = {"A": [("B", 1), ("C", 1)], "B": [("C", 5)], "C": []}
    assert G.dijkstra_path(g, "A", "C") == (1, ["A", "C"])


def test_dijkstra_path_with_missing_endpoints():
    """起点或终点不在图里时，统一返回 (inf, [])。"""
    assert G.dijkstra_path(WEIGHTED, "Z", "A") == (INF, [])
    assert G.dijkstra_path(WEIGHTED, "A", "Z") == (INF, [])


def test_dijkstra_skips_stale_heap_entries():
    """节点先经"贵"边入堆、再被"便宜"路径更新，堆里会留下过期项，必须跳过。"""
    g = {
        0: [(1, 50), (2, 1)],
        1: [(3, 1)],
        2: [(1, 1), (3, 1)],
        3: [],
    }
    # 1 号节点先以距离 50 入堆，随后 0->2->1 把距离压到 2；
    # 3 号节点走 0->2->3 只要 2，比 0->1->3 的 3 更短
    assert G.dijkstra(g, 0) == {0: 0, 1: 2, 2: 1, 3: 2}


def test_dijkstra_rejects_negative_weight():
    with pytest.raises(ValueError, match="负"):
        G.dijkstra({"A": [("B", -1)], "B": []}, "A")


# ------------------------------------------------------------ Bellman-Ford

EDGES = [(0, 1, 4), (0, 2, 5), (1, 2, -3), (2, 3, 2)]


def test_bellman_ford_known_distances():
    assert G.bellman_ford(EDGES, 4, 0) == [0, 4, 1, 3]


def test_bellman_ford_unreachable_is_inf():
    assert G.bellman_ford([(0, 1, 1)], 3, 0) == [0, 1, INF]


def test_bellman_ford_detects_negative_cycle():
    with pytest.raises(ValueError, match="负权环"):
        G.bellman_ford([(0, 1, 1), (1, 2, -2), (2, 1, -2)], 3, 0)


def test_bellman_ford_allows_negative_edge_without_cycle():
    assert G.bellman_ford([(0, 1, -2), (1, 2, -3)], 3, 0) == [0, -2, -5]


def test_bellman_ford_path():
    assert G.bellman_ford_path(EDGES, 4, 0, 3) == (3, [0, 1, 2, 3])
    assert G.bellman_ford_path(EDGES, 4, 3, 0) == (INF, [])


def test_bellman_ford_rejects_bad_start():
    with pytest.raises(ValueError):
        G.bellman_ford(EDGES, 4, 9)


# --------------------------------------------------------- Floyd-Warshall

MATRIX = [
    [0, 5, INF, 10],
    [INF, 0, 3, INF],
    [INF, INF, 0, 1],
    [INF, INF, INF, 0],
]


def test_floyd_warshall_known_matrix():
    assert G.floyd_warshall(MATRIX) == [
        [0, 5, 8, 9],
        [INF, 0, 3, 4],
        [INF, INF, 0, 1],
        [INF, INF, INF, 0],
    ]


def test_floyd_warshall_single_node():
    assert G.floyd_warshall([[0]]) == [[0]]


def test_floyd_warshall_does_not_mutate_input():
    snapshot = [row[:] for row in MATRIX]
    G.floyd_warshall(MATRIX)
    assert MATRIX == snapshot


def test_has_negative_cycle():
    assert G.has_negative_cycle([[0, 1], [1, 0]]) is False
    assert G.has_negative_cycle([[0, 2], [2, 0]]) is False
    assert G.has_negative_cycle([[0, 1], [-2, 0]]) is True


# -------------------------------------------------------------- 并查集

def test_union_find_basics():
    uf = G.UnionFind(5)
    assert uf.component_count == 5
    assert uf.connected(0, 1) is False
    assert uf.union(0, 1) is True
    assert uf.union(0, 1) is False  # 已在同一集合
    assert uf.connected(0, 1) is True
    assert uf.component_count == 4


def test_union_find_groups_and_size():
    uf = G.UnionFind(6)
    for a, b in [(0, 1), (1, 2), (3, 4)]:
        uf.union(a, b)
    assert uf.size(0) == 3
    assert uf.size(5) == 1
    assert uf.groups() == {0: [0, 1, 2], 3: [3, 4], 5: [5]}


def test_union_find_path_compression_flattens_a_deep_node():
    """构造一棵深度 2 的树，再对最深节点 find 一次，验证它被挂到根上。"""
    uf = G.UnionFind(5)
    uf.union(0, 1)  # 根 0，大小 2
    uf.union(2, 3)  # 根 2，大小 2
    uf.union(1, 2)  # 等大 => 2 挂到 0，此时 3 的父节点是 2（深度 2）
    assert uf.find(3) == 0
    assert uf.find(2) == 0  # 路径压缩已把 2 直接挂到根上


def test_union_find_swaps_so_the_smaller_tree_attaches_to_the_bigger_one():
    uf = G.UnionFind(6)
    for x in (1, 2, 3):
        uf.union(0, x)  # 0 号集合长到 4 个元素
    uf.union(4, 5)  # 另一个 2 元素集合，根为 4
    assert uf.union(4, 0) is True  # 传参顺序与大小顺序相反 => 触发交换
    assert uf.find(5) == 0  # 小树整体挂到大树根 0 下
    assert uf.component_count == 1


def test_union_find_empty():
    uf = G.UnionFind(0)
    assert uf.component_count == 0
    assert len(uf) == 0


def test_union_find_rejects_negative_count():
    with pytest.raises(ValueError):
        G.UnionFind(-1)


# ------------------------------------------------------- 最小生成树

MST_EDGES = [(0, 1, 1), (0, 2, 4), (0, 3, 3), (1, 2, 2), (2, 3, 5)]

MST_GRAPH = {
    0: [(1, 1), (2, 4), (3, 3)],
    1: [(0, 1), (2, 2)],
    2: [(0, 4), (1, 2), (3, 5)],
    3: [(0, 3), (2, 5)],
}


def test_kruskal_known_mst():
    total, chosen = G.kruskal(4, MST_EDGES)
    assert total == 6
    assert chosen == [(0, 1, 1), (1, 2, 2), (0, 3, 3)]


def test_kruskal_picks_v_minus_one_edges():
    total, chosen = G.kruskal(4, MST_EDGES)
    assert len(chosen) == 3


def test_kruskal_single_node_and_empty_edges():
    assert G.kruskal(1, []) == (0, [])


def test_kruskal_disconnected_returns_forest():
    total, chosen = G.kruskal(3, [(0, 1, 2)])
    assert total == 2
    assert chosen == [(0, 1, 2)]


def test_kruskal_ignores_duplicate_edges():
    total, chosen = G.kruskal(4, [(0, 1, 1), (0, 1, 1), (1, 2, 1), (0, 2, 5)])
    assert total == 2


def test_prim_known_mst():
    assert G.prim(MST_GRAPH) == (6, [(0, 1, 1), (1, 2, 2), (0, 3, 3)])


def test_prim_single_node():
    assert G.prim({0: []}) == (0, [])


def test_prim_empty_graph():
    assert G.prim({}) == (0, [])


def test_prim_handles_disconnected_graph():
    g = {0: [(1, 2)], 1: [(0, 2)], 2: [(3, 7)], 3: [(2, 7)]}
    total, chosen = G.prim(g)
    assert total == 9
    assert len(chosen) == 2


def test_prim_agrees_with_kruskal_on_total_weight():
    total_k, _ = G.kruskal(4, MST_EDGES)
    total_p, _ = G.prim(MST_GRAPH)
    assert total_k == total_p == 6


# ---------------------------------------------------------------- 环检测

@pytest.mark.parametrize(
    "g, expected",
    [
        ({"A": ["B"], "B": ["C"], "C": []}, False),
        ({"A": ["B"], "B": ["A"]}, True),
        ({"A": ["A"]}, True),
        ({}, False),
        ({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, False),
        ({"A": ["B"], "B": ["C"], "C": ["B"]}, True),
    ],
)
def test_has_cycle_directed(g, expected):
    assert G.has_cycle_directed(g) is expected


def test_find_cycle_directed():
    assert G.find_cycle_directed({"A": ["B"], "B": ["C"], "C": ["A"]}) == [
        "A", "B", "C", "A",
    ]
    assert G.find_cycle_directed({"A": ["B"], "B": []}) is None
    assert G.find_cycle_directed({"A": ["A"]}) == ["A", "A"]


def test_find_cycle_directed_meeting_a_finished_node_is_not_a_cycle():
    """菱形 A->B->D、A->C->D：C 看到的 D 已经完成（BLACK），不是环。"""
    diamond = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
    assert G.find_cycle_directed(diamond) is None


def test_has_cycle_directed_agrees_with_find_cycle():
    for g in [{}, {"A": []}, {"A": ["B"], "B": ["A"]}, {"A": ["B"], "B": ["C"]}]:
        assert G.has_cycle_directed(g) is (G.find_cycle_directed(g) is not None)


@pytest.mark.parametrize(
    "g, expected",
    [
        ({"A": ["B", "C"], "B": ["A"], "C": ["A"]}, False),
        ({"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]}, True),
        ({"A": []}, False),
        ({"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"]}, False),
        # 4 环：A-B-C-D-A
        ({"A": ["B", "D"], "B": ["A", "C"], "C": ["B", "D"], "D": ["C", "A"]}, True),
    ],
)
def test_has_cycle_undirected(g, expected):
    assert G.has_cycle_undirected(g) is expected


def test_has_cycle_undirected_treats_two_directions_as_one_edge():
    """无向图中 B:[C] 与 C:[B] 是同一条边的两个方向，不是环（路径 A-B-C）。"""
    assert G.has_cycle_undirected({"A": ["B"], "B": ["A", "C"], "C": ["B"]}) is False


def test_has_cycle_directed_would_misjudge_that_same_graph():
    """反例：把无向图塞给有向版检测器，A-B 往返会被当成环 —— 两者不可混用。"""
    assert G.has_cycle_directed({"A": ["B"], "B": ["A", "C"], "C": ["B"]}) is True
