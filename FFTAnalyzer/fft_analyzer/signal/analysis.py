"""Spectral analysis tools for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import math

import numpy as np

from FFTAnalyzer.fft_analyzer.core.fft import (
    iterative_fft,
    next_power_of_two,
)
from FFTAnalyzer.fft_analyzer.signal.filters import (
    blackman_window,
    hamming_window,
    hanning_window,
)


def _as_real_signal(values) -> np.ndarray:
    """Convert input to a non-empty one-dimensional real signal."""
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
            "Signal must contain only finite values."
        )

    return signal.copy()


def _validate_sample_rate(
    sample_rate: float,
) -> float:
    """Validate a positive finite sampling rate."""
    try:
        rate = float(
            sample_rate
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "sample_rate must be numeric."
        ) from exc

    if (
        not math.isfinite(rate)
        or rate <= 0
    ):
        raise ValueError(
            "sample_rate must be positive and finite."
        )

    return rate


def _window_values(
    length: int,
    name: str,
) -> np.ndarray:
    """Return a supported analysis window."""
    normalized = str(
        name
    ).lower()

    if normalized in {
        "hann",
        "hanning",
    }:
        return hanning_window(
            length
        )

    if normalized == "hamming":
        return hamming_window(
            length
        )

    if normalized == "blackman":
        return blackman_window(
            length
        )

    if normalized in {
        "rectangular",
        "boxcar",
        "none",
    }:
        return np.ones(
            length,
            dtype=float,
        )

    raise ValueError(
        "window must be 'hanning', 'hamming', "
        "'blackman', or 'rectangular'."
    )


def _validate_n_fft(
    n_fft: int | None,
    minimum_length: int,
) -> int:
    """Validate or choose a radix-2 FFT size."""
    if n_fft is None:
        return next_power_of_two(
            minimum_length
        )

    if not isinstance(
        n_fft,
        int,
    ):
        raise TypeError(
            "n_fft must be an integer."
        )

    if n_fft < minimum_length:
        raise ValueError(
            "n_fft cannot be smaller than the input length."
        )

    if (
        n_fft <= 0
        or (
            n_fft
            & (
                n_fft - 1
            )
        )
        != 0
    ):
        raise ValueError(
            "n_fft must be a positive power of two."
        )

    return n_fft


def frequency_axis(
    n_fft: int,
    sample_rate: float,
) -> np.ndarray:
    """Return the nonnegative one-sided FFT frequency bins."""
    rate = _validate_sample_rate(
        sample_rate
    )

    if not isinstance(
        n_fft,
        int,
    ):
        raise TypeError(
            "n_fft must be an integer."
        )

    if n_fft <= 0:
        raise ValueError(
            "n_fft must be positive."
        )

    return (
        np.arange(
            n_fft // 2 + 1,
            dtype=float,
        )
        * rate
        / n_fft
    )


def periodogram(
    values,
    sample_rate: float,
    *,
    window: str = "hanning",
    n_fft: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute a one-sided power periodogram.

    The signal is windowed, zero-padded to a radix-2 FFT length when
    necessary, transformed with the project's iterative FFT, and
    converted to power.
    """
    signal = _as_real_signal(
        values
    )

    rate = _validate_sample_rate(
        sample_rate
    )

    transform_length = (
        _validate_n_fft(
            n_fft,
            signal.size,
        )
    )

    weights = _window_values(
        signal.size,
        window,
    )

    windowed = (
        signal
        * weights
    )

    padded = np.zeros(
        transform_length,
        dtype=complex,
    )

    padded[
        :signal.size
    ] = windowed

    spectrum = iterative_fft(
        padded
    )

    one_sided = spectrum[
        :transform_length // 2 + 1
    ]

    power = (
        np.abs(
            one_sided
        )
        ** 2
    )

    normalization = float(
        np.sum(
            weights * weights
        )
    )

    if normalization > 0:
        power /= normalization

    if power.size > 2:
        power[
            1:-1
        ] *= 2.0

    frequencies = frequency_axis(
        transform_length,
        rate,
    )

    return (
        frequencies,
        power,
    )


def power_spectral_density(
    values,
    sample_rate: float,
    *,
    window: str = "hanning",
    n_fft: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Estimate one-sided power spectral density.

    PSD is the periodogram power normalized by the sampling rate,
    producing power per Hz.
    """
    frequencies, power = periodogram(
        values,
        sample_rate,
        window=window,
        n_fft=n_fft,
    )

    density = (
        power
        / float(
            sample_rate
        )
    )

    return (
        frequencies,
        density,
    )


def detect_peak_frequencies(
    values,
    sample_rate: float,
    *,
    count: int = 1,
    min_frequency: float = 0.0,
    max_frequency: float | None = None,
    window: str = "hanning",
    n_fft: int | None = None,
) -> list[tuple[float, float]]:
    """
    Return the strongest local spectral peaks.

    Each result is:
        (frequency_hz, power)

    Results are ordered from strongest to weakest.
    """
    if not isinstance(
        count,
        int,
    ):
        raise TypeError(
            "count must be an integer."
        )

    if count <= 0:
        raise ValueError(
            "count must be positive."
        )

    rate = _validate_sample_rate(
        sample_rate
    )

    try:
        minimum = float(
            min_frequency
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "min_frequency must be numeric."
        ) from exc

    if max_frequency is None:
        maximum = (
            rate / 2.0
        )
    else:
        try:
            maximum = float(
                max_frequency
            )
        except (TypeError, ValueError) as exc:
            raise TypeError(
                "max_frequency must be numeric."
            ) from exc

    if minimum < 0:
        raise ValueError(
            "min_frequency cannot be negative."
        )

    if maximum > rate / 2.0:
        raise ValueError(
            "max_frequency cannot exceed Nyquist."
        )

    if minimum > maximum:
        raise ValueError(
            "min_frequency cannot exceed max_frequency."
        )

    frequencies, power = periodogram(
        values,
        rate,
        window=window,
        n_fft=n_fft,
    )

    allowed = (
        (frequencies >= minimum)
        & (frequencies <= maximum)
    )

    candidate_indices = []

    for index in range(
        1,
        power.size - 1,
    ):
        if not allowed[index]:
            continue

        if (
            power[index]
            >= power[index - 1]
            and power[index]
            >= power[index + 1]
        ):
            candidate_indices.append(
                index
            )

    if allowed[0]:
        candidate_indices.append(
            0
        )

    if (
        power.size > 1
        and allowed[-1]
    ):
        candidate_indices.append(
            power.size - 1
        )

    candidate_indices.sort(
        key=lambda index: power[index],
        reverse=True,
    )

    selected = (
        candidate_indices[
            :count
        ]
    )

    return [
        (
            float(
                frequencies[index]
            ),
            float(
                power[index]
            ),
        )
        for index in selected
    ]


def dominant_frequency(
    values,
    sample_rate: float,
    *,
    min_frequency: float = 0.0,
    max_frequency: float | None = None,
    window: str = "hanning",
    n_fft: int | None = None,
) -> float:
    """Return the strongest detected frequency in Hz."""
    peaks = detect_peak_frequencies(
        values,
        sample_rate,
        count=1,
        min_frequency=min_frequency,
        max_frequency=max_frequency,
        window=window,
        n_fft=n_fft,
    )

    if not peaks:
        raise ValueError(
            "No spectral peak was found."
        )

    return peaks[
        0
    ][
        0
    ]


def spectrogram(
    values,
    sample_rate: float,
    *,
    window_size: int = 256,
    hop_size: int | None = None,
    window: str = "hanning",
    n_fft: int | None = None,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """
    Compute a spectrogram using a short-time FFT.

    Returns:
        times
        frequencies
        power_matrix

    power_matrix has shape:
        (frequency_bins, time_frames)
    """
    signal = _as_real_signal(
        values
    )

    rate = _validate_sample_rate(
        sample_rate
    )

    if not isinstance(
        window_size,
        int,
    ):
        raise TypeError(
            "window_size must be an integer."
        )

    if window_size <= 0:
        raise ValueError(
            "window_size must be positive."
        )

    if hop_size is None:
        hop = max(
            1,
            window_size // 2,
        )
    else:
        if not isinstance(
            hop_size,
            int,
        ):
            raise TypeError(
                "hop_size must be an integer."
            )

        if hop_size <= 0:
            raise ValueError(
                "hop_size must be positive."
            )

        hop = hop_size

    transform_length = (
        _validate_n_fft(
            n_fft,
            window_size,
        )
    )

    weights = _window_values(
        window_size,
        window,
    )

    if signal.size <= window_size:
        starts = [
            0
        ]
    else:
        starts = list(
            range(
                0,
                signal.size - window_size + 1,
                hop,
            )
        )

        final_start = (
            signal.size
            - window_size
        )

        if starts[-1] != final_start:
            starts.append(
                final_start
            )

    frequency_bins = (
        transform_length // 2 + 1
    )

    power_matrix = np.zeros(
        (
            frequency_bins,
            len(starts),
        ),
        dtype=float,
    )

    times = np.zeros(
        len(starts),
        dtype=float,
    )

    normalization = float(
        np.sum(
            weights * weights
        )
    )

    for frame_index, start in enumerate(
        starts
    ):
        frame = np.zeros(
            window_size,
            dtype=float,
        )

        available = min(
            window_size,
            signal.size - start,
        )

        frame[
            :available
        ] = signal[
            start:start + available
        ]

        frame *= weights

        padded = np.zeros(
            transform_length,
            dtype=complex,
        )

        padded[
            :window_size
        ] = frame

        spectrum = iterative_fft(
            padded
        )

        one_sided = spectrum[
            :frequency_bins
        ]

        frame_power = (
            np.abs(
                one_sided
            )
            ** 2
        )

        if normalization > 0:
            frame_power /= normalization

        if frame_power.size > 2:
            frame_power[
                1:-1
            ] *= 2.0

        power_matrix[
            :,
            frame_index,
        ] = frame_power

        times[
            frame_index
        ] = (
            start
            + window_size / 2.0
        ) / rate

    frequencies = frequency_axis(
        transform_length,
        rate,
    )

    return (
        times,
        frequencies,
        power_matrix,
    )