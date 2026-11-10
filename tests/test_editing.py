"""Tests for ui/world_config.py and canvas painting (Milestone A)."""

from __future__ import annotations

import pytest

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QApplication

from engine.world import World
from ui.canvas import WorldCanvas
from ui.world_config import WorldConfigDialog


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


class TestWorldConfigDialog:
    def test_defaults(self, qapp):
        d = WorldConfigDialog()
        name, width, height, seed = d.values()
        assert name == "Untitled World"
        assert width >= 8
        assert height >= 8
        assert seed >= 0

    def test_custom_values(self, qapp):
        d = WorldConfigDialog(name="My World", width=16, height=12, seed=7)
        d._name_edit.setText("Custom")
        d._width_spin.setValue(20)
        d._height_spin.setValue(10)
        d._seed_spin.setValue(99)
        name, width, height, seed = d.values()
        assert name == "Custom"
        assert width == 20
        assert height == 10
        assert seed == 99

    def test_validation(self, qapp):
        d = WorldConfigDialog()
        d._width_spin.setValue(4)  # below minimum
        # SpinBox clamps to its range, so the value should be 8.
        assert d._width_spin.value() >= 8


class TestCanvasPainting:
    def test_cell_at(self, qapp):
        canvas = WorldCanvas()
        canvas.set_world(World(4, 4))
        # Zoom is 1.0 so tile size is TILE_SIZE.
        from config import TILE_SIZE
        cell = canvas.cell_at(QPoint(TILE_SIZE + 2, TILE_SIZE + 2))
        assert cell == (1, 1)

    def test_cell_at_out_of_bounds(self, qapp):
        canvas = WorldCanvas()
        canvas.set_world(World(2, 2))
        from config import TILE_SIZE
        assert canvas.cell_at(QPoint(10 * TILE_SIZE, 10 * TILE_SIZE)) is None

    def test_paint_at(self, qapp):
        canvas = WorldCanvas()
        w = World(4, 4)
        canvas.set_world(w)
        canvas.set_brush_terrain("water")
        canvas.paint_at(1, 1)
        assert w.get_terrain(1, 1) == "water"
        from config import TERRAIN_PROPERTIES
        item = canvas._tile_items[(1, 1)]
        assert item.color == TERRAIN_PROPERTIES["water"]["color"]

    def test_paint_out_of_bounds(self, qapp):
        canvas = WorldCanvas()
        w = World(2, 2)
        canvas.set_world(w)
        canvas.set_brush_terrain("water")
        canvas.paint_at(10, 10)  # should not raise
        assert w.get_terrain(1, 1) == "grass"