"""Graph search algorithms over a grid, from scratch.

The grid is a 2D list of cell values.  A cell is *walkable* when
``is_walkable(value)`` returns ``True``.  Movement is 4-connected with an
optional per-cell cost (defaults to 1).

* :func:`bfs` — breadth-first search, shortest path in unweighted grids.
* :func:`dfs` — depth-first search (iterative, so no recursion limits).
* :func:`astar` — A* using :class:`dsa.heap.Heap` as the open set and the
  Manhattan heuristic by default.

All functions return the path as a list of ``(row, col)`` cells from start to
goal inclusive, or an empty list when no path exists.
"""

from __future__ import annotations

from typing import Callable, List, Optional, Tuple

from dsa.queue import Queue
from dsa.heap import Heap

Cell = Tuple[int, int]
Grid = list[list[object]]
Heuristic = Callable[[Cell, Cell], float]


def manhattan(a: Cell, b: Cell) -> float:
    """Manhattan distance — admissible for 4-connected movement."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def diagonal(a: Cell, b: Cell) -> float:
    """Chebyshev distance — admissible when diagonal movement is allowed."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def _bounds(grid: Grid) -> tuple[int, int]:
    return len(grid), len(grid[0]) if grid else 0


def _neighbours(r: int, c: int, height: int, width: int) -> List[Cell]:
    out: List[Cell] = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            out.append((nr, nc))
    return out


def _default_walkable(value: object) -> bool:
    return value not in (None, "wall", "obstacle")


def bfs(
    grid: Grid,
    start: Cell,
    goal: Cell,
    is_walkable: Callable[[object], bool] | None = None,
) -> List[Cell]:
    """BFS shortest path on an unweighted 4-connected grid."""
    if is_walkable is None:
        is_walkable = _default_walkable
    height, width = _bounds(grid)
    if not (0 <= start[0] < height and 0 <= start[1] < width):
        return []
    if not (0 <= goal[0] < height and 0 <= goal[1] < width):
        return []
    if start == goal:
        return [start]

    came_from: dict[Cell, Optional[Cell]] = {start: None}
    queue: Queue[Cell] = Queue()
    queue.enqueue(start)

    while queue:
        current = queue.dequeue()
        assert current is not None
        if current == goal:
            return reconstruct_path(came_from, goal)
        for nxt in _neighbours(current[0], current[1], height, width):
            if nxt in came_from:
                continue
            if not is_walkable(grid[nxt[0]][nxt[1]]):
                continue
            came_from[nxt] = current
            queue.enqueue(nxt)
    return []


def dfs(
    grid: Grid,
    start: Cell,
    goal: Cell,
    is_walkable: Callable[[object], bool] | None = None,
) -> List[Cell]:
    """Iterative DFS path (not guaranteed shortest)."""
    if is_walkable is None:
        is_walkable = _default_walkable
    height, width = _bounds(grid)
    if not (0 <= start[0] < height and 0 <= start[1] < width):
        return []
    if not (0 <= goal[0] < height and 0 <= goal[1] < width):
        return []
    if start == goal:
        return [start]

    came_from: dict[Cell, Optional[Cell]] = {start: None}
    stack: List[Cell] = [start]

    while stack:
        current = stack.pop()
        if current == goal:
            return reconstruct_path(came_from, goal)
        for nxt in _neighbours(current[0], current[1], height, width):
            if nxt in came_from:
                continue
            if not is_walkable(grid[nxt[0]][nxt[1]]):
                continue
            came_from[nxt] = current
            stack.append(nxt)
    return []


def astar(
    grid: Grid,
    start: Cell,
    goal: Cell,
    is_walkable: Callable[[object], bool] | None = None,
    cost: Callable[[Cell, Cell], float] | None = None,
    heuristic: Heuristic = manhattan,
) -> List[Cell]:
    """A* search using :class:`dsa.heap.Heap` as the priority queue."""
    if is_walkable is None:
        is_walkable = _default_walkable
    if cost is None:
        cost = lambda a, b: 1.0  # noqa: E731
    height, width = _bounds(grid)
    if not (0 <= start[0] < height and 0 <= start[1] < width):
        return []
    if not (0 <= goal[0] < height and 0 <= goal[1] < width):
        return []
    if start == goal:
        return [start]

    came_from: dict[Cell, Optional[Cell]] = {start: None}
    g_score: dict[Cell, float] = {start: 0.0}
    open_set: Heap[Cell] = Heap()
    open_set.push(start, heuristic(start, goal))

    while open_set:
        current = open_set.pop()
        assert current is not None
        if current == goal:
            return reconstruct_path(came_from, goal)
        for nxt in _neighbours(current[0], current[1], height, width):
            if not is_walkable(grid[nxt[0]][nxt[1]]):
                continue
            tentative = g_score[current] + cost(current, nxt)
            if nxt not in g_score or tentative < g_score[nxt]:
                g_score[nxt] = tentative
                came_from[nxt] = current
                priority = tentative + heuristic(nxt, goal)
                open_set.push(nxt, priority)
    return []


def reconstruct_path(came_from: dict[Cell, Optional[Cell]], goal: Cell) -> List[Cell]:
    """Walk the ``came_from`` map backwards from *goal* to the start."""
    path: List[Cell] = []
    current: Optional[Cell] = goal
    while current is not None:
        path.append(current)
        current = came_from.get(current)
    path.reverse()
    return path