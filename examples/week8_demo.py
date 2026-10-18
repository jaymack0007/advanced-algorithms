"""Demonstration of the Week 8 complexity algorithms."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.complexity.reduction_demo import (
    assignment_to_vertex_cover,
    explain_reduction,
    is_vertex_cover as reduction_is_vertex_cover,
    reduce_3sat_to_vertex_cover,
)
from src.complexity.satisfiability_solver import (
    evaluate_formula,
    random_sat_heuristic,
    sat_backtracking,
)
from src.complexity.subset_sum_backtracking import (
    greedy_subset_sum,
    subset_sum_backtracking,
)
from src.complexity.traveling_salesman_approx import (
    approximation_ratio as tsp_ratio,
    exact_tsp,
    nearest_neighbor_tsp,
)
from src.complexity.vertex_cover_approx import (
    approximation_ratio as vertex_cover_ratio,
    exact_vertex_cover,
    vertex_cover_2approx,
)


def reduction_demo():
    """Show a small 3-SAT to Vertex Cover reduction."""
    print("=== 3-SAT to Vertex Cover Reduction ===")

    clauses = [
        (
            "x1",
            "~x2",
            "x3",
        ),
        (
            "~x1",
            "x2",
            "x3",
        ),
    ]

    assignment = {
        "x1": True,
        "x2": True,
        "x3": True,
    }

    reduction = reduce_3sat_to_vertex_cover(
        clauses
    )

    cover = assignment_to_vertex_cover(
        reduction,
        assignment,
    )

    print(
        explain_reduction(
            reduction
        )
    )

    print(
        f"Target cover size: {reduction.target_size}"
    )

    print(
        f"Constructed cover size: {len(cover)}"
    )

    print(
        "Valid vertex cover:",
        reduction_is_vertex_cover(
            reduction.edges,
            cover,
        ),
    )

    print()


def subset_sum_demo():
    """Compare exact and greedy Subset Sum."""
    print("=== Subset Sum ===")

    values = [
        6,
        4,
        3,
    ]

    target = 7

    stats = {}

    exact = subset_sum_backtracking(
        values,
        target,
        stats,
    )

    greedy = greedy_subset_sum(
        values,
        target,
    )

    print(
        f"Values: {values}"
    )

    print(
        f"Target: {target}"
    )

    print(
        f"Exact solution: {exact}"
    )

    print(
        f"Nodes visited: {stats['nodes_visited']}"
    )

    print(
        f"Greedy result: {greedy}"
    )

    print()


def sat_demo():
    """Compare exact and randomized SAT methods."""
    print("=== SAT ===")

    clauses = [
        (
            "x1",
            "x2",
        ),
        (
            "~x1",
            "x3",
        ),
        (
            "~x2",
            "x3",
        ),
    ]

    exact = sat_backtracking(
        clauses
    )

    heuristic = random_sat_heuristic(
        clauses,
        trials=100,
        seed=42,
    )

    print(
        f"Exact assignment: {exact}"
    )

    print(
        "Exact assignment satisfies formula:",
        (
            exact is not None
            and evaluate_formula(
                clauses,
                exact,
            )
        ),
    )

    print(
        f"Random heuristic assignment: {heuristic}"
    )

    print()


def vertex_cover_demo():
    """Compare exact and approximate Vertex Cover."""
    print("=== Vertex Cover ===")

    edges = [
        (
            "A",
            "B",
        ),
        (
            "B",
            "C",
        ),
        (
            "C",
            "D",
        ),
        (
            "D",
            "A",
        ),
    ]

    optimal = exact_vertex_cover(
        edges
    )

    approximate = vertex_cover_2approx(
        edges
    )

    ratio = vertex_cover_ratio(
        approximate,
        optimal,
    )

    print(
        f"Optimal cover: {sorted(optimal)}"
    )

    print(
        f"2-approximation cover: {sorted(approximate)}"
    )

    print(
        f"Approximation ratio: {ratio:.3f}"
    )

    print()


def tsp_demo():
    """Compare exact and nearest-neighbor TSP."""
    print("=== Traveling Salesman Problem ===")

    points = {
        "A": (
            0.0,
            0.0,
        ),
        "B": (
            2.0,
            0.0,
        ),
        "C": (
            2.0,
            2.0,
        ),
        "D": (
            0.0,
            2.0,
        ),
        "E": (
            1.0,
            3.0,
        ),
    }

    exact_tour, exact_length = exact_tsp(
        points,
        start="A",
    )

    heuristic_tour, heuristic_length = nearest_neighbor_tsp(
        points,
        start="A",
    )

    ratio = tsp_ratio(
        heuristic_length,
        exact_length,
    )

    print(
        f"Optimal tour: {exact_tour}"
    )

    print(
        f"Optimal length: {exact_length:.3f}"
    )

    print(
        f"Nearest-neighbor tour: {heuristic_tour}"
    )

    print(
        f"Nearest-neighbor length: {heuristic_length:.3f}"
    )

    print(
        f"Approximation ratio: {ratio:.3f}"
    )

    print()


def main():
    """Run all Week 8 demonstrations."""
    print(
        "Week 8: Computational Complexity and Approximation"
    )

    print()

    reduction_demo()
    subset_sum_demo()
    sat_demo()
    vertex_cover_demo()
    tsp_demo()


if __name__ == "__main__":
    main()