"""Week 7 randomized algorithms demonstration."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.randomized.bloom_filter import BloomFilter
from src.randomized.minhash_similarity import (
    estimate_minhash_similarity,
    jaccard_similarity,
)
from src.randomized.montecarlo_primality import (
    fermat_primality_test,
    miller_rabin_primality_test,
)
from src.randomized.randomized_quicksort import (
    randomized_quicksort,
)
from src.randomized.randomized_selection import (
    randomized_select,
)


def main():
    """Run small examples of the Week 7 algorithms."""
    print("Week 7 Randomized Algorithms Demo")
    print()

    values = [
        9,
        3,
        7,
        1,
        5,
    ]

    print(
        "Randomized QuickSort:",
        randomized_quicksort(
            values,
            seed=42,
        ),
    )

    print(
        "Randomized Selection (3rd smallest):",
        randomized_select(
            values,
            3,
            seed=42,
        ),
    )

    number = 104729

    print(
        "Fermat Primality:",
        fermat_primality_test(
            number,
            iterations=10,
            seed=42,
        ),
    )

    print(
        "Miller-Rabin Primality:",
        miller_rabin_primality_test(
            number,
            iterations=10,
            seed=42,
        ),
    )

    bloom = BloomFilter(
        size=1000,
        hash_count=4,
    )

    bloom.add(
        "algorithm"
    )

    print(
        "Bloom Filter 'algorithm':",
        bloom.check(
            "algorithm"
        ),
    )

    print(
        "Bloom Filter 'database':",
        bloom.check(
            "database"
        ),
    )

    first = {
        "data",
        "algorithm",
        "python",
        "graph",
    }

    second = {
        "algorithm",
        "python",
        "database",
        "network",
    }

    exact = jaccard_similarity(
        first,
        second,
    )

    estimated = estimate_minhash_similarity(
        first,
        second,
        num_hashes=128,
        seed=42,
    )

    print(
        "Jaccard Similarity:",
        exact,
    )

    print(
        "MinHash Estimate:",
        estimated,
    )


if __name__ == "__main__":
    main()