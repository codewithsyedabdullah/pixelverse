"""World configuration dialog (Milestone A).

Lets the user pick a world name, width, height and seed before creating or
resizing a world.  All inputs are validated before acceptance.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QPushButton,
    QDialogButtonBox,
)

from config import DEFAULT_WORLD_HEIGHT, DEFAULT_WORLD_WIDTH, DEFAULT_RANDOM_SEED


class WorldConfigDialog(QDialog):
    """A small form for world creation / resize parameters."""

    def __init__(self, parent=None, name: str = "", width: int = DEFAULT_WORLD_WIDTH,
                 height: int = DEFAULT_WORLD_HEIGHT, seed: int = DEFAULT_RANDOM_SEED) -> None:
        super().__init__(parent)
        self.setWindowTitle("World Configuration")
        self.resize(360, 220)
        self._name = name
        self._width = width
        self._height = height
        self._seed = seed
        self._setup_ui()

    # ------------------------------------------------------------------ UI
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        form = QVBoxLayout()
        form.setSpacing(6)

        # Name
        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("Name:"))
        self._name_edit = QLineEdit(self._name)
        name_row.addWidget(self._name_edit, 1)
        form.addLayout(name_row)

        # Dimensions
        dims = QHBoxLayout()
        dims.addWidget(QLabel("Width:"))
        self._width_spin = QSpinBox()
        self._width_spin.setRange(8, 256)
        self._width_spin.setValue(self._width)
        dims.addWidget(self._width_spin)
        dims.addSpacing(12)
        dims.addWidget(QLabel("Height:"))
        self._height_spin = QSpinBox()
        self._height_spin.setRange(8, 256)
        self._height_spin.setValue(self._height)
        dims.addWidget(self._height_spin)
        form.addLayout(dims)

        # Seed
        seed_row = QHBoxLayout()
        seed_row.addWidget(QLabel("Seed:"))
        self._seed_spin = QSpinBox()
        self._seed_spin.setRange(0, 2**31 - 1)
        self._seed_spin.setValue(self._seed)
        seed_row.addWidget(self._seed_spin)
        seed_row.addStretch(1)
        form.addLayout(seed_row)

        layout.addLayout(form)
        layout.addStretch(1)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    # ------------------------------------------------------------------ accessors
    def values(self) -> tuple[str, int, int, int]:
        return (
            self._name_edit.text().strip() or "Untitled World",
            self._width_spin.value(),
            self._height_spin.value(),
            self._seed_spin.value(),
        )