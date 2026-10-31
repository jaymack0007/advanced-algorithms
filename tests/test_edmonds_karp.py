"""Tests for the Edmonds-Karp maximum-flow algorithm."""

import pytest

from FlowNetworkSolver.core.edmonds_karp import (
    EdmondsKarpResult,
    edmonds_karp,
)
from FlowNetworkSolver.core.network import (
    FlowNetwork,
)


def build_classic_network():
    """Create a standard six-node max-flow example."""
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

    result = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert isinstance(
        result,
        EdmondsKarpResult,
    )


def test_single_edge_flow():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        5,
    )

    result = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 5.0


def test_classic_network_max_flow():
    network = build_classic_network()

    result = edmonds_karp(
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

    result = edmonds_karp(
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

    edmonds_karp(
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

    edmonds_karp(
        network,
        "S",
        "T",
    )

    assert (
        network.validate_capacity_constraints()
        is True
    )


def test_iterations_are_tracked():
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

    result = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert result.iterations == 1


def test_bottleneck_is_tracked():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "A",
        10,
    )

    network.add_edge(
        "A",
        "T",
        4,
    )

    result = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert result.bottlenecks == [
        4.0
    ]


def test_augmenting_path_is_tracked():
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

    result = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert result.augmenting_paths == [
        [
            "S",
            "A",
            "T",
        ]
    ]


def test_residual_update_count():
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

    result = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert result.residual_updates == 2


def test_disconnected_sink_returns_zero():
    network = FlowNetwork()

    network.add_node(
        "S"
    )

    network.add_node(
        "T"
    )

    result = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 0.0
    assert result.iterations == 0
    assert result.bottlenecks == []
    assert result.augmenting_paths == []


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

    result = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 12.0


def test_parallel_edges():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        3,
    )

    network.add_edge(
        "S",
        "T",
        4,
    )

    result = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 7.0

    assert (
        result.flow_assignment[
            "S"
        ][
            "T"
        ]
        == 7.0
    )


def test_reset_allows_repeatable_solution():
    network = build_classic_network()

    first = edmonds_karp(
        network,
        "S",
        "T",
    )

    second = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert first.max_flow == 23.0
    assert second.max_flow == 23.0


def test_zero_capacity_edge():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        0,
    )

    result = edmonds_karp(
        network,
        "S",
        "T",
    )

    assert result.max_flow == 0.0


def test_missing_source_rejected():
    network = FlowNetwork()

    network.add_node(
        "T"
    )

    with pytest.raises(ValueError):
        edmonds_karp(
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
        edmonds_karp(
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
        edmonds_karp(
            network,
            "S",
            "S",
        )


def test_invalid_network_rejected():
    with pytest.raises(TypeError):
        edmonds_karp(
            {},
            "S",
            "T",
        )