"""Tests for Week 12 DCT image compression."""

import math

import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.image.compression import (
    JPEG_LUMINANCE_QUANTIZATION,
    compress_and_reconstruct,
    compress_image,
    dct2,
    dct_matrix,
    dequantize_block,
    idct2,
    mean_squared_error,
    pad_image_to_block_size,
    peak_signal_to_noise_ratio,
    quantize_block,
    reconstruct_image,
    scaled_quantization_table,
)


def test_dct_matrix_shape():
    matrix = dct_matrix(
        8
    )

    assert matrix.shape == (
        8,
        8,
    )


def test_dct_matrix_orthonormal():
    matrix = dct_matrix(
        8
    )

    assert np.allclose(
        matrix @ matrix.T,
        np.eye(
            8
        ),
        atol=1e-12,
    )


def test_dct_constant_block_only_dc():
    block = np.full(
        (
            8,
            8,
        ),
        10.0,
    )

    coefficients = dct2(
        block
    )

    assert coefficients[
        0,
        0,
    ] == pytest.approx(
        80.0
    )

    remainder = coefficients.copy()

    remainder[
        0,
        0,
    ] = 0.0

    assert np.max(
        np.abs(
            remainder
        )
    ) < 1e-10


def test_dct_idct_round_trip():
    rng = np.random.default_rng(
        2026
    )

    block = rng.normal(
        size=(
            8,
            8,
        )
    )

    reconstructed = idct2(
        dct2(
            block
        )
    )

    assert np.allclose(
        reconstructed,
        block,
        atol=1e-10,
    )


def test_dct_rejects_nonsquare():
    with pytest.raises(ValueError):
        dct2(
            np.ones(
                (
                    8,
                    4,
                )
            )
        )


def test_standard_quantization_table_shape():
    assert (
        JPEG_LUMINANCE_QUANTIZATION.shape
        == (
            8,
            8,
        )
    )


def test_quality_50_matches_standard_table():
    table = scaled_quantization_table(
        50
    )

    assert np.array_equal(
        table,
        JPEG_LUMINANCE_QUANTIZATION,
    )


def test_high_quality_smaller_quantization_values():
    low_quality = (
        scaled_quantization_table(
            20
        )
    )

    high_quality = (
        scaled_quantization_table(
            90
        )
    )

    assert np.mean(
        high_quality
    ) < np.mean(
        low_quality
    )


def test_quality_100_is_all_ones():
    table = scaled_quantization_table(
        100
    )

    assert np.array_equal(
        table,
        np.ones(
            (
                8,
                8,
            )
        ),
    )


def test_invalid_quality_low():
    with pytest.raises(ValueError):
        scaled_quantization_table(
            0
        )


def test_invalid_quality_high():
    with pytest.raises(ValueError):
        scaled_quantization_table(
            101
        )


def test_quantize_block_shape():
    block = np.ones(
        (
            8,
            8,
        )
    )

    result = quantize_block(
        block,
        quality=50,
    )

    assert result.shape == (
        8,
        8,
    )


def test_quantize_dequantize():
    block = (
        JPEG_LUMINANCE_QUANTIZATION
        * 2
    )

    quantized = quantize_block(
        block,
        quality=50,
    )

    restored = dequantize_block(
        quantized,
        quality=50,
    )

    assert np.allclose(
        restored,
        block,
    )


def test_quantize_rejects_non_8x8():
    with pytest.raises(ValueError):
        quantize_block(
            np.ones(
                (
                    4,
                    4,
                )
            )
        )


def test_padding_exact_block_size():
    image = np.ones(
        (
            16,
            24,
        )
    )

    padded, shape = (
        pad_image_to_block_size(
            image
        )
    )

    assert padded.shape == (
        16,
        24,
    )

    assert shape == (
        16,
        24,
    )


def test_padding_non_multiple():
    image = np.ones(
        (
            10,
            13,
        )
    )

    padded, shape = (
        pad_image_to_block_size(
            image
        )
    )

    assert padded.shape == (
        16,
        16,
    )

    assert shape == (
        10,
        13,
    )


def test_padding_preserves_original():
    image = np.arange(
        35,
        dtype=float,
    ).reshape(
        5,
        7,
    )

    padded, _ = (
        pad_image_to_block_size(
            image
        )
    )

    assert np.array_equal(
        padded[
            :5,
            :7,
        ],
        image,
    )


def test_compress_image_metadata():
    image = np.full(
        (
            16,
            16,
        ),
        128.0,
    )

    result = compress_image(
        image,
        quality=50,
    )

    assert result[
        "original_shape"
    ] == (
        16,
        16,
    )

    assert result[
        "quality"
    ] == 50

    assert result[
        "total_coefficients"
    ] == 256


def test_compress_constant_128_image_all_zero_coefficients():
    image = np.full(
        (
            16,
            16,
        ),
        128.0,
    )

    result = compress_image(
        image,
        quality=50,
    )

    assert np.count_nonzero(
        result[
            "quantized"
        ]
    ) == 0

    assert result[
        "zero_fraction"
    ] == pytest.approx(
        1.0
    )


def test_reconstruct_constant_128_image():
    image = np.full(
        (
            16,
            16,
        ),
        128.0,
    )

    compressed = compress_image(
        image,
        quality=50,
    )

    reconstructed = (
        reconstruct_image(
            compressed
        )
    )

    assert np.allclose(
        reconstructed,
        image,
        atol=1e-10,
    )


def test_reconstruction_shape_matches_original():
    image = np.full(
        (
            13,
            19,
        ),
        120.0,
    )

    compressed = compress_image(
        image,
        quality=50,
    )

    reconstructed = (
        reconstruct_image(
            compressed
        )
    )

    assert reconstructed.shape == (
        13,
        19,
    )


def test_reconstruction_clipped_to_image_range():
    rng = np.random.default_rng(
        10
    )

    image = rng.uniform(
        0,
        255,
        size=(
            16,
            16,
        ),
    )

    reconstructed, _ = (
        compress_and_reconstruct(
            image,
            quality=20,
        )
    )

    assert np.min(
        reconstructed
    ) >= 0.0

    assert np.max(
        reconstructed
    ) <= 255.0


def test_high_quality_lower_mse_than_low_quality():
    x = np.linspace(
        0,
        255,
        32,
    )

    image = np.tile(
        x,
        (
            32,
            1,
        ),
    )

    low_result, _ = (
        compress_and_reconstruct(
            image,
            quality=20,
        )
    )

    high_result, _ = (
        compress_and_reconstruct(
            image,
            quality=90,
        )
    )

    low_error = mean_squared_error(
        image,
        low_result,
    )

    high_error = mean_squared_error(
        image,
        high_result,
    )

    assert high_error < low_error


def test_high_quality_psnr_higher_than_low_quality():
    x = np.linspace(
        0,
        255,
        32,
    )

    image = np.tile(
        x,
        (
            32,
            1,
        ),
    )

    low_result, _ = (
        compress_and_reconstruct(
            image,
            quality=20,
        )
    )

    high_result, _ = (
        compress_and_reconstruct(
            image,
            quality=90,
        )
    )

    assert (
        peak_signal_to_noise_ratio(
            image,
            high_result,
        )
        >
        peak_signal_to_noise_ratio(
            image,
            low_result,
        )
    )


def test_mean_squared_error_identical():
    image = np.ones(
        (
            8,
            8,
        )
    )

    assert mean_squared_error(
        image,
        image,
    ) == 0.0


def test_mean_squared_error_known():
    first = np.zeros(
        (
            2,
            2,
        )
    )

    second = np.ones(
        (
            2,
            2,
        )
    )

    assert mean_squared_error(
        first,
        second,
    ) == pytest.approx(
        1.0
    )


def test_mse_shape_mismatch():
    with pytest.raises(ValueError):
        mean_squared_error(
            np.ones(
                (
                    8,
                    8,
                )
            ),
            np.ones(
                (
                    4,
                    4,
                )
            ),
        )


def test_psnr_identical_is_infinite():
    image = np.ones(
        (
            8,
            8,
        )
    )

    result = (
        peak_signal_to_noise_ratio(
            image,
            image,
        )
    )

    assert math.isinf(
        result
    )


def test_psnr_finite_for_lossy_reconstruction():
    image = np.arange(
        256,
        dtype=float,
    ).reshape(
        16,
        16,
    )

    reconstructed, _ = (
        compress_and_reconstruct(
            image,
            quality=30,
        )
    )

    result = (
        peak_signal_to_noise_ratio(
            image,
            reconstructed,
        )
    )

    assert np.isfinite(
        result
    )


def test_compression_produces_zero_coefficients():
    x = np.linspace(
        0,
        255,
        32,
    )

    image = np.tile(
        x,
        (
            32,
            1,
        ),
    )

    compressed = compress_image(
        image,
        quality=50,
    )

    assert compressed[
        "zero_fraction"
    ] > 0.5


def test_low_quality_has_at_least_as_many_zeros():
    rng = np.random.default_rng(
        99
    )

    image = rng.uniform(
        0,
        255,
        size=(
            32,
            32,
        ),
    )

    low = compress_image(
        image,
        quality=20,
    )

    high = compress_image(
        image,
        quality=90,
    )

    assert (
        low[
            "zero_fraction"
        ]
        >=
        high[
            "zero_fraction"
        ]
    )


def test_reconstruct_requires_dictionary():
    with pytest.raises(TypeError):
        reconstruct_image(
            np.ones(
                (
                    8,
                    8,
                )
            )
        )


def test_reconstruct_requires_fields():
    with pytest.raises(ValueError):
        reconstruct_image(
            {
                "quantized": np.ones(
                    (
                        8,
                        8,
                    )
                )
            }
        )


def test_empty_image_rejected():
    with pytest.raises(ValueError):
        compress_image(
            np.empty(
                (
                    0,
                    0,
                )
            )
        )