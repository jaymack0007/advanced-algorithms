"""Space-optimized 0/1 Knapsack implementation."""

from typing import List


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


def space_optimized_knapsack(
    weights: List[int],
    values: List[int],
    capacity: int,
) -> int:
    """
    Solve 0/1 Knapsack using a one-dimensional DP array.

    The capacity loop runs backward so each item is used
    at most once.
    """
    _validate_inputs(
        weights,
        values,
        capacity,
    )

    dp = [0] * (capacity + 1)

    for weight, value in zip(
        weights,
        values,
    ):
        for current_capacity in range(
            capacity,
            weight - 1,
            -1,
        ):
            dp[current_capacity] = max(
                dp[current_capacity],
                value
                + dp[current_capacity - weight],
            )

    return dp[capacity]