"""Tests for Week 12 signal generators."""

import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.signal.generators import (
    chirp_signal,
    multi_tone,
    pink_noise,
    sample_count,
    sine_wave,
    time_axis,
    white_noise,
)


def test_sample_count():
    assert sample_count(
        1.0,
        1000,
    ) == 1000


def test_sample_count_fractional_duration():
    assert sample_count(
        0.5,
        1000,
    ) == 500


def test_invalid_duration_rejected():
    with pytest.raises(ValueError):
        sample_count(
            0,
            1000,
        )


def test_invalid_sample_rate_rejected():
    with pytest.raises(ValueError):
        sample_count(
            1,
            0,
        )


def test_time_axis_length():
    result = time_axis(
        1.0,
        100,
    )

    assert len(
        result
    ) == 100


def test_time_axis_spacing():
    result = time_axis(
        1.0,
        100,
    )

    assert result[
        1
    ] - result[
        0
    ] == pytest.approx(
        0.01
    )


def test_time_axis_starts_at_zero():
    result = time_axis(
        1.0,
        100,
    )

    assert result[
        0
    ] == 0.0


def test_sine_wave_length():
    signal = sine_wave(
        10,
        1.0,
        1000,
    )

    assert len(
        signal
    ) == 1000


def test_sine_wave_amplitude():
    signal = sine_wave(
        5,
        1.0,
        1000,
        amplitude=2.0,
    )

    assert np.max(
        np.abs(
            signal
        )
    ) == pytest.approx(
        2.0,
        rel=1e-6,
    )


def test_sine_wave_known_samples():
    signal = sine_wave(
        1,
        1.0,
        4,
    )

    assert np.allclose(
        signal,
        [
            0,
            1,
            0,
            -1,
        ],
        atol=1e-12,
    )


def test_sine_phase():
    signal = sine_wave(
        1,
        1.0,
        4,
        phase=np.pi / 2,
    )

    assert signal[
        0
    ] == pytest.approx(
        1.0
    )


def test_sine_frequency_above_nyquist_rejected():
    with pytest.raises(ValueError):
        sine_wave(
            600,
            1.0,
            1000,
        )


def test_negative_amplitude_rejected():
    with pytest.raises(ValueError):
        sine_wave(
            10,
            1.0,
            1000,
            amplitude=-1,
        )


def test_multi_tone_length():
    signal = multi_tone(
        [
            10,
            20,
            30,
        ],
        1.0,
        1000,
    )

    assert len(
        signal
    ) == 1000


def test_multi_tone_equals_sum_of_sines():
    combined = multi_tone(
        [
            10,
            20,
        ],
        1.0,
        1000,
        amplitudes=[
            1.0,
            0.5,
        ],
    )

    expected = (
        sine_wave(
            10,
            1.0,
            1000,
            amplitude=1.0,
        )
        + sine_wave(
            20,
            1.0,
            1000,
            amplitude=0.5,
        )
    )

    assert np.allclose(
        combined,
        expected,
    )


def test_multi_tone_amplitude_count_mismatch():
    with pytest.raises(ValueError):
        multi_tone(
            [
                10,
                20,
            ],
            1.0,
            1000,
            amplitudes=[
                1.0
            ],
        )


def test_multi_tone_phase_count_mismatch():
    with pytest.raises(ValueError):
        multi_tone(
            [
                10,
                20,
            ],
            1.0,
            1000,
            phases=[
                0.0
            ],
        )


def test_multi_tone_requires_frequency():
    with pytest.raises(ValueError):
        multi_tone(
            [],
            1.0,
            1000,
        )


def test_chirp_length():
    signal = chirp_signal(
        10,
        100,
        1.0,
        1000,
    )

    assert len(
        signal
    ) == 1000


def test_chirp_same_start_end_matches_sine():
    chirp = chirp_signal(
        25,
        25,
        1.0,
        1000,
    )

    sine = sine_wave(
        25,
        1.0,
        1000,
    )

    assert np.allclose(
        chirp,
        sine,
        atol=1e-12,
    )


def test_chirp_respects_amplitude():
    signal = chirp_signal(
        10,
        100,
        1.0,
        2000,
        amplitude=0.25,
    )

    assert np.max(
        np.abs(
            signal
        )
    ) <= (
        0.25
        + 1e-12
    )


def test_chirp_invalid_end_frequency():
    with pytest.raises(ValueError):
        chirp_signal(
            10,
            600,
            1.0,
            1000,
        )


def test_white_noise_length():
    noise = white_noise(
        1.0,
        1000,
        seed=1,
    )

    assert len(
        noise
    ) == 1000


def test_white_noise_reproducible():
    first = white_noise(
        1.0,
        1000,
        seed=42,
    )

    second = white_noise(
        1.0,
        1000,
        seed=42,
    )

    assert np.array_equal(
        first,
        second,
    )


def test_white_noise_different_seeds():
    first = white_noise(
        1.0,
        1000,
        seed=1,
    )

    second = white_noise(
        1.0,
        1000,
        seed=2,
    )

    assert not np.array_equal(
        first,
        second,
    )


def test_white_noise_standard_deviation():
    noise = white_noise(
        10.0,
        1000,
        amplitude=2.0,
        seed=2026,
    )

    assert np.std(
        noise
    ) == pytest.approx(
        2.0,
        rel=0.05,
    )


def test_zero_amplitude_white_noise():
    noise = white_noise(
        1.0,
        100,
        amplitude=0,
    )

    assert np.allclose(
        noise,
        0,
    )


def test_pink_noise_length():
    noise = pink_noise(
        1.0,
        1000,
        seed=1,
    )

    assert len(
        noise
    ) == 1000


def test_pink_noise_reproducible():
    first = pink_noise(
        1.0,
        1000,
        seed=99,
    )

    second = pink_noise(
        1.0,
        1000,
        seed=99,
    )

    assert np.array_equal(
        first,
        second,
    )


def test_pink_noise_zero_mean():
    noise = pink_noise(
        2.0,
        1000,
        seed=12,
    )

    assert np.mean(
        noise
    ) == pytest.approx(
        0.0,
        abs=1e-12,
    )


def test_pink_noise_standard_deviation():
    noise = pink_noise(
        2.0,
        1000,
        amplitude=1.5,
        seed=12,
    )

    assert np.std(
        noise
    ) == pytest.approx(
        1.5,
        rel=1e-10,
    )


def test_zero_amplitude_pink_noise():
    noise = pink_noise(
        1.0,
        100,
        amplitude=0,
    )

    assert np.allclose(
        noise,
        0,
    )


def test_invalid_pink_rows():
    with pytest.raises(ValueError):
        pink_noise(
            1.0,
            1000,
            rows=0,
        )