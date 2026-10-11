"""Tests for MinHash similarity estimation."""

import pytest

from src.randomized.minhash_similarity import (
    estimate_minhash_similarity,
    jaccard_similarity,
    minhash_signature,
)


def test_exact_jaccard():
    first = {
        "a",
        "b",
        "c",
    }

    second = {
        "b",
        "c",
        "d",
    }

    assert jaccard_similarity(
        first,
        second,
    ) == 0.5


def test_identical_sets():
    values = {
        "a",
        "b",
        "c",
        "d",
    }

    assert jaccard_similarity(
        values,
        values,
    ) == 1.0

    assert estimate_minhash_similarity(
        values,
        values,
        num_hashes=64,
    ) == 1.0


def test_disjoint_sets():
    first = {
        "a",
        "b",
    }

    second = {
        "x",
        "y",
    }

    assert jaccard_similarity(
        first,
        second,
    ) == 0.0


def test_empty_sets():
    assert jaccard_similarity(
        set(),
        set(),
    ) == 1.0

    assert estimate_minhash_similarity(
        set(),
        set(),
        num_hashes=16,
    ) == 1.0


def test_one_empty_set():
    assert jaccard_similarity(
        {"a"},
        set(),
    ) == 0.0

    assert estimate_minhash_similarity(
        {"a"},
        set(),
        num_hashes=16,
    ) == 0.0


def test_signature_length():
    signature = minhash_signature(
        {
            "a",
            "b",
            "c",
        },
        num_hashes=128,
    )

    assert len(signature) == 128


def test_signature_reproducible():
    values = {
        "one",
        "two",
        "three",
    }

    first = minhash_signature(
        values,
        num_hashes=64,
        seed=100,
    )

    second = minhash_signature(
        values,
        num_hashes=64,
        seed=100,
    )

    assert first == second


def test_order_does_not_matter():
    first = [
        "a",
        "b",
        "c",
    ]

    second = [
        "c",
        "a",
        "b",
    ]

    assert minhash_signature(
        first,
        num_hashes=64,
        seed=42,
    ) == minhash_signature(
        second,
        num_hashes=64,
        seed=42,
    )


def test_estimate_in_valid_range():
    first = {
        "a",
        "b",
        "c",
        "d",
    }

    second = {
        "c",
        "d",
        "e",
        "f",
    }

    estimate = estimate_minhash_similarity(
        first,
        second,
        num_hashes=128,
        seed=42,
    )

    assert 0.0 <= estimate <= 1.0


def test_estimate_reasonably_close():
    first = set(
        range(100)
    )

    second = set(
        range(50, 150)
    )

    exact = jaccard_similarity(
        first,
        second,
    )

    estimate = estimate_minhash_similarity(
        first,
        second,
        num_hashes=512,
        seed=42,
    )

    assert abs(
        exact - estimate
    ) < 0.10


def test_invalid_hash_count_zero():
    with pytest.raises(ValueError):
        minhash_signature(
            {"a"},
            num_hashes=0,
        )


def test_invalid_hash_count_type():
    with pytest.raises(TypeError):
        minhash_signature(
            {"a"},
            num_hashes="64",
        )