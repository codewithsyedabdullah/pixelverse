"""SQLite persistence for simulation snapshots (M11).

Snapshots capture the full state of a simulation — world terrain, entities,
the environmental clock, and the statistics history — so a run can be saved,
loaded, and resumed.  All writes go through Python's :mod:`sqlite3` stdlib.
"""

from __future__ import annotations

import json
import sqlite3
from typing import List, Optional

from engine.clock import Clock
from engine.entities import Entity, Plant
from engine.simulation import Simulation, SimulationStats
from engine.world import World


SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    seed INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    world_name TEXT NOT NULL,
    world_width INTEGER NOT NULL,
    world_height INTEGER NOT NULL,
    tick INTEGER NOT NULL,
    clock_json TEXT NOT NULL,
    entities_json TEXT NOT NULL,
    stats_json TEXT NOT NULL,
    terrain_json TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_snapshots_created ON snapshots(created_at);
"""


class Snapshot:
    """A serialisable bag of simulation state."""

    def __init__(
        self,
        name: str,
        seed: int,
        world: World,
        tick: int,
        clock: Clock,
        entities: List[dict],
        stats: List[SimulationStats],
    ) -> None:
        self.name = name
        self.seed = seed
        self.world = world
        self.tick = tick
        self.clock = clock
        self.entities = entities
        self.stats = stats

    def to_row(self) -> tuple:
        return (
            self.name,
            self.seed,
            self.world.name,
            self.world.width,
            self.world.height,
            self.tick,
            json.dumps(self.clock.to_dict()),
            json.dumps(self.entities),
            json.dumps([self._stats_to_dict(s) for s in self.stats]),
            json.dumps(self.world.to_dict()["terrain"]),
        )

    @staticmethod
    def _stats_to_dict(stats: SimulationStats) -> dict:
        return {
            "tick": stats.tick,
            "populations": {k: v for k, v in stats.populations.items()},
            "total_entities": stats.total_entities,
            "plants": stats.plants,
            "fire_cells": stats.fire_cells,
            "events_handled": stats.events_handled,
        }


class Database:
    """A thin wrapper around a SQLite connection for snapshot storage."""

    def __init__(self, path: str = ":memory:") -> None:
        self.path = path
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    # ------------------------------------------------------------------ write
    def save_snapshot(self, snapshot: Snapshot) -> int:
        import datetime
        created = datetime.datetime.now(datetime.timezone.utc).isoformat()
        row = snapshot.to_row() + (created,)
        cur = self._conn.execute(
            "INSERT INTO snapshots (name, seed, world_name, world_width, "
            "world_height, tick, clock_json, entities_json, stats_json, "
            "terrain_json, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            row,
        )
        self._conn.commit()
        return cur.lastrowid

    # ------------------------------------------------------------------ read
    def load_snapshot(self, snapshot_id: int) -> Optional[Snapshot]:
        row = self._conn.execute(
            "SELECT * FROM snapshots WHERE id = ?", (snapshot_id,)
        ).fetchone()
        if row is None:
            return None
        return self._row_to_snapshot(row)

    def list_snapshots(self) -> List[sqlite3.Row]:
        return list(
            self._conn.execute(
                "SELECT id, name, seed, tick, created_at FROM snapshots "
                "ORDER BY created_at DESC"
            ).fetchall()
        )

    def delete_snapshot(self, snapshot_id: int) -> None:
        self._conn.execute(
            "DELETE FROM snapshots WHERE id = ?", (snapshot_id,)
        )
        self._conn.commit()

    def clear(self) -> None:
        self._conn.execute("DELETE FROM snapshots")
        self._conn.commit()

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _row_to_snapshot(row: sqlite3.Row) -> Snapshot:
        world_dict = json.loads(row["terrain_json"])
        # Rebuild a minimal world from the terrain grid.
        world = World(row["world_width"], row["world_height"], name=row["world_name"])
        world.from_dict({
            "width": row["world_width"],
            "height": row["world_height"],
            "name": row["world_name"],
            "seed": row["seed"],
            "terrain": world_dict,
        })
        clock = Clock.from_dict(json.loads(row["clock_json"]))
        entities = json.loads(row["entities_json"])
        stats_data = json.loads(row["stats_json"])
        stats = []
        for s in stats_data:
            st = SimulationStats()
            st.tick = s["tick"]
            for k, v in s["populations"].items():
                st.populations.put(k, v)
            st.total_entities = s["total_entities"]
            st.plants = s["plants"]
            st.fire_cells = s["fire_cells"]
            st.events_handled = s["events_handled"]
            stats.append(st)
        return Snapshot(
            name=row["name"],
            seed=row["seed"],
            world=world,
            tick=row["tick"],
            clock=clock,
            entities=entities,
            stats=stats,
        )

    def close(self) -> None:
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def snapshot_from_simulation(simulation: Simulation, name: str = "snapshot") -> Snapshot:
    """Build a Snapshot from a live Simulation."""
    entities_data = []
    for entity in simulation.entities.values():
        entities_data.append({
            "id": entity.id,
            "name": entity.name,
            "row": entity.row,
            "col": entity.col,
            "energy": entity.energy,
            "alive": entity.alive,
            "type": type(entity).__name__,
        })
    return Snapshot(
        name=name,
        seed=simulation.world.seed,
        world=simulation.world,
        tick=simulation.tick,
        clock=simulation.clock,
        entities=entities_data,
        stats=list(simulation.stats_history),
    )