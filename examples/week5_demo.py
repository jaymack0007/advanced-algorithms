"""Week 5 dynamic programming demonstration."""

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.dp.fibonacci import (
    fibonacci_memoized,
    fibonacci_recursive,
    fibonacci_tabulated,
)
from src.dp.knapsack import (
    knapsack_memoized,
    knapsack_recursive,
    knapsack_tabulated,
    trace_solution,
)
from src.dp.lcs import (
    lcs_memoized,
    lcs_recursive,
    lcs_tabulated,
    reconstruct_lcs,
)


def fibonacci_demo():
    """Demonstrate the three Fibonacci approaches."""
    n = 10

    print("Fibonacci")
    print("-" * 40)
    print(
        "Naive recursive:",
        fibonacci_recursive(n),
    )
    print(
        "Memoized:",
        fibonacci_memoized(n),
    )
    print(
        "Tabulated:",
        fibonacci_tabulated(n),
    )
    print()


def knapsack_demo():
    """Demonstrate the three Knapsack approaches."""
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50

    print("0/1 Knapsack")
    print("-" * 40)

    print(
        "Naive recursive:",
        knapsack_recursive(
            weights,
            values,
            capacity,
        ),
    )

    print(
        "Memoized:",
        knapsack_memoized(
            weights,
            values,
            capacity,
        ),
    )

    print(
        "Tabulated:",
        knapsack_tabulated(
            weights,
            values,
            capacity,
        ),
    )

    selected = trace_solution(
        weights,
        values,
        capacity,
    )

    print(
        "Selected item indexes:",
        selected,
    )
    print()


def lcs_demo():
    """Demonstrate the three LCS approaches."""
    x = "AGGTAB"
    y = "GXTXAYB"

    print("Longest Common Subsequence")
    print("-" * 40)

    print(
        "Naive recursive:",
        lcs_recursive(x, y),
    )

    print(
        "Memoized:",
        lcs_memoized(x, y),
    )

    print(
        "Tabulated:",
        lcs_tabulated(x, y),
    )

    print(
        "One LCS:",
        reconstruct_lcs(x, y),
    )
    print()


def main():
    """Run all Week 5 examples."""
    print()
    print("Week 5 Dynamic Programming Demo")
    print("=" * 40)
    print()

    fibonacci_demo()
    knapsack_demo()
    lcs_demo()


if __name__ == "__main__":
    main()