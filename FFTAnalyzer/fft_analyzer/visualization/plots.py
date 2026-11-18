"""Visualization helpers for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from FFTAnalyzer.fft_analyzer.core.numerical import (
    condition_number,
)
from FFTAnalyzer.fft_analyzer.image.filters import (
    fft2,
    pad_image_to_power_of_two,
)
from FFTAnalyzer.fft_analyzer.signal.analysis import (
    periodogram,
    spectrogram,
)


def _save_figure(
    figure,
    save_path=None,
) -> None:
    """Save a figure when a path is supplied."""
    if save_path is None:
        return

    path = Path(
        save_path
    )

    if path.parent != Path("."):
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    figure.savefig(
        path,
        bbox_inches="tight",
    )


def plot_fft_spectrum(
    values,
    sample_rate: float,
    *,
    title: str = "Frequency Spectrum",
    window: str = "hanning",
    save_path=None,
):
    """Plot a one-sided FFT power spectrum."""
    frequencies, power = periodogram(
        values,
        sample_rate,
        window=window,
    )

    figure, axis = plt.subplots()

    axis.plot(
        frequencies,
        power,
    )

    axis.set_title(
        title
    )

    axis.set_xlabel(
        "Frequency (Hz)"
    )

    axis.set_ylabel(
        "Power"
    )

    axis.grid(
        True,
        alpha=0.3,
    )

    _save_figure(
        figure,
        save_path,
    )

    return (
        figure,
        axis,
    )


def plot_spectrogram(
    values,
    sample_rate: float,
    *,
    window_size: int = 256,
    hop_size: int | None = None,
    title: str = "Spectrogram",
    save_path=None,
):
    """Plot an STFT spectrogram."""
    times, frequencies, power = spectrogram(
        values,
        sample_rate,
        window_size=window_size,
        hop_size=hop_size,
    )

    figure, axis = plt.subplots()

    decibels = 10.0 * np.log10(
        power
        + 1e-12
    )

    mesh = axis.pcolormesh(
        times,
        frequencies,
        decibels,
        shading="auto",
    )

    axis.set_title(
        title
    )

    axis.set_xlabel(
        "Time (s)"
    )

    axis.set_ylabel(
        "Frequency (Hz)"
    )

    figure.colorbar(
        mesh,
        ax=axis,
        label="Power (dB)",
    )

    _save_figure(
        figure,
        save_path,
    )

    return (
        figure,
        axis,
    )


def plot_fft_heatmap(
    values,
    *,
    title: str = "2D FFT Magnitude",
    logarithmic: bool = True,
    save_path=None,
):
    """Plot a centered 2D FFT magnitude heatmap."""
    image = np.asarray(
        values,
        dtype=float,
    )

    if image.ndim != 2:
        raise ValueError(
            "Image must be two-dimensional."
        )

    if image.size == 0:
        raise ValueError(
            "Image cannot be empty."
        )

    padded, _ = pad_image_to_power_of_two(
        image
    )

    spectrum = fft2(
        padded
    )

    magnitude = np.abs(
        spectrum
    )

    if logarithmic:
        magnitude = np.log1p(
            magnitude
        )

    magnitude = np.roll(
        magnitude,
        shift=magnitude.shape[0] // 2,
        axis=0,
    )

    magnitude = np.roll(
        magnitude,
        shift=magnitude.shape[1] // 2,
        axis=1,
    )

    figure, axis = plt.subplots()

    image_plot = axis.imshow(
        magnitude,
        origin="lower",
        aspect="auto",
    )

    axis.set_title(
        title
    )

    axis.set_xlabel(
        "Frequency X"
    )

    axis.set_ylabel(
        "Frequency Y"
    )

    figure.colorbar(
        image_plot,
        ax=axis,
        label="Log Magnitude"
        if logarithmic
        else "Magnitude",
    )

    _save_figure(
        figure,
        save_path,
    )

    return (
        figure,
        axis,
    )


def plot_condition_numbers(
    matrices,
    *,
    labels=None,
    norm: str = "1",
    title: str = "Matrix Condition Numbers",
    save_path=None,
):
    """Plot condition numbers for a collection of square matrices."""
    matrix_list = list(
        matrices
    )

    if not matrix_list:
        raise ValueError(
            "At least one matrix is required."
        )

    conditions = [
        condition_number(
            matrix,
            norm=norm,
        )
        for matrix in matrix_list
    ]

    if labels is None:
        label_values = [
            f"Matrix {index + 1}"
            for index in range(
                len(matrix_list)
            )
        ]
    else:
        label_values = list(
            labels
        )

        if len(
            label_values
        ) != len(
            matrix_list
        ):
            raise ValueError(
                "labels must match the number of matrices."
            )

    figure, axis = plt.subplots()

    positions = np.arange(
        len(
            conditions
        )
    )

    axis.bar(
        positions,
        conditions,
    )

    axis.set_xticks(
        positions
    )

    axis.set_xticklabels(
        label_values,
        rotation=20,
        ha="right",
    )

    axis.set_title(
        title
    )

    axis.set_xlabel(
        "Matrix"
    )

    axis.set_ylabel(
        "Condition Number"
    )

    axis.grid(
        True,
        axis="y",
        alpha=0.3,
    )

    _save_figure(
        figure,
        save_path,
    )

    return (
        figure,
        axis,
        conditions,
    )


def plot_signal_comparison(
    original,
    processed,
    *,
    sample_rate: float = 1.0,
    title: str = "Signal Comparison",
    save_path=None,
):
    """Plot original and processed signals on the same axes."""
    first = np.asarray(
        original,
        dtype=float,
    )

    second = np.asarray(
        processed,
        dtype=float,
    )

    if (
        first.ndim != 1
        or second.ndim != 1
    ):
        raise ValueError(
            "Signals must be one-dimensional."
        )

    if first.size != second.size:
        raise ValueError(
            "Signals must have matching lengths."
        )

    if first.size == 0:
        raise ValueError(
            "Signals cannot be empty."
        )

    if sample_rate <= 0:
        raise ValueError(
            "sample_rate must be positive."
        )

    times = (
        np.arange(
            first.size
        )
        / sample_rate
    )

    figure, axis = plt.subplots()

    axis.plot(
        times,
        first,
        label="Original",
    )

    axis.plot(
        times,
        second,
        label="Processed",
    )

    axis.set_title(
        title
    )

    axis.set_xlabel(
        "Time"
    )

    axis.set_ylabel(
        "Amplitude"
    )

    axis.legend()

    axis.grid(
        True,
        alpha=0.3,
    )

    _save_figure(
        figure,
        save_path,
    )

    return (
        figure,
        axis,
    )


def close_figure(
    figure,
) -> None:
    """Close a Matplotlib figure explicitly."""
    plt.close(
        figure
    )