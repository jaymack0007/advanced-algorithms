"""Tests for Week 12 FFT-based signal filters."""

import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.core.fft import (
    iterative_fft,
)
from FFTAnalyzer.fft_analyzer.signal.filters import (
    apply_window,
    band_pass_filter,
    blackman_window,
    hamming_window,
    hann_window,
    hanning_window,
    high_pass_filter,
    low_pass_filter,
)
from FFTAnalyzer.fft_analyzer.signal.generators import (
    multi_tone,
    sine_wave,
)


SAMPLE_RATE = 1024
DURATION = 1.0


def _frequency_amplitude(
    signal,
    frequency,
):
    spectrum = iterative_fft(
        signal
    )

    return float(
        np.abs(
            spectrum[
                int(frequency)
            ]
        )
    )


def test_low_pass_preserves_length():
    signal = sine_wave(
        40,
        DURATION,
        SAMPLE_RATE,
    )

    result = low_pass_filter(
        signal,
        SAMPLE_RATE,
        100,
    )

    assert len(
        result
    ) == len(
        signal
    )


def test_low_pass_preserves_low_frequency():
    signal = sine_wave(
        40,
        DURATION,
        SAMPLE_RATE,
    )

    result = low_pass_filter(
        signal,
        SAMPLE_RATE,
        100,
    )

    assert np.allclose(
        result,
        signal,
        atol=1e-10,
    )


def test_low_pass_removes_high_frequency():
    signal = sine_wave(
        300,
        DURATION,
        SAMPLE_RATE,
    )

    result = low_pass_filter(
        signal,
        SAMPLE_RATE,
        100,
    )

    assert np.max(
        np.abs(
            result
        )
    ) < 1e-10


def test_low_pass_mixed_signal():
    signal = multi_tone(
        [
            40,
            300,
        ],
        DURATION,
        SAMPLE_RATE,
    )

    result = low_pass_filter(
        signal,
        SAMPLE_RATE,
        100,
    )

    assert _frequency_amplitude(
        result,
        40,
    ) > 400

    assert _frequency_amplitude(
        result,
        300,
    ) < 1e-8


def test_high_pass_preserves_high_frequency():
    signal = sine_wave(
        300,
        DURATION,
        SAMPLE_RATE,
    )

    result = high_pass_filter(
        signal,
        SAMPLE_RATE,
        100,
    )

    assert np.allclose(
        result,
        signal,
        atol=1e-10,
    )


def test_high_pass_removes_low_frequency():
    signal = sine_wave(
        40,
        DURATION,
        SAMPLE_RATE,
    )

    result = high_pass_filter(
        signal,
        SAMPLE_RATE,
        100,
    )

    assert np.max(
        np.abs(
            result
        )
    ) < 1e-10


def test_high_pass_mixed_signal():
    signal = multi_tone(
        [
            40,
            300,
        ],
        DURATION,
        SAMPLE_RATE,
    )

    result = high_pass_filter(
        signal,
        SAMPLE_RATE,
        100,
    )

    assert _frequency_amplitude(
        result,
        40,
    ) < 1e-8

    assert _frequency_amplitude(
        result,
        300,
    ) > 400


def test_band_pass_keeps_middle_frequency():
    signal = multi_tone(
        [
            40,
            150,
            300,
        ],
        DURATION,
        SAMPLE_RATE,
    )

    result = band_pass_filter(
        signal,
        SAMPLE_RATE,
        100,
        200,
    )

    assert _frequency_amplitude(
        result,
        40,
    ) < 1e-8

    assert _frequency_amplitude(
        result,
        150,
    ) > 400

    assert _frequency_amplitude(
        result,
        300,
    ) < 1e-8


def test_band_pass_preserves_length():
    signal = sine_wave(
        150,
        DURATION,
        SAMPLE_RATE,
    )

    result = band_pass_filter(
        signal,
        SAMPLE_RATE,
        100,
        200,
    )

    assert len(
        result
    ) == len(
        signal
    )


def test_filter_non_power_of_two_length():
    signal = sine_wave(
        50,
        1.0,
        1000,
    )

    result = low_pass_filter(
        signal,
        1000,
        100,
    )

    assert len(
        result
    ) == 1000

    assert np.all(
        np.isfinite(
            result
        )
    )


def test_zero_signal_remains_zero():
    signal = np.zeros(
        128
    )

    result = low_pass_filter(
        signal,
        128,
        20,
    )

    assert np.allclose(
        result,
        0,
    )


def test_invalid_sample_rate_rejected():
    with pytest.raises(ValueError):
        low_pass_filter(
            [
                1,
                2,
            ],
            0,
            1,
        )


def test_negative_cutoff_rejected():
    with pytest.raises(ValueError):
        low_pass_filter(
            [
                1,
                2,
            ],
            100,
            -1,
        )


def test_cutoff_above_nyquist_rejected():
    with pytest.raises(ValueError):
        high_pass_filter(
            [
                1,
                2,
            ],
            100,
            60,
        )


def test_band_pass_invalid_order_rejected():
    with pytest.raises(ValueError):
        band_pass_filter(
            [
                1,
                2,
                3,
                4,
            ],
            100,
            30,
            20,
        )


def test_empty_signal_rejected():
    with pytest.raises(ValueError):
        low_pass_filter(
            [],
            100,
            20,
        )


def test_multidimensional_signal_rejected():
    with pytest.raises(ValueError):
        low_pass_filter(
            [
                [1, 2],
                [3, 4],
            ],
            100,
            20,
        )


def test_hanning_window_length():
    window = hanning_window(
        16
    )

    assert len(
        window
    ) == 16


def test_hanning_window_endpoints():
    window = hanning_window(
        16
    )

    assert window[
        0
    ] == pytest.approx(
        0.0
    )

    assert window[
        -1
    ] == pytest.approx(
        0.0
    )


def test_hanning_window_symmetry():
    window = hanning_window(
        17
    )

    assert np.allclose(
        window,
        window[::-1],
    )


def test_hann_alias():
    assert np.allclose(
        hann_window(
            16
        ),
        hanning_window(
            16
        ),
    )


def test_hamming_window_endpoints():
    window = hamming_window(
        16
    )

    assert window[
        0
    ] == pytest.approx(
        0.08
    )

    assert window[
        -1
    ] == pytest.approx(
        0.08
    )


def test_hamming_window_symmetry():
    window = hamming_window(
        17
    )

    assert np.allclose(
        window,
        window[::-1],
    )


def test_blackman_window_endpoints_near_zero():
    window = blackman_window(
        16
    )

    assert abs(
        window[
            0
        ]
    ) < 1e-12

    assert abs(
        window[
            -1
        ]
    ) < 1e-12


def test_blackman_window_symmetry():
    window = blackman_window(
        17
    )

    assert np.allclose(
        window,
        window[::-1],
    )


def test_single_value_windows():
    assert np.allclose(
        hanning_window(
            1
        ),
        [
            1
        ],
    )

    assert np.allclose(
        hamming_window(
            1
        ),
        [
            1
        ],
    )

    assert np.allclose(
        blackman_window(
            1
        ),
        [
            1
        ],
    )


def test_invalid_window_length_rejected():
    with pytest.raises(ValueError):
        hanning_window(
            0
        )


def test_noninteger_window_length_rejected():
    with pytest.raises(TypeError):
        hamming_window(
            4.5
        )


def test_apply_hanning_window():
    signal = np.ones(
        8
    )

    result = apply_window(
        signal,
        "hanning",
    )

    assert np.allclose(
        result,
        hanning_window(
            8
        ),
    )


def test_apply_hamming_window():
    signal = np.ones(
        8
    )

    result = apply_window(
        signal,
        "hamming",
    )

    assert np.allclose(
        result,
        hamming_window(
            8
        ),
    )


def test_apply_blackman_window():
    signal = np.ones(
        8
    )

    result = apply_window(
        signal,
        "blackman",
    )

    assert np.allclose(
        result,
        blackman_window(
            8
        ),
    )


def test_apply_window_invalid_name():
    with pytest.raises(ValueError):
        apply_window(
            np.ones(
                8
            ),
            "triangle",
        )