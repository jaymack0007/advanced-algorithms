"""Hash table implementations using chaining and linear probing."""

from typing import Any, List, Optional, Tuple


class ChainingHashTable:
    """Hash table using separate chaining."""

    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.size = 0
        self.buckets: List[List[Tuple[Any, Any]]] = [
            [] for _ in range(capacity)
        ]

    def _index(self, key: Any) -> int:
        return hash(key) % self.capacity

    @property
    def load_factor(self) -> float:
        """Return the current load factor."""
        return self.size / self.capacity

    def insert(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair."""
        index = self._index(key)
        bucket = self.buckets[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self.size += 1

        if self.load_factor > 0.75:
            self._rehash()

    def get(self, key: Any) -> Any:
        """Return the value for a key."""
        index = self._index(key)

        for existing_key, value in self.buckets[index]:
            if existing_key == key:
                return value

        raise KeyError(key)

    def delete(self, key: Any) -> None:
        """Delete a key-value pair."""
        index = self._index(key)
        bucket = self.buckets[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket.pop(i)
                self.size -= 1
                return

        raise KeyError(key)

    def _rehash(self) -> None:
        """Double the table size and reinsert all items."""
        old_buckets = self.buckets

        self.capacity *= 2
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

        for bucket in old_buckets:
            for key, value in bucket:
                self.insert(key, value)


class OpenAddressHashTable:
    """Hash table using linear probing."""

    DELETED = object()

    def __init__(self, capacity: int = 8):
        self.capacity = capacity
        self.size = 0
        self.table: List[Optional[Tuple[Any, Any]]] = [
            None for _ in range(capacity)
        ]

    def _index(self, key: Any) -> int:
        return hash(key) % self.capacity

    @property
    def load_factor(self) -> float:
        """Return the current load factor."""
        return self.size / self.capacity

    def insert(self, key: Any, value: Any) -> None:
        """Insert or update a key-value pair."""
        if self.load_factor > 0.65:
            self._rehash()

        index = self._index(key)
        first_deleted = None

        for _ in range(self.capacity):
            entry = self.table[index]

            if entry is None:
                target = first_deleted if first_deleted is not None else index
                self.table[target] = (key, value)
                self.size += 1
                return

            if entry is self.DELETED:
                if first_deleted is None:
                    first_deleted = index

            elif entry[0] == key:
                self.table[index] = (key, value)
                return

            index = (index + 1) % self.capacity

        raise RuntimeError("Hash table is full")

    def get(self, key: Any) -> Any:
        """Return the value for a key."""
        index = self._index(key)

        for _ in range(self.capacity):
            entry = self.table[index]

            if entry is None:
                break

            if entry is not self.DELETED and entry[0] == key:
                return entry[1]

            index = (index + 1) % self.capacity

        raise KeyError(key)

    def delete(self, key: Any) -> None:
        """Delete a key-value pair."""
        index = self._index(key)

        for _ in range(self.capacity):
            entry = self.table[index]

            if entry is None:
                break

            if entry is not self.DELETED and entry[0] == key:
                self.table[index] = self.DELETED
                self.size -= 1
                return

            index = (index + 1) % self.capacity

        raise KeyError(key)

    def _rehash(self) -> None:
        """Double the table size and reinsert all active items."""
        old_table = self.table

        self.capacity *= 2
        self.size = 0
        self.table = [None for _ in range(self.capacity)]

        for entry in old_table:
            if entry is not None and entry is not self.DELETED:
                key, value = entry
                self.insert(key, value)