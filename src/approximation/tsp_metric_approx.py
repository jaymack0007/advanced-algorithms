"""Metric TSP approximation using MST doubling."""

import math
from itertools import permutations
from typing import Dict, List, Set, Tuple


Point = Tuple[float, float]
Points = Dict[str, Point]
Edge = Tuple[str, str]


def _validate_points(
    points: Points,
) -> None:
    """Validate a dictionary of named 2-D points."""
    if not isinstance(
        points,
        dict,
    ):
        raise TypeError(
            "points must be a dictionary"
        )

    if not points:
        raise ValueError(
            "points must not be empty"
        )

    for name, coordinate in points.items():
        if not isinstance(
            name,
            str,
        ):
            raise TypeError(
                "point names must be strings"
            )

        if not isinstance(
            coordinate,
            tuple,
        ):
            raise TypeError(
                "coordinates must be tuples"
            )

        if len(
            coordinate
        ) != 2:
            raise ValueError(
                "coordinates must contain x and y"
            )

        x, y = coordinate

        if not isinstance(
            x,
            (int, float),
        ) or not isinstance(
            y,
            (int, float),
        ):
            raise TypeError(
                "coordinates must be numeric"
            )


def euclidean_distance(
    first: Point,
    second: Point,
) -> float:
    """Return Euclidean distance between two points."""
    return math.hypot(
        first[0] - second[0],
        first[1] - second[1],
    )


def tour_length(
    points: Points,
    tour: List[str],
) -> float:
    """Return the total distance of a closed tour."""
    _validate_points(
        points
    )

    if len(
        tour
    ) < 2:
        return 0.0

    for name in tour:
        if name not in points:
            raise ValueError(
                f"unknown point: {name}"
            )

    return sum(
        euclidean_distance(
            points[
                tour[index]
            ],
            points[
                tour[index + 1]
            ],
        )
        for index in range(
            len(tour) - 1
        )
    )


def minimum_spanning_tree(
    points: Points,
    start: str | None = None,
) -> List[Edge]:
    """
    Build a Euclidean minimum spanning tree with Prim's algorithm.

    Complexity:
        O(n^2)
    """
    _validate_points(
        points
    )

    names = sorted(
        points
    )

    if start is None:
        start = names[0]

    if start not in points:
        raise ValueError(
            "start point must exist"
        )

    if len(
        names
    ) == 1:
        return []

    visited: Set[str] = {
        start
    }

    edges: List[Edge] = []

    while len(
        visited
    ) < len(
        names
    ):
        best_edge = None
        best_key = None

        for first in sorted(
            visited
        ):
            for second in names:
                if second in visited:
                    continue

                distance = euclidean_distance(
                    points[first],
                    points[second],
                )

                key = (
                    distance,
                    first,
                    second,
                )

                if (
                    best_key is None
                    or key < best_key
                ):
                    best_key = key
                    best_edge = (
                        first,
                        second,
                    )

        if best_edge is None:
            raise RuntimeError(
                "failed to construct spanning tree"
            )

        edges.append(
            best_edge
        )

        visited.add(
            best_edge[1]
        )

    return edges


def preorder_walk(
    points: Points,
    mst_edges: List[Edge],
    start: str,
) -> List[str]:
    """
    Return a preorder traversal of the MST.

    Visiting each tree vertex once performs the shortcutting
    step used by the MST-doubling approximation.
    """
    _validate_points(
        points
    )

    if start not in points:
        raise ValueError(
            "start point must exist"
        )

    adjacency = {
        name: []
        for name in points
    }

    for first, second in mst_edges:
        if (
            first not in points
            or second not in points
        ):
            raise ValueError(
                "MST edge contains unknown point"
            )

        adjacency[
            first
        ].append(
            second
        )

        adjacency[
            second
        ].append(
            first
        )

    for neighbors in adjacency.values():
        neighbors.sort()

    order = []
    visited = set()

    def dfs(
        current: str,
    ) -> None:
        visited.add(
            current
        )

        order.append(
            current
        )

        for neighbor in adjacency[
            current
        ]:
            if neighbor not in visited:
                dfs(
                    neighbor
                )

    dfs(
        start
    )

    if len(
        visited
    ) != len(
        points
    ):
        raise ValueError(
            "MST edges do not connect all points"
        )

    return order


def mst_doubling_tsp(
    points: Points,
    start: str | None = None,
) -> Tuple[List[str], float]:
    """
    Compute a 2-approximation for metric TSP.

    The algorithm builds an MST, performs a preorder traversal,
    shortcuts repeated vertices, and returns to the start.

    For metric distances:
        cost(tour) <= 2 * OPT
    """
    _validate_points(
        points
    )

    names = sorted(
        points
    )

    if start is None:
        start = names[0]

    if start not in points:
        raise ValueError(
            "start point must exist"
        )

    if len(
        names
    ) == 1:
        return (
            [
                start,
                start,
            ],
            0.0,
        )

    mst_edges = minimum_spanning_tree(
        points,
        start=start,
    )

    order = preorder_walk(
        points,
        mst_edges,
        start,
    )

    tour = [
        *order,
        start,
    ]

    return (
        tour,
        tour_length(
            points,
            tour,
        ),
    )


def exact_metric_tsp(
    points: Points,
    start: str | None = None,
) -> Tuple[List[str], float]:
    """
    Find the optimal TSP tour by exhaustive search.

    Intended only for small benchmark instances.
    """
    _validate_points(
        points
    )

    names = sorted(
        points
    )

    if start is None:
        start = names[0]

    if start not in points:
        raise ValueError(
            "start point must exist"
        )

    remaining = [
        name
        for name in names
        if name != start
    ]

    if not remaining:
        return (
            [
                start,
                start,
            ],
            0.0,
        )

    best_tour = None
    best_cost = math.inf

    for ordering in permutations(
        remaining
    ):
        candidate = [
            start,
            *ordering,
            start,
        ]

        cost = tour_length(
            points,
            candidate,
        )

        if cost < best_cost:
            best_cost = cost
            best_tour = candidate

    if best_tour is None:
        raise RuntimeError(
            "no TSP tour found"
        )

    return (
        best_tour,
        best_cost,
    )


def approximation_ratio(
    approximate_cost: float,
    optimal_cost: float,
) -> float:
    """Return approximate tour cost divided by optimal cost."""
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