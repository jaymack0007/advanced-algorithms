"""JPEG-style DCT image compression for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import math

import numpy as np


JPEG_LUMINANCE_QUANTIZATION = np.array(
    [
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99],
    ],
    dtype=float,
)


def _as_image(values) -> np.ndarray:
    """Convert input to a non-empty two-dimensional floating-point image."""
    try:
        image = np.asarray(
            values,
            dtype=float,
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Image must contain numeric values."
        ) from exc

    if image.ndim != 2:
        raise ValueError(
            "Image must be two-dimensional."
        )

    if (
        image.shape[0] == 0
        or image.shape[1] == 0
    ):
        raise ValueError(
            "Image cannot be empty."
        )

    if not np.all(
        np.isfinite(image)
    ):
        raise ValueError(
            "Image must contain finite values."
        )

    return image.copy()


def _validate_block_size(
    block_size: int,
) -> int:
    """Validate a positive integer DCT block size."""
    if not isinstance(
        block_size,
        int,
    ):
        raise TypeError(
            "block_size must be an integer."
        )

    if block_size <= 0:
        raise ValueError(
            "block_size must be positive."
        )

    return block_size


def _validate_quality(
    quality: int,
) -> int:
    """Validate JPEG-style quality from 1 through 100."""
    if not isinstance(
        quality,
        int,
    ):
        raise TypeError(
            "quality must be an integer."
        )

    if (
        quality < 1
        or quality > 100
    ):
        raise ValueError(
            "quality must be between 1 and 100."
        )

    return quality


def dct_matrix(
    size: int,
) -> np.ndarray:
    """
    Construct an orthonormal DCT-II transform matrix.

    Applying:
        C @ block @ C.T

    computes the 2D DCT of a square block.
    """
    size = _validate_block_size(
        size
    )

    matrix = np.zeros(
        (
            size,
            size,
        ),
        dtype=float,
    )

    factor = math.pi / (
        2.0 * size
    )

    for frequency in range(
        size
    ):
        if frequency == 0:
            scale = math.sqrt(
                1.0 / size
            )
        else:
            scale = math.sqrt(
                2.0 / size
            )

        for sample in range(
            size
        ):
            matrix[
                frequency,
                sample,
            ] = (
                scale
                * math.cos(
                    (
                        2 * sample
                        + 1
                    )
                    * frequency
                    * factor
                )
            )

    return matrix


def dct2(
    block,
) -> np.ndarray:
    """Compute the orthonormal 2D DCT of a square block."""
    data = _as_image(
        block
    )

    rows, columns = (
        data.shape
    )

    if rows != columns:
        raise ValueError(
            "DCT block must be square."
        )

    transform = dct_matrix(
        rows
    )

    return (
        transform
        @ data
        @ transform.T
    )


def idct2(
    coefficients,
) -> np.ndarray:
    """Compute the inverse orthonormal 2D DCT."""
    data = _as_image(
        coefficients
    )

    rows, columns = (
        data.shape
    )

    if rows != columns:
        raise ValueError(
            "DCT coefficient block must be square."
        )

    transform = dct_matrix(
        rows
    )

    return (
        transform.T
        @ data
        @ transform
    )


def scaled_quantization_table(
    quality: int,
) -> np.ndarray:
    """
    Scale the standard JPEG luminance quantization table.

    Lower quality produces larger quantization steps.
    Higher quality produces smaller quantization steps.
    """
    quality = _validate_quality(
        quality
    )

    if quality < 50:
        scale = (
            5000
            / quality
        )
    else:
        scale = (
            200
            - 2 * quality
        )

    table = np.floor(
        (
            JPEG_LUMINANCE_QUANTIZATION
            * scale
            + 50
        )
        / 100
    )

    table[
        table < 1
    ] = 1

    table[
        table > 255
    ] = 255

    return table.astype(
        float
    )


def quantize_block(
    coefficients,
    *,
    quality: int = 50,
) -> np.ndarray:
    """Quantize an 8x8 DCT coefficient block."""
    data = _as_image(
        coefficients
    )

    if data.shape != (
        8,
        8,
    ):
        raise ValueError(
            "JPEG quantization expects an 8x8 block."
        )

    table = scaled_quantization_table(
        quality
    )

    return np.rint(
        data
        / table
    )


def dequantize_block(
    quantized,
    *,
    quality: int = 50,
) -> np.ndarray:
    """Restore approximate DCT coefficients from an 8x8 quantized block."""
    data = _as_image(
        quantized
    )

    if data.shape != (
        8,
        8,
    ):
        raise ValueError(
            "JPEG dequantization expects an 8x8 block."
        )

    table = scaled_quantization_table(
        quality
    )

    return (
        data
        * table
    )


def pad_image_to_block_size(
    values,
    *,
    block_size: int = 8,
) -> tuple[
    np.ndarray,
    tuple[int, int],
]:
    """
    Pad an image so both dimensions are multiples of block_size.

    Edge values are repeated instead of adding a black border.
    """
    image = _as_image(
        values
    )

    block_size = _validate_block_size(
        block_size
    )

    rows, columns = (
        image.shape
    )

    padded_rows = int(
        math.ceil(
            rows
            / block_size
        )
        * block_size
    )

    padded_columns = int(
        math.ceil(
            columns
            / block_size
        )
        * block_size
    )

    row_padding = (
        padded_rows
        - rows
    )

    column_padding = (
        padded_columns
        - columns
    )

    padded = np.pad(
        image,
        (
            (
                0,
                row_padding,
            ),
            (
                0,
                column_padding,
            ),
        ),
        mode="edge",
    )

    return (
        padded.astype(
            float
        ),
        (
            rows,
            columns,
        ),
    )


def compress_image(
    values,
    *,
    quality: int = 50,
) -> dict[str, object]:
    """
    Compress a grayscale image with 8x8 DCT and JPEG-style quantization.

    Returns a dictionary containing the quantized coefficients plus
    metadata needed for reconstruction.
    """
    image = _as_image(
        values
    )

    quality = _validate_quality(
        quality
    )

    padded, original_shape = (
        pad_image_to_block_size(
            image,
            block_size=8,
        )
    )

    shifted = (
        padded
        - 128.0
    )

    quantized = np.zeros_like(
        shifted,
        dtype=float,
    )

    rows, columns = (
        shifted.shape
    )

    for row in range(
        0,
        rows,
        8,
    ):
        for column in range(
            0,
            columns,
            8,
        ):
            block = shifted[
                row:row + 8,
                column:column + 8,
            ]

            coefficients = dct2(
                block
            )

            quantized[
                row:row + 8,
                column:column + 8,
            ] = quantize_block(
                coefficients,
                quality=quality,
            )

    nonzero = int(
        np.count_nonzero(
            quantized
        )
    )

    total = int(
        quantized.size
    )

    return {
        "quantized": quantized,
        "original_shape": original_shape,
        "padded_shape": padded.shape,
        "quality": quality,
        "nonzero_coefficients": nonzero,
        "total_coefficients": total,
        "zero_fraction": (
            1.0
            - nonzero / total
        ),
    }


def reconstruct_image(
    compressed,
) -> np.ndarray:
    """Reconstruct a grayscale image from compress_image output."""
    if not isinstance(
        compressed,
        dict,
    ):
        raise TypeError(
            "compressed must be a dictionary."
        )

    required = {
        "quantized",
        "original_shape",
        "quality",
    }

    if not required.issubset(
        compressed
    ):
        raise ValueError(
            "Compressed data is missing required fields."
        )

    quantized = _as_image(
        compressed[
            "quantized"
        ]
    )

    quality = _validate_quality(
        int(
            compressed[
                "quality"
            ]
        )
    )

    try:
        original_rows, original_columns = (
            compressed[
                "original_shape"
            ]
        )
    except (
        TypeError,
        ValueError,
    ) as exc:
        raise ValueError(
            "original_shape is invalid."
        ) from exc

    rows, columns = (
        quantized.shape
    )

    if (
        rows % 8 != 0
        or columns % 8 != 0
    ):
        raise ValueError(
            "Quantized image dimensions must be multiples of 8."
        )

    reconstructed = np.zeros_like(
        quantized,
        dtype=float,
    )

    for row in range(
        0,
        rows,
        8,
    ):
        for column in range(
            0,
            columns,
            8,
        ):
            quantized_block = quantized[
                row:row + 8,
                column:column + 8,
            ]

            coefficients = (
                dequantize_block(
                    quantized_block,
                    quality=quality,
                )
            )

            block = idct2(
                coefficients
            )

            reconstructed[
                row:row + 8,
                column:column + 8,
            ] = (
                block
                + 128.0
            )

    reconstructed = np.clip(
        reconstructed,
        0.0,
        255.0,
    )

    return reconstructed[
        :int(
            original_rows
        ),
        :int(
            original_columns
        ),
    ]


def compress_and_reconstruct(
    values,
    *,
    quality: int = 50,
) -> tuple[
    np.ndarray,
    dict[str, object],
]:
    """Compress and immediately reconstruct an image."""
    compressed = compress_image(
        values,
        quality=quality,
    )

    reconstructed = (
        reconstruct_image(
            compressed
        )
    )

    return (
        reconstructed,
        compressed,
    )


def mean_squared_error(
    original,
    reconstructed,
) -> float:
    """Compute mean squared reconstruction error."""
    first = _as_image(
        original
    )

    second = _as_image(
        reconstructed
    )

    if first.shape != second.shape:
        raise ValueError(
            "Images must have matching shapes."
        )

    difference = (
        first
        - second
    )

    return float(
        np.mean(
            difference
            * difference
        )
    )


def peak_signal_to_noise_ratio(
    original,
    reconstructed,
    *,
    max_value: float = 255.0,
) -> float:
    """Compute PSNR in decibels."""
    try:
        max_value = float(
            max_value
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "max_value must be numeric."
        ) from exc

    if max_value <= 0:
        raise ValueError(
            "max_value must be positive."
        )

    mse = mean_squared_error(
        original,
        reconstructed,
    )

    if mse == 0.0:
        return math.inf

    return float(
        10.0
        * math.log10(
            (
                max_value
                * max_value
            )
            / mse
        )
    )