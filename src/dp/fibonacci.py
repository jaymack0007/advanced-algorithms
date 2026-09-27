"""Fibonacci implementations using recursion and dynamic programming."""

from typing import Dict, Optional


def _validate_n(n: int) -> None:
    """Validate Fibonacci input."""
    if not isinstance(n, int):
        raise TypeError("n must be an integer")

    if n < 0:
        raise ValueError("n must be non-negative")


def fibonacci_recursive(
    n: int,
    stats: Optional[Dict[str, int]] = None,
    depth: int = 1,
) -> int:
    """
    Calculate Fibonacci using naive recursion.

    Optional stats track recursive calls and maximum depth.
    """
    _validate_n(n)

    if stats is not None:
        stats["calls"] = stats.get("calls", 0) + 1
        stats["max_depth"] = max(
            stats.get("max_depth", 0),
            depth,
        )

    if n <= 1:
        return n

    return (
        fibonacci_recursive(
            n - 1,
            stats,
            depth + 1,
        )
        + fibonacci_recursive(
            n - 2,
            stats,
            depth + 1,
        )
    )


def fibonacci_memoized(
    n: int,
    memo: Optional[Dict[int, int]] = None,
    stats: Optional[Dict[str, int]] = None,
    depth: int = 1,
) -> int:
    """
    Calculate Fibonacci using top-down memoization.

    Optional stats track recursive calls and maximum depth.
    """
    _validate_n(n)

    if memo is None:
        memo = {}

    if stats is not None:
        stats["calls"] = stats.get("calls", 0) + 1
        stats["max_depth"] = max(
            stats.get("max_depth", 0),
            depth,
        )

    if n in memo:
        return memo[n]

    if n <= 1:
        memo[n] = n
        return n

    memo[n] = (
        fibonacci_memoized(
            n - 1,
            memo,
            stats,
            depth + 1,
        )
        + fibonacci_memoized(
            n - 2,
            memo,
            stats,
            depth + 1,
        )
    )

    return memo[n]


def fibonacci_tabulated(n: int) -> int:
    """
    Calculate Fibonacci using bottom-up tabulation.
    """
    _validate_n(n)

    if n <= 1:
        return n

    previous = 0
    current = 1

    for _ in range(2, n + 1):
        previous, current = (
            current,
            previous + current,
        )

    return current