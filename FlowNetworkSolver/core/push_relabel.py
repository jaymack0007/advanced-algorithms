"""FIFO Push-Relabel maximum-flow algorithm."""

from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Set

from FlowNetworkSolver.core.network import (
    FlowNetwork,
    Node,
)


@dataclass
class PushRelabelEvent:
    """Optional event used later by the visualization system."""

    action: str
    node: Node
    target: Optional[Node] = None
    amount: float = 0.0
    old_height: Optional[int] = None
    new_height: Optional[int] = None
    node_excess: float = 0.0
    target_excess: Optional[float] = None


@dataclass
class PushRelabelResult:
    """Results and execution statistics for FIFO Push-Relabel."""

    max_flow: float
    flow_assignment: Dict[
        Node,
        Dict[
            Node,
            float,
        ],
    ]
    pushes: int
    relabels: int
    discharges: int
    peak_active_vertices: int
    height_labels: Dict[
        Node,
        int,
    ]
    excess: Dict[
        Node,
        float,
    ]
    events: List[
        PushRelabelEvent
    ]


def _validate_terminals(
    network: FlowNetwork,
    source: Node,
    sink: Node,
) -> None:
    """Validate the flow network, source, and sink."""
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


def push_relabel(
    network: FlowNetwork,
    source: Node,
    sink: Node,
    reset: bool = True,
    record_history: bool = False,
) -> PushRelabelResult:
    """
    Compute maximum flow using FIFO Push-Relabel.

    The implementation maintains:
        - vertex height labels
        - excess flow
        - current-edge pointers
        - a FIFO queue of active vertices

    The optional event history is disabled by default so large
    benchmark graphs do not consume unnecessary memory.
    """
    _validate_terminals(
        network,
        source,
        sink,
    )

    if reset:
        network.reset_flows()

    tolerance = 1e-12

    nodes = list(
        network.adjacency
    )

    height = {
        node: 0
        for node in nodes
    }

    excess = {
        node: 0.0
        for node in nodes
    }

    current_edge = {
        node: 0
        for node in nodes
    }

    events: List[
        PushRelabelEvent
    ] = []

    pushes = 0
    relabels = 0
    discharges = 0

    # Account for any existing flow when reset=False.
    if not reset:
        for first, edges in network.adjacency.items():
            for edge in edges:
                if edge.is_residual:
                    continue

                excess[
                    first
                ] -= edge.flow

                excess[
                    edge.to
                ] += edge.flow

    # Standard preflow initialization.
    height[
        source
    ] = len(
        nodes
    )

    active = deque()
    in_queue: Set[
        Node
    ] = set()

    for edge_index, edge in enumerate(
        network.adjacency[
            source
        ]
    ):
        if edge.is_residual:
            continue

        available = (
            edge.residual_capacity
        )

        if available <= tolerance:
            continue

        target = edge.to

        network.augment(
            source,
            edge_index,
            available,
        )

        excess[
            source
        ] -= available

        excess[
            target
        ] += available

        pushes += 1

        if record_history:
            events.append(
                PushRelabelEvent(
                    action="push",
                    node=source,
                    target=target,
                    amount=available,
                    node_excess=excess[
                        source
                    ],
                    target_excess=excess[
                        target
                    ],
                )
            )

        if (
            target != sink
            and target != source
            and excess[
                target
            ] > tolerance
            and target not in in_queue
        ):
            active.append(
                target
            )

            in_queue.add(
                target
            )

    peak_active_vertices = len(
        active
    )

    while active:
        vertex = active.popleft()

        in_queue.discard(
            vertex
        )

        discharges += 1

        while excess[
            vertex
        ] > tolerance:
            adjacency = network.adjacency[
                vertex
            ]

            if current_edge[
                vertex
            ] >= len(
                adjacency
            ):
                residual_neighbor_heights = [
                    height[
                        edge.to
                    ]
                    for edge in adjacency
                    if (
                        edge.residual_capacity
                        > tolerance
                    )
                ]

                if not residual_neighbor_heights:
                    raise RuntimeError(
                        "active vertex has no residual edge"
                    )

                old_height = height[
                    vertex
                ]

                height[
                    vertex
                ] = (
                    min(
                        residual_neighbor_heights
                    )
                    + 1
                )

                current_edge[
                    vertex
                ] = 0

                relabels += 1

                if record_history:
                    events.append(
                        PushRelabelEvent(
                            action="relabel",
                            node=vertex,
                            old_height=old_height,
                            new_height=height[
                                vertex
                            ],
                            node_excess=excess[
                                vertex
                            ],
                        )
                    )

                continue

            edge_index = current_edge[
                vertex
            ]

            edge = adjacency[
                edge_index
            ]

            admissible = (
                edge.residual_capacity
                > tolerance
                and height[
                    vertex
                ]
                == height[
                    edge.to
                ]
                + 1
            )

            if not admissible:
                current_edge[
                    vertex
                ] += 1
                continue

            target = edge.to

            amount = min(
                excess[
                    vertex
                ],
                edge.residual_capacity,
            )

            target_was_inactive = (
                excess[
                    target
                ]
                <= tolerance
            )

            network.augment(
                vertex,
                edge_index,
                amount,
            )

            excess[
                vertex
            ] -= amount

            excess[
                target
            ] += amount

            if abs(
                excess[
                    vertex
                ]
            ) <= tolerance:
                excess[
                    vertex
                ] = 0.0

            if abs(
                excess[
                    target
                ]
            ) <= tolerance:
                excess[
                    target
                ] = 0.0

            pushes += 1

            if record_history:
                events.append(
                    PushRelabelEvent(
                        action="push",
                        node=vertex,
                        target=target,
                        amount=amount,
                        node_excess=excess[
                            vertex
                        ],
                        target_excess=excess[
                            target
                        ],
                    )
                )

            if (
                target_was_inactive
                and target not in {
                    source,
                    sink,
                }
                and excess[
                    target
                ] > tolerance
                and target not in in_queue
            ):
                active.append(
                    target
                )

                in_queue.add(
                    target
                )

                peak_active_vertices = max(
                    peak_active_vertices,
                    len(
                        active
                    ),
                )

    return PushRelabelResult(
        max_flow=network.flow_value(
            source
        ),
        flow_assignment=(
            network.get_flow_assignment()
        ),
        pushes=pushes,
        relabels=relabels,
        discharges=discharges,
        peak_active_vertices=(
            peak_active_vertices
        ),
        height_labels=height,
        excess=excess,
        events=events,
    )