"""Benchmark KMP, Rabin-Karp, suffix arrays, and suffix trees."""

from __future__ import annotations

import argparse
import gc
from pathlib import Path
import sys
from time import perf_counter
import tracemalloc
from typing import Callable, Dict, List, Tuple

import matplotlib

matplotlib.use(
    "Agg"
)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from StringSearchEngine.core.kmp import (
    kmp_search,
)
from StringSearchEngine.core.rabin_karp import (
    rabin_karp_search,
    rabin_karp_search_with_stats,
)
from StringSearchEngine.core.suffix_array import (
    SuffixArrayIndex,
)
from StringSearchEngine.core.suffix_tree import (
    CompressedSuffixTree,
)
from StringSearchEngine.utils.generators import (
    embed_pattern,
    random_text,
)


BENCHMARK_PATTERN = "NEEDLE_PATTERN_2026"

FULL_DATASETS = {
    "small_10KB": 10_000,
    "medium_1MB": 1_000_000,
}

SMOKE_DATASETS = {
    "smoke_2KB": 2_000,
}

TREE_MAX_CHARS = 12_000

COLLISION_MODULI = [
    5,
    17,
    101,
    1009,
    10007,
    1_000_000_007,
]


def create_dataset(
    size: int,
    seed: int = 42,
) -> Tuple[
    str,
    List[int],
]:
    """Create synthetic text with three known pattern occurrences."""
    if (
        isinstance(
            size,
            bool,
        )
        or not isinstance(
            size,
            int,
        )
    ):
        raise TypeError(
            "size must be an integer"
        )

    if size < 200:
        raise ValueError(
            "size must be at least 200 characters"
        )

    text = random_text(
        size,
        alphabet="abcdefghijklmnopqrstuvwxyz ",
        seed=seed,
    )

    pattern_length = len(
        BENCHMARK_PATTERN
    )

    positions = [
        size // 5,
        size // 2,
        size
        - pattern_length
        - 20,
    ]

    text = embed_pattern(
        text,
        BENCHMARK_PATTERN,
        positions,
    )

    return (
        text,
        positions,
    )


def _measure_build(
    builder: Callable,
) -> Tuple[
    object,
    float,
]:
    """
    Measure preprocessing time without tracemalloc.

    Running a large Python suffix-array construction under
    tracemalloc can substantially distort preprocessing time.
    """
    gc.collect()

    start = perf_counter()

    result = builder()

    elapsed = (
        perf_counter()
        - start
    )

    return (
        result,
        elapsed,
    )


def _list_memory_bytes(
    values: list,
    seen: set[int],
) -> int:
    """Estimate retained memory for a list and its unique elements."""
    total = sys.getsizeof(
        values
    )

    for value in values:
        identifier = id(
            value
        )

        if identifier in seen:
            continue

        seen.add(
            identifier
        )

        total += sys.getsizeof(
            value
        )

    return total


def _suffix_array_memory_mb(
    index: SuffixArrayIndex,
) -> float:
    """
    Estimate persistent suffix-array index footprint.

    The estimate includes the text, suffix array, LCP array,
    and unique integer objects retained by those lists.
    """
    seen = set()

    total = sys.getsizeof(
        index
    )

    total += sys.getsizeof(
        index.__dict__
    )

    text_identifier = id(
        index.text
    )

    seen.add(
        text_identifier
    )

    total += sys.getsizeof(
        index.text
    )

    total += _list_memory_bytes(
        index.suffix_array,
        seen,
    )

    total += _list_memory_bytes(
        index.lcp,
        seen,
    )

    return total / (
        1024
        * 1024
    )


def _deep_memory_bytes(
    root: object,
) -> int:
    """
    Estimate retained memory of an object graph.

    Object identities are tracked so shared objects are not
    counted repeatedly.
    """
    seen = set()

    stack = [
        root
    ]

    total = 0

    while stack:
        current = stack.pop()

        identifier = id(
            current
        )

        if identifier in seen:
            continue

        seen.add(
            identifier
        )

        total += sys.getsizeof(
            current
        )

        if isinstance(
            current,
            dict,
        ):
            stack.extend(
                current.keys()
            )

            stack.extend(
                current.values()
            )

        elif isinstance(
            current,
            (list, tuple, set),
        ):
            stack.extend(
                current
            )

        elif hasattr(
            current,
            "__dict__",
        ):
            stack.append(
                current.__dict__
            )

    return total


def _suffix_tree_memory_mb(
    tree: CompressedSuffixTree,
) -> float:
    """Estimate persistent compressed suffix-tree footprint."""
    return _deep_memory_bytes(
        tree
    ) / (
        1024
        * 1024
    )


def _measure_search_memory(
    search: Callable[[], List[int]],
) -> float:
    """Measure peak temporary memory used by one search query."""
    gc.collect()

    tracemalloc.start()

    search()

    _, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    return peak / (
        1024
        * 1024
    )


def _average_search_time(
    search: Callable[[], List[int]],
    repeats: int,
) -> Tuple[
    List[int],
    float,
]:
    """Measure average query time without tracemalloc overhead."""
    if repeats <= 0:
        raise ValueError(
            "repeats must be positive"
        )

    positions = []

    start = perf_counter()

    for _ in range(
        repeats
    ):
        positions = search()

    elapsed = (
        perf_counter()
        - start
    )

    return (
        positions,
        elapsed
        / repeats,
    )


def _result_row(
    dataset: str,
    size: int,
    algorithm: str,
    preprocessing_seconds: float | None,
    average_search_seconds: float | None,
    persistent_index_mb: float | None,
    search_peak_memory_mb: float | None,
    matches: int | None,
    collisions: int | None = None,
    skipped: bool = False,
) -> Dict:
    """Create one benchmark result row."""
    if (
        persistent_index_mb is None
        or search_peak_memory_mb is None
    ):
        combined_memory_mb = None
    else:
        combined_memory_mb = (
            persistent_index_mb
            + search_peak_memory_mb
        )

    return {
        "dataset": dataset,
        "size_chars": size,
        "algorithm": algorithm,
        "preprocessing_seconds": (
            preprocessing_seconds
        ),
        "average_search_seconds": (
            average_search_seconds
        ),
        "persistent_index_mb": (
            persistent_index_mb
        ),
        "search_peak_memory_mb": (
            search_peak_memory_mb
        ),
        "combined_memory_mb": (
            combined_memory_mb
        ),
        "matches": matches,
        "collisions": collisions,
        "skipped": skipped,
    }


def benchmark_dataset(
    name: str,
    size: int,
    repeats: int = 5,
    tree_limit: int = TREE_MAX_CHARS,
) -> Tuple[
    List[Dict],
    Dict,
]:
    """Benchmark all appropriate algorithms on one dataset."""
    text, expected_positions = create_dataset(
        size,
        seed=size,
    )

    rows = []

    kmp_searcher = lambda: kmp_search(
        text,
        BENCHMARK_PATTERN,
    )

    (
        kmp_positions,
        kmp_query_time,
    ) = _average_search_time(
        kmp_searcher,
        repeats,
    )

    if kmp_positions != expected_positions:
        raise RuntimeError(
            "KMP returned unexpected positions"
        )

    kmp_search_memory = _measure_search_memory(
        kmp_searcher
    )

    rows.append(
        _result_row(
            name,
            size,
            "KMP",
            0.0,
            kmp_query_time,
            0.0,
            kmp_search_memory,
            len(
                kmp_positions
            ),
        )
    )

    rk_searcher = lambda: rabin_karp_search(
        text,
        BENCHMARK_PATTERN,
    )

    (
        rk_positions,
        rk_query_time,
    ) = _average_search_time(
        rk_searcher,
        repeats,
    )

    if rk_positions != expected_positions:
        raise RuntimeError(
            "Rabin-Karp returned unexpected positions"
        )

    rk_search_memory = _measure_search_memory(
        rk_searcher
    )

    rk_stats = rabin_karp_search_with_stats(
        text,
        BENCHMARK_PATTERN,
    )

    rows.append(
        _result_row(
            name,
            size,
            "Rabin-Karp",
            0.0,
            rk_query_time,
            0.0,
            rk_search_memory,
            len(
                rk_positions
            ),
            collisions=rk_stats.collisions,
        )
    )

    (
        suffix_array,
        sa_preprocessing,
    ) = _measure_build(
        lambda: SuffixArrayIndex(
            text
        )
    )

    sa_index_memory = _suffix_array_memory_mb(
        suffix_array
    )

    sa_searcher = lambda: suffix_array.find(
        BENCHMARK_PATTERN
    )

    (
        sa_positions,
        sa_query_time,
    ) = _average_search_time(
        sa_searcher,
        repeats,
    )

    if sa_positions != expected_positions:
        raise RuntimeError(
            "Suffix array returned unexpected positions"
        )

    sa_search_memory = _measure_search_memory(
        sa_searcher
    )

    rows.append(
        _result_row(
            name,
            size,
            "Suffix Array",
            sa_preprocessing,
            sa_query_time,
            sa_index_memory,
            sa_search_memory,
            len(
                sa_positions
            ),
        )
    )

    if size <= tree_limit:
        (
            suffix_tree,
            tree_preprocessing,
        ) = _measure_build(
            lambda: CompressedSuffixTree(
                text
            )
        )

        tree_index_memory = (
            _suffix_tree_memory_mb(
                suffix_tree
            )
        )

        tree_searcher = lambda: suffix_tree.find(
            BENCHMARK_PATTERN
        )

        (
            tree_positions,
            tree_query_time,
        ) = _average_search_time(
            tree_searcher,
            repeats,
        )

        if tree_positions != expected_positions:
            raise RuntimeError(
                "Suffix tree returned unexpected positions"
            )

        tree_search_memory = (
            _measure_search_memory(
                tree_searcher
            )
        )

        rows.append(
            _result_row(
                name,
                size,
                "Suffix Tree",
                tree_preprocessing,
                tree_query_time,
                tree_index_memory,
                tree_search_memory,
                len(
                    tree_positions
                ),
            )
        )

    else:
        rows.append(
            _result_row(
                name,
                size,
                "Suffix Tree",
                None,
                None,
                None,
                None,
                None,
                skipped=True,
            )
        )

    lcp_values = suffix_array.lcp

    lcp_stats = {
        "dataset": name,
        "size_chars": size,
        "mean_lcp": (
            float(
                np.mean(
                    lcp_values
                )
            )
            if lcp_values
            else 0.0
        ),
        "max_lcp": (
            max(
                lcp_values
            )
            if lcp_values
            else 0
        ),
    }

    return (
        rows,
        lcp_stats,
    )


def collision_experiment(
    text_size: int = 20_000,
) -> pd.DataFrame:
    """Measure Rabin-Karp collisions using several moduli."""
    if text_size < 200:
        raise ValueError(
            "text_size must be at least 200"
        )

    text = random_text(
        text_size,
        alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        seed=2026,
    )

    pattern = "ALGORITHM"

    text = embed_pattern(
        text,
        pattern,
        [
            text_size // 2
        ],
    )

    rows = []

    for modulus in COLLISION_MODULI:
        result = rabin_karp_search_with_stats(
            text,
            pattern,
            base=256,
            modulus=modulus,
        )

        rows.append(
            {
                "modulus": modulus,
                "hash_hits": result.hash_hits,
                "collisions": result.collisions,
                "matches": len(
                    result.matches
                ),
            }
        )

    return pd.DataFrame(
        rows
    )


def plot_runtime_comparison(
    results: pd.DataFrame,
    output_path: Path,
) -> None:
    """Plot average search latency by dataset and algorithm."""
    usable = results[
        results[
            "skipped"
        ]
        == False
    ].copy()

    usable[
        "search_ms"
    ] = (
        usable[
            "average_search_seconds"
        ]
        * 1000
    )

    pivot = usable.pivot(
        index="dataset",
        columns="algorithm",
        values="search_ms",
    )

    axis = pivot.plot(
        kind="bar",
        figsize=(
            10,
            6,
        ),
    )

    axis.set_title(
        "String Search Runtime Comparison"
    )

    axis.set_xlabel(
        "Dataset"
    )

    axis.set_ylabel(
        "Average Search Time (ms)"
    )

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()


def plot_collision_analysis(
    collisions: pd.DataFrame,
    output_path: Path,
) -> None:
    """Plot Rabin-Karp collision counts by modulus."""
    labels = [
        str(
            value
        )
        for value in collisions[
            "modulus"
        ]
    ]

    values = collisions[
        "collisions"
    ].tolist()

    figure = plt.figure(
        figsize=(
            9,
            5,
        )
    )

    plt.bar(
        labels,
        values,
    )

    plt.title(
        "Rabin-Karp Collision Analysis"
    )

    plt.xlabel(
        "Modulus"
    )

    plt.ylabel(
        "Hash Collisions"
    )

    plt.xticks(
        rotation=30
    )

    plt.tight_layout()

    figure.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def plot_sa_lcp_stats(
    lcp_stats: pd.DataFrame,
    output_path: Path,
) -> None:
    """Plot mean and maximum LCP values by dataset."""
    plot_frame = lcp_stats.set_index(
        "dataset"
    )[
        [
            "mean_lcp",
            "max_lcp",
        ]
    ]

    axis = plot_frame.plot(
        kind="bar",
        figsize=(
            9,
            5,
        ),
    )

    axis.set_title(
        "Suffix Array LCP Statistics"
    )

    axis.set_xlabel(
        "Dataset"
    )

    axis.set_ylabel(
        "LCP Length"
    )

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()


def plot_dataset_heatmap(
    results: pd.DataFrame,
    output_path: Path,
) -> None:
    """Plot search latency as a dataset-size heatmap."""
    algorithms = [
        "KMP",
        "Rabin-Karp",
        "Suffix Array",
        "Suffix Tree",
    ]

    datasets = list(
        dict.fromkeys(
            results[
                "dataset"
            ].tolist()
        )
    )

    matrix = np.full(
        (
            len(
                algorithms
            ),
            len(
                datasets
            ),
        ),
        np.nan,
    )

    for row_index, algorithm in enumerate(
        algorithms
    ):
        for column_index, dataset in enumerate(
            datasets
        ):
            matches = results[
                (
                    results[
                        "algorithm"
                    ]
                    == algorithm
                )
                & (
                    results[
                        "dataset"
                    ]
                    == dataset
                )
                & (
                    results[
                        "skipped"
                    ]
                    == False
                )
            ]

            if not matches.empty:
                matrix[
                    row_index,
                    column_index,
                ] = (
                    matches.iloc[
                        0
                    ][
                        "average_search_seconds"
                    ]
                    * 1000
                )

    figure = plt.figure(
        figsize=(
            9,
            5,
        )
    )

    image = plt.imshow(
        matrix,
        aspect="auto",
    )

    plt.colorbar(
        image,
        label="Average Search Time (ms)",
    )

    plt.xticks(
        range(
            len(
                datasets
            )
        ),
        datasets,
        rotation=20,
    )

    plt.yticks(
        range(
            len(
                algorithms
            )
        ),
        algorithms,
    )

    plt.title(
        "Search Time Heatmap by Dataset Size"
    )

    for row in range(
        len(
            algorithms
        )
    ):
        for column in range(
            len(
                datasets
            )
        ):
            value = matrix[
                row,
                column
            ]

            label = (
                "skip"
                if np.isnan(
                    value
                )
                else f"{value:.3f}"
            )

            plt.text(
                column,
                row,
                label,
                ha="center",
                va="center",
            )

    plt.tight_layout()

    figure.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(
        figure
    )


def run_benchmark(
    output_dir: str | Path,
    smoke: bool = False,
) -> Tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    """Run the benchmark and create all required result artifacts."""
    output = Path(
        output_dir
    )

    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    datasets = (
        SMOKE_DATASETS
        if smoke
        else FULL_DATASETS
    )

    repeats = (
        2
        if smoke
        else 5
    )

    result_rows = []
    lcp_rows = []

    for name, size in datasets.items():
        print(
            f"Benchmarking {name} "
            f"({size:,} characters)..."
        )

        rows, lcp_stats = benchmark_dataset(
            name,
            size,
            repeats=repeats,
        )

        result_rows.extend(
            rows
        )

        lcp_rows.append(
            lcp_stats
        )

    results = pd.DataFrame(
        result_rows
    )

    lcp_frame = pd.DataFrame(
        lcp_rows
    )

    collision_size = (
        2_000
        if smoke
        else 20_000
    )

    collision_frame = collision_experiment(
        collision_size
    )

    results.to_csv(
        output
        / "benchmark_results.csv",
        index=False,
    )

    collision_frame.to_csv(
        output
        / "collision_results.csv",
        index=False,
    )

    lcp_frame.to_csv(
        output
        / "sa_lcp_stats.csv",
        index=False,
    )

    plot_runtime_comparison(
        results,
        output
        / "runtime_comparison.png",
    )

    plot_collision_analysis(
        collision_frame,
        output
        / "collision_analysis.png",
    )

    plot_sa_lcp_stats(
        lcp_frame,
        output
        / "sa_lcp_stats.png",
    )

    plot_dataset_heatmap(
        results,
        output
        / "heatmap_dataset_sizes.png",
    )

    return (
        results,
        collision_frame,
        lcp_frame,
    )


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description=(
            "Benchmark Week 11 string-search algorithms."
        )
    )

    parser.add_argument(
        "--smoke",
        action="store_true",
        help=(
            "Run a small validation benchmark "
            "instead of the full benchmark."
        ),
    )

    parser.add_argument(
        "--output",
        default=(
            "StringSearchEngine/"
            "benchmarks/results"
        ),
        help="Directory for CSV and plot output.",
    )

    arguments = parser.parse_args()

    results, collisions, lcp_stats = (
        run_benchmark(
            arguments.output,
            smoke=arguments.smoke,
        )
    )

    print()
    print(
        results.to_string(
            index=False
        )
    )

    print()
    print(
        "Collision experiment:"
    )

    print(
        collisions.to_string(
            index=False
        )
    )

    print()
    print(
        "LCP statistics:"
    )

    print(
        lcp_stats.to_string(
            index=False
        )
    )


if __name__ == "__main__":
    main()