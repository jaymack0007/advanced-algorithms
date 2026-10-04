"""Traveling Salesman Problem using brute force and bitmask DP."""

from itertools import permutations
from math import inf
from typing import List, Tuple


DistanceMatrix = List[List[float]]


def _validate_matrix(
    distances: DistanceMatrix,
) -> None:
    """Validate a square distance matrix."""
    if not distances:
        raise ValueError(
            "distance matrix must not be empty"
        )

    size = len(distances)

    if any(
        len(row) != size
        for row in distances
    ):
        raise ValueError(
            "distance matrix must be square"
        )

    if any(
        value < 0
        for row in distances
        for value in row
    ):
        raise ValueError(
            "distances must be non-negative"
        )


def tsp_brute_force(
    distances: DistanceMatrix,
    start: int = 0,
) -> Tuple[float, List[int]]:
    """
    Solve TSP by checking every possible tour.

    Returns the minimum cost and complete tour.
    """
    _validate_matrix(distances)

    city_count = len(distances)

    if start < 0 or start >= city_count:
        raise IndexError(
            "start city out of range"
        )

    if city_count == 1:
        return 0, [start, start]

    cities = [
        city
        for city in range(city_count)
        if city != start
    ]

    best_cost = inf
    best_tour = []

    for order in permutations(cities):
        tour = [
            start,
            *order,
            start,
        ]

        cost = 0

        for index in range(
            len(tour) - 1
        ):
            cost += distances[
                tour[index]
            ][
                tour[index + 1]
            ]

        if cost < best_cost:
            best_cost = cost
            best_tour = tour

    return best_cost, best_tour


def tsp_bitmask(
    distances: DistanceMatrix,
    start: int = 0,
) -> Tuple[float, List[int]]:
    """
    Solve TSP using dynamic programming with bitmask states.

    dp[mask][city] stores the minimum cost to start at
    the selected start city, visit all cities in mask,
    and finish at city.
    """
    _validate_matrix(distances)

    city_count = len(distances)

    if start < 0 or start >= city_count:
        raise IndexError(
            "start city out of range"
        )

    if city_count == 1:
        return 0, [start, start]

    state_count = 1 << city_count
    start_mask = 1 << start

    dp = [
        [inf] * city_count
        for _ in range(state_count)
    ]

    parent = [
        [-1] * city_count
        for _ in range(state_count)
    ]

    dp[start_mask][start] = 0

    for mask in range(state_count):
        if not (
            mask & start_mask
        ):
            continue

        for current in range(city_count):
            if not (
                mask & (1 << current)
            ):
                continue

            current_cost = dp[
                mask
            ][
                current
            ]

            if current_cost == inf:
                continue

            for next_city in range(city_count):
                next_bit = (
                    1 << next_city
                )

                if mask & next_bit:
                    continue

                next_mask = (
                    mask | next_bit
                )

                new_cost = (
                    current_cost
                    + distances[current][next_city]
                )

                if (
                    new_cost
                    < dp[next_mask][next_city]
                ):
                    dp[next_mask][next_city] = (
                        new_cost
                    )

                    parent[
                        next_mask
                    ][
                        next_city
                    ] = current

    full_mask = state_count - 1
    best_cost = inf
    last_city = -1

    for city in range(city_count):
        if city == start:
            continue

        tour_cost = (
            dp[full_mask][city]
            + distances[city][start]
        )

        if tour_cost < best_cost:
            best_cost = tour_cost
            last_city = city

    if last_city == -1:
        return inf, []

    reversed_path = []
    mask = full_mask
    current = last_city

    while current != start:
        reversed_path.append(
            current
        )

        previous = parent[
            mask
        ][
            current
        ]

        mask = (
            mask
            ^ (1 << current)
        )

        current = previous

    reversed_path.reverse()

    tour = [
        start,
        *reversed_path,
        start,
    ]

    return best_cost, tour