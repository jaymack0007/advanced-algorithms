"""Edmonds-Karp maximum-flow algorithm."""

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from FlowNetworkSolver.core.network import (
    FlowNetwork,
    Node,
)


@dataclass
class EdmondsKarpResult:
    """Results and execution statistics for Edmonds-Karp."""

    max_flow: float
    flow_assignment: Dict[
        Node,
        Dict[
            Node,
            float,
        ],
    ]
    iterations: int
    bottlenecks: List[float]
    augmenting_paths: List[
        List[Node]
    ]
    residual_updates: int


def _validate_terminals(
    network: FlowNetwork,
    source: Node,
    sink: Node,
) -> None:
    """Validate source and sink vertices."""
    if not isinstance(
        network,
        FlowNetwork,
    ):
        raise TypeError(
            "network must be a FlowNetwork"
        )

    if source not in network.adjacency:
        raise ValueError(
            "source node does not exist"
        )

    if sink not in network.adjacency:
        raise ValueError(
            "sink node does not exist"
        )

    if source == sink:
        raise ValueError(
            "source and sink must be different"
        )


def _bfs_augmenting_path(
    network: FlowNetwork,
    source: Node,
    sink: Node,
    tolerance: float = 1e-12,
) -> Optional[
    Dict[
        Node,
        Tuple[
            Node,
            int,
        ],
    ]
]:
    """
    Find a shortest augmenting path in the residual graph.

    Returns a parent mapping:
        child -> (parent, edge_index)
    """
    parent: Dict[
        Node,
        Tuple[
            Node,
            int,
        ],
    ] = {}

    visited = {
        source
    }

    queue = deque(
        [
            source
        ]
    )

    while queue:
        current = queue.popleft()

        for edge_index, edge in enumerate(
            network.adjacency[
                current
            ]
        ):
            if (
                edge.residual_capacity
                <= tolerance
            ):
                continue

            if edge.to in visited:
                continue

            visited.add(
                edge.to
            )

            parent[
                edge.to
            ] = (
                current,
                edge_index,
            )

            if edge.to == sink:
                return parent

            queue.append(
                edge.to
            )

    return None


def _reconstruct_path(
    parent: Dict[
        Node,
        Tuple[
            Node,
            int,
        ],
    ],
    source: Node,
    sink: Node,
) -> Tuple[
    List[Node],
    List[
        Tuple[
            Node,
            int,
        ]
    ],
]:
    """Reconstruct path vertices and residual edge references."""
    vertices = [
        sink
    ]

    edges = []

    current = sink

    while current != source:
        previous, edge_index = parent[
            current
        ]

        edges.append(
            (
                previous,
                edge_index,
            )
        )

        vertices.append(
            previous
        )

        current = previous

    vertices.reverse()
    edges.reverse()

    return (
        vertices,
        edges,
    )


def edmonds_karp(
    network: FlowNetwork,
    source: Node,
    sink: Node,
    reset: bool = True,
) -> EdmondsKarpResult:
    """
    Compute maximum flow using Edmonds-Karp.

    Edmonds-Karp is the Ford-Fulkerson method with BFS used
    to select the shortest augmenting path by edge count.

    Time complexity:
        O(V * E^2)
    """
    _validate_terminals(
        network,
        source,
        sink,
    )

    if reset:
        network.reset_flows()

    iterations = 0

    bottlenecks: List[
        float
    ] = []

    augmenting_paths: List[
        List[Node]
    ] = []

    residual_updates = 0

    while True:
        parent = _bfs_augmenting_path(
            network,
            source,
            sink,
        )

        if parent is None:
            break

        path_vertices, path_edges = (
            _reconstruct_path(
                parent,
                source,
                sink,
            )
        )

        bottleneck = min(
            network.adjacency[
                vertex
            ][
                edge_index
            ].residual_capacity
            for vertex, edge_index in path_edges
        )

        for vertex, edge_index in path_edges:
            network.augment(
                vertex,
                edge_index,
                bottleneck,
            )

            residual_updates += 1

        iterations += 1

        bottlenecks.append(
            bottleneck
        )

        augmenting_paths.append(
            path_vertices
        )

    return EdmondsKarpResult(
        max_flow=network.flow_value(
            source
        ),
        flow_assignment=(
            network.get_flow_assignment()
        ),
        iterations=iterations,
        bottlenecks=bottlenecks,
        augmenting_paths=augmenting_paths,
        residual_updates=residual_updates,
    )