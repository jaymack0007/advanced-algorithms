"""Compressed suffix-tree visualization utilities."""

from pathlib import Path

import matplotlib

matplotlib.use(
    "Agg"
)

import matplotlib.pyplot as plt
import networkx as nx

from StringSearchEngine.core.suffix_tree import (
    CompressedSuffixTree,
)


def tree_to_networkx(
    tree: CompressedSuffixTree,
    max_nodes: int = 60,
) -> nx.DiGraph:
    """Convert a compressed suffix tree into a NetworkX graph."""
    if not isinstance(
        tree,
        CompressedSuffixTree,
    ):
        raise TypeError(
            "tree must be a CompressedSuffixTree"
        )

    if (
        isinstance(
            max_nodes,
            bool,
        )
        or not isinstance(
            max_nodes,
            int,
        )
    ):
        raise TypeError(
            "max_nodes must be an integer"
        )

    if max_nodes <= 0:
        raise ValueError(
            "max_nodes must be positive"
        )

    graph = nx.DiGraph()

    graph.add_node(
        0,
        label="root",
    )

    records = tree.edge_records()

    for parent, child, label in records:
        if child >= max_nodes:
            break

        graph.add_node(
            child,
            label=str(
                child
            ),
        )

        graph.add_edge(
            parent,
            child,
            label=label,
        )

    return graph


def draw_suffix_tree(
    tree_or_text: CompressedSuffixTree | str,
    output_path: str | Path,
    max_nodes: int = 60,
    show: bool = False,
) -> Path:
    """
    Draw a compressed suffix tree and save it as an image.

    Long edge labels are shortened for readability.
    """
    if isinstance(
        tree_or_text,
        str,
    ):
        tree = CompressedSuffixTree(
            tree_or_text
        )

    elif isinstance(
        tree_or_text,
        CompressedSuffixTree,
    ):
        tree = tree_or_text

    else:
        raise TypeError(
            "tree_or_text must be a string or CompressedSuffixTree"
        )

    if not isinstance(
        show,
        bool,
    ):
        raise TypeError(
            "show must be boolean"
        )

    output = Path(
        output_path
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    graph = tree_to_networkx(
        tree,
        max_nodes=max_nodes,
    )

    figure = plt.figure(
        figsize=(
            12,
            8,
        )
    )

    if graph.number_of_nodes() == 1:
        positions = {
            0: (
                0,
                0,
            )
        }

    else:
        positions = nx.spring_layout(
            graph,
            seed=42,
        )

    nx.draw_networkx(
        graph,
        positions,
        with_labels=True,
        node_size=900,
        font_size=8,
        arrows=True,
    )

    edge_labels = {}

    for source, target, data in graph.edges(
        data=True
    ):
        label = data[
            "label"
        ]

        if len(
            label
        ) > 12:
            label = (
                label[
                    :9
                ]
                + "..."
            )

        edge_labels[
            (
                source,
                target,
            )
        ] = label

    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=edge_labels,
        font_size=7,
    )

    plt.title(
        "Compressed Suffix Tree"
    )

    plt.axis(
        "off"
    )

    figure.tight_layout()

    figure.savefig(
        output,
        dpi=150,
        bbox_inches="tight",
    )

    if show:
        plt.show()

    plt.close(
        figure
    )

    return output