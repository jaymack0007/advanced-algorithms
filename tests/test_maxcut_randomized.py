"""Tests for randomized and local-search Max-Cut."""

import statistics

import pytest

from src.approximation.maxcut_randomized import (
    approximation_ratio,
    cut_value,
    exact_maxcut,
    graph_vertices,
    local_search_maxcut,
    randomized_maxcut,
)


TRIANGLE = [
    (
        "A",
        "B",
    ),
    (
        "B",
        "C",
    ),
    (
        "A",
        "C",
    ),
]


SQUARE = [
    (
        "A",
        "B",
    ),
    (
        "B",
        "C",
    ),
    (
        "C",
        "D",
    ),
    (
        "D",
        "A",
    ),
]


def test_graph_vertices():
    assert graph_vertices(
        TRIANGLE
    ) == [
        "A",
        "B",
        "C",
    ]


def test_triangle_exact_value():
    result = exact_maxcut(
        TRIANGLE
    )

    assert result.cut_value == 2


def test_square_exact_value():
    result = exact_maxcut(
        SQUARE
    )

    assert result.cut_value == 4


def test_cut_value():
    value = cut_value(
        SQUARE,
        {
            "A",
            "C",
        },
    )

    assert value == 4


def test_randomized_partition_contains_all_vertices():
    result = randomized_maxcut(
        TRIANGLE,
        seed=42,
    )

    assert (
        result.left
        | result.right
    ) == {
        "A",
        "B",
        "C",
    }


def test_randomized_partitions_are_disjoint():
    result = randomized_maxcut(
        TRIANGLE,
        seed=42,
    )

    assert (
        result.left
        & result.right
    ) == set()


def test_randomized_is_reproducible():
    first = randomized_maxcut(
        SQUARE,
        seed=42,
    )

    second = randomized_maxcut(
        SQUARE,
        seed=42,
    )

    assert first.left == second.left
    assert first.cut_value == second.cut_value


def test_local_search_never_worse_than_initial():
    random_result = randomized_maxcut(
        TRIANGLE,
        seed=10,
    )

    improved = local_search_maxcut(
        TRIANGLE,
        seed=10,
    )

    assert (
        improved.cut_value
        >= random_result.cut_value
    )


def test_local_search_triangle_reaches_optimum():
    result = local_search_maxcut(
        TRIANGLE,
        seed=7,
    )

    assert result.cut_value == 2


def test_local_search_square_reaches_optimum():
    result = local_search_maxcut(
        SQUARE,
        seed=7,
    )

    assert result.cut_value == 4


def test_randomized_expected_value_experiment():
    values = [
        randomized_maxcut(
            TRIANGLE,
            seed=seed,
        ).cut_value
        for seed in range(
            500
        )
    ]

    average = statistics.mean(
        values
    )

    assert average >= 1.4


def test_randomized_average_at_least_half_optimum():
    optimal = exact_maxcut(
        TRIANGLE
    )

    values = [
        randomized_maxcut(
            TRIANGLE,
            seed=seed,
        ).cut_value
        for seed in range(
            500
        )
    ]

    average = statistics.mean(
        values
    )

    assert (
        average
        >= 0.5
        * optimal.cut_value
    )


def test_approximation_ratio():
    assert approximation_ratio(
        2,
        4,
    ) == 0.5


def test_empty_graph():
    result = exact_maxcut(
        []
    )

    assert result.cut_value == 0
    assert result.left == set()
    assert result.right == set()


def test_duplicate_edges_are_not_double_counted():
    edges = [
        (
            "A",
            "B",
        ),
        (
            "B",
            "A",
        ),
    ]

    assert cut_value(
        edges,
        {
            "A"
        },
    ) == 1


def test_self_loop_rejected():
    with pytest.raises(ValueError):
        randomized_maxcut(
            [
                (
                    "A",
                    "A",
                )
            ]
        )


def test_invalid_edge_type():
    with pytest.raises(TypeError):
        randomized_maxcut(
            [
                [
                    "A",
                    "B",
                ]
            ]
        )


def test_invalid_ratio():
    with pytest.raises(ValueError):
        approximation_ratio(
            1,
            0,
        )