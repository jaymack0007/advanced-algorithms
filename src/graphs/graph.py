"""Graph representation using adjacency lists or adjacency matrices."""

from typing import Any, Dict, List


class Graph:
    """
    Graph supporting adjacency list and adjacency matrix representations.
    """

    def __init__(
        self,
        directed: bool = False,
        weighted: bool = False,
        representation: str = "list",
    ):
        if representation not in ("list", "matrix"):
            raise ValueError("representation must be 'list' or 'matrix'")

        self.directed = directed
        self.weighted = weighted
        self.representation = representation

        self.nodes: List[Any] = []

        if representation == "list":
            self.adjacency: Dict[Any, Dict[Any, float]] = {}
        else:
            self.index: Dict[Any, int] = {}
            self.matrix: List[bytearray] = []
            self.weights: Dict[tuple, float] = {}

    def add_node(self, node: Any) -> None:
        """Add a node to the graph."""
        if node in self.nodes:
            return

        self.nodes.append(node)

        if self.representation == "list":
            self.adjacency[node] = {}
        else:
            new_size = len(self.nodes)

            for row in self.matrix:
                row.append(0)

            self.matrix.append(bytearray(new_size))
            self.index[node] = new_size - 1

    def add_edge(
        self,
        u: Any,
        v: Any,
        weight: float = 1,
    ) -> None:
        """Add an edge between two nodes."""
        if u not in self.nodes:
            self.add_node(u)

        if v not in self.nodes:
            self.add_node(v)

        edge_weight = weight if self.weighted else 1

        if self.representation == "list":
            self.adjacency[u][v] = edge_weight

            if not self.directed:
                self.adjacency[v][u] = edge_weight

        else:
            u_index = self.index[u]
            v_index = self.index[v]

            self.matrix[u_index][v_index] = 1
            self.weights[(u, v)] = edge_weight

            if not self.directed:
                self.matrix[v_index][u_index] = 1
                self.weights[(v, u)] = edge_weight

    def remove_edge(self, u: Any, v: Any) -> None:
        """Remove an edge if it exists."""
        if u not in self.nodes or v not in self.nodes:
            return

        if self.representation == "list":
            self.adjacency[u].pop(v, None)

            if not self.directed:
                self.adjacency[v].pop(u, None)

        else:
            u_index = self.index[u]
            v_index = self.index[v]

            self.matrix[u_index][v_index] = 0
            self.weights.pop((u, v), None)

            if not self.directed:
                self.matrix[v_index][u_index] = 0
                self.weights.pop((v, u), None)

    def remove_node(self, node: Any) -> None:
        """Remove a node and all connected edges."""
        if node not in self.nodes:
            return

        if self.representation == "list":
            self.adjacency.pop(node)

            for neighbors in self.adjacency.values():
                neighbors.pop(node, None)

            self.nodes.remove(node)

        else:
            remove_index = self.index[node]

            self.matrix.pop(remove_index)

            for row in self.matrix:
                row.pop(remove_index)

            self.nodes.remove(node)

            self.weights = {
                edge: weight
                for edge, weight in self.weights.items()
                if node not in edge
            }

            self.index = {
                value: i for i, value in enumerate(self.nodes)
            }

    def get_neighbors(self, node: Any) -> List[Any]:
        """Return the neighbors of a node."""
        if node not in self.nodes:
            return []

        if self.representation == "list":
            return list(self.adjacency[node].keys())

        row = self.matrix[self.index[node]]

        return [
            self.nodes[i]
            for i, connected in enumerate(row)
            if connected
        ]

    def get_weight(self, u: Any, v: Any) -> float:
        """Return the weight of an edge."""
        if self.representation == "list":
            if u not in self.adjacency or v not in self.adjacency[u]:
                raise KeyError((u, v))

            return self.adjacency[u][v]

        if u not in self.index or v not in self.index:
            raise KeyError((u, v))

        if self.matrix[self.index[u]][self.index[v]] == 0:
            raise KeyError((u, v))

        return self.weights[(u, v)]

    def __str__(self) -> str:
        """Return a readable representation of the graph."""
        lines = []

        for node in self.nodes:
            neighbors = self.get_neighbors(node)

            if self.weighted:
                display = [
                    f"{neighbor}({self.get_weight(node, neighbor)})"
                    for neighbor in neighbors
                ]
            else:
                display = [str(neighbor) for neighbor in neighbors]

            lines.append(f"{node}: {', '.join(display)}")

        return "\n".join(lines)