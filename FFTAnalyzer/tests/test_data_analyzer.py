"""Tests for Week 12 time-series analysis workflows."""

import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.applications.data_analyzer import (
    analyze_time_series,
    autocorrelation,
    dominant_period,
    moving_average,
    periodic_frequencies,
    seasonality_strength,
)


def test_moving_average_preserves_length():
    values = np.arange(
        10,
        dtype=float,
    )

    result = moving_average(
        values,
        3,
    )

    assert len(
        result
    ) == len(
        values
    )


def test_moving_average_known_center():
    values = np.array(
        [
            1,
            2,
            3,
            4,
            5,
        ],
        dtype=float,
    )

    result = moving_average(
        values,
        3,
    )

    assert result[
        2
    ] == pytest.approx(
        3.0
    )


def test_moving_average_reduces_noise():
    rng = np.random.default_rng(
        2026
    )

    values = rng.normal(
        size=1000
    )

    smoothed = moving_average(
        values,
        11,
    )

    assert np.std(
        smoothed
    ) < np.std(
        values
    )


def test_moving_average_window_one():
    values = np.array(
        [
            1,
            2,
            3,
        ],
        dtype=float,
    )

    assert np.allclose(
        moving_average(
            values,
            1,
        ),
        values,
    )


def test_moving_average_invalid_window():
    with pytest.raises(ValueError):
        moving_average(
            [
                1,
                2,
                3,
            ],
            0,
        )


def test_moving_average_window_too_large():
    with pytest.raises(ValueError):
        moving_average(
            [
                1,
                2,
                3,
            ],
            4,
        )


def test_autocorrelation_zero_lag_one():
    values = np.array(
        [
            1,
            2,
            3,
            4,
        ],
        dtype=float,
    )

    result = autocorrelation(
        values
    )

    assert result[
        0
    ] == pytest.approx(
        1.0
    )


def test_autocorrelation_length():
    values = np.arange(
        20,
        dtype=float,
    )

    result = autocorrelation(
        values,
        max_lag=5,
    )

    assert len(
        result
    ) == 6


def test_autocorrelation_matches_numpy():
    values = np.array(
        [
            1,
            3,
            2,
            5,
            4,
        ],
        dtype=float,
    )

    centered = (
        values
        - np.mean(
            values
        )
    )

    expected = np.correlate(
        centered,
        centered,
        mode="full",
    )[
        len(values) - 1:
    ]

    expected = (
        expected
        / expected[
            0
        ]
    )

    result = autocorrelation(
        values,
        normalize=True,
    )

    assert np.allclose(
        result,
        expected,
        atol=1e-10,
    )


def test_autocorrelation_unnormalized():
    values = np.array(
        [
            1,
            2,
            3,
        ],
        dtype=float,
    )

    result = autocorrelation(
        values,
        normalize=False,
    )

    assert result[
        0
    ] == pytest.approx(
        2.0
    )


def test_autocorrelation_invalid_lag():
    with pytest.raises(ValueError):
        autocorrelation(
            [
                1,
                2,
                3,
            ],
            max_lag=3,
        )


def test_periodic_frequencies_detect_sine():
    sample_rate = 128
    sample_count = 128

    time = (
        np.arange(
            sample_count
        )
        / sample_rate
    )

    signal = np.sin(
        2
        * np.pi
        * 8
        * time
    )

    peaks = periodic_frequencies(
        signal,
        sample_rate=sample_rate,
        count=1,
    )

    assert peaks[
        0
    ][
        0
    ] == pytest.approx(
        8.0
    )


def test_periodic_frequencies_multiple_cycles():
    sample_rate = 256
    time = (
        np.arange(
            256
        )
        / sample_rate
    )

    signal = (
        np.sin(
            2
            * np.pi
            * 10
            * time
        )
        + 0.5
        * np.sin(
            2
            * np.pi
            * 30
            * time
        )
    )

    peaks = periodic_frequencies(
        signal,
        sample_rate=sample_rate,
        count=2,
    )

    frequencies = {
        round(
            frequency
        )
        for frequency, _ in peaks
    }

    assert frequencies == {
        10,
        30,
    }


def test_dominant_period_known_cycle():
    sample_rate = 100
    time = (
        np.arange(
            200
        )
        / sample_rate
    )

    signal = np.sin(
        2
        * np.pi
        * 5
        * time
    )

    period = dominant_period(
        signal,
        sample_rate=sample_rate,
    )

    assert period == pytest.approx(
        0.2
    )


def test_seasonality_strength_repeating_pattern():
    pattern = np.array(
        [
            1,
            2,
            3,
            4,
        ],
        dtype=float,
    )

    values = np.tile(
        pattern,
        20,
    )

    strength = seasonality_strength(
        values,
        4,
    )

    assert strength > 0.9


def test_seasonality_strength_invalid_period():
    with pytest.raises(ValueError):
        seasonality_strength(
            [
                1,
                2,
                3,
            ],
            3,
        )


def test_analyze_time_series_keys():
    values = np.sin(
        np.linspace(
            0,
            8 * np.pi,
            128,
        )
    )

    result = analyze_time_series(
        values,
        smoothing_window=5,
    )

    assert set(
        result
    ) == {
        "smoothed",
        "autocorrelation",
        "spectral_peaks",
        "dominant_period",
        "mean",
        "standard_deviation",
    }


def test_analyze_time_series_smoothed_length():
    values = np.arange(
        50,
        dtype=float,
    )

    result = analyze_time_series(
        values,
        smoothing_window=5,
    )

    assert len(
        result[
            "smoothed"
        ]
    ) == 50


def test_analyze_time_series_statistics():
    values = np.array(
        [
            1,
            2,
            3,
            4,
        ],
        dtype=float,
    )

    result = analyze_time_series(
        values,
        smoothing_window=3,
    )

    assert result[
        "mean"
    ] == pytest.approx(
        2.5
    )

    assert result[
        "standard_deviation"
    ] == pytest.approx(
        np.std(
            values
        )
    )


def test_empty_series_rejected():
    with pytest.raises(ValueError):
        moving_average(
            [],
            1,
        )


def test_multidimensional_series_rejected():
    with pytest.raises(ValueError):
        autocorrelation(
            [
                [1, 2],
                [3, 4],
            ]
        )


def test_non_numeric_series_rejected():
    with pytest.raises(TypeError):
        periodic_frequencies(
            [
                "a",
                "b",
            ]
        )