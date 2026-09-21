"""Week 4 graph performance benchmarks."""

import gc
import sys
import time
import tracemalloc
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.graphs.bfs import bfs
from src.graphs.dfs import dfs_iterative
from src.graphs.dijkstra import dijkstra, dijkstra_list
from src.graphs.graph import Graph
from src.utils.graph_generator import (
    generate_dense_graph,
    generate_sparse_graph,
    generate_weighted_graph,
)


RESULTS_DIR = PROJECT_ROOT / "benchmarks" / "results"

REPRESENTATION_SIZES = [100, 1_000, 10_000]
TRAVERSAL_SIZES = [100, 500, 1_000]
DIJKSTRA_SIZES = [100, 500, 1_000]

DIJKSTRA_DENSITIES = [0.01, 0.05, 0.10]

REPETITIONS = 3


def build_list_path_graph(node_count):
    """Build a sparse path graph using an adjacency list."""
    graph = Graph(representation="list")

    for node in range(node_count):
        graph.add_node(node)

    for node in range(node_count - 1):
        graph.add_edge(node, node + 1)

    return graph


def build_matrix_path_graph(node_count):
    """
    Build a sparse path graph using an adjacency matrix.

    The matrix is allocated directly so the 10,000-node test
    does not spend excessive time repeatedly resizing rows.
    """
    graph = Graph(representation="matrix")

    graph.nodes = list(range(node_count))
    graph.index = {
        node: node
        for node in graph.nodes
    }

    graph.matrix = [
        bytearray(node_count)
        for _ in range(node_count)
    ]

    graph.weights = {}

    for node in range(node_count - 1):
        graph.matrix[node][node + 1] = 1
        graph.matrix[node + 1][node] = 1

        graph.weights[(node, node + 1)] = 1
        graph.weights[(node + 1, node)] = 1

    return graph


def estimate_graph_memory(graph):
    """Estimate memory used by the graph representation."""
    total = sys.getsizeof(graph)
    total += sys.getsizeof(graph.nodes)

    if graph.representation == "list":
        total += sys.getsizeof(graph.adjacency)

        for neighbors in graph.adjacency.values():
            total += sys.getsizeof(neighbors)

    else:
        total += sys.getsizeof(graph.matrix)

        for row in graph.matrix:
            total += sys.getsizeof(row)

        total += sys.getsizeof(graph.index)
        total += sys.getsizeof(graph.weights)

    return total


def measure_neighbor_lookup(graph, repetitions=100):
    """Measure average time required to retrieve neighbors."""
    node_count = len(graph.nodes)

    targets = [
        0,
        node_count // 4,
        node_count // 2,
        (3 * node_count) // 4,
        node_count - 1,
    ]

    start = time.perf_counter()

    for _ in range(repetitions):
        for node in targets:
            graph.get_neighbors(node)

    elapsed = time.perf_counter() - start

    operations = repetitions * len(targets)

    return elapsed / operations


def benchmark_representations(sizes=None):
    """Compare adjacency list and adjacency matrix storage."""
    if sizes is None:
        sizes = REPRESENTATION_SIZES

    rows = []

    for size in sizes:
        list_graph = build_list_path_graph(size)

        rows.append(
            {
                "category": "Representation",
                "graph_type": "Sparse Path",
                "algorithm": "Adjacency List",
                "size": size,
                "density": None,
                "time_seconds": measure_neighbor_lookup(
                    list_graph
                ),
                "memory_bytes": estimate_graph_memory(
                    list_graph
                ),
            }
        )

        del list_graph
        gc.collect()

        matrix_graph = build_matrix_path_graph(size)

        rows.append(
            {
                "category": "Representation",
                "graph_type": "Sparse Path",
                "algorithm": "Adjacency Matrix",
                "size": size,
                "density": None,
                "time_seconds": measure_neighbor_lookup(
                    matrix_graph
                ),
                "memory_bytes": estimate_graph_memory(
                    matrix_graph
                ),
            }
        )

        del matrix_graph
        gc.collect()

        print(
            f"Representation size {size:,} complete."
        )

    return rows


def measure_traversal(graph, algorithm):
    """Measure traversal time and peak additional memory."""
    times = []
    memory_values = []

    for _ in range(REPETITIONS):
        tracemalloc.start()

        start = time.perf_counter()
        algorithm(graph, 0)
        elapsed = time.perf_counter() - start

        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append(elapsed)
        memory_values.append(peak_memory)

    return (
        sum(times) / len(times),
        sum(memory_values) / len(memory_values),
    )


def benchmark_traversals(sizes=None):
    """Benchmark BFS and DFS on sparse and dense graphs."""
    if sizes is None:
        sizes = TRAVERSAL_SIZES

    rows = []

    algorithms = [
        ("BFS", bfs),
        ("DFS", dfs_iterative),
    ]

    for size in sizes:
        sparse_graph = generate_sparse_graph(
            size,
            seed=42,
        )

        for name, algorithm in algorithms:
            elapsed, memory = measure_traversal(
                sparse_graph,
                algorithm,
            )

            rows.append(
                {
                    "category": "Traversal",
                    "graph_type": "Sparse",
                    "algorithm": name,
                    "size": size,
                    "density": None,
                    "time_seconds": elapsed,
                    "memory_bytes": memory,
                }
            )

        del sparse_graph
        gc.collect()

        dense_graph = generate_dense_graph(
            size,
            density=0.25,
            seed=42,
        )

        for name, algorithm in algorithms:
            elapsed, memory = measure_traversal(
                dense_graph,
                algorithm,
            )

            rows.append(
                {
                    "category": "Traversal",
                    "graph_type": "Dense",
                    "algorithm": name,
                    "size": size,
                    "density": 0.25,
                    "time_seconds": elapsed,
                    "memory_bytes": memory,
                }
            )

        del dense_graph
        gc.collect()

        print(
            f"Traversal size {size:,} complete."
        )

    return rows


def measure_dijkstra(graph, algorithm):
    """Measure average Dijkstra runtime."""
    times = []

    for _ in range(REPETITIONS):
        start = time.perf_counter()
        algorithm(graph, 0)
        elapsed = time.perf_counter() - start

        times.append(elapsed)

    return sum(times) / len(times)


def benchmark_dijkstra(
    sizes=None,
    densities=None,
):
    """Compare list-based and heap-based Dijkstra."""
    if sizes is None:
        sizes = DIJKSTRA_SIZES

    if densities is None:
        densities = DIJKSTRA_DENSITIES

    rows = []

    algorithms = [
        ("Heap Priority Queue", dijkstra),
        ("List Priority Queue", dijkstra_list),
    ]

    for density in densities:
        for size in sizes:
            graph = generate_weighted_graph(
                size,
                edge_probability=density,
                directed=True,
                seed=42,
            )

            for name, algorithm in algorithms:
                elapsed = measure_dijkstra(
                    graph,
                    algorithm,
                )

                rows.append(
                    {
                        "category": "Dijkstra",
                        "graph_type": "Weighted Directed",
                        "algorithm": name,
                        "size": size,
                        "density": density,
                        "time_seconds": elapsed,
                        "memory_bytes": None,
                    }
                )

            del graph
            gc.collect()

            print(
                "Dijkstra size "
                f"{size:,}, density {density:.2f} complete."
            )

    return rows


def plot_traversal(
    dataframe,
    graph_type,
    filename,
):
    """Create BFS vs DFS traversal performance plot."""
    subset = dataframe[
        (dataframe["category"] == "Traversal")
        & (dataframe["graph_type"] == graph_type)
    ]

    plt.figure(figsize=(8, 6))

    for algorithm in ["BFS", "DFS"]:
        data = subset[
            subset["algorithm"] == algorithm
        ].sort_values("size")

        plt.plot(
            data["size"],
            data["time_seconds"],
            marker="o",
            label=algorithm,
        )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Traversal Time (seconds)")
    plt.title(
        f"BFS vs DFS - {graph_type} Graph"
    )
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / filename,
        bbox_inches="tight",
    )

    plt.close()


def plot_dijkstra(dataframe):
    """Create Dijkstra priority queue performance plot."""
    subset = dataframe[
        dataframe["category"] == "Dijkstra"
    ]

    plt.figure(figsize=(9, 6))

    for density in DIJKSTRA_DENSITIES:
        for algorithm in [
            "Heap Priority Queue",
            "List Priority Queue",
        ]:
            data = subset[
                (subset["density"] == density)
                & (subset["algorithm"] == algorithm)
            ].sort_values("size")

            label = (
                f"{algorithm}, density={density:.2f}"
            )

            plt.plot(
                data["size"],
                data["time_seconds"],
                marker="o",
                label=label,
            )

    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Runtime (seconds)")
    plt.title("Dijkstra Performance")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "dijkstra_performance.png",
        bbox_inches="tight",
    )

    plt.close()


def plot_representation(dataframe):
    """Plot adjacency list vs matrix lookup performance."""
    subset = dataframe[
        dataframe["category"] == "Representation"
    ]

    plt.figure(figsize=(8, 6))

    for algorithm in [
        "Adjacency List",
        "Adjacency Matrix",
    ]:
        data = subset[
            subset["algorithm"] == algorithm
        ].sort_values("size")

        plt.plot(
            data["size"],
            data["time_seconds"],
            marker="o",
            label=algorithm,
        )

    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Neighbor Lookup Time (seconds)")
    plt.title("Adjacency List vs Matrix Lookup")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        RESULTS_DIR / "representation_performance.png",
        bbox_inches="tight",
    )

    plt.close()


def main():
    """Run all Week 4 benchmarks."""
    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Running Week 4 graph benchmarks...")
    print()

    rows = []

    rows.extend(
        benchmark_representations()
    )

    rows.extend(
        benchmark_traversals()
    )

    rows.extend(
        benchmark_dijkstra()
    )

    dataframe = pd.DataFrame(rows)

    dataframe.to_csv(
        RESULTS_DIR / "comparison_table.csv",
        index=False,
    )

    plot_traversal(
        dataframe,
        "Sparse",
        "bfs_vs_dfs_sparse.png",
    )

    plot_traversal(
        dataframe,
        "Dense",
        "bfs_vs_dfs_dense.png",
    )

    plot_dijkstra(dataframe)
    plot_representation(dataframe)

    print()
    print("Week 4 benchmark complete.")
    print("Results saved to:")
    print(RESULTS_DIR)


if __name__ == "__main__":
    main()