"""Tests for successive shortest-path Min-Cost Max-Flow."""

import pytest

from FlowNetworkSolver.core.min_cost_flow import (
    MinCostFlowResult,
    min_cost_max_flow,
)
from FlowNetworkSolver.core.network import (
    FlowNetwork,
)


def build_two_path_network():
    """Create two source-sink paths with different costs."""
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        2,
        cost=1,
    )

    network.add_edge(
        "A",
        "T",
        2,
        cost=1,
    )

    network.add_edge(
        "S",
        "B",
        3,
        cost=2,
    )

    network.add_edge(
        "B",
        "T",
        3,
        cost=1,
    )

    return network


def build_assignment_network():
    """Create a small weighted bipartite assignment network."""
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        1,
    )

    network.add_edge(
        "S",
        "B",
        1,
    )

    network.add_edge(
        "A",
        "X",
        1,
        cost=1,
    )

    network.add_edge(
        "A",
        "Y",
        1,
        cost=5,
    )

    network.add_edge(
        "B",
        "X",
        1,
        cost=4,
    )

    network.add_edge(
        "B",
        "Y",
        1,
        cost=1,
    )

    network.add_edge(
        "X",
        "T",
        1,
    )

    network.add_edge(
        "Y",
        "T",
        1,
    )

    return network


def test_returns_result_object():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        5,
        cost=2,
    )

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert isinstance(
        result,
        MinCostFlowResult,
    )


def test_single_edge_flow_and_cost():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        5,
        cost=2,
    )

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 5.0
    assert result.min_cost == 10.0


def test_two_path_max_flow():
    network = build_two_path_network()

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 5.0


def test_two_path_minimum_cost():
    network = build_two_path_network()

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert result.min_cost == 13.0


def test_cheapest_assignment_is_selected():
    network = build_assignment_network()

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 2.0
    assert result.min_cost == 2.0

    assert (
        result.flow_assignment[
            "A"
        ][
            "X"
        ]
        == 1.0
    )

    assert (
        result.flow_assignment[
            "B"
        ][
            "Y"
        ]
        == 1.0
    )


def test_flow_limit_uses_cheapest_path_first():
    network = build_two_path_network()

    result = min_cost_max_flow(
        network,
        "S",
        "T",
        flow_limit=2,
    )

    assert result.max_flow == 2.0
    assert result.min_cost == 4.0


def test_zero_flow_limit():
    network = build_two_path_network()

    result = min_cost_max_flow(
        network,
        "S",
        "T",
        flow_limit=0,
    )

    assert result.max_flow == 0.0
    assert result.min_cost == 0.0
    assert result.augmentations == 0


def test_negative_edge_cost_supported():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        2,
        cost=-1,
    )

    network.add_edge(
        "A",
        "T",
        2,
        cost=2,
    )

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 2.0
    assert result.min_cost == 2.0


def test_flow_assignment_returned():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        3,
        cost=1,
    )

    network.add_edge(
        "A",
        "T",
        3,
        cost=2,
    )

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert (
        result.flow_assignment[
            "S"
        ][
            "A"
        ]
        == 3.0
    )

    assert (
        result.flow_assignment[
            "A"
        ][
            "T"
        ]
        == 3.0
    )


def test_augmentations_are_tracked():
    network = build_two_path_network()

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert result.augmentations == 2


def test_bottlenecks_are_tracked():
    network = build_two_path_network()

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert result.bottlenecks == [
        2.0,
        3.0,
    ]


def test_path_costs_are_tracked():
    network = build_two_path_network()

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert result.path_costs == [
        2.0,
        3.0,
    ]


def test_flow_conservation_after_solution():
    network = build_assignment_network()

    min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert (
        network.validate_flow_conservation(
            "S",
            "T",
        )
        is True
    )


def test_capacity_constraints_after_solution():
    network = build_assignment_network()

    min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert (
        network.validate_capacity_constraints()
        is True
    )


def test_disconnected_sink_returns_zero():
    network = FlowNetwork()

    network.add_node(
        "S"
    )

    network.add_node(
        "T"
    )

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 0.0
    assert result.min_cost == 0.0


def test_zero_capacity_edge():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        0,
        cost=-5,
    )

    result = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 0.0
    assert result.min_cost == 0.0


def test_repeatable_with_reset():
    network = build_assignment_network()

    first = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    second = min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert first.max_flow == 2.0
    assert first.min_cost == 2.0

    assert second.max_flow == 2.0
    assert second.min_cost == 2.0


def test_negative_cycle_rejected():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        1,
        cost=0,
    )

    network.add_edge(
        "A",
        "B",
        1,
        cost=-2,
    )

    network.add_edge(
        "B",
        "A",
        1,
        cost=-2,
    )

    network.add_edge(
        "B",
        "T",
        1,
        cost=0,
    )

    with pytest.raises(ValueError):
        min_cost_max_flow(
            network,
            "S",
            "T",
        )


def test_missing_source_rejected():
    network = FlowNetwork()

    network.add_node(
        "T"
    )

    with pytest.raises(ValueError):
        min_cost_max_flow(
            network,
            "S",
            "T",
        )


def test_missing_sink_rejected():
    network = FlowNetwork()

    network.add_node(
        "S"
    )

    with pytest.raises(ValueError):
        min_cost_max_flow(
            network,
            "S",
            "T",
        )


def test_same_source_and_sink_rejected():
    network = FlowNetwork()

    network.add_node(
        "S"
    )

    with pytest.raises(ValueError):
        min_cost_max_flow(
            network,
            "S",
            "S",
        )


def test_negative_flow_limit_rejected():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        1,
    )

    with pytest.raises(ValueError):
        min_cost_max_flow(
            network,
            "S",
            "T",
            flow_limit=-1,
        )


def test_invalid_network_rejected():
    with pytest.raises(TypeError):
        min_cost_max_flow(
            {},
            "S",
            "T",
        )