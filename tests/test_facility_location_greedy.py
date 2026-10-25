"""Tests for the greedy Facility Location heuristic."""

import pytest

from src.approximation.facility_location_greedy import (
    approximation_ratio,
    evaluate_solution,
    exact_facility_location,
    greedy_facility_location,
)


OPENING_COSTS = {
    "F1": 4.0,
    "F2": 4.0,
    "F3": 7.0,
}


CLIENTS = [
    "C1",
    "C2",
    "C3",
    "C4",
]


SERVICE_COSTS = {
    ("F1", "C1"): 1.0,
    ("F1", "C2"): 1.0,
    ("F1", "C3"): 8.0,
    ("F1", "C4"): 8.0,
    ("F2", "C1"): 8.0,
    ("F2", "C2"): 8.0,
    ("F2", "C3"): 1.0,
    ("F2", "C4"): 1.0,
    ("F3", "C1"): 3.0,
    ("F3", "C2"): 3.0,
    ("F3", "C3"): 3.0,
    ("F3", "C4"): 3.0,
}


def test_evaluate_single_facility():
    result = evaluate_solution(
        OPENING_COSTS,
        CLIENTS,
        SERVICE_COSTS,
        {
            "F1"
        },
    )

    assert result.opening_cost == 4.0
    assert result.service_cost == 18.0
    assert result.total_cost == 22.0


def test_evaluate_two_facilities():
    result = evaluate_solution(
        OPENING_COSTS,
        CLIENTS,
        SERVICE_COSTS,
        {
            "F1",
            "F2",
        },
    )

    assert result.opening_cost == 8.0
    assert result.service_cost == 4.0
    assert result.total_cost == 12.0


def test_assignments_use_cheapest_open_facility():
    result = evaluate_solution(
        OPENING_COSTS,
        CLIENTS,
        SERVICE_COSTS,
        {
            "F1",
            "F2",
        },
    )

    assert result.assignments[
        "C1"
    ] == "F1"

    assert result.assignments[
        "C4"
    ] == "F2"


def test_greedy_returns_valid_solution():
    result = greedy_facility_location(
        OPENING_COSTS,
        CLIENTS,
        SERVICE_COSTS,
    )

    assert result.open_facilities
    assert set(
        result.assignments
    ) == set(
        CLIENTS
    )


def test_greedy_can_stop_at_local_solution():
    result = greedy_facility_location(
        OPENING_COSTS,
        CLIENTS,
        SERVICE_COSTS,
    )

    assert result.open_facilities == {
        "F3"
    }

    assert result.total_cost == 19.0


def test_exact_solution():
    result = exact_facility_location(
        OPENING_COSTS,
        CLIENTS,
        SERVICE_COSTS,
    )

    assert result.open_facilities == {
        "F1",
        "F2",
    }

    assert result.total_cost == 12.0


def test_greedy_ratio_against_optimal():
    greedy = greedy_facility_location(
        OPENING_COSTS,
        CLIENTS,
        SERVICE_COSTS,
    )

    optimal = exact_facility_location(
        OPENING_COSTS,
        CLIENTS,
        SERVICE_COSTS,
    )

    ratio = approximation_ratio(
        greedy.total_cost,
        optimal.total_cost,
    )

    assert ratio == pytest.approx(
        19.0 / 12.0
    )

    assert ratio > 1.0


def test_empty_clients():
    result = greedy_facility_location(
        {
            "F1": 4.0
        },
        [],
        {},
    )

    assert result.open_facilities == set()
    assert result.assignments == {}
    assert result.total_cost == 0.0


def test_exact_empty_clients():
    result = exact_facility_location(
        {
            "F1": 4.0
        },
        [],
        {},
    )

    assert result.total_cost == 0.0


def test_missing_service_cost_rejected():
    with pytest.raises(ValueError):
        greedy_facility_location(
            {
                "F1": 5.0
            },
            [
                "C1"
            ],
            {},
        )


def test_negative_opening_cost_rejected():
    with pytest.raises(ValueError):
        greedy_facility_location(
            {
                "F1": -1.0
            },
            [],
            {},
        )


def test_negative_service_cost_rejected():
    with pytest.raises(ValueError):
        greedy_facility_location(
            {
                "F1": 1.0
            },
            [
                "C1"
            ],
            {
                (
                    "F1",
                    "C1",
                ): -2.0
            },
        )


def test_duplicate_clients_rejected():
    with pytest.raises(ValueError):
        greedy_facility_location(
            {
                "F1": 1.0
            },
            [
                "C1",
                "C1",
            ],
            {
                (
                    "F1",
                    "C1",
                ): 1.0
            },
        )


def test_unknown_open_facility_rejected():
    with pytest.raises(ValueError):
        evaluate_solution(
            OPENING_COSTS,
            CLIENTS,
            SERVICE_COSTS,
            {
                "UNKNOWN"
            },
        )


def test_invalid_ratio():
    with pytest.raises(ValueError):
        approximation_ratio(
            5.0,
            0.0,
        )