"""FFT-based image filtering for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import math

import numpy as np

from FFTAnalyzer.fft_analyzer.core.fft import (
    ifft,
    is_power_of_two,
    iterative_fft,
    next_power_of_two,
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


def _as_complex_matrix(values) -> np.ndarray:
    """Convert input to a non-empty two-dimensional complex matrix."""
    try:
        matrix = np.asarray(
            values,
            dtype=complex,
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Matrix must contain numeric values."
        ) from exc

    if matrix.ndim != 2:
        raise ValueError(
            "Matrix must be two-dimensional."
        )

    if (
        matrix.shape[0] == 0
        or matrix.shape[1] == 0
    ):
        raise ValueError(
            "Matrix cannot be empty."
        )

    return matrix.copy()


def _validate_power_two_shape(
    shape,
) -> None:
    """Require power-of-two row and column dimensions."""
    rows, columns = shape

    if (
        not is_power_of_two(
            int(rows)
        )
        or not is_power_of_two(
            int(columns)
        )
    ):
        raise ValueError(
            "2D FFT dimensions must both be powers of two."
        )


def fft2(values) -> np.ndarray:
    """
    Compute a radix-2 two-dimensional FFT.

    The transform is applied first to every row and then to every column
    using the project's iterative 1D FFT implementation.
    """
    matrix = _as_complex_matrix(
        values
    )

    _validate_power_two_shape(
        matrix.shape
    )

    rows, columns = (
        matrix.shape
    )

    row_transformed = np.empty(
        (
            rows,
            columns,
        ),
        dtype=complex,
    )

    for row in range(rows):
        row_transformed[
            row,
            :,
        ] = iterative_fft(
            matrix[
                row,
                :,
            ]
        )

    result = np.empty(
        (
            rows,
            columns,
        ),
        dtype=complex,
    )

    for column in range(columns):
        result[
            :,
            column,
        ] = iterative_fft(
            row_transformed[
                :,
                column,
            ]
        )

    return result


def ifft2(values) -> np.ndarray:
    """Compute the inverse two-dimensional radix-2 FFT."""
    matrix = _as_complex_matrix(
        values
    )

    _validate_power_two_shape(
        matrix.shape
    )

    rows, columns = (
        matrix.shape
    )

    row_transformed = np.empty(
        (
            rows,
            columns,
        ),
        dtype=complex,
    )

    for row in range(rows):
        row_transformed[
            row,
            :,
        ] = ifft(
            matrix[
                row,
                :,
            ]
        )

    result = np.empty(
        (
            rows,
            columns,
        ),
        dtype=complex,
    )

    for column in range(columns):
        result[
            :,
            column,
        ] = ifft(
            row_transformed[
                :,
                column,
            ]
        )

    return result


def pad_image_to_power_of_two(
    values,
) -> tuple[
    np.ndarray,
    tuple[int, int],
]:
    """
    Zero-pad an image to power-of-two dimensions.

    Returns:
        padded image
        original shape
    """
    image = _as_image(
        values
    )

    rows, columns = (
        image.shape
    )

    padded_rows = (
        next_power_of_two(
            rows
        )
    )

    padded_columns = (
        next_power_of_two(
            columns
        )
    )

    padded = np.zeros(
        (
            padded_rows,
            padded_columns,
        ),
        dtype=float,
    )

    padded[
        :rows,
        :columns,
    ] = image

    return (
        padded,
        (
            rows,
            columns,
        ),
    )


def fft_convolve2d(
    values,
    kernel,
) -> np.ndarray:
    """
    Perform linear 2D convolution using FFT multiplication.

    The returned image has the same shape as the input image.
    """
    image = _as_image(
        values
    )

    kernel_array = _as_image(
        kernel
    )

    image_rows, image_columns = (
        image.shape
    )

    kernel_rows, kernel_columns = (
        kernel_array.shape
    )

    full_rows = (
        image_rows
        + kernel_rows
        - 1
    )

    full_columns = (
        image_columns
        + kernel_columns
        - 1
    )

    transform_rows = (
        next_power_of_two(
            full_rows
        )
    )

    transform_columns = (
        next_power_of_two(
            full_columns
        )
    )

    padded_image = np.zeros(
        (
            transform_rows,
            transform_columns,
        ),
        dtype=complex,
    )

    padded_kernel = np.zeros(
        (
            transform_rows,
            transform_columns,
        ),
        dtype=complex,
    )

    padded_image[
        :image_rows,
        :image_columns,
    ] = image

    padded_kernel[
        :kernel_rows,
        :kernel_columns,
    ] = kernel_array

    image_spectrum = fft2(
        padded_image
    )

    kernel_spectrum = fft2(
        padded_kernel
    )

    full_result = ifft2(
        image_spectrum
        * kernel_spectrum
    )

    full_result = np.real(
        full_result[
            :full_rows,
            :full_columns,
        ]
    )

    row_start = (
        kernel_rows - 1
    ) // 2

    column_start = (
        kernel_columns - 1
    ) // 2

    return full_result[
        row_start:
        row_start + image_rows,
        column_start:
        column_start + image_columns,
    ]


def gaussian_kernel(
    size: int = 5,
    sigma: float = 1.0,
) -> np.ndarray:
    """Create a normalized square Gaussian smoothing kernel."""
    if not isinstance(
        size,
        int,
    ):
        raise TypeError(
            "size must be an integer."
        )

    if (
        size <= 0
        or size % 2 == 0
    ):
        raise ValueError(
            "size must be a positive odd integer."
        )

    try:
        sigma = float(
            sigma
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "sigma must be numeric."
        ) from exc

    if (
        not math.isfinite(
            sigma
        )
        or sigma <= 0
    ):
        raise ValueError(
            "sigma must be positive and finite."
        )

    radius = (
        size // 2
    )

    coordinates = np.arange(
        -radius,
        radius + 1,
        dtype=float,
    )

    x, y = np.meshgrid(
        coordinates,
        coordinates,
    )

    kernel = np.exp(
        -(
            x * x
            + y * y
        )
        / (
            2.0
            * sigma
            * sigma
        )
    )

    kernel /= np.sum(
        kernel
    )

    return kernel


def gaussian_blur(
    values,
    *,
    kernel_size: int = 5,
    sigma: float = 1.0,
) -> np.ndarray:
    """Smooth an image with Gaussian convolution performed through FFT."""
    kernel = gaussian_kernel(
        kernel_size,
        sigma,
    )

    return fft_convolve2d(
        values,
        kernel,
    )


def sobel_edges(
    values,
) -> np.ndarray:
    """Compute Sobel edge magnitude using FFT-based convolution."""
    image = _as_image(
        values
    )

    kernel_x = np.array(
        [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1],
        ],
        dtype=float,
    )

    kernel_y = np.array(
        [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1],
        ],
        dtype=float,
    )

    gradient_x = fft_convolve2d(
        image,
        kernel_x,
    )

    gradient_y = fft_convolve2d(
        image,
        kernel_y,
    )

    return np.sqrt(
        gradient_x * gradient_x
        + gradient_y * gradient_y
    )


def laplacian_edges(
    values,
) -> np.ndarray:
    """Compute Laplacian edge magnitude using FFT-based convolution."""
    kernel = np.array(
        [
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0],
        ],
        dtype=float,
    )

    response = fft_convolve2d(
        values,
        kernel,
    )

    return np.abs(
        response
    )


def frequency_denoise(
    values,
    *,
    cutoff_ratio: float = 0.25,
) -> np.ndarray:
    """
    Remove high spatial frequencies with a circular low-pass mask.

    cutoff_ratio is measured relative to the Nyquist frequency:
        1.0 keeps frequencies through the Nyquist radius
        smaller values increasingly smooth the image
    """
    image = _as_image(
        values
    )

    try:
        cutoff_ratio = float(
            cutoff_ratio
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "cutoff_ratio must be numeric."
        ) from exc

    if (
        not math.isfinite(
            cutoff_ratio
        )
        or cutoff_ratio <= 0
        or cutoff_ratio > 1
    ):
        raise ValueError(
            "cutoff_ratio must be in the interval (0, 1]."
        )

    padded, original_shape = (
        pad_image_to_power_of_two(
            image
        )
    )

    rows, columns = (
        padded.shape
    )

    spectrum = fft2(
        padded
    )

    row_indices = np.arange(
        rows,
        dtype=float,
    )

    column_indices = np.arange(
        columns,
        dtype=float,
    )

    row_frequencies = (
        row_indices
        / rows
    )

    column_frequencies = (
        column_indices
        / columns
    )

    row_frequencies[
        row_indices > rows // 2
    ] -= 1.0

    column_frequencies[
        column_indices > columns // 2
    ] -= 1.0

    frequency_x, frequency_y = (
        np.meshgrid(
            column_frequencies,
            row_frequencies,
        )
    )

    radius = np.sqrt(
        frequency_x
        * frequency_x
        + frequency_y
        * frequency_y
    )

    cutoff = (
        0.5
        * cutoff_ratio
    )

    mask = (
        radius
        <= cutoff
    )

    filtered_spectrum = (
        spectrum
        * mask
    )

    reconstructed = np.real(
        ifft2(
            filtered_spectrum
        )
    )

    original_rows, original_columns = (
        original_shape
    )

    return reconstructed[
        :original_rows,
        :original_columns,
    ]


def sharpen_image(
    values,
    *,
    amount: float = 1.0,
    kernel_size: int = 5,
    sigma: float = 1.0,
) -> np.ndarray:
    """
    Sharpen an image with an FFT-based unsharp-mask approach.

    A Gaussian-blurred image is subtracted from the original to isolate
    detail, then the detail is added back at the requested amount.
    """
    image = _as_image(
        values
    )

    try:
        amount = float(
            amount
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "amount must be numeric."
        ) from exc

    if (
        not math.isfinite(
            amount
        )
        or amount < 0
    ):
        raise ValueError(
            "amount must be nonnegative and finite."
        )

    blurred = gaussian_blur(
        image,
        kernel_size=kernel_size,
        sigma=sigma,
    )

    detail = (
        image
        - blurred
    )

    return (
        image
        + amount
        * detail
    )