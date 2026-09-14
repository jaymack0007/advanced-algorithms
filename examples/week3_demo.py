"""Simple demonstration of the Week 3 data structures."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.structures import (
    AVLTree,
    ChainingHashTable,
    MaxHeap,
    MinHeap,
    OpenAddressHashTable,
)


def main():
    values = [5, 3, 8, 1, 4]

    min_heap = MinHeap(values)
    print("Min-heap first value:", min_heap.peek())

    max_heap = MaxHeap(values)
    print("Max-heap first value:", max_heap.peek())

    tree = AVLTree()
    for value in values:
        tree.insert(value)

    print("AVL in-order:", tree.inorder())

    chaining = ChainingHashTable()
    chaining.insert("name", "Jaymes")
    print("Chaining hash table:", chaining.get("name"))

    open_address = OpenAddressHashTable()
    open_address.insert("course", "CSC5300")
    print("Open addressing hash table:", open_address.get("course"))


if __name__ == "__main__":
    main()