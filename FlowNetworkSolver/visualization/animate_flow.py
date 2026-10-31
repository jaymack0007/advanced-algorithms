"""Animations for Edmonds-Karp and Push-Relabel flow algorithms."""

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.animation import (
    FuncAnimation,
    PillowWriter,
)
import networkx as nx

from FlowNetworkSolver.core.edmonds_karp import (
    EdmondsKarpResult,
)
from FlowNetworkSolver.core.network import (
    FlowNetwork,
)
from FlowNetworkSolver.core.push_relabel import (
    PushRelabelResult,
)


def _build_graph(
    network: FlowNetwork,
):
    """Create a NetworkX graph containing original edges only."""
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

    for (
        source,
        target,
        _,
        _,
        _,
    ) in network.original_edges():
        graph.add_edge(
            source,
            target,
        )

    return graph


def _save_animation(
    animation,
    output_path: Optional[str],
) -> None:
    """Save an animation when an output path is supplied."""
    if output_path is None:
        return

    path = Path(
        output_path
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if path.suffix.lower() != ".gif":
        raise ValueError(
            "animation output must use .gif"
        )

    animation.save(
        path,
        writer=PillowWriter(
            fps=1
        ),
    )


def animate_edmonds_karp(
    network: FlowNetwork,
    result: EdmondsKarpResult,
    output_path: Optional[str] = None,
    show: bool = False,
    interval: int = 1000,
):
    """
    Animate Edmonds-Karp augmenting paths.

    Each frame highlights one augmenting path and reports
    that path's bottleneck capacity.
    """
    if not isinstance(
        result,
        EdmondsKarpResult,
    ):
        raise TypeError(
            "result must be an EdmondsKarpResult"
        )

    graph = _build_graph(
        network
    )

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

    frame_count = max(
        1,
        len(
            result.augmenting_paths
        ),
    )

    def update(
        frame_index,
    ):
        axis.clear()

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
        )

        if result.augmenting_paths:
            path = result.augmenting_paths[
                frame_index
            ]

            highlighted_edges = [
                (
                    path[index],
                    path[
                        index + 1
                    ],
                )
                for index in range(
                    len(path) - 1
                )
            ]

            nx.draw_networkx_edges(
                graph,
                position,
                edgelist=highlighted_edges,
                ax=axis,
                arrows=True,
                arrowsize=24,
                width=3,
            )

            bottleneck = result.bottlenecks[
                frame_index
            ]

            axis.set_title(
                "Edmonds-Karp "
                f"augmentation {frame_index + 1} "
                f"of {len(result.augmenting_paths)} "
                f"| bottleneck={bottleneck:g}"
            )
        else:
            axis.set_title(
                "Edmonds-Karp: no augmenting path"
            )

        axis.set_axis_off()

    animation = FuncAnimation(
        figure,
        update,
        frames=frame_count,
        interval=interval,
        repeat=False,
    )

    _save_animation(
        animation,
        output_path,
    )

    if show:
        plt.show()

    if output_path is not None and not show:
        plt.close(
            figure
        )

    return animation


def animate_push_relabel(
    network: FlowNetwork,
    result: PushRelabelResult,
    output_path: Optional[str] = None,
    show: bool = False,
    interval: int = 800,
):
    """
    Animate recorded Push-Relabel events.

    Push events highlight the active directed edge.
    Relabel events highlight the vertex whose height changed.
    """
    if not isinstance(
        result,
        PushRelabelResult,
    ):
        raise TypeError(
            "result must be a PushRelabelResult"
        )

    if not result.events:
        raise ValueError(
            "Push-Relabel result contains no recorded history"
        )

    graph = _build_graph(
        network
    )

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

    def update(
        frame_index,
    ):
        axis.clear()

        event = result.events[
            frame_index
        ]

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
        )

        if event.action == "push":
            if (
                event.target is not None
                and graph.has_edge(
                    event.node,
                    event.target,
                )
            ):
                nx.draw_networkx_edges(
                    graph,
                    position,
                    edgelist=[
                        (
                            event.node,
                            event.target,
                        )
                    ],
                    ax=axis,
                    arrows=True,
                    arrowsize=24,
                    width=3,
                )

            axis.set_title(
                "Push-Relabel "
                f"event {frame_index + 1} "
                f"of {len(result.events)} "
                f"| push {event.amount:g} "
                f"from {event.node} "
                f"to {event.target}"
            )

        elif event.action == "relabel":
            nx.draw_networkx_nodes(
                graph,
                position,
                nodelist=[
                    event.node
                ],
                ax=axis,
                node_size=1600,
            )

            axis.set_title(
                "Push-Relabel "
                f"event {frame_index + 1} "
                f"of {len(result.events)} "
                f"| relabel {event.node}: "
                f"{event.old_height} -> "
                f"{event.new_height}"
            )

        axis.set_axis_off()

    animation = FuncAnimation(
        figure,
        update,
        frames=len(
            result.events
        ),
        interval=interval,
        repeat=False,
    )

    _save_animation(
        animation,
        output_path,
    )

    if show:
        plt.show()

    if output_path is not None and not show:
        plt.close(
            figure
        )

    return animation