"""Image processing workflows for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.image as mpimg
import numpy as np

from FFTAnalyzer.fft_analyzer.image.compression import (
    compress_and_reconstruct,
    mean_squared_error,
    peak_signal_to_noise_ratio,
)
from FFTAnalyzer.fft_analyzer.image.filters import (
    fft2,
    frequency_denoise,
    gaussian_blur,
    laplacian_edges,
    pad_image_to_power_of_two,
    sharpen_image,
    sobel_edges,
)


def _as_gray_image(values) -> np.ndarray:
    """Convert numeric image data to a two-dimensional grayscale array."""
    try:
        image = np.asarray(
            values,
            dtype=float,
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Image must contain numeric values."
        ) from exc

    if image.size == 0:
        raise ValueError(
            "Image cannot be empty."
        )

    if image.ndim == 2:
        gray = image.copy()

    elif (
        image.ndim == 3
        and image.shape[2] >= 3
    ):
        red = image[
            :,
            :,
            0,
        ]

        green = image[
            :,
            :,
            1,
        ]

        blue = image[
            :,
            :,
            2,
        ]

        gray = (
            0.299 * red
            + 0.587 * green
            + 0.114 * blue
        )

    else:
        raise ValueError(
            "Image must be grayscale, RGB, or RGBA."
        )

    if not np.all(
        np.isfinite(gray)
    ):
        raise ValueError(
            "Image must contain finite values."
        )

    return gray.astype(
        float
    )


def load_image(
    path,
) -> np.ndarray:
    """
    Load an image file as grayscale values in approximately [0, 255].

    Matplotlib commonly returns PNG image data in [0, 1], so those
    values are scaled to the conventional 8-bit image range.
    """
    file_path = Path(
        path
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Image file not found: {file_path}"
        )

    data = mpimg.imread(
        file_path
    )

    data = np.asarray(
        data
    )

    if (
        np.issubdtype(
            data.dtype,
            np.floating,
        )
        and data.size > 0
        and np.min(data) >= 0.0
        and np.max(data) <= 1.0
    ):
        data = (
            data.astype(float)
            * 255.0
        )

    return _as_gray_image(
        data
    )


def save_image(
    path,
    values,
) -> None:
    """Save a grayscale image after clipping values to [0, 255]."""
    image = _as_gray_image(
        values
    )

    clipped = np.clip(
        image,
        0.0,
        255.0,
    )

    file_path = Path(
        path
    )

    if file_path.parent != Path("."):
        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    mpimg.imsave(
        file_path,
        clipped,
        cmap="gray",
        vmin=0.0,
        vmax=255.0,
    )


def apply_image_filter(
    values,
    *,
    filter_type: str,
    kernel_size: int = 5,
    sigma: float = 1.0,
    cutoff_ratio: float = 0.25,
    sharpen_amount: float = 1.0,
) -> np.ndarray:
    """Apply one of the project's FFT-based image filters."""
    image = _as_gray_image(
        values
    )

    normalized = str(
        filter_type
    ).lower()

    if normalized in {
        "blur",
        "gaussian",
        "gaussian-blur",
    }:
        return gaussian_blur(
            image,
            kernel_size=kernel_size,
            sigma=sigma,
        )

    if normalized in {
        "sobel",
        "sobel-edge",
        "sobel-edges",
    }:
        return sobel_edges(
            image
        )

    if normalized in {
        "laplacian",
        "laplacian-edge",
        "laplacian-edges",
    }:
        return laplacian_edges(
            image
        )

    if normalized in {
        "denoise",
        "low-pass",
        "frequency-denoise",
    }:
        return frequency_denoise(
            image,
            cutoff_ratio=cutoff_ratio,
        )

    if normalized in {
        "sharpen",
        "sharp",
    }:
        return sharpen_image(
            image,
            amount=sharpen_amount,
            kernel_size=kernel_size,
            sigma=sigma,
        )

    raise ValueError(
        "filter_type must be blur, sobel, laplacian, "
        "denoise, or sharpen."
    )


def frequency_magnitude(
    values,
    *,
    logarithmic: bool = True,
) -> np.ndarray:
    """
    Return a centered 2D FFT magnitude view.

    Non-power-of-two image dimensions are padded automatically.
    """
    image = _as_gray_image(
        values
    )

    padded, _ = pad_image_to_power_of_two(
        image
    )

    spectrum = fft2(
        padded
    )

    magnitude = np.abs(
        spectrum
    )

    if logarithmic:
        magnitude = np.log1p(
            magnitude
        )

    rows, columns = (
        magnitude.shape
    )

    centered = np.roll(
        magnitude,
        shift=rows // 2,
        axis=0,
    )

    centered = np.roll(
        centered,
        shift=columns // 2,
        axis=1,
    )

    return centered


def compress_image_array(
    values,
    *,
    quality: int = 50,
) -> dict[str, object]:
    """Compress and reconstruct an image while reporting quality metrics."""
    image = _as_gray_image(
        values
    )

    reconstructed, compressed = (
        compress_and_reconstruct(
            image,
            quality=quality,
        )
    )

    mse = mean_squared_error(
        image,
        reconstructed,
    )

    psnr = peak_signal_to_noise_ratio(
        image,
        reconstructed,
    )

    return {
        "reconstructed": reconstructed,
        "compressed": compressed,
        "mse": mse,
        "psnr": psnr,
        "zero_fraction": float(
            compressed[
                "zero_fraction"
            ]
        ),
        "quality": int(
            quality
        ),
    }


def process_image_file(
    input_path,
    output_path,
    *,
    filter_type: str,
    kernel_size: int = 5,
    sigma: float = 1.0,
    cutoff_ratio: float = 0.25,
    sharpen_amount: float = 1.0,
) -> dict[str, object]:
    """Load, filter, and save an image."""
    image = load_image(
        input_path
    )

    result = apply_image_filter(
        image,
        filter_type=filter_type,
        kernel_size=kernel_size,
        sigma=sigma,
        cutoff_ratio=cutoff_ratio,
        sharpen_amount=sharpen_amount,
    )

    save_image(
        output_path,
        result,
    )

    return {
        "input_shape": image.shape,
        "output_shape": result.shape,
        "filter_type": str(
            filter_type
        ),
        "output_path": str(
            output_path
        ),
    }


def compress_image_file(
    input_path,
    output_path,
    *,
    quality: int = 50,
) -> dict[str, object]:
    """Load, DCT-compress, reconstruct, and save an image."""
    image = load_image(
        input_path
    )

    result = compress_image_array(
        image,
        quality=quality,
    )

    save_image(
        output_path,
        result[
            "reconstructed"
        ],
    )

    return {
        "input_shape": image.shape,
        "output_shape": result[
            "reconstructed"
        ].shape,
        "quality": quality,
        "mse": result[
            "mse"
        ],
        "psnr": result[
            "psnr"
        ],
        "zero_fraction": result[
            "zero_fraction"
        ],
        "output_path": str(
            output_path
        ),
    }