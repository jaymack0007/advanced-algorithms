"""Tests for flow-based job scheduling."""

import pytest

from FlowNetworkSolver.applications.scheduling import (
    SchedulingResult,
    schedule_jobs,
)


def test_returns_result_object():
    result = schedule_jobs(
        [
            "J1"
        ],
        {
            "M1": 1
        },
        [
            (
                "J1",
                "M1",
            )
        ],
    )

    assert isinstance(
        result,
        SchedulingResult,
    )


def test_single_job_assignment():
    result = schedule_jobs(
        [
            "J1"
        ],
        {
            "M1": 1
        },
        [
            (
                "J1",
                "M1",
            )
        ],
    )

    assert result.assigned_count == 1
    assert result.assignments == {
        "J1": "M1"
    }
    assert result.feasible is True


def test_multiple_jobs_single_machine_capacity():
    result = schedule_jobs(
        [
            "J1",
            "J2",
        ],
        {
            "M1": 2
        },
        [
            (
                "J1",
                "M1",
            ),
            (
                "J2",
                "M1",
            ),
        ],
    )

    assert result.assigned_count == 2
    assert result.feasible is True


def test_machine_capacity_is_respected():
    result = schedule_jobs(
        [
            "J1",
            "J2",
            "J3",
        ],
        {
            "M1": 2
        },
        [
            (
                "J1",
                "M1",
            ),
            (
                "J2",
                "M1",
            ),
            (
                "J3",
                "M1",
            ),
        ],
    )

    assigned_to_m1 = sum(
        1
        for machine in result.assignments.values()
        if machine == "M1"
    )

    assert assigned_to_m1 == 2
    assert result.assigned_count == 2


def test_job_assigned_at_most_once():
    result = schedule_jobs(
        [
            "J1"
        ],
        {
            "M1": 1,
            "M2": 1,
        },
        [
            (
                "J1",
                "M1",
            ),
            (
                "J1",
                "M2",
            ),
        ],
    )

    assert result.assigned_count == 1

    assert result.assignments[
        "J1"
    ] in {
        "M1",
        "M2",
    }


def test_only_eligible_assignments_used():
    eligibility = [
        (
            "J1",
            "M1",
        ),
        (
            "J2",
            "M2",
        ),
    ]

    result = schedule_jobs(
        [
            "J1",
            "J2",
        ],
        {
            "M1": 1,
            "M2": 1,
        },
        eligibility,
    )

    assert (
        "J1",
        result.assignments[
            "J1"
        ],
    ) in eligibility

    assert (
        "J2",
        result.assignments[
            "J2"
        ],
    ) in eligibility


def test_unassigned_jobs_reported():
    result = schedule_jobs(
        [
            "J1",
            "J2",
        ],
        {
            "M1": 1
        },
        [
            (
                "J1",
                "M1",
            )
        ],
    )

    assert result.unassigned_jobs == [
        "J2"
    ]

    assert result.feasible is False


def test_zero_capacity_machine():
    result = schedule_jobs(
        [
            "J1"
        ],
        {
            "M1": 0
        },
        [
            (
                "J1",
                "M1",
            )
        ],
    )

    assert result.assigned_count == 0
    assert result.unassigned_jobs == [
        "J1"
    ]


def test_empty_jobs():
    result = schedule_jobs(
        [],
        {
            "M1": 2
        },
        [],
    )

    assert result.assigned_count == 0
    assert result.assignments == {}
    assert result.unassigned_jobs == []
    assert result.feasible is True


def test_duplicate_eligibility_ignored():
    result = schedule_jobs(
        [
            "J1"
        ],
        {
            "M1": 1
        },
        [
            (
                "J1",
                "M1",
            ),
            (
                "J1",
                "M1",
            ),
        ],
    )

    assert result.assigned_count == 1


def test_flow_value_equals_assignment_count():
    result = schedule_jobs(
        [
            "J1",
            "J2",
        ],
        {
            "M1": 1,
            "M2": 1,
        },
        [
            (
                "J1",
                "M1",
            ),
            (
                "J2",
                "M2",
            ),
        ],
    )

    assert (
        result.max_flow_result.max_flow
        == result.assigned_count
    )


def test_duplicate_jobs_rejected():
    with pytest.raises(ValueError):
        schedule_jobs(
            [
                "J1",
                "J1",
            ],
            {
                "M1": 1
            },
            [],
        )


def test_negative_machine_capacity_rejected():
    with pytest.raises(ValueError):
        schedule_jobs(
            [
                "J1"
            ],
            {
                "M1": -1
            },
            [],
        )


def test_noninteger_machine_capacity_rejected():
    with pytest.raises(TypeError):
        schedule_jobs(
            [
                "J1"
            ],
            {
                "M1": 1.5
            },
            [],
        )


def test_unknown_job_in_eligibility_rejected():
    with pytest.raises(ValueError):
        schedule_jobs(
            [
                "J1"
            ],
            {
                "M1": 1
            },
            [
                (
                    "J2",
                    "M1",
                )
            ],
        )


def test_unknown_machine_in_eligibility_rejected():
    with pytest.raises(ValueError):
        schedule_jobs(
            [
                "J1"
            ],
            {
                "M1": 1
            },
            [
                (
                    "J1",
                    "M2",
                )
            ],
        )


def test_invalid_jobs_type_rejected():
    with pytest.raises(TypeError):
        schedule_jobs(
            {
                "J1"
            },
            {
                "M1": 1
            },
            [],
        )


def test_invalid_eligibility_edge_rejected():
    with pytest.raises(TypeError):
        schedule_jobs(
            [
                "J1"
            ],
            {
                "M1": 1
            },
            [
                [
                    "J1",
                    "M1",
                ]
            ],
        )