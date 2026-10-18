"""Tests for the small CNF SAT solvers."""

import pytest

from src.complexity.satisfiability_solver import (
    evaluate_formula,
    evaluate_literal,
    random_sat_heuristic,
    sat_backtracking,
)


SAT_FORMULA = [
    (
        "x1",
        "x2",
    ),
    (
        "~x1",
        "x3",
    ),
    (
        "~x2",
        "x3",
    ),
]


UNSAT_FORMULA = [
    (
        "x1",
    ),
    (
        "~x1",
    ),
]


def test_positive_literal():
    assignment = {
        "x1": True,
    }

    assert evaluate_literal(
        "x1",
        assignment,
    )


def test_negative_literal():
    assignment = {
        "x1": False,
    }

    assert evaluate_literal(
        "~x1",
        assignment,
    )


def test_formula_evaluation_true():
    assignment = {
        "x1": True,
        "x2": False,
        "x3": True,
    }

    assert evaluate_formula(
        SAT_FORMULA,
        assignment,
    )


def test_formula_evaluation_false():
    assignment = {
        "x1": False,
        "x2": False,
        "x3": False,
    }

    assert not evaluate_formula(
        SAT_FORMULA,
        assignment,
    )


def test_backtracking_finds_solution():
    result = sat_backtracking(
        SAT_FORMULA
    )

    assert result is not None
    assert evaluate_formula(
        SAT_FORMULA,
        result,
    )


def test_backtracking_detects_unsat():
    result = sat_backtracking(
        UNSAT_FORMULA
    )

    assert result is None


def test_single_literal_formula():
    formula = [
        (
            "x1",
        ),
    ]

    result = sat_backtracking(
        formula
    )

    assert result is not None
    assert result["x1"] is True


def test_stats_recorded():
    stats = {}

    result = sat_backtracking(
        SAT_FORMULA,
        stats=stats,
    )

    assert result is not None
    assert stats["nodes_visited"] > 0
    assert stats["max_depth"] > 0


def test_random_heuristic_can_find_solution():
    result = random_sat_heuristic(
        SAT_FORMULA,
        trials=100,
        seed=42,
    )

    assert result is not None
    assert evaluate_formula(
        SAT_FORMULA,
        result,
    )


def test_random_heuristic_reproducible():
    first = random_sat_heuristic(
        SAT_FORMULA,
        trials=100,
        seed=42,
    )

    second = random_sat_heuristic(
        SAT_FORMULA,
        trials=100,
        seed=42,
    )

    assert first == second


def test_missing_assignment_rejected():
    with pytest.raises(KeyError):
        evaluate_literal(
            "x1",
            {},
        )


def test_invalid_formula_type():
    with pytest.raises(TypeError):
        sat_backtracking(
            "not a list"
        )


def test_invalid_clause_type():
    with pytest.raises(TypeError):
        sat_backtracking(
            [
                [
                    "x1",
                    "x2",
                ]
            ]
        )


def test_empty_clause_rejected():
    with pytest.raises(ValueError):
        sat_backtracking(
            [
                ()
            ]
        )


def test_invalid_trial_count():
    with pytest.raises(ValueError):
        random_sat_heuristic(
            SAT_FORMULA,
            trials=0,
        )