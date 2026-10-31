"""Week 10 performance benchmarks for flow-network algorithms."""

import argparse
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Callable, Dict, List, Tuple


PROJECT_ROOT = Path(
    __file__
).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


import matplotlib.pyplot as plt
import pandas as pd

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
from FlowNetworkSolver.utils.generators import (
    generate_dense_network,
)
from FlowNetworkSolver.utils.validators import (
    validate_flow,
)


RESULTS_DIR = (
    PROJECT_ROOT
    / "FlowNetworkSolver"
    / "results"
)


NetworkBuilder = Callable[
    [],
    Tuple[
        FlowNetwork,
        int,
        int,
    ],
]


def build_chain_network(
    vertex_count: int,
    with_costs: bool = True,
) -> Tuple[
    FlowNetwork,
    int,
    int,
]:
    """
    Build a large sparse chain network.

    The chain provides a controlled scalability experiment
    using O(V) original edges and a guaranteed source-to-sink
    path.
    """
    if vertex_count < 2:
        raise ValueError(
            "vertex_count must be at least 2"
        )

    network = FlowNetwork()

    source = 0
    sink = vertex_count - 1

    for vertex in range(
        vertex_count - 1
    ):
        cost = (
            1
            if with_costs
            else 0
        )

        network.add_edge(
            vertex,
            vertex + 1,
            10,
            cost=cost,
        )

    return (
        network,
        source,
        sink,
    )


def count_original_edges(
    network: FlowNetwork,
) -> int:
    """Count non-residual edges."""
    return sum(
        1
        for _ in network.original_edges()
    )


def measure_solver(
    solver_name: str,
    builder: NetworkBuilder,
    family: str,
    graph_type: str,
    vertex_count: int,
) -> Dict[str, object]:
    """
    Measure runtime, memory, max flow, and convergence activity.

    Memory measurement includes construction of the graph and
    the algorithm execution, but not post-run validation.
    """
    tracemalloc.start()

    (
        network,
        source,
        sink,
    ) = builder()

    edge_count = count_original_edges(
        network
    )

    start = time.perf_counter()

    if solver_name == "Edmonds-Karp":
        result = edmonds_karp(
            network,
            source,
            sink,
        )

        operations = (
            result.iterations
        )

        detail = (
            f"{result.iterations} augmentations"
        )

        min_cost = None

    elif solver_name == "Push-Relabel":
        result = push_relabel(
            network,
            source,
            sink,
        )

        operations = (
            result.pushes
            + result.relabels
        )

        detail = (
            f"{result.pushes} pushes, "
            f"{result.relabels} relabels"
        )

        min_cost = None

    elif solver_name == "Min-Cost Max-Flow":
        result = min_cost_max_flow(
            network,
            source,
            sink,
        )

        operations = (
            result.augmentations
        )

        detail = (
            f"{result.augmentations} augmentations"
        )

        min_cost = (
            result.min_cost
        )

    else:
        tracemalloc.stop()

        raise ValueError(
            f"unknown solver: {solver_name}"
        )

    runtime = (
        time.perf_counter()
        - start
    )

    _current_memory, peak_memory = (
        tracemalloc.get_traced_memory()
    )

    tracemalloc.stop()

    validation = validate_flow(
        network,
        source,
        sink,
    )

    if not validation.valid:
        raise RuntimeError(
            f"{solver_name} produced an invalid flow"
        )

    return {
        "family": family,
        "graph_type": graph_type,
        "vertices": vertex_count,
        "edges": edge_count,
        "solver": solver_name,
        "runtime_seconds": runtime,
        "peak_memory_mb": (
            peak_memory
            / (
                1024
                * 1024
            )
        ),
        "max_flow": result.max_flow,
        "min_cost": min_cost,
        "operations": operations,
        "operation_detail": detail,
    }


def validate_group_consistency(
    rows: List[
        Dict[str, object]
    ],
) -> None:
    """
    Confirm that all solvers ran equivalent max-flow problems.

    Edmonds-Karp, Push-Relabel, and Min-Cost Max-Flow should
    return the same maximum-flow value when given the same
    network.
    """
    if not rows:
        raise ValueError(
            "benchmark group contains no results"
        )

    vertex_counts = {
        int(
            row[
                "vertices"
            ]
        )
        for row in rows
    }

    edge_counts = {
        int(
            row[
                "edges"
            ]
        )
        for row in rows
    }

    flow_values = {
        round(
            float(
                row[
                    "max_flow"
                ]
            ),
            9,
        )
        for row in rows
    }

    if len(
        vertex_counts
    ) != 1:
        raise RuntimeError(
            "solver comparison used different vertex counts"
        )

    if len(
        edge_counts
    ) != 1:
        raise RuntimeError(
            "solver comparison used different edge counts"
        )

    if len(
        flow_values
    ) != 1:
        raise RuntimeError(
            "solver comparison produced inconsistent max-flow values"
        )


def run_solver_group(
    builder_factory: Callable[
        [str],
        NetworkBuilder,
    ],
    family: str,
    graph_type: str,
    vertex_count: int,
) -> List[
    Dict[str, object]
]:
    """Run all three algorithms on equivalent networks."""
    rows = []

    for solver_name in [
        "Edmonds-Karp",
        "Push-Relabel",
        "Min-Cost Max-Flow",
    ]:
        builder = builder_factory(
            solver_name
        )

        row = measure_solver(
            solver_name,
            builder,
            family,
            graph_type,
            vertex_count,
        )

        rows.append(
            row
        )

        print(
            f"{family:16} "
            f"V={vertex_count:<7} "
            f"{solver_name:18} "
            f"time={row['runtime_seconds']:.6f}s "
            f"memory={row['peak_memory_mb']:.3f} MB "
            f"flow={row['max_flow']:g}"
        )

    validate_group_consistency(
        rows
    )

    return rows


def run_large_sparse(
    sizes: List[int],
) -> List[
    Dict[str, object]
]:
    """
    Benchmark large sparse chain networks.

    The same costed network structure is supplied to every
    solver. Edmonds-Karp and Push-Relabel simply ignore costs.
    """
    rows = []

    for size in sizes:

        def builder_factory(
            _solver_name: str,
        ) -> NetworkBuilder:
            return lambda: build_chain_network(
                size,
                with_costs=True,
            )

        rows.extend(
            run_solver_group(
                builder_factory,
                family="large_scaling",
                graph_type="sparse_chain",
                vertex_count=size,
            )
        )

    return rows


def run_dense_comparison(
    sizes: List[int],
    probability: float = 0.15,
) -> List[
    Dict[str, object]
]:
    """
    Benchmark denser acyclic networks at moderate sizes.

    All algorithms receive graphs generated with the same seed,
    capacities, topology, and costs.
    """
    rows = []

    for size in sizes:

        def builder_factory(
            _solver_name: str,
        ) -> NetworkBuilder:
            return lambda: generate_dense_network(
                size,
                edge_probability=probability,
                seed=1000 + size,
                min_capacity=1,
                max_capacity=20,
                with_costs=True,
            )

        rows.extend(
            run_solver_group(
                builder_factory,
                family="dense_comparison",
                graph_type="dense_dag",
                vertex_count=size,
            )
        )

    return rows


def save_results(
    rows: List[
        Dict[str, object]
    ],
) -> pd.DataFrame:
    """Save benchmark results to CSV."""
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe = pd.DataFrame(
        rows
    )

    output = (
        RESULTS_DIR
        / "flow_comparison_table.csv"
    )

    dataframe.to_csv(
        output,
        index=False,
    )

    print(
        f"\nSaved table: {output}"
    )

    return dataframe


def plot_runtime(
    dataframe: pd.DataFrame,
) -> None:
    """Plot runtime for the large sparse scaling experiment."""
    subset = dataframe[
        dataframe[
            "family"
        ]
        == "large_scaling"
    ]

    figure, axis = plt.subplots(
        figsize=(
            9,
            6,
        )
    )

    for solver in subset[
        "solver"
    ].unique():
        solver_rows = subset[
            subset[
                "solver"
            ]
            == solver
        ].sort_values(
            "vertices"
        )

        axis.plot(
            solver_rows[
                "vertices"
            ],
            solver_rows[
                "runtime_seconds"
            ],
            marker="o",
            label=solver,
        )

    axis.set_xlabel(
        "Vertices"
    )

    axis.set_ylabel(
        "Runtime (seconds)"
    )

    axis.set_title(
        "Flow Solver Runtime on Sparse Networks"
    )

    axis.legend()

    axis.grid(
        True,
        alpha=0.3,
    )

    figure.tight_layout()

    output = (
        RESULTS_DIR
        / "flow_runtime.png"
    )

    figure.savefig(
        output,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    print(
        f"Saved plot: {output}"
    )


def plot_memory(
    dataframe: pd.DataFrame,
) -> None:
    """Plot peak graph-plus-solver memory."""
    subset = dataframe[
        dataframe[
            "family"
        ]
        == "large_scaling"
    ]

    figure, axis = plt.subplots(
        figsize=(
            9,
            6,
        )
    )

    for solver in subset[
        "solver"
    ].unique():
        solver_rows = subset[
            subset[
                "solver"
            ]
            == solver
        ].sort_values(
            "vertices"
        )

        axis.plot(
            solver_rows[
                "vertices"
            ],
            solver_rows[
                "peak_memory_mb"
            ],
            marker="o",
            label=solver,
        )

    axis.set_xlabel(
        "Vertices"
    )

    axis.set_ylabel(
        "Peak traced memory (MB)"
    )

    axis.set_title(
        "Flow Solver Peak Memory on Sparse Networks"
    )

    axis.legend()

    axis.grid(
        True,
        alpha=0.3,
    )

    figure.tight_layout()

    output = (
        RESULTS_DIR
        / "flow_memory.png"
    )

    figure.savefig(
        output,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    print(
        f"Saved plot: {output}"
    )


def plot_convergence(
    dataframe: pd.DataFrame,
) -> None:
    """Plot solver operation counts."""
    subset = dataframe[
        dataframe[
            "family"
        ]
        == "large_scaling"
    ]

    figure, axis = plt.subplots(
        figsize=(
            9,
            6,
        )
    )

    for solver in subset[
        "solver"
    ].unique():
        solver_rows = subset[
            subset[
                "solver"
            ]
            == solver
        ].sort_values(
            "vertices"
        )

        axis.plot(
            solver_rows[
                "vertices"
            ],
            solver_rows[
                "operations"
            ],
            marker="o",
            label=solver,
        )

    axis.set_xlabel(
        "Vertices"
    )

    axis.set_ylabel(
        "Algorithm operations"
    )

    axis.set_title(
        "Flow Solver Convergence Activity"
    )

    axis.legend()

    axis.grid(
        True,
        alpha=0.3,
    )

    figure.tight_layout()

    output = (
        RESULTS_DIR
        / "flow_convergence.png"
    )

    figure.savefig(
        output,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    print(
        f"Saved plot: {output}"
    )


def run_benchmark(
    smoke: bool = True,
) -> pd.DataFrame:
    """Run smoke or full Week 10 benchmarks."""
    if smoke:
        sparse_sizes = [
            20,
            50,
            100,
        ]

        dense_sizes = [
            10,
            20,
            30,
        ]

        print(
            "Running Week 10 SMOKE benchmark\n"
        )

    else:
        sparse_sizes = [
            1000,
            5000,
            10000,
            25000,
            50000,
        ]

        dense_sizes = [
            25,
            50,
            100,
            200,
        ]

        print(
            "Running Week 10 FULL benchmark\n"
        )

    rows = []

    rows.extend(
        run_large_sparse(
            sparse_sizes
        )
    )

    rows.extend(
        run_dense_comparison(
            dense_sizes
        )
    )

    dataframe = save_results(
        rows
    )

    plot_runtime(
        dataframe
    )

    plot_memory(
        dataframe
    )

    plot_convergence(
        dataframe
    )

    print(
        "\nBenchmark complete."
    )

    return dataframe


def build_parser() -> argparse.ArgumentParser:
    """Create benchmark command-line options."""
    parser = argparse.ArgumentParser(
        description=(
            "Week 10 flow-network benchmark"
        )
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "--smoke",
        action="store_true",
        help="Run small validation benchmark",
    )

    mode.add_argument(
        "--full",
        action="store_true",
        help="Run full scaling benchmark through 50,000 vertices",
    )

    return parser


def main() -> None:
    """Run benchmark from the command line."""
    parser = build_parser()

    arguments = parser.parse_args()

    run_benchmark(
        smoke=not arguments.full
    )


if __name__ == "__main__":
    main()