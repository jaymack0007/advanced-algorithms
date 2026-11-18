"""Fast Fourier Transform algorithms for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import math

import numpy as np


def _as_complex_vector(values) -> np.ndarray:
    """Convert input to a non-empty one-dimensional complex array."""
    try:
        result = np.asarray(
            values,
            dtype=complex,
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Input must contain numeric values."
        ) from exc

    if result.ndim != 1:
        raise ValueError(
            "Input must be one-dimensional."
        )

    if result.size == 0:
        raise ValueError(
            "Input cannot be empty."
        )

    return result.copy()


def is_power_of_two(value: int) -> bool:
    """Return True when value is a positive power of two."""
    return (
        isinstance(value, int)
        and value > 0
        and (
            value
            & (
                value - 1
            )
        )
        == 0
    )


def next_power_of_two(value: int) -> int:
    """Return the smallest power of two greater than or equal to value."""
    if not isinstance(
        value,
        int,
    ):
        raise TypeError(
            "value must be an integer."
        )

    if value <= 0:
        raise ValueError(
            "value must be positive."
        )

    if is_power_of_two(
        value
    ):
        return value

    return 1 << (
        value - 1
    ).bit_length()


def _validate_fft_length(
    length: int,
) -> None:
    """Require a radix-2 transform length."""
    if not is_power_of_two(
        length
    ):
        raise ValueError(
            "FFT input length must be a power of two."
        )


def recursive_fft(values) -> np.ndarray:
    """
    Compute the radix-2 Cooley-Tukey FFT recursively.

    The recurrence divides the sequence into its even- and odd-indexed
    values and combines the two half-sized FFTs with roots of unity.

    Time complexity:
        O(n log n)

    Space complexity:
        O(n log n) in this educational recursive implementation because
        each level creates array slices and intermediate arrays.
    """
    data = _as_complex_vector(
        values
    )

    _validate_fft_length(
        data.size
    )

    n = data.size

    if n == 1:
        return data.copy()

    even = recursive_fft(
        data[::2]
    )

    odd = recursive_fft(
        data[1::2]
    )

    half = n // 2

    roots = np.exp(
        -2j
        * np.pi
        * np.arange(half)
        / n
    )

    weighted_odd = (
        roots
        * odd
    )

    return np.concatenate(
        (
            even + weighted_odd,
            even - weighted_odd,
        )
    )


def bit_reversal_permutation(
    length: int,
) -> np.ndarray:
    """
    Return the bit-reversed index order for a radix-2 FFT.

    Example for length 8:

        0, 4, 2, 6, 1, 5, 3, 7
    """
    if not isinstance(
        length,
        int,
    ):
        raise TypeError(
            "length must be an integer."
        )

    _validate_fft_length(
        length
    )

    bits = (
        length.bit_length()
        - 1
    )

    indices = np.arange(
        length,
        dtype=np.uint64,
    )

    remaining = (
        indices.copy()
    )

    reversed_indices = np.zeros(
        length,
        dtype=np.uint64,
    )

    for _ in range(bits):
        reversed_indices = (
            reversed_indices
            << np.uint64(1)
        ) | (
            remaining
            & np.uint64(1)
        )

        remaining = (
            remaining
            >> np.uint64(1)
        )

    return reversed_indices.astype(
        np.int64
    )


def iterative_fft(values) -> np.ndarray:
    """
    Compute the radix-2 FFT using iterative butterfly stages.

    The input is first placed in bit-reversed order. Each stage then
    combines increasingly larger blocks using the corresponding roots
    of unity.

    NumPy is used for array storage and vectorized butterfly arithmetic,
    but the FFT stages and bit-reversal algorithm are implemented here
    rather than delegated to numpy.fft.
    """
    data = _as_complex_vector(
        values
    )

    n = data.size

    _validate_fft_length(
        n
    )

    if n == 1:
        return data.copy()

    ordering = (
        bit_reversal_permutation(
            n
        )
    )

    transformed = (
        data[ordering]
        .astype(
            complex,
            copy=True,
        )
    )

    block_size = 2

    while block_size <= n:
        half = (
            block_size
            // 2
        )

        roots = np.exp(
            -2j
            * np.pi
            * np.arange(half)
            / block_size
        )

        blocks = transformed.reshape(
            -1,
            block_size,
        )

        even_part = (
            blocks[
                :,
                :half,
            ].copy()
        )

        odd_part = (
            blocks[
                :,
                half:,
            ].copy()
        )

        weighted_odd = (
            odd_part
            * roots
        )

        blocks[
            :,
            :half,
        ] = (
            even_part
            + weighted_odd
        )

        blocks[
            :,
            half:,
        ] = (
            even_part
            - weighted_odd
        )

        block_size *= 2

    return transformed


def fft(
    values,
    *,
    method: str = "iterative",
) -> np.ndarray:
    """Compute the FFT using either the iterative or recursive method."""
    normalized = str(
        method
    ).lower()

    if normalized in {
        "iterative",
        "iter",
    }:
        return iterative_fft(
            values
        )

    if normalized in {
        "recursive",
        "rec",
    }:
        return recursive_fft(
            values
        )

    raise ValueError(
        "method must be 'iterative' or 'recursive'."
    )


def ifft(
    values,
    *,
    method: str = "iterative",
) -> np.ndarray:
    """
    Compute the inverse FFT using conjugation.

    IFFT(x) = conjugate(FFT(conjugate(x))) / n
    """
    data = _as_complex_vector(
        values
    )

    transformed = fft(
        np.conjugate(
            data
        ),
        method=method,
    )

    return (
        np.conjugate(
            transformed
        )
        / data.size
    )


def circular_convolution(
    left,
    right,
) -> np.ndarray:
    """
    Compute equal-length circular convolution using the FFT.

    Both sequences must have the same power-of-two length because this
    toolkit implements the radix-2 Cooley-Tukey FFT.
    """
    a = _as_complex_vector(
        left
    )

    b = _as_complex_vector(
        right
    )

    if a.size != b.size:
        raise ValueError(
            "Circular convolution requires equal-length inputs."
        )

    _validate_fft_length(
        a.size
    )

    result = ifft(
        iterative_fft(a)
        * iterative_fft(b)
    )

    return np.real_if_close(
        result,
        tol=1000,
    )


def linear_convolution(
    left,
    right,
) -> np.ndarray:
    """
    Compute linear convolution using zero padding and the FFT.

    For input lengths n and m, the exact convolution length is:

        n + m - 1

    The sequences are padded to the next power-of-two transform length.
    """
    a = _as_complex_vector(
        left
    )

    b = _as_complex_vector(
        right
    )

    result_length = (
        a.size
        + b.size
        - 1
    )

    transform_length = (
        next_power_of_two(
            result_length
        )
    )

    padded_a = np.zeros(
        transform_length,
        dtype=complex,
    )

    padded_b = np.zeros(
        transform_length,
        dtype=complex,
    )

    padded_a[
        :a.size
    ] = a

    padded_b[
        :b.size
    ] = b

    result = ifft(
        iterative_fft(
            padded_a
        )
        * iterative_fft(
            padded_b
        )
    )

    result = result[
        :result_length
    ]

    return np.real_if_close(
        result,
        tol=1000,
    )


def direct_dft(values) -> np.ndarray:
    """
    Compute the DFT directly in O(n^2).

    This is included as a small-input reference for demonstrating the
    complexity advantage of the FFT.
    """
    data = _as_complex_vector(
        values
    )

    n = data.size

    output = np.zeros(
        n,
        dtype=complex,
    )

    for frequency in range(n):
        total = 0j

        for sample in range(n):
            angle = (
                -2.0
                * math.pi
                * frequency
                * sample
                / n
            )

            total += (
                data[sample]
                * np.exp(
                    1j
                    * angle
                )
            )

        output[
            frequency
        ] = total

    return output