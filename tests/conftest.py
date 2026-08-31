"""Shared pytest fixtures."""

import random
import pytest


@pytest.fixture
def sample_arrays():
    """Representative arrays that every sorting algorithm should handle."""
    return {
        "empty": [],
        "single": [42],
        "sorted": [1, 2, 3, 4, 5],
        "reverse": [5, 4, 3, 2, 1],
        "duplicates": [3, 1, 4, 1, 5, 9, 2, 6, 5],
        "all_same": [7, 7, 7, 7, 7],
        "negative": [-3, -1, -4, -1, -5],
        "mixed": [3, -1, 4, 0, -2, 7],
    }


@pytest.fixture
def large_random_array():
    """A reproducible larger input used for stress testing."""
    rng = random.Random(42)
    return [rng.randint(-1000, 1000) for _ in range(1000)]
