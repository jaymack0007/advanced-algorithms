"""0/1 Knapsack implementations using recursion and dynamic programming."""

from typing import Dict, List, Optional, Tuple


def _validate_inputs(
    weights: List[int],
    values: List[int],
    capacity: int,
) -> None:
    """Validate knapsack inputs."""
    if len(weights) != len(values):
        raise ValueError(
            "weights and values must have the same length"
        )

    if capacity < 0:
        raise ValueError(
            "capacity must be non-negative"
        )

    if any(weight < 0 for weight in weights):
        raise ValueError(
            "weights must be non-negative"
        )


def knapsack_recursive(
    weights: List[int],
    values: List[int],
    capacity: int,
    n: Optional[int] = None,
    stats: Optional[Dict[str, int]] = None,
    depth: int = 1,
) -> int:
    """
    Solve 0/1 Knapsack using naive recursion.

    Optional stats track recursive calls and maximum depth.
    """
    _validate_inputs(
        weights,
        values,
        capacity,
    )

    if n is None:
        n = len(weights)

    if stats is not None:
        stats["calls"] = stats.get("calls", 0) + 1
        stats["max_depth"] = max(
            stats.get("max_depth", 0),
            depth,
        )

    if n == 0 or capacity == 0:
        return 0

    current_weight = weights[n - 1]
    current_value = values[n - 1]

    if current_weight > capacity:
        return knapsack_recursive(
            weights,
            values,
            capacity,
            n - 1,
            stats,
            depth + 1,
        )

    include_item = (
        current_value
        + knapsack_recursive(
            weights,
            values,
            capacity - current_weight,
            n - 1,
            stats,
            depth + 1,
        )
    )

    exclude_item = knapsack_recursive(
        weights,
        values,
        capacity,
        n - 1,
        stats,
        depth + 1,
    )

    return max(
        include_item,
        exclude_item,
    )


def knapsack_memoized(
    weights: List[int],
    values: List[int],
    capacity: int,
    stats: Optional[Dict[str, int]] = None,
) -> int:
    """Solve 0/1 Knapsack using top-down memoization."""
    _validate_inputs(
        weights,
        values,
        capacity,
    )

    memo: Dict[Tuple[int, int], int] = {}

    def solve(
        n: int,
        remaining: int,
        depth: int,
    ) -> int:
        if stats is not None:
            stats["calls"] = stats.get("calls", 0) + 1
            stats["max_depth"] = max(
                stats.get("max_depth", 0),
                depth,
            )

        if n == 0 or remaining == 0:
            return 0

        key = (n, remaining)

        if key in memo:
            return memo[key]

        current_weight = weights[n - 1]
        current_value = values[n - 1]

        if current_weight > remaining:
            result = solve(
                n - 1,
                remaining,
                depth + 1,
            )
        else:
            include_item = (
                current_value
                + solve(
                    n - 1,
                    remaining - current_weight,
                    depth + 1,
                )
            )

            exclude_item = solve(
                n - 1,
                remaining,
                depth + 1,
            )

            result = max(
                include_item,
                exclude_item,
            )

        memo[key] = result

        return result

    return solve(
        len(weights),
        capacity,
        1,
    )


def knapsack_tabulated(
    weights: List[int],
    values: List[int],
    capacity: int,
) -> int:
    """Solve 0/1 Knapsack using bottom-up tabulation."""
    _validate_inputs(
        weights,
        values,
        capacity,
    )

    item_count = len(weights)

    table = [
        [0] * (capacity + 1)
        for _ in range(item_count + 1)
    ]

    for item in range(1, item_count + 1):
        weight = weights[item - 1]
        value = values[item - 1]

        for current_capacity in range(
            capacity + 1
        ):
            if weight > current_capacity:
                table[item][current_capacity] = (
                    table[item - 1][current_capacity]
                )
            else:
                include_item = (
                    value
                    + table[item - 1][
                        current_capacity - weight
                    ]
                )

                exclude_item = (
                    table[item - 1][current_capacity]
                )

                table[item][current_capacity] = max(
                    include_item,
                    exclude_item,
                )

    return table[item_count][capacity]


def trace_solution(
    weights: List[int],
    values: List[int],
    capacity: int,
) -> List[int]:
    """
    Reconstruct selected item indexes for an optimal solution.
    """
    _validate_inputs(
        weights,
        values,
        capacity,
    )

    item_count = len(weights)

    table = [
        [0] * (capacity + 1)
        for _ in range(item_count + 1)
    ]

    for item in range(1, item_count + 1):
        weight = weights[item - 1]
        value = values[item - 1]

        for current_capacity in range(
            capacity + 1
        ):
            if weight > current_capacity:
                table[item][current_capacity] = (
                    table[item - 1][current_capacity]
                )
            else:
                table[item][current_capacity] = max(
                    table[item - 1][current_capacity],
                    value
                    + table[item - 1][
                        current_capacity - weight
                    ],
                )

    selected = []
    remaining = capacity

    for item in range(
        item_count,
        0,
        -1,
    ):
        if (
            table[item][remaining]
            != table[item - 1][remaining]
        ):
            selected.append(item - 1)
            remaining -= weights[item - 1]

    selected.reverse()

    return selected