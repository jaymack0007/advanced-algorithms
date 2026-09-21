"""Utilities for generating graphs used in Week 4 benchmarks."""

import random

from src.graphs.graph import Graph


def generate_sparse_graph(
    node_count: int,
    directed: bool = False,
    seed: int = 42,
) -> Graph:
    """
    Generate a sparse connected graph.

    Each node is connected to the next node, with a small
    number of additional random edges.
    """
    random.seed(seed)

    graph = Graph(directed=directed)

    for node in range(node_count):
        graph.add_node(node)

    for node in range(node_count - 1):
        graph.add_edge(node, node + 1)

    extra_edges = node_count // 2

    for _ in range(extra_edges):
        u = random.randrange(node_count)
        v = random.randrange(node_count)

        if u != v:
            graph.add_edge(u, v)

    return graph


def generate_dense_graph(
    node_count: int,
    directed: bool = False,
    density: float = 0.25,
    seed: int = 42,
) -> Graph:
    """
    Generate a dense graph using a probability for each edge.
    """
    random.seed(seed)

    graph = Graph(directed=directed)

    for node in range(node_count):
        graph.add_node(node)

    for u in range(node_count):
        for v in range(u + 1, node_count):
            if random.random() < density:
                graph.add_edge(u, v)

                if directed and random.random() < 0.5:
                    graph.add_edge(v, u)

    return graph


def generate_random_graph(
    node_count: int,
    edge_probability: float = 0.05,
    directed: bool = False,
    seed: int = 42,
) -> Graph:
    """
    Generate a random graph.
    """
    random.seed(seed)

    graph = Graph(directed=directed)

    for node in range(node_count):
        graph.add_node(node)

    for u in range(node_count):
        for v in range(u + 1, node_count):
            if random.random() < edge_probability:
                graph.add_edge(u, v)

    return graph


def generate_weighted_graph(
    node_count: int,
    edge_probability: float = 0.05,
    directed: bool = True,
    seed: int = 42,
) -> Graph:
    """
    Generate a weighted graph with positive edge weights.
    """
    random.seed(seed)

    graph = Graph(
        directed=directed,
        weighted=True,
    )

    for node in range(node_count):
        graph.add_node(node)

    # Create a basic path so nodes are reachable.
    for node in range(node_count - 1):
        weight = random.randint(1, 10)
        graph.add_edge(node, node + 1, weight)

    for u in range(node_count):
        for v in range(node_count):
            if u != v and random.random() < edge_probability:
                weight = random.randint(1, 10)
                graph.add_edge(u, v, weight)

    return graph