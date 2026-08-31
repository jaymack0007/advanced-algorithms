"""
Professional benchmarking framework for algorithm analysis.

Provides:
- Multiple-run timing with statistical analysis
- Multiple test-data patterns
- Correctness verification
- Complexity analysis
- Performance visualizations
- CSV result export
"""

import csv
import random
import statistics
import time

from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class BenchmarkResult:
    """Container for one summarized benchmark result."""

    algorithm_name: str
    data_type: str
    input_size: int
    average_time: float
    std_deviation: float
    min_time: float
    max_time: float
    memory_usage: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


class AlgorithmBenchmark:
    """
    Professional algorithm benchmarking and analysis toolkit.

    Features:
    - Multiple-run averaging with statistical analysis
    - Warm-up runs
    - Multiple data patterns
    - Sorting correctness verification
    - Empirical complexity analysis
    - Performance visualization
    - CSV export
    """

    def __init__(self, warmup_runs: int = 2, precision: int = 6):
        """
        Initialize the benchmarking framework.

        Args:
            warmup_runs: Number of untimed runs before measurements.
            precision: Number of decimal places stored in timing results.
        """
        if warmup_runs < 0:
            raise ValueError("warmup_runs must be nonnegative")

        if precision < 0:
            raise ValueError("precision must be nonnegative")

        self.warmup_runs = warmup_runs
        self.precision = precision
        self.results: List[BenchmarkResult] = []

    def generate_test_data(
        self,
        size: int,
        data_type: str = "random",
        seed: Optional[int] = None,
    ) -> List[int]:
        """
        Generate various types of data for algorithm testing.

        Args:
            size: Number of elements to generate.
            data_type: Shape or organization of the test data.
            seed: Optional random seed for reproducibility.

        Returns:
            Generated list of integers.

        Raises:
            ValueError: If size is negative or data_type is unsupported.
        """
        if size < 0:
            raise ValueError("size must be nonnegative")

        rng = random.Random(seed)

        if data_type == "random":
            return [rng.randint(1, 1000) for _ in range(size)]

        if data_type == "sorted":
            return list(range(1, size + 1))

        if data_type == "reverse":
            return list(range(size, 0, -1))

        if data_type == "duplicates":
            # max(1, ...) prevents randint(1, 0) for small arrays.
            upper = max(1, size // 10)
            return [rng.randint(1, upper) for _ in range(size)]

        if data_type == "single_value":
            return [42] * size

        if data_type == "nearly_sorted":
            return self._generate_nearly_sorted(size, rng)

        if data_type == "mountain":
            return self._generate_mountain(size)

        if data_type == "valley":
            return self._generate_valley(size)

        raise ValueError(f"Unknown data type: {data_type}")

    def _generate_nearly_sorted(
        self,
        size: int,
        rng: random.Random,
    ) -> List[int]:
        """Generate sorted data with approximately 5% random swaps."""
        arr = list(range(1, size + 1))

        if size < 2:
            return arr

        num_swaps = max(1, size // 20)

        for _ in range(num_swaps):
            i = rng.randrange(size)
            j = rng.randrange(size)
            arr[i], arr[j] = arr[j], arr[i]

        return arr

    def _generate_mountain(self, size: int) -> List[int]:
        """
        Generate mountain-shaped data that increases and then decreases.

        The returned list always contains exactly `size` elements.
        """
        if size == 0:
            return []

        left_size = (size + 1) // 2
        right_size = size - left_size

        left = list(range(1, left_size + 1))
        right = list(range(right_size, 0, -1))

        return left + right

    def _generate_valley(self, size: int) -> List[int]:
        """
        Generate valley-shaped data that decreases and then increases.

        The returned list always contains exactly `size` elements.
        """
        if size == 0:
            return []

        left_size = size // 2
        right_size = size - left_size

        left = list(range(left_size, 0, -1))
        right = list(range(1, right_size + 1))

        return left + right

    def time_algorithm(
        self,
        algorithm: Callable,
        data: List[Any],
        runs: int = 5,
        verify_correctness: bool = True,
        data_type: str = "unknown",
    ) -> BenchmarkResult:
        """
        Time an algorithm over multiple runs.

        Args:
            algorithm: Sorting function to benchmark.
            data: Input list.
            runs: Number of measured runs.
            verify_correctness: Verify that sorting output is correct.
            data_type: Description of the input organization.

        Returns:
            BenchmarkResult containing timing statistics.

        Raises:
            ValueError: If runs is less than one or sorting is incorrect.
        """
        if runs < 1:
            raise ValueError("runs must be at least 1")

        expected = sorted(data)

        # Warm-up runs are not included in timing measurements.
        for _ in range(self.warmup_runs):
            warmup_data = data.copy()
            warmup_result = algorithm(warmup_data)

            if verify_correctness:
                if not self._verify_sorting_correctness(
                    data,
                    warmup_result,
                ):
                    raise ValueError(
                        f"Algorithm {algorithm.__name__} "
                        "produced an incorrect result"
                    )

        times = []

        for run_number in range(runs):
            test_data = data.copy()

            start_time = time.perf_counter()
            result = algorithm(test_data)
            end_time = time.perf_counter()

            times.append(end_time - start_time)

            # Verification on the first measured run is sufficient.
            if verify_correctness and run_number == 0:
                if not self._verify_sorting_correctness(
                    data,
                    result,
                ):
                    raise ValueError(
                        f"Algorithm {algorithm.__name__} "
                        "produced an incorrect result"
                    )

                if result != expected:
                    raise ValueError(
                        f"Algorithm {algorithm.__name__} "
                        "did not match Python's sorted result"
                    )

        avg_time = statistics.mean(times)
        std_time = (
            statistics.stdev(times)
            if len(times) > 1
            else 0.0
        )

        benchmark_result = BenchmarkResult(
            algorithm_name=algorithm.__name__,
            data_type=data_type,
            input_size=len(data),
            average_time=round(avg_time, self.precision),
            std_deviation=round(std_time, self.precision),
            min_time=round(min(times), self.precision),
            max_time=round(max(times), self.precision),
        )

        self.results.append(benchmark_result)

        return benchmark_result

    def _verify_sorting_correctness(
        self,
        original: List[Any],
        result: List[Any],
    ) -> bool:
        """
        Verify that sorting produced ordered output containing
        the same elements as the original list.
        """
        if result is None:
            return False

        if len(original) != len(result):
            return False

        if not all(
            result[i] <= result[i + 1]
            for i in range(len(result) - 1)
        ):
            return False

        return sorted(original) == sorted(result)

    def benchmark_suite(
        self,
        algorithms: Dict[str, Callable],
        sizes: List[int],
        data_types: Optional[List[str]] = None,
        runs: int = 5,
        seed: int = 42,
    ) -> Dict[str, List[BenchmarkResult]]:
        """
        Run benchmarks across multiple algorithms, sizes, and data types.

        Args:
            algorithms: Dictionary mapping display names to functions.
            sizes: Input sizes to benchmark.
            data_types: Input organizations to benchmark.
            runs: Number of measured runs per test.
            seed: Seed used to reproduce generated data.

        Returns:
            Dictionary mapping algorithm display names to results.
        """
        if data_types is None:
            data_types = ["random"]

        all_results = defaultdict(list)

        total_tests = (
            len(algorithms)
            * len(sizes)
            * len(data_types)
        )

        current_test = 0

        print(f"Running {total_tests} benchmark tests...")
        print("-" * 60)

        for data_type in data_types:
            print(f"\nData type: {data_type}")

            for size in sizes:
                test_data = self.generate_test_data(
                    size,
                    data_type,
                    seed=seed,
                )

                for name, algorithm in algorithms.items():
                    current_test += 1

                    try:
                        result = self.time_algorithm(
                            algorithm=algorithm,
                            data=test_data,
                            runs=runs,
                            verify_correctness=True,
                            data_type=data_type,
                        )

                        all_results[name].append(result)

                        progress = (
                            current_test / total_tests * 100
                        )

                        print(
                            f"  {name:16} "
                            f"n={size:5d} "
                            f"avg={result.average_time:.6f}s "
                            f"+/- {result.std_deviation:.6f}s "
                            f"[{progress:5.1f}%]"
                        )

                    except Exception as error:
                        print(
                            f"  {name:16} "
                            f"n={size:5d} "
                            f"ERROR - {error}"
                        )

        return dict(all_results)

    def plot_comparison(
        self,
        results: Dict[str, List[BenchmarkResult]],
        filename: Optional[str] = None,
        title: str = "Algorithm Performance Comparison",
        data_type: Optional[str] = None,
        log_scale: bool = False,
        show_plot: bool = False,
    ) -> None:
        """
        Create a performance comparison visualization.

        Args:
            results: Results returned by benchmark_suite.
            filename: Optional path used to save the graph.
            title: Graph title.
            data_type: Restrict graph to one input type.
            log_scale: Use logarithmic x and y axes.
            show_plot: Display graph interactively.
        """
        plt.figure(figsize=(12, 8))

        plotted_anything = False

        for name, result_list in results.items():
            selected = result_list

            if data_type is not None:
                selected = [
                    result
                    for result in result_list
                    if result.data_type == data_type
                ]

            selected = sorted(
                selected,
                key=lambda result: result.input_size,
            )

            if not selected:
                continue

            sizes = [
                result.input_size
                for result in selected
            ]

            times = [
                result.average_time
                for result in selected
            ]

            deviations = [
                result.std_deviation
                for result in selected
            ]

            plt.plot(
                sizes,
                times,
                marker="o",
                linewidth=2,
                label=name,
            )

            plt.errorbar(
                sizes,
                times,
                yerr=deviations,
                alpha=0.4,
                capsize=3,
            )

            plotted_anything = True

        plt.xlabel("Input Size (n)")
        plt.ylabel("Average Time (seconds)")

        display_title = title

        if data_type:
            readable_type = data_type.replace("_", " ").title()
            display_title = f"{title} - {readable_type} Data"

        plt.title(display_title)
        plt.grid(True, alpha=0.3)

        if plotted_anything:
            plt.legend()

        if log_scale:
            plt.xscale("log")
            plt.yscale("log")

            # Add theoretical reference lines when enough data exists.
            all_sizes = sorted(
                {
                    result.input_size
                    for result_list in results.values()
                    for result in result_list
                    if (
                        data_type is None
                        or result.data_type == data_type
                    )
                    and result.input_size > 0
                }
            )

            if len(all_sizes) >= 2:
                min_size = min(all_sizes)
                max_size = max(all_sizes)

                ref_sizes = np.logspace(
                    np.log10(min_size),
                    np.log10(max_size),
                    50,
                )

                base_time = 1e-8

                plt.plot(
                    ref_sizes,
                    base_time * ref_sizes,
                    "--",
                    alpha=0.5,
                    label="O(n)",
                )

                plt.plot(
                    ref_sizes,
                    (
                        base_time
                        * ref_sizes
                        * np.log2(ref_sizes)
                    ),
                    "--",
                    alpha=0.5,
                    label="O(n log n)",
                )

                plt.plot(
                    ref_sizes,
                    base_time * ref_sizes ** 2,
                    "--",
                    alpha=0.5,
                    label="O(n^2)",
                )

                plt.legend()

        plt.tight_layout()

        if filename:
            output_path = Path(filename)
            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            plt.savefig(
                output_path,
                dpi=300,
                bbox_inches="tight",
            )

            print(f"Plot saved to {output_path}")

        if show_plot:
            plt.show()

        plt.close()

    def analyze_complexity(
        self,
        results: List[BenchmarkResult],
        algorithm_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Estimate empirical complexity from benchmark measurements.

        Attempts to fit:
        - O(n)
        - O(n log n)
        - O(n^2)

        Args:
            results: Measurements for one algorithm and data type.
            algorithm_name: Optional display name.

        Returns:
            Dictionary containing fit statistics and interpretation.
        """
        if len(results) < 3:
            return {
                "error":
                "Need at least 3 data points for complexity analysis"
            }

        sorted_results = sorted(
            results,
            key=lambda result: result.input_size,
        )

        sizes = np.array(
            [
                result.input_size
                for result in sorted_results
            ],
            dtype=float,
        )

        times = np.array(
            [
                result.average_time
                for result in sorted_results
            ],
            dtype=float,
        )

        # Avoid numerical problems if all measurements rounded to zero.
        if np.all(times == times[0]):
            return {
                "algorithm": algorithm_name or "Unknown",
                "best_fit_complexity": "Undetermined",
                "best_fit_r_squared": 0.0,
                "all_fits": {},
                "average_doubling_ratio": 0.0,
                "interpretation":
                "Timing values did not vary enough for reliable analysis.",
            }

        complexity_fits = {}

        # O(n)
        linear_fit = np.polyfit(sizes, times, 1)
        linear_prediction = np.polyval(
            linear_fit,
            sizes,
        )

        linear_r2 = self._calculate_r_squared(
            times,
            linear_prediction,
        )

        complexity_fits["O(n)"] = {
            "r_squared": linear_r2,
            "coefficients": linear_fit,
        }

        # O(n^2)
        quadratic_input = sizes ** 2

        quadratic_fit = np.polyfit(
            quadratic_input,
            times,
            1,
        )

        quadratic_prediction = np.polyval(
            quadratic_fit,
            quadratic_input,
        )

        quadratic_r2 = self._calculate_r_squared(
            times,
            quadratic_prediction,
        )

        complexity_fits["O(n^2)"] = {
            "r_squared": quadratic_r2,
            "coefficients": quadratic_fit,
        }

        # O(n log n)
        nlogn_input = sizes * np.log2(
            np.maximum(sizes, 2)
        )

        nlogn_fit = np.polyfit(
            nlogn_input,
            times,
            1,
        )

        nlogn_prediction = np.polyval(
            nlogn_fit,
            nlogn_input,
        )

        nlogn_r2 = self._calculate_r_squared(
            times,
            nlogn_prediction,
        )

        complexity_fits["O(n log n)"] = {
            "r_squared": nlogn_r2,
            "coefficients": nlogn_fit,
        }

        best_fit = max(
            complexity_fits.items(),
            key=lambda item: item[1]["r_squared"],
        )

        doubling_ratios = []

        for i in range(1, len(sorted_results)):
            previous_size = sizes[i - 1]
            current_size = sizes[i]

            previous_time = times[i - 1]
            current_time = times[i]

            if (
                previous_size > 0
                and previous_time > 0
                and current_size > previous_size
            ):
                size_ratio = (
                    current_size / previous_size
                )

                time_ratio = (
                    current_time / previous_time
                )

                normalized_ratio = (
                    time_ratio / size_ratio
                )

                doubling_ratios.append(
                    normalized_ratio
                )

        average_ratio = (
            float(np.mean(doubling_ratios))
            if doubling_ratios
            else 0.0
        )

        best_complexity = best_fit[0]
        best_r2 = float(
            best_fit[1]["r_squared"]
        )

        return {
            "algorithm": algorithm_name or "Unknown",
            "best_fit_complexity": best_complexity,
            "best_fit_r_squared": best_r2,
            "all_fits": complexity_fits,
            "average_doubling_ratio": average_ratio,
            "interpretation":
            self._interpret_complexity(
                best_complexity,
                best_r2,
                average_ratio,
            ),
        }

    def _calculate_r_squared(
        self,
        actual: np.ndarray,
        predicted: np.ndarray,
    ) -> float:
        """Calculate the coefficient of determination, R-squared."""
        residual_sum = np.sum(
            (actual - predicted) ** 2
        )

        total_sum = np.sum(
            (actual - np.mean(actual)) ** 2
        )

        if total_sum == 0:
            return 0.0

        return float(
            1 - residual_sum / total_sum
        )

    def _interpret_complexity(
        self,
        complexity: str,
        r_squared: float,
        doubling_ratio: float,
    ) -> str:
        """
        Provide a human-readable interpretation of complexity results.
        """
        interpretation = (
            f"Best fit: {complexity} "
            f"(R^2 = {r_squared:.3f})\n"
        )

        if r_squared > 0.95:
            interpretation += (
                "Excellent fit - high confidence "
                "in the complexity estimate."
            )

        elif r_squared > 0.85:
            interpretation += (
                "Good fit - reasonable confidence "
                "in the complexity estimate."
            )

        else:
            interpretation += (
                "Poor fit - more measurements may "
                "be needed."
            )

        if complexity == "O(n)" and 0.8 < doubling_ratio < 1.2:
            interpretation += (
                "\nDoubling behavior supports "
                "approximately linear growth."
            )

        elif (
            complexity == "O(n^2)"
            and 1.5 < doubling_ratio < 2.5
        ):
            interpretation += (
                "\nDoubling behavior supports "
                "approximately quadratic growth."
            )

        elif (
            complexity == "O(n log n)"
            and 1.0 < doubling_ratio < 1.6
        ):
            interpretation += (
                "\nDoubling behavior suggests "
                "linearithmic growth."
            )

        return interpretation

    def export_results(
        self,
        filename: str,
        format: str = "csv",
    ) -> None:
        """
        Export collected benchmark results.

        Args:
            filename: Destination file.
            format: Export format. Currently CSV only.
        """
        if not self.results:
            print("No results to export")
            return

        if format != "csv":
            raise ValueError(
                f"Unsupported format: {format}"
            )

        output_path = Path(filename)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        fieldnames = list(
            asdict(self.results[0]).keys()
        )

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            for result in self.results:
                writer.writerow(
                    asdict(result)
                )

        print(
            f"Results exported to {output_path}"
        )