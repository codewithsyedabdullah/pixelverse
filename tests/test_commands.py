"""Tests for engine/commands.py (Milestone A)."""

from __future__ import annotations

import pytest

from engine.commands import CommandHistory, PaintCommand, FillCommand
from engine.world import World


class TestPaintCommand:
    def test_apply_and_reverse(self):
        w = World(4, 4)
        cmd = PaintCommand(1, 1, "water")
        cmd.apply(w)
        assert w.get_terrain(1, 1) == "water"
        cmd.reverse(w)
        assert w.get_terrain(1, 1) == "grass"  # default

    def test_out_of_bounds(self):
        w = World(2, 2)
        cmd = PaintCommand(5, 5, "rock")
        cmd.apply(w)  # should not raise
        cmd.reverse(w)  # should not raise


class TestFillCommand:
    def test_fill_region(self):
        w = World(3, 3)
        cmd = FillCommand(0, 0, "water")
        cmd.apply(w)
        assert w.get_terrain(0, 0) == "water"
        assert w.get_terrain(2, 2) == "water"
        cmd.reverse(w)
        assert w.get_terrain(0, 0) == "grass"


class TestCommandHistory:
    def test_undo_redo(self):
        w = World(4, 4)
        history = CommandHistory(world=w)
        cmd = PaintCommand(0, 0, "water")
        cmd.apply(w)
        history.push(cmd)
        assert w.get_terrain(0, 0) == "water"
        undone = history.undo()
        assert undone is cmd
        assert w.get_terrain(0, 0) == "grass"
        redone = history.redo()
        assert redone is cmd
        assert w.get_terrain(0, 0) == "water"

    def test_clears_redo_on_new_command(self):
        history = CommandHistory()
        history.push(PaintCommand(0, 0, "water"))
        history.undo()
        assert history.can_redo()
        history.push(PaintCommand(1, 1, "water"))
        assert not history.can_redo()

    def test_empty(self):
        history = CommandHistory()
        assert not history.can_undo()
        assert not history.can_redo()
        assert history.undo() is None
        assert history.redo() is None

    def test_descriptions(self):
        history = CommandHistory()
        cmd = PaintCommand(0, 0, "water")
        history.push(cmd)
        assert history.undo_description() == cmd.description
        history.undo()
        assert history.redo_description() == cmd.description