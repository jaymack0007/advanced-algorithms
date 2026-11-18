"""Core matrix algorithms for the Week 12 FFTAnalyzer project."""

from __future__ import annotations

import numpy as np


PIVOT_TOLERANCE = 1e-12


def _as_float_matrix(matrix) -> np.ndarray:
    """Convert input to a two-dimensional floating-point NumPy array."""
    result = np.asarray(matrix, dtype=float)

    if result.ndim != 2:
        raise ValueError("Matrix must be two-dimensional.")

    if result.shape[0] == 0 or result.shape[1] == 0:
        raise ValueError("Matrix cannot be empty.")

    return result.copy()


def _as_float_vector(vector) -> np.ndarray:
    """Convert input to a one-dimensional floating-point NumPy array."""
    result = np.asarray(vector, dtype=float)

    if result.ndim != 1:
        raise ValueError("Vector must be one-dimensional.")

    if result.size == 0:
        raise ValueError("Vector cannot be empty.")

    return result.copy()


def _validate_square(matrix: np.ndarray) -> None:
    """Raise an error if a matrix is not square."""
    rows, columns = matrix.shape

    if rows != columns:
        raise ValueError("Matrix must be square.")


def classical_matrix_multiply(left, right) -> np.ndarray:
    """
    Multiply two matrices using the classical O(n^3) algorithm.

    This implementation intentionally uses explicit loops instead of
    np.matmul so the algorithmic work is visible.
    """
    a = _as_float_matrix(left)
    b = _as_float_matrix(right)

    if a.shape[1] != b.shape[0]:
        raise ValueError(
            "Inner matrix dimensions must agree for multiplication."
        )

    rows = a.shape[0]
    inner = a.shape[1]
    columns = b.shape[1]

    result = np.zeros(
        (rows, columns),
        dtype=float,
    )

    for i in range(rows):
        for k in range(inner):
            a_ik = a[i, k]

            for j in range(columns):
                result[i, j] += a_ik * b[k, j]

    return result


def lu_decomposition(matrix) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute the LUP decomposition PA = LU using partial pivoting.

    Returns:
        P: permutation matrix
        L: lower triangular matrix with ones on the diagonal
        U: upper triangular matrix
    """
    a = _as_float_matrix(matrix)
    _validate_square(a)

    n = a.shape[0]

    p = np.eye(
        n,
        dtype=float,
    )

    l = np.eye(
        n,
        dtype=float,
    )

    u = a.copy()

    for column in range(n):
        pivot_offset = int(
            np.argmax(
                np.abs(
                    u[column:, column]
                )
            )
        )

        pivot_row = column + pivot_offset
        pivot_value = abs(
            u[pivot_row, column]
        )

        if pivot_value < PIVOT_TOLERANCE:
            raise ValueError(
                "Matrix is singular or nearly singular."
            )

        if pivot_row != column:
            u[
                [column, pivot_row],
                :,
            ] = u[
                [pivot_row, column],
                :,
            ]

            p[
                [column, pivot_row],
                :,
            ] = p[
                [pivot_row, column],
                :,
            ]

            if column > 0:
                l[
                    [column, pivot_row],
                    :column,
                ] = l[
                    [pivot_row, column],
                    :column,
                ]

        for row in range(
            column + 1,
            n,
        ):
            factor = (
                u[row, column]
                / u[column, column]
            )

            l[row, column] = factor

            u[row, column:] -= (
                factor
                * u[column, column:]
            )

            u[row, column] = 0.0

    return p, l, u


def forward_substitution(
    lower,
    vector,
) -> np.ndarray:
    """Solve Ly = b for a lower triangular matrix L."""
    l = _as_float_matrix(lower)
    b = _as_float_vector(vector)

    _validate_square(l)

    n = l.shape[0]

    if b.size != n:
        raise ValueError(
            "Vector length must match matrix size."
        )

    solution = np.zeros(
        n,
        dtype=float,
    )

    for row in range(n):
        diagonal = l[row, row]

        if abs(diagonal) < PIVOT_TOLERANCE:
            raise ValueError(
                "Lower triangular matrix has a zero diagonal."
            )

        subtotal = 0.0

        for column in range(row):
            subtotal += (
                l[row, column]
                * solution[column]
            )

        solution[row] = (
            b[row] - subtotal
        ) / diagonal

    return solution


def back_substitution(
    upper,
    vector,
) -> np.ndarray:
    """Solve Ux = y for an upper triangular matrix U."""
    u = _as_float_matrix(upper)
    b = _as_float_vector(vector)

    _validate_square(u)

    n = u.shape[0]

    if b.size != n:
        raise ValueError(
            "Vector length must match matrix size."
        )

    solution = np.zeros(
        n,
        dtype=float,
    )

    for row in range(
        n - 1,
        -1,
        -1,
    ):
        diagonal = u[row, row]

        if abs(diagonal) < PIVOT_TOLERANCE:
            raise ValueError(
                "Upper triangular matrix has a zero diagonal."
            )

        subtotal = 0.0

        for column in range(
            row + 1,
            n,
        ):
            subtotal += (
                u[row, column]
                * solution[column]
            )

        solution[row] = (
            b[row] - subtotal
        ) / diagonal

    return solution


def solve_linear_system(
    matrix,
    vector,
) -> np.ndarray:
    """
    Solve Ax = b using LUP decomposition.

    After the O(n^3) factorization, forward and back substitution
    each require O(n^2) work.
    """
    a = _as_float_matrix(matrix)
    b = _as_float_vector(vector)

    _validate_square(a)

    if a.shape[0] != b.size:
        raise ValueError(
            "Vector length must match matrix size."
        )

    p, l, u = lu_decomposition(a)

    permuted_b = p @ b

    y = forward_substitution(
        l,
        permuted_b,
    )

    return back_substitution(
        u,
        y,
    )


def determinant(matrix) -> float:
    """Compute a matrix determinant using LUP decomposition."""
    a = _as_float_matrix(matrix)
    _validate_square(a)

    p, _, u = lu_decomposition(a)

    permutation_count = 0
    permutation = np.argmax(
        p,
        axis=1,
    )

    visited = [
        False
        for _ in range(
            len(permutation)
        )
    ]

    for start in range(
        len(permutation)
    ):
        if visited[start]:
            continue

        cycle_length = 0
        current = start

        while not visited[current]:
            visited[current] = True
            current = int(
                permutation[current]
            )
            cycle_length += 1

        if cycle_length > 0:
            permutation_count += (
                cycle_length - 1
            )

    sign = (
        -1.0
        if permutation_count % 2
        else 1.0
    )

    diagonal_product = 1.0

    for index in range(
        u.shape[0]
    ):
        diagonal_product *= u[
            index,
            index,
        ]

    return float(
        sign * diagonal_product
    )


def qr_decomposition(
    matrix,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute QR decomposition using Householder reflections.

    Householder reflections are generally more numerically stable than
    classical Gram-Schmidt orthogonalization.
    """
    a = _as_float_matrix(matrix)

    rows, columns = a.shape

    if rows < columns:
        raise ValueError(
            "QR decomposition requires rows >= columns."
        )

    q = np.eye(
        rows,
        dtype=float,
    )

    r = a.copy()

    for column in range(
        min(
            rows,
            columns,
        )
    ):
        x = r[
            column:,
            column,
        ]

        norm_x = float(
            np.sqrt(
                np.dot(
                    x,
                    x,
                )
            )
        )

        if norm_x < PIVOT_TOLERANCE:
            continue

        sign = (
            1.0
            if x[0] >= 0.0
            else -1.0
        )

        v = x.copy()
        v[0] += sign * norm_x

        norm_v = float(
            np.sqrt(
                np.dot(
                    v,
                    v,
                )
            )
        )

        if norm_v < PIVOT_TOLERANCE:
            continue

        v /= norm_v

        r[
            column:,
            column:,
        ] -= (
            2.0
            * np.outer(
                v,
                v @ r[
                    column:,
                    column:,
                ],
            )
        )

        q[
            :,
            column:,
        ] -= (
            2.0
            * np.outer(
                q[
                    :,
                    column:
                ] @ v,
                v,
            )
        )

    r[
        np.abs(r)
        < PIVOT_TOLERANCE
    ] = 0.0

    return q, r


def power_method(
    matrix,
    *,
    max_iterations: int = 1000,
    tolerance: float = 1e-10,
    initial_vector=None,
) -> tuple[float, np.ndarray, int]:
    """
    Approximate the dominant eigenvalue and eigenvector.

    Returns:
        eigenvalue
        normalized eigenvector
        iterations used
    """
    a = _as_float_matrix(matrix)
    _validate_square(a)

    if not isinstance(
        max_iterations,
        int,
    ):
        raise TypeError(
            "max_iterations must be an integer."
        )

    if max_iterations <= 0:
        raise ValueError(
            "max_iterations must be positive."
        )

    if tolerance <= 0:
        raise ValueError(
            "tolerance must be positive."
        )

    n = a.shape[0]

    if initial_vector is None:
        vector = np.ones(
            n,
            dtype=float,
        )
    else:
        vector = _as_float_vector(
            initial_vector
        )

        if vector.size != n:
            raise ValueError(
                "Initial vector length must match matrix size."
            )

    vector_norm = float(
        np.sqrt(
            np.dot(
                vector,
                vector,
            )
        )
    )

    if vector_norm < PIVOT_TOLERANCE:
        raise ValueError(
            "Initial vector cannot be the zero vector."
        )

    vector /= vector_norm

    previous_eigenvalue = None

    for iteration in range(
        1,
        max_iterations + 1,
    ):
        next_vector = a @ vector

        next_norm = float(
            np.sqrt(
                np.dot(
                    next_vector,
                    next_vector,
                )
            )
        )

        if next_norm < PIVOT_TOLERANCE:
            return (
                0.0,
                vector,
                iteration,
            )

        next_vector /= next_norm

        eigenvalue = float(
            next_vector
            @ (
                a
                @ next_vector
            )
        )

        if previous_eigenvalue is not None:
            eigenvalue_change = abs(
                eigenvalue
                - previous_eigenvalue
            )

            vector_change = min(
                float(
                    np.max(
                        np.abs(
                            next_vector
                            - vector
                        )
                    )
                ),
                float(
                    np.max(
                        np.abs(
                            next_vector
                            + vector
                        )
                    )
                ),
            )

            if (
                eigenvalue_change
                <= tolerance
                and vector_change
                <= np.sqrt(tolerance)
            ):
                return (
                    eigenvalue,
                    next_vector,
                    iteration,
                )

        vector = next_vector
        previous_eigenvalue = eigenvalue

    return (
        eigenvalue,
        vector,
        max_iterations,
    )


# Simple aliases for convenient public use.
matrix_multiply = classical_matrix_multiply
lu_solve = solve_linear_system