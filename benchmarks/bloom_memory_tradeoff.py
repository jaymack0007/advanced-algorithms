"""Bloom filter memory-versus-accuracy benchmark."""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.randomized.bloom_filter import BloomFilter
from src.utils.probability_analysis import (
    bloom_false_positive_probability,
)


RESULTS_DIR = PROJECT_ROOT / "benchmarks" / "results"

INSERT_COUNTS = [
    250,
    500,
    1000,
    1500,
    2000,
]

MEMORY_BIT_COUNTS = [
    2000,
    5000,
    10000,
    20000,
    40000,
]


def measure_false_positive_rate(
    bit_count,
    hash_count,
    inserted_items,
    query_count,
):
    """Return observed and theoretical false-positive rates."""
    bloom = BloomFilter(
        size=bit_count,
        hash_count=hash_count,
    )

    for value in range(
        inserted_items
    ):
        bloom.add(
            f"stored-{value}"
        )

    false_positives = 0

    for value in range(
        query_count
    ):
        if bloom.check(
            f"query-{value}"
        ):
            false_positives += 1

    observed = (
        false_positives
        / query_count
    )

    theoretical = (
        bloom_false_positive_probability(
            bit_count,
            hash_count,
            inserted_items,
        )
    )

    return {
        "bit_count": bit_count,
        "storage_bytes": bloom.storage_bytes(),
        "inserted_items": inserted_items,
        "load_factor": bloom.load_factor(),
        "observed_fp_rate": observed,
        "theoretical_fp_rate": theoretical,
    }


def main():
    """Run Bloom filter load and memory experiments."""
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    hash_count = 4
    query_count = 5000

    load_rows = []

    for inserted_items in INSERT_COUNTS:
        row = measure_false_positive_rate(
            bit_count=10000,
            hash_count=hash_count,
            inserted_items=inserted_items,
            query_count=query_count,
        )

        row["experiment"] = "Load"
        load_rows.append(
            row
        )

    memory_rows = []

    for bit_count in MEMORY_BIT_COUNTS:
        row = measure_false_positive_rate(
            bit_count=bit_count,
            hash_count=hash_count,
            inserted_items=1000,
            query_count=query_count,
        )

        row["experiment"] = "Memory"
        memory_rows.append(
            row
        )

    dataframe = pd.DataFrame(
        load_rows + memory_rows
    )

    dataframe.to_csv(
        RESULTS_DIR
        / "bloom_memory_tradeoff.csv",
        index=False,
    )

    figure, axes = plt.subplots(
        1,
        2,
        figsize=(12, 5),
    )

    load_data = pd.DataFrame(
        load_rows
    )

    axes[0].plot(
        load_data["inserted_items"],
        load_data["observed_fp_rate"],
        marker="o",
        label="Observed",
    )

    axes[0].plot(
        load_data["inserted_items"],
        load_data["theoretical_fp_rate"],
        marker="o",
        linestyle="--",
        label="Theoretical",
    )

    axes[0].set_title(
        "Load vs False Positive Rate"
    )
    axes[0].set_xlabel(
        "Inserted Items"
    )
    axes[0].set_ylabel(
        "False Positive Rate"
    )
    axes[0].grid(True)
    axes[0].legend()

    memory_data = pd.DataFrame(
        memory_rows
    )

    axes[1].plot(
        memory_data["storage_bytes"],
        memory_data["observed_fp_rate"],
        marker="o",
        label="Observed",
    )

    axes[1].plot(
        memory_data["storage_bytes"],
        memory_data["theoretical_fp_rate"],
        marker="o",
        linestyle="--",
        label="Theoretical",
    )

    axes[1].set_title(
        "Memory vs False Positive Rate"
    )
    axes[1].set_xlabel(
        "Packed Storage (bytes)"
    )
    axes[1].set_ylabel(
        "False Positive Rate"
    )
    axes[1].grid(True)
    axes[1].legend()

    figure.tight_layout()

    figure.savefig(
        RESULTS_DIR
        / "bloom_filter_fp_rate.png",
        bbox_inches="tight",
    )

    plt.close(
        figure
    )

    print(
        dataframe.to_string(
            index=False
        )
    )

    print()
    print(
        "Bloom memory benchmark complete."
    )

    print(
        "Plot:",
        RESULTS_DIR
        / "bloom_filter_fp_rate.png",
    )

    print(
        "CSV:",
        RESULTS_DIR
        / "bloom_memory_tradeoff.csv",
    )


if __name__ == "__main__":
    main()