"""Binary min-heap, from scratch.

Implements a classic binary heap as a flat array.  The minimum element is
always at index 0.  When priorities tie, insertion order decides — entries
inserted earlier come out first.

If no priority is supplied, the value itself is used as the key, so the
heap doubles as a plain value-heap.
"""

from __future__ import annotations

import itertools
from typing import Any, Generic, Iterator, List, Optional, Tuple, TypeVar

T = TypeVar("T")


class Heap(Generic[T]):
    """A binary min-heap.

    Elements are (priority, counter, value) triples.  Lower priority comes
    first.  When priorities tie, the counter (insertion order) decides — the
    first inserted wins.
    """

    def __init__(self) -> None:
        self._heap: List[Tuple[Any, int, T]] = []
        self._counter = itertools.count()

    # ------------------------------------------------------------------ size
    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def __contains__(self, value: object) -> bool:
        return any(entry[2] == value for entry in self._heap)

    def __iter__(self) -> Iterator[T]:
        return iter([entry[2] for entry in self._heap])

    def peek(self) -> Optional[T]:
        """Return the minimum value without removing it. O(1)."""
        return self._heap[0][2] if self._heap else None

    def peek_priority(self) -> Optional[Any]:
        return self._heap[0][0] if self._heap else None

    # ------------------------------------------------------------------ add
    def push(self, value: T, priority: Optional[Any] = None) -> None:
        """Insert *value*.  When *priority* is None the value itself is used
        as the key.  O(log n)."""
        key = value if priority is None else priority
        self._heap.append((key, next(self._counter), value))
        self._sift_up(len(self._heap) - 1)

    def push_all(self, values, priority: Optional[Any] = None) -> None:
        for value in values:
            self.push(value, priority)

    # ------------------------------------------------------------------ remove
    def pop(self) -> Optional[T]:
        """Remove and return the minimum value.  O(log n)."""
        if not self._heap:
            return None
        return self._pop_at(0)

    def remove(self, value: T) -> bool:
        """Remove the first occurrence of *value*.  O(n)."""
        for i, entry in enumerate(self._heap):
            if entry[2] == value:
                self._pop_at(i)
                return True
        return False

    def clear(self) -> None:
        self._heap = []
        self._counter = itertools.count()

    def to_list(self) -> list[T]:
        out: list[T] = []
        while self:
            out.append(self.pop())
        return out

    # ------------------------------------------------------------------ internals
    def _pop_at(self, index: int) -> T:
        last = self._heap.pop()
        if index == len(self._heap):
            return last[2]
        value = self._heap[index][2]
        self._heap[index] = last
        self._sift_down(index)
        self._sift_up(index)
        return value

    def _sift_up(self, index: int) -> None:
        heap = self._heap
        while index > 0:
            parent = (index - 1) // 2
            if self._less(index, parent):
                heap[index], heap[parent] = heap[parent], heap[index]
                index = parent
            else:
                break

    def _sift_down(self, index: int) -> None:
        heap = self._heap
        n = len(heap)
        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            smallest = index
            if left < n and self._less(left, smallest):
                smallest = left
            if right < n and self._less(right, smallest):
                smallest = right
            if smallest == index:
                break
            heap[index], heap[smallest] = heap[smallest], heap[index]
            index = smallest

    def _less(self, a: int, b: int) -> bool:
        pa, ca = self._heap[a][0], self._heap[a][1]
        pb, cb = self._heap[b][0], self._heap[b][1]
        if pa == pb:
            return ca < cb
        try:
            return pa < pb
        except TypeError:
            return ca < cb

    def __repr__(self) -> str:
        return f"Heap({[e[2] for e in self._heap]!r})"