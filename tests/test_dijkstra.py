import pytest

from src.graphs.dijkstra import dijkstra, reconstruct_path
from src.graphs.graph import Graph


def build_weighted_graph():
    graph = Graph(
        directed=True,
        weighted=True,
    )

    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("C", "B", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3),
    ]

    for u, v, weight in edges:
        graph.add_edge(u, v, weight)

    return graph


def test_dijkstra_distances():
    graph = build_weighted_graph()

    distances, _ = dijkstra(graph, "A")

    assert distances["A"] == 0
    assert distances["B"] == 3
    assert distances["C"] == 2
    assert distances["D"] == 8
    assert distances["E"] == 10
    assert distances["F"] == 13


def test_dijkstra_predecessors():
    graph = build_weighted_graph()

    _, predecessors = dijkstra(graph, "A")

    assert predecessors["C"] == "A"
    assert predecessors["B"] == "C"
    assert predecessors["D"] == "B"
    assert predecessors["E"] == "D"
    assert predecessors["F"] == "E"


def test_reconstruct_path():
    graph = build_weighted_graph()

    _, predecessors = dijkstra(graph, "A")

    path = reconstruct_path(
        predecessors,
        "A",
        "F",
    )

    assert path == [
        "A", "C", "B", "D", "E", "F"
    ]


def test_disconnected_graph():
    graph = Graph(
        directed=True,
        weighted=True,
    )

    graph.add_edge("A", "B", 2)
    graph.add_node("C")

    distances, predecessors = dijkstra(graph, "A")

    assert distances["A"] == 0
    assert distances["B"] == 2
    assert distances["C"] == float("inf")
    assert predecessors["C"] is None


def test_unreachable_path():
    graph = Graph(
        directed=True,
        weighted=True,
    )

    graph.add_edge("A", "B", 2)
    graph.add_node("C")

    _, predecessors = dijkstra(graph, "A")

    assert reconstruct_path(
        predecessors,
        "A",
        "C",
    ) == []


def test_missing_source():
    graph = Graph(
        directed=True,
        weighted=True,
    )

    graph.add_node("A")

    with pytest.raises(ValueError):
        dijkstra(graph, "Z")


def test_negative_weight():
    graph = Graph(
        directed=True,
        weighted=True,
    )

    graph.add_edge("A", "B", -1)

    with pytest.raises(ValueError):
        dijkstra(graph, "A")


def test_dijkstra_matrix_graph():
    graph = Graph(
        directed=True,
        weighted=True,
        representation="matrix",
    )

    graph.add_edge("A", "B", 4)
    graph.add_edge("A", "C", 1)
    graph.add_edge("C", "B", 2)

    distances, _ = dijkstra(graph, "A")

    assert distances["B"] == 3
    assert distances["C"] == 1

def test_list_and_heap_dijkstra_match():
    graph = build_weighted_graph()

    heap_distances, _ = dijkstra(graph, "A")

    from src.graphs.dijkstra import dijkstra_list

    list_distances, _ = dijkstra_list(graph, "A")

    assert heap_distances == list_distances