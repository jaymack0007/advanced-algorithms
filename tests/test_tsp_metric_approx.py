"""Tests for the metric TSP MST-doubling approximation."""

import pytest

from src.approximation.tsp_metric_approx import (
    approximation_ratio,
    euclidean_distance,
    exact_metric_tsp,
    minimum_spanning_tree,
    mst_doubling_tsp,
    preorder_walk,
    tour_length,
)


SQUARE = {
    "A": (
        0.0,
        0.0,
    ),
    "B": (
        1.0,
        0.0,
    ),
    "C": (
        1.0,
        1.0,
    ),
    "D": (
        0.0,
        1.0,
    ),
}


def test_euclidean_distance():
    assert euclidean_distance(
        (
            0.0,
            0.0,
        ),
        (
            3.0,
            4.0,
        ),
    ) == 5.0


def test_mst_has_n_minus_one_edges():
    edges = minimum_spanning_tree(
        SQUARE,
        start="A",
    )

    assert len(
        edges
    ) == 3


def test_mst_contains_all_vertices():
    edges = minimum_spanning_tree(
        SQUARE,
        start="A",
    )

    vertices = set()

    for first, second in edges:
        vertices.add(
            first
        )

        vertices.add(
            second
        )

    assert vertices == set(
        SQUARE
    )


def test_preorder_visits_every_vertex_once():
    edges = minimum_spanning_tree(
        SQUARE,
        start="A",
    )

    order = preorder_walk(
        SQUARE,
        edges,
        "A",
    )

    assert len(
        order
    ) == len(
        SQUARE
    )

    assert set(
        order
    ) == set(
        SQUARE
    )


def test_approximation_returns_closed_tour():
    tour, _ = mst_doubling_tsp(
        SQUARE,
        start="A",
    )

    assert tour[0] == "A"
    assert tour[-1] == "A"


def test_approximation_visits_all_vertices():
    tour, _ = mst_doubling_tsp(
        SQUARE,
        start="A",
    )

    assert set(
        tour[:-1]
    ) == set(
        SQUARE
    )

    assert len(
        tour[:-1]
    ) == len(
        SQUARE
    )


def test_square_optimal_cost():
    _, cost = exact_metric_tsp(
        SQUARE,
        start="A",
    )

    assert cost == pytest.approx(
        4.0
    )


def test_square_approximation_ratio_within_two():
    _, approximate = mst_doubling_tsp(
        SQUARE,
        start="A",
    )

    _, optimal = exact_metric_tsp(
        SQUARE,
        start="A",
    )

    ratio = approximation_ratio(
        approximate,
        optimal,
    )

    assert 1.0 <= ratio <= 2.0


def test_tour_length_square():
    tour = [
        "A",
        "B",
        "C",
        "D",
        "A",
    ]

    assert tour_length(
        SQUARE,
        tour,
    ) == pytest.approx(
        4.0
    )


def test_single_point():
    points = {
        "A": (
            0.0,
            0.0,
        )
    }

    tour, cost = mst_doubling_tsp(
        points
    )

    assert tour == [
        "A",
        "A",
    ]

    assert cost == 0.0


def test_single_point_exact():
    points = {
        "A": (
            0.0,
            0.0,
        )
    }

    tour, cost = exact_metric_tsp(
        points
    )

    assert tour == [
        "A",
        "A",
    ]

    assert cost == 0.0


def test_default_start_is_deterministic():
    first, _ = mst_doubling_tsp(
        SQUARE
    )

    second, _ = mst_doubling_tsp(
        SQUARE
    )

    assert first == second
    assert first[0] == "A"


def test_unknown_start_rejected():
    with pytest.raises(ValueError):
        mst_doubling_tsp(
            SQUARE,
            start="Z",
        )


def test_empty_points_rejected():
    with pytest.raises(ValueError):
        mst_doubling_tsp(
            {}
        )


def test_invalid_coordinate_rejected():
    with pytest.raises(ValueError):
        mst_doubling_tsp(
            {
                "A": (
                    0.0,
                    1.0,
                    2.0,
                )
            }
        )


def test_invalid_ratio():
    with pytest.raises(ValueError):
        approximation_ratio(
            5.0,
            0.0,
        )