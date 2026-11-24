
import random

from config import TerrainType


FIRE = "FIRE"
ASH = "ASH"


def _validate_grid(grid):
    if not grid or not grid[0]:
        raise ValueError("Grid cannot be empty")

    width = len(grid[0])

    if any(len(row) != width for row in grid):
        raise ValueError("All grid rows must have equal length")


def spread_fire(grid, probability=1.0, seed=None):
    """Spread fire to neighboring grass and forest cells."""
    _validate_grid(grid)

    if not 0 <= probability <= 1:
        raise ValueError("Probability must be between 0 and 1")

    rng = random.Random(seed)
    new_grid = [row[:] for row in grid]

    rows = len(grid)
    cols = len(grid[0])

    neighbors = [
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != FIRE:
                continue

            new_grid[r][c] = ASH

            for dr, dc in neighbors:
                nr = r + dr
                nc = c + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] in (
                        TerrainType.GRASS,
                        TerrainType.FOREST
                    ):
                        if rng.random() < probability:
                            new_grid[nr][nc] = FIRE

    return new_grid


def grow_plants(grid, probability=1.0, seed=None):
    """Grow grass on soil cells next to existing plants."""
    _validate_grid(grid)

    if not 0 <= probability <= 1:
        raise ValueError("Probability must be between 0 and 1")

    rng = random.Random(seed)
    new_grid = [row[:] for row in grid]

    rows = len(grid)
    cols = len(grid[0])

    neighbors = [
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != TerrainType.SOIL:
                continue

            has_plant_neighbor = any(
                0 <= r + dr < rows
                and 0 <= c + dc < cols
                and grid[r + dr][c + dc] in (
                    TerrainType.GRASS,
                    TerrainType.FOREST
                )
                for dr, dc in neighbors
            )

            if has_plant_neighbor and rng.random() < probability:
                new_grid[r][c] = TerrainType.GRASS

    return new_grid
