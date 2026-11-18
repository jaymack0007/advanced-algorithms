"""FFT-based signal filters and window functions."""

from __future__ import annotations

import math

import numpy as np

from FFTAnalyzer.fft_analyzer.core.fft import (
    ifft,
    iterative_fft,
    next_power_of_two,
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
    """Validate a positive finite sample rate."""
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


def _validate_cutoff(
    cutoff: float,
    sample_rate: float,
    *,
    name: str = "cutoff",
) -> float:
    """Validate a cutoff frequency against the Nyquist frequency."""
    try:
        value = float(
            cutoff
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            f"{name} must be numeric."
        ) from exc

    if (
        not math.isfinite(value)
        or value < 0
    ):
        raise ValueError(
            f"{name} must be nonnegative and finite."
        )

    nyquist = (
        sample_rate
        / 2.0
    )

    if value > nyquist:
        raise ValueError(
            f"{name} cannot exceed the Nyquist frequency."
        )

    return value


def _frequency_bins(
    length: int,
    sample_rate: float,
) -> np.ndarray:
    """
    Return signed DFT-bin frequencies without using numpy.fft.

    For an N-point transform, bins above N/2 represent negative
    frequencies.
    """
    indices = np.arange(
        length,
        dtype=float,
    )

    frequencies = (
        indices
        * sample_rate
        / length
    )

    negative_start = (
        length // 2
        + 1
    )

    frequencies[
        negative_start:
    ] -= sample_rate

    return frequencies


def _apply_frequency_mask(
    values,
    sample_rate: float,
    mask_builder,
) -> np.ndarray:
    """Apply a frequency-domain mask and return the original signal length."""
    signal = _as_real_signal(
        values
    )

    rate = _validate_sample_rate(
        sample_rate
    )

    original_length = (
        signal.size
    )

    transform_length = (
        next_power_of_two(
            original_length
        )
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

    frequencies = _frequency_bins(
        transform_length,
        rate,
    )

    mask = np.asarray(
        mask_builder(
            frequencies
        ),
        dtype=bool,
    )

    if mask.shape != spectrum.shape:
        raise ValueError(
            "Frequency mask shape does not match the spectrum."
        )

    filtered_spectrum = (
        spectrum
        * mask
    )

    filtered = ifft(
        filtered_spectrum
    )

    return np.real(
        filtered[
            :original_length
        ]
    )


def low_pass_filter(
    values,
    sample_rate: float,
    cutoff: float,
) -> np.ndarray:
    """Keep frequencies at or below cutoff."""
    rate = _validate_sample_rate(
        sample_rate
    )

    cutoff = _validate_cutoff(
        cutoff,
        rate,
    )

    return _apply_frequency_mask(
        values,
        rate,
        lambda frequencies: (
            np.abs(
                frequencies
            )
            <= cutoff
        ),
    )


def high_pass_filter(
    values,
    sample_rate: float,
    cutoff: float,
) -> np.ndarray:
    """Keep frequencies at or above cutoff."""
    rate = _validate_sample_rate(
        sample_rate
    )

    cutoff = _validate_cutoff(
        cutoff,
        rate,
    )

    return _apply_frequency_mask(
        values,
        rate,
        lambda frequencies: (
            np.abs(
                frequencies
            )
            >= cutoff
        ),
    )


def band_pass_filter(
    values,
    sample_rate: float,
    low_cutoff: float,
    high_cutoff: float,
) -> np.ndarray:
    """Keep frequencies between low_cutoff and high_cutoff."""
    rate = _validate_sample_rate(
        sample_rate
    )

    low = _validate_cutoff(
        low_cutoff,
        rate,
        name="low_cutoff",
    )

    high = _validate_cutoff(
        high_cutoff,
        rate,
        name="high_cutoff",
    )

    if low >= high:
        raise ValueError(
            "low_cutoff must be less than high_cutoff."
        )

    return _apply_frequency_mask(
        values,
        rate,
        lambda frequencies: (
            (
                np.abs(
                    frequencies
                )
                >= low
            )
            & (
                np.abs(
                    frequencies
                )
                <= high
            )
        ),
    )


def hanning_window(
    length: int,
) -> np.ndarray:
    """
    Return a Hann/Hanning window.

    The assignment uses the common term "Hanning"; this is the
    standard Hann window definition.
    """
    length = _validate_window_length(
        length
    )

    if length == 1:
        return np.ones(
            1,
            dtype=float,
        )

    indices = np.arange(
        length,
        dtype=float,
    )

    return (
        0.5
        - 0.5
        * np.cos(
            2.0
            * np.pi
            * indices
            / (
                length - 1
            )
        )
    )


def hamming_window(
    length: int,
) -> np.ndarray:
    """Return a Hamming window."""
    length = _validate_window_length(
        length
    )

    if length == 1:
        return np.ones(
            1,
            dtype=float,
        )

    indices = np.arange(
        length,
        dtype=float,
    )

    return (
        0.54
        - 0.46
        * np.cos(
            2.0
            * np.pi
            * indices
            / (
                length - 1
            )
        )
    )


def blackman_window(
    length: int,
) -> np.ndarray:
    """Return a Blackman window."""
    length = _validate_window_length(
        length
    )

    if length == 1:
        return np.ones(
            1,
            dtype=float,
        )

    indices = np.arange(
        length,
        dtype=float,
    )

    angle = (
        2.0
        * np.pi
        * indices
        / (
            length - 1
        )
    )

    return (
        0.42
        - 0.5
        * np.cos(angle)
        + 0.08
        * np.cos(
            2.0
            * angle
        )
    )


def _validate_window_length(
    length: int,
) -> int:
    """Validate a positive integer window length."""
    if not isinstance(
        length,
        int,
    ):
        raise TypeError(
            "Window length must be an integer."
        )

    if length <= 0:
        raise ValueError(
            "Window length must be positive."
        )

    return length


def apply_window(
    values,
    window: str = "hanning",
) -> np.ndarray:
    """Apply a named window to a signal."""
    signal = _as_real_signal(
        values
    )

    normalized = str(
        window
    ).lower()

    if normalized in {
        "hann",
        "hanning",
    }:
        weights = hanning_window(
            signal.size
        )

    elif normalized == "hamming":
        weights = hamming_window(
            signal.size
        )

    elif normalized == "blackman":
        weights = blackman_window(
            signal.size
        )

    else:
        raise ValueError(
            "window must be 'hanning', 'hamming', or 'blackman'."
        )

    return (
        signal
        * weights
    )


# Common alternate spelling.
hann_window = hanning_window