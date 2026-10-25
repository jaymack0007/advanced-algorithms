"""Tests for the Week 9 Vertex Cover approximation."""

import pytest

from src.approximation.vertex_cover_2approx import (
    approximation_ratio,
    exact_vertex_cover,
    is_vertex_cover,
    maximal_matching,
    vertex_cover_2approx,
)


def test_triangle_is_covered():
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


def test_single_edge_uses_both_endpoints():
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


def test_star_graph_ratio_is_two():
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

    assert len(
        optimal
    ) == 1

    assert approximation_ratio(
        approximate,
        optimal,
    ) == 2.0


def test_cycle_graph_ratio_at_most_two():
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "A"),
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


def test_matching_edges_are_disjoint():
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "E"),
        ("E", "F"),
    ]

    matching = maximal_matching(
        edges
    )

    used = set()

    for first, second in matching:
        assert first not in used
        assert second not in used

        used.add(
            first
        )

        used.add(
            second
        )


def test_cover_has_two_vertices_per_matching_edge():
    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "E"),
    ]

    matching = maximal_matching(
        edges
    )

    cover = vertex_cover_2approx(
        edges
    )

    assert len(
        cover
    ) == 2 * len(
        matching
    )


def test_empty_graph():
    assert maximal_matching(
        []
    ) == []

    assert vertex_cover_2approx(
        []
    ) == set()

    assert exact_vertex_cover(
        []
    ) == set()


def test_empty_graph_ratio():
    assert approximation_ratio(
        set(),
        set(),
    ) == 1.0


def test_exact_cover_is_valid():
    edges = [
        ("A", "B"),
        ("A", "C"),
        ("B", "D"),
        ("C", "D"),
    ]

    optimal = exact_vertex_cover(
        edges
    )

    assert is_vertex_cover(
        edges,
        optimal,
    )


def test_invalid_edge_collection_type():
    with pytest.raises(TypeError):
        vertex_cover_2approx(
            {
                ("A", "B")
            }
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
                (
                    "A",
                    "B",
                    "C",
                )
            ]
        )


def test_self_loop_rejected():
    with pytest.raises(ValueError):
        vertex_cover_2approx(
            [
                (
                    "A",
                    "A",
                )
            ]
        )


def test_invalid_ratio_for_nonempty_approximation():
    with pytest.raises(ValueError):
        approximation_ratio(
            {
                "A"
            },
            set(),
        )