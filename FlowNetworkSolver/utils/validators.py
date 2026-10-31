"""Validation helpers for flow-network solutions."""

from dataclasses import dataclass
import math

from FlowNetworkSolver.core.network import (
    FlowNetwork,
    Node,
)


@dataclass
class FlowValidationReport:
    """Summary of flow-network validation checks."""

    valid: bool
    capacity_valid: bool
    conservation_valid: bool
    residual_valid: bool
    source_sink_balanced: bool
    total_cost: float


def _validate_network(
    network: FlowNetwork,
) -> None:
    """Require a FlowNetwork instance."""
    if not isinstance(
        network,
        FlowNetwork,
    ):
        raise TypeError(
            "network must be a FlowNetwork"
        )


def validate_capacity_constraints(
    network: FlowNetwork,
    tolerance: float = 1e-9,
) -> bool:
    """Check 0 <= flow <= capacity on original edges."""
    _validate_network(
        network
    )

    return (
        network.validate_capacity_constraints(
            tolerance=tolerance
        )
    )


def validate_flow_conservation(
    network: FlowNetwork,
    source: Node,
    sink: Node,
    tolerance: float = 1e-9,
) -> bool:
    """Check conservation at every nonterminal vertex."""
    _validate_network(
        network
    )

    return (
        network.validate_flow_conservation(
            source,
            sink,
            tolerance=tolerance,
        )
    )


def validate_source_sink_balance(
    network: FlowNetwork,
    source: Node,
    sink: Node,
    tolerance: float = 1e-9,
) -> bool:
    """
    Check that source outflow equals sink inflow.

    FlowNetwork.flow_value() returns:
        outgoing - incoming
    so the sink should have the negative of the source value.
    """
    _validate_network(
        network
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

    source_value = network.flow_value(
        source
    )

    sink_value = network.flow_value(
        sink
    )

    return math.isclose(
        source_value,
        -sink_value,
        rel_tol=0.0,
        abs_tol=tolerance,
    )


def validate_residual_consistency(
    network: FlowNetwork,
    tolerance: float = 1e-9,
) -> bool:
    """
    Verify forward/reverse residual-edge relationships.

    Checks:
        - reverse index exists
        - reverse edge returns to the original source
        - reverse indices point back to each other
        - edge costs are negatives
        - edge flows are negatives
    """
    _validate_network(
        network
    )

    for source, edges in network.adjacency.items():
        for edge_index, edge in enumerate(
            edges
        ):
            if edge.to not in network.adjacency:
                return False

            reverse_edges = network.adjacency[
                edge.to
            ]

            if not 0 <= edge.reverse_index < len(
                reverse_edges
            ):
                return False

            reverse = reverse_edges[
                edge.reverse_index
            ]

            if reverse.to != source:
                return False

            if reverse.reverse_index != edge_index:
                return False

            if not math.isclose(
                edge.cost,
                -reverse.cost,
                rel_tol=0.0,
                abs_tol=tolerance,
            ):
                return False

            if not math.isclose(
                edge.flow,
                -reverse.flow,
                rel_tol=0.0,
                abs_tol=tolerance,
            ):
                return False

    return True


def flow_cost(
    network: FlowNetwork,
) -> float:
    """Return total cost of current flow on original edges."""
    _validate_network(
        network
    )

    return float(
        sum(
            flow * cost
            for (
                _,
                _,
                _,
                flow,
                cost,
            ) in network.original_edges()
        )
    )


def validate_min_cost_feasibility(
    network: FlowNetwork,
    source: Node,
    sink: Node,
    tolerance: float = 1e-9,
) -> bool:
    """
    Check whether the current flow is feasible for a min-cost problem.

    This validates feasibility, not optimality.
    """
    _validate_network(
        network
    )

    if not validate_capacity_constraints(
        network,
        tolerance=tolerance,
    ):
        return False

    if not validate_flow_conservation(
        network,
        source,
        sink,
        tolerance=tolerance,
    ):
        return False

    if not validate_source_sink_balance(
        network,
        source,
        sink,
        tolerance=tolerance,
    ):
        return False

    if not validate_residual_consistency(
        network,
        tolerance=tolerance,
    ):
        return False

    return math.isfinite(
        flow_cost(
            network
        )
    )


def validate_flow(
    network: FlowNetwork,
    source: Node,
    sink: Node,
    tolerance: float = 1e-9,
) -> FlowValidationReport:
    """Run all general flow validation checks."""
    _validate_network(
        network
    )

    capacity_valid = (
        validate_capacity_constraints(
            network,
            tolerance=tolerance,
        )
    )

    conservation_valid = (
        validate_flow_conservation(
            network,
            source,
            sink,
            tolerance=tolerance,
        )
    )

    residual_valid = (
        validate_residual_consistency(
            network,
            tolerance=tolerance,
        )
    )

    source_sink_balanced = (
        validate_source_sink_balance(
            network,
            source,
            sink,
            tolerance=tolerance,
        )
    )

    total_cost = flow_cost(
        network
    )

    valid = all(
        [
            capacity_valid,
            conservation_valid,
            residual_valid,
            source_sink_balanced,
            math.isfinite(
                total_cost
            ),
        ]
    )

    return FlowValidationReport(
        valid=valid,
        capacity_valid=capacity_valid,
        conservation_valid=conservation_valid,
        residual_valid=residual_valid,
        source_sink_balanced=(
            source_sink_balanced
        ),
        total_cost=total_cost,
    )