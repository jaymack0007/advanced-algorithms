"""Tests for Week 12 audio processing workflows."""

import numpy as np
import pytest
from scipy.io import wavfile

from FFTAnalyzer.fft_analyzer.applications.audio_processor import (
    analyze_audio,
    audio_spectrogram,
    filter_audio,
    load_wav,
    process_wav,
    save_wav,
)
from FFTAnalyzer.fft_analyzer.signal.generators import (
    multi_tone,
    sine_wave,
)


def test_filter_audio_low_pass():
    sample_rate = 1024

    signal = multi_tone(
        [
            50,
            300,
        ],
        1.0,
        sample_rate,
    )

    filtered = filter_audio(
        signal,
        sample_rate,
        filter_type="low-pass",
        cutoff=100,
    )

    expected = sine_wave(
        50,
        1.0,
        sample_rate,
    )

    assert np.allclose(
        filtered,
        expected,
        atol=1e-10,
    )


def test_filter_audio_high_pass():
    sample_rate = 1024

    signal = multi_tone(
        [
            50,
            300,
        ],
        1.0,
        sample_rate,
    )

    filtered = filter_audio(
        signal,
        sample_rate,
        filter_type="high-pass",
        cutoff=100,
    )

    expected = sine_wave(
        300,
        1.0,
        sample_rate,
    )

    assert np.allclose(
        filtered,
        expected,
        atol=1e-10,
    )


def test_filter_audio_band_pass():
    sample_rate = 1024

    signal = multi_tone(
        [
            50,
            150,
            300,
        ],
        1.0,
        sample_rate,
    )

    filtered = filter_audio(
        signal,
        sample_rate,
        filter_type="band-pass",
        low_cutoff=100,
        high_cutoff=200,
    )

    expected = sine_wave(
        150,
        1.0,
        sample_rate,
    )

    assert np.allclose(
        filtered,
        expected,
        atol=1e-10,
    )


def test_low_pass_requires_cutoff():
    with pytest.raises(ValueError):
        filter_audio(
            np.ones(
                128
            ),
            128,
            filter_type="low-pass",
        )


def test_band_pass_requires_cutoffs():
    with pytest.raises(ValueError):
        filter_audio(
            np.ones(
                128
            ),
            128,
            filter_type="band-pass",
        )


def test_invalid_filter_type():
    with pytest.raises(ValueError):
        filter_audio(
            np.ones(
                128
            ),
            128,
            filter_type="not-a-filter",
        )


def test_audio_spectrogram_shapes():
    signal = sine_wave(
        32,
        1.0,
        256,
    )

    times, frequencies, power = audio_spectrogram(
        signal,
        256,
        window_size=64,
        hop_size=32,
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


def test_analyze_audio_keys():
    signal = sine_wave(
        40,
        1.0,
        256,
    )

    result = analyze_audio(
        signal,
        256,
    )

    assert set(
        result
    ) == {
        "duration_seconds",
        "peak_amplitude",
        "rms_amplitude",
        "dominant_frequency",
    }


def test_analyze_audio_duration():
    signal = sine_wave(
        40,
        2.0,
        256,
    )

    result = analyze_audio(
        signal,
        256,
    )

    assert result[
        "duration_seconds"
    ] == pytest.approx(
        2.0
    )


def test_analyze_audio_frequency():
    signal = sine_wave(
        40,
        1.0,
        256,
    )

    result = analyze_audio(
        signal,
        256,
    )

    assert result[
        "dominant_frequency"
    ] == pytest.approx(
        40.0
    )


def test_analyze_audio_peak():
    signal = sine_wave(
        10,
        1.0,
        100,
        amplitude=0.5,
    )

    result = analyze_audio(
        signal,
        100,
    )

    assert result[
        "peak_amplitude"
    ] == pytest.approx(
        0.4755282581,
        rel=1e-6,
    )


def test_save_and_load_wav_round_trip(tmp_path):
    path = (
        tmp_path
        / "test.wav"
    )

    sample_rate = 8000

    signal = sine_wave(
        440,
        0.1,
        sample_rate,
        amplitude=0.5,
    )

    save_wav(
        path,
        sample_rate,
        signal,
    )

    loaded_rate, loaded = load_wav(
        path
    )

    assert loaded_rate == sample_rate
    assert len(
        loaded
    ) == len(
        signal
    )

    assert np.allclose(
        loaded,
        signal,
        atol=5e-5,
    )


def test_save_wav_creates_int16_file(tmp_path):
    path = (
        tmp_path
        / "test.wav"
    )

    save_wav(
        path,
        8000,
        np.array(
            [
                -1.0,
                0.0,
                1.0,
            ]
        ),
    )

    _, data = wavfile.read(
        path
    )

    assert data.dtype == np.int16


def test_save_wav_clips_values(tmp_path):
    path = (
        tmp_path
        / "clip.wav"
    )

    save_wav(
        path,
        8000,
        np.array(
            [
                -2.0,
                2.0,
            ]
        ),
    )

    _, data = wavfile.read(
        path
    )

    assert data[
        0
    ] == -32767

    assert data[
        1
    ] == 32767


def test_load_stereo_converts_to_mono(tmp_path):
    path = (
        tmp_path
        / "stereo.wav"
    )

    left = np.array(
        [
            1000,
            2000,
            3000,
        ],
        dtype=np.int16,
    )

    right = np.array(
        [
            3000,
            4000,
            5000,
        ],
        dtype=np.int16,
    )

    stereo = np.column_stack(
        (
            left,
            right,
        )
    )

    wavfile.write(
        path,
        8000,
        stereo,
    )

    _, loaded = load_wav(
        path
    )

    expected = np.array(
        [
            2000,
            3000,
            4000,
        ],
        dtype=float,
    )

    expected /= 32768.0

    assert np.allclose(
        loaded,
        expected,
    )


def test_load_missing_file():
    with pytest.raises(FileNotFoundError):
        load_wav(
            "definitely_missing_file.wav"
        )


def test_process_wav(tmp_path):
    input_path = (
        tmp_path
        / "input.wav"
    )

    output_path = (
        tmp_path
        / "output.wav"
    )

    sample_rate = 1024

    signal = multi_tone(
        [
            50,
            300,
        ],
        1.0,
        sample_rate,
        amplitudes=[
            0.4,
            0.4,
        ],
    )

    save_wav(
        input_path,
        sample_rate,
        signal,
    )

    result = process_wav(
        input_path,
        output_path,
        filter_type="low-pass",
        cutoff=100,
    )

    assert output_path.exists()

    assert result[
        "sample_rate"
    ] == sample_rate

    assert result[
        "input_samples"
    ] == sample_rate

    assert result[
        "output_samples"
    ] == sample_rate


def test_process_wav_output_is_filtered(tmp_path):
    input_path = (
        tmp_path
        / "input.wav"
    )

    output_path = (
        tmp_path
        / "output.wav"
    )

    sample_rate = 1024

    signal = multi_tone(
        [
            50,
            300,
        ],
        1.0,
        sample_rate,
        amplitudes=[
            0.4,
            0.4,
        ],
    )

    save_wav(
        input_path,
        sample_rate,
        signal,
    )

    process_wav(
        input_path,
        output_path,
        filter_type="low-pass",
        cutoff=100,
    )

    loaded_rate, filtered = load_wav(
        output_path
    )

    result = analyze_audio(
        filtered,
        loaded_rate,
    )

    assert result[
        "dominant_frequency"
    ] == pytest.approx(
        50.0
    )


def test_empty_audio_rejected():
    with pytest.raises(ValueError):
        analyze_audio(
            [],
            100,
        )


def test_multichannel_array_rejected():
    with pytest.raises(ValueError):
        filter_audio(
            np.ones(
                (
                    10,
                    2,
                )
            ),
            100,
            filter_type="low-pass",
            cutoff=20,
        )