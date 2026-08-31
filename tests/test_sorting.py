"""Tests for the three required sorting algorithms."""

import pytest

from src.sorting.basic_sorts import (
    bubble_sort,
    insertion_sort,
    selection_sort,
)


ALGORITHMS = [
    bubble_sort,
    selection_sort,
    insertion_sort,
]


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_standard_cases(algorithm, sample_arrays):
    """Every algorithm should correctly sort all standard test cases."""
    for original in sample_arrays.values():
        data = original.copy()
        result = algorithm(data)

        assert result == sorted(original)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_original_list_is_not_modified(algorithm):
    """Sorting algorithms should preserve the original input list."""
    original = [3, 2, 1]
    data = original.copy()

    algorithm(data)

    assert data == original


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_returns_new_list(algorithm):
    """Sorting algorithms should return a new list object."""
    data = [3, 2, 1]

    result = algorithm(data)

    assert result == [1, 2, 3]
    assert result is not data


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_large_random_array(algorithm, large_random_array):
    """Every algorithm should correctly sort a larger random input."""
    original = large_random_array.copy()

    result = algorithm(original)

    assert result == sorted(large_random_array)


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_non_list_input_raises_type_error(algorithm):
    """Non-list input should raise a TypeError."""
    with pytest.raises(TypeError):
        algorithm((3, 2, 1))


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_incomparable_values_raise_type_error(algorithm):
    """Values that Python cannot compare should raise TypeError."""
    with pytest.raises(TypeError):
        algorithm([1, "two", 3])


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_empty_list_returns_new_empty_list(algorithm):
    """An empty list should remain empty and return a separate list object."""
    data = []

    result = algorithm(data)

    assert result == []
    assert result is not data


@pytest.mark.parametrize("algorithm", ALGORITHMS)
def test_single_item_returns_new_list(algorithm):
    """A one-element list should remain unchanged but be copied."""
    data = [42]

    result = algorithm(data)

    assert result == [42]
    assert result is not data