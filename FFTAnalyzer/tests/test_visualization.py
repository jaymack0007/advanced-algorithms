"""Tests for Week 12 visualization helpers."""

import matplotlib.pyplot as plt
import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.signal.generators import (
    sine_wave,
)
from FFTAnalyzer.fft_analyzer.visualization.plots import (
    close_figure,
    plot_condition_numbers,
    plot_fft_heatmap,
    plot_fft_spectrum,
    plot_signal_comparison,
    plot_spectrogram,
)


def test_plot_fft_spectrum_returns_figure_axis():
    signal = sine_wave(
        20,
        1.0,
        128,
    )

    figure, axis = plot_fft_spectrum(
        signal,
        128,
    )

    assert figure is not None
    assert axis is not None

    close_figure(
        figure
    )


def test_plot_fft_spectrum_has_labels():
    signal = sine_wave(
        20,
        1.0,
        128,
    )

    figure, axis = plot_fft_spectrum(
        signal,
        128,
    )

    assert axis.get_xlabel() == "Frequency (Hz)"
    assert axis.get_ylabel() == "Power"

    close_figure(
        figure
    )


def test_plot_fft_spectrum_save(tmp_path):
    path = (
        tmp_path
        / "spectrum.png"
    )

    signal = sine_wave(
        20,
        1.0,
        128,
    )

    figure, _ = plot_fft_spectrum(
        signal,
        128,
        save_path=path,
    )

    assert path.exists()

    close_figure(
        figure
    )


def test_plot_spectrogram_returns_figure():
    signal = sine_wave(
        20,
        1.0,
        128,
    )

    figure, axis = plot_spectrogram(
        signal,
        128,
        window_size=32,
    )

    assert figure is not None
    assert axis is not None

    close_figure(
        figure
    )


def test_plot_spectrogram_save(tmp_path):
    path = (
        tmp_path
        / "spectrogram.png"
    )

    signal = sine_wave(
        20,
        1.0,
        128,
    )

    figure, _ = plot_spectrogram(
        signal,
        128,
        window_size=32,
        save_path=path,
    )

    assert path.exists()

    close_figure(
        figure
    )


def test_plot_fft_heatmap_returns_figure():
    image = np.ones(
        (
            8,
            8,
        )
    )

    figure, axis = plot_fft_heatmap(
        image
    )

    assert figure is not None
    assert axis is not None

    close_figure(
        figure
    )


def test_plot_fft_heatmap_handles_non_power_two():
    image = np.ones(
        (
            7,
            9,
        )
    )

    figure, axis = plot_fft_heatmap(
        image
    )

    assert figure is not None
    assert axis is not None

    close_figure(
        figure
    )


def test_plot_fft_heatmap_save(tmp_path):
    path = (
        tmp_path
        / "heatmap.png"
    )

    image = np.ones(
        (
            8,
            8,
        )
    )

    figure, _ = plot_fft_heatmap(
        image,
        save_path=path,
    )

    assert path.exists()

    close_figure(
        figure
    )


def test_plot_fft_heatmap_invalid_dimension():
    with pytest.raises(ValueError):
        plot_fft_heatmap(
            [
                1,
                2,
                3,
            ]
        )


def test_plot_condition_numbers():
    matrices = [
        np.eye(
            2
        ),
        np.array(
            [
                [1, 0],
                [0, 10],
            ],
            dtype=float,
        ),
    ]

    figure, axis, conditions = (
        plot_condition_numbers(
            matrices
        )
    )

    assert len(
        conditions
    ) == 2

    assert conditions[
        0
    ] == pytest.approx(
        1.0
    )

    assert conditions[
        1
    ] == pytest.approx(
        10.0
    )

    close_figure(
        figure
    )


def test_plot_condition_numbers_labels():
    matrices = [
        np.eye(
            2
        ),
        np.eye(
            3
        ),
    ]

    figure, axis, _ = (
        plot_condition_numbers(
            matrices,
            labels=[
                "A",
                "B",
            ],
        )
    )

    labels = [
        item.get_text()
        for item in axis.get_xticklabels()
    ]

    assert labels == [
        "A",
        "B",
    ]

    close_figure(
        figure
    )


def test_plot_condition_numbers_label_mismatch():
    with pytest.raises(ValueError):
        plot_condition_numbers(
            [
                np.eye(
                    2
                ),
                np.eye(
                    2
                ),
            ],
            labels=[
                "Only One"
            ],
        )


def test_plot_condition_numbers_empty():
    with pytest.raises(ValueError):
        plot_condition_numbers(
            []
        )


def test_plot_condition_numbers_save(tmp_path):
    path = (
        tmp_path
        / "conditions.png"
    )

    figure, _, _ = plot_condition_numbers(
        [
            np.eye(
                2
            )
        ],
        save_path=path,
    )

    assert path.exists()

    close_figure(
        figure
    )


def test_signal_comparison_returns_figure():
    original = np.array(
        [
            1,
            2,
            3,
            4,
        ],
        dtype=float,
    )

    processed = np.array(
        [
            1,
            1.5,
            2.5,
            4,
        ],
        dtype=float,
    )

    figure, axis = plot_signal_comparison(
        original,
        processed,
    )

    assert figure is not None
    assert axis is not None

    close_figure(
        figure
    )


def test_signal_comparison_two_lines():
    original = np.arange(
        10,
        dtype=float,
    )

    processed = original * 0.5

    figure, axis = plot_signal_comparison(
        original,
        processed,
    )

    assert len(
        axis.lines
    ) == 2

    close_figure(
        figure
    )


def test_signal_comparison_length_mismatch():
    with pytest.raises(ValueError):
        plot_signal_comparison(
            [
                1,
                2,
            ],
            [
                1,
            ],
        )


def test_signal_comparison_invalid_rate():
    with pytest.raises(ValueError):
        plot_signal_comparison(
            [
                1,
                2,
            ],
            [
                1,
                2,
            ],
            sample_rate=0,
        )


def test_close_figure():
    figure = plt.figure()

    number = figure.number

    close_figure(
        figure
    )

    assert not plt.fignum_exists(
        number
    )