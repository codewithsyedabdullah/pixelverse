"""Undo/redo command pattern for world editing (Milestone A).

Each edit (paint, erase, fill, place) is wrapped in a :class:`Command`
that knows how to apply and reverse itself.  The :class:`CommandHistory`
stores commands on a `dsa/stack`-backed redo stack.
"""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from dsa.stack import Stack


class Command:
    """Base class for an editable command.  Subclasses override apply/reverse."""

    def __init__(self, description: str = "") -> None:
        self.description = description

    def apply(self, world) -> None:
        raise NotImplementedError

    def reverse(self, world) -> None:
        raise NotImplementedError


class PaintCommand(Command):
    """Set a single cell's terrain."""

    def __init__(self, col: int, row: int, terrain: str) -> None:
        super().__init__(description=f"paint ({col},{row}) -> {terrain}")
        self.col = col
        self.row = row
        self.terrain = terrain
        self._previous: Optional[str] = None

    def apply(self, world) -> None:
        if world.in_bounds(self.col, self.row):
            self._previous = world.get_terrain(self.col, self.row)
            world.set_terrain(self.col, self.row, self.terrain)

    def reverse(self, world) -> None:
        if self._previous is not None and world.in_bounds(self.col, self.row):
            world.set_terrain(self.col, self.row, self._previous)


class FillCommand(Command):
    """Fill a connected region with a new terrain (uses flood_fill)."""

    def __init__(self, col: int, row: int, terrain: str) -> None:
        super().__init__(description=f"fill from ({col},{row}) -> {terrain}")
        self.col = col
        self.row = row
        self.terrain = terrain
        self._cells: List[Tuple[int, int, str]] = []

    def apply(self, world) -> None:
        from algorithms.flood_fill import flood_fill

        grid = [
            [world.get_terrain(c, r) for c in range(world.width)]
            for r in range(world.height)
        ]
        if not (0 <= self.col < world.width and 0 <= self.row < world.height):
            return
        target = grid[self.row][self.col]
        region = flood_fill(grid, (self.row, self.col), target_value=target)
        for r, c in region:
            if 0 <= c < world.width and 0 <= r < world.height:
                self._cells.append((c, r, world.get_terrain(c, r)))
                world.set_terrain(c, r, self.terrain)

    def reverse(self, world) -> None:
        for c, r, prev in self._cells:
            world.set_terrain(c, r, prev)


class CommandHistory:
    """Tracks applied commands and supports undo/redo.

    Uses a `dsa/stack` for the redo stack; the undo stack is a plain list.
    """

    def __init__(self, world=None) -> None:
        self._undo: List[Command] = []
        self._redo: Stack[Command] = Stack()
        self._on_change: Optional[Callable[[], None]] = None
        self._world = world

    def set_on_change(self, callback: Callable[[], None]) -> None:
        self._on_change = callback

    def push(self, command: Command) -> None:
        self._undo.append(command)
        self._redo = Stack()  # clear redo on new action
        self._notify()

    def undo(self, world=None) -> Optional[Command]:
        if not self._undo:
            return None
        command = self._undo.pop()
        command.reverse(world if world is not None else self._world)
        self._redo.push(command)
        self._notify()
        return command

    def redo(self, world=None) -> Optional[Command]:
        if not self._redo:
            return None
        command = self._redo.pop()
        command.apply(world if world is not None else self._world)
        self._undo.append(command)
        self._notify()
        return command

    def can_undo(self) -> bool:
        return len(self._undo) > 0

    def can_redo(self) -> bool:
        return len(self._redo) > 0

    def clear(self) -> None:
        self._undo = []
        self._redo = Stack()
        self._notify()

    def undo_description(self) -> Optional[str]:
        return self._undo[-1].description if self._undo else None

    def redo_description(self) -> Optional[str]:
        return self._redo.peek().description if self._redo else None

    def _notify(self) -> None:
        if self._on_change is not None:
            self._on_change()

    def __len__(self) -> int:
        return len(self._undo)