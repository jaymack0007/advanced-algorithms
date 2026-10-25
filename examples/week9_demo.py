"""Demonstration of the Week 9 approximation algorithms."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


from src.approximation.facility_location_greedy import (
    exact_facility_location,
    greedy_facility_location,
)
from src.approximation.maxcut_randomized import (
    exact_maxcut,
    local_search_maxcut,
    randomized_maxcut,
)
from src.approximation.set_cover_lpround import (
    deterministic_lp_rounding,
    exact_set_cover,
    randomized_lp_rounding,
)
from src.approximation.tsp_metric_approx import (
    exact_metric_tsp,
    mst_doubling_tsp,
)
from src.approximation.vertex_cover_2approx import (
    exact_vertex_cover,
    vertex_cover_2approx,
)


def vertex_cover_demo():
    """Demonstrate the Vertex Cover 2-approximation."""
    print("\n=== Vertex Cover ===")

    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "A"),
    ]

    approximate = vertex_cover_2approx(
        edges
    )

    optimal = exact_vertex_cover(
        edges
    )

    print(
        "Approximate cover:",
        sorted(approximate),
    )

    print(
        "Optimal cover:",
        sorted(optimal),
    )

    print(
        "Approximation ratio:",
        len(approximate)
        / len(optimal),
    )


def facility_location_demo():
    """Demonstrate greedy Facility Location."""
    print("\n=== Facility Location ===")

    opening_costs = {
        "F1": 4.0,
        "F2": 4.0,
        "F3": 7.0,
    }

    clients = [
        "C1",
        "C2",
        "C3",
        "C4",
    ]

    service_costs = {
        ("F1", "C1"): 1.0,
        ("F1", "C2"): 1.0,
        ("F1", "C3"): 8.0,
        ("F1", "C4"): 8.0,
        ("F2", "C1"): 8.0,
        ("F2", "C2"): 8.0,
        ("F2", "C3"): 1.0,
        ("F2", "C4"): 1.0,
        ("F3", "C1"): 3.0,
        ("F3", "C2"): 3.0,
        ("F3", "C3"): 3.0,
        ("F3", "C4"): 3.0,
    }

    greedy = greedy_facility_location(
        opening_costs,
        clients,
        service_costs,
    )

    optimal = exact_facility_location(
        opening_costs,
        clients,
        service_costs,
    )

    print(
        "Greedy facilities:",
        sorted(
            greedy.open_facilities
        ),
    )

    print(
        "Greedy cost:",
        greedy.total_cost,
    )

    print(
        "Optimal facilities:",
        sorted(
            optimal.open_facilities
        ),
    )

    print(
        "Optimal cost:",
        optimal.total_cost,
    )


def set_cover_demo():
    """Demonstrate LP rounding for Set Cover."""
    print("\n=== Set Cover ===")

    universe = {
        "A",
        "B",
        "C",
    }

    subsets = {
        "S1": {
            "A",
            "B",
        },
        "S2": {
            "B",
            "C",
        },
        "S3": {
            "A",
            "C",
        },
    }

    costs = {
        "S1": 1.0,
        "S2": 1.0,
        "S3": 1.0,
    }

    deterministic = deterministic_lp_rounding(
        universe,
        subsets,
        costs,
    )

    randomized = randomized_lp_rounding(
        universe,
        subsets,
        costs,
        seed=42,
    )

    optimal = exact_set_cover(
        universe,
        subsets,
        costs,
    )

    print(
        "LP lower bound:",
        deterministic.lp_cost,
    )

    print(
        "Deterministic sets:",
        sorted(
            deterministic.selected_sets
        ),
        "cost:",
        deterministic.total_cost,
    )

    print(
        "Randomized sets:",
        sorted(
            randomized.selected_sets
        ),
        "cost:",
        randomized.total_cost,
    )

    print(
        "Optimal sets:",
        sorted(
            optimal.selected_sets
        ),
        "cost:",
        optimal.total_cost,
    )


def tsp_demo():
    """Demonstrate the metric TSP approximation."""
    print("\n=== Metric TSP ===")

    points = {
        "A": (
            0.0,
            0.0,
        ),
        "B": (
            1.0,
            0.0,
        ),
        "C": (
            1.0,
            1.0,
        ),
        "D": (
            0.0,
            1.0,
        ),
    }

    approximate_tour, approximate_cost = (
        mst_doubling_tsp(
            points,
            start="A",
        )
    )

    optimal_tour, optimal_cost = (
        exact_metric_tsp(
            points,
            start="A",
        )
    )

    print(
        "MST-doubling tour:",
        approximate_tour,
    )

    print(
        "Approximate cost:",
        approximate_cost,
    )

    print(
        "Optimal tour:",
        optimal_tour,
    )

    print(
        "Optimal cost:",
        optimal_cost,
    )


def maxcut_demo():
    """Demonstrate randomized and local-search Max-Cut."""
    print("\n=== Max-Cut ===")

    edges = [
        ("A", "B"),
        ("B", "C"),
        ("C", "D"),
        ("D", "A"),
        ("A", "C"),
    ]

    randomized = randomized_maxcut(
        edges,
        seed=42,
    )

    local = local_search_maxcut(
        edges,
        seed=42,
    )

    optimal = exact_maxcut(
        edges
    )

    print(
        "Randomized cut:",
        randomized.cut_value,
    )

    print(
        "Local-search cut:",
        local.cut_value,
    )

    print(
        "Optimal cut:",
        optimal.cut_value,
    )


def main():
    """Run all Week 9 demonstrations."""
    print(
        "Week 9 Approximation Algorithms Demo"
    )

    vertex_cover_demo()
    facility_location_demo()
    set_cover_demo()
    tsp_demo()
    maxcut_demo()

    print(
        "\nDemo complete."
    )


if __name__ == "__main__":
    main()