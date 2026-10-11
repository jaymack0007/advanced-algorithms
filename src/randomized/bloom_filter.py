"""Bloom filter implementation using multiple hash functions."""

import hashlib
from typing import Any


class BloomFilter:
    """
    Space-efficient probabilistic membership structure.

    False positives are possible.
    False negatives should not occur.
    """

    def __init__(
        self,
        size: int,
        hash_count: int,
    ) -> None:
        if not isinstance(size, int):
            raise TypeError(
                "size must be an integer"
            )

        if not isinstance(hash_count, int):
            raise TypeError(
                "hash_count must be an integer"
            )

        if size <= 0:
            raise ValueError(
                "size must be positive"
            )

        if hash_count <= 0:
            raise ValueError(
                "hash_count must be positive"
            )

        self.size = size
        self.hash_count = hash_count
        self.bits = bytearray(size)

    def _hashes(
        self,
        item: Any,
    ) -> list[int]:
        """Generate Bloom filter indexes for an item."""
        item_bytes = str(item).encode(
            "utf-8"
        )

        indexes = []

        for index in range(
            self.hash_count
        ):
            hasher = hashlib.sha256()

            hasher.update(
                index.to_bytes(
                    4,
                    byteorder="little",
                )
            )

            hasher.update(
                item_bytes
            )

            digest = hasher.digest()

            value = int.from_bytes(
                digest[:8],
                byteorder="little",
            )

            indexes.append(
                value % self.size
            )

        return indexes

    def add(
        self,
        item: Any,
    ) -> None:
        """Add an item to the filter."""
        for index in self._hashes(
            item
        ):
            self.bits[index] = 1

    def check(
        self,
        item: Any,
    ) -> bool:
        """
        Check whether an item may be present.

        True means possibly present.
        False means definitely not present.
        """
        return all(
            self.bits[index]
            for index in self._hashes(
                item
            )
        )

    def bit_count(
        self,
    ) -> int:
        """Return the number of set bits."""
        return sum(
            self.bits
        )

    def load_factor(
        self,
    ) -> float:
        """Return the fraction of bits currently set."""
        return (
            self.bit_count()
            / self.size
        )