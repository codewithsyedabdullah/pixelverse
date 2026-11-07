"""Tests for ui/toolbar.py (Milestone A)."""

from __future__ import annotations

import pytest

from PySide6.QtWidgets import QApplication
from ui.toolbar import ToolPalette


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


class TestToolPalette:
    def test_initial_select(self, qapp):
        tp = ToolPalette()
        assert tp.active_tool() == "select"

    def test_select_other_tool(self, qapp):
        tp = ToolPalette()
        seen = []
        tp.set_on_tool_change(lambda t: seen.append(t))
        tp._select_tool("eraser")
        assert tp.active_tool() == "eraser"
        assert seen == ["eraser"]

    def test_all_tools_present(self, qapp):
        tp = ToolPalette()
        for tool_id, _label in ToolPalette.TOOLS:
            assert tool_id in tp._buttons