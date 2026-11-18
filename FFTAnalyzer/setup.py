"""Package configuration for the Week 12 FFTAnalyzer project."""

from setuptools import (
    find_packages,
    setup,
)


setup(
    name="fft-analyzer",
    version="1.0.0",
    description=(
        "Numerical algorithms, FFT, signal processing, "
        "image processing, and analysis toolkit."
    ),
    author="Jaymes McKenzie",
    packages=find_packages(
        exclude=[
            "tests",
            "tests.*",
        ]
    ),
    python_requires=">=3.10",
    install_requires=[
        "numpy",
        "matplotlib",
        "scipy",
    ],
)