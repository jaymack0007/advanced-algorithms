"""Tests for the FIFO Push-Relabel maximum-flow algorithm."""

import pytest

from FlowNetworkSolver.core.network import (
    FlowNetwork,
)
from FlowNetworkSolver.core.push_relabel import (
    PushRelabelResult,
    push_relabel,
)


def build_classic_network():
    """Create the standard six-node maximum-flow example."""
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        16,
    )

    network.add_edge(
        "S",
        "C",
        13,
    )

    network.add_edge(
        "A",
        "B",
        12,
    )

    network.add_edge(
        "B",
        "C",
        9,
    )

    network.add_edge(
        "C",
        "A",
        4,
    )

    network.add_edge(
        "C",
        "D",
        14,
    )

    network.add_edge(
        "D",
        "B",
        7,
    )

    network.add_edge(
        "B",
        "T",
        20,
    )

    network.add_edge(
        "D",
        "T",
        4,
    )

    return network


def test_returns_result_object():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        5,
    )

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert isinstance(
        result,
        PushRelabelResult,
    )


def test_single_edge_flow():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        5,
    )

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 5.0


def test_classic_network_max_flow():
    network = build_classic_network()

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 23.0


def test_flow_assignment_returned():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        4,
    )

    network.add_edge(
        "A",
        "T",
        4,
    )

    result = push_relabel(
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
        == 4.0
    )

    assert (
        result.flow_assignment[
            "A"
        ][
            "T"
        ]
        == 4.0
    )


def test_flow_conservation_after_solution():
    network = build_classic_network()

    push_relabel(
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
    network = build_classic_network()

    push_relabel(
        network,
        "S",
        "T",
    )

    assert (
        network.validate_capacity_constraints()
        is True
    )


def test_pushes_are_tracked():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        3,
    )

    network.add_edge(
        "A",
        "T",
        3,
    )

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert result.pushes >= 2


def test_relabels_are_tracked():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        3,
    )

    network.add_edge(
        "A",
        "T",
        3,
    )

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert result.relabels >= 1


def test_discharges_are_tracked():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        3,
    )

    network.add_edge(
        "A",
        "T",
        3,
    )

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert result.discharges >= 1


def test_source_height_initialization():
    network = build_classic_network()

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert (
        result.height_labels[
            "S"
        ]
        == len(
            network
        )
    )


def test_intermediate_excess_is_zero_at_end():
    network = build_classic_network()

    result = push_relabel(
        network,
        "S",
        "T",
    )

    for node in {
        "A",
        "B",
        "C",
        "D",
    }:
        assert result.excess[
            node
        ] == pytest.approx(
            0.0
        )


def test_sink_excess_equals_max_flow():
    network = build_classic_network()

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert result.excess[
        "T"
    ] == pytest.approx(
        result.max_flow
    )


def test_parallel_paths():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        5,
    )

    network.add_edge(
        "A",
        "T",
        5,
    )

    network.add_edge(
        "S",
        "B",
        7,
    )

    network.add_edge(
        "B",
        "T",
        7,
    )

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 12.0


def test_disconnected_sink_returns_zero():
    network = FlowNetwork()

    network.add_node(
        "S"
    )

    network.add_node(
        "T"
    )

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 0.0


def test_repeatable_with_reset():
    network = build_classic_network()

    first = push_relabel(
        network,
        "S",
        "T",
    )

    second = push_relabel(
        network,
        "S",
        "T",
    )

    assert first.max_flow == 23.0
    assert second.max_flow == 23.0


def test_history_disabled_by_default():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        3,
    )

    network.add_edge(
        "A",
        "T",
        3,
    )

    result = push_relabel(
        network,
        "S",
        "T",
    )

    assert result.events == []


def test_history_can_be_recorded():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        3,
    )

    network.add_edge(
        "A",
        "T",
        3,
    )

    result = push_relabel(
        network,
        "S",
        "T",
        record_history=True,
    )

    assert len(
        result.events
    ) > 0

    actions = {
        event.action
        for event in result.events
    }

    assert "push" in actions
    assert "relabel" in actions


def test_missing_source_rejected():
    network = FlowNetwork()

    network.add_node(
        "T"
    )

    with pytest.raises(ValueError):
        push_relabel(
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
        push_relabel(
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
        push_relabel(
            network,
            "S",
            "S",
        )


def test_invalid_network_rejected():
    with pytest.raises(TypeError):
        push_relabel(
            {},
            "S",
            "T",
        )