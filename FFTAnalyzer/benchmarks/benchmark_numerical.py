"""Numerical conditioning and image-compression benchmarks for Week 12."""

from __future__ import annotations

import csv
from pathlib import Path
from time import perf_counter

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from FFTAnalyzer.fft_analyzer.core.numerical import (
    condition_number,
    is_ill_conditioned,
)
from FFTAnalyzer.fft_analyzer.image.compression import (
    compress_and_reconstruct,
    mean_squared_error,
    peak_signal_to_noise_ratio,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent

RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def benchmark_conditioning():
    """Measure condition numbers for increasingly difficult matrices."""
    epsilon_values = [
        1e-1,
        1e-3,
        1e-5,
        1e-7,
        1e-9,
        1e-11,
    ]

    rows = []

    print(
        "Matrix Conditioning Experiment"
    )

    print(
        "-" * 78
    )

    for epsilon in epsilon_values:
        matrix = np.array(
            [
                [1.0, 1.0],
                [1.0, 1.0 + epsilon],
            ],
            dtype=float,
        )

        condition = condition_number(
            matrix,
            norm="1",
        )

        ill_conditioned = is_ill_conditioned(
            matrix,
            threshold=1e10,
            norm="1",
        )

        rows.append(
            {
                "epsilon": epsilon,
                "condition_number": condition,
                "ill_conditioned": ill_conditioned,
            }
        )

        print(
            f"epsilon={epsilon:.0e} | "
            f"condition={condition:.6e} | "
            f"ill-conditioned={ill_conditioned}"
        )

    return rows


def make_test_image(
    size: int = 128,
) -> np.ndarray:
    """Create a deterministic synthetic grayscale image."""
    axis = np.linspace(
        0.0,
        255.0,
        size,
    )

    horizontal = np.tile(
        axis,
        (
            size,
            1,
        ),
    )

    vertical = horizontal.T

    image = (
        0.6 * horizontal
        + 0.4 * vertical
    )

    checker = (
        (
            np.indices(
                (
                    size,
                    size,
                )
            ).sum(
                axis=0
            )
            // 16
        )
        % 2
    )

    image += (
        checker
        * 20.0
    )

    return np.clip(
        image,
        0.0,
        255.0,
    )


def benchmark_image_compression():
    """Measure DCT reconstruction quality across JPEG-style qualities."""
    image = make_test_image()

    qualities = [
        10,
        30,
        50,
        70,
        90,
    ]

    rows = []

    print()

    print(
        "DCT Image Compression Experiment"
    )

    print(
        "-" * 78
    )

    for quality in qualities:
        start = perf_counter()

        reconstructed, compressed = compress_and_reconstruct(
            image,
            quality=quality,
        )

        elapsed = (
            perf_counter()
            - start
        )

        mse = mean_squared_error(
            image,
            reconstructed,
        )

        psnr = peak_signal_to_noise_ratio(
            image,
            reconstructed,
        )

        zero_fraction = float(
            compressed[
                "zero_fraction"
            ]
        )

        rows.append(
            {
                "quality": quality,
                "time_seconds": elapsed,
                "mse": mse,
                "psnr_db": psnr,
                "zero_fraction": zero_fraction,
            }
        )

        print(
            f"quality={quality:>3} | "
            f"time={elapsed:.6f}s | "
            f"MSE={mse:.6f} | "
            f"PSNR={psnr:.3f} dB | "
            f"zeros={zero_fraction:.3%}"
        )

    return rows


def save_csv(
    path: Path,
    rows,
    fieldnames,
) -> None:
    """Save dictionary rows to CSV."""
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


def plot_conditioning(
    rows,
) -> Path:
    """Plot condition number as epsilon approaches zero."""
    path = (
        RESULTS_DIR
        / "matrix_conditioning.png"
    )

    epsilon = [
        row[
            "epsilon"
        ]
        for row in rows
    ]

    conditions = [
        row[
            "condition_number"
        ]
        for row in rows
    ]

    figure, axis = plt.subplots()

    axis.plot(
        epsilon,
        conditions,
        marker="o",
    )

    axis.set_xscale(
        "log"
    )

    axis.set_yscale(
        "log"
    )

    axis.invert_xaxis()

    axis.set_title(
        "Condition Number as Matrix Rows Become Similar"
    )

    axis.set_xlabel(
        "Epsilon"
    )

    axis.set_ylabel(
        "1-Norm Condition Number"
    )

    axis.grid(
        True,
        alpha=0.3,
    )

    figure.tight_layout()

    figure.savefig(
        path,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    return path


def plot_compression_quality(
    rows,
) -> Path:
    """Plot PSNR across image-compression quality settings."""
    path = (
        RESULTS_DIR
        / "compression_quality.png"
    )

    qualities = [
        row[
            "quality"
        ]
        for row in rows
    ]

    psnr = [
        row[
            "psnr_db"
        ]
        for row in rows
    ]

    figure, axis = plt.subplots()

    axis.plot(
        qualities,
        psnr,
        marker="o",
    )

    axis.set_title(
        "DCT Compression Quality vs PSNR"
    )

    axis.set_xlabel(
        "Quality Setting"
    )

    axis.set_ylabel(
        "PSNR (dB)"
    )

    axis.grid(
        True,
        alpha=0.3,
    )

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
    conditioning_rows = benchmark_conditioning()

    compression_rows = benchmark_image_compression()

    conditioning_csv = (
        RESULTS_DIR
        / "conditioning_results.csv"
    )

    compression_csv = (
        RESULTS_DIR
        / "compression_results.csv"
    )

    save_csv(
        conditioning_csv,
        conditioning_rows,
        [
            "epsilon",
            "condition_number",
            "ill_conditioned",
        ],
    )

    save_csv(
        compression_csv,
        compression_rows,
        [
            "quality",
            "time_seconds",
            "mse",
            "psnr_db",
            "zero_fraction",
        ],
    )

    condition_plot = plot_conditioning(
        conditioning_rows
    )

    compression_plot = plot_compression_quality(
        compression_rows
    )

    print()

    print(
        "Saved Results"
    )

    print(
        "-" * 78
    )

    for path in [
        conditioning_csv,
        compression_csv,
        condition_plot,
        compression_plot,
    ]:
        print(
            path
        )


if __name__ == "__main__":
    main()