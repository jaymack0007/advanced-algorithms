"""Tests for flow validation and network-generation helpers."""

import pytest

from FlowNetworkSolver.core.edmonds_karp import (
    edmonds_karp,
)
from FlowNetworkSolver.core.min_cost_flow import (
    min_cost_max_flow,
)
from FlowNetworkSolver.core.network import (
    FlowNetwork,
)
from FlowNetworkSolver.utils.generators import (
    generate_bipartite_graph,
    generate_capacity_distribution,
    generate_dense_network,
    generate_grid_graph,
    generate_sparse_network,
)
from FlowNetworkSolver.utils.validators import (
    FlowValidationReport,
    flow_cost,
    validate_capacity_constraints,
    validate_flow,
    validate_flow_conservation,
    validate_min_cost_feasibility,
    validate_residual_consistency,
    validate_source_sink_balance,
)


def build_valid_flow():
    """Create and solve a small valid flow network."""
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

    edmonds_karp(
        network,
        "S",
        "T",
    )

    return network


def test_capacity_constraints_valid():
    network = build_valid_flow()

    assert (
        validate_capacity_constraints(
            network
        )
        is True
    )


def test_capacity_above_limit_invalid():
    network = FlowNetwork()

    index = network.add_edge(
        "S",
        "T",
        5,
    )

    network.adjacency[
        "S"
    ][
        index
    ].flow = 6.0

    assert (
        validate_capacity_constraints(
            network
        )
        is False
    )


def test_negative_forward_flow_invalid():
    network = FlowNetwork()

    index = network.add_edge(
        "S",
        "T",
        5,
    )

    network.adjacency[
        "S"
    ][
        index
    ].flow = -1.0

    assert (
        validate_capacity_constraints(
            network
        )
        is False
    )


def test_flow_conservation_valid():
    network = build_valid_flow()

    assert (
        validate_flow_conservation(
            network,
            "S",
            "T",
        )
        is True
    )


def test_flow_conservation_invalid():
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
        5,
    )

    network.augment(
        "A",
        second,
        3,
    )

    assert (
        validate_flow_conservation(
            network,
            "S",
            "T",
        )
        is False
    )


def test_source_sink_balance_valid():
    network = build_valid_flow()

    assert (
        validate_source_sink_balance(
            network,
            "S",
            "T",
        )
        is True
    )


def test_source_sink_balance_invalid():
    network = FlowNetwork()

    first = network.add_edge(
        "S",
        "A",
        5,
    )

    network.add_edge(
        "A",
        "T",
        5,
    )

    network.augment(
        "S",
        first,
        4,
    )

    assert (
        validate_source_sink_balance(
            network,
            "S",
            "T",
        )
        is False
    )


def test_residual_consistency_valid():
    network = build_valid_flow()

    assert (
        validate_residual_consistency(
            network
        )
        is True
    )


def test_bad_reverse_index_invalid():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        5,
    )

    network.adjacency[
        "S"
    ][
        0
    ].reverse_index = 99

    assert (
        validate_residual_consistency(
            network
        )
        is False
    )


def test_bad_reverse_target_invalid():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        5,
    )

    network.adjacency[
        "T"
    ][
        0
    ].to = "X"

    assert (
        validate_residual_consistency(
            network
        )
        is False
    )


def test_bad_reverse_flow_invalid():
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

    network.adjacency[
        "T"
    ][
        0
    ].flow = -2.0

    assert (
        validate_residual_consistency(
            network
        )
        is False
    )


def test_bad_reverse_cost_invalid():
    network = FlowNetwork()

    network.add_edge(
        "S",
        "T",
        5,
        cost=4,
    )

    network.adjacency[
        "T"
    ][
        0
    ].cost = -3.0

    assert (
        validate_residual_consistency(
            network
        )
        is False
    )


def test_flow_cost():
    network = FlowNetwork()

    first = network.add_edge(
        "S",
        "A",
        3,
        cost=2,
    )

    second = network.add_edge(
        "A",
        "T",
        3,
        cost=4,
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

    assert flow_cost(
        network
    ) == 18.0


def test_min_cost_feasibility_valid():
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
        cost=2,
    )

    min_cost_max_flow(
        network,
        "S",
        "T",
    )

    assert (
        validate_min_cost_feasibility(
            network,
            "S",
            "T",
        )
        is True
    )


def test_min_cost_feasibility_invalid_capacity():
    network = build_valid_flow()

    network.adjacency[
        "S"
    ][
        0
    ].flow = 10.0

    assert (
        validate_min_cost_feasibility(
            network,
            "S",
            "T",
        )
        is False
    )


def test_full_validation_report():
    network = build_valid_flow()

    report = validate_flow(
        network,
        "S",
        "T",
    )

    assert isinstance(
        report,
        FlowValidationReport,
    )

    assert report.valid is True
    assert report.capacity_valid is True
    assert report.conservation_valid is True
    assert report.residual_valid is True
    assert report.source_sink_balanced is True
    assert report.total_cost == 0.0


def test_invalid_network_rejected():
    with pytest.raises(TypeError):
        validate_capacity_constraints(
            {}
        )


def test_missing_source_rejected():
    network = FlowNetwork()

    network.add_node(
        "T"
    )

    with pytest.raises(ValueError):
        validate_source_sink_balance(
            network,
            "S",
            "T",
        )


def test_sparse_generator_is_reproducible():
    first, first_source, first_sink = (
        generate_sparse_network(
            8,
            extra_edges=5,
            seed=99,
        )
    )

    second, second_source, second_sink = (
        generate_sparse_network(
            8,
            extra_edges=5,
            seed=99,
        )
    )

    assert (
        first.original_edges()
        == second.original_edges()
    )

    assert first_source == second_source
    assert first_sink == second_sink


def test_sparse_generator_has_source_sink_path():
    network, source, sink = (
        generate_sparse_network(
            10,
            extra_edges=0,
            seed=1,
        )
    )

    assert source == 0
    assert sink == 9

    residual = (
        network.get_residual_graph()
    )

    assert any(
        target == 1
        for (
            target,
            _,
            _,
        ) in residual[
            source
        ]
    )


def test_dense_generator_reproducible():
    first, _, _ = generate_dense_network(
        7,
        edge_probability=0.7,
        seed=12,
    )

    second, _, _ = generate_dense_network(
        7,
        edge_probability=0.7,
        seed=12,
    )

    assert (
        first.original_edges()
        == second.original_edges()
    )


def test_bipartite_generator_reproducible():
    first = generate_bipartite_graph(
        4,
        5,
        edge_probability=0.5,
        seed=7,
    )

    second = generate_bipartite_graph(
        4,
        5,
        edge_probability=0.5,
        seed=7,
    )

    assert first == second


def test_grid_generator_node_count():
    network = generate_grid_graph(
        3,
        4,
        seed=5,
    )

    assert len(
        network
    ) == 12


def test_capacity_distribution_reproducible():
    first = generate_capacity_distribution(
        10,
        seed=20,
    )

    second = generate_capacity_distribution(
        10,
        seed=20,
    )

    assert first == second


def test_capacity_distribution_bounds():
    values = generate_capacity_distribution(
        100,
        seed=20,
        minimum=5,
        maximum=9,
    )

    assert all(
        5 <= value <= 9
        for value in values
    )


def test_invalid_sparse_vertex_count():
    with pytest.raises(ValueError):
        generate_sparse_network(
            1
        )


def test_invalid_dense_probability():
    with pytest.raises(ValueError):
        generate_dense_network(
            5,
            edge_probability=2.0,
        )


def test_invalid_grid_size():
    with pytest.raises(ValueError):
        generate_grid_graph(
            0,
            5,
        )