"""Core residual-network representation for flow algorithms."""

from dataclasses import dataclass
import math
from numbers import Real
from typing import Dict, Hashable, List, Tuple


Node = Hashable


@dataclass
class Edge:
    """One directed edge in a residual flow network."""

    to: Node
    reverse_index: int
    capacity: float
    cost: float = 0.0
    flow: float = 0.0
    is_residual: bool = False

    @property
    def residual_capacity(self) -> float:
        """Return unused capacity available on this residual edge."""
        return self.capacity - self.flow


class FlowNetwork:
    """
    Directed flow network using adjacency lists.

    Every forward edge automatically receives a reverse residual edge.
    Reverse edges begin with capacity zero and the negative forward cost.
    """

    def __init__(self) -> None:
        self.adjacency: Dict[
            Node,
            List[Edge],
        ] = {}

    def __len__(self) -> int:
        """Return the number of vertices."""
        return len(
            self.adjacency
        )

    @property
    def nodes(self) -> List[Node]:
        """Return network vertices in insertion order."""
        return list(
            self.adjacency
        )

    def add_node(
        self,
        node: Node,
    ) -> None:
        """Add a vertex if it is not already present."""
        try:
            hash(
                node
            )
        except TypeError as error:
            raise TypeError(
                "node must be hashable"
            ) from error

        if node not in self.adjacency:
            self.adjacency[
                node
            ] = []

    @staticmethod
    def _validate_number(
        value,
        name: str,
    ) -> float:
        """Validate a finite numeric value."""
        if (
            isinstance(
                value,
                bool,
            )
            or not isinstance(
                value,
                Real,
            )
        ):
            raise TypeError(
                f"{name} must be numeric"
            )

        result = float(
            value
        )

        if not math.isfinite(
            result
        ):
            raise ValueError(
                f"{name} must be finite"
            )

        return result

    def add_edge(
        self,
        source: Node,
        target: Node,
        capacity: float,
        cost: float = 0.0,
    ) -> int:
        """
        Add a directed edge and its automatic residual reverse edge.

        Returns the adjacency-list index of the forward edge.
        """
        if source == target:
            raise ValueError(
                "self-loops are not supported"
            )

        capacity_value = self._validate_number(
            capacity,
            "capacity",
        )

        cost_value = self._validate_number(
            cost,
            "cost",
        )

        if capacity_value < 0:
            raise ValueError(
                "capacity must be non-negative"
            )

        self.add_node(
            source
        )

        self.add_node(
            target
        )

        forward_index = len(
            self.adjacency[
                source
            ]
        )

        reverse_index = len(
            self.adjacency[
                target
            ]
        )

        forward = Edge(
            to=target,
            reverse_index=reverse_index,
            capacity=capacity_value,
            cost=cost_value,
            flow=0.0,
            is_residual=False,
        )

        reverse = Edge(
            to=source,
            reverse_index=forward_index,
            capacity=0.0,
            cost=-cost_value,
            flow=0.0,
            is_residual=True,
        )

        self.adjacency[
            source
        ].append(
            forward
        )

        self.adjacency[
            target
        ].append(
            reverse
        )

        return forward_index

    def augment(
        self,
        source: Node,
        edge_index: int,
        amount: float,
    ) -> None:
        """
        Send flow through one residual edge.

        The reverse edge is updated automatically.
        """
        if source not in self.adjacency:
            raise ValueError(
                "source node does not exist"
            )

        if (
            not isinstance(
                edge_index,
                int,
            )
            or isinstance(
                edge_index,
                bool,
            )
        ):
            raise TypeError(
                "edge_index must be an integer"
            )

        if not 0 <= edge_index < len(
            self.adjacency[
                source
            ]
        ):
            raise IndexError(
                "edge_index is out of range"
            )

        amount_value = self._validate_number(
            amount,
            "amount",
        )

        if amount_value <= 0:
            raise ValueError(
                "augmentation amount must be positive"
            )

        edge = self.adjacency[
            source
        ][
            edge_index
        ]

        tolerance = 1e-12

        if (
            amount_value
            > edge.residual_capacity
            + tolerance
        ):
            raise ValueError(
                "augmentation exceeds residual capacity"
            )

        reverse = self.adjacency[
            edge.to
        ][
            edge.reverse_index
        ]

        edge.flow += amount_value
        reverse.flow -= amount_value

    def get_residual_graph(
        self,
        tolerance: float = 1e-12,
    ) -> Dict[
        Node,
        List[
            Tuple[
                Node,
                float,
                float,
            ]
        ],
    ]:
        """
        Return positive-capacity residual edges.

        Each tuple contains:
            (target, residual_capacity, cost)
        """
        residual = {
            node: []
            for node in self.adjacency
        }

        for source, edges in self.adjacency.items():
            for edge in edges:
                available = (
                    edge.residual_capacity
                )

                if available > tolerance:
                    residual[
                        source
                    ].append(
                        (
                            edge.to,
                            available,
                            edge.cost,
                        )
                    )

        return residual

    def get_flow_assignment(
        self,
    ) -> Dict[
        Node,
        Dict[
            Node,
            float,
        ],
    ]:
        """
        Return a sparse flow-assignment matrix.

        Parallel forward edges are combined.
        Only original forward edges are represented.
        """
        assignment = {
            node: {}
            for node in self.adjacency
        }

        for source, edges in self.adjacency.items():
            for edge in edges:
                if edge.is_residual:
                    continue

                assignment[
                    source
                ][
                    edge.to
                ] = (
                    assignment[
                        source
                    ].get(
                        edge.to,
                        0.0,
                    )
                    + edge.flow
                )

        return assignment

    def original_edges(
        self,
    ) -> List[
        Tuple[
            Node,
            Node,
            float,
            float,
            float,
        ]
    ]:
        """
        Return original directed edges.

        Each tuple contains:
            (source, target, capacity, flow, cost)
        """
        result = []

        for source, edges in self.adjacency.items():
            for edge in edges:
                if not edge.is_residual:
                    result.append(
                        (
                            source,
                            edge.to,
                            edge.capacity,
                            edge.flow,
                            edge.cost,
                        )
                    )

        return result

    def flow_value(
        self,
        source: Node,
    ) -> float:
        """Return net flow leaving a vertex."""
        if source not in self.adjacency:
            raise ValueError(
                "source node does not exist"
            )

        outgoing = 0.0
        incoming = 0.0

        for first, edges in self.adjacency.items():
            for edge in edges:
                if edge.is_residual:
                    continue

                if first == source:
                    outgoing += edge.flow

                if edge.to == source:
                    incoming += edge.flow

        return (
            outgoing
            - incoming
        )

    def validate_capacity_constraints(
        self,
        tolerance: float = 1e-9,
    ) -> bool:
        """Check 0 <= flow <= capacity on every original edge."""
        for edges in self.adjacency.values():
            for edge in edges:
                if edge.is_residual:
                    continue

                if edge.flow < -tolerance:
                    return False

                if (
                    edge.flow
                    > edge.capacity
                    + tolerance
                ):
                    return False

        return True

    def validate_flow_conservation(
        self,
        source: Node,
        sink: Node,
        tolerance: float = 1e-9,
    ) -> bool:
        """Check flow conservation at every nonterminal vertex."""
        if source not in self.adjacency:
            raise ValueError(
                "source node does not exist"
            )

        if sink not in self.adjacency:
            raise ValueError(
                "sink node does not exist"
            )

        incoming = {
            node: 0.0
            for node in self.adjacency
        }

        outgoing = {
            node: 0.0
            for node in self.adjacency
        }

        for first, edges in self.adjacency.items():
            for edge in edges:
                if edge.is_residual:
                    continue

                outgoing[
                    first
                ] += edge.flow

                incoming[
                    edge.to
                ] += edge.flow

        for node in self.adjacency:
            if node in {
                source,
                sink,
            }:
                continue

            if not math.isclose(
                incoming[
                    node
                ],
                outgoing[
                    node
                ],
                rel_tol=0.0,
                abs_tol=tolerance,
            ):
                return False

        return True

    def reset_flows(
        self,
    ) -> None:
        """Reset all forward and residual flows to zero."""
        for edges in self.adjacency.values():
            for edge in edges:
                edge.flow = 0.0