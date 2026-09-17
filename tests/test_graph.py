"""图论测试。"""

from myalgo.graph import bfs_order, shortest_path_length

GRAPH = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}


def test_bfs_order():
    assert bfs_order(GRAPH, "A") == ["A", "B", "C", "D"]


def test_bfs_unknown_start():
    assert bfs_order(GRAPH, "Z") == []


def test_bfs_single_node():
    assert bfs_order({"X": []}, "X") == ["X"]


def test_bfs_cycle_terminates():
    cyclic = {"A": ["B"], "B": ["C"], "C": ["A"]}
    assert bfs_order(cyclic, "A") == ["A", "B", "C"]


def test_shortest_path_length():
    assert shortest_path_length(GRAPH, "A", "D") == 2
    assert shortest_path_length(GRAPH, "A", "A") == 0
    assert shortest_path_length(GRAPH, "D", "A") == -1


def test_shortest_path_unknown_start():
    assert shortest_path_length(GRAPH, "Z", "A") == -1
