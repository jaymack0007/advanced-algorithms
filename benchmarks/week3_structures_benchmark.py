"""Week 3 benchmarks for heaps, AVL trees, hash tables, and lists."""

import heapq
import random
import statistics
import sys
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.structures import (
    AVLTree,
    ChainingHashTable,
    MinHeap,
    OpenAddressHashTable,
)

RESULTS_DIR = PROJECT_ROOT / "benchmarks" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

HEAP_SIZES = [1_000, 10_000, 100_000, 1_000_000]
OTHER_SIZES = [1_000, 5_000, 10_000, 50_000]
REPETITIONS = 3


def benchmark_heap():
    """Compare the custom min-heap with Python heapq."""
    rows = []

    for n in HEAP_SIZES:
        data = list(range(n))
        random.Random(42).shuffle(data)

        custom_insert = []
        custom_extract = []
        python_insert = []
        python_extract = []

        for _ in range(REPETITIONS):
            heap = MinHeap()

            start = time.perf_counter()
            for value in data:
                heap.insert(value)
            custom_insert.append(
                (time.perf_counter() - start) / n
            )

            start = time.perf_counter()
            while not heap.is_empty():
                heap.extract_min()
            custom_extract.append(
                (time.perf_counter() - start) / n
            )

            python_heap = []

            start = time.perf_counter()
            for value in data:
                heapq.heappush(python_heap, value)
            python_insert.append(
                (time.perf_counter() - start) / n
            )

            start = time.perf_counter()
            while python_heap:
                heapq.heappop(python_heap)
            python_extract.append(
                (time.perf_counter() - start) / n
            )

        rows.append(
            {
                "category": "Heap",
                "structure": "Custom Heap",
                "size": n,
                "insert": statistics.mean(custom_insert),
                "extract": statistics.mean(custom_extract),
            }
        )

        rows.append(
            {
                "category": "Heap",
                "structure": "heapq",
                "size": n,
                "insert": statistics.mean(python_insert),
                "extract": statistics.mean(python_extract),
            }
        )

        print(f"Heap size {n:,} complete.")

    return pd.DataFrame(rows)


def benchmark_tree_and_list():
    """Compare AVL tree, Python dict, and list search."""
    rows = []

    for n in OTHER_SIZES:
        data = list(range(n))
        random.Random(42).shuffle(data)

        query_count = min(1_000, n)
        queries = random.Random(99).sample(data, query_count)

        avl_insert = []
        avl_search = []
        dict_insert = []
        dict_search = []
        list_search = []

        for _ in range(REPETITIONS):
            tree = AVLTree()

            start = time.perf_counter()
            for value in data:
                tree.insert(value)
            avl_insert.append(
                (time.perf_counter() - start) / n
            )

            start = time.perf_counter()
            for value in queries:
                tree.search(value)
            avl_search.append(
                (time.perf_counter() - start) / query_count
            )

            dictionary = {}

            start = time.perf_counter()
            for value in data:
                dictionary[value] = value
            dict_insert.append(
                (time.perf_counter() - start) / n
            )

            start = time.perf_counter()
            for value in queries:
                _ = dictionary[value]
            dict_search.append(
                (time.perf_counter() - start) / query_count
            )

            list_data = list(data)

            start = time.perf_counter()
            for value in queries:
                _ = value in list_data
            list_search.append(
                (time.perf_counter() - start) / query_count
            )

        rows.append(
            {
                "category": "Tree",
                "structure": "AVL Tree",
                "size": n,
                "insert": statistics.mean(avl_insert),
                "search": statistics.mean(avl_search),
            }
        )

        rows.append(
            {
                "category": "Tree",
                "structure": "Python dict",
                "size": n,
                "insert": statistics.mean(dict_insert),
                "search": statistics.mean(dict_search),
            }
        )

        rows.append(
            {
                "category": "List",
                "structure": "Python List",
                "size": n,
                "search": statistics.mean(list_search),
            }
        )

        print(f"Tree/list size {n:,} complete.")

    return pd.DataFrame(rows)


def benchmark_hash_tables():
    """Compare chaining and open addressing."""
    rows = []

    structures = [
        ("Chaining", ChainingHashTable),
        ("Open Addressing", OpenAddressHashTable),
    ]

    for n in OTHER_SIZES:
        data = list(range(n))
        random.Random(42).shuffle(data)

        for name, table_class in structures:
            insert_times = []
            search_times = []
            delete_times = []
            final_load_factor = 0.0

            for _ in range(REPETITIONS):
                table = table_class()

                start = time.perf_counter()
                for value in data:
                    table.insert(value, value)
                insert_times.append(
                    (time.perf_counter() - start) / n
                )

                final_load_factor = table.load_factor

                start = time.perf_counter()
                for value in data:
                    table.get(value)
                search_times.append(
                    (time.perf_counter() - start) / n
                )

                start = time.perf_counter()
                for value in data:
                    table.delete(value)
                delete_times.append(
                    (time.perf_counter() - start) / n
                )

            rows.append(
                {
                    "category": "Hash Table",
                    "structure": name,
                    "size": n,
                    "insert": statistics.mean(insert_times),
                    "search": statistics.mean(search_times),
                    "delete": statistics.mean(delete_times),
                    "load_factor": final_load_factor,
                }
            )

        print(f"Hash size {n:,} complete.")

    return pd.DataFrame(rows)


def benchmark_hash_load_factor():
    """Measure hash lookup time at different load factors."""
    rows = []

    capacity = 100_000
    load_factors = [0.20, 0.40, 0.60]

    structures = [
        ("Chaining", ChainingHashTable),
        ("Open Addressing", OpenAddressHashTable),
    ]

    for name, table_class in structures:
        for target_load in load_factors:
            count = int(capacity * target_load)
            values = list(range(count))

            query_count = min(1_000, count)
            queries = random.Random(123).sample(
                values,
                query_count,
            )

            search_times = []

            for _ in range(REPETITIONS):
                table = table_class(capacity=capacity)

                for value in values:
                    table.insert(value, value)

                start = time.perf_counter()

                for value in queries:
                    table.get(value)

                search_times.append(
                    (time.perf_counter() - start) / query_count
                )

            rows.append(
                {
                    "category": "Hash Load Factor",
                    "structure": name,
                    "size": count,
                    "load_factor": target_load,
                    "search": statistics.mean(search_times),
                }
            )

    return pd.DataFrame(rows)


def plot_heap(results):
    """Create heap performance graph."""
    plt.figure(figsize=(8, 5))

    for structure in results["structure"].unique():
        data = results[results["structure"] == structure]

        plt.plot(
            data["size"],
            data["insert"],
            marker="o",
            label=f"{structure} insert",
        )

        plt.plot(
            data["size"],
            data["extract"],
            marker="o",
            label=f"{structure} extract",
        )

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input Size")
    plt.ylabel("Average Time per Operation (seconds)")
    plt.title("Heap Performance")
    plt.legend()
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / "heap_performance.png")
    plt.close()


def plot_tree(results):
    """Create AVL, dict, and list comparison graph."""
    plt.figure(figsize=(8, 5))

    for structure in results["structure"].unique():
        data = results[results["structure"] == structure]

        if data["insert"].notna().any():
            plt.plot(
                data["size"],
                data["insert"],
                marker="o",
                label=f"{structure} insert",
            )

        if data["search"].notna().any():
            plt.plot(
                data["size"],
                data["search"],
                marker="o",
                label=f"{structure} search",
            )

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input Size")
    plt.ylabel("Average Time per Operation (seconds)")
    plt.title("AVL Tree, Dict, and List Performance")
    plt.legend()
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / "tree_performance.png")
    plt.close()


def plot_hash(results, list_results):
    """Create hash table and list search comparison graph."""
    plt.figure(figsize=(8, 5))

    for structure in results["structure"].unique():
        data = results[results["structure"] == structure]

        plt.plot(
            data["size"],
            data["insert"],
            marker="o",
            label=f"{structure} insert",
        )

        plt.plot(
            data["size"],
            data["search"],
            marker="o",
            label=f"{structure} search",
        )

        plt.plot(
            data["size"],
            data["delete"],
            marker="o",
            label=f"{structure} delete",
        )

    plt.plot(
        list_results["size"],
        list_results["search"],
        marker="o",
        label="Python List search",
    )

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input Size")
    plt.ylabel("Average Time per Operation (seconds)")
    plt.title("Hash Table Performance")
    plt.legend()
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / "hash_performance.png")
    plt.close()


def plot_hash_load_factor(results):
    """Create load factor versus lookup time graph."""
    plt.figure(figsize=(8, 5))

    for structure in results["structure"].unique():
        data = results[results["structure"] == structure]

        plt.plot(
            data["load_factor"],
            data["search"],
            marker="o",
            label=structure,
        )

    plt.xlabel("Load Factor")
    plt.ylabel("Average Lookup Time (seconds)")
    plt.title("Hash Table Load Factor vs Lookup Time")
    plt.legend()
    plt.tight_layout()

    plt.savefig(RESULTS_DIR / "hash_load_factor.png")
    plt.close()


def main():
    print("Running Week 3 benchmarks with 3 repetitions...")

    heap_results = benchmark_heap()
    tree_results = benchmark_tree_and_list()
    hash_results = benchmark_hash_tables()
    load_results = benchmark_hash_load_factor()

    list_results = tree_results[
        tree_results["structure"] == "Python List"
    ]

    plot_heap(heap_results)
    plot_tree(tree_results)
    plot_hash(hash_results, list_results)
    plot_hash_load_factor(load_results)

    combined = pd.concat(
        [
            heap_results,
            tree_results,
            hash_results,
            load_results,
        ],
        ignore_index=True,
    )

    combined.to_csv(
        RESULTS_DIR / "comparison_table.csv",
        index=False,
    )

    print()
    print("Week 3 benchmark complete.")
    print("Results saved to:")
    print(RESULTS_DIR)


if __name__ == "__main__":
    main()