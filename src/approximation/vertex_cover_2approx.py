"""2-approximation and exact baseline for Vertex Cover."""

from itertools import combinations
from typing import Iterable, List, Set, Tuple


Edge = Tuple[str, str]


def _validate_edges(
    edges: Iterable[Edge],
) -> List[Edge]:
    """Validate and copy an edge collection."""
    if not isinstance(
        edges,
        (list, tuple),
    ):
        raise TypeError(
            "edges must be a list or tuple"
        )

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
    """Return True when every edge has an endpoint in the cover."""
    normalized = _validate_edges(
        edges
    )

    return all(
        first in cover
        or second in cover
        for first, second in normalized
    )


def maximal_matching(
    edges: Iterable[Edge],
) -> List[Edge]:
    """
    Build a maximal matching greedily.

    No two selected edges share an endpoint.
    """
    normalized = _validate_edges(
        edges
    )

    used_vertices: Set[str] = set()
    matching = []

    for first, second in normalized:
        if (
            first not in used_vertices
            and second not in used_vertices
        ):
            matching.append(
                (
                    first,
                    second,
                )
            )

            used_vertices.add(
                first
            )

            used_vertices.add(
                second
            )

    return matching


def vertex_cover_2approx(
    edges: Iterable[Edge],
) -> Set[str]:
    """
    Compute the standard 2-approximation for Vertex Cover.

    The algorithm constructs a maximal matching and places
    both endpoints of every selected edge into the cover.

    Because every vertex cover must contain at least one
    endpoint from each matching edge, the returned cover
    has size at most twice the optimal cover size.
    """
    matching = maximal_matching(
        edges
    )

    cover: Set[str] = set()

    for first, second in matching:
        cover.add(
            first
        )

        cover.add(
            second
        )

    return cover


def exact_vertex_cover(
    edges: Iterable[Edge],
) -> Set[str]:
    """
    Find a minimum Vertex Cover by exhaustive search.

    This function is intended only for small benchmark
    instances because its running time is exponential.
    """
    normalized = _validate_edges(
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
    """Return approximate solution size divided by optimal size."""
    if not isinstance(
        approximate_cover,
        set,
    ) or not isinstance(
        optimal_cover,
        set,
    ):
        raise TypeError(
            "covers must be sets"
        )

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