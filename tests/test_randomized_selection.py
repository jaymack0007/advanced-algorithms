"""Tests for Randomized QuickSelect."""

import pytest

from src.randomized.randomized_selection import (
    deterministic_select,
    randomized_select,
)


VALUES = [
    9,
    1,
    7,
    3,
    5,
    2,
    8,
    6,
    4,
]


def test_randomized_minimum():
    assert randomized_select(
        VALUES,
        1,
        seed=42,
    ) == 1


def test_randomized_median():
    assert randomized_select(
        VALUES,
        5,
        seed=42,
    ) == 5


def test_randomized_maximum():
    assert randomized_select(
        VALUES,
        9,
        seed=42,
    ) == 9


def test_deterministic_minimum():
    assert deterministic_select(
        VALUES,
        1,
    ) == 1


def test_deterministic_median():
    assert deterministic_select(
        VALUES,
        5,
    ) == 5


def test_deterministic_maximum():
    assert deterministic_select(
        VALUES,
        9,
    ) == 9


def test_duplicates():
    values = [
        4,
        2,
        4,
        1,
        2,
        4,
    ]

    expected = sorted(values)

    for k in range(
        1,
        len(values) + 1,
    ):
        assert randomized_select(
            values,
            k,
            seed=42,
        ) == expected[k - 1]


def test_original_not_modified():
    values = [
        5,
        1,
        4,
        2,
        3,
    ]

    original = values.copy()

    randomized_select(
        values,
        3,
        seed=42,
    )

    assert values == original


def test_seed_is_reproducible():
    first_stats = {}
    second_stats = {}

    first = randomized_select(
        VALUES,
        5,
        seed=100,
        stats=first_stats,
    )

    second = randomized_select(
        VALUES,
        5,
        seed=100,
        stats=second_stats,
    )

    assert first == second
    assert first_stats == second_stats


def test_statistics_recorded():
    stats = {}

    result = randomized_select(
        VALUES,
        5,
        seed=42,
        stats=stats,
    )

    assert result == 5
    assert stats["comparisons"] > 0
    assert stats["max_depth"] > 0


def test_invalid_k_too_small():
    with pytest.raises(ValueError):
        randomized_select(
            VALUES,
            0,
        )


def test_invalid_k_too_large():
    with pytest.raises(ValueError):
        randomized_select(
            VALUES,
            10,
        )


def test_empty_input():
    with pytest.raises(ValueError):
        randomized_select(
            [],
            1,
        )


def test_invalid_input_type():
    with pytest.raises(TypeError):
        randomized_select(
            "not a list",
            1,
        )