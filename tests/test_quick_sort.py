"""Tests for randomized QuickSort."""

import pytest

from src.sorting.quick_sort import (
    INSERTION_SORT_THRESHOLD,
    partition,
    quick_sort,
)


@pytest.mark.parametrize(
    "values",
    [
        [],
        [42],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 4, 1, 5, 9, 2, 6],
        [7, 7, 7, 7, 7],
        [-5, -1, -8, 0, 3],
        [3, -1, 4, 0, -2, 7],
    ],
)
def test_quick_sort_standard_cases(values):
    """QuickSort should handle common and edge cases."""
    result = quick_sort(values)

    assert result == sorted(values)


def test_quick_sort_does_not_modify_original():
    """QuickSort should preserve the original list."""
    original = [5, 2, 4, 1, 3]
    data = original.copy()

    result = quick_sort(data)

    assert result == [1, 2, 3, 4, 5]
    assert data == original


def test_quick_sort_returns_new_list():
    """QuickSort should return a different list object."""
    data = [3, 2, 1]

    result = quick_sort(data)

    assert result is not data


def test_quick_sort_all_equal():
    """QuickSort should efficiently handle equal values."""
    data = [5] * 1000

    assert quick_sort(data) == data


def test_quick_sort_many_duplicates():
    """QuickSort should correctly handle many duplicate values."""
    data = [
        3, 1, 2, 3, 1, 2, 3, 1, 2, 3,
        1, 2, 3, 1, 2, 3, 1, 2, 3, 1,
    ]

    assert quick_sort(data) == sorted(data)


def test_quick_sort_large_input():
    """QuickSort should correctly sort a larger input."""
    data = list(range(5000, 0, -1))

    assert quick_sort(data) == sorted(data)


def test_quick_sort_invalid_input():
    """Non-list input should raise TypeError."""
    with pytest.raises(TypeError):
        quick_sort((3, 2, 1))


def test_quick_sort_incomparable_values():
    """Incomparable values should raise TypeError."""
    with pytest.raises(TypeError):
        quick_sort([1, "two", 3])


def test_partition_correctness():
    """
    Values returned by partition should be correctly separated
    around the pivot section.
    """
    data = [
        5, 2, 7, 3, 5, 1, 5, 9, 4,
        5, 8, 6,
    ]

    equal_start, equal_end = partition(
        data,
        0,
        len(data) - 1,
    )

    pivot_value = data[equal_start]

    assert all(
        value < pivot_value
        for value in data[:equal_start]
    )

    assert all(
        value == pivot_value
        for value in data[equal_start:equal_end + 1]
    )

    assert all(
        value > pivot_value
        for value in data[equal_end + 1:]
    )


def test_insertion_sort_threshold():
    """The hybrid QuickSort threshold should be approximately 10."""
    assert 8 <= INSERTION_SORT_THRESHOLD <= 15