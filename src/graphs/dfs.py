"""Depth-First Search implementations."""

from typing import Any, List, Set

from .graph import Graph


def dfs_iterative(graph: Graph, start: Any) -> List[Any]:
    """
    Perform iterative Depth-First Search beginning at start.

    Returns the nodes in traversal order.
    """
    if start not in graph.nodes:
        return []

    visited = set()
    stack = [start]
    traversal = []

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        traversal.append(node)

        neighbors = graph.get_neighbors(node)

        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                stack.append(neighbor)

    return traversal


def dfs_recursive(graph: Graph, start: Any) -> List[Any]:
    """
    Perform recursive Depth-First Search beginning at start.

    Returns the nodes in traversal order.
    """
    if start not in graph.nodes:
        return []

    visited: Set[Any] = set()
    traversal: List[Any] = []

    def visit(node: Any) -> None:
        visited.add(node)
        traversal.append(node)

        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                visit(neighbor)

    visit(start)

    return traversal