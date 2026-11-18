"""Numerical stability utilities for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import math

import numpy as np

from FFTAnalyzer.fft_analyzer.core.matrix import (
    power_method,
    solve_linear_system,
)


DEFAULT_CONDITION_THRESHOLD = 1e10
ZERO_TOLERANCE = 1e-15


def _as_numeric_array(value) -> np.ndarray:
    """Convert input into a floating-point NumPy array."""
    try:
        result = np.asarray(
            value,
            dtype=float,
        )
    except (TypeError, ValueError) as exc:
        raise TypeError(
            "Input must contain numeric values."
        ) from exc

    if result.size == 0:
        raise ValueError(
            "Input cannot be empty."
        )

    return result


def _as_matrix(matrix) -> np.ndarray:
    """Convert input to a non-empty two-dimensional float matrix."""
    result = _as_numeric_array(
        matrix
    )

    if result.ndim != 2:
        raise ValueError(
            "Matrix must be two-dimensional."
        )

    if (
        result.shape[0] == 0
        or result.shape[1] == 0
    ):
        raise ValueError(
            "Matrix cannot be empty."
        )

    return result.copy()


def absolute_error(
    actual,
    approximation,
):
    """
    Compute absolute error.

    Scalars return a float. Arrays return an array containing
    element-by-element absolute error.
    """
    actual_array = _as_numeric_array(
        actual
    )

    approximation_array = _as_numeric_array(
        approximation
    )

    if (
        actual_array.shape
        != approximation_array.shape
    ):
        raise ValueError(
            "Inputs must have matching shapes."
        )

    result = np.abs(
        actual_array
        - approximation_array
    )

    if result.ndim == 0:
        return float(result)

    return result


def relative_error(
    actual,
    approximation,
    *,
    zero_tolerance: float = ZERO_TOLERANCE,
):
    """
    Compute relative error |actual - approximation| / |actual|.

    When the actual value is effectively zero:
    - error is 0 if approximation is also effectively zero
    - error is infinity otherwise
    """
    if zero_tolerance < 0:
        raise ValueError(
            "zero_tolerance cannot be negative."
        )

    actual_array = _as_numeric_array(
        actual
    )

    approximation_array = _as_numeric_array(
        approximation
    )

    if (
        actual_array.shape
        != approximation_array.shape
    ):
        raise ValueError(
            "Inputs must have matching shapes."
        )

    difference = np.abs(
        actual_array
        - approximation_array
    )

    denominator = np.abs(
        actual_array
    )

    result = np.empty_like(
        difference,
        dtype=float,
    )

    nonzero_mask = (
        denominator
        > zero_tolerance
    )

    result[nonzero_mask] = (
        difference[nonzero_mask]
        / denominator[nonzero_mask]
    )

    zero_mask = ~nonzero_mask

    result[
        zero_mask
        & (
            difference
            <= zero_tolerance
        )
    ] = 0.0

    result[
        zero_mask
        & (
            difference
            > zero_tolerance
        )
    ] = np.inf

    if result.ndim == 0:
        return float(result)

    return result


def l1_norm(values) -> float:
    """Return the L1 norm of a vector or matrix entries."""
    array = _as_numeric_array(
        values
    )

    return float(
        np.sum(
            np.abs(array)
        )
    )


def l2_norm(values) -> float:
    """Return the Euclidean/Frobenius L2 norm."""
    array = _as_numeric_array(
        values
    )

    return float(
        np.sqrt(
            np.sum(
                array * array
            )
        )
    )


def infinity_norm(values) -> float:
    """
    Return the infinity norm.

    For vectors this is the maximum absolute value.
    For matrices this is the maximum absolute row sum.
    """
    array = _as_numeric_array(
        values
    )

    if array.ndim == 1:
        return float(
            np.max(
                np.abs(array)
            )
        )

    if array.ndim == 2:
        row_sums = np.sum(
            np.abs(array),
            axis=1,
        )

        return float(
            np.max(
                row_sums
            )
        )

    raise ValueError(
        "Infinity norm supports vectors or matrices only."
    )


def matrix_one_norm(matrix) -> float:
    """Return the matrix 1-norm: maximum absolute column sum."""
    a = _as_matrix(
        matrix
    )

    column_sums = np.sum(
        np.abs(a),
        axis=0,
    )

    return float(
        np.max(
            column_sums
        )
    )


def matrix_infinity_norm(
    matrix,
) -> float:
    """Return the matrix infinity norm: maximum absolute row sum."""
    return infinity_norm(
        _as_matrix(matrix)
    )


def inverse_matrix(matrix) -> np.ndarray:
    """
    Compute the inverse by solving Ax = e_i for each identity column.

    This deliberately reuses the project's LU-based linear-system solver.
    """
    a = _as_matrix(
        matrix
    )

    rows, columns = a.shape

    if rows != columns:
        raise ValueError(
            "Matrix must be square."
        )

    inverse = np.zeros(
        (rows, columns),
        dtype=float,
    )

    identity = np.eye(
        rows,
        dtype=float,
    )

    for column in range(
        columns
    ):
        inverse[
            :,
            column,
        ] = solve_linear_system(
            a,
            identity[
                :,
                column,
            ],
        )

    return inverse


def spectral_norm_estimate(
    matrix,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> float:
    """
    Estimate the matrix 2-norm using the dominant eigenvalue of A^T A.
    """
    a = _as_matrix(
        matrix
    )

    gram = a.T @ a

    eigenvalue, _, _ = power_method(
        gram,
        tolerance=tolerance,
        max_iterations=max_iterations,
    )

    if eigenvalue < 0:
        eigenvalue = 0.0

    return float(
        math.sqrt(
            eigenvalue
        )
    )


def condition_number(
    matrix,
    *,
    norm: str = "1",
) -> float:
    """
    Estimate the condition number of a nonsingular square matrix.

    Supported norms:
        "1"   - matrix 1-norm
        "2"   - spectral norm estimate
        "inf" - matrix infinity norm
    """
    a = _as_matrix(
        matrix
    )

    rows, columns = a.shape

    if rows != columns:
        raise ValueError(
            "Condition number requires a square matrix."
        )

    inverse = inverse_matrix(
        a
    )

    normalized = str(
        norm
    ).lower()

    if normalized in {
        "1",
        "l1",
    }:
        return (
            matrix_one_norm(a)
            * matrix_one_norm(
                inverse
            )
        )

    if normalized in {
        "2",
        "l2",
    }:
        return (
            spectral_norm_estimate(a)
            * spectral_norm_estimate(
                inverse
            )
        )

    if normalized in {
        "inf",
        "infinity",
    }:
        return (
            matrix_infinity_norm(a)
            * matrix_infinity_norm(
                inverse
            )
        )

    raise ValueError(
        "norm must be '1', '2', or 'inf'."
    )


def is_ill_conditioned(
    matrix,
    *,
    threshold: float = DEFAULT_CONDITION_THRESHOLD,
    norm: str = "1",
) -> bool:
    """Return True when the estimated condition number exceeds threshold."""
    if threshold <= 0:
        raise ValueError(
            "threshold must be positive."
        )

    value = condition_number(
        matrix,
        norm=norm,
    )

    return bool(
        value >= threshold
    )


def cancellation_demo(
    x: float = 1e16,
) -> dict[str, float]:
    """
    Demonstrate catastrophic cancellation.

    The expression:

        sqrt(x + 1) - sqrt(x)

    loses precision for large x because two nearly equal values are
    subtracted. The algebraically equivalent expression:

        1 / (sqrt(x + 1) + sqrt(x))

    is numerically more stable.
    """
    x = float(x)

    if x <= 0:
        raise ValueError(
            "x must be positive."
        )

    root_x_plus_one = math.sqrt(
        x + 1.0
    )

    root_x = math.sqrt(
        x
    )

    naive = (
        root_x_plus_one
        - root_x
    )

    stable = (
        1.0
        / (
            root_x_plus_one
            + root_x
        )
    )

    abs_err = abs(
        naive - stable
    )

    if stable == 0.0:
        rel_err = (
            0.0
            if abs_err == 0.0
            else math.inf
        )
    else:
        rel_err = (
            abs_err
            / abs(stable)
        )

    return {
        "x": x,
        "naive": naive,
        "stable": stable,
        "absolute_error": abs_err,
        "relative_error": rel_err,
    }


def residual_norm(
    matrix,
    solution,
    vector,
) -> float:
    """Compute ||Ax - b||_2 for a proposed linear-system solution."""
    a = _as_matrix(
        matrix
    )

    x = _as_numeric_array(
        solution
    )

    b = _as_numeric_array(
        vector
    )

    if (
        x.ndim != 1
        or b.ndim != 1
    ):
        raise ValueError(
            "solution and vector must be one-dimensional."
        )

    if (
        a.shape[1] != x.size
        or a.shape[0] != b.size
    ):
        raise ValueError(
            "Matrix and vector dimensions do not agree."
        )

    residual = (
        a @ x
        - b
    )

    return l2_norm(
        residual
    )