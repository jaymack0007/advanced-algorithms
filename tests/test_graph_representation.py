import pytest

from src.graphs.graph import Graph


def test_adjacency_list_undirected():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")

    assert set(graph.get_neighbors("A")) == {"B", "C"}
    assert graph.get_neighbors("B") == ["A"]
    assert graph.get_neighbors("C") == ["A"]


def test_directed_graph():
    graph = Graph(directed=True)

    graph.add_edge("A", "B")

    assert graph.get_neighbors("A") == ["B"]
    assert graph.get_neighbors("B") == []


def test_weighted_graph():
    graph = Graph(weighted=True)

    graph.add_edge("A", "B", 5)

    assert graph.get_weight("A", "B") == 5
    assert graph.get_weight("B", "A") == 5


def test_unweighted_graph_uses_weight_one():
    graph = Graph(weighted=False)

    graph.add_edge("A", "B", 10)

    assert graph.get_weight("A", "B") == 1


def test_adjacency_matrix():
    graph = Graph(representation="matrix")

    graph.add_edge("A", "B")
    graph.add_edge("B", "C")

    assert graph.get_neighbors("A") == ["B"]
    assert set(graph.get_neighbors("B")) == {"A", "C"}


def test_weighted_adjacency_matrix():
    graph = Graph(
        directed=True,
        weighted=True,
        representation="matrix",
    )

    graph.add_edge("A", "B", 7)

    assert graph.get_neighbors("A") == ["B"]
    assert graph.get_weight("A", "B") == 7
    assert graph.get_neighbors("B") == []


def test_remove_edge():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.remove_edge("A", "B")

    assert graph.get_neighbors("A") == []
    assert graph.get_neighbors("B") == []


def test_remove_node():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("B", "C")

    graph.remove_node("B")

    assert "B" not in graph.nodes
    assert graph.get_neighbors("A") == []
    assert graph.get_neighbors("C") == []


def test_remove_node_from_matrix():
    graph = Graph(representation="matrix")

    graph.add_edge("A", "B")
    graph.add_edge("B", "C")

    graph.remove_node("B")

    assert graph.nodes == ["A", "C"]
    assert graph.get_neighbors("A") == []
    assert graph.get_neighbors("C") == []


def test_string_output():
    graph = Graph()

    graph.add_edge("A", "B")

    output = str(graph)

    assert "A: B" in output
    assert "B: A" in output


def test_invalid_representation():
    with pytest.raises(ValueError):
        Graph(representation="invalid")