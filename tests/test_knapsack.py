"""Tests for 0/1 Knapsack implementations."""

import pytest

from src.dp.knapsack import (
    knapsack_memoized,
    knapsack_recursive,
    knapsack_tabulated,
    trace_solution,
)


WEIGHTS = [10, 20, 30]
VALUES = [60, 100, 120]
CAPACITY = 50


def test_knapsack_recursive():
    result = knapsack_recursive(
        WEIGHTS,
        VALUES,
        CAPACITY,
    )

    assert result == 220


def test_knapsack_memoized():
    result = knapsack_memoized(
        WEIGHTS,
        VALUES,
        CAPACITY,
    )

    assert result == 220


def test_knapsack_tabulated():
    result = knapsack_tabulated(
        WEIGHTS,
        VALUES,
        CAPACITY,
    )

    assert result == 220


def test_all_versions_match():
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 5

    recursive = knapsack_recursive(
        weights,
        values,
        capacity,
    )

    memoized = knapsack_memoized(
        weights,
        values,
        capacity,
    )

    tabulated = knapsack_tabulated(
        weights,
        values,
        capacity,
    )

    assert recursive == 7
    assert recursive == memoized
    assert memoized == tabulated


def test_trace_solution():
    selected = trace_solution(
        WEIGHTS,
        VALUES,
        CAPACITY,
    )

    assert selected == [1, 2]

    total_weight = sum(
        WEIGHTS[index]
        for index in selected
    )

    total_value = sum(
        VALUES[index]
        for index in selected
    )

    assert total_weight <= CAPACITY
    assert total_value == 220


def test_empty_items():
    assert knapsack_recursive([], [], 10) == 0
    assert knapsack_memoized([], [], 10) == 0
    assert knapsack_tabulated([], [], 10) == 0
    assert trace_solution([], [], 10) == []


def test_zero_capacity():
    assert (
        knapsack_recursive(
            WEIGHTS,
            VALUES,
            0,
        )
        == 0
    )

    assert (
        knapsack_memoized(
            WEIGHTS,
            VALUES,
            0,
        )
        == 0
    )

    assert (
        knapsack_tabulated(
            WEIGHTS,
            VALUES,
            0,
        )
        == 0
    )


def test_recursive_stats():
    stats = {}

    result = knapsack_recursive(
        WEIGHTS,
        VALUES,
        CAPACITY,
        stats=stats,
    )

    assert result == 220
    assert stats["calls"] > 1
    assert stats["max_depth"] > 1


def test_memoized_uses_fewer_calls():
    weights = [1, 2, 3, 4, 5, 6]
    values = [2, 4, 4, 5, 7, 8]
    capacity = 10

    recursive_stats = {}
    memoized_stats = {}

    knapsack_recursive(
        weights,
        values,
        capacity,
        stats=recursive_stats,
    )

    knapsack_memoized(
        weights,
        values,
        capacity,
        stats=memoized_stats,
    )

    assert (
        memoized_stats["calls"]
        < recursive_stats["calls"]
    )


def test_mismatched_lengths():
    with pytest.raises(ValueError):
        knapsack_recursive(
            [1, 2],
            [10],
            5,
        )


def test_negative_capacity():
    with pytest.raises(ValueError):
        knapsack_tabulated(
            [1, 2],
            [10, 20],
            -1,
        )


def test_negative_weight():
    with pytest.raises(ValueError):
        knapsack_memoized(
            [1, -2],
            [10, 20],
            5,
        )