"""Probability and benchmark analysis utilities."""

import math
import statistics
from typing import Iterable, Tuple


def mean_and_variance(
    values: Iterable[float],
) -> Tuple[float, float]:
    """Return population mean and variance."""
    data = list(values)

    if not data:
        raise ValueError(
            "values must not be empty"
        )

    return (
        statistics.mean(data),
        statistics.pvariance(data),
    )


def bloom_false_positive_probability(
    bit_count: int,
    hash_count: int,
    inserted_items: int,
) -> float:
    """
    Return the theoretical Bloom filter false-positive rate.

    Formula:
        (1 - e^(-kn/m))^k
    """
    if bit_count <= 0:
        raise ValueError(
            "bit_count must be positive"
        )

    if hash_count <= 0:
        raise ValueError(
            "hash_count must be positive"
        )

    if inserted_items < 0:
        raise ValueError(
            "inserted_items must be non-negative"
        )

    probability = (
        1
        - math.exp(
            -hash_count
            * inserted_items
            / bit_count
        )
    ) ** hash_count

    return probability


def miller_rabin_error_bound(
    iterations: int,
) -> float:
    """
    Return the standard Miller-Rabin false-prime bound.

    For a composite number, the probability that all
    rounds fail to expose compositeness is at most:

        (1 / 4)^k
    """
    if iterations <= 0:
        raise ValueError(
            "iterations must be positive"
        )

    return (
        0.25 ** iterations
    )


def absolute_error(
    actual: float,
    estimate: float,
) -> float:
    """Return absolute estimation error."""
    return abs(
        actual - estimate
    )