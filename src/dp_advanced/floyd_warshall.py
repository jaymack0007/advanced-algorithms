"""Floyd-Warshall all-pairs shortest path algorithm."""

from math import inf, isfinite
from typing import List, Optional, Tuple


Number = int | float
DistanceMatrix = List[List[Number]]
PredecessorMatrix = List[List[Optional[int]]]


def _validate_matrix(
    graph: DistanceMatrix,
) -> None:
    """Validate that the graph is a square matrix."""
    if not graph:
        raise ValueError(
            "graph must not be empty"
        )

    size = len(graph)

    if any(
        len(row) != size
        for row in graph
    ):
        raise ValueError(
            "graph must be a square matrix"
        )


def floyd_warshall(
    graph: DistanceMatrix,
) -> Tuple[
    DistanceMatrix,
    PredecessorMatrix,
]:
    """
    Compute all-pairs shortest paths.

    Missing edges should be represented by math.inf.

    Returns:
        distance matrix
        predecessor matrix
    """
    _validate_matrix(graph)

    size = len(graph)

    distance = [
        row.copy()
        for row in graph
    ]

    predecessor: PredecessorMatrix = [
        [None] * size
        for _ in range(size)
    ]

    for i in range(size):
        for j in range(size):
            if (
                i != j
                and isfinite(distance[i][j])
            ):
                predecessor[i][j] = i

    for k in range(size):
        for i in range(size):
            for j in range(size):
                through_k = (
                    distance[i][k]
                    + distance[k][j]
                )

                if through_k < distance[i][j]:
                    distance[i][j] = through_k
                    predecessor[i][j] = (
                        predecessor[k][j]
                    )

    for vertex in range(size):
        if distance[vertex][vertex] < 0:
            raise ValueError(
                "graph contains a negative cycle"
            )

    return distance, predecessor


def reconstruct_path(
    predecessor: PredecessorMatrix,
    start: int,
    end: int,
) -> List[int]:
    """
    Reconstruct a shortest path from start to end.
    """
    size = len(predecessor)

    if (
        start < 0
        or end < 0
        or start >= size
        or end >= size
    ):
        raise IndexError(
            "vertex index out of range"
        )

    if start == end:
        return [start]

    if predecessor[start][end] is None:
        return []

    path = [end]
    current = end

    while current != start:
        previous = predecessor[start][current]

        if previous is None:
            return []

        current = previous
        path.append(current)

    path.reverse()

    return path