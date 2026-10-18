"""Tests for Vertex Cover approximation algorithms."""

import pytest

from src.complexity.vertex_cover_approx import (
    approximation_ratio,
    exact_vertex_cover,
    is_vertex_cover,
    vertex_cover_2approx,
)


def test_triangle_approximation_is_cover():
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("A", "C"),
    ]

    cover = vertex_cover_2approx(
        edges
    )

    assert is_vertex_cover(
        edges,
        cover,
    )


def test_triangle_optimal_size():
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("A", "C"),
    ]

    optimal = exact_vertex_cover(
        edges
    )

    assert len(
        optimal
    ) == 2


def test_single_edge():
    edges = [
        ("A", "B"),
    ]

    cover = vertex_cover_2approx(
        edges
    )

    assert cover == {
        "A",
        "B",
    }


def test_path_graph():
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
    ]

    cover = vertex_cover_2approx(
        edges
    )

    assert is_vertex_cover(
        edges,
        cover,
    )


def test_star_graph():
    edges = [
        ("C", "A"),
        ("C", "B"),
        ("C", "D"),
        ("C", "E"),
    ]

    approximate = vertex_cover_2approx(
        edges
    )

    optimal = exact_vertex_cover(
        edges
    )

    assert is_vertex_cover(
        edges,
        approximate,
    )

    assert len(
        optimal
    ) == 1

    assert approximation_ratio(
        approximate,
        optimal,
    ) <= 2.0


def test_empty_graph():
    assert vertex_cover_2approx(
        []
    ) == set()

    assert exact_vertex_cover(
        []
    ) == set()


def test_approximation_ratio_triangle():
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("A", "C"),
    ]

    approximate = vertex_cover_2approx(
        edges
    )

    optimal = exact_vertex_cover(
        edges
    )

    ratio = approximation_ratio(
        approximate,
        optimal,
    )

    assert 1.0 <= ratio <= 2.0


def test_exact_cover_is_valid():
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "A"),
    ]

    optimal = exact_vertex_cover(
        edges
    )

    assert is_vertex_cover(
        edges,
        optimal,
    )


def test_invalid_edge_type():
    with pytest.raises(TypeError):
        vertex_cover_2approx(
            [
                ["A", "B"]
            ]
        )


def test_invalid_edge_length():
    with pytest.raises(ValueError):
        vertex_cover_2approx(
            [
                ("A", "B", "C")
            ]
        )


def test_invalid_vertex_type():
    with pytest.raises(TypeError):
        vertex_cover_2approx(
            [
                ("A", 2)
            ]
        )


def test_self_loop_rejected():
    with pytest.raises(ValueError):
        vertex_cover_2approx(
            [
                ("A", "A")
            ]
        )


def test_invalid_empty_optimal_ratio():
    with pytest.raises(ValueError):
        approximation_ratio(
            {
                "A"
            },
            set(),
        )