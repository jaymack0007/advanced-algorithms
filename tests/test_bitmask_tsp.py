"""Tests for Traveling Salesman implementations."""

import pytest

from src.dp_advanced.bitmask_traveling_salesman import (
    tsp_bitmask,
    tsp_brute_force,
)


DISTANCES = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0],
]


def test_bitmask_known_cost():
    cost, tour = tsp_bitmask(
        DISTANCES
    )

    assert cost == 80
    assert tour[0] == 0
    assert tour[-1] == 0


def test_brute_force_known_cost():
    cost, tour = tsp_brute_force(
        DISTANCES
    )

    assert cost == 80
    assert tour[0] == 0
    assert tour[-1] == 0


def test_algorithms_match():
    bitmask_cost, _ = tsp_bitmask(
        DISTANCES
    )

    brute_cost, _ = tsp_brute_force(
        DISTANCES
    )

    assert bitmask_cost == brute_cost


def test_tour_visits_each_city():
    _, tour = tsp_bitmask(
        DISTANCES
    )

    visited = tour[:-1]

    assert len(visited) == 4
    assert set(visited) == {
        0,
        1,
        2,
        3,
    }


def test_different_start_city():
    bitmask_cost, tour = tsp_bitmask(
        DISTANCES,
        start=2,
    )

    brute_cost, _ = tsp_brute_force(
        DISTANCES,
        start=2,
    )

    assert bitmask_cost == brute_cost
    assert tour[0] == 2
    assert tour[-1] == 2


def test_single_city():
    distances = [
        [0],
    ]

    assert tsp_bitmask(
        distances
    ) == (
        0,
        [0, 0],
    )

    assert tsp_brute_force(
        distances
    ) == (
        0,
        [0, 0],
    )


def test_three_cities():
    distances = [
        [0, 2, 9],
        [1, 0, 6],
        [15, 7, 0],
    ]

    bitmask_cost, _ = tsp_bitmask(
        distances
    )

    brute_cost, _ = tsp_brute_force(
        distances
    )

    assert bitmask_cost == brute_cost
    assert bitmask_cost == 17


def test_asymmetric_matrix():
    distances = [
        [0, 1, 10, 10],
        [10, 0, 1, 10],
        [10, 10, 0, 1],
        [1, 10, 10, 0],
    ]

    cost, tour = tsp_bitmask(
        distances
    )

    assert cost == 4
    assert tour == [
        0,
        1,
        2,
        3,
        0,
    ]


def test_empty_matrix():
    with pytest.raises(ValueError):
        tsp_bitmask([])


def test_non_square_matrix():
    distances = [
        [0, 1, 2],
        [1, 0],
    ]

    with pytest.raises(ValueError):
        tsp_brute_force(
            distances
        )


def test_negative_distance():
    distances = [
        [0, -1],
        [1, 0],
    ]

    with pytest.raises(ValueError):
        tsp_bitmask(
            distances
        )


def test_invalid_start():
    with pytest.raises(IndexError):
        tsp_bitmask(
            DISTANCES,
            start=5,
        )