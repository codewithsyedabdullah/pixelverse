"""A binary min-heap, from scratch.

Used by A* as the priority queue (M5).  ``HeapEntry`` tuples store ``(priority, counter, value)`` so
that equal-priority items are dequeued in insertion order (stable).
"""

from __future__ import annotations

from typing import Generic, TypeVar, Iterator, Optional, Any

T = TypeVar("T")


class HeapEntry(Generic[T]):
    """A single entry in the heap: ``(priority, sequence, value)``."""

    __slots__ = ("priority", "sequence", "value")

    def __init__(self, priority: float, sequence: int, value: T) -> None:
        self.priority = priority
        self.sequence = sequence
        self.value = value

    def __lt__(self, other: "HeapEntry[T]") -> bool:
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.sequence < other.sequence

    def __repr__(self) -> str:
        return f"HeapEntry({self.priority!r}, {self.sequence!r}, {self.value!r})"


class Heap(Generic[T]):
    """Binary min-heap of :class:`HeapEntry` items."""

    def __init__(self) -> None:
        self._data: list[HeapEntry[T]] = []
        self._counter = 0

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _left(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def _right(i: int) -> int:
        return 2 * i + 2

    def _sift_up(self, i: int) -> None:
        while i > 0:
            p = self._parent(i)
            if self._data[i] < self._data[p]:
                self._data[i], self._data[p] = self._data[p], self._data[i]
                i = p
            else:
                break

    def _sift_down(self, i: int) -> None:
        n = len(self._data)
        while True:
            smallest = i
            l = self._left(i)
            r = self._right(i)
            if l < n and self._data[l] < self._data[smallest]:
                smallest = l
            if r < n and self._data[r] < self._data[smallest]:
                smallest = r
            if smallest == i:
                break
            self._data[i], self._data[smallest] = self._data[smallest], self._data[i]
            i = smallest

    # ------------------------------------------------------------------ public API
    def push(self, value: T, priority: float) -> None:
        """Insert *value* with *priority* (lower = sooner)."""
        entry = HeapEntry(priority, self._counter, value)
        self._counter += 1
        self._data.append(entry)
        self._sift_up(len(self._data) - 1)

    def pop(self) -> Optional[T]:
        """Remove and return the lowest-priority value, or ``None`` if empty."""
        if not self._data:
            return None
        top = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return top.value

    def peek(self) -> Optional[T]:
        """Return the lowest-priority value without removing it, or ``None``."""
        return self._data[0].value if self._data else None

    def peek_entry(self) -> Optional[HeapEntry[T]]:
        return self._data[0] if self._data else None

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __iter__(self) -> Iterator[T]:
        # Snapshot iteration (not heap order) — used by the DSA lab visualiser.
        return iter(entry.value for entry in self._data)

    def clear(self) -> None:
        self._data.clear()
        self._counter = 0

    def __repr__(self) -> str:
        return f"Heap({self._data!r})"