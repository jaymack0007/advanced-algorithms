"""Tests for Subset Sum backtracking and heuristic solutions."""

import pytest

from src.complexity.subset_sum_backtracking import (
    greedy_subset_sum,
    subset_sum_backtracking,
    subset_sum_is_valid,
)


def test_exact_solution_found():
    values = [
        3,
        34,
        4,
        12,
        5,
        2,
    ]

    result = subset_sum_backtracking(
        values,
        9,
    )

    assert result is not None
    assert sum(result) == 9


def test_exact_no_solution():
    values = [
        2,
        4,
        6,
    ]

    result = subset_sum_backtracking(
        values,
        5,
    )

    assert result is None


def test_target_zero():
    result = subset_sum_backtracking(
        [
            1,
            2,
            3,
        ],
        0,
    )

    assert result == []


def test_empty_list_target_zero():
    result = subset_sum_backtracking(
        [],
        0,
    )

    assert result == []


def test_empty_list_no_solution():
    result = subset_sum_backtracking(
        [],
        10,
    )

    assert result is None


def test_duplicate_values():
    result = subset_sum_backtracking(
        [
            5,
            5,
            5,
        ],
        10,
    )

    assert result is not None
    assert sum(result) == 10


def test_original_not_modified():
    values = [
        8,
        3,
        6,
        2,
    ]

    original = values.copy()

    subset_sum_backtracking(
        values,
        11,
    )

    assert values == original


def test_stats_recorded():
    stats = {}

    result = subset_sum_backtracking(
        [
            1,
            2,
            4,
        ],
        6,
        stats=stats,
    )

    assert result is not None
    assert stats["nodes_visited"] > 0
    assert stats["max_depth"] > 0


def test_greedy_solution_found():
    result = greedy_subset_sum(
        [
            8,
            7,
            6,
            5,
        ],
        13,
    )

    assert result is not None
    assert sum(result) == 13


def test_greedy_can_miss_existing_solution():
    values = [
        6,
        4,
        3,
    ]

    exact = subset_sum_backtracking(
        values,
        7,
    )

    greedy = greedy_subset_sum(
        values,
        7,
    )

    assert exact is not None
    assert sum(exact) == 7
    assert greedy is None


def test_subset_validation():
    assert subset_sum_is_valid(
        [
            2,
            3,
        ],
        5,
    )

    assert not subset_sum_is_valid(
        None,
        5,
    )


def test_invalid_values_type():
    with pytest.raises(TypeError):
        subset_sum_backtracking(
            "not a list",
            5,
        )


def test_negative_value_rejected():
    with pytest.raises(ValueError):
        subset_sum_backtracking(
            [
                1,
                -2,
                3,
            ],
            4,
        )


def test_negative_target_rejected():
    with pytest.raises(ValueError):
        subset_sum_backtracking(
            [
                1,
                2,
                3,
            ],
            -1,
        )


def test_non_integer_value_rejected():
    with pytest.raises(TypeError):
        greedy_subset_sum(
            [
                1,
                2.5,
                3,
            ],
            4,
        )