"""Time-series analysis workflows for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import math

import numpy as np

from FFTAnalyzer.fft_analyzer.core.fft import (
    ifft,
    iterative_fft,
    linear_convolution,
    next_power_of_two,
)
from FFTAnalyzer.fft_analyzer.signal.analysis import (
    detect_peak_frequencies,
)


def _as_series(values) -> np.ndarray:
    """Convert input to a non-empty one-dimensional floating-point series."""
    try:
        series = np.asarray(
            values,
            dtype=float,
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Time series must contain numeric values."
        ) from exc

    if series.ndim != 1:
        raise ValueError(
            "Time series must be one-dimensional."
        )

    if series.size == 0:
        raise ValueError(
            "Time series cannot be empty."
        )

    if not np.all(
        np.isfinite(series)
    ):
        raise ValueError(
            "Time series must contain finite values."
        )

    return series.copy()


def moving_average(
    values,
    window_size: int = 5,
) -> np.ndarray:
    """
    Smooth a time series with convolution.

    The returned result uses "same" alignment and therefore has the
    same length as the original series.
    """
    series = _as_series(
        values
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

    if window_size > series.size:
        raise ValueError(
            "window_size cannot exceed the series length."
        )

    kernel = np.ones(
        window_size,
        dtype=float,
    ) / window_size

    full = linear_convolution(
        series,
        kernel,
    )

    start = (
        window_size - 1
    ) // 2

    return np.asarray(
        full[
            start:
            start + series.size
        ],
        dtype=float,
    )


def autocorrelation(
    values,
    *,
    max_lag: int | None = None,
    normalize: bool = True,
) -> np.ndarray:
    """
    Compute nonnegative-lag autocorrelation using the FFT.

    The series mean is removed first. Zero padding prevents circular
    wraparound from contaminating the requested linear autocorrelation.
    """
    series = _as_series(
        values
    )

    n = series.size

    if max_lag is None:
        maximum = (
            n - 1
        )
    else:
        if not isinstance(
            max_lag,
            int,
        ):
            raise TypeError(
                "max_lag must be an integer."
            )

        if (
            max_lag < 0
            or max_lag >= n
        ):
            raise ValueError(
                "max_lag must be between 0 and len(series) - 1."
            )

        maximum = max_lag

    centered = (
        series
        - np.mean(
            series
        )
    )

    transform_length = (
        next_power_of_two(
            2 * n
        )
    )

    padded = np.zeros(
        transform_length,
        dtype=complex,
    )

    padded[
        :n
    ] = centered

    spectrum = iterative_fft(
        padded
    )

    power = (
        spectrum
        * np.conjugate(
            spectrum
        )
    )

    correlation = np.real(
        ifft(
            power
        )
    )[
        :maximum + 1
    ]

    if normalize:
        zero_lag = float(
            correlation[
                0
            ]
        )

        if abs(
            zero_lag
        ) > 1e-15:
            correlation = (
                correlation
                / zero_lag
            )
        else:
            correlation = np.zeros_like(
                correlation
            )

            correlation[
                0
            ] = 1.0

    return correlation


def periodic_frequencies(
    values,
    *,
    sample_rate: float = 1.0,
    count: int = 3,
    min_frequency: float | None = None,
    max_frequency: float | None = None,
) -> list[tuple[float, float]]:
    """
    Return the strongest non-DC periodic frequencies.

    This is useful for seasonality detection in time-series data.
    """
    series = _as_series(
        values
    )

    try:
        rate = float(
            sample_rate
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "sample_rate must be numeric."
        ) from exc

    if (
        not math.isfinite(
            rate
        )
        or rate <= 0
    ):
        raise ValueError(
            "sample_rate must be positive and finite."
        )

    if min_frequency is None:
        minimum = (
            rate
            / max(
                series.size,
                1,
            )
        )
    else:
        minimum = float(
            min_frequency
        )

    return detect_peak_frequencies(
        series,
        rate,
        count=count,
        min_frequency=minimum,
        max_frequency=max_frequency,
        window="hanning",
    )


def dominant_period(
    values,
    *,
    sample_rate: float = 1.0,
) -> float:
    """
    Estimate the strongest repeating period.

    The FFT first supplies an approximate dominant frequency. The
    estimate is then refined with autocorrelation so that a repeating
    cycle can be aligned to the nearest sample lag.

    The returned period uses the same time units represented by
    sample_rate.
    """
    series = _as_series(
        values
    )

    try:
        rate = float(
            sample_rate
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "sample_rate must be numeric."
        ) from exc

    if (
        not math.isfinite(
            rate
        )
        or rate <= 0
    ):
        raise ValueError(
            "sample_rate must be positive and finite."
        )

    peaks = periodic_frequencies(
        series,
        sample_rate=rate,
        count=1,
    )

    if not peaks:
        raise ValueError(
            "No periodic frequency was detected."
        )

    frequency = peaks[
        0
    ][
        0
    ]

    if frequency <= 0:
        raise ValueError(
            "Dominant frequency must be greater than zero."
        )

    approximate_lag = (
        rate
        / frequency
    )

    search_radius = max(
        2,
        int(
            round(
                approximate_lag
                * 0.20
            )
        ),
    )

    minimum_lag = max(
        1,
        int(
            math.floor(
                approximate_lag
            )
        )
        - search_radius,
    )

    maximum_lag = min(
        series.size - 1,
        int(
            math.ceil(
                approximate_lag
            )
        )
        + search_radius,
    )

    correlation = autocorrelation(
        series,
        max_lag=maximum_lag,
        normalize=True,
    )

    best_lag = max(
        range(
            minimum_lag,
            maximum_lag + 1,
        ),
        key=lambda lag: correlation[
            lag
        ],
    )

    return float(
        best_lag
        / rate
    )


def seasonality_strength(
    values,
    period: int,
) -> float:
    """
    Estimate seasonality strength using autocorrelation at a given lag.

    Values near 1 indicate strong positive repetition at that period.
    Values near 0 indicate weak repetition.
    Negative values indicate inverse repetition.
    """
    series = _as_series(
        values
    )

    if not isinstance(
        period,
        int,
    ):
        raise TypeError(
            "period must be an integer."
        )

    if (
        period <= 0
        or period >= series.size
    ):
        raise ValueError(
            "period must be between 1 and len(series) - 1."
        )

    correlation = autocorrelation(
        series,
        max_lag=period,
        normalize=True,
    )

    return float(
        correlation[
            period
        ]
    )


def analyze_time_series(
    values,
    *,
    sample_rate: float = 1.0,
    smoothing_window: int = 5,
    peak_count: int = 3,
) -> dict[str, object]:
    """
    Run a compact time-series analysis workflow.

    Returns smoothed data, autocorrelation, spectral peaks, and an
    estimated dominant period.
    """
    series = _as_series(
        values
    )

    smoothed = moving_average(
        series,
        smoothing_window,
    )

    correlation = autocorrelation(
        series,
        max_lag=min(
            series.size - 1,
            max(
                1,
                series.size // 4,
            ),
        ),
    )

    peaks = periodic_frequencies(
        series,
        sample_rate=sample_rate,
        count=peak_count,
    )

    period = None

    if peaks:
        try:
            period = dominant_period(
                series,
                sample_rate=sample_rate,
            )
        except ValueError:
            period = None

    return {
        "smoothed": smoothed,
        "autocorrelation": correlation,
        "spectral_peaks": peaks,
        "dominant_period": period,
        "mean": float(
            np.mean(
                series
            )
        ),
        "standard_deviation": float(
            np.std(
                series
            )
        ),
    }