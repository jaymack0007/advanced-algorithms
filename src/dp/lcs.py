"""Longest Common Subsequence implementations."""

from typing import Dict, Optional, Tuple


def lcs_recursive(
    x: str,
    y: str,
    stats: Optional[Dict[str, int]] = None,
) -> int:
    """
    Find LCS length using naive recursion.

    Optional stats track recursive calls and maximum depth.
    """

    def solve(
        i: int,
        j: int,
        depth: int,
    ) -> int:
        if stats is not None:
            stats["calls"] = stats.get("calls", 0) + 1
            stats["max_depth"] = max(
                stats.get("max_depth", 0),
                depth,
            )

        if i == 0 or j == 0:
            return 0

        if x[i - 1] == y[j - 1]:
            return (
                1
                + solve(
                    i - 1,
                    j - 1,
                    depth + 1,
                )
            )

        return max(
            solve(
                i - 1,
                j,
                depth + 1,
            ),
            solve(
                i,
                j - 1,
                depth + 1,
            ),
        )

    return solve(
        len(x),
        len(y),
        1,
    )


def lcs_memoized(
    x: str,
    y: str,
    stats: Optional[Dict[str, int]] = None,
) -> int:
    """
    Find LCS length using top-down memoization.

    Optional stats track recursive calls and maximum depth.
    """
    memo: Dict[Tuple[int, int], int] = {}

    def solve(
        i: int,
        j: int,
        depth: int,
    ) -> int:
        if stats is not None:
            stats["calls"] = stats.get("calls", 0) + 1
            stats["max_depth"] = max(
                stats.get("max_depth", 0),
                depth,
            )

        key = (i, j)

        if key in memo:
            return memo[key]

        if i == 0 or j == 0:
            result = 0

        elif x[i - 1] == y[j - 1]:
            result = (
                1
                + solve(
                    i - 1,
                    j - 1,
                    depth + 1,
                )
            )

        else:
            result = max(
                solve(
                    i - 1,
                    j,
                    depth + 1,
                ),
                solve(
                    i,
                    j - 1,
                    depth + 1,
                ),
            )

        memo[key] = result

        return result

    return solve(
        len(x),
        len(y),
        1,
    )


def lcs_tabulated(
    x: str,
    y: str,
) -> int:
    """
    Find LCS length using bottom-up tabulation.
    """
    rows = len(x) + 1
    columns = len(y) + 1

    table = [
        [0] * columns
        for _ in range(rows)
    ]

    for i in range(1, rows):
        for j in range(1, columns):
            if x[i - 1] == y[j - 1]:
                table[i][j] = (
                    table[i - 1][j - 1] + 1
                )
            else:
                table[i][j] = max(
                    table[i - 1][j],
                    table[i][j - 1],
                )

    return table[-1][-1]


def reconstruct_lcs(
    x: str,
    y: str,
) -> str:
    """
    Reconstruct one longest common subsequence.
    """
    rows = len(x) + 1
    columns = len(y) + 1

    table = [
        [0] * columns
        for _ in range(rows)
    ]

    for i in range(1, rows):
        for j in range(1, columns):
            if x[i - 1] == y[j - 1]:
                table[i][j] = (
                    table[i - 1][j - 1] + 1
                )
            else:
                table[i][j] = max(
                    table[i - 1][j],
                    table[i][j - 1],
                )

    i = len(x)
    j = len(y)
    sequence = []

    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            sequence.append(x[i - 1])
            i -= 1
            j -= 1

        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1

        else:
            j -= 1

    sequence.reverse()

    return "".join(sequence)