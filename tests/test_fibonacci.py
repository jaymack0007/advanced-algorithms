"""Tests for Fibonacci implementations."""

import pytest

from src.dp.fibonacci import (
    fibonacci_memoized,
    fibonacci_recursive,
    fibonacci_tabulated,
)


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (5, 5),
        (10, 55),
        (20, 6765),
    ],
)
def test_fibonacci_recursive(n, expected):
    assert fibonacci_recursive(n) == expected


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (5, 5),
        (10, 55),
        (20, 6765),
        (45, 1134903170),
    ],
)
def test_fibonacci_memoized(n, expected):
    assert fibonacci_memoized(n) == expected


@pytest.mark.parametrize(
    "n, expected",
    [
        (0, 0),
        (1, 1),
        (2, 1),
        (5, 5),
        (10, 55),
        (20, 6765),
        (45, 1134903170),
    ],
)
def test_fibonacci_tabulated(n, expected):
    assert fibonacci_tabulated(n) == expected


def test_all_versions_match():
    for n in range(15):
        assert fibonacci_recursive(n) == fibonacci_memoized(n)
        assert fibonacci_memoized(n) == fibonacci_tabulated(n)


def test_recursive_stats():
    stats = {}

    result = fibonacci_recursive(
        5,
        stats=stats,
    )

    assert result == 5
    assert stats["calls"] > 1
    assert stats["max_depth"] > 1


def test_memoized_uses_fewer_calls():
    recursive_stats = {}
    memoized_stats = {}

    fibonacci_recursive(
        10,
        stats=recursive_stats,
    )

    fibonacci_memoized(
        10,
        stats=memoized_stats,
    )

    assert (
        memoized_stats["calls"]
        < recursive_stats["calls"]
    )


def test_negative_input():
    with pytest.raises(ValueError):
        fibonacci_recursive(-1)

    with pytest.raises(ValueError):
        fibonacci_memoized(-1)

    with pytest.raises(ValueError):
        fibonacci_tabulated(-1)


def test_non_integer_input():
    with pytest.raises(TypeError):
        fibonacci_recursive(5.5)