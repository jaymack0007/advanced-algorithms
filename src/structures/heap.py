"""Binary heap and priority queue implementations."""

from typing import Generic, Iterable, List, Optional, TypeVar

T = TypeVar("T")


class MinHeap(Generic[T]):
    """Array-based min-heap."""

    def __init__(self, values: Optional[Iterable[T]] = None):
        self.items: List[T] = list(values) if values is not None else []
        if self.items:
            self.heapify()

    def insert(self, value: T) -> None:
        """Insert a value into the heap."""
        self.items.append(value)
        self._bubble_up(len(self.items) - 1)

    def extract_min(self) -> T:
        """Remove and return the smallest value."""
        if self.is_empty():
            raise IndexError("extract from empty heap")

        minimum = self.items[0]
        last = self.items.pop()

        if self.items:
            self.items[0] = last
            self._bubble_down(0)

        return minimum

    def peek(self) -> T:
        """Return the smallest value without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self.items[0]

    def is_empty(self) -> bool:
        """Return True when the heap has no values."""
        return len(self.items) == 0

    def heapify(self) -> None:
        """Restore min-heap order for the current items."""
        for index in range(len(self.items) // 2 - 1, -1, -1):
            self._bubble_down(index)

    def _bubble_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2

            if self.items[index] >= self.items[parent]:
                break

            self.items[index], self.items[parent] = (
                self.items[parent],
                self.items[index],
            )
            index = parent

    def _bubble_down(self, index: int) -> None:
        size = len(self.items)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index

            if left < size and self.items[left] < self.items[smallest]:
                smallest = left

            if right < size and self.items[right] < self.items[smallest]:
                smallest = right

            if smallest == index:
                break

            self.items[index], self.items[smallest] = (
                self.items[smallest],
                self.items[index],
            )
            index = smallest


class MaxHeap(Generic[T]):
    """Array-based max-heap."""

    def __init__(self, values: Optional[Iterable[T]] = None):
        self.items: List[T] = list(values) if values is not None else []
        if self.items:
            self.heapify()

    def insert(self, value: T) -> None:
        """Insert a value into the heap."""
        self.items.append(value)
        self._bubble_up(len(self.items) - 1)

    def extract_max(self) -> T:
        """Remove and return the largest value."""
        if self.is_empty():
            raise IndexError("extract from empty heap")

        maximum = self.items[0]
        last = self.items.pop()

        if self.items:
            self.items[0] = last
            self._bubble_down(0)

        return maximum

    def peek(self) -> T:
        """Return the largest value without removing it."""
        if self.is_empty():
            raise IndexError("peek from empty heap")
        return self.items[0]

    def is_empty(self) -> bool:
        """Return True when the heap has no values."""
        return len(self.items) == 0

    def heapify(self) -> None:
        """Restore max-heap order for the current items."""
        for index in range(len(self.items) // 2 - 1, -1, -1):
            self._bubble_down(index)

    def _bubble_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2

            if self.items[index] <= self.items[parent]:
                break

            self.items[index], self.items[parent] = (
                self.items[parent],
                self.items[index],
            )
            index = parent

    def _bubble_down(self, index: int) -> None:
        size = len(self.items)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            largest = index

            if left < size and self.items[left] > self.items[largest]:
                largest = left

            if right < size and self.items[right] > self.items[largest]:
                largest = right

            if largest == index:
                break

            self.items[index], self.items[largest] = (
                self.items[largest],
                self.items[index],
            )
            index = largest


class PriorityQueue:
    """Simple priority queue using a min-heap."""

    def __init__(self):
        self.heap = MinHeap()

    def enqueue(self, value, priority: int) -> None:
        """Add a value with its priority."""
        self.heap.insert((priority, value))

    def dequeue(self):
        """Remove and return the highest-priority value."""
        _, value = self.heap.extract_min()
        return value

    def peek(self):
        """Return the highest-priority value without removing it."""
        _, value = self.heap.peek()
        return value

    def is_empty(self) -> bool:
        """Return True when the queue is empty."""
        return self.heap.is_empty()