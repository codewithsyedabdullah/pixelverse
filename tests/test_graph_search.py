"""Tests for algorithms/flood_fill.py and algorithms/graph_search.py."""

from __future__ import annotations

import pytest

from algorithms.flood_fill import flood_fill
from algorithms.graph_search import bfs, dfs, astar, reconstruct_path, manhattan, diagonal


# --------------------------------------------------------------------------- helpers
def grid_from(rows):
    """Build a grid where each *row* is a string of single-character cells."""
    return [list(r) for r in rows]


def word_grid(rows):
    """Build a grid where each *row* is a single multi-character cell."""
    return [[r] for r in rows]


def walkable(c):
    """A cell is walkable when it is not an obstacle marker."""
    return c != "#"


def unwalkable(c):
    """A cell is walkable only when it equals ``'open'``."""
    return c == "open"


# --------------------------------------------------------------------------- flood fill
class TestFloodFill:
    def test_empty_grid(self):
        g = grid_from([""])
        assert flood_fill(g, (0, 0)) == set()

    def test_single_cell(self):
        g = grid_from(["A"])
        assert flood_fill(g, (0, 0), target_value="A") == {(0, 0)}

    def test_region(self):
        g = grid_from([
            "AAA",
            "A#A",
            "AAA",
        ])
        assert flood_fill(g, (0, 0), target_value="A") == {
            (0, 0), (0, 1), (0, 2),
            (1, 0),         (1, 2),
            (2, 0), (2, 1), (2, 2),
        }

    def test_target_value(self):
        g = grid_from([
            "AB",
            "BA",
        ])
        region = flood_fill(g, (0, 0), target_value="A")
        assert region == {(0, 0)}

    def test_predicate(self):
        g = grid_from(["abc", "def"])
        region = flood_fill(g, (0, 0), predicate=lambda v: v.isalpha())
        assert region == {(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)}

    def test_start_out_of_bounds(self):
        g = grid_from(["AB"])
        assert flood_fill(g, (5, 5)) == set()

    def test_start_on_wall(self):
        g = grid_from(["#A"])
        assert flood_fill(g, (0, 0), target_value="#") == {(0, 0)}


# --------------------------------------------------------------------------- graph search
class TestBFS:
    def test_same_start_goal(self):
        g = grid_from(["."])
        assert bfs(g, (0, 0), (0, 0)) == [(0, 0)]

    def test_no_path(self):
        # Start is open but the goal is a wall, so it can never be reached.
        g = grid_from(["open", "wall"])
        assert bfs(g, (0, 0), (0, 1), unwalkable) == []

    def test_shortest_path(self):
        g = grid_from([
            "openopen",
            "open#open",
            "openopen",
        ])
        path = bfs(g, (0, 0), (2, 1), walkable)
        assert path[0] == (0, 0) and path[-1] == (2, 1)
        assert len(path) == 4  # Manhattan distance 3 -> 4 cells

    def test_around_wall(self):
        # Row 1 is a wall except at column 4, so the shortest route goes
        # through the gap in the middle of the wall.
        g = grid_from([
            "openopenopenopenopen",
            "####open#######",
            "openopenopenopenopen",
        ])
        path = bfs(g, (0, 0), (2, 2), walkable)
        assert path[0] == (0, 0) and path[-1] == (2, 2)
        assert path == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                        (1, 4), (2, 4), (2, 3), (2, 2)]


class TestDFS:
    def test_finds_path(self):
        g = grid_from([
            "...",
            ".#.",
            "...",
        ])
        path = dfs(g, (0, 0), (2, 2), walkable)
        assert path[0] == (0, 0) and path[-1] == (2, 2)

    def test_no_path(self):
        # Start is open but the goal is a wall, so it can never be reached.
        g = word_grid(["open", "wall"])
        assert dfs(g, (0, 0), (0, 1), unwalkable) == []


class TestAStar:
    def test_same_start_goal(self):
        g = grid_from(["."])
        assert astar(g, (0, 0), (0, 0)) == [(0, 0)]

    def test_no_path(self):
        # Start is open but the goal is a wall, so it can never be reached.
        g = word_grid(["open", "wall"])
        assert astar(g, (0, 0), (0, 1), unwalkable) == []

    def test_shortest_path(self):
        g = grid_from([
            "...",
            ".#.",
            "...",
        ])
        path = astar(g, (0, 0), (2, 2), walkable)
        assert path[0] == (0, 0) and path[-1] == (2, 2)
        assert len(path) == 5

    def test_with_cost(self):
        g = grid_from([
            ".#.",
            ".#.",
            "...",
        ])
        path = astar(g, (0, 0), (2, 2), walkable)
        assert path[0] == (0, 0) and path[-1] == (2, 2)

    def test_manhattan_heuristic_admissible(self):
        assert manhattan((0, 0), (3, 4)) == 7
        assert diagonal((0, 0), (3, 4)) == 4


class TestReconstructPath:
    def test_empty(self):
        assert reconstruct_path({}, (5, 5)) == [(5, 5)]

    def test_chain(self):
        came_from = {(0, 0): None, (0, 1): (0, 0), (0, 2): (0, 1)}
        assert reconstruct_path(came_from, (0, 2)) == [(0, 0), (0, 1), (0, 2)]