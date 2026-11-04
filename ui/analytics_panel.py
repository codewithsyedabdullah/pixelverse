"""Analytics panel: population charts over simulation time (M9).

Uses matplotlib's ``Canvas`` widget to render live population charts.  The
panel subscribes to the simulation's per-tick statistics and redraws the
chart when new data arrives.
"""

from __future__ import annotations

from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QComboBox,
    QLabel,
    QCheckBox,
    QHBoxLayout,
)

from engine.simulation import SimulationStats

# Matplotlib is imported lazily so the rest of the app still works if the
# user has not installed it (the panel just becomes a stub in that case).
try:
    from matplotlib.backends.backend_qtagg import FigureCanvas
    from matplotlib.figure import Figure
    HAS_MPL = True
except Exception:  # pragma: no cover - matplotlib optional at import time
    HAS_MPL = False


class AnalyticsPanel(QWidget):
    """A widget that plots population counts over simulation ticks."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._history: List[SimulationStats] = []
        self._visible: dict[str, bool] = {}
        self._setup_ui()

    # ------------------------------------------------------------------ UI
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = QLabel("Population Analytics")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        # Series toggle row.
        toggle_row = QHBoxLayout()
        self._check_boxes: dict[str, QCheckBox] = {}
        for series in ("plants", "herbivores", "predators"):
            cb = QCheckBox(series.capitalize())
            cb.setChecked(True)
            cb.toggled.connect(self._on_toggle)
            self._check_boxes[series] = cb
            toggle_row.addWidget(cb)
        layout.addLayout(toggle_row)

        if HAS_MPL:
            self._figure = Figure(figsize=(6, 4), dpi=100)
            self._canvas = FigureCanvas(self._figure)
            self._ax = self._figure.add_subplot(111)
            self._ax.set_xlabel("Tick")
            self._ax.set_ylabel("Count")
            self._ax.set_title("Population over time")
            self._ax.grid(True, alpha=0.3)
            layout.addWidget(self._canvas, 1)
        else:
            layout.addWidget(QLabel("matplotlib not installed"))

    # ------------------------------------------------------------------ data
    def update_history(self, stats: SimulationStats) -> None:
        """Append a new statistics snapshot and refresh the chart."""
        self._history.append(stats)
        # Track which series we have seen.
        for key in stats.populations.keys():
            if key not in self._visible:
                self._visible[key] = True
        self._redraw()

    def set_history(self, history: List[SimulationStats]) -> None:
        """Replace the entire history and refresh."""
        self._history = list(history)
        self._redraw()

    def clear(self) -> None:
        self._history = []
        self._redraw()

    # ------------------------------------------------------------------ draw
    def _on_toggle(self) -> None:
        for key, cb in self._check_boxes.items():
            self._visible[key] = cb.isChecked()
        self._redraw()

    def _redraw(self) -> None:
        if not HAS_MPL or not self._history:
            return
        self._ax.clear()
        ticks = [s.tick for s in self._history]

        # Aggregate population by class name across all snapshots.
        series: dict[str, List[int]] = {}
        for s in self._history:
            for cls, count in s.populations.items():
                series.setdefault(cls, []).append(count)
        # Pad shorter series so all lines share the same x-axis.
        max_len = max((len(v) for v in series.values()), default=0)
        for name, values in series.items():
            if len(values) < max_len:
                values = values + [0] * (max_len - len(values))
            series[name] = values

        colors = {
            "Plant": "#4caf50",
            "Herbivore": "#ff9800",
            "Predator": "#f44336",
        }
        for name, values in series.items():
            if not self._visible.get(name, True):
                continue
            self._ax.plot(ticks[: len(values)], values, label=name,
                          color=colors.get(name, None))
        self._ax.set_xlabel("Tick")
        self._ax.set_ylabel("Count")
        self._ax.set_title("Population over time")
        self._ax.legend(loc="upper right")
        self._ax.grid(True, alpha=0.3)
        self._canvas.draw_idle()