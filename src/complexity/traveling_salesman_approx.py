"""Nearest-neighbor and exact solvers for small TSP instances."""

import math
from itertools import permutations
from typing import Dict, List, Tuple


Point = Tuple[float, float]
Points = Dict[str, Point]


def _validate_points(
    points: Points,
) -> None:
    """Validate a mapping of city names to coordinates."""
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

    for city, coordinate in points.items():
        if not isinstance(
            city,
            str,
        ):
            raise TypeError(
                "city names must be strings"
            )

        if not isinstance(
            coordinate,
            tuple,
        ):
            raise TypeError(
                "coordinates must be tuples"
            )

        if len(coordinate) != 2:
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
    """Return the total length of a closed TSP tour."""
    _validate_points(
        points
    )

    if len(tour) < 2:
        return 0.0

    for city in tour:
        if city not in points:
            raise ValueError(
                f"unknown city: {city}"
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


def nearest_neighbor_tsp(
    points: Points,
    start: str | None = None,
) -> Tuple[List[str], float]:
    """
    Build a TSP tour with the nearest-neighbor heuristic.

    Complexity:
        O(n^2)
    """
    _validate_points(
        points
    )

    cities = sorted(
        points
    )

    if start is None:
        start = cities[0]

    if start not in points:
        raise ValueError(
            "start city must exist in points"
        )

    unvisited = set(
        cities
    )

    unvisited.remove(
        start
    )

    tour = [
        start
    ]

    current = start

    while unvisited:
        next_city = min(
            unvisited,
            key=lambda city: (
                euclidean_distance(
                    points[current],
                    points[city],
                ),
                city,
            ),
        )

        tour.append(
            next_city
        )

        unvisited.remove(
            next_city
        )

        current = next_city

    tour.append(
        start
    )

    return (
        tour,
        tour_length(
            points,
            tour,
        ),
    )


def exact_tsp(
    points: Points,
    start: str | None = None,
) -> Tuple[List[str], float]:
    """
    Find an optimal TSP tour by exhaustive search.

    Intended only for small benchmark instances.
    """
    _validate_points(
        points
    )

    cities = sorted(
        points
    )

    if start is None:
        start = cities[0]

    if start not in points:
        raise ValueError(
            "start city must exist in points"
        )

    remaining = [
        city
        for city in cities
        if city != start
    ]

    best_tour = None
    best_length = math.inf

    for ordering in permutations(
        remaining
    ):
        candidate = [
            start,
            *ordering,
            start,
        ]

        candidate_length = tour_length(
            points,
            candidate,
        )

        if candidate_length < best_length:
            best_length = candidate_length
            best_tour = candidate

    if best_tour is None:
        best_tour = [
            start,
            start,
        ]

        best_length = 0.0

    return (
        best_tour,
        best_length,
    )


def approximation_ratio(
    approximate_length: float,
    optimal_length: float,
) -> float:
    """Return heuristic tour length divided by optimal tour length."""
    if approximate_length < 0:
        raise ValueError(
            "approximate length must be non-negative"
        )

    if optimal_length < 0:
        raise ValueError(
            "optimal length must be non-negative"
        )

    if optimal_length == 0:
        if approximate_length == 0:
            return 1.0

        raise ValueError(
            "optimal length cannot be zero when approximate length is positive"
        )

    return (
        approximate_length
        / optimal_length
    )