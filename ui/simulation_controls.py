"""Simulation controls: run / pause / step / reset / speed (M9)."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QLabel,
)


class SimulationControls(QWidget):
    """Buttons and a speed slider for driving the simulation."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._tick = 0
        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self._on_tick)
        self._on_tick_callback = None
        self._setup_ui()

    # ------------------------------------------------------------------ UI
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = QLabel("Simulation Controls")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        self._tick_label = QLabel("Tick: 0")
        self._tick_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._tick_label)

        button_row = QHBoxLayout()
        self._run_button = QPushButton("▶ Run")
        self._run_button.clicked.connect(self.toggle_run)
        button_row.addWidget(self._run_button)

        self._step_button = QPushButton("⏭ Step")
        self._step_button.clicked.connect(self.step_once)
        button_row.addWidget(self._step_button)

        self._reset_button = QPushButton("↺ Reset")
        self._reset_button.clicked.connect(self.reset)
        button_row.addWidget(self._reset_button)

        layout.addLayout(button_row)

        speed_row = QHBoxLayout()
        speed_label = QLabel("Speed:")
        speed_row.addWidget(speed_label)
        self._speed_slider = QSlider(Qt.Horizontal)
        self._speed_slider.setRange(1, 100)
        self._speed_slider.setValue(50)
        self._speed_slider.valueChanged.connect(self._on_speed)
        speed_row.addWidget(self._speed_slider, 1)
        self._speed_value_label = QLabel("50 ms")
        speed_row.addWidget(self._speed_value_label)
        layout.addLayout(speed_row)

    # ------------------------------------------------------------------ control
    def set_on_tick(self, callback) -> None:
        self._on_tick_callback = callback

    def toggle_run(self) -> None:
        if self._timer.isActive():
            self._timer.stop()
            self._run_button.setText("▶ Run")
        else:
            self._timer.start()
            self._run_button.setText("⏸ Pause")

    def step_once(self) -> None:
        self._tick += 1
        self._tick_label.setText(f"Tick: {self._tick}")
        if self._on_tick_callback is not None:
            self._on_tick_callback(self._tick)

    def _on_tick(self) -> None:
        self.step_once()

    def _on_speed(self, value: int) -> None:
        # 1 ms .. 1000 ms, logarithmic-ish mapping from 1..100.
        interval = max(1, int(1000 / (value / 10.0)))
        self._timer.setInterval(interval)
        self._speed_value_label.setText(f"{interval} ms")

    def reset(self) -> None:
        self._timer.stop()
        self._run_button.setText("▶ Run")
        self._tick = 0
        self._tick_label.setText("Tick: 0")

    def current_tick(self) -> int:
        return self._tick