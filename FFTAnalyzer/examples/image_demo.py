"""Image-processing demonstration for the Week 12 FFTAnalyzer project."""

from pathlib import Path

import numpy as np

from FFTAnalyzer.fft_analyzer.applications.image_processor import (
    apply_image_filter,
    compress_image_array,
    frequency_magnitude,
    save_image,
)


PROJECT_ROOT = Path(
    __file__
).resolve().parent.parent

RESULTS_DIR = (
    PROJECT_ROOT
    / "results"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def create_test_image(
    size: int = 128,
) -> np.ndarray:
    """Create a deterministic grayscale image for the demonstration."""
    axis = np.linspace(
        0.0,
        180.0,
        size,
    )

    image = np.tile(
        axis,
        (
            size,
            1,
        ),
    )

    image[
        24:64,
        20:60,
    ] = 240.0

    image[
        72:108,
        70:112,
    ] = 40.0

    rows, columns = np.indices(
        (
            size,
            size,
        )
    )

    circle = (
        (
            rows - 72
        )
        ** 2
        + (
            columns - 40
        )
        ** 2
        <= 15**2
    )

    image[
        circle
    ] = 210.0

    return np.clip(
        image,
        0.0,
        255.0,
    )


def main() -> None:
    """Filter, analyze, compress, and save a sample image."""
    image = create_test_image()

    blurred = apply_image_filter(
        image,
        filter_type="blur",
        kernel_size=7,
        sigma=1.5,
    )

    edges = apply_image_filter(
        image,
        filter_type="sobel",
    )

    sharpened = apply_image_filter(
        image,
        filter_type="sharpen",
        sharpen_amount=1.0,
        kernel_size=5,
        sigma=1.0,
    )

    frequency_view = frequency_magnitude(
        image,
        logarithmic=True,
    )

    compression = compress_image_array(
        image,
        quality=50,
    )

    reconstructed = compression[
        "reconstructed"
    ]

    original_path = (
        RESULTS_DIR
        / "image_demo_original.png"
    )

    blur_path = (
        RESULTS_DIR
        / "image_demo_blur.png"
    )

    edges_path = (
        RESULTS_DIR
        / "image_demo_edges.png"
    )

    sharpen_path = (
        RESULTS_DIR
        / "image_demo_sharpen.png"
    )

    frequency_path = (
        RESULTS_DIR
        / "image_demo_frequency.png"
    )

    compressed_path = (
        RESULTS_DIR
        / "image_demo_compressed.png"
    )

    save_image(
        original_path,
        image,
    )

    save_image(
        blur_path,
        blurred,
    )

    save_image(
        edges_path,
        edges,
    )

    save_image(
        sharpen_path,
        sharpened,
    )

    save_image(
        frequency_path,
        frequency_view,
    )

    save_image(
        compressed_path,
        reconstructed,
    )

    print(
        "Week 12 Image Demo"
    )

    print(
        "-" * 60
    )

    print(
        f"Image size: {image.shape}"
    )

    print(
        f"Compression quality: "
        f"{compression['quality']}"
    )

    print(
        f"MSE: "
        f"{compression['mse']:.4f}"
    )

    print(
        f"PSNR: "
        f"{compression['psnr']:.4f} dB"
    )

    print(
        f"Zero coefficients: "
        f"{compression['zero_fraction']:.2%}"
    )

    print()

    print(
        "Saved:"
    )

    for path in [
        original_path,
        blur_path,
        edges_path,
        sharpen_path,
        frequency_path,
        compressed_path,
    ]:
        print(
            path
        )


if __name__ == "__main__":
    main()