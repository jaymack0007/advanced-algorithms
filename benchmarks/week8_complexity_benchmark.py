"""Week 8 computational complexity benchmark."""

import random
import statistics
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.complexity.satisfiability_solver import (
    random_sat_heuristic,
    sat_backtracking,
)
from src.complexity.subset_sum_backtracking import (
    greedy_subset_sum,
    subset_sum_backtracking,
)
from src.complexity.traveling_salesman_approx import (
    approximation_ratio as tsp_ratio,
    exact_tsp,
    nearest_neighbor_tsp,
)
from src.complexity.vertex_cover_approx import (
    approximation_ratio as vertex_cover_ratio,
    exact_vertex_cover,
    vertex_cover_2approx,
)


RESULTS_DIR = (
    PROJECT_ROOT
    / "benchmarks"
    / "results"
)

SUBSET_SIZES = [
    8,
    10,
    12,
    14,
    16,
    18,
]

SAT_SIZES = [
    6,
    8,
    10,
    12,
    14,
]

VERTEX_COVER_SIZES = [
    4,
    6,
    8,
    10,
    12,
]

TSP_SIZES = [
    4,
    5,
    6,
    7,
    8,
    9,
]


def elapsed_time(
    function,
    *args,
    **kwargs,
):
    """Return a function result and elapsed time."""
    start = time.perf_counter()

    result = function(
        *args,
        **kwargs,
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    return result, elapsed


def benchmark_subset_sum(
    sizes=None,
    trials=3,
):
    """
    Compare exact Subset Sum with the greedy heuristic.

    Target is deliberately larger than the total sum so the
    exact solver must explore the full include/exclude tree.
    """
    if sizes is None:
        sizes = SUBSET_SIZES

    rows = []

    for size in sizes:
        values = list(
            range(
                1,
                size + 1,
            )
        )

        target = (
            sum(values)
            + 1
        )

        exact_times = []
        nodes = []

        for _ in range(trials):
            stats = {}

            result, runtime = elapsed_time(
                subset_sum_backtracking,
                values,
                target,
                stats,
            )

            if result is not None:
                raise RuntimeError(
                    "Expected unsatisfiable Subset Sum instance"
                )

            exact_times.append(
                runtime
            )

            nodes.append(
                stats[
                    "nodes_visited"
                ]
            )

        greedy_times = []

        for _ in range(trials):
            result, runtime = elapsed_time(
                greedy_subset_sum,
                values,
                target,
            )

            if result is not None:
                raise RuntimeError(
                    "Expected greedy heuristic to return no solution"
                )

            greedy_times.append(
                runtime
            )

        rows.append(
            {
                "problem": "Subset Sum",
                "algorithm": "Exact Backtracking",
                "input_size": size,
                "mean_time_seconds": statistics.mean(
                    exact_times
                ),
                "runtime_variance": statistics.pvariance(
                    exact_times
                ),
                "nodes_visited": statistics.mean(
                    nodes
                ),
                "approximation_ratio": None,
                "success_rate": 1.0,
                "solution_size": None,
                "solution_cost": None,
            }
        )

        rows.append(
            {
                "problem": "Subset Sum",
                "algorithm": "Greedy Heuristic",
                "input_size": size,
                "mean_time_seconds": statistics.mean(
                    greedy_times
                ),
                "runtime_variance": statistics.pvariance(
                    greedy_times
                ),
                "nodes_visited": None,
                "approximation_ratio": None,
                "success_rate": 1.0,
                "solution_size": None,
                "solution_cost": None,
            }
        )

        print(
            f"Subset Sum n={size} complete."
        )

    return rows


def generate_sat_formula(
    variable_count,
    seed,
):
    """
    Generate a small satisfiable 3-CNF instance.

    Each clause contains at least one negative literal,
    so assigning every variable False satisfies the formula.
    """
    if variable_count < 3:
        raise ValueError(
            "variable_count must be at least 3"
        )

    random_generator = random.Random(
        seed
    )

    variables = [
        f"x{index}"
        for index in range(
            1,
            variable_count + 1,
        )
    ]

    clauses = []

    for _ in range(
        variable_count * 4
    ):
        chosen = random_generator.sample(
            variables,
            3,
        )

        literals = []

        for variable in chosen:
            if random_generator.random() < 0.5:
                literals.append(
                    f"~{variable}"
                )
            else:
                literals.append(
                    variable
                )

        if all(
            not literal.startswith(
                "~"
            )
            for literal in literals
        ):
            literals[0] = (
                f"~{chosen[0]}"
            )

        clauses.append(
            tuple(
                literals
            )
        )

    return clauses


def benchmark_sat(
    sizes=None,
    trials=3,
    heuristic_trials=100,
):
    """Compare exact SAT backtracking with random search."""
    if sizes is None:
        sizes = SAT_SIZES

    rows = []

    for size in sizes:
        clauses = generate_sat_formula(
            size,
            seed=1000 + size,
        )

        exact_times = []
        exact_nodes = []

        for _ in range(trials):
            stats = {}

            result, runtime = elapsed_time(
                sat_backtracking,
                clauses,
                stats,
            )

            if result is None:
                raise RuntimeError(
                    "Generated SAT instance should be satisfiable"
                )

            exact_times.append(
                runtime
            )

            exact_nodes.append(
                stats[
                    "nodes_visited"
                ]
            )

        heuristic_times = []
        heuristic_successes = 0

        for trial in range(
            trials
        ):
            result, runtime = elapsed_time(
                random_sat_heuristic,
                clauses,
                heuristic_trials,
                2000 + trial,
            )

            heuristic_times.append(
                runtime
            )

            if result is not None:
                heuristic_successes += 1

        rows.append(
            {
                "problem": "SAT",
                "algorithm": "Exact Backtracking",
                "input_size": size,
                "mean_time_seconds": statistics.mean(
                    exact_times
                ),
                "runtime_variance": statistics.pvariance(
                    exact_times
                ),
                "nodes_visited": statistics.mean(
                    exact_nodes
                ),
                "approximation_ratio": None,
                "success_rate": 1.0,
                "solution_size": None,
                "solution_cost": None,
            }
        )

        rows.append(
            {
                "problem": "SAT",
                "algorithm": "Random Heuristic",
                "input_size": size,
                "mean_time_seconds": statistics.mean(
                    heuristic_times
                ),
                "runtime_variance": statistics.pvariance(
                    heuristic_times
                ),
                "nodes_visited": None,
                "approximation_ratio": None,
                "success_rate": (
                    heuristic_successes
                    / trials
                ),
                "solution_size": None,
                "solution_cost": None,
            }
        )

        print(
            f"SAT variables={size} complete."
        )

    return rows


def cycle_graph(
    size,
):
    """Return the edge list for a cycle graph."""
    vertices = [
        f"v{index}"
        for index in range(
            size
        )
    ]

    return [
        (
            vertices[index],
            vertices[
                (index + 1)
                % size
            ],
        )
        for index in range(
            size
        )
    ]


def benchmark_vertex_cover(
    sizes=None,
):
    """Compare exact and 2-approximation Vertex Cover."""
    if sizes is None:
        sizes = VERTEX_COVER_SIZES

    rows = []

    for size in sizes:
        edges = cycle_graph(
            size
        )

        optimal, exact_time = elapsed_time(
            exact_vertex_cover,
            edges,
        )

        approximate, approx_time = elapsed_time(
            vertex_cover_2approx,
            edges,
        )

        ratio = vertex_cover_ratio(
            approximate,
            optimal,
        )

        rows.append(
            {
                "problem": "Vertex Cover",
                "algorithm": "Exact Exhaustive",
                "input_size": size,
                "mean_time_seconds": exact_time,
                "runtime_variance": 0.0,
                "nodes_visited": None,
                "approximation_ratio": 1.0,
                "success_rate": 1.0,
                "solution_size": len(
                    optimal
                ),
                "solution_cost": len(
                    optimal
                ),
            }
        )

        rows.append(
            {
                "problem": "Vertex Cover",
                "algorithm": "2-Approximation",
                "input_size": size,
                "mean_time_seconds": approx_time,
                "runtime_variance": 0.0,
                "nodes_visited": None,
                "approximation_ratio": ratio,
                "success_rate": 1.0,
                "solution_size": len(
                    approximate
                ),
                "solution_cost": len(
                    approximate
                ),
            }
        )

        print(
            f"Vertex Cover n={size} complete."
        )

    return rows


def generate_tsp_points(
    size,
    seed,
):
    """Generate reproducible two-dimensional TSP points."""
    random_generator = random.Random(
        seed
    )

    return {
        f"C{index}": (
            random_generator.uniform(
                0,
                100,
            ),
            random_generator.uniform(
                0,
                100,
            ),
        )
        for index in range(
            size
        )
    }


def benchmark_tsp(
    sizes=None,
):
    """Compare exact TSP with nearest-neighbor."""
    if sizes is None:
        sizes = TSP_SIZES

    rows = []

    for size in sizes:
        points = generate_tsp_points(
            size,
            seed=3000 + size,
        )

        (
            exact_result,
            exact_time,
        ) = elapsed_time(
            exact_tsp,
            points,
        )

        (
            heuristic_result,
            heuristic_time,
        ) = elapsed_time(
            nearest_neighbor_tsp,
            points,
        )

        _, optimal_length = (
            exact_result
        )

        _, heuristic_length = (
            heuristic_result
        )

        ratio = tsp_ratio(
            heuristic_length,
            optimal_length,
        )

        rows.append(
            {
                "problem": "TSP",
                "algorithm": "Exact Exhaustive",
                "input_size": size,
                "mean_time_seconds": exact_time,
                "runtime_variance": 0.0,
                "nodes_visited": None,
                "approximation_ratio": 1.0,
                "success_rate": 1.0,
                "solution_size": size,
                "solution_cost": optimal_length,
            }
        )

        rows.append(
            {
                "problem": "TSP",
                "algorithm": "Nearest Neighbor",
                "input_size": size,
                "mean_time_seconds": heuristic_time,
                "runtime_variance": 0.0,
                "nodes_visited": None,
                "approximation_ratio": ratio,
                "success_rate": 1.0,
                "solution_size": size,
                "solution_cost": heuristic_length,
            }
        )

        print(
            f"TSP cities={size} complete."
        )

    return rows


def plot_runtime_growth(
    dataframe,
):
    """Plot empirical runtime growth for the Week 8 algorithms."""
    figure, axes = plt.subplots(
        2,
        2,
        figsize=(12, 9),
    )

    configurations = [
        (
            "Subset Sum",
            axes[0][0],
        ),
        (
            "SAT",
            axes[0][1],
        ),
        (
            "Vertex Cover",
            axes[1][0],
        ),
        (
            "TSP",
            axes[1][1],
        ),
    ]

    for problem, axis in configurations:
        subset = dataframe[
            dataframe[
                "problem"
            ] == problem
        ]

        for algorithm in subset[
            "algorithm"
        ].unique():
            data = subset[
                subset[
                    "algorithm"
                ] == algorithm
            ].sort_values(
                "input_size"
            )

            axis.plot(
                data[
                    "input_size"
                ],
                data[
                    "mean_time_seconds"
                ],
                marker="o",
                label=algorithm,
            )

        axis.set_title(
            problem
        )

        axis.set_xlabel(
            "Input Size"
        )

        axis.set_ylabel(
            "Runtime (seconds)"
        )

        axis.set_yscale(
            "log"
        )

        axis.grid(
            True
        )

        axis.legend()

    figure.suptitle(
        "Runtime Growth: Exact vs Practical Methods"
    )

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "runtime_growth.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_approximation_quality(
    dataframe,
):
    """Plot approximation quality and runtime-quality trade-offs."""
    figure, axes = plt.subplots(
        2,
        2,
        figsize=(12, 9),
    )

    vertex_data = dataframe[
        (
            dataframe[
                "problem"
            ] == "Vertex Cover"
        )
        & (
            dataframe[
                "algorithm"
            ] == "2-Approximation"
        )
    ].sort_values(
        "input_size"
    )

    tsp_data = dataframe[
        (
            dataframe[
                "problem"
            ] == "TSP"
        )
        & (
            dataframe[
                "algorithm"
            ] == "Nearest Neighbor"
        )
    ].sort_values(
        "input_size"
    )

    axes[0][0].plot(
        vertex_data[
            "input_size"
        ],
        vertex_data[
            "approximation_ratio"
        ],
        marker="o",
    )

    axes[0][0].axhline(
        2.0,
        linestyle="--",
        label="2x Guarantee",
    )

    axes[0][0].set_title(
        "Vertex Cover Approximation Ratio"
    )

    axes[0][0].set_xlabel(
        "Vertices"
    )

    axes[0][0].set_ylabel(
        "Approximate / Optimal"
    )

    axes[0][0].legend()

    axes[0][0].grid(
        True
    )

    axes[0][1].plot(
        tsp_data[
            "input_size"
        ],
        tsp_data[
            "approximation_ratio"
        ],
        marker="o",
    )

    axes[0][1].axhline(
        1.0,
        linestyle="--",
        label="Optimal",
    )

    axes[0][1].set_title(
        "TSP Nearest-Neighbor Quality"
    )

    axes[0][1].set_xlabel(
        "Cities"
    )

    axes[0][1].set_ylabel(
        "Heuristic / Optimal"
    )

    axes[0][1].legend()

    axes[0][1].grid(
        True
    )

    axes[1][0].scatter(
        vertex_data[
            "mean_time_seconds"
        ],
        vertex_data[
            "approximation_ratio"
        ],
    )

    axes[1][0].set_title(
        "Vertex Cover Runtime vs Quality"
    )

    axes[1][0].set_xlabel(
        "Approximation Runtime (seconds)"
    )

    axes[1][0].set_ylabel(
        "Approximation Ratio"
    )

    axes[1][0].grid(
        True
    )

    axes[1][1].scatter(
        tsp_data[
            "mean_time_seconds"
        ],
        tsp_data[
            "approximation_ratio"
        ],
    )

    axes[1][1].set_title(
        "TSP Runtime vs Quality"
    )

    axes[1][1].set_xlabel(
        "Heuristic Runtime (seconds)"
    )

    axes[1][1].set_ylabel(
        "Approximation Ratio"
    )

    axes[1][1].grid(
        True
    )

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "approximation_quality.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def main():
    """Run all Week 8 benchmarks and export results."""
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "Running Week 8 complexity benchmarks..."
    )
    print()

    rows = []

    rows.extend(
        benchmark_subset_sum()
    )

    rows.extend(
        benchmark_sat()
    )

    rows.extend(
        benchmark_vertex_cover()
    )

    rows.extend(
        benchmark_tsp()
    )

    dataframe = pd.DataFrame(
        rows
    )

    dataframe.to_csv(
        RESULTS_DIR
        / "comparison_table.csv",
        index=False,
    )

    plot_runtime_growth(
        dataframe
    )

    plot_approximation_quality(
        dataframe
    )

    print()
    print(
        dataframe.to_string(
            index=False
        )
    )

    print()
    print(
        "Week 8 benchmark complete."
    )

    print(
        "Results saved to:"
    )

    print(
        RESULTS_DIR
    )


if __name__ == "__main__":
    main()