"""LIFO stack, from scratch.

Backed by :class:`dsa.linked_list.LinkedList` so push/pop are O(1).
"""

from __future__ import annotations

from typing import Generic, Iterator, Optional, TypeVar

from dsa.linked_list import LinkedList

T = TypeVar("T")


class Stack(Generic[T]):
    """A last-in, first-out stack."""

    def __init__(self) -> None:
        self._list: LinkedList[T] = LinkedList()

    def push(self, value: T) -> None:
        """Add *value* to the top of the stack. O(1)."""
        self._list.prepend(value)

    def pop(self) -> Optional[T]:
        """Remove and return the top value, or None if empty. O(1)."""
        if not self._list:
            return None
        value = self._list._head.value
        self._list.remove(value)
        return value

    def peek(self) -> Optional[T]:
        """Return the top value without removing it. O(1)."""
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
        return f"Stack({self._list.to_list()!r})"