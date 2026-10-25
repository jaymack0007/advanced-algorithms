"""Tests for Set Cover LP relaxation and rounding."""

import pytest

from src.approximation.set_cover_lpround import (
    approximation_ratio,
    deterministic_lp_rounding,
    exact_set_cover,
    is_set_cover,
    randomized_lp_rounding,
)
from src.utils.lp_solver import solve_set_cover_lp


UNIVERSE = {
    "A",
    "B",
    "C",
}


SUBSETS = {
    "S1": {
        "A",
        "B",
    },
    "S2": {
        "B",
        "C",
    },
    "S3": {
        "A",
        "C",
    },
}


COSTS = {
    "S1": 1.0,
    "S2": 1.0,
    "S3": 1.0,
}


def test_lp_solution_is_feasible():
    result = solve_set_cover_lp(
        sorted(
            UNIVERSE
        ),
        SUBSETS,
        COSTS,
    )

    for element in UNIVERSE:
        coverage = sum(
            result.values[name]
            for name in SUBSETS
            if element in SUBSETS[name]
        )

        assert coverage >= (
            1.0 - 1e-8
        )


def test_lp_relaxation_cost():
    result = solve_set_cover_lp(
        sorted(
            UNIVERSE
        ),
        SUBSETS,
        COSTS,
    )

    assert result.objective == pytest.approx(
        1.5
    )


def test_exact_set_cover_cost():
    result = exact_set_cover(
        UNIVERSE,
        SUBSETS,
        COSTS,
    )

    assert result.total_cost == 2.0

    assert len(
        result.selected_sets
    ) == 2


def test_lp_is_lower_bound_on_optimum():
    lp = solve_set_cover_lp(
        sorted(
            UNIVERSE
        ),
        SUBSETS,
        COSTS,
    )

    exact = exact_set_cover(
        UNIVERSE,
        SUBSETS,
        COSTS,
    )

    assert lp.objective <= exact.total_cost


def test_deterministic_rounding_is_cover():
    result = deterministic_lp_rounding(
        UNIVERSE,
        SUBSETS,
        COSTS,
    )

    assert is_set_cover(
        UNIVERSE,
        SUBSETS,
        result.selected_sets,
    )


def test_deterministic_rounding_records_lp_cost():
    result = deterministic_lp_rounding(
        UNIVERSE,
        SUBSETS,
        COSTS,
    )

    assert result.lp_cost == pytest.approx(
        1.5
    )


def test_randomized_rounding_is_cover():
    result = randomized_lp_rounding(
        UNIVERSE,
        SUBSETS,
        COSTS,
        seed=42,
    )

    assert is_set_cover(
        UNIVERSE,
        SUBSETS,
        result.selected_sets,
    )


def test_randomized_rounding_is_reproducible():
    first = randomized_lp_rounding(
        UNIVERSE,
        SUBSETS,
        COSTS,
        seed=42,
    )

    second = randomized_lp_rounding(
        UNIVERSE,
        SUBSETS,
        COSTS,
        seed=42,
    )

    assert (
        first.selected_sets
        == second.selected_sets
    )

    assert (
        first.total_cost
        == second.total_cost
    )


def test_approximation_ratio():
    exact = exact_set_cover(
        UNIVERSE,
        SUBSETS,
        COSTS,
    )

    rounded = deterministic_lp_rounding(
        UNIVERSE,
        SUBSETS,
        COSTS,
    )

    ratio = approximation_ratio(
        rounded.total_cost,
        exact.total_cost,
    )

    assert ratio >= 1.0


def test_empty_universe():
    result = deterministic_lp_rounding(
        set(),
        {},
        {},
    )

    assert result.selected_sets == set()
    assert result.total_cost == 0.0


def test_randomized_empty_universe():
    result = randomized_lp_rounding(
        set(),
        {},
        {},
        seed=1,
    )

    assert result.total_cost == 0.0


def test_incomplete_cover_rejected():
    with pytest.raises(ValueError):
        deterministic_lp_rounding(
            {
                "A",
                "B",
            },
            {
                "S1": {
                    "A"
                }
            },
            {
                "S1": 1.0
            },
        )


def test_missing_cost_rejected():
    with pytest.raises(ValueError):
        deterministic_lp_rounding(
            {
                "A"
            },
            {
                "S1": {
                    "A"
                }
            },
            {},
        )


def test_negative_cost_rejected():
    with pytest.raises(ValueError):
        deterministic_lp_rounding(
            {
                "A"
            },
            {
                "S1": {
                    "A"
                }
            },
            {
                "S1": -1.0
            },
        )


def test_invalid_ratio():
    with pytest.raises(ValueError):
        approximation_ratio(
            2.0,
            0.0,
        )