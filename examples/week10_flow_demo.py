"""Week 10 demonstration of flow-network algorithms and applications."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(
    __file__
).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from FlowNetworkSolver.applications.image_seg import (
    segment_grayscale,
)
from FlowNetworkSolver.applications.matching import (
    maximum_bipartite_matching,
)
from FlowNetworkSolver.applications.scheduling import (
    schedule_jobs,
)
from FlowNetworkSolver.core.edmonds_karp import (
    edmonds_karp,
)
from FlowNetworkSolver.core.min_cost_flow import (
    min_cost_max_flow,
)
from FlowNetworkSolver.core.network import (
    FlowNetwork,
)
from FlowNetworkSolver.core.push_relabel import (
    push_relabel,
)
from FlowNetworkSolver.utils.validators import (
    validate_flow,
)


def build_demo_network():
    """Create a small flow network for solver comparison."""
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        10,
        cost=1,
    )

    network.add_edge(
        "S",
        "B",
        5,
        cost=2,
    )

    network.add_edge(
        "A",
        "B",
        5,
        cost=1,
    )

    network.add_edge(
        "A",
        "T",
        5,
        cost=2,
    )

    network.add_edge(
        "B",
        "T",
        10,
        cost=1,
    )

    return network


def demo_core_algorithms():
    """Demonstrate the three core flow algorithms."""
    print(
        "\n=== Core Flow Algorithms ==="
    )

    network = build_demo_network()

    ek_result = edmonds_karp(
        network,
        "S",
        "T",
    )

    print(
        f"Edmonds-Karp max flow: "
        f"{ek_result.max_flow:g}"
    )

    print(
        f"Edmonds-Karp augmentations: "
        f"{ek_result.iterations}"
    )

    print(
        "Flow valid:",
        validate_flow(
            network,
            "S",
            "T",
        ).valid,
    )

    network = build_demo_network()

    pr_result = push_relabel(
        network,
        "S",
        "T",
    )

    print(
        f"Push-Relabel max flow: "
        f"{pr_result.max_flow:g}"
    )

    print(
        f"Pushes: {pr_result.pushes}"
    )

    print(
        f"Relabels: {pr_result.relabels}"
    )

    print(
        "Flow valid:",
        validate_flow(
            network,
            "S",
            "T",
        ).valid,
    )

    network = build_demo_network()

    mcf_result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    print(
        f"Min-Cost Max-Flow: "
        f"{mcf_result.max_flow:g}"
    )

    print(
        f"Minimum cost: "
        f"{mcf_result.min_cost:g}"
    )

    print(
        "Flow valid:",
        validate_flow(
            network,
            "S",
            "T",
        ).valid,
    )


def demo_matching():
    """Demonstrate bipartite matching."""
    print(
        "\n=== Bipartite Matching ==="
    )

    result = maximum_bipartite_matching(
        [
            "Alice",
            "Bob",
            "Carol",
        ],
        [
            "Task1",
            "Task2",
            "Task3",
        ],
        [
            (
                "Alice",
                "Task1",
            ),
            (
                "Alice",
                "Task2",
            ),
            (
                "Bob",
                "Task2",
            ),
            (
                "Carol",
                "Task3",
            ),
        ],
    )

    print(
        f"Matching size: "
        f"{result.cardinality}"
    )

    for left, right in result.matches:
        print(
            f"{left} -> {right}"
        )


def demo_segmentation():
    """Demonstrate grayscale graph-cut segmentation."""
    print(
        "\n=== Image Segmentation ==="
    )

    image = [
        [
            10,
            20,
            230,
            245,
        ],
        [
            15,
            25,
            220,
            250,
        ],
        [
            5,
            30,
            225,
            240,
        ],
    ]

    result = segment_grayscale(
        image,
        foreground_reference=240,
        background_reference=20,
        smoothness=5,
    )

    print(
        f"Cut value: "
        f"{result.cut_value:g}"
    )

    print(
        "Binary mask:"
    )

    for row in result.mask:
        print(
            " ".join(
                str(
                    value
                )
                for value in row
            )
        )


def demo_scheduling():
    """Demonstrate resource-allocation scheduling."""
    print(
        "\n=== Scheduling ==="
    )

    result = schedule_jobs(
        [
            "Job1",
            "Job2",
            "Job3",
            "Job4",
        ],
        {
            "MachineA": 2,
            "MachineB": 2,
        },
        [
            (
                "Job1",
                "MachineA",
            ),
            (
                "Job2",
                "MachineA",
            ),
            (
                "Job2",
                "MachineB",
            ),
            (
                "Job3",
                "MachineB",
            ),
            (
                "Job4",
                "MachineA",
            ),
            (
                "Job4",
                "MachineB",
            ),
        ],
    )

    print(
        f"Assigned jobs: "
        f"{result.assigned_count}"
    )

    print(
        f"Fully feasible: "
        f"{result.feasible}"
    )

    for job in sorted(
        result.assignments
    ):
        print(
            f"{job} -> "
            f"{result.assignments[job]}"
        )

    if result.unassigned_jobs:
        print(
            "Unassigned jobs:",
            result.unassigned_jobs,
        )


def main():
    """Run all Week 10 demonstrations."""
    print(
        "Week 10 Flow Network Solver Demo"
    )

    demo_core_algorithms()

    demo_matching()

    demo_segmentation()

    demo_scheduling()

    print(
        "\nDemo complete."
    )


if __name__ == "__main__":
    main()