"""World grid model — the 2D terrain array that everything else sits on.

The world is a rectangular grid of cells.  Each cell holds a single terrain
type (grass, water, sand, rock, forest, soil).  Organisms and pathfinding in
later milestones read and write this grid; M2 only needs the data model and
basic accessors.

Coordinate system
-----------------
Cells are addressed by (x, y) where ``x`` is the column (0 .. width-1) and
``y`` is the row (0 .. height-1).  Origin (0, 0) is the top-left corner,
matching how a QGraphicsScene maps cells to pixels.
"""

from __future__ import annotations

from typing import List

from config import (
    DEFAULT_WORLD_HEIGHT,
    DEFAULT_WORLD_WIDTH,
    TERRAIN_PROPERTIES,
    TerrainType,
)


class World:
    """A rectangular grid of terrain cells.

    Parameters
    ----------
    width:
        Number of columns.  Must be positive.
    height:
        Number of rows.  Must be positive.
    default_terrain:
        The terrain type used to fill every cell on creation.
        Defaults to grass so a fresh world is walkable.
    """

    def __init__(
        self,
        width: int = DEFAULT_WORLD_WIDTH,
        height: int = DEFAULT_WORLD_HEIGHT,
        default_terrain: str = TerrainType.GRASS,
    ) -> None:
        if width < 1:
            raise ValueError(f"width must be >= 1, got {width}")
        if height < 1:
            raise ValueError(f"height must be >= 1, got {height}")
        if default_terrain not in TERRAIN_PROPERTIES:
            raise ValueError(
                f"unknown terrain {default_terrain!r}; "
                f"expected one of {TerrainType.ALL}"
            )
        self._width = width
        self._height = height
        # Flat row-major list: index = y * width + x.
        self._cells: List[str] = [default_terrain] * (width * height)
        self._default_terrain = default_terrain

    # ------------------------------------------------------------------ size
    @property
    def width(self) -> int:
        """Number of columns."""
        return self._width

    @property
    def height(self) -> int:
        """Number of rows."""
        return self._height

    @property
    def default_terrain(self) -> str:
        """Terrain type used for new cells."""
        return self._default_terrain

    def __len__(self) -> int:
        return self._width * self._height

    # ------------------------------------------------------------------ access
    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if (x, y) is inside the grid."""
        return 0 <= x < self._width and 0 <= y < self._height

    def get(self, x: int, y: int) -> str:
        """Return the terrain type at (x, y).

        Raises ``IndexError`` if the coordinate is out of bounds.
        """
        if not self.in_bounds(x, y):
            raise IndexError(f"({x}, {y}) is outside a {self._width}x{self._height} world")
        return self._cells[y * self._width + x]

    def set(self, x: int, y: int, terrain: str) -> None:
        """Set the terrain type at (x, y).

        Raises ``IndexError`` if the coordinate is out of bounds,
        ``ValueError`` if *terrain* is not a known terrain type.
        """
        if not self.in_bounds(x, y):
            raise IndexError(f"({x}, {y}) is outside a {self._width}x{self._height} world")
        if terrain not in TERRAIN_PROPERTIES:
            raise ValueError(f"unknown terrain {terrain!r}")
        self._cells[y * self._width + x] = terrain

    def terrain_at(self, x: int, y: int) -> str:
        """Alias for :meth:`get` — reads naturally as "terrain at (x, y)"."""
        return self.get(x, y)

    # ------------------------------------------------------------------ batch
    def fill(self, terrain: str) -> None:
        """Fill the entire grid with *terrain*.  O(n)."""
        if terrain not in TERRAIN_PROPERTIES:
            raise ValueError(f"unknown terrain {terrain!r}")
        self._cells = [terrain] * (self._width * self._height)
        self._default_terrain = terrain

    def clone(self) -> "World":
        """Return a deep copy of this world.  O(n)."""
        copy = World(self._width, self._height, self._default_terrain)
        copy._cells = list(self._cells)
        return copy

    def rows(self) -> List[List[str]]:
        """Return the grid as a list of rows (each a list of terrain strings).

        Useful for debugging and serialisation.
        """
        return [
            self._cells[y * self._width : (y + 1) * self._width]
            for y in range(self._height)
        ]

    # ------------------------------------------------------------------ properties
    def count_terrain(self, terrain: str) -> int:
        """Count how many cells hold *terrain*.  O(n)."""
        return self._cells.count(terrain)

    def __repr__(self) -> str:
        return f"World({self._width}x{self._height}, default={self._default_terrain!r})"