"""Tests for ui/canvas.py — the QGraphicsView pixel-art renderer.

These tests use Qt's offscreen platform so they run headlessly in CI.
"""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

from config import TerrainType
from engine.world import World


@pytest.fixture(scope="module")
def qapp():
    """Create a single QApplication for all canvas tests."""
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class TestWorldCanvas:
    def test_canvas_creates_cells(self, qapp):
        from ui.canvas import WorldCanvas

        world = World(width=5, height=4)
        canvas = WorldCanvas(world)
        # One _CellItem per cell in the scene.
        from ui.canvas import _CellItem

        cells = [item for item in canvas.scene().items() if isinstance(item, _CellItem)]
        assert len(cells) == 20

    def test_initial_zoom(self, qapp):
        from ui.canvas import WorldCanvas

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        assert canvas.zoom == 1.0

    def test_zoom_in(self, qapp):
        from ui.canvas import WorldCanvas, ZOOM_STEP

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        canvas.zoom_in()
        assert canvas.zoom == 1.0 + ZOOM_STEP

    def test_zoom_out(self, qapp):
        from ui.canvas import WorldCanvas, ZOOM_STEP

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        canvas.zoom_out()
        assert canvas.zoom == 1.0 - ZOOM_STEP

    def test_zoom_clamped_min(self, qapp):
        from ui.canvas import MIN_ZOOM, WorldCanvas

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        for _ in range(20):
            canvas.zoom_out()
        assert canvas.zoom == MIN_ZOOM

    def test_zoom_clamped_max(self, qapp):
        from ui.canvas import MAX_ZOOM, WorldCanvas

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        for _ in range(20):
            canvas.zoom_in()
        assert canvas.zoom == MAX_ZOOM

    def test_zoom_reset(self, qapp):
        from ui.canvas import WorldCanvas

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        canvas.zoom_in()
        canvas.zoom_in()
        canvas.zoom_reset()
        assert canvas.zoom == 1.0

    def test_grid_visible_default(self, qapp):
        from ui.canvas import WorldCanvas

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        assert canvas.grid_visible is True

    def test_grid_toggle(self, qapp):
        from ui.canvas import WorldCanvas

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        canvas.set_grid_visible(False)
        assert canvas.grid_visible is False
        canvas.set_grid_visible(True)
        assert canvas.grid_visible is True

    def test_set_world(self, qapp):
        from ui.canvas import WorldCanvas, _CellItem

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        new_world = World(width=3, height=2)
        canvas.set_world(new_world)
        cells = [item for item in canvas.scene().items() if isinstance(item, _CellItem)]
        assert len(cells) == 6

    def test_cell_at(self, qapp):
        from ui.canvas import WorldCanvas

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        # At zoom 1.0, tile size is 16px.  Cell (2, 3) is at (32, 48).
        result = canvas.cell_at(32, 48)
        assert result == (2, 3)
        # Out of bounds returns None.
        result = canvas.cell_at(-1, -1)
        assert result is None
        result = canvas.cell_at(999, 999)
        assert result is None

    def test_zoom_signal(self, qapp):
        from ui.canvas import WorldCanvas

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        zooms = []
        canvas.zoom_changed.connect(lambda z: zooms.append(z))
        canvas.zoom_in()
        canvas.zoom_in()
        assert zooms == [1.25, 1.5]

    def test_grid_signal(self, qapp):
        from ui.canvas import WorldCanvas

        world = World(width=5, height=5)
        canvas = WorldCanvas(world)
        states = []
        canvas.grid_toggled.connect(lambda v: states.append(v))
        canvas.set_grid_visible(False)
        canvas.set_grid_visible(True)
        assert states == [False, True]

    def test_terrain_rendered(self, qapp):
        """Verify that cell colours match the terrain properties."""
        from PySide6.QtGui import QColor

        from config import TERRAIN_PROPERTIES
        from ui.canvas import WorldCanvas, _CellItem

        world = World(width=5, height=5)
        world.set(2, 2, TerrainType.WATER)
        canvas = WorldCanvas(world)
        for item in canvas.scene().items():
            if isinstance(item, _CellItem) and item.cell_x == 2 and item.cell_y == 2:
                expected = QColor(TERRAIN_PROPERTIES[TerrainType.WATER]["color"])
                actual = item.brush().color()
                assert actual == expected
                return
        pytest.fail("water cell not found in scene")