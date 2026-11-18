"""Tests for Week 12 Fast Fourier Transform algorithms."""

import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.core.fft import (
    bit_reversal_permutation,
    circular_convolution,
    direct_dft,
    fft,
    ifft,
    is_power_of_two,
    iterative_fft,
    linear_convolution,
    next_power_of_two,
    recursive_fft,
)


def test_is_power_of_two_true():
    assert is_power_of_two(
        1
    )

    assert is_power_of_two(
        2
    )

    assert is_power_of_two(
        1024
    )


def test_is_power_of_two_false():
    assert not is_power_of_two(
        0
    )

    assert not is_power_of_two(
        3
    )

    assert not is_power_of_two(
        1000
    )


def test_next_power_of_two_exact():
    assert next_power_of_two(
        16
    ) == 16


def test_next_power_of_two_rounds_up():
    assert next_power_of_two(
        17
    ) == 32


def test_next_power_of_two_one():
    assert next_power_of_two(
        1
    ) == 1


def test_next_power_of_two_invalid_value():
    with pytest.raises(ValueError):
        next_power_of_two(
            0
        )


def test_bit_reversal_length_eight():
    result = (
        bit_reversal_permutation(
            8
        )
    )

    assert result.tolist() == [
        0,
        4,
        2,
        6,
        1,
        5,
        3,
        7,
    ]


def test_bit_reversal_length_one():
    result = (
        bit_reversal_permutation(
            1
        )
    )

    assert result.tolist() == [
        0
    ]


def test_bit_reversal_non_power_of_two_rejected():
    with pytest.raises(ValueError):
        bit_reversal_permutation(
            6
        )


def test_recursive_fft_single_value():
    result = recursive_fft(
        [5]
    )

    assert np.allclose(
        result,
        [5],
    )


def test_recursive_fft_matches_numpy_length_two():
    values = np.array(
        [
            1,
            2,
        ],
        dtype=float,
    )

    assert np.allclose(
        recursive_fft(values),
        np.fft.fft(values),
    )


def test_recursive_fft_matches_numpy_length_eight():
    values = np.array(
        [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
        ],
        dtype=float,
    )

    assert np.allclose(
        recursive_fft(values),
        np.fft.fft(values),
    )


def test_recursive_fft_complex_input():
    values = np.array(
        [
            1 + 2j,
            3 - 1j,
            2 + 0.5j,
            -1 + 4j,
        ],
        dtype=complex,
    )

    assert np.allclose(
        recursive_fft(values),
        np.fft.fft(values),
    )


def test_recursive_fft_non_power_of_two_rejected():
    with pytest.raises(ValueError):
        recursive_fft(
            [
                1,
                2,
                3,
            ]
        )


def test_iterative_fft_single_value():
    result = iterative_fft(
        [7]
    )

    assert np.allclose(
        result,
        [7],
    )


def test_iterative_fft_matches_numpy_length_four():
    values = np.array(
        [
            1,
            2,
            3,
            4,
        ],
        dtype=float,
    )

    assert np.allclose(
        iterative_fft(values),
        np.fft.fft(values),
    )


def test_iterative_fft_matches_numpy_length_sixteen():
    rng = np.random.default_rng(
        42
    )

    values = rng.normal(
        size=16
    )

    assert np.allclose(
        iterative_fft(values),
        np.fft.fft(values),
        atol=1e-10,
    )


def test_iterative_fft_complex_input():
    values = np.array(
        [
            1 + 1j,
            2 - 3j,
            4 + 2j,
            -2 + 0.5j,
            1 - 2j,
            0 + 3j,
            5 - 1j,
            2 + 2j,
        ],
        dtype=complex,
    )

    assert np.allclose(
        iterative_fft(values),
        np.fft.fft(values),
        atol=1e-10,
    )


def test_iterative_fft_non_power_of_two_rejected():
    with pytest.raises(ValueError):
        iterative_fft(
            [
                1,
                2,
                3,
                4,
                5,
                6,
            ]
        )


def test_recursive_and_iterative_match():
    rng = np.random.default_rng(
        123
    )

    values = rng.normal(
        size=32
    )

    assert np.allclose(
        recursive_fft(values),
        iterative_fft(values),
        atol=1e-10,
    )


def test_fft_default_is_iterative():
    values = [
        1,
        2,
        3,
        4,
    ]

    assert np.allclose(
        fft(values),
        iterative_fft(values),
    )


def test_fft_recursive_method():
    values = [
        1,
        2,
        3,
        4,
    ]

    assert np.allclose(
        fft(
            values,
            method="recursive",
        ),
        recursive_fft(values),
    )


def test_fft_invalid_method():
    with pytest.raises(ValueError):
        fft(
            [
                1,
                2,
            ],
            method="unknown",
        )


def test_ifft_round_trip_iterative():
    rng = np.random.default_rng(
        55
    )

    values = rng.normal(
        size=64
    )

    transformed = iterative_fft(
        values
    )

    reconstructed = ifft(
        transformed
    )

    assert np.allclose(
        reconstructed,
        values,
        atol=1e-10,
    )


def test_ifft_round_trip_recursive():
    values = np.array(
        [
            1,
            4,
            2,
            8,
            3,
            7,
            5,
            6,
        ],
        dtype=float,
    )

    transformed = recursive_fft(
        values
    )

    reconstructed = ifft(
        transformed,
        method="recursive",
    )

    assert np.allclose(
        reconstructed,
        values,
        atol=1e-10,
    )


def test_fft_detects_sine_frequency():
    sample_count = 128
    frequency = 8

    time = np.arange(
        sample_count
    )

    signal = np.sin(
        2
        * np.pi
        * frequency
        * time
        / sample_count
    )

    spectrum = iterative_fft(
        signal
    )

    positive_half = np.abs(
        spectrum[
            :sample_count // 2
        ]
    )

    peak = int(
        np.argmax(
            positive_half
        )
    )

    assert peak == frequency


def test_direct_dft_matches_numpy():
    values = np.array(
        [
            1,
            2,
            3,
            4,
        ],
        dtype=float,
    )

    assert np.allclose(
        direct_dft(values),
        np.fft.fft(values),
        atol=1e-10,
    )


def test_direct_dft_matches_fft():
    values = np.array(
        [
            2,
            1,
            0,
            -1,
            3,
            4,
            2,
            1,
        ],
        dtype=float,
    )

    assert np.allclose(
        direct_dft(values),
        iterative_fft(values),
        atol=1e-10,
    )


def test_circular_convolution_matches_numpy_fft():
    left = np.array(
        [
            1,
            2,
            3,
            4,
        ],
        dtype=float,
    )

    right = np.array(
        [
            2,
            0,
            1,
            0,
        ],
        dtype=float,
    )

    expected = np.fft.ifft(
        np.fft.fft(left)
        * np.fft.fft(right)
    ).real

    result = circular_convolution(
        left,
        right,
    )

    assert np.allclose(
        result,
        expected,
        atol=1e-10,
    )


def test_circular_convolution_known_result():
    result = circular_convolution(
        [
            1,
            2,
            3,
            4,
        ],
        [
            1,
            0,
            0,
            0,
        ],
    )

    assert np.allclose(
        result,
        [
            1,
            2,
            3,
            4,
        ],
    )


def test_circular_convolution_requires_equal_lengths():
    with pytest.raises(ValueError):
        circular_convolution(
            [
                1,
                2,
            ],
            [
                1,
                2,
                3,
                4,
            ],
        )


def test_circular_convolution_requires_power_of_two():
    with pytest.raises(ValueError):
        circular_convolution(
            [
                1,
                2,
                3,
            ],
            [
                4,
                5,
                6,
            ],
        )


def test_linear_convolution_matches_numpy():
    left = np.array(
        [
            1,
            2,
            3,
        ],
        dtype=float,
    )

    right = np.array(
        [
            4,
            5,
        ],
        dtype=float,
    )

    result = linear_convolution(
        left,
        right,
    )

    expected = np.convolve(
        left,
        right,
    )

    assert np.allclose(
        result,
        expected,
        atol=1e-10,
    )


def test_linear_convolution_known_result():
    result = linear_convolution(
        [
            1,
            2,
        ],
        [
            3,
            4,
        ],
    )

    assert np.allclose(
        result,
        [
            3,
            10,
            8,
        ],
    )


def test_linear_convolution_different_lengths():
    left = np.array(
        [
            1,
            -1,
            2,
            0,
            3,
        ],
        dtype=float,
    )

    right = np.array(
        [
            2,
            1,
            -2,
        ],
        dtype=float,
    )

    assert np.allclose(
        linear_convolution(
            left,
            right,
        ),
        np.convolve(
            left,
            right,
        ),
        atol=1e-10,
    )


def test_linear_convolution_complex_values():
    left = np.array(
        [
            1 + 1j,
            2 - 1j,
        ],
        dtype=complex,
    )

    right = np.array(
        [
            2 + 0j,
            1 + 2j,
        ],
        dtype=complex,
    )

    assert np.allclose(
        linear_convolution(
            left,
            right,
        ),
        np.convolve(
            left,
            right,
        ),
        atol=1e-10,
    )


def test_empty_fft_input_rejected():
    with pytest.raises(ValueError):
        iterative_fft([])


def test_multidimensional_fft_input_rejected():
    with pytest.raises(ValueError):
        iterative_fft(
            [
                [1, 2],
                [3, 4],
            ]
        )


def test_large_iterative_fft_matches_numpy():
    rng = np.random.default_rng(
        2026
    )

    values = rng.normal(
        size=4096
    )

    result = iterative_fft(
        values
    )

    expected = np.fft.fft(
        values
    )

    assert np.allclose(
        result,
        expected,
        atol=1e-9,
    )