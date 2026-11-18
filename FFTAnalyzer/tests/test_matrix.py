"""Tests for Week 12 matrix algorithms."""

import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.core.matrix import (
    back_substitution,
    classical_matrix_multiply,
    determinant,
    forward_substitution,
    lu_decomposition,
    matrix_multiply,
    power_method,
    qr_decomposition,
    solve_linear_system,
)


def test_classical_matrix_multiply_square():
    a = np.array(
        [
            [1, 2],
            [3, 4],
        ],
        dtype=float,
    )

    b = np.array(
        [
            [5, 6],
            [7, 8],
        ],
        dtype=float,
    )

    result = classical_matrix_multiply(
        a,
        b,
    )

    expected = np.array(
        [
            [19, 22],
            [43, 50],
        ],
        dtype=float,
    )

    assert np.allclose(
        result,
        expected,
    )


def test_classical_matrix_multiply_rectangular():
    a = np.array(
        [
            [1, 2, 3],
            [4, 5, 6],
        ],
        dtype=float,
    )

    b = np.array(
        [
            [7, 8],
            [9, 10],
            [11, 12],
        ],
        dtype=float,
    )

    result = classical_matrix_multiply(
        a,
        b,
    )

    assert np.allclose(
        result,
        a @ b,
    )


def test_matrix_multiply_alias():
    a = [
        [1, 2],
        [3, 4],
    ]

    b = [
        [2, 0],
        [1, 2],
    ]

    assert np.allclose(
        matrix_multiply(
            a,
            b,
        ),
        np.asarray(a) @ np.asarray(b),
    )


def test_matrix_multiply_dimension_error():
    with pytest.raises(ValueError):
        classical_matrix_multiply(
            [
                [1, 2],
            ],
            [
                [1, 2],
            ],
        )


def test_lu_decomposition_reconstructs_permuted_matrix():
    a = np.array(
        [
            [2, 1, 1],
            [4, -6, 0],
            [-2, 7, 2],
        ],
        dtype=float,
    )

    p, l, u = lu_decomposition(a)

    assert np.allclose(
        p @ a,
        l @ u,
    )


def test_lu_decomposition_uses_partial_pivoting():
    a = np.array(
        [
            [0, 2],
            [1, 3],
        ],
        dtype=float,
    )

    p, l, u = lu_decomposition(a)

    assert not np.allclose(
        p,
        np.eye(2),
    )

    assert np.allclose(
        p @ a,
        l @ u,
    )


def test_lu_lower_triangular():
    a = np.array(
        [
            [4, 3],
            [6, 3],
        ],
        dtype=float,
    )

    _, l, _ = lu_decomposition(a)

    assert np.allclose(
        l,
        np.tril(l),
    )

    assert np.allclose(
        np.diag(l),
        np.ones(2),
    )


def test_lu_upper_triangular():
    a = np.array(
        [
            [4, 3],
            [6, 3],
        ],
        dtype=float,
    )

    _, _, u = lu_decomposition(a)

    assert np.allclose(
        u,
        np.triu(u),
    )


def test_lu_rejects_nonsquare_matrix():
    with pytest.raises(ValueError):
        lu_decomposition(
            [
                [1, 2, 3],
                [4, 5, 6],
            ]
        )


def test_lu_rejects_singular_matrix():
    with pytest.raises(ValueError):
        lu_decomposition(
            [
                [1, 2],
                [2, 4],
            ]
        )


def test_forward_substitution():
    lower = np.array(
        [
            [1, 0, 0],
            [2, 1, 0],
            [3, 4, 1],
        ],
        dtype=float,
    )

    b = np.array(
        [1, 4, 14],
        dtype=float,
    )

    result = forward_substitution(
        lower,
        b,
    )

    assert np.allclose(
        result,
        [1, 2, 3],
    )


def test_back_substitution():
    upper = np.array(
        [
            [2, 1, 1],
            [0, 3, 2],
            [0, 0, 4],
        ],
        dtype=float,
    )

    expected = np.array(
        [1, 2, 3],
        dtype=float,
    )

    b = upper @ expected

    result = back_substitution(
        upper,
        b,
    )

    assert np.allclose(
        result,
        expected,
    )


def test_solve_linear_system():
    a = np.array(
        [
            [3, 1, -1],
            [2, 4, 1],
            [-1, 2, 5],
        ],
        dtype=float,
    )

    expected = np.array(
        [4, 1, 1],
        dtype=float,
    )

    b = a @ expected

    result = solve_linear_system(
        a,
        b,
    )

    assert np.allclose(
        result,
        expected,
    )


def test_solve_matches_numpy():
    a = np.array(
        [
            [10, 2, 3],
            [3, 15, 1],
            [2, 1, 8],
        ],
        dtype=float,
    )

    b = np.array(
        [7, 8, 9],
        dtype=float,
    )

    result = solve_linear_system(
        a,
        b,
    )

    expected = np.linalg.solve(
        a,
        b,
    )

    assert np.allclose(
        result,
        expected,
    )


def test_determinant_no_swap():
    a = np.array(
        [
            [4, 2],
            [1, 3],
        ],
        dtype=float,
    )

    assert determinant(a) == pytest.approx(
        np.linalg.det(a)
    )


def test_determinant_with_row_swap():
    a = np.array(
        [
            [0, 2],
            [3, 4],
        ],
        dtype=float,
    )

    assert determinant(a) == pytest.approx(
        np.linalg.det(a)
    )


def test_qr_reconstructs_matrix():
    a = np.array(
        [
            [12, -51, 4],
            [6, 167, -68],
            [-4, 24, -41],
        ],
        dtype=float,
    )

    q, r = qr_decomposition(a)

    assert np.allclose(
        q @ r,
        a,
        atol=1e-9,
    )


def test_qr_q_is_orthogonal():
    a = np.array(
        [
            [12, -51, 4],
            [6, 167, -68],
            [-4, 24, -41],
        ],
        dtype=float,
    )

    q, _ = qr_decomposition(a)

    identity = np.eye(
        q.shape[0]
    )

    assert np.allclose(
        q.T @ q,
        identity,
        atol=1e-9,
    )


def test_qr_r_is_upper_triangular():
    a = np.array(
        [
            [12, -51, 4],
            [6, 167, -68],
            [-4, 24, -41],
        ],
        dtype=float,
    )

    _, r = qr_decomposition(a)

    assert np.allclose(
        r,
        np.triu(r),
        atol=1e-9,
    )


def test_qr_rectangular_matrix():
    a = np.array(
        [
            [1, 2],
            [3, 4],
            [5, 6],
        ],
        dtype=float,
    )

    q, r = qr_decomposition(a)

    assert q.shape == (3, 3)
    assert r.shape == (3, 2)

    assert np.allclose(
        q @ r,
        a,
        atol=1e-9,
    )


def test_qr_rejects_wide_matrix():
    with pytest.raises(ValueError):
        qr_decomposition(
            [
                [1, 2, 3],
                [4, 5, 6],
            ]
        )


def test_power_method_dominant_eigenvalue():
    a = np.array(
        [
            [2, 0],
            [0, 5],
        ],
        dtype=float,
    )

    eigenvalue, eigenvector, iterations = power_method(
        a
    )

    assert eigenvalue == pytest.approx(
        5.0,
        rel=1e-8,
    )

    assert abs(
        eigenvector[1]
    ) > 0.999

    assert iterations > 0


def test_power_method_general_matrix():
    a = np.array(
        [
            [4, 1],
            [2, 3],
        ],
        dtype=float,
    )

    eigenvalue, _, _ = power_method(
        a
    )

    expected = max(
        np.linalg.eigvals(a).real
    )

    assert eigenvalue == pytest.approx(
        expected,
        rel=1e-7,
    )


def test_power_method_normalizes_eigenvector():
    a = np.array(
        [
            [3, 0],
            [0, 1],
        ],
        dtype=float,
    )

    _, eigenvector, _ = power_method(a)

    assert np.sqrt(
        np.dot(
            eigenvector,
            eigenvector,
        )
    ) == pytest.approx(1.0)


def test_power_method_zero_initial_vector_rejected():
    with pytest.raises(ValueError):
        power_method(
            [
                [2, 0],
                [0, 1],
            ],
            initial_vector=[
                0,
                0,
            ],
        )


def test_power_method_invalid_iterations_rejected():
    with pytest.raises(ValueError):
        power_method(
            [
                [2, 0],
                [0, 1],
            ],
            max_iterations=0,
        )


def test_power_method_invalid_tolerance_rejected():
    with pytest.raises(ValueError):
        power_method(
            [
                [2, 0],
                [0, 1],
            ],
            tolerance=0,
        )


def test_non_matrix_input_rejected():
    with pytest.raises(ValueError):
        classical_matrix_multiply(
            [1, 2, 3],
            [
                [1],
                [2],
                [3],
            ],
        )