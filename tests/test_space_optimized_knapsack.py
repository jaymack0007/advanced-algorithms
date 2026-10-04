"""Tests for space-optimized 0/1 Knapsack."""

import pytest

from src.dp.knapsack import (
    knapsack_tabulated,
)
from src.dp_advanced.space_optimized_knapsack import (
    space_optimized_knapsack,
)


def test_standard_example():
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    assert (
        space_optimized_knapsack(
            weights,
            values,
            capacity,
        )
        == 220
    )


def test_matches_week5_tabulation():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5

    optimized = space_optimized_knapsack(
        weights,
        values,
        capacity,
    )

    standard = knapsack_tabulated(
        weights,
        values,
        capacity,
    )

    assert optimized == standard
    assert optimized == 7


def test_empty_items():
    assert (
        space_optimized_knapsack(
            [],
            [],
            10,
        )
        == 0
    )


def test_zero_capacity():
    assert (
        space_optimized_knapsack(
            [1, 2, 3],
            [10, 20, 30],
            0,
        )
        == 0
    )


def test_single_item_fits():
    assert (
        space_optimized_knapsack(
            [5],
            [25],
            5,
        )
        == 25
    )


def test_single_item_does_not_fit():
    assert (
        space_optimized_knapsack(
            [6],
            [25],
            5,
        )
        == 0
    )


def test_item_not_reused():
    result = space_optimized_knapsack(
        [2],
        [10],
        6,
    )

    assert result == 10


def test_multiple_items():
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7

    assert (
        space_optimized_knapsack(
            weights,
            values,
            capacity,
        )
        == 9
    )


def test_mismatched_lengths():
    with pytest.raises(ValueError):
        space_optimized_knapsack(
            [1, 2],
            [10],
            5,
        )


def test_negative_capacity():
    with pytest.raises(ValueError):
        space_optimized_knapsack(
            [1, 2],
            [10, 20],
            -1,
        )


def test_negative_weight():
    with pytest.raises(ValueError):
        space_optimized_knapsack(
            [1, -2],
            [10, 20],
            5,
        )