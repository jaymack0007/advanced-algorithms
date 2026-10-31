"""Tests for bipartite matching via max flow."""

import pytest

from FlowNetworkSolver.applications.matching import (
    MatchingResult,
    maximum_bipartite_matching,
)


def test_returns_result_object():
    result = maximum_bipartite_matching(
        [
            "A"
        ],
        [
            "X"
        ],
        [
            (
                "A",
                "X",
            )
        ],
    )

    assert isinstance(
        result,
        MatchingResult,
    )


def test_single_match():
    result = maximum_bipartite_matching(
        [
            "A"
        ],
        [
            "X"
        ],
        [
            (
                "A",
                "X",
            )
        ],
    )

    assert result.cardinality == 1
    assert result.matches == [
        (
            "A",
            "X",
        )
    ]


def test_perfect_matching():
    result = maximum_bipartite_matching(
        [
            "A",
            "B",
            "C",
        ],
        [
            "X",
            "Y",
            "Z",
        ],
        [
            (
                "A",
                "X",
            ),
            (
                "A",
                "Y",
            ),
            (
                "B",
                "Y",
            ),
            (
                "C",
                "Z",
            ),
        ],
    )

    assert result.cardinality == 3


def test_matching_has_unique_left_vertices():
    result = maximum_bipartite_matching(
        [
            "A",
            "B",
        ],
        [
            "X",
            "Y",
        ],
        [
            (
                "A",
                "X",
            ),
            (
                "A",
                "Y",
            ),
            (
                "B",
                "X",
            ),
        ],
    )

    left_vertices = [
        first
        for first, _ in result.matches
    ]

    assert len(
        left_vertices
    ) == len(
        set(
            left_vertices
        )
    )


def test_matching_has_unique_right_vertices():
    result = maximum_bipartite_matching(
        [
            "A",
            "B",
        ],
        [
            "X",
            "Y",
        ],
        [
            (
                "A",
                "X",
            ),
            (
                "A",
                "Y",
            ),
            (
                "B",
                "X",
            ),
        ],
    )

    right_vertices = [
        second
        for _, second in result.matches
    ]

    assert len(
        right_vertices
    ) == len(
        set(
            right_vertices
        )
    )


def test_incomplete_matching():
    result = maximum_bipartite_matching(
        [
            "A",
            "B",
            "C",
        ],
        [
            "X",
            "Y",
        ],
        [
            (
                "A",
                "X",
            ),
            (
                "B",
                "X",
            ),
            (
                "C",
                "Y",
            ),
        ],
    )

    assert result.cardinality == 2


def test_empty_partitions():
    result = maximum_bipartite_matching(
        [],
        [],
        [],
    )

    assert result.cardinality == 0
    assert result.matches == []


def test_no_candidate_edges():
    result = maximum_bipartite_matching(
        [
            "A",
            "B",
        ],
        [
            "X",
            "Y",
        ],
        [],
    )

    assert result.cardinality == 0


def test_duplicate_candidate_edges_ignored():
    result = maximum_bipartite_matching(
        [
            "A"
        ],
        [
            "X"
        ],
        [
            (
                "A",
                "X",
            ),
            (
                "A",
                "X",
            ),
        ],
    )

    assert result.cardinality == 1


def test_flow_value_equals_cardinality():
    result = maximum_bipartite_matching(
        [
            "A",
            "B",
        ],
        [
            "X",
            "Y",
        ],
        [
            (
                "A",
                "X",
            ),
            (
                "B",
                "Y",
            ),
        ],
    )

    assert (
        result.max_flow_result.max_flow
        == result.cardinality
    )


def test_duplicate_left_vertex_rejected():
    with pytest.raises(ValueError):
        maximum_bipartite_matching(
            [
                "A",
                "A",
            ],
            [
                "X"
            ],
            [
                (
                    "A",
                    "X",
                )
            ],
        )


def test_duplicate_right_vertex_rejected():
    with pytest.raises(ValueError):
        maximum_bipartite_matching(
            [
                "A"
            ],
            [
                "X",
                "X",
            ],
            [
                (
                    "A",
                    "X",
                )
            ],
        )


def test_overlapping_partitions_rejected():
    with pytest.raises(ValueError):
        maximum_bipartite_matching(
            [
                "A"
            ],
            [
                "A"
            ],
            [],
        )


def test_unknown_left_vertex_rejected():
    with pytest.raises(ValueError):
        maximum_bipartite_matching(
            [
                "A"
            ],
            [
                "X"
            ],
            [
                (
                    "B",
                    "X",
                )
            ],
        )


def test_unknown_right_vertex_rejected():
    with pytest.raises(ValueError):
        maximum_bipartite_matching(
            [
                "A"
            ],
            [
                "X"
            ],
            [
                (
                    "A",
                    "Y",
                )
            ],
        )


def test_invalid_partition_type():
    with pytest.raises(TypeError):
        maximum_bipartite_matching(
            {
                "A"
            },
            [
                "X"
            ],
            [],
        )


def test_invalid_edge_type():
    with pytest.raises(TypeError):
        maximum_bipartite_matching(
            [
                "A"
            ],
            [
                "X"
            ],
            [
                [
                    "A",
                    "X",
                ]
            ],
        )


def test_reserved_names_rejected():
    with pytest.raises(ValueError):
        maximum_bipartite_matching(
            [
                "__source__"
            ],
            [
                "X"
            ],
            [],
        )