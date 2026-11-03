"""A FIFO queue implemented on a linked list, from scratch.

Used for the simulation event queue (M6) and BFS frontier (M5).
"""

from __future__ import annotations

from typing import Generic, TypeVar, Iterator, Optional

T = TypeVar("T")


class Queue(Generic[T]):
    """First-in / first-out container backed by a singly linked list."""

    def __init__(self) -> None:
        self._head: Optional[_Node[T]] = None
        self._tail: Optional[_Node[T]] = None
        self._length = 0

    def enqueue(self, item: T) -> None:
        """Add *item* to the back of the queue."""
        node = _Node(item)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._length += 1

    def dequeue(self) -> Optional[T]:
        """Remove and return the front item, or ``None`` if empty."""
        if self._head is None:
            return None
        item = self._head.value
        self._head = self._head.next
        if self._head is None:
            self._tail = None
        self._length -= 1
        return item

    def peek(self) -> Optional[T]:
        """Return the front item without removing it, or ``None``."""
        return self._head.value if self._head is not None else None

    def __len__(self) -> int:
        return self._length

    def __bool__(self) -> bool:
        return self._length > 0

    def __iter__(self) -> Iterator[T]:
        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def clear(self) -> None:
        self._head = self._tail = None
        self._length = 0

    def __repr__(self) -> str:
        return f"Queue([{', '.join(repr(x) for x in self)}])"


class _Node(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T) -> None:
        self.value = value
        self.next: Optional[_Node[T]] = None