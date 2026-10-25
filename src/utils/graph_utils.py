"""Reusable graph-generation helpers for Week 9 benchmarks."""

import math
import random
from typing import Dict, List, Tuple


Point = Tuple[float, float]
Edge = Tuple[str, str]


def generate_points(
    count: int,
    seed: int,
    prefix: str = "P",
) -> Dict[str, Point]:
    """Generate reproducible two-dimensional points."""
    if count < 0:
        raise ValueError(
            "count must be non-negative"
        )

    generator = random.Random(
        seed
    )

    return {
        f"{prefix}{index}": (
            generator.uniform(
                0.0,
                100.0,
            ),
            generator.uniform(
                0.0,
                100.0,
            ),
        )
        for index in range(
            count
        )
    }


def euclidean_distance(
    first: Point,
    second: Point,
) -> float:
    """Return Euclidean distance between two points."""
    return math.hypot(
        first[0] - second[0],
        first[1] - second[1],
    )


def cycle_edges(
    size: int,
    prefix: str = "V",
) -> List[Edge]:
    """Return the edges of a simple cycle graph."""
    if size < 3:
        raise ValueError(
            "cycle size must be at least 3"
        )

    vertices = [
        f"{prefix}{index}"
        for index in range(
            size
        )
    ]

    return [
        (
            vertices[index],
            vertices[
                (index + 1)
                % size
            ],
        )
        for index in range(
            size
        )
    ]


def random_graph_edges(
    vertex_count: int,
    edge_probability: float,
    seed: int,
    prefix: str = "V",
) -> List[Edge]:
    """
    Generate a reproducible connected undirected graph.

    A path is inserted first to guarantee connectivity, then
    additional edges are included independently.
    """
    if vertex_count < 0:
        raise ValueError(
            "vertex_count must be non-negative"
        )

    if not 0.0 <= edge_probability <= 1.0:
        raise ValueError(
            "edge_probability must be between 0 and 1"
        )

    if vertex_count < 2:
        return []

    generator = random.Random(
        seed
    )

    vertices = [
        f"{prefix}{index}"
        for index in range(
            vertex_count
        )
    ]

    edges = set()

    for index in range(
        vertex_count - 1
    ):
        edges.add(
            (
                vertices[index],
                vertices[index + 1],
            )
        )

    for first_index in range(
        vertex_count
    ):
        for second_index in range(
            first_index + 1,
            vertex_count,
        ):
            edge = (
                vertices[first_index],
                vertices[second_index],
            )

            if edge in edges:
                continue

            if generator.random() < edge_probability:
                edges.add(
                    edge
                )

    return sorted(
        edges
    )