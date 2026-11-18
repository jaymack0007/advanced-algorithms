"""Tests for Week 12 image processing workflows."""

import math

import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.applications.image_processor import (
    apply_image_filter,
    compress_image_array,
    compress_image_file,
    frequency_magnitude,
    load_image,
    process_image_file,
    save_image,
)


def test_apply_blur_preserves_shape():
    image = np.ones(
        (
            16,
            16,
        )
    )

    result = apply_image_filter(
        image,
        filter_type="blur",
    )

    assert result.shape == image.shape


def test_apply_sobel_preserves_shape():
    image = np.zeros(
        (
            16,
            16,
        )
    )

    result = apply_image_filter(
        image,
        filter_type="sobel",
    )

    assert result.shape == image.shape


def test_apply_laplacian_preserves_shape():
    image = np.zeros(
        (
            16,
            16,
        )
    )

    result = apply_image_filter(
        image,
        filter_type="laplacian",
    )

    assert result.shape == image.shape


def test_apply_denoise_preserves_shape():
    image = np.ones(
        (
            15,
            19,
        )
    )

    result = apply_image_filter(
        image,
        filter_type="denoise",
    )

    assert result.shape == image.shape


def test_apply_sharpen_preserves_shape():
    image = np.ones(
        (
            12,
            14,
        )
    )

    result = apply_image_filter(
        image,
        filter_type="sharpen",
    )

    assert result.shape == image.shape


def test_invalid_filter_type():
    with pytest.raises(ValueError):
        apply_image_filter(
            np.ones(
                (
                    8,
                    8,
                )
            ),
            filter_type="unknown",
        )


def test_frequency_magnitude_power_two_shape():
    image = np.ones(
        (
            8,
            16,
        )
    )

    result = frequency_magnitude(
        image
    )

    assert result.shape == (
        8,
        16,
    )


def test_frequency_magnitude_pads_shape():
    image = np.ones(
        (
            10,
            13,
        )
    )

    result = frequency_magnitude(
        image
    )

    assert result.shape == (
        16,
        16,
    )


def test_frequency_magnitude_constant_center_peak():
    image = np.ones(
        (
            8,
            8,
        )
    )

    result = frequency_magnitude(
        image,
        logarithmic=False,
    )

    center = result[
        4,
        4,
    ]

    assert center == pytest.approx(
        np.max(
            result
        )
    )


def test_compress_image_array_keys():
    image = np.full(
        (
            16,
            16,
        ),
        128.0,
    )

    result = compress_image_array(
        image,
        quality=50,
    )

    assert set(
        result
    ) == {
        "reconstructed",
        "compressed",
        "mse",
        "psnr",
        "zero_fraction",
        "quality",
    }


def test_compress_image_array_shape():
    image = np.ones(
        (
            13,
            19,
        )
    ) * 100.0

    result = compress_image_array(
        image,
        quality=50,
    )

    assert result[
        "reconstructed"
    ].shape == image.shape


def test_constant_image_compression_low_error():
    image = np.full(
        (
            16,
            16,
        ),
        128.0,
    )

    result = compress_image_array(
        image,
        quality=50,
    )

    assert result[
        "mse"
    ] == pytest.approx(
        0.0,
        abs=1e-10,
    )

    assert math.isinf(
        result[
            "psnr"
        ]
    )


def test_compression_reports_zero_fraction():
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

    result = compress_image_array(
        image,
        quality=50,
    )

    assert (
        0.0
        <= result[
            "zero_fraction"
        ]
        <= 1.0
    )


def test_save_image_creates_file(tmp_path):
    path = (
        tmp_path
        / "saved.png"
    )

    image = np.arange(
        64,
        dtype=float,
    ).reshape(
        8,
        8,
    )

    save_image(
        path,
        image,
    )

    assert path.exists()


def test_save_load_round_trip_shape(tmp_path):
    path = (
        tmp_path
        / "roundtrip.png"
    )

    image = np.arange(
        64,
        dtype=float,
    ).reshape(
        8,
        8,
    ) * 4.0

    save_image(
        path,
        image,
    )

    loaded = load_image(
        path
    )

    assert loaded.shape == image.shape


def test_save_load_round_trip_values(tmp_path):
    path = (
        tmp_path
        / "roundtrip.png"
    )

    image = np.array(
        [
            [0, 64],
            [128, 255],
        ],
        dtype=float,
    )

    save_image(
        path,
        image,
    )

    loaded = load_image(
        path
    )

    assert np.allclose(
        loaded,
        image,
        atol=2.0,
    )


def test_load_missing_image():
    with pytest.raises(FileNotFoundError):
        load_image(
            "definitely_missing_image.png"
        )


def test_process_image_file(tmp_path):
    input_path = (
        tmp_path
        / "input.png"
    )

    output_path = (
        tmp_path
        / "output.png"
    )

    image = np.zeros(
        (
            16,
            16,
        )
    )

    image[
        8,
        8,
    ] = 255.0

    save_image(
        input_path,
        image,
    )

    result = process_image_file(
        input_path,
        output_path,
        filter_type="blur",
    )

    assert output_path.exists()

    assert result[
        "input_shape"
    ] == (
        16,
        16,
    )

    assert result[
        "output_shape"
    ] == (
        16,
        16,
    )


def test_compress_image_file(tmp_path):
    input_path = (
        tmp_path
        / "input.png"
    )

    output_path = (
        tmp_path
        / "compressed.png"
    )

    x = np.linspace(
        0,
        255,
        16,
    )

    image = np.tile(
        x,
        (
            16,
            1,
        ),
    )

    save_image(
        input_path,
        image,
    )

    result = compress_image_file(
        input_path,
        output_path,
        quality=60,
    )

    assert output_path.exists()

    assert result[
        "quality"
    ] == 60

    assert result[
        "input_shape"
    ] == (
        16,
        16,
    )


def test_empty_image_rejected():
    with pytest.raises(ValueError):
        apply_image_filter(
            np.empty(
                (
                    0,
                    0,
                )
            ),
            filter_type="blur",
        )


def test_invalid_image_dimensions():
    with pytest.raises(ValueError):
        apply_image_filter(
            [
                1,
                2,
                3,
            ],
            filter_type="blur",
        )