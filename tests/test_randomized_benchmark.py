"""Tests for the Week 7 randomized benchmark."""

from benchmarks.week7_randomized_benchmark import (
    benchmark_bloom_filter,
    benchmark_minhash,
    benchmark_primality,
    benchmark_quicksort,
    benchmark_selection,
    expected_quicksort_comparisons,
)


def test_quicksort_benchmark():
    rows = benchmark_quicksort(
        sizes=[100],
        trials=2,
    )

    assert len(rows) == 2

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Randomized QuickSort",
        "Deterministic QuickSort",
    }

    for row in rows:
        assert row["problem"] == "QuickSort"
        assert row["input_size"] == 100
        assert row["mean_time_seconds"] >= 0
        assert row["accuracy"] == 1.0


def test_expected_quicksort_comparisons():
    result = expected_quicksort_comparisons(
        100
    )

    assert result > 0


def test_selection_benchmark():
    rows = benchmark_selection(
        sizes=[100],
        trials=2,
    )

    assert len(rows) == 6

    randomized = [
        row
        for row in rows
        if row["algorithm"].startswith(
            "Randomized"
        )
    ]

    assert len(randomized) == 3

    for row in randomized:
        assert row["accuracy"] == 1.0
        assert row["average_depth"] > 0


def test_primality_benchmark():
    rows = benchmark_primality(
        iteration_counts=[5],
        trials=2,
    )

    assert len(rows) == 3

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Deterministic Trial Division",
        "Fermat k=5",
        "Miller-Rabin k=5",
    }


def test_miller_rabin_error_bound_present():
    rows = benchmark_primality(
        iteration_counts=[5],
        trials=2,
    )

    miller = next(
        row
        for row in rows
        if row["algorithm"]
        == "Miller-Rabin k=5"
    )

    assert (
        miller["theoretical_error"]
        == 0.25 ** 5
    )


def test_bloom_filter_benchmark():
    rows = benchmark_bloom_filter(
        insert_counts=[50],
        bit_count=1000,
        hash_count=3,
        query_count=100,
    )

    assert len(rows) == 1

    row = rows[0]

    assert row["problem"] == "Bloom Filter"
    assert 0 <= row["error_rate"] <= 1
    assert 0 <= row["theoretical_error"] <= 1
    assert 0 <= row["load_factor"] <= 1


def test_minhash_benchmark():
    rows = benchmark_minhash(
        signature_sizes=[16],
        trials=2,
    )

    assert len(rows) == 1

    row = rows[0]

    assert row["problem"] == "MinHash"
    assert row["input_size"] == 16
    assert 0 <= row["estimated_similarity"] <= 1
    assert 0 <= row["error_rate"] <= 1


def test_randomized_results_have_variance_field():
    rows = benchmark_quicksort(
        sizes=[100],
        trials=2,
    )

    randomized = next(
        row
        for row in rows
        if row["algorithm"]
        == "Randomized QuickSort"
    )

    assert randomized["runtime_variance"] >= 0