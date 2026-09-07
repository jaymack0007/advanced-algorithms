"""Comparison tests for all five sorting algorithms."""

import random

import pytest

from src.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
)


ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "QuickSort": quick_sort,
}


@pytest.mark.parametrize(
    "values",
    [
        [],
        [42],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [3, 1, 4, 1, 5, 9, 2, 6],
        [7, 7, 7, 7, 7],
        [-5, -1, -8, 0, 3],
        [3, -1, 4, 0, -2, 7],
    ],
)
def test_all_algorithms_match_python_sorted(values):
    """Every sorting algorithm should match Python's sorted result."""
    expected = sorted(values)

    for name, algorithm in ALGORITHMS.items():
        result = algorithm(values)

        assert result == expected, (
            f"{name} produced {result}, "
            f"but expected {expected}"
        )


def test_all_algorithms_preserve_original_input():
    """All algorithms should leave the original input unchanged."""
    original = [5, 2, 9, 1, 5, 6]

    for name, algorithm in ALGORITHMS.items():
        data = original.copy()

        algorithm(data)

        assert data == original, (
            f"{name} modified the original input"
        )


def test_all_algorithms_random_data():
    """All algorithms should correctly sort the same random data."""
    rng = random.Random(42)

    data = [
        rng.randint(-1000, 1000)
        for _ in range(500)
    ]

    expected = sorted(data)

    for name, algorithm in ALGORITHMS.items():
        assert algorithm(data) == expected, (
            f"{name} failed on random data"
        )


def test_all_algorithms_many_duplicates():
    """All algorithms should correctly handle many duplicate values."""
    rng = random.Random(42)

    data = [
        rng.randint(1, 10)
        for _ in range(500)
    ]

    expected = sorted(data)

    for name, algorithm in ALGORITHMS.items():
        assert algorithm(data) == expected, (
            f"{name} failed on duplicate data"
        )


def test_all_algorithms_few_unique_values():
    """All algorithms should correctly handle only three unique values."""
    rng = random.Random(42)

    data = [
        rng.choice([1, 2, 3])
        for _ in range(500)
    ]

    expected = sorted(data)

    for name, algorithm in ALGORITHMS.items():
        assert algorithm(data) == expected, (
            f"{name} failed on few-unique data"
        )


def test_all_algorithms_reverse_data():
    """All algorithms should correctly sort reverse-ordered data."""
    data = list(range(500, 0, -1))
    expected = sorted(data)

    for name, algorithm in ALGORITHMS.items():
        assert algorithm(data) == expected, (
            f"{name} failed on reverse data"
        )