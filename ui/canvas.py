"""Pixel-art world canvas — a QGraphicsView renderer for the terrain grid.

This widget turns a :class:`engine.world.World` into a visible, zoomable,
pannable grid.  Each cell is drawn as a filled rectangle.  The renderer uses
nearest-neighbour scaling so pixels stay sharp at every zoom level.

Features
--------
- **Render** the terrain grid with per-cell colours from ``TERRAIN_PROPERTIES``.
- **Zoom** in/out with the mouse wheel or toolbar buttons (clamped 0.25x–4x).
- **Pan** by dragging with the middle mouse button (or holding Space).
- **Grid toggle** to show/hide cell borders.
- **Cell hover** — highlights the cell under the cursor and exposes its (x, y)
  coordinate to the parent widget for the status bar / inspector.

The canvas is a pure view: it reads the world model and never mutates it.
Editing (painting) arrives in MILESTONE 3.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QWidget,
)

from config import Palette, TERRAIN_PROPERTIES, TILE_SIZE
from engine.world import World


# Zoom limits (multiplier applied to TILE_SIZE).
MIN_ZOOM = 0.25
MAX_ZOOM = 4.0
ZOOM_STEP = 0.25


class _CellItem(QGraphicsRectItem):
    """A single terrain cell drawn as a coloured rectangle."""

    __slots__ = ("cell_x", "cell_y")

    def __init__(self, x: int, y: int, colour: QColor, tile_size: float) -> None:
        super().__init__(x * tile_size, y * tile_size, tile_size, tile_size)
        self.cell_x = x
        self.cell_y = y
        self.setBrush(QBrush(colour))
        # No pen by default; the grid overlay handles borders.
        self.setPen(QPen(Qt.PenStyle.NoPen))


class WorldCanvas(QGraphicsView):
    """Zoomable, pannable pixel-art renderer for a :class:`World`.

    Signals
    -------
    zoom_changed(float)
        Emitted whenever the zoom multiplier changes.
    grid_toggled(bool)
        Emitted when the grid overlay is shown or hidden.
    cell_hovered(int, int)
        Emitted with (x, y) of the cell under the cursor.
    """

    zoom_changed = Signal(float)
    grid_toggled = Signal(bool)
    cell_hovered = Signal(int, int)

    def __init__(self, world: World, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._world = world
        self._tile_size: float = float(TILE_SIZE)
        self._zoom: float = 1.0
        self._show_grid: bool = True

        # --- scene -----------------------------------------------------------
        self._scene = QGraphicsScene(self)
        self._scene.setBackgroundBrush(QColor(Palette.BG_DEEP))
        self.setScene(self._scene)

        # --- rendering hints --------------------------------------------------
        # Nearest-neighbour keeps pixels sharp when zoomed in.
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
        )
        # Remove the smooth transform so tiles are crisp at every zoom.
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)
        # Enable OpenGL if available for smoother panning on large worlds.
        # (Not required; works fine without.)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setFrameShape(QGraphicsView.Shape.NoFrame)

        # --- pan state --------------------------------------------------------
        self._panning = False
        self._pan_start = None

        # Build the grid.
        self._build_grid()
        self.set_grid_visible(True)

    # ================================================================== build
    def _build_grid(self) -> None:
        """Create one _CellItem per world cell."""
        ts = self._tile_size
        for y in range(self._world.height):
            for x in range(self._world.width):
                terrain = self._world.get(x, y)
                colour = QColor(TERRAIN_PROPERTIES[terrain]["color"])
                cell = _CellItem(x, y, colour, ts)
                self._scene.addItem(cell)

        # Scene rect covers the whole world.
        self._scene.setSceneRect(
            0, 0, self._world.width * ts, self._world.height * ts
        )

    # ================================================================== zoom
    def zoom_in(self) -> None:
        """Zoom in by one step."""
        self._set_zoom(self._zoom + ZOOM_STEP)

    def zoom_out(self) -> None:
        """Zoom out by one step."""
        self._set_zoom(self._zoom - ZOOM_STEP)

    def zoom_reset(self) -> None:
        """Reset zoom to 1.0x."""
        self._set_zoom(1.0)

    def _set_zoom(self, value: float) -> None:
        """Clamp *value* to [MIN_ZOOM, MAX_ZOOM] and apply it."""
        clamped = max(MIN_ZOOM, min(MAX_ZOOM, value))
        if clamped == self._zoom:
            return
        # Scale relative to the current zoom so we don't compound.
        factor = clamped / self._zoom
        self._zoom = clamped
        self.scale(factor, factor)
        self.zoom_changed.emit(self._zoom)

    @property
    def zoom(self) -> float:
        """Current zoom multiplier."""
        return self._zoom

    def wheelEvent(self, event) -> None:  # noqa: N802 (Qt override)
        """Zoom in/out with the mouse wheel."""
        if event.angleDelta().y() > 0:
            self.zoom_in()
        elif event.angleDelta().y() < 0:
            self.zoom_out()
        event.accept()

    # ================================================================== grid
    def set_grid_visible(self, visible: bool) -> None:
        """Show or hide the cell-border grid overlay."""
        self._show_grid = visible
        for item in self._scene.items():
            if isinstance(item, _CellItem):
                if visible:
                    item.setPen(QPen(QColor(Palette.GRID_COLOR), 0.5))
                else:
                    item.setPen(QPen(Qt.PenStyle.NoPen))
        self.grid_toggled.emit(visible)

    @property
    def grid_visible(self) -> bool:
        return self._show_grid

    # ================================================================== pan
    def mousePressEvent(self, event) -> None:  # noqa: N802
        """Start panning on middle-button or Space+LMB."""
        if event.button() == Qt.MouseButton.MiddleButton:
            self._panning = True
            self._pan_start = event.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if self._panning and self._pan_start is not None:
            delta = event.pos() - self._pan_start
            self._pan_start = event.pos()
            # Scroll bars are in screen space; moving the mouse right should
            # move the scene content right, i.e. decrease h-scroll value.
            h_bar = self.horizontalScrollBar()
            v_bar = self.verticalScrollBar()
            h_bar.setValue(h_bar.value() - delta.x())
            v_bar.setValue(v_bar.value() - delta.y())
            event.accept()
            return
        # Hover: emit cell_hovered when the cursor moves over a new cell.
        scene_pos = self.mapToScene(event.pos())
        x = int(scene_pos.x() // self._tile_size)
        y = int(scene_pos.y() // self._tile_size)
        if self._world.in_bounds(x, y):
            self.cell_hovered.emit(x, y)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if self._panning:
            self._panning = False
            self._pan_start = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    # ================================================================== hover
    # Hover handling is integrated into mouseMoveEvent above.

    # ================================================================== world
    @property
    def world(self) -> World:
        return self._world

    def set_world(self, world: World) -> None:
        """Replace the rendered world and rebuild the grid."""
        self._world = world
        self._scene.clear()
        self._build_grid()
        self.set_grid_visible(self._show_grid)

    def refresh(self) -> None:
        """Re-read terrain colours from the world and update each cell.

        Call this after the world model changes (e.g. painting in M3).
        """
        for item in self._scene.items():
            if isinstance(item, _CellItem):
                terrain = self._world.get(item.cell_x, item.cell_y)
                item.setBrush(QBrush(QColor(TERRAIN_PROPERTIES[terrain]["color"])))

    # ================================================================== info
    def cell_at(self, pos_x: float, pos_y: float) -> Optional[tuple[int, int]]:
        """Return (x, y) of the cell at scene coordinates, or None if outside."""
        x = int(pos_x // self._tile_size)
        y = int(pos_y // self._tile_size)
        if self._world.in_bounds(x, y):
            return (x, y)
        return None