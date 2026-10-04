"""Tests for Matrix Chain Multiplication."""

import pytest

from src.dp_advanced.matrix_chain_multiplication import (
    matrix_chain_bottom_up,
    matrix_chain_memoized,
)


def test_classic_example_memoized():
    dimensions = [
        30,
        35,
        15,
        5,
        10,
        20,
        25,
    ]

    cost, order = matrix_chain_memoized(
        dimensions
    )

    assert cost == 15125
    assert (
        order
        == "((A1(A2A3))((A4A5)A6))"
    )


def test_classic_example_bottom_up():
    dimensions = [
        30,
        35,
        15,
        5,
        10,
        20,
        25,
    ]

    cost, order = matrix_chain_bottom_up(
        dimensions
    )

    assert cost == 15125
    assert (
        order
        == "((A1(A2A3))((A4A5)A6))"
    )


def test_two_matrices():
    dimensions = [
        10,
        20,
        30,
    ]

    memoized = matrix_chain_memoized(
        dimensions
    )

    bottom_up = matrix_chain_bottom_up(
        dimensions
    )

    assert memoized == (
        6000,
        "(A1A2)",
    )

    assert bottom_up == memoized


def test_single_matrix():
    dimensions = [
        10,
        20,
    ]

    assert matrix_chain_memoized(
        dimensions
    ) == (
        0,
        "A1",
    )

    assert matrix_chain_bottom_up(
        dimensions
    ) == (
        0,
        "A1",
    )


def test_three_matrices():
    dimensions = [
        10,
        30,
        5,
        60,
    ]

    memoized = matrix_chain_memoized(
        dimensions
    )

    bottom_up = matrix_chain_bottom_up(
        dimensions
    )

    assert memoized[0] == 4500
    assert bottom_up[0] == 4500
    assert memoized == bottom_up


def test_methods_match():
    dimensions = [
        5,
        10,
        3,
        12,
        5,
        50,
        6,
    ]

    assert (
        matrix_chain_memoized(
            dimensions
        )
        == matrix_chain_bottom_up(
            dimensions
        )
    )


def test_equal_dimensions():
    dimensions = [
        10,
        10,
        10,
        10,
    ]

    memoized_cost, _ = (
        matrix_chain_memoized(
            dimensions
        )
    )

    bottom_up_cost, _ = (
        matrix_chain_bottom_up(
            dimensions
        )
    )

    assert memoized_cost == 2000
    assert bottom_up_cost == 2000


def test_too_few_dimensions():
    with pytest.raises(ValueError):
        matrix_chain_memoized(
            [10]
        )

    with pytest.raises(ValueError):
        matrix_chain_bottom_up(
            []
        )


def test_zero_dimension():
    with pytest.raises(ValueError):
        matrix_chain_memoized(
            [10, 0, 20]
        )


def test_negative_dimension():
    with pytest.raises(ValueError):
        matrix_chain_bottom_up(
            [10, -5, 20]
        )