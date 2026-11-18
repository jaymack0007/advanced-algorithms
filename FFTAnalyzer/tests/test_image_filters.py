"""Tests for Week 12 FFT-based image filters."""

import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.image.filters import (
    fft2,
    fft_convolve2d,
    frequency_denoise,
    gaussian_blur,
    gaussian_kernel,
    ifft2,
    laplacian_edges,
    pad_image_to_power_of_two,
    sharpen_image,
    sobel_edges,
)


def test_fft2_matches_numpy():
    image = np.arange(
        16,
        dtype=float,
    ).reshape(
        4,
        4,
    )

    result = fft2(
        image
    )

    expected = np.fft.fft2(
        image
    )

    assert np.allclose(
        result,
        expected,
        atol=1e-10,
    )


def test_fft2_complex_input():
    image = np.array(
        [
            [1 + 1j, 2 - 1j],
            [3 + 2j, 4 + 0j],
        ],
        dtype=complex,
    )

    assert np.allclose(
        fft2(image),
        np.fft.fft2(image),
        atol=1e-10,
    )


def test_fft2_rejects_non_power_two_shape():
    with pytest.raises(ValueError):
        fft2(
            np.ones(
                (
                    3,
                    4,
                )
            )
        )


def test_ifft2_round_trip():
    image = np.arange(
        64,
        dtype=float,
    ).reshape(
        8,
        8,
    )

    transformed = fft2(
        image
    )

    reconstructed = ifft2(
        transformed
    )

    assert np.allclose(
        reconstructed,
        image,
        atol=1e-10,
    )


def test_pad_image_power_two_shape():
    image = np.ones(
        (
            5,
            7,
        )
    )

    padded, shape = (
        pad_image_to_power_of_two(
            image
        )
    )

    assert padded.shape == (
        8,
        8,
    )

    assert shape == (
        5,
        7,
    )


def test_pad_image_preserves_values():
    image = np.arange(
        15,
        dtype=float,
    ).reshape(
        3,
        5,
    )

    padded, _ = (
        pad_image_to_power_of_two(
            image
        )
    )

    assert np.allclose(
        padded[
            :3,
            :5,
        ],
        image,
    )


def test_fft_convolve_identity_kernel():
    image = np.arange(
        16,
        dtype=float,
    ).reshape(
        4,
        4,
    )

    result = fft_convolve2d(
        image,
        [
            [1],
        ],
    )

    assert np.allclose(
        result,
        image,
        atol=1e-10,
    )


def test_fft_convolve_shape_preserved():
    image = np.ones(
        (
            6,
            7,
        )
    )

    kernel = np.ones(
        (
            3,
            3,
        )
    )

    result = fft_convolve2d(
        image,
        kernel,
    )

    assert result.shape == (
        6,
        7,
    )


def test_gaussian_kernel_shape():
    kernel = gaussian_kernel(
        5,
        1.0,
    )

    assert kernel.shape == (
        5,
        5,
    )


def test_gaussian_kernel_sums_to_one():
    kernel = gaussian_kernel(
        5,
        1.0,
    )

    assert np.sum(
        kernel
    ) == pytest.approx(
        1.0
    )


def test_gaussian_kernel_symmetric():
    kernel = gaussian_kernel(
        7,
        1.5,
    )

    assert np.allclose(
        kernel,
        kernel[::-1, :],
    )

    assert np.allclose(
        kernel,
        kernel[:, ::-1],
    )


def test_gaussian_kernel_center_largest():
    kernel = gaussian_kernel(
        5,
        1.0,
    )

    assert kernel[
        2,
        2,
    ] == pytest.approx(
        np.max(
            kernel
        )
    )


def test_gaussian_kernel_even_size_rejected():
    with pytest.raises(ValueError):
        gaussian_kernel(
            4,
            1.0,
        )


def test_gaussian_kernel_invalid_sigma():
    with pytest.raises(ValueError):
        gaussian_kernel(
            5,
            0,
        )


def test_gaussian_blur_shape():
    image = np.ones(
        (
            16,
            16,
        )
    )

    result = gaussian_blur(
        image
    )

    assert result.shape == (
        16,
        16,
    )


def test_gaussian_blur_impulse_spreads_energy():
    image = np.zeros(
        (
            17,
            17,
        )
    )

    image[
        8,
        8,
    ] = 1.0

    result = gaussian_blur(
        image,
        kernel_size=5,
        sigma=1.0,
    )

    assert (
        0.0
        < result[
            8,
            8,
        ]
        < 1.0
    )

    assert result[
        8,
        9,
    ] > 0.0


def test_gaussian_blur_impulse_preserves_sum():
    image = np.zeros(
        (
            17,
            17,
        )
    )

    image[
        8,
        8,
    ] = 1.0

    result = gaussian_blur(
        image,
        kernel_size=5,
        sigma=1.0,
    )

    assert np.sum(
        result
    ) == pytest.approx(
        1.0,
        abs=1e-10,
    )


def test_sobel_zero_image():
    image = np.zeros(
        (
            16,
            16,
        )
    )

    result = sobel_edges(
        image
    )

    assert np.allclose(
        result,
        0,
        atol=1e-10,
    )


def test_sobel_detects_vertical_edge():
    image = np.zeros(
        (
            16,
            16,
        )
    )

    image[
        :,
        8:,
    ] = 1.0

    result = sobel_edges(
        image
    )

    assert np.max(
        result[
            :,
            7:10,
        ]
    ) > 1.0


def test_sobel_shape_preserved():
    image = np.zeros(
        (
            10,
            12,
        )
    )

    assert sobel_edges(
        image
    ).shape == (
        10,
        12,
    )


def test_laplacian_zero_image():
    image = np.zeros(
        (
            16,
            16,
        )
    )

    result = laplacian_edges(
        image
    )

    assert np.allclose(
        result,
        0,
        atol=1e-10,
    )


def test_laplacian_detects_impulse():
    image = np.zeros(
        (
            16,
            16,
        )
    )

    image[
        8,
        8,
    ] = 1.0

    result = laplacian_edges(
        image
    )

    assert np.max(
        result
    ) >= 4.0 - 1e-10


def test_frequency_denoise_preserves_shape():
    image = np.ones(
        (
            15,
            19,
        )
    )

    result = frequency_denoise(
        image,
        cutoff_ratio=0.25,
    )

    assert result.shape == (
        15,
        19,
    )


def test_frequency_denoise_reduces_checkerboard_variation():
    row = np.arange(
        32
    )

    x, y = np.meshgrid(
        row,
        row,
    )

    image = (
        (
            x + y
        )
        % 2
    ).astype(
        float
    )

    result = frequency_denoise(
        image,
        cutoff_ratio=0.2,
    )

    assert np.std(
        result
    ) < np.std(
        image
    )


def test_frequency_denoise_finite_output():
    rng = np.random.default_rng(
        2026
    )

    image = rng.normal(
        size=(
            20,
            30,
        )
    )

    result = frequency_denoise(
        image,
        cutoff_ratio=0.4,
    )

    assert np.all(
        np.isfinite(
            result
        )
    )


def test_frequency_denoise_invalid_cutoff():
    with pytest.raises(ValueError):
        frequency_denoise(
            np.ones(
                (
                    8,
                    8,
                )
            ),
            cutoff_ratio=0,
        )


def test_frequency_denoise_cutoff_above_one():
    with pytest.raises(ValueError):
        frequency_denoise(
            np.ones(
                (
                    8,
                    8,
                )
            ),
            cutoff_ratio=1.1,
        )


def test_sharpen_shape_preserved():
    image = np.ones(
        (
            12,
            14,
        )
    )

    result = sharpen_image(
        image
    )

    assert result.shape == (
        12,
        14,
    )


def test_sharpen_zero_amount_returns_original():
    rng = np.random.default_rng(
        7
    )

    image = rng.normal(
        size=(
            16,
            16,
        )
    )

    result = sharpen_image(
        image,
        amount=0,
    )

    assert np.allclose(
        result,
        image,
    )


def test_sharpen_increases_impulse_contrast():
    image = np.zeros(
        (
            17,
            17,
        )
    )

    image[
        8,
        8,
    ] = 1.0

    result = sharpen_image(
        image,
        amount=1.0,
    )

    assert result[
        8,
        8,
    ] > image[
        8,
        8,
    ]


def test_sharpen_negative_amount_rejected():
    with pytest.raises(ValueError):
        sharpen_image(
            np.ones(
                (
                    8,
                    8,
                )
            ),
            amount=-1,
        )


def test_empty_image_rejected():
    with pytest.raises(ValueError):
        gaussian_blur(
            np.empty(
                (
                    0,
                    0,
                )
            )
        )


def test_one_dimensional_image_rejected():
    with pytest.raises(ValueError):
        sobel_edges(
            [
                1,
                2,
                3,
            ]
        )


def test_non_numeric_image_rejected():
    with pytest.raises(TypeError):
        laplacian_edges(
            [
                ["a", "b"],
                ["c", "d"],
            ]
        )