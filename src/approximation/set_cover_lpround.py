"""LP relaxation and rounding algorithms for weighted Set Cover."""

import math
import random
from dataclasses import dataclass
from itertools import combinations
from typing import Dict, Iterable, Mapping, Optional, Set

from src.utils.lp_solver import solve_set_cover_lp


@dataclass
class SetCoverResult:
    """Store a Set Cover solution."""

    selected_sets: Set[str]
    total_cost: float
    lp_cost: float
    method: str


def _validate_instance(
    universe: Iterable[str],
    subsets: Mapping[str, Set[str]],
    costs: Mapping[str, float],
) -> Set[str]:
    """Validate a weighted Set Cover instance."""
    if not isinstance(
        universe,
        (set, list, tuple),
    ):
        raise TypeError(
            "universe must be a set, list, or tuple"
        )

    if not isinstance(
        subsets,
        dict,
    ):
        raise TypeError(
            "subsets must be a dictionary"
        )

    if not isinstance(
        costs,
        dict,
    ):
        raise TypeError(
            "costs must be a dictionary"
        )

    universe_set = set(
        universe
    )

    for element in universe_set:
        if not isinstance(
            element,
            str,
        ):
            raise TypeError(
                "universe elements must be strings"
            )

    for name, members in subsets.items():
        if not isinstance(
            name,
            str,
        ):
            raise TypeError(
                "subset names must be strings"
            )

        if not isinstance(
            members,
            set,
        ):
            raise TypeError(
                "subset members must be stored in sets"
            )

        if name not in costs:
            raise ValueError(
                f"missing cost for subset {name}"
            )

        cost = costs[
            name
        ]

        if not isinstance(
            cost,
            (int, float),
        ):
            raise TypeError(
                "subset costs must be numeric"
            )

        if cost < 0:
            raise ValueError(
                "subset costs must be non-negative"
            )

    covered = set().union(
        *subsets.values()
    ) if subsets else set()

    if not universe_set.issubset(
        covered
    ):
        raise ValueError(
            "subsets do not cover the entire universe"
        )

    return universe_set


def is_set_cover(
    universe: Iterable[str],
    subsets: Mapping[str, Set[str]],
    selected_sets: Set[str],
) -> bool:
    """Return True when selected subsets cover the universe."""
    universe_set = set(
        universe
    )

    covered = set()

    for name in selected_sets:
        if name not in subsets:
            return False

        covered.update(
            subsets[name]
        )

    return universe_set.issubset(
        covered
    )


def _solution_cost(
    selected_sets: Set[str],
    costs: Mapping[str, float],
) -> float:
    """Return the total cost of selected subsets."""
    return float(
        sum(
            costs[name]
            for name in selected_sets
        )
    )


def _repair_cover(
    universe: Set[str],
    subsets: Mapping[str, Set[str]],
    costs: Mapping[str, float],
    selected_sets: Set[str],
) -> Set[str]:
    """
    Greedily add sets until every universe element is covered.

    Sets are selected by minimum cost per newly covered element.
    """
    selected = set(
        selected_sets
    )

    covered = set()

    for name in selected:
        covered.update(
            subsets[name]
        )

    uncovered = (
        universe
        - covered
    )

    while uncovered:
        candidates = []

        for name, members in subsets.items():
            if name in selected:
                continue

            newly_covered = (
                members
                & uncovered
            )

            if not newly_covered:
                continue

            candidates.append(
                (
                    costs[name]
                    / len(
                        newly_covered
                    ),
                    costs[name],
                    name,
                )
            )

        if not candidates:
            raise RuntimeError(
                "unable to repair Set Cover solution"
            )

        _, _, best_name = min(
            candidates
        )

        selected.add(
            best_name
        )

        uncovered -= subsets[
            best_name
        ]

    return selected


def deterministic_lp_rounding(
    universe: Iterable[str],
    subsets: Mapping[str, Set[str]],
    costs: Mapping[str, float],
) -> SetCoverResult:
    """
    Deterministically round a Set Cover LP solution.

    Sets with sufficiently large LP values are selected first.
    Any uncovered elements are then repaired greedily.
    """
    universe_set = _validate_instance(
        universe,
        subsets,
        costs,
    )

    lp = solve_set_cover_lp(
        sorted(
            universe_set
        ),
        subsets,
        costs,
    )

    if not universe_set:
        return SetCoverResult(
            selected_sets=set(),
            total_cost=0.0,
            lp_cost=0.0,
            method="Deterministic LP Rounding",
        )

    alpha = (
        math.log(
            len(
                universe_set
            )
        )
        + 1.0
    )

    threshold = (
        1.0
        / alpha
    )

    selected = {
        name
        for name, value in lp.values.items()
        if value >= threshold
    }

    selected = _repair_cover(
        universe_set,
        subsets,
        costs,
        selected,
    )

    return SetCoverResult(
        selected_sets=selected,
        total_cost=_solution_cost(
            selected,
            costs,
        ),
        lp_cost=lp.objective,
        method="Deterministic LP Rounding",
    )


def randomized_lp_rounding(
    universe: Iterable[str],
    subsets: Mapping[str, Set[str]],
    costs: Mapping[str, float],
    seed: Optional[int] = None,
) -> SetCoverResult:
    """
    Randomly round the Set Cover LP solution.

    Each set is independently selected with probability
    min(1, alpha * x_j), where alpha = ln(n) + 1.
    A greedy repair guarantees a complete final cover.
    """
    universe_set = _validate_instance(
        universe,
        subsets,
        costs,
    )

    lp = solve_set_cover_lp(
        sorted(
            universe_set
        ),
        subsets,
        costs,
    )

    if not universe_set:
        return SetCoverResult(
            selected_sets=set(),
            total_cost=0.0,
            lp_cost=0.0,
            method="Randomized LP Rounding",
        )

    alpha = (
        math.log(
            len(
                universe_set
            )
        )
        + 1.0
    )

    generator = random.Random(
        seed
    )

    selected = set()

    for name in sorted(
        subsets
    ):
        probability = min(
            1.0,
            alpha
            * lp.values[name],
        )

        if generator.random() <= probability:
            selected.add(
                name
            )

    selected = _repair_cover(
        universe_set,
        subsets,
        costs,
        selected,
    )

    return SetCoverResult(
        selected_sets=selected,
        total_cost=_solution_cost(
            selected,
            costs,
        ),
        lp_cost=lp.objective,
        method="Randomized LP Rounding",
    )


def exact_set_cover(
    universe: Iterable[str],
    subsets: Mapping[str, Set[str]],
    costs: Mapping[str, float],
) -> SetCoverResult:
    """
    Find a minimum-cost Set Cover by exhaustive search.

    Intended only for small benchmark instances.
    """
    universe_set = _validate_instance(
        universe,
        subsets,
        costs,
    )

    lp = solve_set_cover_lp(
        sorted(
            universe_set
        ),
        subsets,
        costs,
    )

    if not universe_set:
        return SetCoverResult(
            selected_sets=set(),
            total_cost=0.0,
            lp_cost=0.0,
            method="Exact Exhaustive",
        )

    names = sorted(
        subsets
    )

    best_sets = None
    best_cost = math.inf

    for size in range(
        1,
        len(names) + 1,
    ):
        for candidate in combinations(
            names,
            size,
        ):
            selected = set(
                candidate
            )

            if not is_set_cover(
                universe_set,
                subsets,
                selected,
            ):
                continue

            cost = _solution_cost(
                selected,
                costs,
            )

            if cost < best_cost:
                best_cost = cost
                best_sets = selected

    if best_sets is None:
        raise RuntimeError(
            "no Set Cover solution found"
        )

    return SetCoverResult(
        selected_sets=best_sets,
        total_cost=float(
            best_cost
        ),
        lp_cost=lp.objective,
        method="Exact Exhaustive",
    )


def approximation_ratio(
    approximate_cost: float,
    optimal_cost: float,
) -> float:
    """Return approximate Set Cover cost divided by optimal cost."""
    if approximate_cost < 0:
        raise ValueError(
            "approximate cost must be non-negative"
        )

    if optimal_cost < 0:
        raise ValueError(
            "optimal cost must be non-negative"
        )

    if optimal_cost == 0:
        if approximate_cost == 0:
            return 1.0

        raise ValueError(
            "optimal cost cannot be zero when approximate cost is positive"
        )

    return (
        approximate_cost
        / optimal_cost
    )