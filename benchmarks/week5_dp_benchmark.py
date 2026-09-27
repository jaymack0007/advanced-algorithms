"""Week 5 dynamic programming benchmarks."""

import random
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.dp.fibonacci import (
    fibonacci_memoized,
    fibonacci_recursive,
    fibonacci_tabulated,
)
from src.dp.knapsack import (
    knapsack_memoized,
    knapsack_recursive,
    knapsack_tabulated,
)
from src.dp.lcs import (
    lcs_memoized,
    lcs_recursive,
    lcs_tabulated,
)
from src.utils.timer import measure_function


RESULTS_DIR = PROJECT_ROOT / "benchmarks" / "results"

FIBONACCI_SIZES = [
    10,
    20,
    30,
    35,
    40,
    45,
]

KNAPSACK_SIZES = [
    5,
    10,
    15,
    20,
    30,
    40,
]

LCS_SIZES = [
    10,
    50,
    100,
    250,
    500,
    1000,
]


def fibonacci_recursive_call_count(n: int) -> int:
    """
    Return the exact number of calls made by naive Fibonacci.

    For the standard recursive implementation:
    calls(n) = 2 * Fibonacci(n + 1) - 1
    """
    return (
        2 * fibonacci_tabulated(n + 1)
        - 1
    )


def benchmark_fibonacci(
    sizes=None,
    naive_max=30,
):
    """Benchmark recursive and DP Fibonacci versions."""
    if sizes is None:
        sizes = FIBONACCI_SIZES

    rows = []

    for n in sizes:
        naive_time = None

        if n <= naive_max:
            stats = {}

            result = measure_function(
                fibonacci_recursive,
                n,
                stats=stats,
            )

            naive_time = result["time_seconds"]

            rows.append(
                {
                    "problem": "Fibonacci",
                    "algorithm": "Naive Recursive",
                    "input_size": n,
                    "time_seconds": result[
                        "time_seconds"
                    ],
                    "memory_bytes": result[
                        "memory_bytes"
                    ],
                    "calls": stats["calls"],
                    "max_depth": stats["max_depth"],
                    "speedup": 1.0,
                    "status": "measured",
                }
            )

        else:
            rows.append(
                {
                    "problem": "Fibonacci",
                    "algorithm": "Naive Recursive",
                    "input_size": n,
                    "time_seconds": None,
                    "memory_bytes": None,
                    "calls": (
                        fibonacci_recursive_call_count(n)
                    ),
                    "max_depth": n,
                    "speedup": None,
                    "status": "skipped_exponential",
                }
            )

        memo_stats = {}

        memo_result = measure_function(
            fibonacci_memoized,
            n,
            stats=memo_stats,
        )

        memo_speedup = None

        if naive_time is not None:
            memo_speedup = (
                naive_time
                / memo_result["time_seconds"]
            )

        rows.append(
            {
                "problem": "Fibonacci",
                "algorithm": "Memoized",
                "input_size": n,
                "time_seconds": memo_result[
                    "time_seconds"
                ],
                "memory_bytes": memo_result[
                    "memory_bytes"
                ],
                "calls": memo_stats["calls"],
                "max_depth": memo_stats[
                    "max_depth"
                ],
                "speedup": memo_speedup,
                "status": "measured",
            }
        )

        tab_result = measure_function(
            fibonacci_tabulated,
            n,
        )

        tab_speedup = None

        if naive_time is not None:
            tab_speedup = (
                naive_time
                / tab_result["time_seconds"]
            )

        rows.append(
            {
                "problem": "Fibonacci",
                "algorithm": "Tabulated",
                "input_size": n,
                "time_seconds": tab_result[
                    "time_seconds"
                ],
                "memory_bytes": tab_result[
                    "memory_bytes"
                ],
                "calls": 0,
                "max_depth": 0,
                "speedup": tab_speedup,
                "status": "measured",
            }
        )

        print(
            f"Fibonacci n={n} complete."
        )

    return rows


def make_knapsack_items(item_count):
    """Create deterministic knapsack test data."""
    weights = [
        (index % 9) + 1
        for index in range(item_count)
    ]

    values = [
        ((index * 7) % 20) + 5
        for index in range(item_count)
    ]

    capacity = max(
        1,
        sum(weights) // 3,
    )

    return weights, values, capacity


def benchmark_knapsack(
    sizes=None,
    naive_max=15,
):
    """Benchmark recursive and DP Knapsack versions."""
    if sizes is None:
        sizes = KNAPSACK_SIZES

    rows = []

    for item_count in sizes:
        weights, values, capacity = (
            make_knapsack_items(item_count)
        )

        naive_time = None

        if item_count <= naive_max:
            stats = {}

            result = measure_function(
                knapsack_recursive,
                weights,
                values,
                capacity,
                stats=stats,
            )

            naive_time = result["time_seconds"]

            rows.append(
                {
                    "problem": "Knapsack",
                    "algorithm": "Naive Recursive",
                    "input_size": item_count,
                    "time_seconds": result[
                        "time_seconds"
                    ],
                    "memory_bytes": result[
                        "memory_bytes"
                    ],
                    "calls": stats["calls"],
                    "max_depth": stats["max_depth"],
                    "speedup": 1.0,
                    "status": "measured",
                }
            )

        else:
            rows.append(
                {
                    "problem": "Knapsack",
                    "algorithm": "Naive Recursive",
                    "input_size": item_count,
                    "time_seconds": None,
                    "memory_bytes": None,
                    "calls": None,
                    "max_depth": None,
                    "speedup": None,
                    "status": "skipped_exponential",
                }
            )

        memo_stats = {}

        memo_result = measure_function(
            knapsack_memoized,
            weights,
            values,
            capacity,
            stats=memo_stats,
        )

        memo_speedup = None

        if naive_time is not None:
            memo_speedup = (
                naive_time
                / memo_result["time_seconds"]
            )

        rows.append(
            {
                "problem": "Knapsack",
                "algorithm": "Memoized",
                "input_size": item_count,
                "time_seconds": memo_result[
                    "time_seconds"
                ],
                "memory_bytes": memo_result[
                    "memory_bytes"
                ],
                "calls": memo_stats["calls"],
                "max_depth": memo_stats[
                    "max_depth"
                ],
                "speedup": memo_speedup,
                "status": "measured",
            }
        )

        tab_result = measure_function(
            knapsack_tabulated,
            weights,
            values,
            capacity,
        )

        tab_speedup = None

        if naive_time is not None:
            tab_speedup = (
                naive_time
                / tab_result["time_seconds"]
            )

        rows.append(
            {
                "problem": "Knapsack",
                "algorithm": "Tabulated",
                "input_size": item_count,
                "time_seconds": tab_result[
                    "time_seconds"
                ],
                "memory_bytes": tab_result[
                    "memory_bytes"
                ],
                "calls": 0,
                "max_depth": 0,
                "speedup": tab_speedup,
                "status": "measured",
            }
        )

        print(
            f"Knapsack items={item_count} complete."
        )

    return rows


def make_lcs_strings(length):
    """Create deterministic strings for LCS benchmarks."""
    random_generator = random.Random(
        42 + length
    )

    alphabet = "ABCD"

    x = "".join(
        random_generator.choice(alphabet)
        for _ in range(length)
    )

    y = "".join(
        random_generator.choice(alphabet)
        for _ in range(length)
    )

    return x, y


def benchmark_lcs(
    sizes=None,
    naive_max=10,
):
    """Benchmark recursive and DP LCS versions."""
    if sizes is None:
        sizes = LCS_SIZES

    rows = []

    old_limit = sys.getrecursionlimit()

    if old_limit < 5000:
        sys.setrecursionlimit(5000)

    try:
        for length in sizes:
            x, y = make_lcs_strings(length)

            naive_time = None

            if length <= naive_max:
                stats = {}

                result = measure_function(
                    lcs_recursive,
                    x,
                    y,
                    stats=stats,
                )

                naive_time = result[
                    "time_seconds"
                ]

                rows.append(
                    {
                        "problem": "LCS",
                        "algorithm": "Naive Recursive",
                        "input_size": length,
                        "time_seconds": result[
                            "time_seconds"
                        ],
                        "memory_bytes": result[
                            "memory_bytes"
                        ],
                        "calls": stats["calls"],
                        "max_depth": stats[
                            "max_depth"
                        ],
                        "speedup": 1.0,
                        "status": "measured",
                    }
                )

            else:
                rows.append(
                    {
                        "problem": "LCS",
                        "algorithm": "Naive Recursive",
                        "input_size": length,
                        "time_seconds": None,
                        "memory_bytes": None,
                        "calls": None,
                        "max_depth": None,
                        "speedup": None,
                        "status": (
                            "skipped_exponential"
                        ),
                    }
                )

            memo_stats = {}

            memo_result = measure_function(
                lcs_memoized,
                x,
                y,
                stats=memo_stats,
            )

            memo_speedup = None

            if naive_time is not None:
                memo_speedup = (
                    naive_time
                    / memo_result[
                        "time_seconds"
                    ]
                )

            rows.append(
                {
                    "problem": "LCS",
                    "algorithm": "Memoized",
                    "input_size": length,
                    "time_seconds": memo_result[
                        "time_seconds"
                    ],
                    "memory_bytes": memo_result[
                        "memory_bytes"
                    ],
                    "calls": memo_stats["calls"],
                    "max_depth": memo_stats[
                        "max_depth"
                    ],
                    "speedup": memo_speedup,
                    "status": "measured",
                }
            )

            tab_result = measure_function(
                lcs_tabulated,
                x,
                y,
            )

            tab_speedup = None

            if naive_time is not None:
                tab_speedup = (
                    naive_time
                    / tab_result[
                        "time_seconds"
                    ]
                )

            rows.append(
                {
                    "problem": "LCS",
                    "algorithm": "Tabulated",
                    "input_size": length,
                    "time_seconds": tab_result[
                        "time_seconds"
                    ],
                    "memory_bytes": tab_result[
                        "memory_bytes"
                    ],
                    "calls": 0,
                    "max_depth": 0,
                    "speedup": tab_speedup,
                    "status": "measured",
                }
            )

            print(
                f"LCS length={length} complete."
            )

    finally:
        sys.setrecursionlimit(old_limit)

    return rows


def plot_problem(
    dataframe,
    problem,
    filename,
):
    """
    Plot runtime, recursive calls, and speedup.

    Runtime and calls use logarithmic scales.
    """
    subset = dataframe[
        dataframe["problem"] == problem
    ]

    algorithms = [
        "Naive Recursive",
        "Memoized",
        "Tabulated",
    ]

    figure, axes = plt.subplots(
        1,
        3,
        figsize=(16, 5),
    )

    for algorithm in algorithms:
        data = subset[
            subset["algorithm"] == algorithm
        ].sort_values("input_size")

        measured = data[
            data["time_seconds"].notna()
        ]

        axes[0].plot(
            measured["input_size"],
            measured["time_seconds"],
            marker="o",
            label=algorithm,
        )

        call_data = data[
            data["calls"].notna()
        ]

        axes[1].plot(
            call_data["input_size"],
            call_data["calls"],
            marker="o",
            label=algorithm,
        )

        speedup_data = data[
            data["speedup"].notna()
        ]

        if algorithm != "Naive Recursive":
            axes[2].plot(
                speedup_data["input_size"],
                speedup_data["speedup"],
                marker="o",
                label=algorithm,
            )

    axes[0].set_title(
        f"{problem} Runtime"
    )
    axes[0].set_xlabel("Input Size")
    axes[0].set_ylabel("Time (seconds)")
    axes[0].set_yscale("log")
    axes[0].grid(True)

    axes[1].set_title(
        f"{problem} Calls"
    )
    axes[1].set_xlabel("Input Size")
    axes[1].set_ylabel("Calls")
    axes[1].set_yscale("log")
    axes[1].grid(True)

    axes[2].set_title(
        f"{problem} DP Speedup"
    )
    axes[2].set_xlabel("Input Size")
    axes[2].set_ylabel(
        "Recursive Time / DP Time"
    )
    axes[2].grid(True)

    for axis in axes:
        axis.legend()

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR / filename,
        bbox_inches="tight",
    )

    plt.close(figure)


def print_summary(dataframe):
    """Print a concise benchmark summary table."""
    display = dataframe[
        [
            "problem",
            "algorithm",
            "input_size",
            "time_seconds",
            "memory_bytes",
            "calls",
            "max_depth",
            "speedup",
            "status",
        ]
    ]

    print()
    print(display.to_string(index=False))


def main():
    """Run the complete Week 5 benchmark."""
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "Running Week 5 dynamic programming benchmarks..."
    )
    print()

    rows = []

    rows.extend(
        benchmark_fibonacci()
    )

    rows.extend(
        benchmark_knapsack()
    )

    rows.extend(
        benchmark_lcs()
    )

    dataframe = pd.DataFrame(rows)

    dataframe.to_csv(
        RESULTS_DIR
        / "dp_vs_recursive_table.csv",
        index=False,
    )

    plot_problem(
        dataframe,
        "Fibonacci",
        "fibonacci_comparison.png",
    )

    plot_problem(
        dataframe,
        "Knapsack",
        "knapsack_performance.png",
    )

    plot_problem(
        dataframe,
        "LCS",
        "lcs_performance.png",
    )

    print_summary(dataframe)

    print()
    print("Week 5 benchmark complete.")
    print("Results saved to:")
    print(RESULTS_DIR)


if __name__ == "__main__":
    main()