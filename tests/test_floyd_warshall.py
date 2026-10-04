"""Tests for the Floyd-Warshall algorithm."""

from math import inf

import pytest

from src.dp_advanced.floyd_warshall import (
    floyd_warshall,
    reconstruct_path,
)


def test_basic_shortest_paths():
    graph = [
        [0, 5, inf, 10],
        [inf, 0, 3, inf],
        [inf, inf, 0, 1],
        [inf, inf, inf, 0],
    ]

    distance, _ = floyd_warshall(
        graph
    )

    assert distance[0][2] == 8
    assert distance[0][3] == 9
    assert distance[1][3] == 4


def test_distance_matrix_expected():
    graph = [
        [0, 5, inf, 10],
        [inf, 0, 3, inf],
        [inf, inf, 0, 1],
        [inf, inf, inf, 0],
    ]

    distance, _ = floyd_warshall(
        graph
    )

    expected = [
        [0, 5, 8, 9],
        [inf, 0, 3, 4],
        [inf, inf, 0, 1],
        [inf, inf, inf, 0],
    ]

    assert distance == expected


def test_reconstruct_path():
    graph = [
        [0, 5, inf, 10],
        [inf, 0, 3, inf],
        [inf, inf, 0, 1],
        [inf, inf, inf, 0],
    ]

    _, predecessor = floyd_warshall(
        graph
    )

    path = reconstruct_path(
        predecessor,
        0,
        3,
    )

    assert path == [0, 1, 2, 3]


def test_direct_path():
    graph = [
        [0, 2],
        [inf, 0],
    ]

    _, predecessor = floyd_warshall(
        graph
    )

    assert reconstruct_path(
        predecessor,
        0,
        1,
    ) == [0, 1]


def test_unreachable_path():
    graph = [
        [0, inf],
        [inf, 0],
    ]

    _, predecessor = floyd_warshall(
        graph
    )

    assert reconstruct_path(
        predecessor,
        0,
        1,
    ) == []


def test_same_start_and_end():
    graph = [
        [0, 2],
        [2, 0],
    ]

    _, predecessor = floyd_warshall(
        graph
    )

    assert reconstruct_path(
        predecessor,
        1,
        1,
    ) == [1]


def test_negative_edge_without_cycle():
    graph = [
        [0, 1, 4, inf],
        [inf, 0, -2, 5],
        [inf, inf, 0, 2],
        [inf, inf, inf, 0],
    ]

    distance, predecessor = (
        floyd_warshall(graph)
    )

    assert distance[0][2] == -1
    assert distance[0][3] == 1

    assert reconstruct_path(
        predecessor,
        0,
        3,
    ) == [0, 1, 2, 3]


def test_negative_cycle_detected():
    graph = [
        [0, -1],
        [-1, 0],
    ]

    with pytest.raises(ValueError):
        floyd_warshall(graph)


def test_original_matrix_not_modified():
    graph = [
        [0, 5, inf],
        [inf, 0, 2],
        [inf, inf, 0],
    ]

    original = [
        row.copy()
        for row in graph
    ]

    floyd_warshall(graph)

    assert graph == original


def test_non_square_matrix():
    graph = [
        [0, 1, 2],
        [1, 0],
    ]

    with pytest.raises(ValueError):
        floyd_warshall(graph)


def test_empty_graph():
    with pytest.raises(ValueError):
        floyd_warshall([])


def test_invalid_path_vertex():
    graph = [
        [0, 1],
        [1, 0],
    ]

    _, predecessor = floyd_warshall(
        graph
    )

    with pytest.raises(IndexError):
        reconstruct_path(
            predecessor,
            0,
            5,
        )