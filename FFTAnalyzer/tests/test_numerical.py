"""Tests for Week 12 numerical stability utilities."""

import math

import numpy as np
import pytest

from FFTAnalyzer.fft_analyzer.core.numerical import (
    absolute_error,
    cancellation_demo,
    condition_number,
    infinity_norm,
    inverse_matrix,
    is_ill_conditioned,
    l1_norm,
    l2_norm,
    matrix_infinity_norm,
    matrix_one_norm,
    relative_error,
    residual_norm,
    spectral_norm_estimate,
)


def test_absolute_error_scalar():
    assert absolute_error(
        10.0,
        9.5,
    ) == pytest.approx(
        0.5
    )


def test_absolute_error_array():
    result = absolute_error(
        [1, 2, 3],
        [1.1, 1.5, 2.5],
    )

    assert np.allclose(
        result,
        [
            0.1,
            0.5,
            0.5,
        ],
    )


def test_absolute_error_shape_mismatch():
    with pytest.raises(ValueError):
        absolute_error(
            [1, 2],
            [1, 2, 3],
        )


def test_relative_error_scalar():
    assert relative_error(
        100,
        90,
    ) == pytest.approx(
        0.1
    )


def test_relative_error_array():
    result = relative_error(
        [10, 20],
        [9, 18],
    )

    assert np.allclose(
        result,
        [
            0.1,
            0.1,
        ],
    )


def test_relative_error_zero_exact():
    assert relative_error(
        0.0,
        0.0,
    ) == 0.0


def test_relative_error_zero_nonzero_approximation():
    assert math.isinf(
        relative_error(
            0.0,
            1.0,
        )
    )


def test_l1_norm_vector():
    assert l1_norm(
        [
            -1,
            2,
            -3,
        ]
    ) == pytest.approx(
        6.0
    )


def test_l2_norm_vector():
    assert l2_norm(
        [
            3,
            4,
        ]
    ) == pytest.approx(
        5.0
    )


def test_l2_norm_matrix_is_frobenius():
    matrix = np.array(
        [
            [1, 2],
            [3, 4],
        ],
        dtype=float,
    )

    assert l2_norm(
        matrix
    ) == pytest.approx(
        np.linalg.norm(
            matrix,
            "fro",
        )
    )


def test_infinity_norm_vector():
    assert infinity_norm(
        [
            -3,
            7,
            -2,
        ]
    ) == pytest.approx(
        7.0
    )


def test_infinity_norm_matrix():
    matrix = [
        [1, -2],
        [3, 4],
    ]

    assert infinity_norm(
        matrix
    ) == pytest.approx(
        7.0
    )


def test_matrix_one_norm():
    matrix = [
        [1, -2],
        [3, 4],
    ]

    assert matrix_one_norm(
        matrix
    ) == pytest.approx(
        6.0
    )


def test_matrix_infinity_norm():
    matrix = [
        [1, -2],
        [3, 4],
    ]

    assert matrix_infinity_norm(
        matrix
    ) == pytest.approx(
        7.0
    )


def test_inverse_matrix_identity():
    identity = np.eye(3)

    result = inverse_matrix(
        identity
    )

    assert np.allclose(
        result,
        identity,
    )


def test_inverse_matrix_matches_numpy():
    matrix = np.array(
        [
            [4, 7],
            [2, 6],
        ],
        dtype=float,
    )

    result = inverse_matrix(
        matrix
    )

    assert np.allclose(
        result,
        np.linalg.inv(
            matrix
        ),
    )


def test_inverse_matrix_reconstructs_identity():
    matrix = np.array(
        [
            [3, 1],
            [1, 2],
        ],
        dtype=float,
    )

    inverse = inverse_matrix(
        matrix
    )

    assert np.allclose(
        matrix @ inverse,
        np.eye(2),
    )


def test_inverse_matrix_rejects_nonsquare():
    with pytest.raises(ValueError):
        inverse_matrix(
            [
                [1, 2, 3],
                [4, 5, 6],
            ]
        )


def test_condition_number_identity_one_norm():
    assert condition_number(
        np.eye(4),
        norm="1",
    ) == pytest.approx(
        1.0
    )


def test_condition_number_identity_infinity_norm():
    assert condition_number(
        np.eye(4),
        norm="inf",
    ) == pytest.approx(
        1.0
    )


def test_condition_number_matches_numpy_one_norm():
    matrix = np.array(
        [
            [4, 2],
            [1, 3],
        ],
        dtype=float,
    )

    result = condition_number(
        matrix,
        norm="1",
    )

    expected = np.linalg.cond(
        matrix,
        1,
    )

    assert result == pytest.approx(
        expected,
        rel=1e-10,
    )


def test_condition_number_matches_numpy_infinity_norm():
    matrix = np.array(
        [
            [4, 2],
            [1, 3],
        ],
        dtype=float,
    )

    result = condition_number(
        matrix,
        norm="inf",
    )

    expected = np.linalg.cond(
        matrix,
        np.inf,
    )

    assert result == pytest.approx(
        expected,
        rel=1e-10,
    )


def test_spectral_norm_estimate():
    matrix = np.array(
        [
            [3, 0],
            [0, 2],
        ],
        dtype=float,
    )

    assert spectral_norm_estimate(
        matrix
    ) == pytest.approx(
        3.0,
        rel=1e-8,
    )


def test_condition_number_two_norm():
    matrix = np.array(
        [
            [4, 0],
            [0, 2],
        ],
        dtype=float,
    )

    assert condition_number(
        matrix,
        norm="2",
    ) == pytest.approx(
        2.0,
        rel=1e-7,
    )


def test_invalid_condition_norm():
    with pytest.raises(ValueError):
        condition_number(
            np.eye(2),
            norm="banana",
        )


def test_well_conditioned_identity():
    assert (
        is_ill_conditioned(
            np.eye(3)
        )
        is False
    )


def test_ill_conditioned_matrix():
    matrix = np.array(
        [
            [1.0, 1.0],
            [
                1.0,
                1.0 + 1e-11,
            ],
        ],
        dtype=float,
    )

    assert (
        is_ill_conditioned(
            matrix,
            threshold=1e10,
        )
        is True
    )


def test_invalid_condition_threshold():
    with pytest.raises(ValueError):
        is_ill_conditioned(
            np.eye(2),
            threshold=0,
        )


def test_cancellation_demo_contains_expected_fields():
    result = cancellation_demo()

    assert set(
        result
    ) == {
        "x",
        "naive",
        "stable",
        "absolute_error",
        "relative_error",
    }


def test_cancellation_demo_shows_precision_loss():
    result = cancellation_demo(
        1e16
    )

    assert result[
        "stable"
    ] > 0.0

    assert result[
        "absolute_error"
    ] > 0.0


def test_cancellation_demo_rejects_nonpositive_input():
    with pytest.raises(ValueError):
        cancellation_demo(
            0
        )


def test_residual_norm_exact_solution():
    matrix = np.array(
        [
            [2, 0],
            [0, 3],
        ],
        dtype=float,
    )

    solution = np.array(
        [2, 4],
        dtype=float,
    )

    vector = (
        matrix
        @ solution
    )

    assert residual_norm(
        matrix,
        solution,
        vector,
    ) == pytest.approx(
        0.0
    )


def test_residual_norm_inexact_solution():
    matrix = np.eye(2)

    result = residual_norm(
        matrix,
        [
            1,
            1,
        ],
        [
            1,
            2,
        ],
    )

    assert result == pytest.approx(
        1.0
    )


def test_residual_norm_dimension_mismatch():
    with pytest.raises(ValueError):
        residual_norm(
            np.eye(2),
            [
                1,
                2,
                3,
            ],
            [
                1,
                2,
            ],
        )


def test_empty_input_rejected():
    with pytest.raises(ValueError):
        l1_norm([])


def test_non_numeric_input_rejected():
    with pytest.raises(TypeError):
        l2_norm(
            [
                "a",
                "b",
            ]
        )