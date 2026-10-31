"""Static visualization for flow networks."""

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import networkx as nx

from FlowNetworkSolver.core.network import (
    FlowNetwork,
)


def plot_flow_network(
    network: FlowNetwork,
    title: str = "Flow Network",
    output_path: Optional[str] = None,
    show: bool = False,
):
    """
    Draw a flow network using NetworkX and Matplotlib.

    Original edges are labeled as:
        flow / capacity

    When a nonzero cost exists, the label also includes cost.
    """
    if not isinstance(
        network,
        FlowNetwork,
    ):
        raise TypeError(
            "network must be a FlowNetwork"
        )

    graph = nx.DiGraph()

    for node in network.nodes:
        graph.add_node(
            node
        )

    edge_labels = {}

    for (
        source,
        target,
        capacity,
        flow,
        cost,
    ) in network.original_edges():
        graph.add_edge(
            source,
            target,
        )

        label = (
            f"{flow:g}/{capacity:g}"
        )

        if cost != 0:
            label += (
                f"\ncost={cost:g}"
            )

        edge_labels[
            (
                source,
                target,
            )
        ] = label

    position = nx.spring_layout(
        graph,
        seed=42,
    )

    figure, axis = plt.subplots(
        figsize=(
            9,
            6,
        )
    )

    nx.draw_networkx_nodes(
        graph,
        position,
        ax=axis,
        node_size=1200,
    )

    nx.draw_networkx_labels(
        graph,
        position,
        ax=axis,
    )

    nx.draw_networkx_edges(
        graph,
        position,
        ax=axis,
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0.05",
    )

    nx.draw_networkx_edge_labels(
        graph,
        position,
        edge_labels=edge_labels,
        ax=axis,
        font_size=8,
    )

    axis.set_title(
        title
    )

    axis.set_axis_off()

    figure.tight_layout()

    if output_path is not None:
        path = Path(
            output_path
        )

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        figure.savefig(
            path,
            bbox_inches="tight",
        )

    if show:
        plt.show()

    return figure