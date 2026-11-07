"""FIFO queue, from scratch.

Backed by :class:`dsa.linked_list.LinkedList` so enqueue/dequeue are O(1).
"""

from __future__ import annotations

from typing import Generic, Iterator, Optional, TypeVar

from dsa.linked_list import LinkedList

T = TypeVar("T")


class Queue(Generic[T]):
    """A first-in, first-out queue."""

    def __init__(self) -> None:
        self._list: LinkedList[T] = LinkedList()

    def enqueue(self, value: T) -> None:
        """Add *value* to the tail of the queue. O(1)."""
        self._list.append(value)

    def dequeue(self) -> Optional[T]:
        """Remove and return the head value, or None if empty. O(1)."""
        if not self._list:
            return None
        value = self._list._head.value
        self._list.remove(value)
        return value

    def peek(self) -> Optional[T]:
        """Return the head value without removing it. O(1)."""
        return self._list._head.value if self._list._head is not None else None

    def __len__(self) -> int:
        return len(self._list)

    def __bool__(self) -> bool:
        return bool(self._list)

    def __contains__(self, value: object) -> bool:
        return value in self._list

    def __iter__(self) -> Iterator[T]:
        return iter(self._list)

    def clear(self) -> None:
        self._list.clear()

    def to_list(self) -> list[T]:
        return self._list.to_list()

    def __repr__(self) -> str:
        return f"Queue({self._list.to_list()!r})"