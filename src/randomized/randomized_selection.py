"""Randomized and deterministic selection algorithms."""

import random
from typing import Any, Dict, List, Optional, TypeVar


T = TypeVar("T")


def _validate_input(
    values: List[T],
    k: int,
) -> None:
    """Validate selection input."""
    if not isinstance(values, list):
        raise TypeError(
            "input must be a list"
        )

    if not values:
        raise ValueError(
            "input list must not be empty"
        )

    if not isinstance(k, int):
        raise TypeError(
            "k must be an integer"
        )

    if k < 1 or k > len(values):
        raise ValueError(
            "k must be between 1 and the list length"
        )


def _partition(
    values: List[T],
    low: int,
    high: int,
    pivot_index: int,
    stats: Optional[Dict[str, Any]],
) -> int:
    """Partition values around a selected pivot."""
    values[pivot_index], values[high] = (
        values[high],
        values[pivot_index],
    )

    pivot = values[high]
    boundary = low

    for index in range(low, high):
        if stats is not None:
            stats["comparisons"] = (
                stats.get("comparisons", 0)
                + 1
            )

        if values[index] <= pivot:
            values[boundary], values[index] = (
                values[index],
                values[boundary],
            )
            boundary += 1

    values[boundary], values[high] = (
        values[high],
        values[boundary],
    )

    return boundary


def randomized_select(
    values: List[T],
    k: int,
    seed: Optional[int] = None,
    stats: Optional[Dict[str, Any]] = None,
) -> T:
    """
    Return the kth smallest value using randomized QuickSelect.

    k uses 1-based indexing.

    Expected time:
        O(n)

    Worst-case time:
        O(n^2)
    """
    _validate_input(
        values,
        k,
    )

    result = values.copy()
    target = k - 1
    random_generator = random.Random(seed)

    if stats is not None:
        stats.clear()
        stats["comparisons"] = 0
        stats["max_depth"] = 0

    def select(
        low: int,
        high: int,
        depth: int,
    ) -> T:
        if stats is not None:
            stats["max_depth"] = max(
                stats.get("max_depth", 0),
                depth,
            )

        if low == high:
            return result[low]

        pivot_index = random_generator.randint(
            low,
            high,
        )

        pivot_position = _partition(
            result,
            low,
            high,
            pivot_index,
            stats,
        )

        if pivot_position == target:
            return result[pivot_position]

        if target < pivot_position:
            return select(
                low,
                pivot_position - 1,
                depth + 1,
            )

        return select(
            pivot_position + 1,
            high,
            depth + 1,
        )

    return select(
        0,
        len(result) - 1,
        1,
    )


def deterministic_select(
    values: List[T],
    k: int,
    stats: Optional[Dict[str, Any]] = None,
) -> T:
    """
    Return the kth smallest value using deterministic QuickSelect.

    The final element is always selected as the pivot.
    k uses 1-based indexing.
    """
    _validate_input(
        values,
        k,
    )

    result = values.copy()
    target = k - 1

    if stats is not None:
        stats.clear()
        stats["comparisons"] = 0
        stats["max_depth"] = 0

    def select(
        low: int,
        high: int,
        depth: int,
    ) -> T:
        if stats is not None:
            stats["max_depth"] = max(
                stats.get("max_depth", 0),
                depth,
            )

        if low == high:
            return result[low]

        pivot_position = _partition(
            result,
            low,
            high,
            high,
            stats,
        )

        if pivot_position == target:
            return result[pivot_position]

        if target < pivot_position:
            return select(
                low,
                pivot_position - 1,
                depth + 1,
            )

        return select(
            pivot_position + 1,
            high,
            depth + 1,
        )

    return select(
        0,
        len(result) - 1,
        1,
    )