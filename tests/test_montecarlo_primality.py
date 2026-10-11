"""Tests for probabilistic primality algorithms."""

import pytest

from src.randomized.montecarlo_primality import (
    deterministic_is_prime,
    fermat_primality_test,
    miller_rabin_primality_test,
)


@pytest.mark.parametrize(
    "number",
    [
        2,
        3,
        5,
        7,
        11,
        97,
        101,
        104729,
    ],
)
def test_deterministic_primes(
    number,
):
    assert deterministic_is_prime(
        number
    )


@pytest.mark.parametrize(
    "number",
    [
        -1,
        0,
        1,
        4,
        9,
        21,
        100,
        1001,
    ],
)
def test_deterministic_composites(
    number,
):
    assert not deterministic_is_prime(
        number
    )


def test_fermat_prime():
    assert fermat_primality_test(
        104729,
        iterations=10,
        seed=42,
    )


def test_fermat_composite():
    assert not fermat_primality_test(
        1001,
        iterations=10,
        seed=42,
    )


def test_miller_rabin_prime():
    assert miller_rabin_primality_test(
        104729,
        iterations=10,
        seed=42,
    )


def test_miller_rabin_composite():
    assert not miller_rabin_primality_test(
        1001,
        iterations=10,
        seed=42,
    )


def test_miller_rabin_carmichael_number():
    assert not miller_rabin_primality_test(
        561,
        iterations=10,
        seed=42,
    )


def test_large_prime():
    number = 1000003

    assert deterministic_is_prime(
        number
    )

    assert miller_rabin_primality_test(
        number,
        iterations=20,
        seed=42,
    )


def test_large_composite():
    number = 1000005

    assert not deterministic_is_prime(
        number
    )

    assert not miller_rabin_primality_test(
        number,
        iterations=20,
        seed=42,
    )


def test_seed_is_reproducible():
    first = miller_rabin_primality_test(
        104729,
        iterations=10,
        seed=100,
    )

    second = miller_rabin_primality_test(
        104729,
        iterations=10,
        seed=100,
    )

    assert first == second


def test_invalid_iterations_zero():
    with pytest.raises(ValueError):
        miller_rabin_primality_test(
            17,
            iterations=0,
        )


def test_invalid_iterations_type():
    with pytest.raises(TypeError):
        fermat_primality_test(
            17,
            iterations="five",
        )


def test_invalid_number_type():
    with pytest.raises(TypeError):
        deterministic_is_prime(
            17.5
        )