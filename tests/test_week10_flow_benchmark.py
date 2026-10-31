"""Tests for the Week 10 flow benchmark."""

import pytest

from benchmarks.week10_flow_benchmark import (
    build_chain_network,
    count_original_edges,
    measure_solver,
    run_solver_group,
)
from FlowNetworkSolver.utils.generators import (
    generate_dense_network,
)


def test_chain_rejects_too_few_vertices():
    with pytest.raises(ValueError):
        build_chain_network(
            1
        )


def test_chain_network_size():
    network, source, sink = (
        build_chain_network(
            10
        )
    )

    assert len(
        network
    ) == 10

    assert source == 0
    assert sink == 9

    assert count_original_edges(
        network
    ) == 9


def test_chain_network_has_costs():
    network, _, _ = (
        build_chain_network(
            5,
            with_costs=True,
        )
    )

    costs = [
        cost
        for (
            _,
            _,
            _,
            _,
            cost,
        ) in network.original_edges()
    ]

    assert costs == [
        1.0,
        1.0,
        1.0,
        1.0,
    ]


def test_count_original_edges():
    network, _, _ = (
        build_chain_network(
            7
        )
    )

    assert count_original_edges(
        network
    ) == 6


def test_measure_edmonds_karp():
    row = measure_solver(
        "Edmonds-Karp",
        lambda: build_chain_network(
            8
        ),
        "test",
        "chain",
        8,
    )

    assert row[
        "max_flow"
    ] == 10

    assert row[
        "solver"
    ] == "Edmonds-Karp"


def test_measure_push_relabel():
    row = measure_solver(
        "Push-Relabel",
        lambda: build_chain_network(
            8
        ),
        "test",
        "chain",
        8,
    )

    assert row[
        "max_flow"
    ] == 10

    assert row[
        "solver"
    ] == "Push-Relabel"


def test_measure_min_cost_flow():
    row = measure_solver(
        "Min-Cost Max-Flow",
        lambda: build_chain_network(
            8
        ),
        "test",
        "chain",
        8,
    )

    assert row[
        "max_flow"
    ] == 10

    assert row[
        "min_cost"
    ] == 70


def test_solver_group_has_equal_max_flow():
    def factory(
        _solver_name,
    ):
        return lambda: build_chain_network(
            12
        )

    rows = run_solver_group(
        factory,
        "test",
        "chain",
        12,
    )

    flows = {
        row[
            "max_flow"
        ]
        for row in rows
    }

    assert flows == {
        10
    }


def test_dense_solver_group_has_equal_max_flow():
    def factory(
        _solver_name,
    ):
        return lambda: generate_dense_network(
            12,
            edge_probability=0.4,
            seed=1234,
            with_costs=True,
        )

    rows = run_solver_group(
        factory,
        "test",
        "dense",
        12,
    )

    flows = {
        row[
            "max_flow"
        ]
        for row in rows
    }

    assert len(
        flows
    ) == 1


def test_unknown_solver_rejected():
    with pytest.raises(ValueError):
        measure_solver(
            "Unknown",
            lambda: build_chain_network(
                5
            ),
            "test",
            "chain",
            5,
        )