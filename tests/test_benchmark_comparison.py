"""Tests for the Week 9 approximation benchmark."""

from benchmarks.week9_approx_benchmark import (
    benchmark_facility_location,
    benchmark_maxcut,
    benchmark_set_cover,
    benchmark_tsp,
    benchmark_vertex_cover,
    generate_facility_instance,
    generate_set_cover_instance,
)


def test_vertex_cover_benchmark_rows():
    rows = benchmark_vertex_cover(
        [
            4
        ]
    )

    assert len(
        rows
    ) == 2

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Exact Exhaustive",
        "2-Approximation",
    }


def test_vertex_cover_ratio_within_guarantee():
    rows = benchmark_vertex_cover(
        [
            4
        ]
    )

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


def test_facility_location_benchmark_rows():
    rows = benchmark_facility_location(
        [
            3
        ]
    )

    assert len(
        rows
    ) == 2

    heuristic = next(
        row
        for row in rows
        if row["algorithm"]
        == "Greedy Heuristic"
    )

    assert (
        heuristic[
            "approximation_ratio"
        ]
        >= 1.0
    )


def test_set_cover_benchmark_rows():
    rows = benchmark_set_cover(
        sizes=[
            4
        ],
        randomized_trials=3,
    )

    assert len(
        rows
    ) == 3

    algorithms = {
        row["algorithm"]
        for row in rows
    }

    assert algorithms == {
        "Exact Exhaustive",
        "Deterministic LP Rounding",
        "Randomized LP Rounding",
    }


def test_tsp_benchmark_ratio_within_two():
    rows = benchmark_tsp(
        [
            4
        ]
    )

    approximate = next(
        row
        for row in rows
        if row["algorithm"]
        == "MST Doubling"
    )

    assert (
        1.0
        <= approximate[
            "approximation_ratio"
        ]
        <= 2.0
    )


def test_maxcut_benchmark_rows():
    rows = benchmark_maxcut(
        sizes=[
            6
        ],
        randomized_trials=5,
        local_trials=3,
    )

    assert len(
        rows
    ) == 3

    randomized = next(
        row
        for row in rows
        if row["algorithm"]
        == "Randomized"
    )

    local = next(
        row
        for row in rows
        if row["algorithm"]
        == "Local Search"
    )

    assert (
        0.0
        <= randomized[
            "approximation_ratio"
        ]
        <= 1.0
    )

    assert (
        0.0
        <= local[
            "approximation_ratio"
        ]
        <= 1.0
    )


def test_generators_are_reproducible():
    first_facility = generate_facility_instance(
        3,
        seed=42,
    )

    second_facility = generate_facility_instance(
        3,
        seed=42,
    )

    assert (
        first_facility
        == second_facility
    )

    first_set_cover = generate_set_cover_instance(
        4,
        seed=42,
    )

    second_set_cover = generate_set_cover_instance(
        4,
        seed=42,
    )

    assert (
        first_set_cover
        == second_set_cover
    )