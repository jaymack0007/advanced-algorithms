"""Smoke benchmark for the Week 12 FFT implementation."""

from __future__ import annotations

from time import perf_counter

import numpy as np

from FFTAnalyzer.fft_analyzer.core.fft import (
    iterative_fft,
    recursive_fft,
)


def run_iterative_test(
    size: int,
) -> None:
    """Time the iterative FFT and compare it with NumPy."""
    rng = np.random.default_rng(
        2026
    )

    values = rng.normal(
        size=size
    )

    start = perf_counter()

    result = iterative_fft(
        values
    )

    elapsed = (
        perf_counter()
        - start
    )

    expected = np.fft.fft(
        values
    )

    maximum_error = float(
        np.max(
            np.abs(
                result
                - expected
            )
        )
    )

    print(
        f"Iterative FFT | "
        f"n={size:,} | "
        f"time={elapsed:.6f}s | "
        f"max error={maximum_error:.3e}"
    )


def run_recursive_test(
    size: int,
) -> None:
    """Time the recursive FFT on a moderate input size."""
    rng = np.random.default_rng(
        2026
    )

    values = rng.normal(
        size=size
    )

    start = perf_counter()

    result = recursive_fft(
        values
    )

    elapsed = (
        perf_counter()
        - start
    )

    expected = np.fft.fft(
        values
    )

    maximum_error = float(
        np.max(
            np.abs(
                result
                - expected
            )
        )
    )

    print(
        f"Recursive FFT | "
        f"n={size:,} | "
        f"time={elapsed:.6f}s | "
        f"max error={maximum_error:.3e}"
    )


def main() -> None:
    print(
        "Week 12 FFT Smoke Benchmark"
    )

    print(
        "-" * 70
    )

    for size in [
        2**12,
        2**16,
        2**20,
    ]:
        run_iterative_test(
            size
        )

    print()

    run_recursive_test(
        2**14
    )


if __name__ == "__main__":
    main()