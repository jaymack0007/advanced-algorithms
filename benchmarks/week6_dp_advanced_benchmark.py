"""Week 6 advanced dynamic programming benchmarks."""

import sys
import time
import tracemalloc
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.dp.knapsack import (
    knapsack_tabulated,
)
from src.dp_advanced.bitmask_traveling_salesman import (
    tsp_bitmask,
    tsp_brute_force,
)
from src.dp_advanced.floyd_warshall import (
    floyd_warshall,
)
from src.dp_advanced.matrix_chain_multiplication import (
    matrix_chain_bottom_up,
    matrix_chain_memoized,
)
from src.dp_advanced.space_optimized_knapsack import (
    space_optimized_knapsack,
)
from src.graphs.dijkstra import (
    dijkstra,
)
from src.graphs.graph import Graph
from src.utils.matrix_utils import (
    generate_complete_distance_matrix,
    generate_matrix_dimensions,
    generate_weighted_graph_matrix,
)


RESULTS_DIR = PROJECT_ROOT / "benchmarks" / "results"

KNAPSACK_SIZES = [
    20,
    40,
    80,
    120,
]

MCM_SIZES = [
    5,
    10,
    20,
    30,
    40,
]

FLOYD_SIZES = [
    50,
    100,
    200,
    500,
]

TSP_SIZES = [
    4,
    6,
    8,
    10,
    12,
]


def measure(
    function,
    *args,
):
    """Measure execution time and peak traced memory."""
    tracemalloc.start()

    start = time.perf_counter()

    result = function(
        *args,
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    _, peak_memory = (
        tracemalloc.get_traced_memory()
    )

    tracemalloc.stop()

    return (
        result,
        elapsed,
        peak_memory,
    )


def make_knapsack_data(
    item_count,
):
    """Create deterministic Knapsack benchmark data."""
    weights = [
        (index % 10) + 1
        for index in range(item_count)
    ]

    values = [
        ((index * 7) % 25) + 5
        for index in range(item_count)
    ]

    capacity = max(
        1,
        sum(weights) // 3,
    )

    return (
        weights,
        values,
        capacity,
    )


def benchmark_knapsack(
    sizes=None,
):
    """Compare standard and space-optimized Knapsack."""
    if sizes is None:
        sizes = KNAPSACK_SIZES

    rows = []

    for item_count in sizes:
        weights, values, capacity = (
            make_knapsack_data(
                item_count
            )
        )

        (
            standard_result,
            standard_time,
            standard_memory,
        ) = measure(
            knapsack_tabulated,
            weights,
            values,
            capacity,
        )

        (
            optimized_result,
            optimized_time,
            optimized_memory,
        ) = measure(
            space_optimized_knapsack,
            weights,
            values,
            capacity,
        )

        if standard_result != optimized_result:
            raise RuntimeError(
                "Knapsack implementations disagree"
            )

        rows.append(
            {
                "problem": "Knapsack",
                "algorithm": "Standard DP",
                "input_size": item_count,
                "time_seconds": standard_time,
                "memory_bytes": standard_memory,
                "speedup": 1.0,
                "status": "measured",
            }
        )

        rows.append(
            {
                "problem": "Knapsack",
                "algorithm": "Space Optimized",
                "input_size": item_count,
                "time_seconds": optimized_time,
                "memory_bytes": optimized_memory,
                "speedup": (
                    standard_time
                    / optimized_time
                ),
                "status": "measured",
            }
        )

        print(
            f"Knapsack size {item_count} complete."
        )

    return rows


def benchmark_mcm(
    sizes=None,
):
    """Compare memoized and bottom-up MCM."""
    if sizes is None:
        sizes = MCM_SIZES

    rows = []

    for matrix_count in sizes:
        dimensions = (
            generate_matrix_dimensions(
                matrix_count,
                seed=42 + matrix_count,
            )
        )

        (
            memo_result,
            memo_time,
            memo_memory,
        ) = measure(
            matrix_chain_memoized,
            dimensions,
        )

        (
            bottom_result,
            bottom_time,
            bottom_memory,
        ) = measure(
            matrix_chain_bottom_up,
            dimensions,
        )

        if memo_result[0] != bottom_result[0]:
            raise RuntimeError(
                "MCM implementations disagree"
            )

        rows.append(
            {
                "problem": "MCM",
                "algorithm": "Memoized",
                "input_size": matrix_count,
                "time_seconds": memo_time,
                "memory_bytes": memo_memory,
                "speedup": 1.0,
                "status": "measured",
            }
        )

        rows.append(
            {
                "problem": "MCM",
                "algorithm": "Bottom Up",
                "input_size": matrix_count,
                "time_seconds": bottom_time,
                "memory_bytes": bottom_memory,
                "speedup": (
                    memo_time
                    / bottom_time
                ),
                "status": "measured",
            }
        )

        print(
            f"MCM size {matrix_count} complete."
        )

    return rows


def matrix_to_graph(
    matrix,
):
    """Convert an adjacency matrix into the Week 4 Graph."""
    graph = Graph(
        directed=True,
        weighted=True,
    )

    size = len(matrix)

    for vertex in range(size):
        graph.add_node(vertex)

    for i in range(size):
        for j in range(size):
            weight = matrix[i][j]

            if (
                i != j
                and weight != float("inf")
            ):
                graph.add_edge(
                    i,
                    j,
                    weight,
                )

    return graph


def benchmark_floyd_warshall(
    sizes=None,
):
    """Benchmark Floyd-Warshall and compare small cases to Dijkstra."""
    if sizes is None:
        sizes = FLOYD_SIZES

    rows = []

    for size in sizes:
        matrix = generate_weighted_graph_matrix(
            size,
            density=0.10,
            seed=42 + size,
        )

        (
            floyd_result,
            floyd_time,
            floyd_memory,
        ) = measure(
            floyd_warshall,
            matrix,
        )

        rows.append(
            {
                "problem": "Floyd-Warshall",
                "algorithm": "Floyd-Warshall",
                "input_size": size,
                "time_seconds": floyd_time,
                "memory_bytes": floyd_memory,
                "speedup": None,
                "status": "measured",
            }
        )

        if size <= 100:
            graph = matrix_to_graph(
                matrix
            )

            start = time.perf_counter()

            all_distances = {}

            for source in range(size):
                distances, _ = dijkstra(
                    graph,
                    source,
                )

                all_distances[source] = (
                    distances
                )

            dijkstra_time = (
                time.perf_counter()
                - start
            )

            floyd_distances = floyd_result[0]

            for source in range(size):
                for target in range(size):
                    if (
                        all_distances[source][target]
                        != floyd_distances[source][target]
                    ):
                        raise RuntimeError(
                            "Floyd-Warshall and "
                            "Dijkstra disagree"
                        )

            rows.append(
                {
                    "problem": "Floyd-Warshall",
                    "algorithm": "Repeated Dijkstra",
                    "input_size": size,
                    "time_seconds": dijkstra_time,
                    "memory_bytes": None,
                    "speedup": (
                        floyd_time
                        / dijkstra_time
                    ),
                    "status": "measured",
                }
            )

        print(
            f"Floyd-Warshall size {size} complete."
        )

    return rows


def benchmark_tsp(
    sizes=None,
    brute_force_max=10,
):
    """Compare bitmask TSP with brute force."""
    if sizes is None:
        sizes = TSP_SIZES

    rows = []

    for size in sizes:
        distances = (
            generate_complete_distance_matrix(
                size,
                seed=42 + size,
            )
        )

        (
            bitmask_result,
            bitmask_time,
            bitmask_memory,
        ) = measure(
            tsp_bitmask,
            distances,
        )

        brute_time = None

        if size <= brute_force_max:
            (
                brute_result,
                brute_time,
                brute_memory,
            ) = measure(
                tsp_brute_force,
                distances,
            )

            if (
                bitmask_result[0]
                != brute_result[0]
            ):
                raise RuntimeError(
                    "TSP implementations disagree"
                )

            rows.append(
                {
                    "problem": "TSP",
                    "algorithm": "Brute Force",
                    "input_size": size,
                    "time_seconds": brute_time,
                    "memory_bytes": brute_memory,
                    "speedup": 1.0,
                    "status": "measured",
                }
            )

        else:
            rows.append(
                {
                    "problem": "TSP",
                    "algorithm": "Brute Force",
                    "input_size": size,
                    "time_seconds": None,
                    "memory_bytes": None,
                    "speedup": None,
                    "status": "skipped_factorial",
                }
            )

        speedup = None

        if brute_time is not None:
            speedup = (
                brute_time
                / bitmask_time
            )

        rows.append(
            {
                "problem": "TSP",
                "algorithm": "Bitmask DP",
                "input_size": size,
                "time_seconds": bitmask_time,
                "memory_bytes": bitmask_memory,
                "speedup": speedup,
                "status": "measured",
            }
        )

        print(
            f"TSP size {size} complete."
        )

    return rows


def plot_comparison(
    dataframe,
    problem,
    filename,
    title,
):
    """Create runtime and memory plots."""
    subset = dataframe[
        dataframe["problem"] == problem
    ]

    figure, axes = plt.subplots(
        1,
        2,
        figsize=(12, 5),
    )

    for algorithm in subset[
        "algorithm"
    ].unique():
        data = subset[
            subset["algorithm"] == algorithm
        ].sort_values(
            "input_size"
        )

        runtime_data = data[
            data["time_seconds"].notna()
        ]

        axes[0].plot(
            runtime_data["input_size"],
            runtime_data["time_seconds"],
            marker="o",
            label=algorithm,
        )

        memory_data = data[
            data["memory_bytes"].notna()
        ]

        if not memory_data.empty:
            axes[1].plot(
                memory_data["input_size"],
                memory_data["memory_bytes"],
                marker="o",
                label=algorithm,
            )

    axes[0].set_title(
        f"{title} Runtime"
    )
    axes[0].set_xlabel(
        "Input Size"
    )
    axes[0].set_ylabel(
        "Time (seconds)"
    )
    axes[0].set_yscale(
        "log"
    )
    axes[0].grid(True)
    axes[0].legend()

    axes[1].set_title(
        f"{title} Memory"
    )
    axes[1].set_xlabel(
        "Input Size"
    )
    axes[1].set_ylabel(
        "Peak Memory (bytes)"
    )
    axes[1].set_yscale(
        "log"
    )
    axes[1].grid(True)
    axes[1].legend()

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR / filename,
        bbox_inches="tight",
    )

    plt.close(figure)


def main():
    """Run all Week 6 benchmarks."""
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "Running Week 6 advanced DP benchmarks..."
    )
    print()

    rows = []

    rows.extend(
        benchmark_knapsack()
    )

    rows.extend(
        benchmark_mcm()
    )

    rows.extend(
        benchmark_floyd_warshall()
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

    plot_comparison(
        dataframe,
        "Knapsack",
        "knapsack_space_comparison.png",
        "Knapsack",
    )

    plot_comparison(
        dataframe,
        "MCM",
        "mcm_performance.png",
        "Matrix Chain Multiplication",
    )

    plot_comparison(
        dataframe,
        "Floyd-Warshall",
        "floyd_warshall_scaling.png",
        "Floyd-Warshall",
    )

    plot_comparison(
        dataframe,
        "TSP",
        "tsp_bitmask_runtime.png",
        "Traveling Salesman",
    )

    print()
    print(
        dataframe.to_string(
            index=False
        )
    )

    print()
    print(
        "Week 6 benchmark complete."
    )

    print(
        "Results saved to:"
    )

    print(
        RESULTS_DIR
    )


if __name__ == "__main__":
    main()