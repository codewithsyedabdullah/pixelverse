"""A singly linked list, from scratch.

Used as the frontier store in pathfinding when a plain list is preferred, and
as a teaching example in the DSA lab panel.
"""

from __future__ import annotations

from typing import Generic, TypeVar, Iterator, Optional

T = TypeVar("T")


class LinkedList(Generic[T]):
    """Singly linked list with head/tail pointers."""

    def __init__(self, iterable=()) -> None:
        self._head: Optional[_LLNode[T]] = None
        self._tail: Optional[_LLNode[T]] = None
        self._length = 0
        for item in iterable:
            self.append(item)

    def append(self, item: T) -> None:
        """Append *item* to the tail in O(1)."""
        node = _LLNode(item)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._length += 1

    def prepend(self, item: T) -> None:
        """Insert *item* at the head in O(1)."""
        node = _LLNode(item, self._head)
        self._head = node
        if self._tail is None:
            self._tail = node
        self._length += 1

    def pop(self) -> Optional[T]:
        """Remove and return the tail, or ``None`` if empty (O(n))."""
        if self._head is None:
            return None
        if self._head is self._tail:
            item = self._head.value
            self._head = self._tail = None
            self._length -= 1
            return item
        current = self._head
        while current.next is not self._tail:
            current = current.next
        assert current.next is not None
        item = current.next.value
        current.next = None
        self._tail = current
        self._length -= 1
        return item

    def __len__(self) -> int:
        return self._length

    def __bool__(self) -> bool:
        return self._length > 0

    def __iter__(self) -> Iterator[T]:
        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def __repr__(self) -> str:
        return f"LinkedList([{', '.join(repr(x) for x in self)}])"


class _LLNode(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T, nxt: Optional[_LLNode[T]] = None) -> None:
        self.value = value
        self.next = nxt