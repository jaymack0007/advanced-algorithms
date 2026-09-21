"""Breadth-First Search implementation."""

from collections import deque
from typing import Any, List

from .graph import Graph


def bfs(graph: Graph, start: Any) -> List[Any]:
    """
    Perform Breadth-First Search beginning at start.

    Returns the nodes in traversal order.
    """
    if start not in graph.nodes:
        return []

    visited = {start}
    queue = deque([start])
    traversal = []

    while queue:
        node = queue.popleft()
        traversal.append(node)

        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return traversal