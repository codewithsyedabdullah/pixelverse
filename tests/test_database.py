"""Tests for storage/database.py (M11)."""

from __future__ import annotations

import os
import tempfile

import pytest

from engine.simulation import Simulation
from engine.world import World
from storage.database import Database, Snapshot, snapshot_from_simulation


@pytest.fixture
def tmp_db():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.db")
        db = Database(path)
        yield db
        db.close()


class TestDatabase:
    def test_save_and_load_roundtrip(self, tmp_db):
        sim = Simulation(World(8, 8, seed=42, name="Roundtrip"))
        sim.world.generate_random()
        sim.spawn_plant(0, 0)
        sim.run(5)
        snap = snapshot_from_simulation(sim, name="test")
        snap_id = tmp_db.save_snapshot(snap)
        loaded = tmp_db.load_snapshot(snap_id)
        assert loaded is not None
        assert loaded.name == "test"
        assert loaded.tick == 5
        assert loaded.clock.day == sim.clock.day
        assert loaded.world.width == 8

    def test_list_snapshots(self, tmp_db):
        sim = Simulation(World(4, 4, seed=1))
        sim.run(2)
        tmp_db.save_snapshot(snapshot_from_simulation(sim, name="a"))
        sim.run(2)
        tmp_db.save_snapshot(snapshot_from_simulation(sim, name="b"))
        rows = tmp_db.list_snapshots()
        assert len(rows) == 2

    def test_delete(self, tmp_db):
        sim = Simulation(World(4, 4, seed=1))
        tmp_db.save_snapshot(snapshot_from_simulation(sim, name="x"))
        rows = tmp_db.list_snapshots()
        assert len(rows) == 1
        tmp_db.delete_snapshot(rows[0]["id"])
        assert len(tmp_db.list_snapshots()) == 0

    def test_clear(self, tmp_db):
        sim = Simulation(World(4, 4, seed=1))
        tmp_db.save_snapshot(snapshot_from_simulation(sim, name="x"))
        tmp_db.save_snapshot(snapshot_from_simulation(sim, name="y"))
        tmp_db.clear()
        assert len(tmp_db.list_snapshots()) == 0

    def test_context_manager(self):
        with tempfile.TemporaryDirectory() as tmp:
            with Database(os.path.join(tmp, "test.db")) as db:
                sim = Simulation(World(4, 4, seed=1))
                db.save_snapshot(snapshot_from_simulation(sim, name="ctx"))
                assert len(db.list_snapshots()) == 1