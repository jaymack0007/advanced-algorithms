"""MinHash similarity estimation."""

import hashlib
import random
from typing import Iterable, List, Set


PRIME = 4294967311


def _stable_hash(
    item: object,
) -> int:
    """Create a stable integer hash for an item."""
    digest = hashlib.sha256(
        str(item).encode("utf-8")
    ).digest()

    return int.from_bytes(
        digest[:8],
        byteorder="little",
    ) % PRIME


def jaccard_similarity(
    first: Iterable[object],
    second: Iterable[object],
) -> float:
    """Return the exact Jaccard similarity."""
    first_set: Set[object] = set(first)
    second_set: Set[object] = set(second)

    union = first_set | second_set

    if not union:
        return 1.0

    intersection = (
        first_set & second_set
    )

    return (
        len(intersection)
        / len(union)
    )


def minhash_signature(
    items: Iterable[object],
    num_hashes: int,
    seed: int = 42,
) -> List[int]:
    """
    Create a MinHash signature for a set.

    Time complexity:
        O(k * |S|)
    """
    if not isinstance(num_hashes, int):
        raise TypeError(
            "num_hashes must be an integer"
        )

    if num_hashes <= 0:
        raise ValueError(
            "num_hashes must be positive"
        )

    item_set = set(items)

    random_generator = random.Random(
        seed
    )

    coefficients = [
        (
            random_generator.randint(
                1,
                PRIME - 1,
            ),
            random_generator.randint(
                0,
                PRIME - 1,
            ),
        )
        for _ in range(num_hashes)
    ]

    if not item_set:
        return [
            PRIME
            for _ in range(num_hashes)
        ]

    hashed_items = [
        _stable_hash(item)
        for item in item_set
    ]

    signature = []

    for a, b in coefficients:
        minimum = min(
            (
                a * value + b
            ) % PRIME
            for value in hashed_items
        )

        signature.append(
            minimum
        )

    return signature


def estimate_minhash_similarity(
    first: Iterable[object],
    second: Iterable[object],
    num_hashes: int,
    seed: int = 42,
) -> float:
    """Estimate Jaccard similarity using MinHash."""
    first_set = set(first)
    second_set = set(second)

    if not first_set and not second_set:
        return 1.0

    if not first_set or not second_set:
        return 0.0

    first_signature = minhash_signature(
        first_set,
        num_hashes,
        seed,
    )

    second_signature = minhash_signature(
        second_set,
        num_hashes,
        seed,
    )

    matches = sum(
        first_value == second_value
        for first_value, second_value in zip(
            first_signature,
            second_signature,
        )
    )

    return (
        matches
        / num_hashes
    )