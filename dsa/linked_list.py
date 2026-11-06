"""Singly linked list, from scratch.

Used as the backing container for :class:`dsa.queue.Queue` and as the
collision-chaining buckets in :class:`dsa.hash_table.HashTable`.
"""

from __future__ import annotations

from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


class _Node(Generic[T]):
    __slots__ = ("value", "next")

    def __init__(self, value: T, next: Optional["_Node[T]"] = None) -> None:
        self.value = value
        self.next = next


class LinkedList(Generic[T]):
    """A singly linked list with O(1) append and prepend."""

    def __init__(self) -> None:
        self._head: Optional[_Node[T]] = None
        self._tail: Optional[_Node[T]] = None
        self._length = 0

    # ------------------------------------------------------------------ size
    def __len__(self) -> int:
        return self._length

    def __bool__(self) -> bool:
        return self._length > 0

    def __contains__(self, value: object) -> bool:
        return any(value == v for v in self)

    def __iter__(self) -> Iterator[T]:
        node = self._head
        while node is not None:
            yield node.value
            node = node.next

    def __repr__(self) -> str:
        return f"LinkedList([{', '.join(repr(v) for v in self)}])"

    # ------------------------------------------------------------------ add
    def append(self, value: T) -> None:
        """Add *value* to the tail. O(1)."""
        node = _Node(value)
        if self._tail is None:
            self._head = self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._length += 1

    def prepend(self, value: T) -> None:
        """Add *value* to the head. O(1)."""
        node = _Node(value, self._head)
        self._head = node
        if self._tail is None:
            self._tail = node
        self._length += 1

    # ------------------------------------------------------------------ remove
    def remove(self, value: T) -> bool:
        """Remove the first node whose value equals *value*. O(n)."""
        prev: Optional[_Node[T]] = None
        node = self._head
        while node is not None:
            if node.value == value:
                if prev is None:
                    self._head = node.next
                else:
                    prev.next = node.next
                if node is self._tail:
                    self._tail = prev
                self._length -= 1
                return True
            prev = node
            node = node.next
        return False

    # ------------------------------------------------------------------ access
    def to_list(self) -> list[T]:
        return list(self)

    def clear(self) -> None:
        self._head = None
        self._tail = None
        self._length = 0