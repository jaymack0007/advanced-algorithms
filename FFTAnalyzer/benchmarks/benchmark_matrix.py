"""Stable matrix multiplication benchmark for Week 12."""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import median
from time import perf_counter

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from FFTAnalyzer.fft_analyzer.core.matrix import (
    classical_matrix_multiply,
)


PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def median_time_per_call(
    function,
    *args,
    calls_per_batch: int,
    batches: int = 5,
) -> float:
    """
    Measure median execution time per function call.

    A warm-up call is performed first so one-time initialization does
    not distort the recorded timings.
    """
    function(
        *args
    )

    batch_times = []

    for _ in range(
        batches
    ):
        start = perf_counter()

        for _ in range(
            calls_per_batch
        ):
            function(
                *args
            )

        elapsed = (
            perf_counter()
            - start
        )

        batch_times.append(
            elapsed
            / calls_per_batch
        )

    return float(
        median(
            batch_times
        )
    )


def classical_calls(
    size: int,
) -> int:
    """Choose reasonable batch sizes for the slower Python algorithm."""
    if size <= 16:
        return 5

    if size <= 32:
        return 3

    return 1


def numpy_calls(
    size: int,
) -> int:
    """Use many NumPy calls so very short runtimes can be measured fairly."""
    if size <= 16:
        return 5000

    if size <= 32:
        return 2000

    if size <= 64:
        return 500

    return 100


def benchmark_matrix_multiplication():
    """Compare classical O(n^3) multiplication with optimized NumPy."""
    sizes = [
        16,
        32,
        64,
        128,
    ]

    rng = np.random.default_rng(
        2026
    )

    rows = []

    print(
        "Stable Matrix Multiplication Benchmark"
    )

    print(
        "-" * 86
    )

    for size in sizes:
        left = rng.normal(
            size=(
                size,
                size,
            )
        )

        right = rng.normal(
            size=(
                size,
                size,
            )
        )

        classical_batch = classical_calls(
            size
        )

        numpy_batch = numpy_calls(
            size
        )

        classical_time = median_time_per_call(
            classical_matrix_multiply,
            left,
            right,
            calls_per_batch=classical_batch,
            batches=3,
        )

        numpy_time = median_time_per_call(
            np.matmul,
            left,
            right,
            calls_per_batch=numpy_batch,
            batches=5,
        )

        result = classical_matrix_multiply(
            left,
            right,
        )

        expected = (
            left
            @ right
        )

        maximum_error = float(
            np.max(
                np.abs(
                    result
                    - expected
                )
            )
        )

        ratio = (
            classical_time
            / numpy_time
        )

        rows.append(
            {
                "size": size,
                "classical_time_seconds": classical_time,
                "numpy_time_seconds": numpy_time,
                "classical_vs_numpy_ratio": ratio,
                "max_error": maximum_error,
                "classical_calls_per_batch": classical_batch,
                "numpy_calls_per_batch": numpy_batch,
            }
        )

        print(
            f"n={size:>3} | "
            f"Classical={classical_time:.6f}s | "
            f"NumPy={numpy_time:.8f}s | "
            f"ratio={ratio:.2f}x | "
            f"error={maximum_error:.3e}"
        )

    return rows


def save_results(
    rows,
) -> Path:
    """Save corrected matrix benchmark results."""
    path = (
        RESULTS_DIR
        / "matrix_benchmark_results.csv"
    )

    fieldnames = [
        "size",
        "classical_time_seconds",
        "numpy_time_seconds",
        "classical_vs_numpy_ratio",
        "max_error",
        "classical_calls_per_batch",
        "numpy_calls_per_batch",
    ]

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(
            rows
        )

    return path


def plot_results(
    rows,
) -> Path:
    """Create corrected matrix runtime plot."""
    path = (
        RESULTS_DIR
        / "matrix_runtime.png"
    )

    sizes = [
        row[
            "size"
        ]
        for row in rows
    ]

    classical = [
        row[
            "classical_time_seconds"
        ]
        for row in rows
    ]

    numpy_times = [
        row[
            "numpy_time_seconds"
        ]
        for row in rows
    ]

    figure, axis = plt.subplots()

    axis.plot(
        sizes,
        classical,
        marker="o",
        label="Classical O(n^3)",
    )

    axis.plot(
        sizes,
        numpy_times,
        marker="o",
        label="NumPy",
    )

    axis.set_yscale(
        "log"
    )

    axis.set_title(
        "Matrix Multiplication Runtime"
    )

    axis.set_xlabel(
        "Square Matrix Size (n)"
    )

    axis.set_ylabel(
        "Median Runtime per Call (seconds)"
    )

    axis.grid(
        True,
        alpha=0.3,
    )

    axis.legend()

    figure.tight_layout()

    figure.savefig(
        path,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    return path


def main() -> None:
    rows = benchmark_matrix_multiplication()

    csv_path = save_results(
        rows
    )

    plot_path = plot_results(
        rows
    )

    print()

    print(
        "Saved Corrected Results"
    )

    print(
        "-" * 86
    )

    print(
        csv_path
    )

    print(
        plot_path
    )


if __name__ == "__main__":
    main()