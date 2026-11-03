"""A LIFO stack implemented on a Python list, from scratch.

Used for undo/redo history in the world editor (M3).
"""

from __future__ import annotations

from typing import Generic, TypeVar, Iterator, Optional

T = TypeVar("T")


class Stack(Generic[T]):
    """Last-in / first-out container."""

    def __init__(self) -> None:
        self._data: list[T] = []

    def push(self, item: T) -> None:
        """Add *item* to the top of the stack."""
        self._data.append(item)

    def pop(self) -> Optional[T]:
        """Remove and return the top item, or ``None`` if empty."""
        if not self._data:
            return None
        return self._data.pop()

    def peek(self) -> Optional[T]:
        """Return the top item without removing it, or ``None``."""
        return self._data[-1] if self._data else None

    def __len__(self) -> int:
        return len(self._data)

    def __bool__(self) -> bool:
        return bool(self._data)

    def __iter__(self) -> Iterator[T]:
        # Top-to-bottom iteration (most-recent first).
        return iter(reversed(self._data))

    def clear(self) -> None:
        self._data.clear()

    def __repr__(self) -> str:
        return f"Stack({self._data!r})"