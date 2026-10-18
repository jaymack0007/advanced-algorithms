"""Tests for the 3-SAT to Vertex Cover reduction."""

import pytest

from src.complexity.reduction_demo import (
    assignment_to_vertex_cover,
    evaluate_formula,
    explain_reduction,
    is_vertex_cover,
    reduce_3sat_to_vertex_cover,
)


CLAUSES = [
    (
        "x1",
        "~x2",
        "x3",
    ),
    (
        "~x1",
        "x2",
        "x3",
    ),
]


ASSIGNMENT = {
    "x1": True,
    "x2": True,
    "x3": True,
}


def test_formula_is_satisfied():
    assert evaluate_formula(
        CLAUSES,
        ASSIGNMENT,
    )


def test_reduction_target_size():
    reduction = (
        reduce_3sat_to_vertex_cover(
            CLAUSES
        )
    )

    assert reduction.target_size == 7


def test_variable_vertices_created():
    reduction = (
        reduce_3sat_to_vertex_cover(
            CLAUSES
        )
    )

    assert "x1" in reduction.vertices
    assert "~x1" in reduction.vertices
    assert "x2" in reduction.vertices
    assert "~x2" in reduction.vertices
    assert "x3" in reduction.vertices
    assert "~x3" in reduction.vertices


def test_variable_edges_created():
    reduction = (
        reduce_3sat_to_vertex_cover(
            CLAUSES
        )
    )

    assert (
        "x1",
        "~x1",
    ) in reduction.edges

    assert (
        "x2",
        "~x2",
    ) in reduction.edges


def test_clause_triangles_created():
    reduction = (
        reduce_3sat_to_vertex_cover(
            CLAUSES
        )
    )

    assert len(
        reduction.clause_vertices
    ) == 2

    assert len(
        reduction.clause_vertices[0]
    ) == 3

    assert len(
        reduction.clause_vertices[1]
    ) == 3


def test_satisfying_assignment_creates_cover():
    reduction = (
        reduce_3sat_to_vertex_cover(
            CLAUSES
        )
    )

    cover = assignment_to_vertex_cover(
        reduction,
        ASSIGNMENT,
    )

    assert len(
        cover
    ) == reduction.target_size

    assert is_vertex_cover(
        reduction.edges,
        cover,
    )


def test_unsatisfying_assignment_rejected():
    clauses = [
        (
            "x1",
            "x1",
            "x1",
        ),
    ]

    reduction = (
        reduce_3sat_to_vertex_cover(
            clauses
        )
    )

    assignment = {
        "x1": False,
    }

    with pytest.raises(ValueError):
        assignment_to_vertex_cover(
            reduction,
            assignment,
        )


def test_explanation_contains_steps():
    reduction = (
        reduce_3sat_to_vertex_cover(
            CLAUSES
        )
    )

    explanation = explain_reduction(
        reduction
    )

    assert "Step 1" in explanation
    assert "Step 2" in explanation
    assert "Step 3" in explanation
    assert "Step 4" in explanation


def test_empty_formula_rejected():
    with pytest.raises(ValueError):
        reduce_3sat_to_vertex_cover(
            []
        )


def test_non_three_literal_clause_rejected():
    with pytest.raises(ValueError):
        reduce_3sat_to_vertex_cover(
            [
                (
                    "x1",
                    "x2",
                )
            ]
        )