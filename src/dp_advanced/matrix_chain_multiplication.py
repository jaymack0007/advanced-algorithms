"""Matrix Chain Multiplication using dynamic programming."""

from functools import lru_cache
from typing import Dict, List, Tuple


def _validate_dimensions(
    dimensions: List[int],
) -> None:
    """Validate matrix-chain dimensions."""
    if len(dimensions) < 2:
        raise ValueError(
            "at least two dimensions are required"
        )

    if any(dimension <= 0 for dimension in dimensions):
        raise ValueError(
            "matrix dimensions must be positive"
        )


def matrix_chain_memoized(
    dimensions: List[int],
) -> Tuple[int, str]:
    """
    Solve Matrix Chain Multiplication using memoization.

    Returns the minimum scalar multiplication cost
    and an optimal parenthesization.
    """
    _validate_dimensions(dimensions)

    matrix_count = len(dimensions) - 1
    split: Dict[Tuple[int, int], int] = {}

    @lru_cache(maxsize=None)
    def solve(
        i: int,
        j: int,
    ) -> int:
        if i == j:
            return 0

        best_cost = float("inf")
        best_split = i

        for k in range(i, j):
            cost = (
                solve(i, k)
                + solve(k + 1, j)
                + dimensions[i - 1]
                * dimensions[k]
                * dimensions[j]
            )

            if cost < best_cost:
                best_cost = cost
                best_split = k

        split[(i, j)] = best_split

        return int(best_cost)

    def build_parenthesization(
        i: int,
        j: int,
    ) -> str:
        if i == j:
            return f"A{i}"

        k = split[(i, j)]

        left = build_parenthesization(
            i,
            k,
        )

        right = build_parenthesization(
            k + 1,
            j,
        )

        return f"({left}{right})"

    minimum_cost = solve(
        1,
        matrix_count,
    )

    order = build_parenthesization(
        1,
        matrix_count,
    )

    return minimum_cost, order


def matrix_chain_bottom_up(
    dimensions: List[int],
) -> Tuple[int, str]:
    """
    Solve Matrix Chain Multiplication using bottom-up DP.

    Returns the minimum scalar multiplication cost
    and an optimal parenthesization.
    """
    _validate_dimensions(dimensions)

    matrix_count = len(dimensions) - 1

    cost = [
        [0] * (matrix_count + 1)
        for _ in range(matrix_count + 1)
    ]

    split = [
        [0] * (matrix_count + 1)
        for _ in range(matrix_count + 1)
    ]

    for chain_length in range(
        2,
        matrix_count + 1,
    ):
        for i in range(
            1,
            matrix_count - chain_length + 2,
        ):
            j = i + chain_length - 1
            cost[i][j] = float("inf")

            for k in range(i, j):
                current_cost = (
                    cost[i][k]
                    + cost[k + 1][j]
                    + dimensions[i - 1]
                    * dimensions[k]
                    * dimensions[j]
                )

                if current_cost < cost[i][j]:
                    cost[i][j] = current_cost
                    split[i][j] = k

    def build_parenthesization(
        i: int,
        j: int,
    ) -> str:
        if i == j:
            return f"A{i}"

        k = split[i][j]

        left = build_parenthesization(
            i,
            k,
        )

        right = build_parenthesization(
            k + 1,
            j,
        )

        return f"({left}{right})"

    minimum_cost = int(
        cost[1][matrix_count]
    )

    order = build_parenthesization(
        1,
        matrix_count,
    )

    return minimum_cost, order