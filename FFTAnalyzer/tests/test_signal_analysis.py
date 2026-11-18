"""Tests for Week 12 spectral analysis tools."""

import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.signal.analysis import (
    detect_peak_frequencies,
    dominant_frequency,
    frequency_axis,
    periodogram,
    power_spectral_density,
    spectrogram,
)
from FFTAnalyzer.fft_analyzer.signal.generators import (
    chirp_signal,
    multi_tone,
    sine_wave,
)


SAMPLE_RATE = 1024
DURATION = 1.0


def test_frequency_axis_length():
    result = frequency_axis(
        1024,
        SAMPLE_RATE,
    )

    assert len(
        result
    ) == 513


def test_frequency_axis_starts_zero():
    result = frequency_axis(
        1024,
        SAMPLE_RATE,
    )

    assert result[
        0
    ] == 0.0


def test_frequency_axis_ends_nyquist():
    result = frequency_axis(
        1024,
        SAMPLE_RATE,
    )

    assert result[
        -1
    ] == pytest.approx(
        SAMPLE_RATE / 2
    )


def test_periodogram_shapes():
    signal = sine_wave(
        50,
        DURATION,
        SAMPLE_RATE,
    )

    frequencies, power = periodogram(
        signal,
        SAMPLE_RATE,
    )

    assert frequencies.shape == power.shape
    assert len(
        frequencies
    ) == 513


def test_periodogram_detects_sine_peak():
    signal = sine_wave(
        50,
        DURATION,
        SAMPLE_RATE,
    )

    frequencies, power = periodogram(
        signal,
        SAMPLE_RATE,
        window="rectangular",
    )

    peak = frequencies[
        np.argmax(
            power
        )
    ]

    assert peak == pytest.approx(
        50.0
    )


def test_periodogram_non_power_of_two_input():
    signal = sine_wave(
        50,
        1.0,
        1000,
    )

    frequencies, power = periodogram(
        signal,
        1000,
    )

    assert len(
        frequencies
    ) == len(
        power
    )

    assert len(
        frequencies
    ) == 513


def test_periodogram_custom_fft_size():
    signal = sine_wave(
        50,
        0.25,
        SAMPLE_RATE,
    )

    frequencies, power = periodogram(
        signal,
        SAMPLE_RATE,
        n_fft=1024,
    )

    assert len(
        frequencies
    ) == 513

    assert len(
        power
    ) == 513


def test_periodogram_rejects_small_fft():
    signal = np.ones(
        512
    )

    with pytest.raises(ValueError):
        periodogram(
            signal,
            SAMPLE_RATE,
            n_fft=256,
        )


def test_periodogram_rejects_non_power_two_fft():
    signal = np.ones(
        100
    )

    with pytest.raises(ValueError):
        periodogram(
            signal,
            SAMPLE_RATE,
            n_fft=300,
        )


def test_psd_shapes():
    signal = sine_wave(
        50,
        DURATION,
        SAMPLE_RATE,
    )

    frequencies, density = (
        power_spectral_density(
            signal,
            SAMPLE_RATE,
        )
    )

    assert frequencies.shape == density.shape


def test_psd_is_nonnegative():
    signal = sine_wave(
        50,
        DURATION,
        SAMPLE_RATE,
    )

    _, density = power_spectral_density(
        signal,
        SAMPLE_RATE,
    )

    assert np.all(
        density >= 0
    )


def test_psd_related_to_periodogram():
    signal = sine_wave(
        50,
        DURATION,
        SAMPLE_RATE,
    )

    _, power = periodogram(
        signal,
        SAMPLE_RATE,
    )

    _, density = power_spectral_density(
        signal,
        SAMPLE_RATE,
    )

    assert np.allclose(
        density,
        power / SAMPLE_RATE,
    )


def test_detect_single_peak():
    signal = sine_wave(
        80,
        DURATION,
        SAMPLE_RATE,
    )

    peaks = detect_peak_frequencies(
        signal,
        SAMPLE_RATE,
        count=1,
        window="rectangular",
    )

    assert peaks[
        0
    ][
        0
    ] == pytest.approx(
        80.0
    )


def test_detect_multiple_peaks():
    signal = multi_tone(
        [
            40,
            120,
            300,
        ],
        DURATION,
        SAMPLE_RATE,
        amplitudes=[
            1.0,
            0.8,
            0.6,
        ],
    )

    peaks = detect_peak_frequencies(
        signal,
        SAMPLE_RATE,
        count=3,
        window="rectangular",
    )

    frequencies = {
        round(
            frequency
        )
        for frequency, _ in peaks
    }

    assert frequencies == {
        40,
        120,
        300,
    }


def test_detect_peak_respects_frequency_range():
    signal = multi_tone(
        [
            40,
            200,
        ],
        DURATION,
        SAMPLE_RATE,
    )

    peaks = detect_peak_frequencies(
        signal,
        SAMPLE_RATE,
        count=1,
        min_frequency=100,
        window="rectangular",
    )

    assert peaks[
        0
    ][
        0
    ] == pytest.approx(
        200.0
    )


def test_detect_peak_count_validation():
    with pytest.raises(ValueError):
        detect_peak_frequencies(
            np.ones(
                128
            ),
            SAMPLE_RATE,
            count=0,
        )


def test_detect_invalid_frequency_range():
    with pytest.raises(ValueError):
        detect_peak_frequencies(
            np.ones(
                128
            ),
            SAMPLE_RATE,
            min_frequency=300,
            max_frequency=100,
        )


def test_dominant_frequency():
    signal = sine_wave(
        75,
        DURATION,
        SAMPLE_RATE,
    )

    result = dominant_frequency(
        signal,
        SAMPLE_RATE,
        window="rectangular",
    )

    assert result == pytest.approx(
        75.0
    )


def test_dominant_frequency_louder_tone():
    signal = multi_tone(
        [
            50,
            200,
        ],
        DURATION,
        SAMPLE_RATE,
        amplitudes=[
            0.2,
            1.0,
        ],
    )

    result = dominant_frequency(
        signal,
        SAMPLE_RATE,
        window="rectangular",
    )

    assert result == pytest.approx(
        200.0
    )


def test_spectrogram_shapes():
    signal = sine_wave(
        50,
        1.0,
        SAMPLE_RATE,
    )

    times, frequencies, power = spectrogram(
        signal,
        SAMPLE_RATE,
        window_size=256,
        hop_size=128,
    )

    assert power.shape[
        0
    ] == len(
        frequencies
    )

    assert power.shape[
        1
    ] == len(
        times
    )


def test_spectrogram_frequency_bins():
    signal = sine_wave(
        50,
        1.0,
        SAMPLE_RATE,
    )

    _, frequencies, _ = spectrogram(
        signal,
        SAMPLE_RATE,
        window_size=256,
        n_fft=256,
    )

    assert len(
        frequencies
    ) == 129


def test_spectrogram_detects_stationary_tone():
    signal = sine_wave(
        64,
        1.0,
        SAMPLE_RATE,
    )

    _, frequencies, power = spectrogram(
        signal,
        SAMPLE_RATE,
        window_size=256,
        hop_size=128,
        window="rectangular",
        n_fft=256,
    )

    average_power = np.mean(
        power,
        axis=1,
    )

    peak_frequency = frequencies[
        np.argmax(
            average_power
        )
    ]

    assert peak_frequency == pytest.approx(
        64.0
    )


def test_spectrogram_chirp_changes_peak():
    signal = chirp_signal(
        40,
        300,
        1.0,
        SAMPLE_RATE,
    )

    _, frequencies, power = spectrogram(
        signal,
        SAMPLE_RATE,
        window_size=128,
        hop_size=64,
        n_fft=128,
    )

    first_peak = frequencies[
        np.argmax(
            power[
                :,
                0,
            ]
        )
    ]

    last_peak = frequencies[
        np.argmax(
            power[
                :,
                -1,
            ]
        )
    ]

    assert last_peak > first_peak


def test_spectrogram_short_signal():
    signal = sine_wave(
        20,
        0.05,
        SAMPLE_RATE,
    )

    times, frequencies, power = spectrogram(
        signal,
        SAMPLE_RATE,
        window_size=128,
    )

    assert len(
        times
    ) == 1

    assert power.shape == (
        len(
            frequencies
        ),
        1,
    )


def test_spectrogram_default_overlap():
    signal = np.ones(
        512
    )

    times, _, _ = spectrogram(
        signal,
        SAMPLE_RATE,
        window_size=128,
    )

    assert len(
        times
    ) > 1


def test_spectrogram_invalid_window_size():
    with pytest.raises(ValueError):
        spectrogram(
            np.ones(
                128
            ),
            SAMPLE_RATE,
            window_size=0,
        )


def test_spectrogram_invalid_hop_size():
    with pytest.raises(ValueError):
        spectrogram(
            np.ones(
                128
            ),
            SAMPLE_RATE,
            window_size=64,
            hop_size=0,
        )


def test_invalid_analysis_window():
    with pytest.raises(ValueError):
        periodogram(
            np.ones(
                128
            ),
            SAMPLE_RATE,
            window="triangle",
        )


def test_empty_signal_rejected():
    with pytest.raises(ValueError):
        periodogram(
            [],
            SAMPLE_RATE,
        )


def test_invalid_sample_rate_rejected():
    with pytest.raises(ValueError):
        periodogram(
            np.ones(
                128
            ),
            0,
        )