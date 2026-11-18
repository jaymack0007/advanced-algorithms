"""Tests for Week 12 animation helpers."""

from matplotlib.animation import FuncAnimation
import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.signal.generators import (
    multi_tone,
    sine_wave,
)
from FFTAnalyzer.fft_analyzer.visualization.animations import (
    animate_fft_build,
    animate_frequency_filter,
    close_animation,
)


pytestmark = pytest.mark.filterwarnings(
    "ignore:Animation was deleted without rendering anything.*:UserWarning"
)


def test_fft_animation_returns_figure_and_animation():
    signal = sine_wave(
        10,
        1.0,
        128,
    )

    figure, animation = animate_fft_build(
        signal,
        128,
        frames=5,
    )

    assert figure is not None
    assert isinstance(
        animation,
        FuncAnimation,
    )

    close_animation(
        figure
    )


def test_fft_animation_frame_count():
    signal = sine_wave(
        10,
        1.0,
        128,
    )

    figure, animation = animate_fft_build(
        signal,
        128,
        frames=7,
    )

    frame_sequence = list(
        animation.new_frame_seq()
    )

    assert len(
        frame_sequence
    ) == 7

    close_animation(
        figure
    )


def test_fft_animation_invalid_frames():
    with pytest.raises(ValueError):
        animate_fft_build(
            np.ones(
                32
            ),
            128,
            frames=1,
        )


def test_fft_animation_invalid_interval():
    with pytest.raises(ValueError):
        animate_fft_build(
            np.ones(
                32
            ),
            128,
            interval=0,
        )


def test_filter_animation_returns_figure_and_animation():
    signal = multi_tone(
        [
            10,
            40,
        ],
        1.0,
        128,
    )

    figure, animation = animate_frequency_filter(
        signal,
        128,
        frames=5,
    )

    assert figure is not None
    assert isinstance(
        animation,
        FuncAnimation,
    )

    close_animation(
        figure
    )


def test_filter_animation_frame_count():
    signal = sine_wave(
        10,
        1.0,
        128,
    )

    figure, animation = animate_frequency_filter(
        signal,
        128,
        frames=6,
    )

    frame_sequence = list(
        animation.new_frame_seq()
    )

    assert len(
        frame_sequence
    ) == 6

    close_animation(
        figure
    )


def test_filter_animation_non_power_two_signal():
    signal = sine_wave(
        10,
        1.0,
        100,
    )

    figure, animation = animate_frequency_filter(
        signal,
        100,
        frames=5,
    )

    assert isinstance(
        animation,
        FuncAnimation,
    )

    close_animation(
        figure
    )


def test_filter_animation_invalid_frames():
    with pytest.raises(ValueError):
        animate_frequency_filter(
            np.ones(
                32
            ),
            128,
            frames=1,
        )


def test_filter_animation_invalid_interval():
    with pytest.raises(ValueError):
        animate_frequency_filter(
            np.ones(
                32
            ),
            128,
            interval=0,
        )


def test_empty_signal_rejected():
    with pytest.raises(ValueError):
        animate_fft_build(
            [],
            128,
        )


def test_multidimensional_signal_rejected():
    with pytest.raises(ValueError):
        animate_frequency_filter(
            [
                [1, 2],
                [3, 4],
            ],
            128,
        )


def test_invalid_sample_rate_rejected():
    with pytest.raises(ValueError):
        animate_fft_build(
            np.ones(
                32
            ),
            0,
        )