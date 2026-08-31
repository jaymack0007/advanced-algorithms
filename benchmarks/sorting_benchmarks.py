"""Run the final sorting performance experiment."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.sorting.basic_sorts import (
    bubble_sort,
    insertion_sort,
    selection_sort,
)

from src.utils.benchmark import AlgorithmBenchmark


def main():
    """Run the final benchmark suite and generate submission results."""

    benchmark = AlgorithmBenchmark(
        warmup_runs=2,
        precision=9,
    )

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
    }

    sizes = [
        100,
        250,
        500,
        1000,
    ]

    data_types = [
        "random",
        "sorted",
        "reverse",
        "nearly_sorted",
    ]

    results = benchmark.benchmark_suite(
        algorithms=algorithms,
        sizes=sizes,
        data_types=data_types,
        runs=5,
        seed=42,
    )

    benchmark.export_results(
        "results/sorting_results.csv"
    )

    for data_type in data_types:
        benchmark.plot_comparison(
            results=results,
            filename=(
                f"results/"
                f"{data_type}_performance.png"
            ),
            title="Sorting Algorithm Performance",
            data_type=data_type,
            log_scale=False,
            show_plot=False,
        )

    print("\n" + "=" * 60)
    print("EMPIRICAL COMPLEXITY ANALYSIS")
    print("=" * 60)

    for data_type in data_types:
        print(
            f"\nData type: {data_type.upper()}"
        )

        for algorithm_name, result_list in results.items():

            selected_results = [
                result
                for result in result_list
                if result.data_type == data_type
            ]

            analysis = benchmark.analyze_complexity(
                selected_results,
                algorithm_name,
            )

            if "error" in analysis:
                print(
                    f"  {algorithm_name}: "
                    f"{analysis['error']}"
                )
                continue

            print(
                f"  {algorithm_name:16}: "
                f"{analysis['best_fit_complexity']} "
                f"(R^2 = "
                f"{analysis['best_fit_r_squared']:.3f})"
            )

    print("\nCreated:")
    print("  results/sorting_results.csv")

    for data_type in data_types:
        print(
            f"  results/"
            f"{data_type}_performance.png"
        )


if __name__ == "__main__":
    main()