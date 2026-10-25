"""Tests for the Week 6 benchmark system."""

from benchmarks.week6_dp_advanced_benchmark import (
    benchmark_floyd_warshall,
    benchmark_knapsack,
    benchmark_mcm,
    benchmark_tsp,
    make_knapsack_data,
)
from src.utils.matrix_utils import (
    generate_complete_distance_matrix,
    generate_matrix_dimensions,
    generate_weighted_graph_matrix,
)


def test_knapsack_benchmark():
    rows = benchmark_knapsack(
        sizes=[5],
    )

    assert len(rows) == 2

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Standard DP",
        "Space Optimized",
    }

    for row in rows:
        assert row["problem"] == "Knapsack"
        assert row["input_size"] == 5
        assert row["status"] == "measured"
        assert row["time_seconds"] >= 0
        assert row["memory_bytes"] >= 0


def test_mcm_benchmark():
    rows = benchmark_mcm(
        sizes=[4],
    )

    assert len(rows) == 2

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Memoized",
        "Bottom Up",
    }

    for row in rows:
        assert row["problem"] == "MCM"
        assert row["input_size"] == 4
        assert row["status"] == "measured"
        assert row["time_seconds"] >= 0


def test_floyd_warshall_benchmark():
    rows = benchmark_floyd_warshall(
        sizes=[5],
    )

    assert len(rows) == 2

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Floyd-Warshall",
        "Repeated Dijkstra",
    }

    for row in rows:
        assert row["problem"] == "Floyd-Warshall"
        assert row["input_size"] == 5
        assert row["time_seconds"] >= 0


def test_tsp_benchmark():
    rows = benchmark_tsp(
        sizes=[4],
        brute_force_max=4,
    )

    assert len(rows) == 2

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Brute Force",
        "Bitmask DP",
    }

    for row in rows:
        assert row["problem"] == "TSP"
        assert row["input_size"] == 4
        assert row["status"] == "measured"
        assert row["time_seconds"] >= 0


def test_tsp_brute_force_skip():
    rows = benchmark_tsp(
        sizes=[5],
        brute_force_max=4,
    )

    brute_row = next(
        row
        for row in rows
        if row["algorithm"] == "Brute Force"
    )

    bitmask_row = next(
        row
        for row in rows
        if row["algorithm"] == "Bitmask DP"
    )

    assert (
        brute_row["status"]
        == "skipped_factorial"
    )

    assert brute_row["time_seconds"] is None
    assert bitmask_row["status"] == "measured"


def test_knapsack_data_generator():
    weights, values, capacity = (
        make_knapsack_data(10)
    )

    assert len(weights) == 10
    assert len(values) == 10
    assert capacity > 0

    assert all(
        weight > 0
        for weight in weights
    )

    assert all(
        value > 0
        for value in values
    )


def test_matrix_generators_are_deterministic():
    graph_one = (
        generate_weighted_graph_matrix(
            5,
            seed=50,
        )
    )

    graph_two = (
        generate_weighted_graph_matrix(
            5,
            seed=50,
        )
    )

    tsp_one = (
        generate_complete_distance_matrix(
            5,
            seed=50,
        )
    )

    tsp_two = (
        generate_complete_distance_matrix(
            5,
            seed=50,
        )
    )

    assert graph_one == graph_two
    assert tsp_one == tsp_two


def test_matrix_dimension_generator():
    dimensions = (
        generate_matrix_dimensions(
            6,
            seed=50,
        )
    )

    assert len(dimensions) == 7

    assert all(
        dimension > 0
        for dimension in dimensions
    )