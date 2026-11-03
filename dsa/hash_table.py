"""A hash table with separate-chaining collision handling, from scratch.

Used for the entity registry (M7) and general key/value storage.
"""

from __future__ import annotations

from typing import Generic, TypeVar, Iterator, Any

K = TypeVar("K")
V = TypeVar("V")

_INITIAL_CAPACITY = 16
_LOAD_FACTOR = 0.75


class _ChainEntry(Generic[K, V]):
    __slots__ = ("key", "value", "next")

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.next: "_ChainEntry[K, V] | None" = None


class HashTable(Generic[K, V]):
    """Open-addressing-ish hash map using separate chaining on a list of buckets.

    Supports ``get``, ``put``, ``remove``, ``__contains__`` and iteration.
    Resizes automatically when the load factor exceeds ``_LOAD_FACTOR``.
    """

    def __init__(self, capacity: int = _INITIAL_CAPACITY) -> None:
        self._capacity = max(4, capacity)
        self._buckets: list[list[_ChainEntry[K, V]]] = [[] for _ in range(self._capacity)]
        self._size = 0

    # ------------------------------------------------------------------ helpers
    def _hash(self, key: K) -> int:
        return hash(key) % self._capacity

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for bucket in old_buckets:
            for entry in bucket:
                self.put(entry.key, entry.value)

    # ------------------------------------------------------------------ public API
    def put(self, key: K, value: V) -> None:
        """Insert or update *key* -> *value*."""
        if self._size / self._capacity > _LOAD_FACTOR:
            self._resize(self._capacity * 2)
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for entry in bucket:
            if entry.key == key:
                entry.value = value
                return
        bucket.append(_ChainEntry(key, value))
        self._size += 1

    def get(self, key: K, default: Any = None) -> Any:
        """Return the value for *key*, or *default* if absent."""
        idx = self._hash(key)
        for entry in self._buckets[idx]:
            if entry.key == key:
                return entry.value
        return default

    def remove(self, key: K) -> bool:
        """Remove *key*; return ``True`` if it was present."""
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, entry in enumerate(bucket):
            if entry.key == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key: object) -> bool:
        idx = self._hash(key)  # type: ignore[arg-type]
        for entry in self._buckets[idx]:
            if entry.key == key:
                return True
        return False

    def __getitem__(self, key: K) -> V:
        value = self.get(key, _MISSING)
        if value is _MISSING:
            raise KeyError(key)
        return value  # type: ignore[return-value]

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def __delitem__(self, key: K) -> None:
        if not self.remove(key):
            raise KeyError(key)

    def __len__(self) -> int:
        return self._size

    def __bool__(self) -> bool:
        return self._size > 0

    def keys(self) -> Iterator[K]:
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.key

    def values(self) -> Iterator[V]:
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.value

    def items(self) -> Iterator[tuple[K, V]]:
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.key, entry.value

    def __iter__(self) -> Iterator[K]:
        return self.keys()

    def __repr__(self) -> str:
        return "HashTable({" + ", ".join(f"{k!r}: {v!r}" for k, v in self.items()) + "})"


_MISSING: Any = object()