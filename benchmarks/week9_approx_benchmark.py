"""Week 9 approximation-algorithm benchmark."""

import random
import statistics
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from src.approximation.facility_location_greedy import (
    approximation_ratio as facility_ratio,
    exact_facility_location,
    greedy_facility_location,
)
from src.approximation.maxcut_randomized import (
    approximation_ratio as maxcut_ratio,
    exact_maxcut,
    local_search_maxcut,
    randomized_maxcut,
)
from src.approximation.set_cover_lpround import (
    approximation_ratio as set_cover_ratio,
    deterministic_lp_rounding,
    exact_set_cover,
    randomized_lp_rounding,
)
from src.approximation.tsp_metric_approx import (
    approximation_ratio as tsp_ratio,
    exact_metric_tsp,
    mst_doubling_tsp,
)
from src.approximation.vertex_cover_2approx import (
    approximation_ratio as vertex_cover_ratio,
    exact_vertex_cover,
    vertex_cover_2approx,
)
from src.utils.graph_utils import (
    cycle_edges,
    euclidean_distance,
    generate_points,
    random_graph_edges,
)


RESULTS_DIR = (
    PROJECT_ROOT
    / "benchmarks"
    / "results"
)

VERTEX_COVER_SIZES = [
    4,
    6,
    8,
    10,
    12,
]

FACILITY_SIZES = [
    3,
    4,
    5,
    6,
    7,
]

SET_COVER_SIZES = [
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

MAXCUT_SIZES = [
    6,
    8,
    10,
    12,
    14,
]


def elapsed_time(
    function,
    *args,
    **kwargs,
):
    """Return a function result and elapsed execution time."""
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


def make_row(
    problem,
    algorithm,
    input_size,
    mean_time,
    runtime_variance,
    solution_value,
    optimal_value,
    ratio,
    quality_variance=0.0,
    trials=1,
    lp_lower_bound=None,
):
    """Create one standardized benchmark-result row."""
    return {
        "problem": problem,
        "algorithm": algorithm,
        "input_size": input_size,
        "mean_time_seconds": mean_time,
        "runtime_variance": runtime_variance,
        "solution_value": solution_value,
        "optimal_value": optimal_value,
        "approximation_ratio": ratio,
        "quality_variance": quality_variance,
        "trials": trials,
        "lp_lower_bound": lp_lower_bound,
    }


def benchmark_vertex_cover(
    sizes=None,
):
    """Compare exact and 2-approximation Vertex Cover."""
    if sizes is None:
        sizes = VERTEX_COVER_SIZES

    rows = []

    for size in sizes:
        edges = cycle_edges(
            size,
            prefix="V",
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
            make_row(
                "Vertex Cover",
                "Exact Exhaustive",
                size,
                exact_time,
                0.0,
                len(optimal),
                len(optimal),
                1.0,
            )
        )

        rows.append(
            make_row(
                "Vertex Cover",
                "2-Approximation",
                size,
                approx_time,
                0.0,
                len(approximate),
                len(optimal),
                ratio,
            )
        )

        print(
            f"Vertex Cover n={size} complete."
        )

    return rows


def generate_facility_instance(
    facility_count,
    seed,
):
    """Generate a reproducible geometric facility instance."""
    client_count = (
        facility_count
        * 2
    )

    facility_points = generate_points(
        facility_count,
        seed,
        prefix="F",
    )

    client_points = generate_points(
        client_count,
        seed + 1000,
        prefix="C",
    )

    generator = random.Random(
        seed + 2000
    )

    opening_costs = {
        facility: generator.uniform(
            20.0,
            45.0,
        )
        for facility in facility_points
    }

    service_costs = {}

    for facility, facility_point in facility_points.items():
        for client, client_point in client_points.items():
            service_costs[
                (
                    facility,
                    client,
                )
            ] = euclidean_distance(
                facility_point,
                client_point,
            )

    return (
        opening_costs,
        sorted(
            client_points
        ),
        service_costs,
    )


def benchmark_facility_location(
    sizes=None,
):
    """Compare greedy and exact Facility Location."""
    if sizes is None:
        sizes = FACILITY_SIZES

    rows = []

    for size in sizes:
        (
            opening_costs,
            clients,
            service_costs,
        ) = generate_facility_instance(
            size,
            seed=2000 + size,
        )

        optimal, exact_time = elapsed_time(
            exact_facility_location,
            opening_costs,
            clients,
            service_costs,
        )

        greedy, greedy_time = elapsed_time(
            greedy_facility_location,
            opening_costs,
            clients,
            service_costs,
        )

        ratio = facility_ratio(
            greedy.total_cost,
            optimal.total_cost,
        )

        rows.append(
            make_row(
                "Facility Location",
                "Exact Exhaustive",
                size,
                exact_time,
                0.0,
                optimal.total_cost,
                optimal.total_cost,
                1.0,
            )
        )

        rows.append(
            make_row(
                "Facility Location",
                "Greedy Heuristic",
                size,
                greedy_time,
                0.0,
                greedy.total_cost,
                optimal.total_cost,
                ratio,
            )
        )

        print(
            f"Facility Location facilities={size} complete."
        )

    return rows


def generate_set_cover_instance(
    universe_size,
    seed,
):
    """Generate a reproducible weighted Set Cover instance."""
    generator = random.Random(
        seed
    )

    universe = {
        f"E{index}"
        for index in range(
            universe_size
        )
    }

    subset_count = (
        universe_size
        + 2
    )

    subsets = {}

    ordered_elements = sorted(
        universe
    )

    for subset_index in range(
        subset_count
    ):
        members = {
            element
            for element in ordered_elements
            if generator.random() < 0.45
        }

        if not members:
            members.add(
                generator.choice(
                    ordered_elements
                )
            )

        subsets[
            f"S{subset_index}"
        ] = members

    covered = set().union(
        *subsets.values()
    )

    missing = (
        universe
        - covered
    )

    for element in sorted(
        missing
    ):
        chosen_name = generator.choice(
            sorted(
                subsets
            )
        )

        subsets[
            chosen_name
        ].add(
            element
        )

    costs = {
        name: float(
            generator.randint(
                1,
                10,
            )
        )
        for name in subsets
    }

    return (
        universe,
        subsets,
        costs,
    )


def benchmark_set_cover(
    sizes=None,
    randomized_trials=30,
):
    """Compare exact, deterministic, and randomized Set Cover."""
    if sizes is None:
        sizes = SET_COVER_SIZES

    rows = []

    for size in sizes:
        (
            universe,
            subsets,
            costs,
        ) = generate_set_cover_instance(
            size,
            seed=3000 + size,
        )

        optimal, exact_time = elapsed_time(
            exact_set_cover,
            universe,
            subsets,
            costs,
        )

        deterministic, deterministic_time = elapsed_time(
            deterministic_lp_rounding,
            universe,
            subsets,
            costs,
        )

        deterministic_ratio = set_cover_ratio(
            deterministic.total_cost,
            optimal.total_cost,
        )

        randomized_costs = []
        randomized_times = []

        for trial in range(
            randomized_trials
        ):
            result, runtime = elapsed_time(
                randomized_lp_rounding,
                universe,
                subsets,
                costs,
                4000 + trial,
            )

            randomized_costs.append(
                result.total_cost
            )

            randomized_times.append(
                runtime
            )

        random_mean_cost = statistics.mean(
            randomized_costs
        )

        random_ratio = set_cover_ratio(
            random_mean_cost,
            optimal.total_cost,
        )

        rows.append(
            make_row(
                "Set Cover",
                "Exact Exhaustive",
                size,
                exact_time,
                0.0,
                optimal.total_cost,
                optimal.total_cost,
                1.0,
                lp_lower_bound=optimal.lp_cost,
            )
        )

        rows.append(
            make_row(
                "Set Cover",
                "Deterministic LP Rounding",
                size,
                deterministic_time,
                0.0,
                deterministic.total_cost,
                optimal.total_cost,
                deterministic_ratio,
                lp_lower_bound=deterministic.lp_cost,
            )
        )

        rows.append(
            make_row(
                "Set Cover",
                "Randomized LP Rounding",
                size,
                statistics.mean(
                    randomized_times
                ),
                statistics.pvariance(
                    randomized_times
                ),
                random_mean_cost,
                optimal.total_cost,
                random_ratio,
                quality_variance=statistics.pvariance(
                    randomized_costs
                ),
                trials=randomized_trials,
                lp_lower_bound=optimal.lp_cost,
            )
        )

        print(
            f"Set Cover universe={size} complete."
        )

    return rows


def benchmark_tsp(
    sizes=None,
):
    """Compare exact TSP with MST doubling."""
    if sizes is None:
        sizes = TSP_SIZES

    rows = []

    for size in sizes:
        points = generate_points(
            size,
            seed=5000 + size,
            prefix="C",
        )

        exact_result, exact_time = elapsed_time(
            exact_metric_tsp,
            points,
        )

        approx_result, approx_time = elapsed_time(
            mst_doubling_tsp,
            points,
        )

        _, optimal_cost = exact_result
        _, approximate_cost = approx_result

        ratio = tsp_ratio(
            approximate_cost,
            optimal_cost,
        )

        rows.append(
            make_row(
                "Metric TSP",
                "Exact Exhaustive",
                size,
                exact_time,
                0.0,
                optimal_cost,
                optimal_cost,
                1.0,
            )
        )

        rows.append(
            make_row(
                "Metric TSP",
                "MST Doubling",
                size,
                approx_time,
                0.0,
                approximate_cost,
                optimal_cost,
                ratio,
            )
        )

        print(
            f"Metric TSP cities={size} complete."
        )

    return rows


def benchmark_maxcut(
    sizes=None,
    randomized_trials=100,
    local_trials=30,
):
    """Compare exact, randomized, and local-search Max-Cut."""
    if sizes is None:
        sizes = MAXCUT_SIZES

    rows = []

    for size in sizes:
        edges = random_graph_edges(
            size,
            0.35,
            seed=6000 + size,
            prefix="V",
        )

        optimal, exact_time = elapsed_time(
            exact_maxcut,
            edges,
        )

        random_values = []
        random_times = []

        for trial in range(
            randomized_trials
        ):
            result, runtime = elapsed_time(
                randomized_maxcut,
                edges,
                7000 + trial,
            )

            random_values.append(
                result.cut_value
            )

            random_times.append(
                runtime
            )

        local_values = []
        local_times = []

        for trial in range(
            local_trials
        ):
            result, runtime = elapsed_time(
                local_search_maxcut,
                edges,
                8000 + trial,
            )

            local_values.append(
                result.cut_value
            )

            local_times.append(
                runtime
            )

        random_mean = statistics.mean(
            random_values
        )

        local_mean = statistics.mean(
            local_values
        )

        rows.append(
            make_row(
                "Max-Cut",
                "Exact Exhaustive",
                size,
                exact_time,
                0.0,
                optimal.cut_value,
                optimal.cut_value,
                1.0,
            )
        )

        rows.append(
            make_row(
                "Max-Cut",
                "Randomized",
                size,
                statistics.mean(
                    random_times
                ),
                statistics.pvariance(
                    random_times
                ),
                random_mean,
                optimal.cut_value,
                maxcut_ratio(
                    random_mean,
                    optimal.cut_value,
                ),
                quality_variance=statistics.pvariance(
                    random_values
                ),
                trials=randomized_trials,
            )
        )

        rows.append(
            make_row(
                "Max-Cut",
                "Local Search",
                size,
                statistics.mean(
                    local_times
                ),
                statistics.pvariance(
                    local_times
                ),
                local_mean,
                optimal.cut_value,
                maxcut_ratio(
                    local_mean,
                    optimal.cut_value,
                ),
                quality_variance=statistics.pvariance(
                    local_values
                ),
                trials=local_trials,
            )
        )

        print(
            f"Max-Cut vertices={size} complete."
        )

    return rows


def plot_approximation_ratios(
    dataframe,
):
    """Plot approximation ratios for minimization and maximization."""
    figure, axes = plt.subplots(
        1,
        2,
        figsize=(13, 5),
    )

    minimization = [
        (
            "Vertex Cover",
            "2-Approximation",
        ),
        (
            "Facility Location",
            "Greedy Heuristic",
        ),
        (
            "Set Cover",
            "Deterministic LP Rounding",
        ),
        (
            "Set Cover",
            "Randomized LP Rounding",
        ),
        (
            "Metric TSP",
            "MST Doubling",
        ),
    ]

    for problem, algorithm in minimization:
        data = dataframe[
            (
                dataframe[
                    "problem"
                ] == problem
            )
            & (
                dataframe[
                    "algorithm"
                ] == algorithm
            )
        ].sort_values(
            "input_size"
        )

        axes[0].plot(
            data[
                "input_size"
            ],
            data[
                "approximation_ratio"
            ],
            marker="o",
            label=f"{problem}: {algorithm}",
        )

    axes[0].axhline(
        1.0,
        linestyle="--",
        label="Optimal",
    )

    axes[0].set_title(
        "Minimization Approximation Ratios"
    )

    axes[0].set_xlabel(
        "Input Size"
    )

    axes[0].set_ylabel(
        "Approximate Cost / Optimal Cost"
    )

    axes[0].grid(
        True
    )

    axes[0].legend(
        fontsize=8
    )

    for algorithm in [
        "Randomized",
        "Local Search",
    ]:
        data = dataframe[
            (
                dataframe[
                    "problem"
                ] == "Max-Cut"
            )
            & (
                dataframe[
                    "algorithm"
                ] == algorithm
            )
        ].sort_values(
            "input_size"
        )

        axes[1].plot(
            data[
                "input_size"
            ],
            data[
                "approximation_ratio"
            ],
            marker="o",
            label=algorithm,
        )

    axes[1].axhline(
        1.0,
        linestyle="--",
        label="Optimal",
    )

    axes[1].axhline(
        0.5,
        linestyle=":",
        label="1/2 Guarantee",
    )

    axes[1].set_title(
        "Max-Cut Approximation Ratios"
    )

    axes[1].set_xlabel(
        "Vertices"
    )

    axes[1].set_ylabel(
        "Approximate Value / Optimal Value"
    )

    axes[1].grid(
        True
    )

    axes[1].legend()

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "approx_ratios.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_cost_vs_optimal(
    dataframe,
):
    """Plot approximate solution cost against optimal cost."""
    figure, axes = plt.subplots(
        2,
        2,
        figsize=(12, 9),
    )

    configurations = [
        (
            "Vertex Cover",
            "2-Approximation",
            axes[0][0],
        ),
        (
            "Facility Location",
            "Greedy Heuristic",
            axes[0][1],
        ),
        (
            "Set Cover",
            "Deterministic LP Rounding",
            axes[1][0],
        ),
        (
            "Metric TSP",
            "MST Doubling",
            axes[1][1],
        ),
    ]

    for problem, algorithm, axis in configurations:
        data = dataframe[
            (
                dataframe[
                    "problem"
                ] == problem
            )
            & (
                dataframe[
                    "algorithm"
                ] == algorithm
            )
        ].sort_values(
            "input_size"
        )

        axis.plot(
            data[
                "input_size"
            ],
            data[
                "optimal_value"
            ],
            marker="o",
            label="Optimal",
        )

        axis.plot(
            data[
                "input_size"
            ],
            data[
                "solution_value"
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
            "Solution Cost"
        )

        axis.grid(
            True
        )

        axis.legend()

    figure.suptitle(
        "Approximate Solution Cost vs Optimal"
    )

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "cost_vs_optimal.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_randomized_maxcut(
    dataframe,
):
    """Plot randomized Max-Cut quality and variance."""
    figure, axes = plt.subplots(
        1,
        2,
        figsize=(12, 5),
    )

    random_data = dataframe[
        (
            dataframe[
                "problem"
            ] == "Max-Cut"
        )
        & (
            dataframe[
                "algorithm"
            ] == "Randomized"
        )
    ].sort_values(
        "input_size"
    )

    local_data = dataframe[
        (
            dataframe[
                "problem"
            ] == "Max-Cut"
        )
        & (
            dataframe[
                "algorithm"
            ] == "Local Search"
        )
    ].sort_values(
        "input_size"
    )

    exact_data = dataframe[
        (
            dataframe[
                "problem"
            ] == "Max-Cut"
        )
        & (
            dataframe[
                "algorithm"
            ] == "Exact Exhaustive"
        )
    ].sort_values(
        "input_size"
    )

    axes[0].plot(
        exact_data[
            "input_size"
        ],
        exact_data[
            "solution_value"
        ],
        marker="o",
        label="Optimal",
    )

    axes[0].plot(
        random_data[
            "input_size"
        ],
        random_data[
            "solution_value"
        ],
        marker="o",
        label="Randomized Mean",
    )

    axes[0].plot(
        local_data[
            "input_size"
        ],
        local_data[
            "solution_value"
        ],
        marker="o",
        label="Local Search Mean",
    )

    axes[0].set_title(
        "Max-Cut Solution Quality"
    )

    axes[0].set_xlabel(
        "Vertices"
    )

    axes[0].set_ylabel(
        "Cut Value"
    )

    axes[0].grid(
        True
    )

    axes[0].legend()

    axes[1].plot(
        random_data[
            "input_size"
        ],
        random_data[
            "quality_variance"
        ],
        marker="o",
        label="Randomized Variance",
    )

    axes[1].plot(
        local_data[
            "input_size"
        ],
        local_data[
            "quality_variance"
        ],
        marker="o",
        label="Local Search Variance",
    )

    axes[1].set_title(
        "Max-Cut Trial Variance"
    )

    axes[1].set_xlabel(
        "Vertices"
    )

    axes[1].set_ylabel(
        "Cut-Value Variance"
    )

    axes[1].grid(
        True
    )

    axes[1].legend()

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "randomized_maxcut_results.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def main():
    """Run all Week 9 approximation benchmarks."""
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "Running Week 9 approximation benchmarks..."
    )

    print()

    rows = []

    rows.extend(
        benchmark_vertex_cover()
    )

    rows.extend(
        benchmark_facility_location()
    )

    rows.extend(
        benchmark_set_cover()
    )

    rows.extend(
        benchmark_tsp()
    )

    rows.extend(
        benchmark_maxcut()
    )

    dataframe = pd.DataFrame(
        rows
    )

    dataframe.to_csv(
        RESULTS_DIR
        / "comparison_table.csv",
        index=False,
    )

    plot_approximation_ratios(
        dataframe
    )

    plot_cost_vs_optimal(
        dataframe
    )

    plot_randomized_maxcut(
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
        "Week 9 benchmark complete."
    )

    print(
        "Results saved to:"
    )

    print(
        RESULTS_DIR
    )


if __name__ == "__main__":
    main()