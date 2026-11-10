"""World canvas: QGraphicsView pixel-art renderer with zoom and pan.

Renders the world grid as crisp tiles.  Uses nearest-neighbour scaling so
pixels stay sharp at any zoom level.  Contains NO simulation logic.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QRectF, QPoint
from PySide6.QtGui import QColor, QPaintEvent, QMouseEvent, QWheelEvent, QPainter
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem

from config import Palette, TILE_SIZE, TERRAIN_PROPERTIES
from engine.world import World


class TileItem(QGraphicsItem):
    """A single terrain tile drawn as a solid colour with a border."""

    def __init__(self, col: int, row: int, color: str, size: float) -> None:
        super().__init__()
        self.col = col
        self.row = row
        self.color = color
        self.size = size
        self._selected = False

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.color))
        painter.drawRect(0, 0, self.size, self.size)
        if self._selected:
            painter.setPen(QColor(Palette.SELECTION_COLOR))
            painter.setBrush(Qt.NoPen)
            painter.drawRect(1, 1, self.size - 2, self.size - 2)

    def set_selected(self, selected: bool) -> None:
        self._selected = selected
        self.update()


class WorldCanvas(QGraphicsView):
    """A zoomable, pannable view of the world grid."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self._world: World | None = None
        self._tile_items: dict[tuple[int, int], TileItem] = {}
        self._zoom = 1.0
        self._show_grid = True
        self._selected_cell: tuple[int, int] | None = None
        self._panning = False
        self._last_mouse = QPoint()
        self._active_tool = "select"
        self._brush_terrain = "grass"

        self.setRenderHint(QPainter.Antialiasing, False)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    # ------------------------------------------------------------------ world
    def set_world(self, world: World) -> None:
        """Load a world and redraw all tiles."""
        self._world = world
        self._tile_items.clear()
        self._scene.clear()
        self._selected_cell = None
        for col, row, terrain in world.iter_cells():
            self._add_tile(col, row, terrain)
        self._fit_view()

    def _add_tile(self, col: int, row: int, terrain: str) -> None:
        color = TERRAIN_PROPERTIES[terrain]["color"]
        size = TILE_SIZE * self._zoom
        item = TileItem(col, row, color, size)
        self._scene.addItem(item)
        item.setPos(col * size, row * size)
        self._tile_items[(col, row)] = item

    def _fit_view(self) -> None:
        if self._world is None:
            return
        w = self._world.width * TILE_SIZE * self._zoom
        h = self._world.height * TILE_SIZE * self._zoom
        self._scene.setSceneRect(QRectF(0, 0, w, h))

    # ------------------------------------------------------------------ zoom
    def zoom_in(self) -> None:
        self._set_zoom(self._zoom * 1.2)

    def zoom_out(self) -> None:
        self._set_zoom(self._zoom / 1.2)

    def _set_zoom(self, zoom: float) -> None:
        self._zoom = max(0.25, min(4.0, zoom))
        self._redraw_tiles()
        self._fit_view()

    def _redraw_tiles(self) -> None:
        if self._world is None:
            return
        size = TILE_SIZE * self._zoom
        for (col, row), item in self._tile_items.items():
            item.size = size
            item.setPos(col * size, row * size)
        self._scene.update()

    # ------------------------------------------------------------------ grid
    def toggle_grid(self) -> None:
        self._show_grid = not self._show_grid
        self.update()

    # ------------------------------------------------------------------ events
    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            self._panning = True
            self._last_mouse = event.position().toPoint()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
        elif event.button() == Qt.LeftButton and self._world is not None:
            cell = self.cell_at(event.position().toPoint())
            if cell is not None and self._active_tool in (
                "terrain", "eraser", "water", "plant", "animal", "object"
            ):
                self.paint_at(cell[0], cell[1])
                event.accept()
                return
            super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.RightButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._panning:
            delta = event.position().toPoint() - self._last_mouse
            self._last_mouse = event.position().toPoint()
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta.x()
            )
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta.y()
            )
            event.accept()
        else:
            super().mouseMoveEvent(event)

    # ------------------------------------------------------------------ editing
    def cell_at(self, pos: QPoint) -> tuple[int, int] | None:
        """Return the (col, row) of the world cell under *pos*, or None."""
        if self._world is None:
            return None
        size = TILE_SIZE * self._zoom
        col = int(pos.x() / size)
        row = int(pos.y() / size)
        if 0 <= col < self._world.width and 0 <= row < self._world.height:
            return (col, row)
        return None

    def set_active_tool(self, tool: str) -> None:
        self._active_tool = tool

    def set_brush_terrain(self, terrain: str) -> None:
        self._brush_terrain = terrain

    def _tool_brush(self) -> str:
        """Map the active tool to a terrain brush."""
        if self._active_tool == "eraser":
            return "grass"
        if self._active_tool == "water":
            return "water"
        if self._active_tool == "plant":
            return "grass"  # plants are entities; terrain stays grass
        if self._active_tool == "animal":
            return "grass"
        if self._active_tool == "object":
            return "grass"
        return self._brush_terrain

    def paint_at(self, col: int, row: int) -> None:
        """Paint a single cell with the current brush terrain."""
        if self._world is None:
            return
        if not (0 <= col < self._world.width and 0 <= row < self._world.height):
            return
        terrain = getattr(self, "_brush_terrain", None)
        if terrain is None:
            return
        self._world.set_terrain(col, row, terrain)
        item = self._tile_items.get((col, row))
        if item is not None:
            from config import TERRAIN_PROPERTIES
            item.color = TERRAIN_PROPERTIES[terrain]["color"]
            item.update()