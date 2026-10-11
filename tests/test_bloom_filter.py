"""Tests for the Bloom filter."""

import pytest

from src.randomized.bloom_filter import (
    BloomFilter,
)


def test_added_item_is_present():
    bloom = BloomFilter(
        size=100,
        hash_count=3,
    )

    bloom.add(
        "apple"
    )

    assert bloom.check(
        "apple"
    )


def test_multiple_items_present():
    bloom = BloomFilter(
        size=200,
        hash_count=4,
    )

    items = [
        "apple",
        "banana",
        "orange",
        "grape",
    ]

    for item in items:
        bloom.add(
            item
        )

    for item in items:
        assert bloom.check(
            item
        )


def test_no_false_negatives():
    bloom = BloomFilter(
        size=500,
        hash_count=5,
    )

    items = [
        f"item-{index}"
        for index in range(100)
    ]

    for item in items:
        bloom.add(
            item
        )

    assert all(
        bloom.check(item)
        for item in items
    )


def test_unadded_item_can_be_false():
    bloom = BloomFilter(
        size=1000,
        hash_count=4,
    )

    bloom.add(
        "known"
    )

    assert not bloom.check(
        "definitely-different"
    )


def test_duplicate_add():
    bloom = BloomFilter(
        size=100,
        hash_count=3,
    )

    bloom.add(
        "apple"
    )

    first_count = bloom.bit_count()

    bloom.add(
        "apple"
    )

    second_count = bloom.bit_count()

    assert first_count == second_count


def test_bit_count():
    bloom = BloomFilter(
        size=100,
        hash_count=3,
    )

    assert bloom.bit_count() == 0

    bloom.add(
        "apple"
    )

    assert bloom.bit_count() > 0


def test_load_factor():
    bloom = BloomFilter(
        size=100,
        hash_count=3,
    )

    assert bloom.load_factor() == 0.0

    bloom.add(
        "apple"
    )

    assert 0 < bloom.load_factor() <= 1


def test_integer_item():
    bloom = BloomFilter(
        size=100,
        hash_count=3,
    )

    bloom.add(
        12345
    )

    assert bloom.check(
        12345
    )


def test_hashes_are_reproducible():
    first = BloomFilter(
        size=100,
        hash_count=3,
    )

    second = BloomFilter(
        size=100,
        hash_count=3,
    )

    assert first._hashes(
        "test"
    ) == second._hashes(
        "test"
    )


def test_invalid_size_zero():
    with pytest.raises(ValueError):
        BloomFilter(
            size=0,
            hash_count=3,
        )


def test_invalid_hash_count_zero():
    with pytest.raises(ValueError):
        BloomFilter(
            size=100,
            hash_count=0,
        )


def test_invalid_size_type():
    with pytest.raises(TypeError):
        BloomFilter(
            size="100",
            hash_count=3,
        )


def test_invalid_hash_count_type():
    with pytest.raises(TypeError):
        BloomFilter(
            size=100,
            hash_count="3",
        )