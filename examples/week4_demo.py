"""Simple demonstration of the Week 4 graph algorithms."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.graphs import (
    Graph,
    bfs,
    dfs_iterative,
    dfs_recursive,
    dijkstra,
    reconstruct_path,
)


def main():
    graph = Graph()

    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")
    graph.add_edge("C", "E")

    print("BFS:", bfs(graph, "A"))
    print("DFS iterative:", dfs_iterative(graph, "A"))
    print("DFS recursive:", dfs_recursive(graph, "A"))

    weighted_graph = Graph(
        directed=True,
        weighted=True,
    )

    weighted_graph.add_edge("A", "B", 4)
    weighted_graph.add_edge("A", "C", 2)
    weighted_graph.add_edge("C", "B", 1)
    weighted_graph.add_edge("B", "D", 5)
    weighted_graph.add_edge("C", "D", 8)

    distances, predecessors = dijkstra(
        weighted_graph,
        "A",
    )

    print("Dijkstra distances:", distances)

    path = reconstruct_path(
        predecessors,
        "A",
        "D",
    )

    print("Shortest path A to D:", path)


if __name__ == "__main__":
    main()