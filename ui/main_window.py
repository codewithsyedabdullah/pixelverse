"""Main application window for PIXELVERSE.

This is the top-level container that owns the navigation bar and the three
main regions: the left toolbar, the central world canvas, and the right
inspector.  The bottom simulation controls and collapsible panels are added
in later milestones.

MILESTONE 2 adds the world canvas (zoom, pan, grid toggle) to the central
area.  The toolbar and inspector arrive in MILESTONE 3.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config import (
    APP_NAME,
    APP_VERSION,
    DEFAULT_WORLD_HEIGHT,
    DEFAULT_WORLD_WIDTH,
    Palette,
)
from engine.world import World
from ui.canvas import WorldCanvas


class MainWindow(QMainWindow):
    """The root window of PIXELVERSE."""

    def __init__(self) -> None:
        super().__init__()
        self._world: World = World(DEFAULT_WORLD_WIDTH, DEFAULT_WORLD_HEIGHT)
        self._setup_window()
        self._setup_nav_bar()
        self._setup_central_area()
        self._setup_status_bar()

    # ------------------------------------------------------------------ setup
    def _setup_window(self) -> None:
        """Configure the window title, size and minimum size."""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1280, 820)
        self.setMinimumSize(960, 640)

    def _setup_nav_bar(self) -> None:
        """Build the top navigation bar with logo, world name and actions."""
        nav = QWidget()
        nav.setFixedHeight(48)
        nav.setStyleSheet(
            f"background-color: {Palette.BG_PANEL}; "
            f"border-bottom: 1px solid {Palette.BORDER};"
        )
        layout = QHBoxLayout(nav)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(8)

        # Logo / app name
        logo = QLabel("◆ PIXELVERSE")
        logo.setStyleSheet(
            f"color: {Palette.ACCENT_TEAL}; font-weight: bold; font-size: 15px;"
        )
        layout.addWidget(logo)

        # Current world name
        self.world_name_label = QLabel("Untitled World")
        self.world_name_label.setStyleSheet(
            f"color: {Palette.TEXT_SECONDARY}; font-size: 13px;"
        )
        layout.addWidget(self.world_name_label)

        layout.addStretch(1)

        # Zoom controls (MILESTONE 2)
        zoom_out_btn = QPushButton("−")
        zoom_out_btn.setFixedSize(28, 28)
        zoom_out_btn.setStyleSheet(self._tool_button_style())
        zoom_out_btn.clicked.connect(self._on_zoom_out)
        layout.addWidget(zoom_out_btn)

        self.zoom_label = QLabel("100%")
        self.zoom_label.setStyleSheet(
            f"color: {Palette.TEXT_SECONDARY}; font-size: 12px; min-width: 48px;"
            "text-align: center;"
        )
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.zoom_label)

        zoom_in_btn = QPushButton("+")
        zoom_in_btn.setFixedSize(28, 28)
        zoom_in_btn.setStyleSheet(self._tool_button_style())
        zoom_in_btn.clicked.connect(self._on_zoom_in)
        layout.addWidget(zoom_in_btn)

        self.grid_btn = QPushButton("Grid")
        self.grid_btn.setFixedHeight(28)
        self.grid_btn.setCheckable(True)
        self.grid_btn.setChecked(True)
        self.grid_btn.setStyleSheet(self._tool_button_style())
        self.grid_btn.clicked.connect(self._on_toggle_grid)
        layout.addWidget(self.grid_btn)

        # Application status
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(
            f"color: {Palette.ACCENT_TEAL}; font-size: 12px;"
        )
        layout.addWidget(self.status_label)

        self._nav_bar = nav

    def _setup_central_area(self) -> None:
        """Create the central area with the world canvas."""
        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Navigation bar at the top
        central_layout.addWidget(self._nav_bar)

        # World canvas
        self.canvas = WorldCanvas(self._world)
        self.canvas.zoom_changed.connect(self._on_zoom_changed)
        self.canvas.grid_toggled.connect(self._on_grid_toggled)
        self.canvas.cell_hovered.connect(self._on_cell_hovered)
        central_layout.addWidget(self.canvas)

        self.setCentralWidget(central)

    def _setup_status_bar(self) -> None:
        """Create the bottom status bar."""
        self.statusBar().showMessage(
            "PIXELVERSE ready — use the canvas to explore your world."
        )

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _tool_button_style() -> str:
        """Shared stylesheet for the small toolbar buttons."""
        return (
            f"QPushButton {{"
            f"  background-color: {Palette.BG_CARD};"
            f"  color: {Palette.TEXT_PRIMARY};"
            f"  border: 1px solid {Palette.BORDER};"
            f"  border-radius: 4px;"
            f"  padding: 2px 8px;"
            f"}}"
            f"QPushButton:hover {{"
            f"  background-color: {Palette.BG_HOVER};"
            f"}}"
            f"QPushButton:checked {{"
            f"  background-color: {Palette.ACCENT_TEAL};"
            f"  color: {Palette.BG_DEEP};"
            f"}}"
        )

    # ------------------------------------------------------------------ canvas signals
    def _on_zoom_in(self) -> None:
        self.canvas.zoom_in()

    def _on_zoom_out(self) -> None:
        self.canvas.zoom_out()

    def _on_zoom_changed(self, zoom: float) -> None:
        self.zoom_label.setText(f"{int(zoom * 100)}%")

    def _on_toggle_grid(self) -> None:
        self.canvas.set_grid_visible(self.grid_btn.isChecked())

    def _on_grid_toggled(self, visible: bool) -> None:
        self.grid_btn.setChecked(visible)
        self.status_label.setText(f"Grid {'visible' if visible else 'hidden'}")

    def _on_cell_hovered(self, x: int, y: int) -> None:
        terrain = self._world.get(x, y)
        self.status_label.setText(f"Cell ({x}, {y}) — {terrain}")
        self.statusBar().showMessage(f"Cell ({x}, {y}) — {terrain}")

    # ------------------------------------------------------------------ public API
    def set_world_name(self, name: str) -> None:
        """Update the world name shown in the navigation bar."""
        self.world_name_label.setText(name)

    def set_status(self, message: str) -> None:
        """Update the application status text."""
        self.status_label.setText(message)
        self.statusBar().showMessage(message)