"""Tests for the Week 10 residual flow-network structure."""

import pytest

from FlowNetworkSolver.core.network import (
    Edge,
    FlowNetwork,
)


def test_empty_network():
    network = FlowNetwork()

    assert len(
        network
    ) == 0

    assert network.nodes == []


def test_add_node():
    network = FlowNetwork()

    network.add_node(
        "A"
    )

    assert network.nodes == [
        "A"
    ]


def test_add_duplicate_node_once():
    network = FlowNetwork()

    network.add_node(
        "A"
    )

    network.add_node(
        "A"
    )

    assert len(
        network
    ) == 1


def test_add_edge_creates_nodes():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        5,
    )

    assert set(
        network.nodes
    ) == {
        "S",
        "T",
    }


def test_forward_edge_properties():
    network = FlowNetwork()

    index = network.add_edge(
        "S",
        "T",
        5,
        cost=3,
    )

    edge = network.adjacency[
        "S"
    ][
        index
    ]

    assert isinstance(
        edge,
        Edge
    )

    assert edge.to == "T"
    assert edge.capacity == 5.0
    assert edge.cost == 3.0
    assert edge.flow == 0.0
    assert edge.is_residual is False
    assert edge.residual_capacity == 5.0


def test_reverse_edge_created_automatically():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        5,
        cost=3,
    )

    reverse = network.adjacency[
        "T"
    ][
        0
    ]

    assert reverse.to == "S"
    assert reverse.capacity == 0.0
    assert reverse.cost == -3.0
    assert reverse.flow == 0.0
    assert reverse.is_residual is True


def test_augment_updates_forward_and_reverse():
    network = FlowNetwork()

    index = network.add_edge(
        "S",
        "T",
        5,
    )

    network.augment(
        "S",
        index,
        3,
    )

    forward = network.adjacency[
        "S"
    ][
        index
    ]

    reverse = network.adjacency[
        "T"
    ][
        forward.reverse_index
    ]

    assert forward.flow == 3.0
    assert forward.residual_capacity == 2.0

    assert reverse.flow == -3.0
    assert reverse.residual_capacity == 3.0


def test_reverse_augmentation_cancels_flow():
    network = FlowNetwork()

    forward_index = network.add_edge(
        "S",
        "T",
        5,
    )

    network.augment(
        "S",
        forward_index,
        4,
    )

    forward = network.adjacency[
        "S"
    ][
        forward_index
    ]

    reverse_index = (
        forward.reverse_index
    )

    network.augment(
        "T",
        reverse_index,
        2,
    )

    assert (
        network.adjacency[
            "S"
        ][
            forward_index
        ].flow
        == 2.0
    )


def test_residual_graph():
    network = FlowNetwork()

    index = network.add_edge(
        "S",
        "T",
        5,
        cost=2,
    )

    network.augment(
        "S",
        index,
        3,
    )

    residual = (
        network.get_residual_graph()
    )

    assert (
        "T",
        2.0,
        2.0,
    ) in residual[
        "S"
    ]

    assert (
        "S",
        3.0,
        -2.0,
    ) in residual[
        "T"
    ]


def test_sparse_flow_assignment():
    network = FlowNetwork()

    first = network.add_edge(
        "S",
        "A",
        5,
    )

    second = network.add_edge(
        "A",
        "T",
        5,
    )

    network.augment(
        "S",
        first,
        4,
    )

    network.augment(
        "A",
        second,
        4,
    )

    assignment = (
        network.get_flow_assignment()
    )

    assert assignment[
        "S"
    ][
        "A"
    ] == 4.0

    assert assignment[
        "A"
    ][
        "T"
    ] == 4.0


def test_parallel_edges_are_combined_in_assignment():
    network = FlowNetwork()

    first = network.add_edge(
        "S",
        "T",
        3,
    )

    second = network.add_edge(
        "S",
        "T",
        4,
    )

    network.augment(
        "S",
        first,
        2,
    )

    network.augment(
        "S",
        second,
        3,
    )

    assignment = (
        network.get_flow_assignment()
    )

    assert assignment[
        "S"
    ][
        "T"
    ] == 5.0


def test_flow_value():
    network = FlowNetwork()

    first = network.add_edge(
        "S",
        "A",
        5,
    )

    second = network.add_edge(
        "A",
        "T",
        5,
    )

    network.augment(
        "S",
        first,
        4,
    )

    network.augment(
        "A",
        second,
        4,
    )

    assert network.flow_value(
        "S"
    ) == 4.0


def test_capacity_constraints():
    network = FlowNetwork()

    index = network.add_edge(
        "S",
        "T",
        5,
    )

    network.augment(
        "S",
        index,
        5,
    )

    assert (
        network.validate_capacity_constraints()
        is True
    )


def test_flow_conservation():
    network = FlowNetwork()

    first = network.add_edge(
        "S",
        "A",
        5,
    )

    second = network.add_edge(
        "A",
        "T",
        5,
    )

    network.augment(
        "S",
        first,
        3,
    )

    network.augment(
        "A",
        second,
        3,
    )

    assert (
        network.validate_flow_conservation(
            "S",
            "T",
        )
        is True
    )


def test_reset_flows():
    network = FlowNetwork()

    index = network.add_edge(
        "S",
        "T",
        5,
    )

    network.augment(
        "S",
        index,
        3,
    )

    network.reset_flows()

    assert (
        network.adjacency[
            "S"
        ][
            index
        ].flow
        == 0.0
    )

    assert (
        network.adjacency[
            "T"
        ][
            0
        ].flow
        == 0.0
    )


def test_negative_capacity_rejected():
    network = FlowNetwork()

    with pytest.raises(ValueError):
        network.add_edge(
            "S",
            "T",
            -1,
        )


def test_self_loop_rejected():
    network = FlowNetwork()

    with pytest.raises(ValueError):
        network.add_edge(
            "A",
            "A",
            5,
        )


def test_over_augmentation_rejected():
    network = FlowNetwork()

    index = network.add_edge(
        "S",
        "T",
        5,
    )

    with pytest.raises(ValueError):
        network.augment(
            "S",
            index,
            6,
        )


def test_nonpositive_augmentation_rejected():
    network = FlowNetwork()

    index = network.add_edge(
        "S",
        "T",
        5,
    )

    with pytest.raises(ValueError):
        network.augment(
            "S",
            index,
            0,
        )