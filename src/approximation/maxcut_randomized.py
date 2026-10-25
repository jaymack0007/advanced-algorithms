"""Randomized approximation and local search for Max-Cut."""

import random
from dataclasses import dataclass
from itertools import product
from typing import Iterable, List, Optional, Set, Tuple


Edge = Tuple[str, str]


@dataclass
class MaxCutResult:
    """Store a Max-Cut solution."""

    left: Set[str]
    right: Set[str]
    cut_value: int
    method: str


def _validate_edges(
    edges: Iterable[Edge],
) -> List[Edge]:
    """Validate and normalize an undirected graph."""
    if not isinstance(
        edges,
        (list, tuple),
    ):
        raise TypeError(
            "edges must be a list or tuple"
        )

    normalized = []
    seen = set()

    for edge in edges:
        if not isinstance(
            edge,
            tuple,
        ):
            raise TypeError(
                "each edge must be a tuple"
            )

        if len(
            edge
        ) != 2:
            raise ValueError(
                "each edge must contain exactly two vertices"
            )

        first, second = edge

        if not isinstance(
            first,
            str,
        ) or not isinstance(
            second,
            str,
        ):
            raise TypeError(
                "vertex names must be strings"
            )

        if first == second:
            raise ValueError(
                "self-loops are not supported"
            )

        canonical = tuple(
            sorted(
                (
                    first,
                    second,
                )
            )
        )

        if canonical not in seen:
            seen.add(
                canonical
            )

            normalized.append(
                canonical
            )

    return normalized


def graph_vertices(
    edges: Iterable[Edge],
) -> List[str]:
    """Return sorted vertices appearing in the edge list."""
    normalized = _validate_edges(
        edges
    )

    return sorted(
        {
            vertex
            for edge in normalized
            for vertex in edge
        }
    )


def cut_value(
    edges: Iterable[Edge],
    left: Set[str],
) -> int:
    """Return the number of edges crossing the cut."""
    normalized = _validate_edges(
        edges
    )

    if not isinstance(
        left,
        set,
    ):
        raise TypeError(
            "left partition must be a set"
        )

    return sum(
        1
        for first, second in normalized
        if (
            first in left
        )
        != (
            second in left
        )
    )


def randomized_maxcut(
    edges: Iterable[Edge],
    seed: Optional[int] = None,
) -> MaxCutResult:
    """
    Construct a random cut.

    Each vertex independently chooses one of two sides
    with equal probability.

    Every edge is cut with probability 1/2, so the
    expected cut value is |E| / 2.
    """
    normalized = _validate_edges(
        edges
    )

    vertices = graph_vertices(
        normalized
    )

    generator = random.Random(
        seed
    )

    left = {
        vertex
        for vertex in vertices
        if generator.random() < 0.5
    }

    right = (
        set(
            vertices
        )
        - left
    )

    value = cut_value(
        normalized,
        left,
    )

    return MaxCutResult(
        left=left,
        right=right,
        cut_value=value,
        method="Randomized",
    )


def local_search_maxcut(
    edges: Iterable[Edge],
    seed: Optional[int] = None,
) -> MaxCutResult:
    """
    Improve a random cut using single-vertex local search.

    A vertex is moved to the opposite side whenever doing
    so strictly increases the cut value. Search stops at a
    local optimum.
    """
    normalized = _validate_edges(
        edges
    )

    vertices = graph_vertices(
        normalized
    )

    initial = randomized_maxcut(
        normalized,
        seed=seed,
    )

    left = set(
        initial.left
    )

    current_value = initial.cut_value

    improved = True

    while improved:
        improved = False

        for vertex in vertices:
            candidate_left = set(
                left
            )

            if vertex in candidate_left:
                candidate_left.remove(
                    vertex
                )
            else:
                candidate_left.add(
                    vertex
                )

            candidate_value = cut_value(
                normalized,
                candidate_left,
            )

            if candidate_value > current_value:
                left = candidate_left
                current_value = candidate_value
                improved = True

    return MaxCutResult(
        left=left,
        right=(
            set(
                vertices
            )
            - left
        ),
        cut_value=current_value,
        method="Local Search",
    )


def exact_maxcut(
    edges: Iterable[Edge],
) -> MaxCutResult:
    """
    Find an optimal Max-Cut by exhaustive search.

    Intended only for small benchmark instances.
    """
    normalized = _validate_edges(
        edges
    )

    vertices = graph_vertices(
        normalized
    )

    if not vertices:
        return MaxCutResult(
            left=set(),
            right=set(),
            cut_value=0,
            method="Exact Exhaustive",
        )

    first = vertices[0]

    remaining = vertices[
        1:
    ]

    best_left = {
        first
    }

    best_value = cut_value(
        normalized,
        best_left,
    )

    for choices in product(
        (
            False,
            True,
        ),
        repeat=len(
            remaining
        ),
    ):
        left = {
            first
        }

        for vertex, include in zip(
            remaining,
            choices,
        ):
            if include:
                left.add(
                    vertex
                )

        value = cut_value(
            normalized,
            left,
        )

        if value > best_value:
            best_value = value
            best_left = left

    return MaxCutResult(
        left=best_left,
        right=(
            set(
                vertices
            )
            - best_left
        ),
        cut_value=best_value,
        method="Exact Exhaustive",
    )


def approximation_ratio(
    approximate_value: int,
    optimal_value: int,
) -> float:
    """
    Return approximate value divided by optimal value.

    For maximization problems, ratios are normally between
    0 and 1 when the optimal baseline is correct.
    """
    if approximate_value < 0:
        raise ValueError(
            "approximate value must be non-negative"
        )

    if optimal_value < 0:
        raise ValueError(
            "optimal value must be non-negative"
        )

    if optimal_value == 0:
        if approximate_value == 0:
            return 1.0

        raise ValueError(
            "optimal value cannot be zero when approximate value is positive"
        )

    return (
        approximate_value
        / optimal_value
    )