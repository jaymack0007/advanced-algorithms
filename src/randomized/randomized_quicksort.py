"""Randomized and deterministic QuickSort implementations."""

import random
from typing import Any, Dict, List, Optional, TypeVar


T = TypeVar("T")


def _validate_input(values: List[T]) -> None:
    """Validate QuickSort input."""
    if not isinstance(values, list):
        raise TypeError(
            "input must be a list"
        )


def _record_depth(
    stats: Optional[Dict[str, Any]],
    depth: int,
) -> None:
    """Update maximum recursion depth."""
    if stats is not None:
        stats["max_depth"] = max(
            stats.get("max_depth", 0),
            depth,
        )


def _partition(
    values: List[T],
    low: int,
    high: int,
    pivot_index: int,
    stats: Optional[Dict[str, Any]],
) -> int:
    """Partition around a selected pivot."""
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


def randomized_quicksort(
    values: List[T],
    seed: Optional[int] = None,
    stats: Optional[Dict[str, Any]] = None,
) -> List[T]:
    """
    Sort a list using Randomized QuickSort.

    A random pivot is selected during every partition.

    Expected time:
        O(n log n)

    Worst-case time:
        O(n^2)
    """
    _validate_input(values)

    result = values.copy()
    random_generator = random.Random(seed)

    if stats is not None:
        stats.clear()
        stats["comparisons"] = 0
        stats["max_depth"] = 0

    def sort(
        low: int,
        high: int,
        depth: int,
    ) -> None:
        _record_depth(
            stats,
            depth,
        )

        if low >= high:
            return

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

        sort(
            low,
            pivot_position - 1,
            depth + 1,
        )

        sort(
            pivot_position + 1,
            high,
            depth + 1,
        )

    if result:
        sort(
            0,
            len(result) - 1,
            1,
        )

    return result


def deterministic_quicksort(
    values: List[T],
    stats: Optional[Dict[str, Any]] = None,
) -> List[T]:
    """
    Sort a list using a deterministic final-element pivot.

    This function is used as a comparison baseline for
    the Week 7 randomized implementation.
    """
    _validate_input(values)

    result = values.copy()

    if stats is not None:
        stats.clear()
        stats["comparisons"] = 0
        stats["max_depth"] = 0

    def sort(
        low: int,
        high: int,
        depth: int,
    ) -> None:
        _record_depth(
            stats,
            depth,
        )

        if low >= high:
            return

        pivot_position = _partition(
            result,
            low,
            high,
            high,
            stats,
        )

        sort(
            low,
            pivot_position - 1,
            depth + 1,
        )

        sort(
            pivot_position + 1,
            high,
            depth + 1,
        )

    if result:
        sort(
            0,
            len(result) - 1,
            1,
        )

    return result