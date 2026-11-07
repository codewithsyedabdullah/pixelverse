"""Left vertical toolbar for world editing (Milestone A).

Provides tool buttons: select, terrain brush, eraser, fill, water, plant,
animal, object, inspect.  The active tool determines how canvas clicks are
interpreted.
"""

from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QButtonGroup,
    QGridLayout,
)

from config import Palette


class ToolPalette(QWidget):
    """A vertical strip of tool buttons."""

    TOOLS = (
        ("select", "Select"),
        ("terrain", "Terrain"),
        ("eraser", "Eraser"),
        ("fill", "Fill"),
        ("water", "Water"),
        ("plant", "Plant"),
        ("animal", "Animal"),
        ("object", "Object"),
        ("inspect", "Inspect"),
    )

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._active_tool = "select"
        self._on_tool_change: Optional[Callable[[str], None]] = None
        self._setup_ui()

    # ------------------------------------------------------------------ UI
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        title = QLabel("Tools")
        title.setStyleSheet(
            f"color: {Palette.ACCENT_TEAL}; font-weight: bold; font-size: 13px;"
        )
        layout.addWidget(title)

        self._button_group = QButtonGroup(self)
        self._buttons: dict[str, QPushButton] = {}
        grid = QGridLayout()
        grid.setHorizontalSpacing(2)
        grid.setVerticalSpacing(2)
        col = 0
        for tool_id, label in self.TOOLS:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setChecked(tool_id == "select")
            btn.clicked.connect(lambda _checked, t=tool_id: self._select_tool(t))
            self._button_group.addButton(btn)
            self._buttons[tool_id] = btn
            grid.addWidget(btn, 0, col)
            col += 1
        layout.addLayout(grid)
        layout.addStretch(1)

    # ------------------------------------------------------------------ tool
    def _select_tool(self, tool_id: str) -> None:
        self._active_tool = tool_id
        for tid, btn in self._buttons.items():
            btn.setChecked(tid == tool_id)
        if self._on_tool_change is not None:
            self._on_tool_change(tool_id)

    def set_on_tool_change(self, callback: Callable[[str], None]) -> None:
        self._on_tool_change = callback

    def active_tool(self) -> str:
        return self._active_tool