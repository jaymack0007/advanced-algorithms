"""Tests for the Week 5 benchmark system."""

from benchmarks.week5_dp_benchmark import (
    benchmark_fibonacci,
    benchmark_knapsack,
    benchmark_lcs,
    fibonacci_recursive_call_count,
    make_knapsack_items,
    make_lcs_strings,
)


def test_fibonacci_call_count():
    assert fibonacci_recursive_call_count(0) == 1
    assert fibonacci_recursive_call_count(1) == 1
    assert fibonacci_recursive_call_count(5) == 15
    assert fibonacci_recursive_call_count(10) == 177


def test_fibonacci_benchmark():
    rows = benchmark_fibonacci(
        sizes=[5],
        naive_max=5,
    )

    assert len(rows) == 3

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Naive Recursive",
        "Memoized",
        "Tabulated",
    }

    for row in rows:
        assert row["problem"] == "Fibonacci"
        assert row["input_size"] == 5
        assert row["status"] == "measured"
        assert row["time_seconds"] >= 0


def test_fibonacci_skip_large_recursive():
    rows = benchmark_fibonacci(
        sizes=[20],
        naive_max=10,
    )

    recursive_row = next(
        row
        for row in rows
        if row["algorithm"] == "Naive Recursive"
    )

    assert (
        recursive_row["status"]
        == "skipped_exponential"
    )
    assert recursive_row["time_seconds"] is None
    assert recursive_row["calls"] > 0


def test_knapsack_generator():
    weights, values, capacity = (
        make_knapsack_items(10)
    )

    assert len(weights) == 10
    assert len(values) == 10
    assert capacity > 0
    assert all(weight > 0 for weight in weights)
    assert all(value > 0 for value in values)


def test_knapsack_benchmark():
    rows = benchmark_knapsack(
        sizes=[5],
        naive_max=5,
    )

    assert len(rows) == 3

    for row in rows:
        assert row["problem"] == "Knapsack"
        assert row["input_size"] == 5
        assert row["status"] == "measured"
        assert row["time_seconds"] >= 0


def test_lcs_generator():
    x1, y1 = make_lcs_strings(10)
    x2, y2 = make_lcs_strings(10)

    assert len(x1) == 10
    assert len(y1) == 10

    assert x1 == x2
    assert y1 == y2


def test_lcs_benchmark():
    rows = benchmark_lcs(
        sizes=[5],
        naive_max=5,
    )

    assert len(rows) == 3

    for row in rows:
        assert row["problem"] == "LCS"
        assert row["input_size"] == 5
        assert row["status"] == "measured"
        assert row["time_seconds"] >= 0


def test_lcs_skip_large_recursive():
    rows = benchmark_lcs(
        sizes=[20],
        naive_max=5,
    )

    recursive_row = next(
        row
        for row in rows
        if row["algorithm"] == "Naive Recursive"
    )

    assert (
        recursive_row["status"]
        == "skipped_exponential"
    )

    assert recursive_row["time_seconds"] is None