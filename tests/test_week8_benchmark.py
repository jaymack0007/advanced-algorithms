"""Tests for the Week 8 complexity benchmark."""

from benchmarks.week8_complexity_benchmark import (
    benchmark_sat,
    benchmark_subset_sum,
    benchmark_tsp,
    benchmark_vertex_cover,
    cycle_graph,
    generate_sat_formula,
    generate_tsp_points,
)


def test_subset_sum_benchmark():
    rows = benchmark_subset_sum(
        sizes=[6],
        trials=1,
    )

    assert len(rows) == 2

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Exact Backtracking",
        "Greedy Heuristic",
    }

    exact = next(
        row
        for row in rows
        if row["algorithm"]
        == "Exact Backtracking"
    )

    assert exact["nodes_visited"] > 0
    assert exact["mean_time_seconds"] >= 0


def test_sat_benchmark():
    rows = benchmark_sat(
        sizes=[4],
        trials=1,
        heuristic_trials=10,
    )

    assert len(rows) == 2

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Exact Backtracking",
        "Random Heuristic",
    }


def test_vertex_cover_benchmark():
    rows = benchmark_vertex_cover(
        sizes=[4]
    )

    assert len(rows) == 2

    approximate = next(
        row
        for row in rows
        if row["algorithm"]
        == "2-Approximation"
    )

    assert (
        1.0
        <= approximate[
            "approximation_ratio"
        ]
        <= 2.0
    )


def test_tsp_benchmark():
    rows = benchmark_tsp(
        sizes=[4]
    )

    assert len(rows) == 2

    heuristic = next(
        row
        for row in rows
        if row["algorithm"]
        == "Nearest Neighbor"
    )

    assert (
        heuristic[
            "approximation_ratio"
        ]
        >= 1.0
    )


def test_cycle_graph():
    edges = cycle_graph(
        5
    )

    assert len(
        edges
    ) == 5

    assert (
        "v4",
        "v0",
    ) in edges


def test_generators_are_reproducible():
    first_formula = generate_sat_formula(
        6,
        seed=42,
    )

    second_formula = generate_sat_formula(
        6,
        seed=42,
    )

    assert first_formula == second_formula

    first_points = generate_tsp_points(
        5,
        seed=42,
    )

    second_points = generate_tsp_points(
        5,
        seed=42,
    )

    assert first_points == second_points