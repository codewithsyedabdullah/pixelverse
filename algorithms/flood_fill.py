"""Flood fill — 4-connected region growing, from scratch.

Used for the "paint bucket" terrain tool (M3) and for region analysis in the
simulation (e.g. finding a contiguous water body).
"""

from __future__ import annotations

from typing import Callable, Set, Tuple

Cell = Tuple[int, int]
Grid = list[list[object]]


def flood_fill(
    grid: Grid,
    start: Cell,
    predicate: Callable[[object], bool] | None = None,
    target_value: object = None,
) -> Set[Cell]:
    """Return the set of cells reachable from *start* that match the predicate.

    If *predicate* is given it is used; otherwise cells whose value equals
    *target_value* are matched.  Movement is 4-connected (up/down/left/right).
    """
    if predicate is None:
        def predicate(value: object) -> bool:
            return value == target_value

    if not (0 <= start[0] < len(grid) and 0 <= start[1] < len(grid[0])):
        return set()
    if not predicate(grid[start[0]][start[1]]):
        return set()

    height = len(grid)
    width = len(grid[0])
    visited: Set[Cell] = set()
    stack = [start]
    visited.add(start)

    while stack:
        r, c = stack.pop()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                if (nr, nc) not in visited and predicate(grid[nr][nc]):
                    visited.add((nr, nc))
                    stack.append((nr, nc))
    return visited