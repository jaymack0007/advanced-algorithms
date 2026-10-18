"""Tests for TSP nearest-neighbor and exact solvers."""

import pytest

from src.complexity.traveling_salesman_approx import (
    approximation_ratio,
    euclidean_distance,
    exact_tsp,
    nearest_neighbor_tsp,
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
    distance = euclidean_distance(
        (
            0.0,
            0.0,
        ),
        (
            3.0,
            4.0,
        ),
    )

    assert distance == 5.0


def test_nearest_neighbor_returns_closed_tour():
    tour, _ = nearest_neighbor_tsp(
        SQUARE,
        start="A",
    )

    assert tour[0] == "A"
    assert tour[-1] == "A"


def test_nearest_neighbor_visits_all_cities():
    tour, _ = nearest_neighbor_tsp(
        SQUARE,
        start="A",
    )

    assert set(
        tour[:-1]
    ) == set(
        SQUARE
    )


def test_square_nearest_neighbor_length():
    _, length = nearest_neighbor_tsp(
        SQUARE,
        start="A",
    )

    assert length == pytest.approx(
        4.0
    )


def test_exact_square_length():
    _, length = exact_tsp(
        SQUARE,
        start="A",
    )

    assert length == pytest.approx(
        4.0
    )


def test_square_ratio_is_one():
    _, approximate = nearest_neighbor_tsp(
        SQUARE,
        start="A",
    )

    _, optimal = exact_tsp(
        SQUARE,
        start="A",
    )

    assert approximation_ratio(
        approximate,
        optimal,
    ) == pytest.approx(
        1.0
    )


def test_tour_length():
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


def test_single_city():
    points = {
        "A": (
            0.0,
            0.0,
        )
    }

    tour, length = nearest_neighbor_tsp(
        points
    )

    assert tour == [
        "A",
        "A",
    ]

    assert length == 0.0


def test_exact_single_city():
    points = {
        "A": (
            0.0,
            0.0,
        )
    }

    tour, length = exact_tsp(
        points
    )

    assert tour == [
        "A",
        "A",
    ]

    assert length == 0.0


def test_default_start_is_deterministic():
    first, _ = nearest_neighbor_tsp(
        SQUARE
    )

    second, _ = nearest_neighbor_tsp(
        SQUARE
    )

    assert first == second
    assert first[0] == "A"


def test_unknown_start_rejected():
    with pytest.raises(ValueError):
        nearest_neighbor_tsp(
            SQUARE,
            start="Z",
        )


def test_empty_points_rejected():
    with pytest.raises(ValueError):
        nearest_neighbor_tsp(
            {}
        )


def test_invalid_points_type():
    with pytest.raises(TypeError):
        nearest_neighbor_tsp(
            [
                (
                    0,
                    0,
                )
            ]
        )


def test_invalid_coordinate_length():
    with pytest.raises(ValueError):
        nearest_neighbor_tsp(
            {
                "A": (
                    0,
                    1,
                    2,
                )
            }
        )


def test_invalid_ratio():
    with pytest.raises(ValueError):
        approximation_ratio(
            5.0,
            0.0,
        )