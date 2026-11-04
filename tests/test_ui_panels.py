"""Tests for the M9 UI panels (analytics, DSA lab, simulation controls)."""

from __future__ import annotations

import pytest

from PySide6.QtWidgets import QApplication

from engine.simulation import Simulation, SimulationStats
from engine.world import World
from ui.analytics_panel import AnalyticsPanel
from ui.dsa_lab import DSALabPanel
from ui.simulation_controls import SimulationControls


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def _stats(tick, populations=None):
    s = SimulationStats()
    s.tick = tick
    if populations:
        for k, v in populations.items():
            s.populations.put(k, v)
        s.total_entities = sum(populations.values())
    else:
        s.total_entities = 0
    return s


class TestAnalyticsPanel:
    def test_update_and_clear(self, qapp):
        panel = AnalyticsPanel()
        panel.update_history(_stats(1, {"Plant": 5}))
        panel.update_history(_stats(2, {"Plant": 7}))
        assert len(panel._history) == 2
        panel.clear()
        assert len(panel._history) == 0

    def test_set_history(self, qapp):
        panel = AnalyticsPanel()
        panel.set_history([_stats(1, {"Plant": 3}), _stats(2, {"Plant": 4})])
        assert len(panel._history) == 2


class TestDSALabPanel:
    def test_run_queue(self, qapp):
        panel = DSALabPanel()
        # Select "Queue" (index 0) and run.
        panel._demo_combo.setCurrentIndex(0)
        panel._run_selected()
        assert len(panel._frames) > 0
        assert panel._output.toPlainText().startswith("Queue:")

    def test_step(self, qapp):
        panel = DSALabPanel()
        panel._demo_combo.setCurrentIndex(1)  # Stack
        panel._run_selected()
        first = panel._output.toPlainText()
        panel._step()
        # Should still have content.
        assert panel._output.toPlainText()


class TestSimulationControls:
    def test_step_increments(self, qapp):
        sc = SimulationControls()
        sc.step_once()
        assert sc.current_tick() == 1
        sc.step_once()
        assert sc.current_tick() == 2

    def test_reset(self, qapp):
        sc = SimulationControls()
        sc.step_once()
        sc.step_once()
        sc.reset()
        assert sc.current_tick() == 0

    def test_callback(self, qapp):
        sc = SimulationControls()
        seen = []
        sc.set_on_tick(lambda tick: seen.append(tick))
        sc.step_once()
        assert seen == [1]