"""Linear-programming helpers for approximation algorithms."""

from dataclasses import dataclass
from typing import Dict, Mapping, Sequence, Set

import numpy as np
from scipy.optimize import linprog


@dataclass
class LPResult:
    """Store the solution to a linear-programming relaxation."""

    values: Dict[str, float]
    objective: float


def solve_set_cover_lp(
    universe: Sequence[str],
    subsets: Mapping[str, Set[str]],
    costs: Mapping[str, float],
) -> LPResult:
    """
    Solve the LP relaxation of weighted Set Cover.

    Minimize:
        sum(cost_j * x_j)

    Subject to:
        sum(x_j for sets containing element_i) >= 1

        0 <= x_j <= 1
    """
    if not universe:
        return LPResult(
            values={
                name: 0.0
                for name in subsets
            },
            objective=0.0,
        )

    names = sorted(
        subsets
    )

    objective = np.array(
        [
            float(
                costs[name]
            )
            for name in names
        ],
        dtype=float,
    )

    rows = []
    bounds_vector = []

    for element in universe:
        row = [
            -1.0
            if element in subsets[name]
            else 0.0
            for name in names
        ]

        rows.append(
            row
        )

        bounds_vector.append(
            -1.0
        )

    result = linprog(
        c=objective,
        A_ub=np.array(
            rows,
            dtype=float,
        ),
        b_ub=np.array(
            bounds_vector,
            dtype=float,
        ),
        bounds=[
            (
                0.0,
                1.0,
            )
            for _ in names
        ],
        method="highs",
    )

    if not result.success:
        raise RuntimeError(
            f"LP solver failed: {result.message}"
        )

    values = {
        name: min(
            1.0,
            max(
                0.0,
                float(
                    result.x[index]
                ),
            ),
        )
        for index, name in enumerate(
            names
        )
    }

    return LPResult(
        values=values,
        objective=float(
            result.fun
        ),
    )