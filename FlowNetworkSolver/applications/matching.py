"""Bipartite matching via maximum-flow reduction."""

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

from FlowNetworkSolver.core.edmonds_karp import (
    EdmondsKarpResult,
    edmonds_karp,
)
from FlowNetworkSolver.core.network import (
    FlowNetwork,
)


Pair = Tuple[str, str]


@dataclass
class MatchingResult:
    """Store a bipartite matching solution."""

    cardinality: int
    matches: List[Pair]
    max_flow_result: EdmondsKarpResult


def _validate_partition(
    values: Sequence[str],
    name: str,
) -> List[str]:
    """Validate one bipartite partition."""
    if not isinstance(
        values,
        (list, tuple),
    ):
        raise TypeError(
            f"{name} must be a list or tuple"
        )

    result = list(
        values
    )

    if len(
        result
    ) != len(
        set(
            result
        )
    ):
        raise ValueError(
            f"{name} contains duplicate vertices"
        )

    for vertex in result:
        if not isinstance(
            vertex,
            str,
        ):
            raise TypeError(
                f"{name} vertices must be strings"
            )

    return result


def _validate_edges(
    edges: Iterable[Pair],
    left: set[str],
    right: set[str],
) -> List[Pair]:
    """Validate candidate matching edges."""
    if not isinstance(
        edges,
        (list, tuple),
    ):
        raise TypeError(
            "edges must be a list or tuple"
        )

    normalized = []
    seen = set()

    for edge in edges:
        if not isinstance(
            edge,
            tuple,
        ):
            raise TypeError(
                "each edge must be a tuple"
            )

        if len(
            edge
        ) != 2:
            raise ValueError(
                "each edge must contain two vertices"
            )

        first, second = edge

        if first not in left:
            raise ValueError(
                f"left vertex does not exist: {first}"
            )

        if second not in right:
            raise ValueError(
                f"right vertex does not exist: {second}"
            )

        if edge not in seen:
            seen.add(
                edge
            )

            normalized.append(
                edge
            )

    return normalized


def maximum_bipartite_matching(
    left_partition: Sequence[str],
    right_partition: Sequence[str],
    edges: Iterable[Pair],
) -> MatchingResult:
    """
    Compute a maximum-cardinality bipartite matching.

    Reduction:
        source -> left vertices
        left -> right candidate edges
        right -> sink

    Every edge has capacity 1.
    """
    left = _validate_partition(
        left_partition,
        "left_partition",
    )

    right = _validate_partition(
        right_partition,
        "right_partition",
    )

    if set(
        left
    ) & set(
        right
    ):
        raise ValueError(
            "left and right partitions must be disjoint"
        )

    normalized_edges = _validate_edges(
        edges,
        set(
            left
        ),
        set(
            right
        ),
    )

    source = "__source__"
    sink = "__sink__"

    existing = (
        set(
            left
        )
        | set(
            right
        )
    )

    if (
        source in existing
        or sink in existing
    ):
        raise ValueError(
            "partition vertices use reserved names"
        )

    network = FlowNetwork()

    network.add_node(
        source
    )

    network.add_node(
        sink
    )

    for vertex in left:
        network.add_edge(
            source,
            vertex,
            1,
        )

    for first, second in normalized_edges:
        network.add_edge(
            first,
            second,
            1,
        )

    for vertex in right:
        network.add_edge(
            vertex,
            sink,
            1,
        )

    result = edmonds_karp(
        network,
        source,
        sink,
    )

    matches = []

    assignment = (
        result.flow_assignment
    )

    for first, second in normalized_edges:
        if (
            assignment[
                first
            ].get(
                second,
                0.0,
            )
            > 0.5
        ):
            matches.append(
                (
                    first,
                    second,
                )
            )

    matches.sort()

    return MatchingResult(
        cardinality=len(
            matches
        ),
        matches=matches,
        max_flow_result=result,
    )