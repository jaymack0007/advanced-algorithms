"""Command-line interface for the Week 10 Flow Network Solver."""

import argparse
import json
from pathlib import Path
from typing import Any, Dict

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
from FlowNetworkSolver.visualization.plot_network import (
    plot_flow_network,
)


def load_json(
    path: str,
) -> Dict[str, Any]:
    """Load a JSON input file."""
    file_path = Path(
        path
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"input file not found: {path}"
        )

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as handle:
        data = json.load(
            handle
        )

    if not isinstance(
        data,
        dict,
    ):
        raise ValueError(
            "input JSON must contain an object"
        )

    return data


def build_network(
    data: Dict[str, Any],
) -> tuple[
    FlowNetwork,
    Any,
    Any,
]:
    """Build a FlowNetwork from JSON data."""
    if "source" not in data:
        raise ValueError(
            "graph input requires 'source'"
        )

    if "sink" not in data:
        raise ValueError(
            "graph input requires 'sink'"
        )

    if "edges" not in data:
        raise ValueError(
            "graph input requires 'edges'"
        )

    edges = data[
        "edges"
    ]

    if not isinstance(
        edges,
        list,
    ):
        raise TypeError(
            "'edges' must be a list"
        )

    network = FlowNetwork()

    source = data[
        "source"
    ]

    sink = data[
        "sink"
    ]

    network.add_node(
        source
    )

    network.add_node(
        sink
    )

    for edge in edges:
        if not isinstance(
            edge,
            dict,
        ):
            raise TypeError(
                "each graph edge must be an object"
            )

        if (
            "source" not in edge
            or "target" not in edge
            or "capacity" not in edge
        ):
            raise ValueError(
                "each edge requires source, target, and capacity"
            )

        network.add_edge(
            edge[
                "source"
            ],
            edge[
                "target"
            ],
            edge[
                "capacity"
            ],
            cost=edge.get(
                "cost",
                0,
            ),
        )

    return (
        network,
        source,
        sink,
    )


def run_edmonds_karp(
    data: Dict[str, Any],
    plot_path: str | None,
) -> None:
    """Run Edmonds-Karp from JSON input."""
    (
        network,
        source,
        sink,
    ) = build_network(
        data
    )

    result = edmonds_karp(
        network,
        source,
        sink,
    )

    print(
        f"Max flow: {result.max_flow:g}"
    )

    print(
        f"Augmentations: {result.iterations}"
    )

    print(
        f"Residual updates: {result.residual_updates}"
    )

    print(
        "Bottlenecks:",
        result.bottlenecks,
    )

    if plot_path:
        plot_flow_network(
            network,
            title="Edmonds-Karp Result",
            output_path=plot_path,
        )

        print(
            f"Plot saved: {plot_path}"
        )


def run_push_relabel(
    data: Dict[str, Any],
    plot_path: str | None,
) -> None:
    """Run Push-Relabel from JSON input."""
    (
        network,
        source,
        sink,
    ) = build_network(
        data
    )

    result = push_relabel(
        network,
        source,
        sink,
    )

    print(
        f"Max flow: {result.max_flow:g}"
    )

    print(
        f"Pushes: {result.pushes}"
    )

    print(
        f"Relabels: {result.relabels}"
    )

    print(
        f"Discharges: {result.discharges}"
    )

    print(
        "Peak active vertices:",
        result.peak_active_vertices,
    )

    if plot_path:
        plot_flow_network(
            network,
            title="Push-Relabel Result",
            output_path=plot_path,
        )

        print(
            f"Plot saved: {plot_path}"
        )


def run_min_cost_flow(
    data: Dict[str, Any],
    plot_path: str | None,
    flow_limit: float | None,
) -> None:
    """Run Min-Cost Max-Flow from JSON input."""
    (
        network,
        source,
        sink,
    ) = build_network(
        data
    )

    result = min_cost_max_flow(
        network,
        source,
        sink,
        flow_limit=flow_limit,
    )

    print(
        f"Max flow: {result.max_flow:g}"
    )

    print(
        f"Minimum cost: {result.min_cost:g}"
    )

    print(
        f"Augmentations: {result.augmentations}"
    )

    print(
        "Path costs:",
        result.path_costs,
    )

    if plot_path:
        plot_flow_network(
            network,
            title="Min-Cost Max-Flow Result",
            output_path=plot_path,
        )

        print(
            f"Plot saved: {plot_path}"
        )


def run_matching(
    data: Dict[str, Any],
) -> None:
    """Run bipartite matching from JSON input."""
    required = {
        "left",
        "right",
        "edges",
    }

    missing = (
        required
        - set(
            data
        )
    )

    if missing:
        raise ValueError(
            f"matching input missing: {sorted(missing)}"
        )

    edges = [
        tuple(
            edge
        )
        for edge in data[
            "edges"
        ]
    ]

    result = maximum_bipartite_matching(
        data[
            "left"
        ],
        data[
            "right"
        ],
        edges,
    )

    print(
        f"Matching size: {result.cardinality}"
    )

    for first, second in result.matches:
        print(
            f"{first} -> {second}"
        )


def run_segmentation(
    data: Dict[str, Any],
) -> None:
    """Run grayscale graph-cut segmentation."""
    if "image" not in data:
        raise ValueError(
            "segmentation input requires 'image'"
        )

    result = segment_grayscale(
        data[
            "image"
        ],
        foreground_reference=data.get(
            "foreground_reference",
            220.0,
        ),
        background_reference=data.get(
            "background_reference",
            30.0,
        ),
        data_weight=data.get(
            "data_weight",
            1.0,
        ),
        smoothness=data.get(
            "smoothness",
            10.0,
        ),
    )

    print(
        f"Cut value: {result.cut_value:g}"
    )

    print(
        "Segmented mask:"
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


def run_scheduling(
    data: Dict[str, Any],
) -> None:
    """Run flow-based scheduling from JSON input."""
    required = {
        "jobs",
        "machine_capacities",
        "eligible_assignments",
    }

    missing = (
        required
        - set(
            data
        )
    )

    if missing:
        raise ValueError(
            f"schedule input missing: {sorted(missing)}"
        )

    eligibility = [
        tuple(
            edge
        )
        for edge in data[
            "eligible_assignments"
        ]
    ]

    result = schedule_jobs(
        data[
            "jobs"
        ],
        data[
            "machine_capacities"
        ],
        eligibility,
    )

    print(
        f"Assigned jobs: {result.assigned_count}"
    )

    print(
        f"Fully feasible: {result.feasible}"
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
            "Unassigned:",
            ", ".join(
                result.unassigned_jobs
            ),
        )


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Week 10 modular flow-network solver"
        )
    )

    mode = parser.add_mutually_exclusive_group(
        required=True
    )

    mode.add_argument(
        "--ek",
        action="store_true",
        help="Run Edmonds-Karp max flow",
    )

    mode.add_argument(
        "--pr",
        action="store_true",
        help="Run Push-Relabel max flow",
    )

    mode.add_argument(
        "--mcf",
        action="store_true",
        help="Run Min-Cost Max-Flow",
    )

    mode.add_argument(
        "--match",
        action="store_true",
        help="Run bipartite matching",
    )

    mode.add_argument(
        "--segment",
        action="store_true",
        help="Run grayscale image segmentation",
    )

    mode.add_argument(
        "--schedule",
        action="store_true",
        help="Run scheduling/resource allocation",
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to JSON input file",
    )

    parser.add_argument(
        "--plot",
        help="Optional PNG output for flow solver visualization",
    )

    parser.add_argument(
        "--flow-limit",
        type=float,
        help="Optional Min-Cost Flow limit",
    )

    return parser


def main() -> None:
    """Run the selected solver or application."""
    parser = build_parser()

    arguments = parser.parse_args()

    data = load_json(
        arguments.input
    )

    if arguments.ek:
        run_edmonds_karp(
            data,
            arguments.plot,
        )

    elif arguments.pr:
        run_push_relabel(
            data,
            arguments.plot,
        )

    elif arguments.mcf:
        run_min_cost_flow(
            data,
            arguments.plot,
            arguments.flow_limit,
        )

    elif arguments.match:
        run_matching(
            data
        )

    elif arguments.segment:
        run_segmentation(
            data
        )

    elif arguments.schedule:
        run_scheduling(
            data
        )


if __name__ == "__main__":
    main()