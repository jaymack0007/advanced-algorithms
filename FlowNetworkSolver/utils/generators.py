"""Reproducible generators for Week 10 flow-network experiments."""

import random
from typing import List, Tuple

from FlowNetworkSolver.core.network import FlowNetwork


def generate_capacity(
    generator: random.Random,
    minimum: int = 1,
    maximum: int = 20,
) -> int:
    """Return one random integer capacity."""
    if minimum < 0:
        raise ValueError(
            "minimum capacity must be non-negative"
        )

    if maximum < minimum:
        raise ValueError(
            "maximum capacity must be >= minimum capacity"
        )

    return generator.randint(
        minimum,
        maximum,
    )


def generate_sparse_network(
    vertex_count: int,
    extra_edges: int | None = None,
    seed: int = 42,
    min_capacity: int = 1,
    max_capacity: int = 20,
    with_costs: bool = False,
) -> Tuple[
    FlowNetwork,
    int,
    int,
]:
    """
    Generate a connected sparse directed flow network.

    A source-to-sink backbone guarantees at least one path.
    Additional forward edges are added without duplicates.
    """
    if vertex_count < 2:
        raise ValueError(
            "vertex_count must be at least 2"
        )

    if extra_edges is None:
        extra_edges = vertex_count

    if extra_edges < 0:
        raise ValueError(
            "extra_edges must be non-negative"
        )

    generator = random.Random(
        seed
    )

    network = FlowNetwork()

    source = 0
    sink = vertex_count - 1

    used_edges = set()

    for vertex in range(
        vertex_count - 1
    ):
        cost = (
            generator.randint(
                0,
                10,
            )
            if with_costs
            else 0
        )

        network.add_edge(
            vertex,
            vertex + 1,
            generate_capacity(
                generator,
                min_capacity,
                max_capacity,
            ),
            cost=cost,
        )

        used_edges.add(
            (
                vertex,
                vertex + 1,
            )
        )

    possible_extra = max(
        0,
        (
            vertex_count
            * (
                vertex_count - 1
            )
            // 2
        )
        - (
            vertex_count - 1
        ),
    )

    target_extra = min(
        extra_edges,
        possible_extra,
    )

    added = 0

    while added < target_extra:
        first = generator.randrange(
            0,
            vertex_count - 1,
        )

        second = generator.randrange(
            first + 1,
            vertex_count,
        )

        edge = (
            first,
            second,
        )

        if edge in used_edges:
            continue

        cost = (
            generator.randint(
                0,
                10,
            )
            if with_costs
            else 0
        )

        network.add_edge(
            first,
            second,
            generate_capacity(
                generator,
                min_capacity,
                max_capacity,
            ),
            cost=cost,
        )

        used_edges.add(
            edge
        )

        added += 1

    return (
        network,
        source,
        sink,
    )


def generate_dense_network(
    vertex_count: int,
    edge_probability: float = 0.5,
    seed: int = 42,
    min_capacity: int = 1,
    max_capacity: int = 20,
    with_costs: bool = False,
) -> Tuple[
    FlowNetwork,
    int,
    int,
]:
    """
    Generate a reproducible dense acyclic flow network.

    Edges point from lower-numbered vertices toward
    higher-numbered vertices.
    """
    if vertex_count < 2:
        raise ValueError(
            "vertex_count must be at least 2"
        )

    if not 0.0 <= edge_probability <= 1.0:
        raise ValueError(
            "edge_probability must be between 0 and 1"
        )

    generator = random.Random(
        seed
    )

    network = FlowNetwork()

    source = 0
    sink = vertex_count - 1

    used_edges = set()

    for vertex in range(
        vertex_count - 1
    ):
        cost = (
            generator.randint(
                0,
                10,
            )
            if with_costs
            else 0
        )

        network.add_edge(
            vertex,
            vertex + 1,
            generate_capacity(
                generator,
                min_capacity,
                max_capacity,
            ),
            cost=cost,
        )

        used_edges.add(
            (
                vertex,
                vertex + 1,
            )
        )

    for first in range(
        vertex_count
    ):
        for second in range(
            first + 1,
            vertex_count,
        ):
            edge = (
                first,
                second,
            )

            if edge in used_edges:
                continue

            if (
                generator.random()
                > edge_probability
            ):
                continue

            cost = (
                generator.randint(
                    0,
                    10,
                )
                if with_costs
                else 0
            )

            network.add_edge(
                first,
                second,
                generate_capacity(
                    generator,
                    min_capacity,
                    max_capacity,
                ),
                cost=cost,
            )

            used_edges.add(
                edge
            )

    return (
        network,
        source,
        sink,
    )


def generate_bipartite_graph(
    left_count: int,
    right_count: int,
    edge_probability: float = 0.4,
    seed: int = 42,
) -> Tuple[
    List[str],
    List[str],
    List[
        Tuple[
            str,
            str,
        ]
    ],
]:
    """Generate a reproducible bipartite matching instance."""
    if left_count < 0:
        raise ValueError(
            "left_count must be non-negative"
        )

    if right_count < 0:
        raise ValueError(
            "right_count must be non-negative"
        )

    if not 0.0 <= edge_probability <= 1.0:
        raise ValueError(
            "edge_probability must be between 0 and 1"
        )

    generator = random.Random(
        seed
    )

    left = [
        f"L{index}"
        for index in range(
            left_count
        )
    ]

    right = [
        f"R{index}"
        for index in range(
            right_count
        )
    ]

    edges = []

    for first in left:
        for second in right:
            if (
                generator.random()
                <= edge_probability
            ):
                edges.append(
                    (
                        first,
                        second,
                    )
                )

    return (
        left,
        right,
        edges,
    )


def generate_grid_graph(
    rows: int,
    columns: int,
    seed: int = 42,
    min_capacity: int = 1,
    max_capacity: int = 10,
) -> FlowNetwork:
    """
    Generate a bidirectional grid-shaped flow network.

    Vertices are represented as (row, column) tuples.
    """
    if rows <= 0:
        raise ValueError(
            "rows must be positive"
        )

    if columns <= 0:
        raise ValueError(
            "columns must be positive"
        )

    generator = random.Random(
        seed
    )

    network = FlowNetwork()

    for row in range(
        rows
    ):
        for column in range(
            columns
        ):
            network.add_node(
                (
                    row,
                    column,
                )
            )

    for row in range(
        rows
    ):
        for column in range(
            columns
        ):
            current = (
                row,
                column,
            )

            if column + 1 < columns:
                right = (
                    row,
                    column + 1,
                )

                network.add_edge(
                    current,
                    right,
                    generate_capacity(
                        generator,
                        min_capacity,
                        max_capacity,
                    ),
                )

                network.add_edge(
                    right,
                    current,
                    generate_capacity(
                        generator,
                        min_capacity,
                        max_capacity,
                    ),
                )

            if row + 1 < rows:
                below = (
                    row + 1,
                    column,
                )

                network.add_edge(
                    current,
                    below,
                    generate_capacity(
                        generator,
                        min_capacity,
                        max_capacity,
                    ),
                )

                network.add_edge(
                    below,
                    current,
                    generate_capacity(
                        generator,
                        min_capacity,
                        max_capacity,
                    ),
                )

    return network


def generate_capacity_distribution(
    count: int,
    seed: int = 42,
    minimum: int = 1,
    maximum: int = 20,
) -> List[int]:
    """Generate a reproducible list of capacities."""
    if count < 0:
        raise ValueError(
            "count must be non-negative"
        )

    generator = random.Random(
        seed
    )

    return [
        generate_capacity(
            generator,
            minimum,
            maximum,
        )
        for _ in range(
            count
        )
    ]