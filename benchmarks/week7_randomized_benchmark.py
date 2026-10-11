"""Week 7 randomized algorithms benchmark."""

import math
import statistics
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.randomized.bloom_filter import BloomFilter
from src.randomized.minhash_similarity import (
    estimate_minhash_similarity,
    jaccard_similarity,
)
from src.randomized.montecarlo_primality import (
    deterministic_is_prime,
    fermat_primality_test,
    miller_rabin_primality_test,
)
from src.randomized.randomized_quicksort import (
    deterministic_quicksort,
    randomized_quicksort,
)
from src.randomized.randomized_selection import (
    deterministic_select,
    randomized_select,
)
from src.utils.probability_analysis import (
    bloom_false_positive_probability,
    miller_rabin_error_bound,
)
from src.utils.random_utils import (
    make_minhash_sets,
    shuffled_range,
)


RESULTS_DIR = PROJECT_ROOT / "benchmarks" / "results"

QUICKSORT_SIZES = [
    100,
    1000,
    10000,
    100000,
]

SELECTION_SIZES = [
    100,
    1000,
    10000,
    100000,
]

PRIMALITY_ITERATIONS = [
    5,
    10,
    20,
]

BLOOM_INSERT_COUNTS = [
    250,
    500,
    1000,
    1500,
    2000,
]

MINHASH_SIZES = [
    16,
    32,
    64,
    128,
    256,
    512,
]


def elapsed_time(
    function,
    *args,
    **kwargs,
):
    """Return function result and elapsed seconds."""
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


def expected_quicksort_comparisons(
    size,
):
    """
    Expected comparison count for classic randomized QuickSort.

    Assumes distinct values.
    """
    harmonic = sum(
        1.0 / value
        for value in range(
            1,
            size + 1,
        )
    )

    return (
        2
        * (size + 1)
        * harmonic
        - 4 * size
    )


def benchmark_quicksort(
    sizes=None,
    trials=5,
):
    """Benchmark randomized and deterministic QuickSort."""
    if sizes is None:
        sizes = QUICKSORT_SIZES

    rows = []

    for size in sizes:
        source = shuffled_range(
            size,
            seed=42 + size,
        )

        randomized_times = []
        randomized_comparisons = []
        randomized_depths = []

        for trial in range(trials):
            stats = {}

            result, runtime = elapsed_time(
                randomized_quicksort,
                source,
                seed=100 + trial,
                stats=stats,
            )

            if result != sorted(source):
                raise RuntimeError(
                    "Randomized QuickSort produced "
                    "an incorrect result"
                )

            randomized_times.append(
                runtime
            )

            randomized_comparisons.append(
                stats["comparisons"]
            )

            randomized_depths.append(
                stats["max_depth"]
            )

        deterministic_times = []
        deterministic_comparisons = []
        deterministic_depths = []

        for _ in range(trials):
            stats = {}

            result, runtime = elapsed_time(
                deterministic_quicksort,
                source,
                stats=stats,
            )

            if result != sorted(source):
                raise RuntimeError(
                    "Deterministic QuickSort produced "
                    "an incorrect result"
                )

            deterministic_times.append(
                runtime
            )

            deterministic_comparisons.append(
                stats["comparisons"]
            )

            deterministic_depths.append(
                stats["max_depth"]
            )

        randomized_mean = statistics.mean(
            randomized_times
        )

        deterministic_mean = statistics.mean(
            deterministic_times
        )

        rows.append(
            {
                "problem": "QuickSort",
                "algorithm": "Randomized QuickSort",
                "input_size": size,
                "mean_time_seconds": randomized_mean,
                "runtime_variance": statistics.pvariance(
                    randomized_times
                ),
                "comparisons": statistics.mean(
                    randomized_comparisons
                ),
                "expected_comparisons": (
                    expected_quicksort_comparisons(
                        size
                    )
                ),
                "average_depth": statistics.mean(
                    randomized_depths
                ),
                "accuracy": 1.0,
                "error_rate": 0.0,
                "theoretical_error": None,
            }
        )

        rows.append(
            {
                "problem": "QuickSort",
                "algorithm": "Deterministic QuickSort",
                "input_size": size,
                "mean_time_seconds": deterministic_mean,
                "runtime_variance": statistics.pvariance(
                    deterministic_times
                ),
                "comparisons": statistics.mean(
                    deterministic_comparisons
                ),
                "expected_comparisons": None,
                "average_depth": statistics.mean(
                    deterministic_depths
                ),
                "accuracy": 1.0,
                "error_rate": 0.0,
                "theoretical_error": None,
            }
        )

        print(
            f"QuickSort size {size} complete."
        )

    return rows


def benchmark_selection(
    sizes=None,
    trials=5,
):
    """Benchmark randomized and deterministic selection."""
    if sizes is None:
        sizes = SELECTION_SIZES

    rows = []

    for size in sizes:
        source = shuffled_range(
            size,
            seed=200 + size,
        )

        positions = {
            "Minimum": 1,
            "Median": (
                size + 1
            ) // 2,
            "Maximum": size,
        }

        sorted_source = sorted(
            source
        )

        for label, k in positions.items():
            randomized_times = []
            randomized_depths = []
            successes = 0

            expected_value = (
                sorted_source[k - 1]
            )

            for trial in range(trials):
                stats = {}

                result, runtime = elapsed_time(
                    randomized_select,
                    source,
                    k,
                    seed=300 + trial,
                    stats=stats,
                )

                randomized_times.append(
                    runtime
                )

                randomized_depths.append(
                    stats["max_depth"]
                )

                if result == expected_value:
                    successes += 1

            deterministic_stats = {}

            (
                deterministic_result,
                deterministic_runtime,
            ) = elapsed_time(
                deterministic_select,
                source,
                k,
                stats=deterministic_stats,
            )

            if deterministic_result != expected_value:
                raise RuntimeError(
                    "Deterministic selection produced "
                    "an incorrect result"
                )

            rows.append(
                {
                    "problem": "Selection",
                    "algorithm": (
                        f"Randomized {label}"
                    ),
                    "input_size": size,
                    "mean_time_seconds": statistics.mean(
                        randomized_times
                    ),
                    "runtime_variance": statistics.pvariance(
                        randomized_times
                    ),
                    "comparisons": None,
                    "expected_comparisons": None,
                    "average_depth": statistics.mean(
                        randomized_depths
                    ),
                    "accuracy": (
                        successes / trials
                    ),
                    "error_rate": (
                        1 - successes / trials
                    ),
                    "theoretical_error": 0.0,
                }
            )

            rows.append(
                {
                    "problem": "Selection",
                    "algorithm": (
                        f"Deterministic {label}"
                    ),
                    "input_size": size,
                    "mean_time_seconds": deterministic_runtime,
                    "runtime_variance": 0.0,
                    "comparisons": deterministic_stats[
                        "comparisons"
                    ],
                    "expected_comparisons": None,
                    "average_depth": deterministic_stats[
                        "max_depth"
                    ],
                    "accuracy": 1.0,
                    "error_rate": 0.0,
                    "theoretical_error": 0.0,
                }
            )

        print(
            f"Selection size {size} complete."
        )

    return rows


def primality_test_values():
    """
    Return numbers with deterministic truth labels.

    Includes primes, ordinary composites, and Carmichael numbers.
    """
    return [
        97,
        101,
        104729,
        1000003,
        221,
        1001,
        1000005,
        561,
        1105,
        1729,
        2465,
        2821,
        6601,
    ]


def benchmark_primality(
    iteration_counts=None,
    trials=10,
):
    """Benchmark deterministic and Monte Carlo primality tests."""
    if iteration_counts is None:
        iteration_counts = PRIMALITY_ITERATIONS

    values = primality_test_values()

    truth = {
        number: deterministic_is_prime(
            number
        )
        for number in values
    }

    rows = []

    large_number = 1000003

    _, deterministic_runtime = elapsed_time(
        deterministic_is_prime,
        large_number,
    )

    rows.append(
        {
            "problem": "Primality",
            "algorithm": "Deterministic Trial Division",
            "input_size": large_number,
            "mean_time_seconds": deterministic_runtime,
            "runtime_variance": 0.0,
            "comparisons": None,
            "expected_comparisons": None,
            "average_depth": None,
            "accuracy": 1.0,
            "error_rate": 0.0,
            "theoretical_error": 0.0,
        }
    )

    for iterations in iteration_counts:
        for name, function in [
            (
                "Fermat",
                fermat_primality_test,
            ),
            (
                "Miller-Rabin",
                miller_rabin_primality_test,
            ),
        ]:
            runtimes = []
            correct = 0
            total = 0

            for trial in range(trials):
                for number in values:
                    result, runtime = elapsed_time(
                        function,
                        number,
                        iterations=iterations,
                        seed=(
                            500
                            + trial
                            + number
                        ),
                    )

                    runtimes.append(
                        runtime
                    )

                    total += 1

                    if result == truth[number]:
                        correct += 1

            accuracy = (
                correct / total
            )

            theoretical_error = None

            if name == "Miller-Rabin":
                theoretical_error = (
                    miller_rabin_error_bound(
                        iterations
                    )
                )

            rows.append(
                {
                    "problem": "Primality",
                    "algorithm": (
                        f"{name} k={iterations}"
                    ),
                    "input_size": iterations,
                    "mean_time_seconds": statistics.mean(
                        runtimes
                    ),
                    "runtime_variance": statistics.pvariance(
                        runtimes
                    ),
                    "comparisons": None,
                    "expected_comparisons": None,
                    "average_depth": None,
                    "accuracy": accuracy,
                    "error_rate": (
                        1 - accuracy
                    ),
                    "theoretical_error": theoretical_error,
                }
            )

        print(
            f"Primality k={iterations} complete."
        )

    return rows


def benchmark_bloom_filter(
    insert_counts=None,
    bit_count=10000,
    hash_count=4,
    query_count=5000,
):
    """Measure empirical and theoretical Bloom filter FP rates."""
    if insert_counts is None:
        insert_counts = BLOOM_INSERT_COUNTS

    rows = []

    for inserted_items in insert_counts:
        bloom = BloomFilter(
            size=bit_count,
            hash_count=hash_count,
        )

        for value in range(
            inserted_items
        ):
            bloom.add(
                f"stored-{value}"
            )

        false_positives = 0

        start = time.perf_counter()

        for value in range(
            query_count
        ):
            if bloom.check(
                f"query-{value}"
            ):
                false_positives += 1

        runtime = (
            time.perf_counter()
            - start
        )

        observed_rate = (
            false_positives
            / query_count
        )

        theoretical_rate = (
            bloom_false_positive_probability(
                bit_count,
                hash_count,
                inserted_items,
            )
        )

        rows.append(
            {
                "problem": "Bloom Filter",
                "algorithm": "Bloom Filter",
                "input_size": inserted_items,
                "mean_time_seconds": runtime,
                "runtime_variance": 0.0,
                "comparisons": None,
                "expected_comparisons": None,
                "average_depth": None,
                "accuracy": (
                    1 - observed_rate
                ),
                "error_rate": observed_rate,
                "theoretical_error": theoretical_rate,
                "load_factor": bloom.load_factor(),
            }
        )

        print(
            "Bloom filter "
            f"{inserted_items} items complete."
        )

    return rows


def benchmark_minhash(
    signature_sizes=None,
    trials=10,
):
    """Compare exact Jaccard similarity with MinHash estimates."""
    if signature_sizes is None:
        signature_sizes = MINHASH_SIZES

    first, second = make_minhash_sets(
        set_size=1000,
        overlap=500,
    )

    exact = jaccard_similarity(
        first,
        second,
    )

    rows = []

    for signature_size in signature_sizes:
        estimates = []
        runtimes = []

        for trial in range(trials):
            estimate, runtime = elapsed_time(
                estimate_minhash_similarity,
                first,
                second,
                signature_size,
                700 + trial,
            )

            estimates.append(
                estimate
            )

            runtimes.append(
                runtime
            )

        mean_estimate = statistics.mean(
            estimates
        )

        error = abs(
            exact - mean_estimate
        )

        rows.append(
            {
                "problem": "MinHash",
                "algorithm": "MinHash",
                "input_size": signature_size,
                "mean_time_seconds": statistics.mean(
                    runtimes
                ),
                "runtime_variance": statistics.pvariance(
                    runtimes
                ),
                "comparisons": None,
                "expected_comparisons": None,
                "average_depth": None,
                "accuracy": (
                    1 - error
                ),
                "error_rate": error,
                "theoretical_error": None,
                "true_similarity": exact,
                "estimated_similarity": mean_estimate,
            }
        )

        print(
            f"MinHash k={signature_size} complete."
        )

    return rows


def plot_quicksort(
    dataframe,
):
    """Plot QuickSort runtime and comparison counts."""
    subset = dataframe[
        dataframe["problem"] == "QuickSort"
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

        axes[0].plot(
            data["input_size"],
            data["mean_time_seconds"],
            marker="o",
            label=algorithm,
        )

        axes[1].plot(
            data["input_size"],
            data["comparisons"],
            marker="o",
            label=algorithm,
        )

    randomized = subset[
        subset["algorithm"]
        == "Randomized QuickSort"
    ].sort_values(
        "input_size"
    )

    axes[1].plot(
        randomized["input_size"],
        randomized["expected_comparisons"],
        marker="o",
        linestyle="--",
        label="Randomized Expected",
    )

    axes[0].set_title(
        "QuickSort Runtime"
    )
    axes[0].set_xlabel(
        "Array Size"
    )
    axes[0].set_ylabel(
        "Mean Time (seconds)"
    )
    axes[0].set_xscale(
        "log"
    )
    axes[0].set_yscale(
        "log"
    )
    axes[0].grid(True)
    axes[0].legend()

    axes[1].set_title(
        "QuickSort Comparisons"
    )
    axes[1].set_xlabel(
        "Array Size"
    )
    axes[1].set_ylabel(
        "Comparisons"
    )
    axes[1].set_xscale(
        "log"
    )
    axes[1].set_yscale(
        "log"
    )
    axes[1].grid(True)
    axes[1].legend()

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "quicksort_comparison.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_selection(
    dataframe,
):
    """Plot randomized selection runtime."""
    subset = dataframe[
        dataframe["problem"] == "Selection"
    ]

    randomized = subset[
        subset["algorithm"].str.startswith(
            "Randomized"
        )
    ]

    figure, axes = plt.subplots(
        1,
        2,
        figsize=(12, 5),
    )

    for algorithm in randomized[
        "algorithm"
    ].unique():
        data = randomized[
            randomized["algorithm"] == algorithm
        ].sort_values(
            "input_size"
        )

        axes[0].plot(
            data["input_size"],
            data["mean_time_seconds"],
            marker="o",
            label=algorithm,
        )

        axes[1].plot(
            data["input_size"],
            data["average_depth"],
            marker="o",
            label=algorithm,
        )

    axes[0].set_title(
        "Randomized Selection Runtime"
    )
    axes[0].set_xlabel(
        "Input Size"
    )
    axes[0].set_ylabel(
        "Mean Time (seconds)"
    )
    axes[0].set_xscale(
        "log"
    )
    axes[0].set_yscale(
        "log"
    )
    axes[0].grid(True)
    axes[0].legend()

    axes[1].set_title(
        "Average Recursion Depth"
    )
    axes[1].set_xlabel(
        "Input Size"
    )
    axes[1].set_ylabel(
        "Depth"
    )
    axes[1].set_xscale(
        "log"
    )
    axes[1].grid(True)
    axes[1].legend()

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "selection_runtime.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_primality(
    dataframe,
):
    """Plot probabilistic primality accuracy."""
    subset = dataframe[
        dataframe["problem"] == "Primality"
    ]

    subset = subset[
        subset["algorithm"]
        != "Deterministic Trial Division"
    ].copy()

    subset["test"] = subset[
        "algorithm"
    ].str.split(
        " k="
    ).str[0]

    figure, axes = plt.subplots(
        1,
        2,
        figsize=(12, 5),
    )

    for test_name in [
        "Fermat",
        "Miller-Rabin",
    ]:
        data = subset[
            subset["test"] == test_name
        ].sort_values(
            "input_size"
        )

        axes[0].plot(
            data["input_size"],
            data["accuracy"],
            marker="o",
            label=test_name,
        )

        axes[1].plot(
            data["input_size"],
            data["error_rate"],
            marker="o",
            label=f"{test_name} Observed",
        )

    miller = subset[
        subset["test"] == "Miller-Rabin"
    ].sort_values(
        "input_size"
    )

    axes[1].plot(
        miller["input_size"],
        miller["theoretical_error"],
        marker="o",
        linestyle="--",
        label="Miller-Rabin Bound",
    )

    axes[0].set_title(
        "Primality Accuracy"
    )
    axes[0].set_xlabel(
        "Iterations (k)"
    )
    axes[0].set_ylabel(
        "Accuracy"
    )
    axes[0].set_ylim(
        0,
        1.05,
    )
    axes[0].grid(True)
    axes[0].legend()

    axes[1].set_title(
        "Primality Error"
    )
    axes[1].set_xlabel(
        "Iterations (k)"
    )
    axes[1].set_ylabel(
        "Error Rate"
    )
    axes[1].set_yscale(
        "log"
    )
    axes[1].grid(True)
    axes[1].legend()

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "primality_accuracy.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_bloom(
    dataframe,
):
    """Plot observed and theoretical Bloom filter FP rates."""
    data = dataframe[
        dataframe["problem"] == "Bloom Filter"
    ].sort_values(
        "input_size"
    )

    figure, axis = plt.subplots(
        figsize=(8, 5),
    )

    axis.plot(
        data["input_size"],
        data["error_rate"],
        marker="o",
        label="Observed FP Rate",
    )

    axis.plot(
        data["input_size"],
        data["theoretical_error"],
        marker="o",
        linestyle="--",
        label="Theoretical FP Rate",
    )

    axis.set_title(
        "Bloom Filter False Positive Rate"
    )
    axis.set_xlabel(
        "Inserted Items"
    )
    axis.set_ylabel(
        "False Positive Rate"
    )
    axis.grid(True)
    axis.legend()

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "bloom_filter_fp_rate.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_minhash(
    dataframe,
):
    """Plot MinHash estimated similarity and error."""
    data = dataframe[
        dataframe["problem"] == "MinHash"
    ].sort_values(
        "input_size"
    )

    figure, axes = plt.subplots(
        1,
        2,
        figsize=(12, 5),
    )

    axes[0].plot(
        data["input_size"],
        data["estimated_similarity"],
        marker="o",
        label="Estimated Similarity",
    )

    axes[0].axhline(
        data["true_similarity"].iloc[0],
        linestyle="--",
        label="True Jaccard",
    )

    axes[1].plot(
        data["input_size"],
        data["error_rate"],
        marker="o",
        label="Absolute Error",
    )

    axes[0].set_title(
        "MinHash Similarity Estimate"
    )
    axes[0].set_xlabel(
        "Number of Hash Functions"
    )
    axes[0].set_ylabel(
        "Similarity"
    )
    axes[0].grid(True)
    axes[0].legend()

    axes[1].set_title(
        "MinHash Estimation Error"
    )
    axes[1].set_xlabel(
        "Number of Hash Functions"
    )
    axes[1].set_ylabel(
        "Absolute Error"
    )
    axes[1].grid(True)
    axes[1].legend()

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "minhash_similarity_plot.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def main():
    """Run the complete Week 7 benchmark."""
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "Running Week 7 randomized algorithm benchmarks..."
    )
    print()

    rows = []

    rows.extend(
        benchmark_quicksort()
    )

    rows.extend(
        benchmark_selection()
    )

    rows.extend(
        benchmark_primality()
    )

    rows.extend(
        benchmark_bloom_filter()
    )

    rows.extend(
        benchmark_minhash()
    )

    dataframe = pd.DataFrame(
        rows
    )

    dataframe.to_csv(
        RESULTS_DIR
        / "summary_table.csv",
        index=False,
    )

    plot_quicksort(
        dataframe
    )

    plot_selection(
        dataframe
    )

    plot_primality(
        dataframe
    )

    plot_bloom(
        dataframe
    )

    plot_minhash(
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
        "Week 7 benchmark complete."
    )

    print(
        "Results saved to:"
    )

    print(
        RESULTS_DIR
    )


if __name__ == "__main__":
    main()