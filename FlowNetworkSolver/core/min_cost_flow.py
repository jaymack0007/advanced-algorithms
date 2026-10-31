"""Successive shortest-path Min-Cost Max-Flow algorithm."""

import heapq
import math
from dataclasses import dataclass
from itertools import count
from numbers import Real
from typing import Dict, List, Optional, Tuple

from FlowNetworkSolver.core.network import (
    FlowNetwork,
    Node,
)


@dataclass
class MinCostFlowResult:
    """Results and statistics for Min-Cost Max-Flow."""

    max_flow: float
    min_cost: float
    flow_assignment: Dict[
        Node,
        Dict[
            Node,
            float,
        ],
    ]
    augmentations: int
    bottlenecks: List[float]
    path_costs: List[float]
    potentials: Dict[
        Node,
        float,
    ]


def _validate_terminals(
    network: FlowNetwork,
    source: Node,
    sink: Node,
) -> None:
    """Validate the network and terminal vertices."""
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


def _validate_flow_limit(
    flow_limit,
) -> Optional[float]:
    """Validate an optional total-flow limit."""
    if flow_limit is None:
        return None

    if (
        isinstance(
            flow_limit,
            bool,
        )
        or not isinstance(
            flow_limit,
            Real,
        )
    ):
        raise TypeError(
            "flow_limit must be numeric"
        )

    value = float(
        flow_limit
    )

    if not math.isfinite(
        value
    ):
        raise ValueError(
            "flow_limit must be finite"
        )

    if value < 0:
        raise ValueError(
            "flow_limit must be non-negative"
        )

    return value


def _initial_potentials(
    network: FlowNetwork,
    source: Node,
    tolerance: float = 1e-12,
) -> Dict[
    Node,
    float,
]:
    """
    Compute initial Johnson potentials with Bellman-Ford.

    This permits negative edge costs while rejecting a reachable
    negative-cost cycle, which would make shortest paths undefined.
    """
    nodes = list(
        network.adjacency
    )

    distance = {
        node: math.inf
        for node in nodes
    }

    distance[
        source
    ] = 0.0

    for _ in range(
        max(
            0,
            len(nodes) - 1,
        )
    ):
        changed = False

        for vertex in nodes:
            if math.isinf(
                distance[
                    vertex
                ]
            ):
                continue

            for edge in network.adjacency[
                vertex
            ]:
                if (
                    edge.residual_capacity
                    <= tolerance
                ):
                    continue

                candidate = (
                    distance[
                        vertex
                    ]
                    + edge.cost
                )

                if (
                    candidate
                    < distance[
                        edge.to
                    ]
                    - tolerance
                ):
                    distance[
                        edge.to
                    ] = candidate

                    changed = True

        if not changed:
            break

    for vertex in nodes:
        if math.isinf(
            distance[
                vertex
            ]
        ):
            continue

        for edge in network.adjacency[
            vertex
        ]:
            if (
                edge.residual_capacity
                <= tolerance
            ):
                continue

            if (
                distance[
                    vertex
                ]
                + edge.cost
                < distance[
                    edge.to
                ]
                - tolerance
            ):
                raise ValueError(
                    "reachable negative-cost cycle detected"
                )

    return {
        node: (
            0.0
            if math.isinf(
                distance[
                    node
                ]
            )
            else distance[
                node
            ]
        )
        for node in nodes
    }


def _dijkstra_with_potentials(
    network: FlowNetwork,
    source: Node,
    potentials: Dict[
        Node,
        float,
    ],
    tolerance: float = 1e-12,
) -> Tuple[
    Dict[
        Node,
        float,
    ],
    Dict[
        Node,
        Tuple[
            Node,
            int,
        ],
    ],
]:
    """Run Dijkstra using non-negative reduced edge costs."""
    distance = {
        node: math.inf
        for node in network.adjacency
    }

    parent: Dict[
        Node,
        Tuple[
            Node,
            int,
        ],
    ] = {}

    distance[
        source
    ] = 0.0

    tie_breaker = count()

    heap = [
        (
            0.0,
            next(
                tie_breaker
            ),
            source,
        )
    ]

    while heap:
        current_distance, _, vertex = (
            heapq.heappop(
                heap
            )
        )

        if (
            current_distance
            > distance[
                vertex
            ]
            + tolerance
        ):
            continue

        for edge_index, edge in enumerate(
            network.adjacency[
                vertex
            ]
        ):
            if (
                edge.residual_capacity
                <= tolerance
            ):
                continue

            reduced_cost = (
                edge.cost
                + potentials[
                    vertex
                ]
                - potentials[
                    edge.to
                ]
            )

            if (
                reduced_cost < 0
                and abs(
                    reduced_cost
                )
                <= 1e-9
            ):
                reduced_cost = 0.0

            if reduced_cost < -1e-9:
                raise RuntimeError(
                    "negative reduced cost encountered"
                )

            candidate = (
                current_distance
                + reduced_cost
            )

            if (
                candidate
                < distance[
                    edge.to
                ]
                - tolerance
            ):
                distance[
                    edge.to
                ] = candidate

                parent[
                    edge.to
                ] = (
                    vertex,
                    edge_index,
                )

                heapq.heappush(
                    heap,
                    (
                        candidate,
                        next(
                            tie_breaker
                        ),
                        edge.to,
                    ),
                )

    return (
        distance,
        parent,
    )


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
) -> List[
    Tuple[
        Node,
        int,
    ]
]:
    """Return residual edge references from source to sink."""
    path = []

    current = sink

    while current != source:
        previous, edge_index = parent[
            current
        ]

        path.append(
            (
                previous,
                edge_index,
            )
        )

        current = previous

    path.reverse()

    return path


def _current_cost(
    network: FlowNetwork,
) -> float:
    """Return cost of the current flow on original edges."""
    return sum(
        flow
        * cost
        for (
            _,
            _,
            _,
            flow,
            cost,
        ) in network.original_edges()
    )


def min_cost_max_flow(
    network: FlowNetwork,
    source: Node,
    sink: Node,
    flow_limit: Optional[float] = None,
    reset: bool = True,
) -> MinCostFlowResult:
    """
    Compute a minimum-cost maximum flow.

    Successive shortest augmenting paths are found using
    Johnson potentials and Dijkstra's algorithm.

    If flow_limit is supplied, the algorithm stops when that
    total amount of flow has been sent or no augmenting path remains.
    """
    _validate_terminals(
        network,
        source,
        sink,
    )

    limit = _validate_flow_limit(
        flow_limit
    )

    if reset:
        network.reset_flows()

    tolerance = 1e-12

    total_flow = network.flow_value(
        source
    )

    min_cost = _current_cost(
        network
    )

    potentials = _initial_potentials(
        network,
        source,
    )

    augmentations = 0

    bottlenecks: List[
        float
    ] = []

    path_costs: List[
        float
    ] = []

    while True:
        if (
            limit is not None
            and total_flow
            >= limit
            - tolerance
        ):
            break

        distance, parent = (
            _dijkstra_with_potentials(
                network,
                source,
                potentials,
            )
        )

        if math.isinf(
            distance[
                sink
            ]
        ):
            break

        for node in network.adjacency:
            if not math.isinf(
                distance[
                    node
                ]
            ):
                potentials[
                    node
                ] += distance[
                    node
                ]

        path = _reconstruct_path(
            parent,
            source,
            sink,
        )

        bottleneck = min(
            network.adjacency[
                vertex
            ][
                edge_index
            ].residual_capacity
            for vertex, edge_index in path
        )

        if limit is not None:
            bottleneck = min(
                bottleneck,
                limit
                - total_flow,
            )

        path_cost = sum(
            network.adjacency[
                vertex
            ][
                edge_index
            ].cost
            for vertex, edge_index in path
        )

        for vertex, edge_index in path:
            network.augment(
                vertex,
                edge_index,
                bottleneck,
            )

        total_flow += bottleneck

        min_cost += (
            bottleneck
            * path_cost
        )

        augmentations += 1

        bottlenecks.append(
            bottleneck
        )

        path_costs.append(
            path_cost
        )

    return MinCostFlowResult(
        max_flow=network.flow_value(
            source
        ),
        min_cost=min_cost,
        flow_assignment=(
            network.get_flow_assignment()
        ),
        augmentations=augmentations,
        bottlenecks=bottlenecks,
        path_costs=path_costs,
        potentials=potentials,
    )