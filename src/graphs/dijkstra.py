"""Dijkstra shortest path algorithm."""

from typing import Any, Dict, Optional, Tuple

from src.structures.heap import MinHeap

from .graph import Graph


def dijkstra(
    graph: Graph,
    source: Any,
) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
    """
    Find shortest path distances from source to all nodes.

    Returns a distance dictionary and predecessor dictionary.
    """
    if source not in graph.nodes:
        raise ValueError("source node is not in the graph")

    distances = {
        node: float("inf")
        for node in graph.nodes
    }

    predecessors = {
        node: None
        for node in graph.nodes
    }

    distances[source] = 0

    queue = MinHeap()
    counter = 0
    queue.insert((0, counter, source))

    while not queue.is_empty():
        current_distance, _, current = queue.extract_min()

        if current_distance > distances[current]:
            continue

        for neighbor in graph.get_neighbors(current):
            weight = graph.get_weight(current, neighbor)

            if weight < 0:
                raise ValueError(
                    "Dijkstra's algorithm does not support negative weights"
                )

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current

                counter += 1
                queue.insert(
                    (new_distance, counter, neighbor)
                )

    return distances, predecessors

def dijkstra_list(
    graph: Graph,
    source: Any,
) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
    """
    Dijkstra using a list as the priority queue.

    This version is included for performance comparison
    with the heap-based implementation.
    """
    if source not in graph.nodes:
        raise ValueError("source node is not in the graph")

    distances = {
        node: float("inf")
        for node in graph.nodes
    }

    predecessors = {
        node: None
        for node in graph.nodes
    }

    distances[source] = 0
    queue = [(0, source)]

    while queue:
        smallest_index = min(
            range(len(queue)),
            key=lambda i: queue[i][0],
        )

        current_distance, current = queue.pop(smallest_index)

        if current_distance > distances[current]:
            continue

        for neighbor in graph.get_neighbors(current):
            weight = graph.get_weight(current, neighbor)

            if weight < 0:
                raise ValueError(
                    "Dijkstra's algorithm does not support negative weights"
                )

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current

                queue.append(
                    (new_distance, neighbor)
                )

    return distances, predecessors

def reconstruct_path(
    predecessors: Dict[Any, Optional[Any]],
    source: Any,
    target: Any,
):
    """Reconstruct a path using a predecessor dictionary."""
    path = []
    current = target

    while current is not None:
        path.append(current)

        if current == source:
            break

        current = predecessors.get(current)

    if not path or path[-1] != source:
        return []

    path.reverse()

    return path