"""Week 6 advanced dynamic programming demonstration."""

import sys
from math import inf
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.dp_advanced.bitmask_traveling_salesman import (
    tsp_bitmask,
)
from src.dp_advanced.floyd_warshall import (
    floyd_warshall,
    reconstruct_path,
)
from src.dp_advanced.matrix_chain_multiplication import (
    matrix_chain_bottom_up,
    matrix_chain_memoized,
)
from src.dp_advanced.space_optimized_knapsack import (
    space_optimized_knapsack,
)


def main():
    """Run small examples of each Week 6 algorithm."""
    print("Week 6 Advanced Dynamic Programming Demo")
    print()

    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    knapsack_result = space_optimized_knapsack(
        weights,
        values,
        capacity,
    )

    print(
        "Space-Optimized Knapsack:",
        knapsack_result,
    )

    dimensions = [
        30,
        35,
        15,
        5,
        10,
        20,
        25,
    ]

    memo_cost, memo_order = (
        matrix_chain_memoized(
            dimensions
        )
    )

    bottom_cost, bottom_order = (
        matrix_chain_bottom_up(
            dimensions
        )
    )

    print(
        "MCM Memoized:",
        memo_cost,
        memo_order,
    )

    print(
        "MCM Bottom-Up:",
        bottom_cost,
        bottom_order,
    )

    graph = [
        [0, 5, inf, 10],
        [inf, 0, 3, inf],
        [inf, inf, 0, 1],
        [inf, inf, inf, 0],
    ]

    distances, predecessors = (
        floyd_warshall(
            graph
        )
    )

    path = reconstruct_path(
        predecessors,
        0,
        3,
    )

    print(
        "Floyd-Warshall 0 to 3:",
        distances[0][3],
        path,
    )

    tsp_distances = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]

    tsp_cost, tsp_tour = tsp_bitmask(
        tsp_distances
    )

    print(
        "Bitmask TSP:",
        tsp_cost,
        tsp_tour,
    )


if __name__ == "__main__":
    main()