"""Probabilistic and deterministic primality tests."""

import math
import random
from typing import Optional


def _validate_iterations(
    iterations: int,
) -> None:
    """Validate the number of probabilistic test rounds."""
    if not isinstance(iterations, int):
        raise TypeError(
            "iterations must be an integer"
        )

    if iterations <= 0:
        raise ValueError(
            "iterations must be positive"
        )


def deterministic_is_prime(
    number: int,
) -> bool:
    """
    Test primality using deterministic trial division.

    Time complexity:
        O(sqrt(n))
    """
    if not isinstance(number, int):
        raise TypeError(
            "number must be an integer"
        )

    if number < 2:
        return False

    if number in (
        2,
        3,
    ):
        return True

    if number % 2 == 0:
        return False

    limit = math.isqrt(
        number
    )

    divisor = 3

    while divisor <= limit:
        if number % divisor == 0:
            return False

        divisor += 2

    return True


def fermat_primality_test(
    number: int,
    iterations: int = 5,
    seed: Optional[int] = None,
) -> bool:
    """
    Perform Fermat's probabilistic primality test.

    True means the number is probably prime.
    False means the number is definitely composite.
    """
    if not isinstance(number, int):
        raise TypeError(
            "number must be an integer"
        )

    _validate_iterations(
        iterations
    )

    if number < 2:
        return False

    if number in (
        2,
        3,
    ):
        return True

    if number % 2 == 0:
        return False

    random_generator = random.Random(
        seed
    )

    for _ in range(iterations):
        base = random_generator.randint(
            2,
            number - 2,
        )

        if math.gcd(
            base,
            number,
        ) != 1:
            return False

        if pow(
            base,
            number - 1,
            number,
        ) != 1:
            return False

    return True


def miller_rabin_primality_test(
    number: int,
    iterations: int = 5,
    seed: Optional[int] = None,
) -> bool:
    """
    Perform the Miller-Rabin probabilistic primality test.

    True means the number is probably prime.
    False means the number is definitely composite.
    """
    if not isinstance(number, int):
        raise TypeError(
            "number must be an integer"
        )

    _validate_iterations(
        iterations
    )

    if number < 2:
        return False

    if number in (
        2,
        3,
    ):
        return True

    if number % 2 == 0:
        return False

    d = number - 1
    power_of_two = 0

    while d % 2 == 0:
        power_of_two += 1
        d //= 2

    random_generator = random.Random(
        seed
    )

    for _ in range(iterations):
        base = random_generator.randint(
            2,
            number - 2,
        )

        value = pow(
            base,
            d,
            number,
        )

        if value in (
            1,
            number - 1,
        ):
            continue

        for _ in range(
            power_of_two - 1
        ):
            value = pow(
                value,
                2,
                number,
            )

            if value == number - 1:
                break

        else:
            return False

    return True