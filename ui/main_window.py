"""Main application window for PIXELVERSE.

This is the top-level container that owns the navigation bar and the three
main regions: the left toolbar, the central world canvas, and the right
inspector.  The bottom simulation controls and collapsible panels are added
in later milestones.

For MILESTONE 1 this file only needs to open a polished window with a
navigation bar and a status line.  It imports no simulation logic.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QStackedWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from config import APP_NAME, APP_VERSION, Palette
from ui.theme import apply_theme


class MainWindow(QMainWindow):
    """The root window of PIXELVERSE."""

    def __init__(self) -> None:
        super().__init__()
        self._setup_window()
        self._setup_theme()
        self._setup_nav_bar()
        self._setup_central_area()
        self._setup_status_bar()

    # ------------------------------------------------------------------ setup
    def _setup_window(self) -> None:
        """Configure the window title, size and minimum size."""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(1280, 820)
        self.setMinimumSize(960, 640)

    def _setup_theme(self) -> None:
        """Apply the dark palette and stylesheet."""
        apply_theme(QApplication.instance())

    def _setup_nav_bar(self) -> None:
        """Build the top navigation bar with logo, world name and actions.

        We style a plain ``QWidget`` as a nav bar and place it at the top of
        the central layout.  Using a custom widget (rather than ``QMenuBar``)
        gives us full control over spacing and lets us embed a status label
        and world name next to the logo.
        """
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
        self.world_name_label = QLabel("No world loaded")
        self.world_name_label.setStyleSheet(
            f"color: {Palette.TEXT_SECONDARY}; font-size: 13px;"
        )
        layout.addWidget(self.world_name_label)

        layout.addStretch(1)

        # Application status
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet(
            f"color: {Palette.ACCENT_TEAL}; font-size: 12px;"
        )
        layout.addWidget(self.status_label)

        self._nav_bar = nav

    def _setup_central_area(self) -> None:
        """Create the central placeholder area (canvas comes later).

        The navigation bar sits at the top; the world canvas will fill the
        rest of the space in later milestones.
        """
        central = QWidget()
        central_layout = QVBoxLayout(central)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        # Navigation bar at the top
        central_layout.addWidget(self._nav_bar)

        placeholder = QLabel("World canvas will appear here (MILESTONE 2)")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setStyleSheet(
            f"color: {Palette.TEXT_DISABLED}; font-size: 14px;"
        )
        central_layout.addWidget(placeholder)

        self.setCentralWidget(central)

    def _setup_status_bar(self) -> None:
        """Create the bottom status bar."""
        self.statusBar().showMessage("PIXELVERSE ready — create or open a world to begin.")

    # ------------------------------------------------------------------ helpers
    def set_world_name(self, name: str) -> None:
        """Update the world name shown in the navigation bar."""
        self.world_name_label.setText(name)

    def set_status(self, message: str) -> None:
        """Update the application status text."""
        self.status_label.setText(message)
        self.statusBar().showMessage(message)