import pytest

from src.structures.heap import MaxHeap, MinHeap, PriorityQueue


def test_min_heap_insert_and_extract():
    heap = MinHeap()

    for value in [5, 3, 8, 1, 4]:
        heap.insert(value)

    assert heap.peek() == 1

    result = []
    while not heap.is_empty():
        result.append(heap.extract_min())

    assert result == [1, 3, 4, 5, 8]


def test_max_heap_insert_and_extract():
    heap = MaxHeap()

    for value in [5, 3, 8, 1, 4]:
        heap.insert(value)

    assert heap.peek() == 8

    result = []
    while not heap.is_empty():
        result.append(heap.extract_max())

    assert result == [8, 5, 4, 3, 1]


def test_min_heap_heapify():
    heap = MinHeap([9, 4, 7, 1, 3])

    assert heap.peek() == 1


def test_max_heap_heapify():
    heap = MaxHeap([9, 4, 7, 1, 3])

    assert heap.peek() == 9


def test_empty_heap_errors():
    min_heap = MinHeap()
    max_heap = MaxHeap()

    with pytest.raises(IndexError):
        min_heap.peek()

    with pytest.raises(IndexError):
        min_heap.extract_min()

    with pytest.raises(IndexError):
        max_heap.peek()

    with pytest.raises(IndexError):
        max_heap.extract_max()


def test_priority_queue():
    queue = PriorityQueue()

    queue.enqueue("low", 3)
    queue.enqueue("high", 1)
    queue.enqueue("medium", 2)

    assert queue.peek() == "high"
    assert queue.dequeue() == "high"
    assert queue.dequeue() == "medium"
    assert queue.dequeue() == "low"
    assert queue.is_empty()