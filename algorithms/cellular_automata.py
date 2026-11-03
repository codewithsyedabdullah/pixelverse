"""Cellular automata — fire spread and plant growth, from scratch.

Each rule is a function taking a grid and returning a new grid of the same
shape.  Rules are pure: they never mutate their input.
"""

from __future__ import annotations

from typing import Callable, List, Optional

Grid = list[list[str]]


class CARule:
    """Base class for a cellular-automaton rule."""

    def step(self, grid: Grid) -> Grid:
        raise NotImplementedError


def _copy(grid: Grid) -> Grid:
    return [row[:] for row in grid]


def _neighbour_values(grid: Grid, r: int, c: int) -> List[str]:
    out: List[str] = []
    height = len(grid)
    width = len(grid[0]) if grid else 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                out.append(grid[nr][nc])
    return out


def cellular_step(
    grid: Grid,
    rule: Callable[[str, List[str]], str],
    boundary: str = "empty",
) -> Grid:
    """Apply *rule(current, neighbours)* to every cell, returning a new grid."""
    height = len(grid)
    width = len(grid[0]) if grid else 0
    out = _copy(grid)
    for r in range(height):
        for c in range(width):
            neighbours = _neighbour_values(grid, r, c)
            out[r][c] = rule(grid[r][c], neighbours)
    return out


class FireSpreadRule(CARule):
    """Moore-neighbourhood fire spread.

    States: ``"empty"``, ``"fuel"`` (combustible), ``"fire"``, ``"ash"``.
    * A ``"fire"`` cell becomes ``"ash"`` next tick.
    * A ``"fuel"`` cell becomes ``"fire"`` if any Moore neighbour is on fire.
    * Otherwise cells keep their state.
    """

    FUEL = "fuel"
    FIRE = "fire"
    ASH = "ash"
    EMPTY = "empty"

    def step(self, grid: Grid) -> Grid:
        def rule(current: str, neighbours: List[str]) -> str:
            if current == self.FIRE:
                return self.ASH
            if current == self.FUEL:
                if any(n == self.FIRE for n in neighbours):
                    return self.FIRE
            return current

        return cellular_step(grid, rule)


class PlantGrowthRule(CARule):
    """Sparse plant growth on empty cells adjacent to plants.

    States: ``"empty"``, ``"plant"``, ``"water"``.
    * An ``"empty"`` cell becomes ``"plant"`` with probability *spread* if it
      has at least one ``"plant"`` neighbour (Moore) and is not adjacent to
      water on all sides.
    """

    EMPTY = "empty"
    PLANT = "plant"
    WATER = "water"

    def __init__(self, spread: float = 0.3, rng=None) -> None:
        self.spread = spread
        self._rng = rng

    def _rand(self) -> float:
        if self._rng is not None:
            return self._rng.random()
        import random
        return random.random()

    def step(self, grid: Grid) -> Grid:
        height = len(grid)
        width = len(grid[0]) if grid else 0
        out = _copy(grid)
        for r in range(height):
            for c in range(width):
                if grid[r][c] != self.EMPTY:
                    continue
                neighbours = _neighbour_values(grid, r, c)
                if not any(n == self.PLANT for n in neighbours):
                    continue
                if all(n == self.WATER for n in neighbours):
                    continue
                if self._rand() < self.spread:
                    out[r][c] = self.PLANT
        return out


# Convenience aliases matching the public API in algorithms/__init__.py.
fire_spread_step = FireSpreadRule().step
plant_growth_step = PlantGrowthRule().step