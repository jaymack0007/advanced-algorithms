"""Tests for the Week 4 graph benchmark framework."""

from benchmarks.week4_graph_benchmark import (
    benchmark_dijkstra,
    benchmark_representations,
    benchmark_traversals,
    build_list_path_graph,
    build_matrix_path_graph,
)


def test_list_path_graph():
    graph = build_list_path_graph(10)

    assert len(graph.nodes) == 10
    assert graph.get_neighbors(0) == [1]
    assert set(graph.get_neighbors(5)) == {4, 6}


def test_matrix_path_graph():
    graph = build_matrix_path_graph(10)

    assert len(graph.nodes) == 10
    assert graph.get_neighbors(0) == [1]
    assert set(graph.get_neighbors(5)) == {4, 6}


def test_representation_benchmark():
    results = benchmark_representations([20])

    assert len(results) == 2

    algorithms = {
        row["algorithm"]
        for row in results
    }

    assert algorithms == {
        "Adjacency List",
        "Adjacency Matrix",
    }

    for row in results:
        assert row["time_seconds"] >= 0
        assert row["memory_bytes"] > 0


def test_traversal_benchmark():
    results = benchmark_traversals([20])

    assert len(results) == 4

    algorithms = {
        row["algorithm"]
        for row in results
    }

    graph_types = {
        row["graph_type"]
        for row in results
    }

    assert algorithms == {"BFS", "DFS"}
    assert graph_types == {"Sparse", "Dense"}

    for row in results:
        assert row["time_seconds"] >= 0
        assert row["memory_bytes"] >= 0


def test_dijkstra_benchmark():
    results = benchmark_dijkstra(
        [20],
        [0.05],
    )

    assert len(results) == 2

    algorithms = {
        row["algorithm"]
        for row in results
    }

    assert algorithms == {
        "Heap Priority Queue",
        "List Priority Queue",
    }

    for row in results:
        assert row["time_seconds"] >= 0
        assert row["density"] == 0.05