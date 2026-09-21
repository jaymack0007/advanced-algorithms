from src.graphs.dfs import dfs_iterative, dfs_recursive
from src.graphs.graph import Graph


def build_test_graph():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")

    return graph


def test_dfs_iterative_basic():
    graph = build_test_graph()

    assert dfs_iterative(graph, "A") == [
        "A", "B", "D", "C", "E"
    ]


def test_dfs_recursive_basic():
    graph = build_test_graph()

    assert dfs_recursive(graph, "A") == [
        "A", "B", "D", "C", "E"
    ]


def test_dfs_versions_match():
    graph = build_test_graph()

    assert dfs_iterative(graph, "A") == dfs_recursive(graph, "A")


def test_dfs_disconnected_graph():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("C", "D")

    assert dfs_iterative(graph, "A") == ["A", "B"]
    assert dfs_recursive(graph, "A") == ["A", "B"]


def test_dfs_single_node():
    graph = Graph()
    graph.add_node("A")

    assert dfs_iterative(graph, "A") == ["A"]
    assert dfs_recursive(graph, "A") == ["A"]


def test_dfs_missing_start():
    graph = Graph()
    graph.add_node("A")

    assert dfs_iterative(graph, "Z") == []
    assert dfs_recursive(graph, "Z") == []


def test_dfs_directed_graph():
    graph = Graph(directed=True)

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    assert dfs_iterative(graph, "A") == [
        "A", "B", "D", "C"
    ]


def test_dfs_adjacency_matrix():
    graph = Graph(representation="matrix")

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    assert dfs_iterative(graph, "A") == [
        "A", "B", "D", "C"
    ]