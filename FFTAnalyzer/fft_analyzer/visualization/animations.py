"""Animation helpers for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

from FFTAnalyzer.fft_analyzer.core.fft import (
    iterative_fft,
    next_power_of_two,
)


def _as_signal(values) -> np.ndarray:
    """Convert input to a finite, one-dimensional signal."""
    try:
        signal = np.asarray(
            values,
            dtype=float,
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Signal must contain numeric values."
        ) from exc

    if signal.ndim != 1:
        raise ValueError(
            "Signal must be one-dimensional."
        )

    if signal.size == 0:
        raise ValueError(
            "Signal cannot be empty."
        )

    if not np.all(
        np.isfinite(signal)
    ):
        raise ValueError(
            "Signal must contain finite values."
        )

    return signal.copy()


def _validate_sample_rate(
    sample_rate: float,
) -> float:
    """Validate a positive sampling rate."""
    try:
        rate = float(
            sample_rate
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "sample_rate must be numeric."
        ) from exc

    if (
        not np.isfinite(rate)
        or rate <= 0
    ):
        raise ValueError(
            "sample_rate must be positive and finite."
        )

    return rate


def animate_fft_build(
    values,
    sample_rate: float,
    *,
    frames: int = 20,
    interval: int = 150,
):
    """
    Animate the frequency spectrum as more signal samples are included.

    Each frame uses a progressively larger portion of the original
    signal and computes its spectrum using the project's FFT.
    """
    signal = _as_signal(
        values
    )

    rate = _validate_sample_rate(
        sample_rate
    )

    if not isinstance(
        frames,
        int,
    ):
        raise TypeError(
            "frames must be an integer."
        )

    if frames < 2:
        raise ValueError(
            "frames must be at least 2."
        )

    if not isinstance(
        interval,
        int,
    ):
        raise TypeError(
            "interval must be an integer."
        )

    if interval <= 0:
        raise ValueError(
            "interval must be positive."
        )

    figure, axis = plt.subplots()

    line, = axis.plot(
        [],
        [],
    )

    axis.set_title(
        "FFT Build-Up"
    )

    axis.set_xlabel(
        "Frequency (Hz)"
    )

    axis.set_ylabel(
        "Magnitude"
    )

    maximum_frequency = (
        rate / 2.0
    )

    axis.set_xlim(
        0,
        maximum_frequency,
    )

    full_length = signal.size

    frame_lengths = np.linspace(
        max(
            2,
            full_length // frames,
        ),
        full_length,
        frames,
        dtype=int,
    )

    def update(frame_index):
        current_length = int(
            frame_lengths[
                frame_index
            ]
        )

        current = signal[
            :current_length
        ]

        transform_length = next_power_of_two(
            current_length
        )

        padded = np.zeros(
            transform_length,
            dtype=complex,
        )

        padded[
            :current_length
        ] = current

        spectrum = iterative_fft(
            padded
        )

        positive_count = (
            transform_length // 2 + 1
        )

        frequencies = (
            np.arange(
                positive_count,
                dtype=float,
            )
            * rate
            / transform_length
        )

        magnitude = np.abs(
            spectrum[
                :positive_count
            ]
        )

        line.set_data(
            frequencies,
            magnitude,
        )

        maximum = float(
            np.max(
                magnitude
            )
        )

        if maximum <= 0:
            maximum = 1.0

        axis.set_ylim(
            0,
            maximum * 1.05,
        )

        axis.set_title(
            f"FFT Build-Up: {current_length} Samples"
        )

        return (
            line,
        )

    animation = FuncAnimation(
        figure,
        update,
        frames=frames,
        interval=interval,
        blit=False,
        repeat=False,
    )

    return (
        figure,
        animation,
    )


def animate_frequency_filter(
    values,
    sample_rate: float,
    *,
    frames: int = 20,
    interval: int = 150,
):
    """
    Animate progressive removal of high-frequency FFT components.

    The first frame keeps most of the available spectrum. Later frames
    lower the cutoff until mainly low-frequency content remains.
    """
    signal = _as_signal(
        values
    )

    rate = _validate_sample_rate(
        sample_rate
    )

    if not isinstance(
        frames,
        int,
    ):
        raise TypeError(
            "frames must be an integer."
        )

    if frames < 2:
        raise ValueError(
            "frames must be at least 2."
        )

    if not isinstance(
        interval,
        int,
    ):
        raise TypeError(
            "interval must be an integer."
        )

    if interval <= 0:
        raise ValueError(
            "interval must be positive."
        )

    original_length = signal.size

    transform_length = next_power_of_two(
        original_length
    )

    padded = np.zeros(
        transform_length,
        dtype=complex,
    )

    padded[
        :original_length
    ] = signal

    spectrum = iterative_fft(
        padded
    )

    indices = np.arange(
        transform_length,
        dtype=float,
    )

    frequencies = (
        indices
        * rate
        / transform_length
    )

    frequencies[
        indices > transform_length // 2
    ] -= rate

    maximum_cutoff = (
        rate / 2.0
    )

    minimum_cutoff = (
        maximum_cutoff
        / max(
            frames,
            2,
        )
    )

    cutoffs = np.linspace(
        maximum_cutoff,
        minimum_cutoff,
        frames,
    )

    times = (
        np.arange(
            original_length,
            dtype=float,
        )
        / rate
    )

    figure, axis = plt.subplots()

    line, = axis.plot(
        times,
        signal,
    )

    axis.set_xlabel(
        "Time (s)"
    )

    axis.set_ylabel(
        "Amplitude"
    )

    maximum_amplitude = float(
        np.max(
            np.abs(
                signal
            )
        )
    )

    if maximum_amplitude <= 0:
        maximum_amplitude = 1.0

    axis.set_ylim(
        -maximum_amplitude * 1.2,
        maximum_amplitude * 1.2,
    )

    axis.set_xlim(
        times[
            0
        ],
        times[
            -1
        ]
        if times.size > 1
        else 1.0 / rate,
    )

    def update(frame_index):
        cutoff = float(
            cutoffs[
                frame_index
            ]
        )

        mask = (
            np.abs(
                frequencies
            )
            <= cutoff
        )

        filtered_spectrum = (
            spectrum
            * mask
        )

        conjugated = np.conjugate(
            filtered_spectrum
        )

        reconstructed = np.conjugate(
            iterative_fft(
                conjugated
            )
        ) / transform_length

        filtered = np.real(
            reconstructed[
                :original_length
            ]
        )

        line.set_data(
            times,
            filtered,
        )

        axis.set_title(
            f"Low-Pass Filtering: Cutoff {cutoff:.2f} Hz"
        )

        return (
            line,
        )

    animation = FuncAnimation(
        figure,
        update,
        frames=frames,
        interval=interval,
        blit=False,
        repeat=False,
    )

    return (
        figure,
        animation,
    )


def close_animation(
    figure,
) -> None:
    """Close the figure associated with an animation."""
    plt.close(
        figure
    )