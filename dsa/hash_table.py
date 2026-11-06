"""Separate-chaining hash table, from scratch.

Keys may be any hashable value.  Collisions are resolved by chaining entries
into a :class:`dsa.linked_list.LinkedList`.  The table resizes automatically
when the load factor exceeds a threshold.
"""

from __future__ import annotations

from typing import Iterator, Optional, Tuple, TypeVar

from dsa.linked_list import LinkedList

T = TypeVar("T")

DEFAULT_CAPACITY = 16
DEFAULT_LOAD_FACTOR = 0.75


def _hash_key(key: object) -> int:
    """Hash *key* into a non-negative integer."""
    h = hash(key)
    return h if h >= 0 else -h


class HashTable:
    """A hash map with separate-chaining collision resolution."""

    def __init__(self, capacity: int = DEFAULT_CAPACITY,
                 load_factor: float = DEFAULT_LOAD_FACTOR) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        if not (0.0 < load_factor <= 1.0):
            raise ValueError("load_factor must be in (0, 1]")
        self._capacity = capacity
        self._load_factor = load_factor
        self._buckets: list[LinkedList[Tuple[object, object]]] = [
            LinkedList() for _ in range(capacity)
        ]
        self._size = 0

    # ------------------------------------------------------------------ size
    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def __contains__(self, key: object) -> bool:
        return self.get(key) is not None

    def __iter__(self) -> Iterator[object]:
        for bucket in self._buckets:
            for key, _value in bucket:
                yield key

    def keys(self) -> list[object]:
        return list(self)

    def values(self) -> list[object]:
        out: list[object] = []
        for bucket in self._buckets:
            for _key, value in bucket:
                out.append(value)
        return out

    def items(self) -> list[Tuple[object, object]]:
        out: list[Tuple[object, object]] = []
        for bucket in self._buckets:
            for entry in bucket:
                out.append(entry)
        return out

    # ------------------------------------------------------------------ access
    def _bucket_index(self, key: object) -> int:
        return _hash_key(key) % self._capacity

    def _find(self, key: object) -> Optional[Tuple[object, object]]:
        bucket = self._buckets[self._bucket_index(key)]
        for entry in bucket:
            if entry[0] == key:
                return entry
        return None

    def get(self, key: object, default: object = None) -> object:
        entry = self._find(key)
        return entry[1] if entry is not None else default

    def put(self, key: object, value: object) -> None:
        """Insert or update *key* -> *value*.  Resizes when overloaded."""
        bucket = self._buckets[self._bucket_index(key)]
        for entry in bucket:
            if entry[0] == key:
                # Replace value in place.
                bucket.remove(entry)
                bucket.append((key, value))
                return
        bucket.append((key, value))
        self._size += 1
        if self._size > self._capacity * self._load_factor:
            self._resize(self._capacity * 2)

    def remove(self, key: object) -> Optional[object]:
        """Remove *key* and return its value, or None if absent."""
        bucket = self._buckets[self._bucket_index(key)]
        entry = self._find(key)
        if entry is None:
            return None
        bucket.remove(entry)
        self._size -= 1
        return entry[1]

    def clear(self) -> None:
        for i in range(self._capacity):
            self._buckets[i].clear()
        self._size = 0

    # ------------------------------------------------------------------ resize
    def _resize(self, new_capacity: int) -> None:
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [LinkedList() for _ in range(new_capacity)]
        self._size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)

    def __repr__(self) -> str:
        return f"HashTable(size={self._size}, capacity={self._capacity})"