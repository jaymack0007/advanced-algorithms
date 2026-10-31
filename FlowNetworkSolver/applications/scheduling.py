"""Job-to-machine scheduling using maximum flow."""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

from FlowNetworkSolver.core.network import (
    FlowNetwork,
)
from FlowNetworkSolver.core.push_relabel import (
    PushRelabelResult,
    push_relabel,
)


AssignmentEdge = Tuple[str, str]


@dataclass
class SchedulingResult:
    """Store a scheduling/resource-allocation solution."""

    assigned_count: int
    assignments: Dict[str, str]
    unassigned_jobs: List[str]
    feasible: bool
    max_flow_result: PushRelabelResult


def _validate_jobs(
    jobs: Sequence[str],
) -> List[str]:
    """Validate job identifiers."""
    if not isinstance(
        jobs,
        (list, tuple),
    ):
        raise TypeError(
            "jobs must be a list or tuple"
        )

    result = list(
        jobs
    )

    if len(
        result
    ) != len(
        set(
            result
        )
    ):
        raise ValueError(
            "jobs contain duplicate identifiers"
        )

    for job in result:
        if not isinstance(
            job,
            str,
        ):
            raise TypeError(
                "job identifiers must be strings"
            )

    return result


def _validate_machines(
    machine_capacities: Mapping[str, int],
) -> Dict[str, int]:
    """Validate machine capacities."""
    if not isinstance(
        machine_capacities,
        dict,
    ):
        raise TypeError(
            "machine_capacities must be a dictionary"
        )

    result = {}

    for machine, capacity in machine_capacities.items():
        if not isinstance(
            machine,
            str,
        ):
            raise TypeError(
                "machine identifiers must be strings"
            )

        if (
            isinstance(
                capacity,
                bool,
            )
            or not isinstance(
                capacity,
                int,
            )
        ):
            raise TypeError(
                "machine capacities must be integers"
            )

        if capacity < 0:
            raise ValueError(
                "machine capacities must be non-negative"
            )

        result[
            machine
        ] = capacity

    return result


def _validate_eligibility(
    eligible_assignments: Iterable[AssignmentEdge],
    jobs: set[str],
    machines: set[str],
) -> List[AssignmentEdge]:
    """Validate job-to-machine eligibility edges."""
    if not isinstance(
        eligible_assignments,
        (list, tuple),
    ):
        raise TypeError(
            "eligible_assignments must be a list or tuple"
        )

    normalized = []
    seen = set()

    for edge in eligible_assignments:
        if not isinstance(
            edge,
            tuple,
        ):
            raise TypeError(
                "each eligibility edge must be a tuple"
            )

        if len(
            edge
        ) != 2:
            raise ValueError(
                "each eligibility edge must contain a job and machine"
            )

        job, machine = edge

        if job not in jobs:
            raise ValueError(
                f"unknown job: {job}"
            )

        if machine not in machines:
            raise ValueError(
                f"unknown machine: {machine}"
            )

        if edge not in seen:
            seen.add(
                edge
            )

            normalized.append(
                edge
            )

    return normalized


def schedule_jobs(
    jobs: Sequence[str],
    machine_capacities: Mapping[str, int],
    eligible_assignments: Iterable[AssignmentEdge],
) -> SchedulingResult:
    """
    Assign as many jobs as possible to eligible machines.

    Flow model:
        source -> job            capacity 1
        job -> eligible machine  capacity 1
        machine -> sink          machine capacity
    """
    job_list = _validate_jobs(
        jobs
    )

    capacities = _validate_machines(
        machine_capacities
    )

    eligibility = _validate_eligibility(
        eligible_assignments,
        set(
            job_list
        ),
        set(
            capacities
        ),
    )

    source = (
        "__source__",
        "schedule",
    )

    sink = (
        "__sink__",
        "schedule",
    )

    network = FlowNetwork()

    network.add_node(
        source
    )

    network.add_node(
        sink
    )

    job_nodes = {
        job: (
            "job",
            job,
        )
        for job in job_list
    }

    machine_nodes = {
        machine: (
            "machine",
            machine,
        )
        for machine in capacities
    }

    for job in job_list:
        network.add_edge(
            source,
            job_nodes[
                job
            ],
            1,
        )

    for job, machine in eligibility:
        network.add_edge(
            job_nodes[
                job
            ],
            machine_nodes[
                machine
            ],
            1,
        )

    for machine, capacity in capacities.items():
        network.add_edge(
            machine_nodes[
                machine
            ],
            sink,
            capacity,
        )

    result = push_relabel(
        network,
        source,
        sink,
    )

    flow_assignment = (
        result.flow_assignment
    )

    assignments = {}

    for job, machine in eligibility:
        job_node = job_nodes[
            job
        ]

        machine_node = machine_nodes[
            machine
        ]

        if (
            flow_assignment[
                job_node
            ].get(
                machine_node,
                0.0,
            )
            > 0.5
        ):
            assignments[
                job
            ] = machine

    unassigned_jobs = [
        job
        for job in job_list
        if job not in assignments
    ]

    return SchedulingResult(
        assigned_count=len(
            assignments
        ),
        assignments=assignments,
        unassigned_jobs=unassigned_jobs,
        feasible=(
            len(
                assignments
            )
            == len(
                job_list
            )
        ),
        max_flow_result=result,
    )