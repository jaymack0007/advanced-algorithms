"""Approximation algorithms for the Vertex Cover problem."""

from itertools import combinations
from typing import Iterable, List, Set, Tuple


Edge = Tuple[str, str]


def _normalize_edges(
    edges: Iterable[Edge],
) -> List[Edge]:
    """Validate and normalize an edge collection."""
    normalized = []

    for edge in edges:
        if not isinstance(
            edge,
            tuple,
        ):
            raise TypeError(
                "each edge must be a tuple"
            )

        if len(edge) != 2:
            raise ValueError(
                "each edge must contain two vertices"
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

        normalized.append(
            (
                first,
                second,
            )
        )

    return normalized


def is_vertex_cover(
    edges: Iterable[Edge],
    cover: Set[str],
) -> bool:
    """Return True if every edge has an endpoint in the cover."""
    normalized = _normalize_edges(
        edges
    )

    return all(
        first in cover
        or second in cover
        for first, second in normalized
    )


def vertex_cover_2approx(
    edges: Iterable[Edge],
) -> Set[str]:
    """
    Compute the standard 2-approximation for Vertex Cover.

    Repeatedly selects an uncovered edge and adds both
    endpoints to the cover.

    The returned cover is at most twice the size of an
    optimal cover.
    """
    remaining = _normalize_edges(
        edges
    )

    cover: Set[str] = set()

    while remaining:
        first, second = remaining[0]

        cover.add(
            first
        )

        cover.add(
            second
        )

        remaining = [
            edge
            for edge in remaining
            if first not in edge
            and second not in edge
        ]

    return cover


def exact_vertex_cover(
    edges: Iterable[Edge],
) -> Set[str]:
    """
    Find a minimum Vertex Cover by exhaustive search.

    Intended only for small benchmark instances.
    """
    normalized = _normalize_edges(
        edges
    )

    if not normalized:
        return set()

    vertices = sorted(
        {
            vertex
            for edge in normalized
            for vertex in edge
        }
    )

    for size in range(
        len(vertices) + 1
    ):
        for candidate in combinations(
            vertices,
            size,
        ):
            cover = set(
                candidate
            )

            if is_vertex_cover(
                normalized,
                cover,
            ):
                return cover

    return set(
        vertices
    )


def approximation_ratio(
    approximate_cover: Set[str],
    optimal_cover: Set[str],
) -> float:
    """Return approximation size divided by optimal size."""
    if not optimal_cover:
        if not approximate_cover:
            return 1.0

        raise ValueError(
            "optimal cover cannot be empty when approximate cover is not"
        )

    return (
        len(approximate_cover)
        / len(optimal_cover)
    )