"""
Complete Week 1 demonstration: From theory to practice.

This script demonstrates:
1. Algorithm correctness
2. Performance benchmarking
3. Empirical complexity analysis
4. Performance visualization
5. Best-case and worst-case behavior
"""

import os
import sys
import time

# Allow this script to import modules from the project root.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.sorting.basic_sorts import (
    bubble_sort,
    selection_sort,
    insertion_sort,
)

from src.utils.benchmark import AlgorithmBenchmark


def demonstrate_correctness():
    """Demonstrate that all three sorting algorithms work correctly."""

    print("\nCORRECTNESS DEMONSTRATION")
    print("=" * 60)

    test_cases = {
        "Empty array": [],
        "Single element": [42],
        "Already sorted": [1, 2, 3, 4, 5],
        "Reverse sorted": [5, 4, 3, 2, 1],
        "Random order": [3, 1, 4, 1, 5, 9, 2, 6],
        "All same": [7, 7, 7, 7],
        "Negative numbers": [-3, -1, -4, -1, -5],
        "Mixed positive/negative": [3, -1, 4, 0, -2],
    }

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
    }

    all_passed = True

    for test_name, test_array in test_cases.items():
        print(f"\nTest case: {test_name}")
        print(f"  Input:    {test_array}")

        expected = sorted(test_array)

        print(f"  Expected: {expected}")

        for algorithm_name, algorithm in algorithms.items():
            try:
                original = test_array.copy()

                result = algorithm(original)

                # Verify both sorting correctness and preservation
                # of the original input list.
                correct = (
                    result == expected
                    and original == test_array
                )

                if correct:
                    status = "PASS"
                else:
                    status = "FAIL"
                    all_passed = False

                print(
                    f"  {algorithm_name:15}: "
                    f"{result} [{status}]"
                )

            except Exception as error:
                print(
                    f"  {algorithm_name:15}: "
                    f"ERROR - {error}"
                )

                all_passed = False

    print("\n" + "-" * 60)

    if all_passed:
        print("Overall result: All correctness demonstrations passed!")
    else:
        print("Overall result: Some correctness demonstrations failed.")

    return all_passed


def demonstrate_efficiency():
    """
    Benchmark the sorting algorithms and perform
    empirical complexity analysis.
    """

    print("\n\nEFFICIENCY DEMONSTRATION")
    print("=" * 60)

    algorithms = {
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
    }

    sizes = [50, 100, 200, 500]

    data_types = [
        "random",
        "sorted",
        "reverse",
    ]

    # Extra precision helps when measuring very fast sorted cases.
    benchmark = AlgorithmBenchmark(
        warmup_runs=2,
        precision=9,
    )

    for data_type in data_types:
        print(
            f"\nBenchmarking {data_type.upper()} data"
        )
        print("-" * 60)

        results = benchmark.benchmark_suite(
            algorithms=algorithms,
            sizes=sizes,
            data_types=[data_type],
            runs=3,
            seed=42,
        )

        print(
            f"\nComplexity analysis for "
            f"{data_type} data:"
        )

        for algorithm_name, result_list in results.items():

            analysis = benchmark.analyze_complexity(
                result_list,
                algorithm_name,
            )

            if "error" in analysis:
                print(
                    f"  {algorithm_name}: "
                    f"{analysis['error']}"
                )

                continue

            print(
                f"\n  {algorithm_name}"
            )

            print(
                f"    Best empirical fit: "
                f"{analysis['best_fit_complexity']}"
            )

            print(
                f"    R-squared: "
                f"{analysis['best_fit_r_squared']:.3f}"
            )

            print(
                f"    {analysis['interpretation']}"
            )

        # Save a chart for this data type.
        chart_path = (
            f"results/demo_{data_type}_performance.png"
        )

        benchmark.plot_comparison(
            results=results,
            filename=chart_path,
            title="Week 1 Sorting Performance",
            data_type=data_type,
            log_scale=False,
            show_plot=False,
        )

        print(
            f"\nVisualization saved to {chart_path}"
        )


def demonstrate_best_vs_worst_case():
    """
    Compare insertion sort on sorted, random,
    and reverse-sorted data.
    """

    print("\n\nBEST VS WORST CASE ANALYSIS")
    print("=" * 60)

    size = 500

    benchmark = AlgorithmBenchmark(
        warmup_runs=0,
        precision=9,
    )

    test_cases = {
        "Best case (sorted)":
            list(range(size)),

        "Average case (random)":
            benchmark.generate_test_data(
                size,
                "random",
                seed=42,
            ),

        "Worst case (reverse)":
            list(range(size, 0, -1)),
    }

    print(
        f"Testing insertion sort with "
        f"{size} elements:\n"
    )

    times = {}

    for case_name, test_data in test_cases.items():

        start_time = time.perf_counter()

        result = insertion_sort(test_data)

        end_time = time.perf_counter()

        elapsed = end_time - start_time

        times[case_name] = elapsed

        # Additional correctness verification.
        assert result == sorted(test_data)

        print(
            f"  {case_name:22}: "
            f"{elapsed:.9f} seconds"
        )

    best_time = times["Best case (sorted)"]
    average_time = times["Average case (random)"]
    worst_time = times["Worst case (reverse)"]

    print("\nPerformance ratios:")

    if best_time > 0:
        print(
            f"  Worst / Best:   "
            f"{worst_time / best_time:.1f}x"
        )

        print(
            f"  Average / Best: "
            f"{average_time / best_time:.1f}x"
        )

    if average_time > 0:
        print(
            f"  Worst / Average: "
            f"{worst_time / average_time:.1f}x"
        )

    print(
        "\nThis demonstrates that insertion sort's "
        "performance depends strongly on how ordered "
        "the input already is."
    )


def main():
    """Run the complete Week 1 algorithm laboratory demonstration."""

    print("=" * 60)
    print("ADVANCED ALGORITHMS - WEEK 1 COMPLETE DEMONSTRATION")
    print("=" * 60)

    print(
        "\nThis demonstration covers:"
    )

    print(
        "- Algorithm correctness verification"
    )

    print(
        "- Original-input preservation"
    )

    print(
        "- Performance benchmarking"
    )

    print(
        "- Empirical complexity analysis"
    )

    print(
        "- Performance visualization"
    )

    print(
        "- Best-case and worst-case behavior"
    )

    try:
        correctness_passed = demonstrate_correctness()

        if correctness_passed:
            demonstrate_efficiency()
            demonstrate_best_vs_worst_case()

        else:
            print(
                "\nPerformance demonstrations were skipped "
                "because correctness verification failed."
            )

        print("\n\n" + "=" * 60)
        print("DEMONSTRATION COMPLETE")
        print("=" * 60)

        print("\nKey Week 1 takeaways:")

        print(
            "- Algorithm correctness should be verified systematically."
        )

        print(
            "- Input size affects algorithm execution time."
        )

        print(
            "- Input organization can significantly affect performance."
        )

        print(
            "- Big-O analysis predicts general scaling behavior."
        )

        print(
            "- Empirical measurements help validate theoretical analysis."
        )

        print(
            "- Testing, benchmarking, and visualization work together."
        )

    except KeyboardInterrupt:
        print(
            "\nDemonstration interrupted by user."
        )

    except Exception as error:
        print(
            f"\nError during demonstration: {error}"
        )

        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()