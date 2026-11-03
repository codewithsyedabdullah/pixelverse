"""Pixelverse algorithms — all implemented from scratch, no external libs.

* :mod:`algorithms.sorting` — classic comparison sorts.
* :mod:`algorithms.flood_fill` — 4-connected flood fill.
* :mod:`algorithms.graph_search` — BFS / DFS / A* over a grid graph.
* :mod:`algorithms.cellular_automata` — fire spread, plant growth.
"""

from __future__ import annotations

from .sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort,
)
from .flood_fill import flood_fill
from .graph_search import bfs, dfs, astar, reconstruct_path, manhattan, diagonal
from .cellular_automata import (
    cellular_step,
    fire_spread_step,
    plant_growth_step,
    CARule,
)

__all__ = [
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "heap_sort",
    "flood_fill",
    "bfs",
    "dfs",
    "astar",
    "reconstruct_path",
    "manhattan",
    "diagonal",
    "cellular_step",
    "fire_spread_step",
    "plant_growth_step",
    "CARule",
]