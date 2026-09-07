"""
Week 2 performance comparison.

Compares:
- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- QuickSort

across six input types and the required input sizes.
"""

import argparse
import math
import random
import statistics
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# Allow imports from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
)


RESULTS_DIR = PROJECT_ROOT / "benchmarks" / "results"


ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "QuickSort": quick_sort,
}


FULL_SIZES = [
    100,
    500,
    1000,
    5000,
    10000,
    50000,
]


QUICK_SIZES = [
    100,
    500,
    1000,
]


DATA_TYPES = [
    "random",
    "sorted",
    "reverse",
    "nearly_sorted",
    "many_duplicates",
    "few_unique",
]


PLOT_NAMES = {
    "random": "random_data.png",
    "sorted": "sorted_data.png",
    "reverse": "reverse_data.png",
    "nearly_sorted": "nearly_sorted.png",
    "many_duplicates": "many_duplicates.png",
    "few_unique": "few_unique.png",
}


def generate_data(
    size: int,
    data_type: str,
    seed: int = 42,
) -> list[int]:
    """
    Generate test data for one benchmark condition.

    Args:
        size: Number of elements.
        data_type: Type of input data to generate.
        seed: Random seed for repeatable results.

    Returns:
        A generated list of integers.
    """
    rng = random.Random(seed)

    if data_type == "random":
        return [
            rng.randint(0, size * 10)
            for _ in range(size)
        ]

    if data_type == "sorted":
        return list(range(size))

    if data_type == "reverse":
        return list(range(size, 0, -1))

    if data_type == "nearly_sorted":
        data = list(range(size))

        # Each swap changes two positions. Swapping about 2.5%
        # of the list leaves approximately 95% in its original
        # sorted position.
        swap_count = max(1, int(size * 0.025))

        for _ in range(swap_count):
            first = rng.randrange(size)
            second = rng.randrange(size)

            data[first], data[second] = (
                data[second],
                data[first],
            )

        return data

    if data_type == "many_duplicates":
        # Only 10 possible values.
        return [
            rng.randint(0, 9)
            for _ in range(size)
        ]

    if data_type == "few_unique":
        # Only 3 possible values.
        return [
            rng.randint(0, 2)
            for _ in range(size)
        ]

    raise ValueError(
        f"Unsupported data type: {data_type}"
    )


def choose_runs(size: int) -> int:
    """
    Choose the number of timed runs.

    Small tests are repeated more often for a stable average.
    Large quadratic tests use fewer repetitions because they
    take much longer.
    """
    if size <= 1000:
        return 5

    if size <= 5000:
        return 3

    return 1


def benchmark_algorithm(
    algorithm,
    data: list[int],
    runs: int,
    seed: int,
) -> dict:
    """
    Time a sorting algorithm and verify its result.
    """
    expected = sorted(data)
    times = []

    # Warm up on smaller data only.
    if len(data) <= 1000:
        random.seed(seed)
        warmup_result = algorithm(data.copy())

        if warmup_result != expected:
            raise ValueError(
                "Algorithm failed correctness check "
                "during warm-up."
            )

    for run_number in range(runs):
        test_data = data.copy()

        # Makes randomized QuickSort testing repeatable.
        random.seed(seed + run_number)

        start = time.perf_counter()

        result = algorithm(test_data)

        elapsed = time.perf_counter() - start

        if result != expected:
            raise ValueError(
                "Algorithm returned an incorrect result."
            )

        times.append(elapsed)

    return {
        "average_time": statistics.mean(times),
        "min_time": min(times),
        "max_time": max(times),
        "runs": runs,
    }


def run_benchmarks(
    sizes: list[int],
) -> pd.DataFrame:
    """
    Run all algorithms on all requested test conditions.
    """
    records = []

    total_tests = (
        len(DATA_TYPES)
        * len(sizes)
        * len(ALGORITHMS)
    )

    test_number = 0

    for data_type in DATA_TYPES:
        print()
        print("=" * 70)
        print(f"DATA TYPE: {data_type.upper()}")
        print("=" * 70)

        for size in sizes:
            data = generate_data(
                size,
                data_type,
                seed=42,
            )

            runs = choose_runs(size)

            for algorithm_name, algorithm in ALGORITHMS.items():
                test_number += 1

                print(
                    f"[{test_number}/{total_tests}] "
                    f"{algorithm_name:<15} "
                    f"{data_type:<16} "
                    f"n={size:<6} "
                    f"runs={runs}",
                    end=" ... ",
                    flush=True,
                )

                result = benchmark_algorithm(
                    algorithm,
                    data,
                    runs,
                    seed=42,
                )

                print(
                    f"{result['average_time']:.9f} s"
                )

                records.append(
                    {
                        "data_type": data_type,
                        "input_size": size,
                        "algorithm": algorithm_name,
                        "average_time": result[
                            "average_time"
                        ],
                        "min_time": result["min_time"],
                        "max_time": result["max_time"],
                        "runs": result["runs"],
                    }
                )

    return pd.DataFrame(records)


def create_comparison_table(
    results: pd.DataFrame,
    output_dir: Path,
) -> None:
    """
    Create a wide CSV comparison table.
    """
    comparison = results.pivot_table(
        index=[
            "data_type",
            "input_size",
        ],
        columns="algorithm",
        values="average_time",
    )

    comparison = comparison.reset_index()

    comparison.to_csv(
        output_dir / "comparison_table.csv",
        index=False,
    )


def create_plots(
    results: pd.DataFrame,
    output_dir: Path,
) -> None:
    """
    Generate one performance plot for each data type.
    """
    for data_type in DATA_TYPES:
        subset = results[
            results["data_type"] == data_type
        ]

        fig, ax = plt.subplots(
            figsize=(10, 6)
        )

        for algorithm_name in ALGORITHMS:
            algorithm_data = subset[
                subset["algorithm"]
                == algorithm_name
            ].sort_values(
                "input_size"
            )

            ax.plot(
                algorithm_data["input_size"],
                algorithm_data["average_time"],
                marker="o",
                label=algorithm_name,
            )

        readable_title = (
            data_type
            .replace("_", " ")
            .title()
        )

        ax.set_title(
            f"Sorting Performance - {readable_title}"
        )

        ax.set_xlabel("Input Size (n)")
        ax.set_ylabel(
            "Average Execution Time (seconds)"
        )

        # Log scales make both O(n^2) and O(n log n)
        # algorithms visible on the same graph.
        ax.set_xscale("log")
        ax.set_yscale("log")

        ax.grid(
            True,
            alpha=0.3,
        )

        ax.legend()

        fig.tight_layout()

        output_path = (
            output_dir
            / PLOT_NAMES[data_type]
        )

        fig.savefig(
            output_path,
            dpi=200,
        )

        plt.close(fig)

        print(
            f"Saved plot: {output_path.name}"
        )


def calculate_r_squared(
    actual: list[float],
    predicted: list[float],
) -> float:
    """
    Calculate R-squared for a fitted model.
    """
    mean_actual = statistics.mean(actual)

    total = sum(
        (value - mean_actual) ** 2
        for value in actual
    )

    residual = sum(
        (actual_value - predicted_value) ** 2
        for actual_value, predicted_value
        in zip(actual, predicted)
    )

    if total == 0:
        return 1.0

    return 1 - residual / total


def fit_model(
    sizes: list[int],
    times: list[float],
    model_name: str,
) -> float:
    """
    Fit timing results to a basic complexity model.
    """
    if model_name == "O(n)":
        model_values = [
            float(n)
            for n in sizes
        ]

    elif model_name == "O(n log n)":
        model_values = [
            n * math.log2(max(n, 2))
            for n in sizes
        ]

    elif model_name == "O(n^2)":
        model_values = [
            float(n * n)
            for n in sizes
        ]

    else:
        raise ValueError(
            f"Unknown model: {model_name}"
        )

    numerator = sum(
        x * y
        for x, y in zip(
            model_values,
            times,
        )
    )

    denominator = sum(
        x * x
        for x in model_values
    )

    scale = numerator / denominator

    predicted = [
        scale * value
        for value in model_values
    ]

    return calculate_r_squared(
        times,
        predicted,
    )


def doubling_ratio(
    subset: pd.DataFrame,
    first_size: int,
    second_size: int,
):
    """
    Calculate a timing ratio for two input sizes.
    """
    first = subset[
        subset["input_size"]
        == first_size
    ]

    second = subset[
        subset["input_size"]
        == second_size
    ]

    if first.empty or second.empty:
        return None

    first_time = float(
        first.iloc[0]["average_time"]
    )

    second_time = float(
        second.iloc[0]["average_time"]
    )

    if first_time == 0:
        return None

    return second_time / first_time


def create_complexity_validation(
    results: pd.DataFrame,
    output_dir: Path,
) -> None:
    """
    Compare measured performance with common complexity models.
    """
    records = []

    models = [
        "O(n)",
        "O(n log n)",
        "O(n^2)",
    ]

    for data_type in DATA_TYPES:
        for algorithm_name in ALGORITHMS:
            subset = results[
                (
                    results["data_type"]
                    == data_type
                )
                & (
                    results["algorithm"]
                    == algorithm_name
                )
            ].sort_values(
                "input_size"
            )

            sizes = (
                subset["input_size"]
                .astype(int)
                .tolist()
            )

            times = (
                subset["average_time"]
                .astype(float)
                .tolist()
            )

            scores = {
                model: fit_model(
                    sizes,
                    times,
                    model,
                )
                for model in models
            }

            best_model = max(
                scores,
                key=scores.get,
            )

            records.append(
                {
                    "data_type": data_type,
                    "algorithm": algorithm_name,
                    "best_empirical_fit": best_model,
                    "r_squared": scores[
                        best_model
                    ],
                    "ratio_500_to_1000":
                        doubling_ratio(
                            subset,
                            500,
                            1000,
                        ),
                    "ratio_5000_to_10000":
                        doubling_ratio(
                            subset,
                            5000,
                            10000,
                        ),
                }
            )

    complexity_df = pd.DataFrame(
        records
    )

    complexity_df.to_csv(
        output_dir
        / "complexity_validation.csv",
        index=False,
    )

    print()
    print("EMPIRICAL COMPLEXITY SUMMARY")
    print("-" * 70)

    print(
        complexity_df.to_string(
            index=False
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Week 2 sorting performance benchmark"
        )
    )

    parser.add_argument(
        "--quick",
        action="store_true",
        help=(
            "Run only sizes 100, 500, and 1000 "
            "as a short validation test."
        ),
    )

    args = parser.parse_args()

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if args.quick:
        sizes = QUICK_SIZES

        print(
            "QUICK VALIDATION MODE"
        )
    else:
        sizes = FULL_SIZES

        print(
            "FULL WEEK 2 BENCHMARK"
        )

    print(
        f"Input sizes: {sizes}"
    )

    print(
        f"Data types: {len(DATA_TYPES)}"
    )

    print(
        f"Algorithms: {len(ALGORITHMS)}"
    )

    start_time = time.perf_counter()

    results = run_benchmarks(
        sizes
    )

    results.to_csv(
        RESULTS_DIR
        / "week2_benchmark_results.csv",
        index=False,
    )

    create_comparison_table(
        results,
        RESULTS_DIR,
    )

    create_plots(
        results,
        RESULTS_DIR,
    )

    create_complexity_validation(
        results,
        RESULTS_DIR,
    )

    elapsed = (
        time.perf_counter()
        - start_time
    )

    print()
    print("=" * 70)
    print("BENCHMARK COMPLETE")
    print("=" * 70)

    print(
        f"Total time: "
        f"{elapsed / 60:.2f} minutes"
    )

    print(
        f"Results saved to: "
        f"{RESULTS_DIR}"
    )


if __name__ == "__main__":
    main()