"""World grid model for PIXELVERSE.

A World holds a two-dimensional array of terrain cells plus the metadata
needed to save, load and reset a simulation.  This module contains NO UI
logic and NO entity behaviour, so it can be tested headlessly.
"""

from __future__ import annotations

import copy
import random
from typing import List, Optional, Tuple

from config import (
    DEFAULT_WORLD_HEIGHT,
    DEFAULT_WORLD_WIDTH,
    DEFAULT_RANDOM_SEED,
    TerrainType,
    TERRAIN_PROPERTIES,
)


class World:
    """A grid-based world made of terrain cells.

    The grid is a plain Python list-of-lists (a two-dimensional array).
    Accessing a cell is O(1): ``self._grid[row][col]``.
    """

    def __init__(
        self,
        width: int = DEFAULT_WORLD_WIDTH,
        height: int = DEFAULT_WORLD_HEIGHT,
        name: str = "Untitled World",
        seed: int = DEFAULT_RANDOM_SEED,
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("World dimensions must be positive.")
        self.width = width
        self.height = height
        self.name = name
        self.seed = seed
        self._rng = random.Random(seed)
        # Two-dimensional array: grid[row][col] -> terrain name string
        self._grid: List[List[str]] = self._build_empty_grid()

    # ----------------------------------------------------------- grid helpers
    def _build_empty_grid(self) -> List[List[str]]:
        """Create a grid filled with grass (a reasonable starting terrain)."""
        return [
            [TerrainType.GRASS for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def in_bounds(self, col: int, row: int) -> bool:
        """Return True if (col, row) is inside the world."""
        return 0 <= col < self.width and 0 <= row < self.height

    def get_terrain(self, col: int, row: int) -> str:
        """Return the terrain name at (col, row)."""
        return self._grid[row][col]

    def set_terrain(self, col: int, row: int, terrain: str) -> None:
        """Set the terrain at (col, row)."""
        self._grid[row][col] = terrain

    def is_walkable(self, col: int, row: int) -> bool:
        """Return True if an organism can stand on this cell."""
        if not self.in_bounds(col, row):
            return False
        return TERRAIN_PROPERTIES[self._grid[row][col]]["walkable"]

    def movement_cost(self, col: int, row: int) -> float:
        """Return the movement cost for this cell (used as graph edge weight)."""
        return TERRAIN_PROPERTIES[self._grid[row][col]]["movement_cost"]

    # ------------------------------------------------------------- generators
    def generate_random(self) -> None:
        """Fill the world with a random mix of terrain.

        This gives the user something interesting to start with instead of
        an empty grass field.  Uses the world's seeded RNG so the result is
        reproducible.
        """
        for row in range(self.height):
            for col in range(self.width):
                roll = self._rng.random()
                if roll < 0.45:
                    self._grid[row][col] = TerrainType.GRASS
                elif roll < 0.55:
                    self._grid[row][col] = TerrainType.WATER
                elif roll < 0.70:
                    self._grid[row][col] = TerrainType.SAND
                elif roll < 0.82:
                    self._grid[row][col] = TerrainType.ROCK
                elif roll < 0.93:
                    self._grid[row][col] = TerrainType.FOREST
                else:
                    self._grid[row][col] = TerrainType.SOIL

    def clear(self, terrain: str = TerrainType.GRASS) -> None:
        """Reset every cell to the given terrain."""
        for row in range(self.height):
            for col in range(self.width):
                self._grid[row][col] = terrain

    # ----------------------------------------------------------- grid access
    def iter_cells(self):
        """Yield (col, row, terrain) for every cell in the world."""
        for row in range(self.height):
            for col in range(self.width):
                yield col, row, self._grid[row][col]

    def to_dict(self) -> dict:
        """Serialise the world to a plain dictionary (for JSON saving)."""
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "seed": self.seed,
            "terrain": [
                [self._grid[row][col] for col in range(self.width)]
                for row in range(self.height)
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "World":
        """Rebuild a World from a dictionary produced by ``to_dict``."""
        world = cls(
            width=data["width"],
            height=data["height"],
            name=data.get("name", "Untitled World"),
            seed=data.get("seed", DEFAULT_RANDOM_SEED),
        )
        terrain = data["terrain"]
        for row in range(world.height):
            for col in range(world.width):
                world._grid[row][col] = terrain[row][col]
        return world

    def clone(self) -> "World":
        """Return an independent deep copy of this world."""
        return World.from_dict(self.to_dict())

    # ------------------------------------------------------------- debugging
    def __repr__(self) -> str:
        return (
            f"World(name={self.name!r}, size={self.width}x{self.height}, "
            f"seed={self.seed})"
        )