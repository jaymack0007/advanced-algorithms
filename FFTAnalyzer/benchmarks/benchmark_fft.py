"""Stable FFT benchmarks for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import csv
from pathlib import Path
from statistics import median
from time import perf_counter

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from FFTAnalyzer.fft_analyzer.core.fft import (
    direct_dft,
    iterative_fft,
    recursive_fft,
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
    values,
    *,
    calls_per_batch: int,
    batches: int,
) -> float:
    """Return a warmed-up median execution time per call."""
    function(
        values
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
                values
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


def iterative_calls(
    size: int,
) -> int:
    """Choose batch size for the custom iterative FFT."""
    if size <= 2**12:
        return 10

    if size <= 2**16:
        return 5

    if size <= 2**18:
        return 2

    return 1


def numpy_calls(
    size: int,
) -> int:
    """Use larger batches for the faster NumPy FFT."""
    if size <= 2**12:
        return 500

    if size <= 2**16:
        return 100

    if size <= 2**18:
        return 20

    return 5


def recursive_calls(
    size: int,
) -> int:
    """Choose batch size for the slower recursive FFT."""
    if size <= 2**10:
        return 5

    if size <= 2**12:
        return 3

    return 1


def benchmark_fft_scaling():
    """Benchmark iterative, recursive, and NumPy FFT implementations."""
    sizes = [
        2**8,
        2**10,
        2**12,
        2**14,
        2**16,
        2**18,
        2**20,
    ]

    recursive_limit = (
        2**16
    )

    rng = np.random.default_rng(
        2026
    )

    rows = []

    print(
        "Stable FFT Scaling Benchmark"
    )

    print(
        "-" * 86
    )

    for size in sizes:
        values = rng.normal(
            size=size
        )

        expected = np.fft.fft(
            values
        )

        iterative_batch = iterative_calls(
            size
        )

        numpy_batch = numpy_calls(
            size
        )

        iterative_time = median_time_per_call(
            iterative_fft,
            values,
            calls_per_batch=iterative_batch,
            batches=5,
        )

        numpy_time = median_time_per_call(
            np.fft.fft,
            values,
            calls_per_batch=numpy_batch,
            batches=5,
        )

        iterative_result = iterative_fft(
            values
        )

        iterative_error = float(
            np.max(
                np.abs(
                    iterative_result
                    - expected
                )
            )
        )

        rows.append(
            {
                "size": size,
                "method": "Iterative FFT",
                "time_seconds": iterative_time,
                "max_error": iterative_error,
                "calls_per_batch": iterative_batch,
                "batches": 5,
            }
        )

        rows.append(
            {
                "size": size,
                "method": "NumPy FFT",
                "time_seconds": numpy_time,
                "max_error": 0.0,
                "calls_per_batch": numpy_batch,
                "batches": 5,
            }
        )

        print(
            f"n={size:>9,} | "
            f"Iterative={iterative_time:.6f}s | "
            f"NumPy={numpy_time:.6f}s | "
            f"error={iterative_error:.3e}"
        )

        if size <= recursive_limit:
            recursive_batch = recursive_calls(
                size
            )

            recursive_time = median_time_per_call(
                recursive_fft,
                values,
                calls_per_batch=recursive_batch,
                batches=3,
            )

            recursive_result = recursive_fft(
                values
            )

            recursive_error = float(
                np.max(
                    np.abs(
                        recursive_result
                        - expected
                    )
                )
            )

            rows.append(
                {
                    "size": size,
                    "method": "Recursive FFT",
                    "time_seconds": recursive_time,
                    "max_error": recursive_error,
                    "calls_per_batch": recursive_batch,
                    "batches": 3,
                }
            )

            print(
                f"{'':>13} | "
                f"Recursive={recursive_time:.6f}s | "
                f"error={recursive_error:.3e}"
            )

    return rows


def dft_calls(
    size: int,
) -> int:
    """Choose batch size for direct DFT timing."""
    if size <= 64:
        return 5

    if size <= 128:
        return 3

    return 1


def fft_comparison_calls(
    size: int,
) -> int:
    """Choose batch size for FFT timing in the DFT comparison."""
    if size <= 128:
        return 100

    return 50


def benchmark_dft_comparison():
    """Compare direct O(n^2) DFT with O(n log n) iterative FFT."""
    sizes = [
        32,
        64,
        128,
        256,
        512,
    ]

    rng = np.random.default_rng(
        5300
    )

    rows = []

    print()

    print(
        "Stable Direct DFT vs Iterative FFT"
    )

    print(
        "-" * 86
    )

    for size in sizes:
        values = rng.normal(
            size=size
        )

        dft_batch = dft_calls(
            size
        )

        fft_batch = fft_comparison_calls(
            size
        )

        dft_time = median_time_per_call(
            direct_dft,
            values,
            calls_per_batch=dft_batch,
            batches=5,
        )

        fft_time = median_time_per_call(
            iterative_fft,
            values,
            calls_per_batch=fft_batch,
            batches=5,
        )

        dft_result = direct_dft(
            values
        )

        fft_result = iterative_fft(
            values
        )

        maximum_difference = float(
            np.max(
                np.abs(
                    dft_result
                    - fft_result
                )
            )
        )

        speedup = (
            dft_time
            / fft_time
        )

        rows.append(
            {
                "size": size,
                "dft_time_seconds": dft_time,
                "fft_time_seconds": fft_time,
                "speedup": speedup,
                "max_difference": maximum_difference,
            }
        )

        print(
            f"n={size:>4} | "
            f"DFT={dft_time:.6f}s | "
            f"FFT={fft_time:.6f}s | "
            f"speedup={speedup:.2f}x | "
            f"difference={maximum_difference:.3e}"
        )

    return rows


def save_fft_csv(
    rows,
) -> Path:
    """Save FFT scaling benchmark data."""
    path = (
        RESULTS_DIR
        / "fft_benchmark_results.csv"
    )

    fieldnames = [
        "size",
        "method",
        "time_seconds",
        "max_error",
        "calls_per_batch",
        "batches",
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


def save_dft_csv(
    rows,
) -> Path:
    """Save direct DFT versus FFT benchmark data."""
    path = (
        RESULTS_DIR
        / "dft_vs_fft_results.csv"
    )

    fieldnames = [
        "size",
        "dft_time_seconds",
        "fft_time_seconds",
        "speedup",
        "max_difference",
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


def plot_fft_scaling(
    rows,
) -> Path:
    """Create a log-log FFT runtime scaling plot."""
    path = (
        RESULTS_DIR
        / "fft_runtime_scaling.png"
    )

    figure, axis = plt.subplots()

    for method in [
        "Iterative FFT",
        "Recursive FFT",
        "NumPy FFT",
    ]:
        method_rows = [
            row
            for row in rows
            if row[
                "method"
            ] == method
        ]

        if not method_rows:
            continue

        sizes = [
            row[
                "size"
            ]
            for row in method_rows
        ]

        times = [
            row[
                "time_seconds"
            ]
            for row in method_rows
        ]

        axis.plot(
            sizes,
            times,
            marker="o",
            label=method,
        )

    axis.set_xscale(
        "log",
        base=2,
    )

    axis.set_yscale(
        "log",
    )

    axis.set_title(
        "FFT Runtime Scaling"
    )

    axis.set_xlabel(
        "Input Size (n)"
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


def plot_dft_comparison(
    rows,
) -> Path:
    """Create direct DFT versus FFT runtime comparison plot."""
    path = (
        RESULTS_DIR
        / "dft_vs_fft.png"
    )

    sizes = [
        row[
            "size"
        ]
        for row in rows
    ]

    dft_times = [
        row[
            "dft_time_seconds"
        ]
        for row in rows
    ]

    fft_times = [
        row[
            "fft_time_seconds"
        ]
        for row in rows
    ]

    figure, axis = plt.subplots()

    axis.plot(
        sizes,
        dft_times,
        marker="o",
        label="Direct DFT O(n^2)",
    )

    axis.plot(
        sizes,
        fft_times,
        marker="o",
        label="Iterative FFT O(n log n)",
    )

    axis.set_yscale(
        "log",
    )

    axis.set_title(
        "Direct DFT vs Iterative FFT"
    )

    axis.set_xlabel(
        "Input Size (n)"
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
    fft_rows = benchmark_fft_scaling()

    dft_rows = benchmark_dft_comparison()

    fft_csv = save_fft_csv(
        fft_rows
    )

    dft_csv = save_dft_csv(
        dft_rows
    )

    fft_plot = plot_fft_scaling(
        fft_rows
    )

    dft_plot = plot_dft_comparison(
        dft_rows
    )

    print()

    print(
        "Saved Stable Results"
    )

    print(
        "-" * 86
    )

    for path in [
        fft_csv,
        dft_csv,
        fft_plot,
        dft_plot,
    ]:
        print(
            path
        )


if __name__ == "__main__":
    main()