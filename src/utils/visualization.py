"""Graph visualization utilities using NetworkX and Matplotlib."""

from pathlib import Path
from typing import Any, List, Optional

import matplotlib.pyplot as plt
import networkx as nx

from src.graphs.graph import Graph


def to_networkx(graph: Graph):
    """Convert the custom Graph object to a NetworkX graph."""
    if graph.directed:
        nx_graph = nx.DiGraph()
    else:
        nx_graph = nx.Graph()

    nx_graph.add_nodes_from(graph.nodes)

    for node in graph.nodes:
        for neighbor in graph.get_neighbors(node):
            weight = graph.get_weight(node, neighbor)

            nx_graph.add_edge(
                node,
                neighbor,
                weight=weight,
            )

    return nx_graph


def visualize_graph(
    graph: Graph,
    traversal_order: Optional[List[Any]] = None,
    title: str = "Graph",
    save_path: Optional[str] = None,
) -> None:
    """
    Visualize a graph and optionally display traversal order.

    If traversal_order is supplied, each node label includes
    its position in the traversal.
    """
    nx_graph = to_networkx(graph)

    position = nx.spring_layout(
        nx_graph,
        seed=42,
    )

    if traversal_order:
        order = {
            node: index + 1
            for index, node in enumerate(traversal_order)
        }

        labels = {
            node: f"{node}\n({order.get(node, '-')})"
            for node in graph.nodes
        }
    else:
        labels = {
            node: str(node)
            for node in graph.nodes
        }

    plt.figure(figsize=(8, 6))

    nx.draw(
        nx_graph,
        position,
        labels=labels,
        with_labels=True,
        node_size=1200,
        font_size=9,
    )

    if graph.weighted:
        edge_labels = nx.get_edge_attributes(
            nx_graph,
            "weight",
        )

        nx.draw_networkx_edge_labels(
            nx_graph,
            position,
            edge_labels=edge_labels,
        )

    plt.title(title)
    plt.tight_layout()

    if save_path:
        path = Path(save_path)
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        plt.savefig(
            path,
            bbox_inches="tight",
        )

    plt.close()