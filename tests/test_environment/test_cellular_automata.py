from config import TerrainType
from algorithms.cellular_automata import (
    FIRE,
    ASH,
    spread_fire,
    grow_plants,
)


def test_fire_spreads_to_neighbors():
    grid = [
        [TerrainType.GRASS, FIRE, TerrainType.SOIL],
        [TerrainType.SOIL, TerrainType.GRASS, TerrainType.SOIL],
    ]

    result = spread_fire(grid, probability=1.0)

    assert result[0][1] == ASH
    assert result[0][0] == FIRE
    assert result[1][1] == FIRE


def test_fire_does_not_spread_to_soil():
    grid = [[FIRE, TerrainType.SOIL]]
    result = spread_fire(grid, probability=1.0)

    assert result[0][1] == TerrainType.SOIL


def test_plant_grows_near_grass():
    grid = [[TerrainType.GRASS, TerrainType.SOIL]]
    result = grow_plants(grid, probability=1.0)

    assert result[0][1] == TerrainType.GRASS


def test_plant_does_not_grow_without_neighbor():
    grid = [[TerrainType.SOIL, TerrainType.SOIL]]
    result = grow_plants(grid)

    assert result == grid


def test_original_grid_is_not_modified():
    grid = [[FIRE, TerrainType.GRASS]]
    original = [row[:] for row in grid]

    spread_fire(grid)

    assert grid == original


def test_invalid_probability():
    grid = [[TerrainType.GRASS]]

    try:
        spread_fire(grid, probability=2.0)
        assert False
    except ValueError:
        pass


def test_empty_grid():
    try:
        grow_plants([])
        assert False
    except ValueError:
        pass
