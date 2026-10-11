"""Tests for Randomized QuickSort."""

import pytest

from src.randomized.randomized_quicksort import (
    deterministic_quicksort,
    randomized_quicksort,
)


def test_randomized_basic():
    values = [
        5,
        3,
        8,
        1,
        2,
    ]

    assert randomized_quicksort(
        values,
        seed=42,
    ) == [
        1,
        2,
        3,
        5,
        8,
    ]


def test_deterministic_basic():
    values = [
        5,
        3,
        8,
        1,
        2,
    ]

    assert deterministic_quicksort(
        values
    ) == [
        1,
        2,
        3,
        5,
        8,
    ]


def test_empty_list():
    assert randomized_quicksort(
        [],
        seed=42,
    ) == []


def test_single_value():
    assert randomized_quicksort(
        [10],
        seed=42,
    ) == [10]


def test_duplicates():
    values = [
        4,
        2,
        4,
        1,
        2,
        4,
    ]

    assert randomized_quicksort(
        values,
        seed=42,
    ) == sorted(values)


def test_negative_values():
    values = [
        -4,
        8,
        -1,
        0,
        3,
    ]

    assert randomized_quicksort(
        values,
        seed=42,
    ) == sorted(values)


def test_already_sorted():
    values = list(
        range(25)
    )

    assert randomized_quicksort(
        values,
        seed=42,
    ) == values


def test_reverse_sorted():
    values = list(
        range(25, 0, -1)
    )

    assert randomized_quicksort(
        values,
        seed=42,
    ) == sorted(values)


def test_original_not_modified():
    values = [
        3,
        1,
        2,
    ]

    original = values.copy()

    randomized_quicksort(
        values,
        seed=42,
    )

    assert values == original


def test_returns_new_list():
    values = [
        1,
        2,
        3,
    ]

    result = randomized_quicksort(
        values,
        seed=42,
    )

    assert result is not values


def test_seed_is_reproducible():
    values = list(
        range(30, 0, -1)
    )

    first_stats = {}
    second_stats = {}

    first = randomized_quicksort(
        values,
        seed=100,
        stats=first_stats,
    )

    second = randomized_quicksort(
        values,
        seed=100,
        stats=second_stats,
    )

    assert first == second
    assert first_stats == second_stats


def test_statistics_recorded():
    stats = {}

    result = randomized_quicksort(
        [5, 1, 4, 2, 3],
        seed=42,
        stats=stats,
    )

    assert result == [
        1,
        2,
        3,
        4,
        5,
    ]

    assert stats["comparisons"] > 0
    assert stats["max_depth"] > 0


def test_deterministic_statistics():
    stats = {}

    deterministic_quicksort(
        [4, 3, 2, 1],
        stats=stats,
    )

    assert stats["comparisons"] > 0
    assert stats["max_depth"] > 0


def test_invalid_input():
    with pytest.raises(TypeError):
        randomized_quicksort(
            "not a list"
        )