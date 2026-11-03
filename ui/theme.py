"""Application theme: dark palette and QSS stylesheet.

This module turns a default PySide6 window into a polished dark interface.
All colours live in ``config.Palette``; this module only builds the stylesheet
string and exposes helper functions for creating styled widgets.
"""

from __future__ import annotations

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

from config import Palette


def build_stylesheet() -> str:
    """Return a QSS stylesheet string for the dark theme."""
    return f"""
    QWidget {{
        background-color: {Palette.BG_DEEP};
        color: {Palette.TEXT_PRIMARY};
        font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
        font-size: 13px;
    }}
    QMainWindow {{
        background-color: {Palette.BG_DEEP};
    }}
    QMenuBar {{
        background-color: {Palette.BG_DEEP};
        color: {Palette.TEXT_PRIMARY};
    }}
    QMenuBar::item {{
        background: transparent;
        padding: 6px 10px;
    }}
    QMenuBar::item:selected {{
        background-color: {Palette.BG_HOVER};
    }}
    QStatusBar {{
        background-color: {Palette.BG_PANEL};
        color: {Palette.TEXT_SECONDARY};
        border-top: 1px solid {Palette.BORDER};
    }}
    QScrollArea {{
        background-color: transparent;
        border: none;
    }}
    QScrollBar::vertical {{
        background-color: {Palette.BG_PANEL};
        width: 10px;
    }}
    QScrollBar::vertical::handle {{
        background-color: {Palette.BORDER};
        border-radius: 5px;
    }}
    QScrollBar::vertical::handle:hover {{
        background-color: {Palette.ACCENT_TEAL};
    }}
    """


def apply_theme(app: QApplication) -> None:
    """Apply the dark palette and stylesheet to the whole application."""
    app.setApplicationName("PIXELVERSE")
    app.setOrganizationName("PIXELVERSE")
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(Palette.BG_DEEP))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(Palette.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Base, QColor(Palette.BG_PANEL))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(Palette.BG_PANEL))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(Palette.BG_CARD))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(Palette.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Text, QColor(Palette.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Button, QColor(Palette.BG_CARD))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(Palette.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(Palette.ACCENT_RED))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(Palette.ACCENT_TEAL))
    app.setPalette(palette)

    app.setStyleSheet(build_stylesheet())