from src.structures import (
    AVLTree,
    ChainingHashTable,
    MaxHeap,
    MinHeap,
    OpenAddressHashTable,
)


def test_min_heap_orders_values():
    heap = MinHeap([5, 1, 4, 2, 3])

    result = []
    while not heap.is_empty():
        result.append(heap.extract_min())

    assert result == [1, 2, 3, 4, 5]


def test_max_heap_orders_values():
    heap = MaxHeap([5, 1, 4, 2, 3])

    result = []
    while not heap.is_empty():
        result.append(heap.extract_max())

    assert result == [5, 4, 3, 2, 1]


def test_avl_matches_sorted_values():
    values = [8, 3, 10, 1, 6, 14, 4, 7]

    tree = AVLTree()

    for value in values:
        tree.insert(value)

    assert tree.inorder() == sorted(values)


def test_hash_tables_match_dictionary():
    values = {
        "alpha": 1,
        "beta": 2,
        "gamma": 3,
    }

    chaining = ChainingHashTable()
    open_address = OpenAddressHashTable()

    for key, value in values.items():
        chaining.insert(key, value)
        open_address.insert(key, value)

    for key, value in values.items():
        assert chaining.get(key) == value
        assert open_address.get(key) == value