from src.graphs.bfs import bfs
from src.graphs.graph import Graph


def test_bfs_basic():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")

    assert bfs(graph, "A") == ["A", "B", "C", "D", "E"]


def test_bfs_directed():
    graph = Graph(directed=True)

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    assert bfs(graph, "A") == ["A", "B", "C", "D"]


def test_bfs_disconnected_graph():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("C", "D")

    assert bfs(graph, "A") == ["A", "B"]


def test_bfs_single_node():
    graph = Graph()
    graph.add_node("A")

    assert bfs(graph, "A") == ["A"]


def test_bfs_missing_start():
    graph = Graph()
    graph.add_node("A")

    assert bfs(graph, "Z") == []


def test_bfs_adjacency_matrix():
    graph = Graph(representation="matrix")

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    assert bfs(graph, "A") == ["A", "B", "C", "D"]