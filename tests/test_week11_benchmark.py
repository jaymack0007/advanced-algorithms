"""Tests for the Week 11 string-search benchmark."""

import pandas as pd
import pytest

from StringSearchEngine.benchmarks.benchmark_search import (
    BENCHMARK_PATTERN,
    COLLISION_MODULI,
    benchmark_dataset,
    collision_experiment,
    create_dataset,
    run_benchmark,
)


def test_create_dataset_length():
    text, _ = create_dataset(
        1000
    )

    assert len(
        text
    ) == 1000


def test_create_dataset_positions():
    text, positions = create_dataset(
        1000
    )

    for position in positions:
        assert text.startswith(
            BENCHMARK_PATTERN,
            position,
        )


def test_create_dataset_three_positions():
    _, positions = create_dataset(
        1000
    )

    assert len(
        positions
    ) == 3


def test_create_dataset_is_deterministic():
    first, first_positions = create_dataset(
        1000,
        seed=7,
    )

    second, second_positions = create_dataset(
        1000,
        seed=7,
    )

    assert first == second

    assert (
        first_positions
        == second_positions
    )


def test_small_size_rejected():
    with pytest.raises(ValueError):
        create_dataset(
            100
        )


def test_benchmark_dataset_returns_four_algorithms():
    rows, _ = benchmark_dataset(
        "test",
        500,
        repeats=1,
        tree_limit=1000,
    )

    assert [
        row[
            "algorithm"
        ]
        for row in rows
    ] == [
        "KMP",
        "Rabin-Karp",
        "Suffix Array",
        "Suffix Tree",
    ]


def test_benchmark_algorithms_agree_on_match_count():
    rows, _ = benchmark_dataset(
        "test",
        500,
        repeats=1,
        tree_limit=1000,
    )

    assert {
        row[
            "matches"
        ]
        for row in rows
    } == {
        3
    }


def test_tree_can_be_skipped():
    rows, _ = benchmark_dataset(
        "test",
        500,
        repeats=1,
        tree_limit=100,
    )

    tree_row = next(
        row
        for row in rows
        if row[
            "algorithm"
        ]
        == "Suffix Tree"
    )

    assert tree_row[
        "skipped"
    ] is True


def test_lcp_stats_returned():
    _, stats = benchmark_dataset(
        "test",
        500,
        repeats=1,
        tree_limit=1000,
    )

    assert stats[
        "dataset"
    ] == "test"

    assert stats[
        "max_lcp"
    ] >= 0


def test_collision_experiment_dataframe():
    frame = collision_experiment(
        500
    )

    assert isinstance(
        frame,
        pd.DataFrame,
    )


def test_collision_experiment_all_moduli():
    frame = collision_experiment(
        500
    )

    assert frame[
        "modulus"
    ].tolist() == COLLISION_MODULI


def test_collision_experiment_preserves_match():
    frame = collision_experiment(
        500
    )

    assert set(
        frame[
            "matches"
        ].tolist()
    ) == {
        1
    }


def test_smoke_benchmark_creates_csv_files(
    tmp_path,
):
    run_benchmark(
        tmp_path,
        smoke=True,
    )

    assert (
        tmp_path
        / "benchmark_results.csv"
    ).exists()

    assert (
        tmp_path
        / "collision_results.csv"
    ).exists()

    assert (
        tmp_path
        / "sa_lcp_stats.csv"
    ).exists()


def test_smoke_benchmark_creates_required_plots(
    tmp_path,
):
    run_benchmark(
        tmp_path,
        smoke=True,
    )

    required = [
        "runtime_comparison.png",
        "collision_analysis.png",
        "sa_lcp_stats.png",
        "heatmap_dataset_sizes.png",
    ]

    for filename in required:
        path = (
            tmp_path
            / filename
        )

        assert path.exists()
        assert path.stat().st_size > 0