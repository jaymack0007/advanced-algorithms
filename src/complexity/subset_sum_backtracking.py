"""Exact and heuristic solutions for the Subset Sum problem."""

from typing import Dict, List, Optional


def _validate_input(
    values: List[int],
    target: int,
) -> None:
    """Validate Subset Sum input."""
    if not isinstance(values, list):
        raise TypeError(
            "values must be a list"
        )

    if not isinstance(target, int):
        raise TypeError(
            "target must be an integer"
        )

    if target < 0:
        raise ValueError(
            "target must be non-negative"
        )

    for value in values:
        if not isinstance(value, int):
            raise TypeError(
                "all values must be integers"
            )

        if value < 0:
            raise ValueError(
                "all values must be non-negative"
            )


def subset_sum_backtracking(
    values: List[int],
    target: int,
    stats: Optional[
        Dict[str, int]
    ] = None,
) -> Optional[List[int]]:
    """
    Find an exact subset whose sum equals target.

    Uses include/exclude backtracking.

    Worst-case time complexity:
        O(2^n)

    Returns:
        A matching subset, or None when no solution exists.
    """
    _validate_input(
        values,
        target,
    )

    data = values.copy()

    if stats is not None:
        stats.clear()
        stats["nodes_visited"] = 0
        stats["max_depth"] = 0

    def search(
        index: int,
        current_sum: int,
        chosen: List[int],
    ) -> Optional[List[int]]:
        if stats is not None:
            stats["nodes_visited"] += 1
            stats["max_depth"] = max(
                stats["max_depth"],
                index,
            )

        if current_sum == target:
            return chosen.copy()

        if index == len(data):
            return None

        with_current = search(
            index + 1,
            current_sum + data[index],
            chosen + [data[index]],
        )

        if with_current is not None:
            return with_current

        without_current = search(
            index + 1,
            current_sum,
            chosen,
        )

        return without_current

    return search(
        0,
        0,
        [],
    )


def greedy_subset_sum(
    values: List[int],
    target: int,
) -> Optional[List[int]]:
    """
    Try to find a subset using a descending greedy heuristic.

    The heuristic is fast but is not guaranteed to find a
    solution even when one exists.

    Approximate complexity:
        O(n log n)
    """
    _validate_input(
        values,
        target,
    )

    if target == 0:
        return []

    remaining = target

    chosen = []

    for value in sorted(
        values,
        reverse=True,
    ):
        if value <= remaining:
            chosen.append(
                value
            )

            remaining -= value

        if remaining == 0:
            return chosen

    return None


def subset_sum_is_valid(
    subset: Optional[List[int]],
    target: int,
) -> bool:
    """Return whether a returned subset reaches the target."""
    if subset is None:
        return False

    return sum(
        subset
    ) == target