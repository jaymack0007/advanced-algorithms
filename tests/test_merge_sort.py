"""Tests for merge sort and the merge helper function."""

import pytest

from src.sorting.merge_sort import merge, merge_sort


def test_merge_two_sorted_lists():
    """Merge should correctly combine two sorted lists."""
    left = [1, 3, 5]
    right = [2, 4, 6]

    result = merge(left, right)

    assert result == [1, 2, 3, 4, 5, 6]


def test_merge_with_empty_left():
    """Merge should work when the left list is empty."""
    assert merge([], [1, 2, 3]) == [1, 2, 3]


def test_merge_with_empty_right():
    """Merge should work when the right list is empty."""
    assert merge([1, 2, 3], []) == [1, 2, 3]


def test_merge_with_duplicates():
    """Merge should preserve duplicate values."""
    result = merge(
        [1, 2, 2, 5],
        [2, 3, 5],
    )

    assert result == [1, 2, 2, 2, 3, 5, 5]


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
def test_merge_sort_standard_cases(values):
    """Merge sort should correctly handle common and edge cases."""
    result = merge_sort(values)

    assert result == sorted(values)


def test_merge_sort_does_not_modify_original():
    """Merge sort should leave the original input unchanged."""
    original = [5, 2, 4, 1, 3]
    data = original.copy()

    result = merge_sort(data)

    assert result == [1, 2, 3, 4, 5]
    assert data == original


def test_merge_sort_returns_new_list():
    """Merge sort should return a different list object."""
    data = [3, 2, 1]

    result = merge_sort(data)

    assert result is not data


def test_merge_sort_all_equal():
    """Merge sort should correctly handle all-equal values."""
    data = [5] * 100

    assert merge_sort(data) == data


def test_merge_sort_large_input():
    """Merge sort should correctly sort a larger input."""
    data = list(range(1000, 0, -1))

    result = merge_sort(data)

    assert result == sorted(data)


def test_merge_sort_invalid_input():
    """Non-list input should raise TypeError."""
    with pytest.raises(TypeError):
        merge_sort((3, 2, 1))


def test_merge_sort_incomparable_values():
    """Incomparable list values should raise TypeError."""
    with pytest.raises(TypeError):
        merge_sort([1, "two", 3])