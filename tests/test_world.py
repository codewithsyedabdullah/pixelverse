"""Tests for engine/world.py — the terrain grid model."""

from __future__ import annotations

import pytest

from config import TerrainType
from engine.world import World


class TestWorldCreation:
    def test_default_size(self):
        w = World()
        assert w.width == 60
        assert w.height == 40
        assert len(w) == 60 * 40

    def test_custom_size(self):
        w = World(width=10, height=5)
        assert w.width == 10
        assert w.height == 5
        assert len(w) == 50

    def test_default_terrain_is_grass(self):
        w = World()
        assert w.default_terrain == TerrainType.GRASS
        assert w.get(0, 0) == TerrainType.GRASS
        assert w.get(w.width - 1, w.height - 1) == TerrainType.GRASS

    def test_custom_default_terrain(self):
        w = World(width=5, height=5, default_terrain=TerrainType.SOIL)
        assert w.get(2, 2) == TerrainType.SOIL

    def test_invalid_width(self):
        with pytest.raises(ValueError):
            World(width=0, height=5)

    def test_invalid_height(self):
        with pytest.raises(ValueError):
            World(width=5, height=0)

    def test_invalid_default_terrain(self):
        with pytest.raises(ValueError):
            World(width=5, height=5, default_terrain="lava")


class TestWorldAccess:
    def test_get_and_set(self):
        w = World(width=5, height=5)
        assert w.get(0, 0) == TerrainType.GRASS
        w.set(2, 3, TerrainType.WATER)
        assert w.get(2, 3) == TerrainType.WATER

    def test_get_out_of_bounds(self):
        w = World(width=5, height=5)
        with pytest.raises(IndexError):
            w.get(-1, 0)
        with pytest.raises(IndexError):
            w.get(5, 0)
        with pytest.raises(IndexError):
            w.get(0, -1)
        with pytest.raises(IndexError):
            w.get(0, 5)

    def test_set_out_of_bounds(self):
        w = World(width=5, height=5)
        with pytest.raises(IndexError):
            w.set(-1, 0, TerrainType.WATER)
        with pytest.raises(IndexError):
            w.set(5, 0, TerrainType.WATER)

    def test_set_invalid_terrain(self):
        w = World(width=5, height=5)
        with pytest.raises(ValueError):
            w.set(0, 0, "lava")

    def test_terrain_at_alias(self):
        w = World(width=5, height=5)
        w.set(1, 1, TerrainType.FOREST)
        assert w.terrain_at(1, 1) == TerrainType.FOREST
        assert w.terrain_at(1, 1) == w.get(1, 1)

    def test_in_bounds(self):
        w = World(width=5, height=3)
        assert w.in_bounds(0, 0)
        assert w.in_bounds(4, 2)
        assert not w.in_bounds(-1, 0)
        assert not w.in_bounds(5, 0)
        assert not w.in_bounds(0, -1)
        assert not w.in_bounds(0, 3)


class TestWorldBatch:
    def test_fill(self):
        w = World(width=5, height=5)
        w.fill(TerrainType.WATER)
        for y in range(5):
            for x in range(5):
                assert w.get(x, y) == TerrainType.WATER
        assert w.default_terrain == TerrainType.WATER

    def test_fill_invalid_terrain(self):
        w = World(width=5, height=5)
        with pytest.raises(ValueError):
            w.fill("lava")

    def test_clone_is_independent(self):
        w = World(width=5, height=5)
        w.set(0, 0, TerrainType.ROCK)
        clone = w.clone()
        assert clone.get(0, 0) == TerrainType.ROCK
        clone.set(0, 0, TerrainType.WATER)
        assert w.get(0, 0) == TerrainType.ROCK
        assert clone.get(0, 0) == TerrainType.WATER

    def test_rows(self):
        w = World(width=3, height=2)
        w.set(0, 0, TerrainType.WATER)
        w.set(2, 1, TerrainType.SAND)
        rows = w.rows()
        assert len(rows) == 2
        assert rows[0] == [TerrainType.WATER, TerrainType.GRASS, TerrainType.GRASS]
        assert rows[1] == [TerrainType.GRASS, TerrainType.GRASS, TerrainType.SAND]


class TestWorldProperties:
    def test_count_terrain(self):
        w = World(width=4, height=4)
        w.set(0, 0, TerrainType.WATER)
        w.set(1, 0, TerrainType.WATER)
        assert w.count_terrain(TerrainType.WATER) == 2
        assert w.count_terrain(TerrainType.GRASS) == 14

    def test_repr(self):
        w = World(width=5, height=3)
        assert "5x3" in repr(w)
        assert "grass" in repr(w)