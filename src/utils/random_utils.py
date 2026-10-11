"""Utility functions for reproducible randomized benchmarks."""

import random
from typing import List, Set, Tuple


def shuffled_range(
    size: int,
    seed: int = 42,
) -> List[int]:
    """Return numbers 0 through size - 1 in random order."""
    if size < 0:
        raise ValueError(
            "size must be non-negative"
        )

    values = list(
        range(size)
    )

    random_generator = random.Random(
        seed
    )

    random_generator.shuffle(
        values
    )

    return values


def make_minhash_sets(
    set_size: int = 1000,
    overlap: int = 500,
) -> Tuple[
    Set[int],
    Set[int],
]:
    """
    Create two sets with a controlled overlap.
    """
    if set_size <= 0:
        raise ValueError(
            "set_size must be positive"
        )

    if overlap < 0 or overlap > set_size:
        raise ValueError(
            "overlap must be between 0 and set_size"
        )

    first = set(
        range(set_size)
    )

    second_start = (
        set_size - overlap
    )

    second = set(
        range(
            second_start,
            second_start + set_size,
        )
    )

    return first, second