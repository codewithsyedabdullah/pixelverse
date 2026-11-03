"""The simulation engine: a deterministic tick loop over a world + entities.

The engine owns the world, the entity registry, and the event queue.  Each
tick it:

1. Dispatches events (high-priority first, FIFO within a priority).
2. Updates every alive entity.
3. Runs cellular-automaton rules (fire spread, plant growth).
4. Records statistics.

The engine is deterministic: with the same seed and the same initial world +
entity set, repeated runs produce identical results.
"""

from __future__ import annotations

from typing import Iterator, List, Optional

from dsa.hash_table import HashTable
from dsa.queue import Queue

from engine.entities import Entity, Plant
from engine.event_manager import Event, EventManager
from engine.world import World
from algorithms.cellular_automata import FireSpreadRule, PlantGrowthRule


class SimulationStats:
    """Per-tick aggregate statistics for the analytics panel (M9)."""

    def __init__(self) -> None:
        self.tick = 0
        self.populations: HashTable[str, int] = HashTable()
        self.total_entities = 0
        self.plants = 0
        self.fire_cells = 0
        self.events_handled = 0

    def snapshot(self) -> "SimulationStats":
        s = SimulationStats()
        s.tick = self.tick
        s.populations = HashTable({k: v for k, v in self.populations.items()})
        s.total_entities = self.total_entities
        s.plants = self.plants
        s.fire_cells = self.fire_cells
        s.events_handled = self.events_handled
        return s


class Simulation:
    """Drives the world, entities and events forward one tick at a time."""

    def __init__(self, world: World, rng_seed: Optional[int] = None) -> None:
        self.world = world
        self.tick = 0
        self.running = False
        self.event_manager = EventManager()
        self.entities: HashTable[int, Entity] = HashTable()
        self._next_id = 1
        self.stats_history: List[SimulationStats] = []
        self.fire_rule = FireSpreadRule()
        self.plant_rule = PlantGrowthRule(spread=0.25)
        # Terrain grid used by cellular rules (separate from the world terrain
        # so fire can spread over walkable cells).
        self._ca_grid: List[List[str]] = [
            [world.get_terrain(c, r) for c in range(world.width)]
            for r in range(world.height)
        ]

    # ------------------------------------------------------------------ entities
    def add_entity(self, entity: Entity) -> None:
        if entity.id == 0:
            entity.id = self._next_id
            self._next_id += 1
        self.entities.put(entity.id, entity)

    def spawn_plant(self, col: int, row: int, terrain: str = "grass") -> Plant:
        plant = Plant(self._next_id, row, col, terrain)
        self._next_id += 1
        self.entities.put(plant.id, plant)
        return plant

    def entities_at(self, col: int, row: int) -> List[Entity]:
        out: List[Entity] = []
        for e in self.entities.values():
            if e.alive and e.col == col and e.row == row:
                out.append(e)
        return out

    # ------------------------------------------------------------------ events
    def post(self, event_type: str, payload=None, priority: int = 0) -> None:
        self.event_manager.enqueue(Event(event_type, payload, priority))

    # ------------------------------------------------------------------ tick
    def step(self) -> SimulationStats:
        """Advance the simulation by exactly one tick."""
        self.tick += 1
        self.event_manager.begin_tick(self.tick)

        # 1. Dispatch events.
        handled = self.event_manager.dispatch()
        events_handled = len(handled)

        # 2. Update entities.
        for entity in list(self.entities.values()):
            if entity.alive:
                entity.update(self.world, self.event_manager, self.tick)

        # 3. Cellular automaton rules.
        self._ca_grid = self.plant_rule.step(self._ca_grid)
        self._ca_grid = self.fire_rule.step(self._ca_grid)

        # 4. Statistics.
        stats = SimulationStats()
        stats.tick = self.tick
        stats.events_handled = events_handled
        populations: HashTable[str, int] = HashTable()
        plants = 0
        fire_cells = 0
        for entity in self.entities.values():
            if entity.alive:
                cls = type(entity).__name__
                populations.put(cls, populations.get(cls, 0) + 1)
                if isinstance(entity, Plant):
                    plants += 1
        for row in self._ca_grid:
            for cell in row:
                if cell == FireSpreadRule.FIRE:
                    fire_cells += 1
        stats.populations = populations
        stats.total_entities = sum(populations.values())
        stats.plants = plants
        stats.fire_cells = fire_cells
        self.stats_history.append(stats)
        return stats

    def run(self, ticks: int = 1) -> List[SimulationStats]:
        """Run *ticks* steps and return the per-tick stats."""
        out: List[SimulationStats] = []
        for _ in range(ticks):
            out.append(self.step())
        return out

    # ------------------------------------------------------------------ control
    def pause(self) -> None:
        self.running = False

    def resume(self) -> None:
        self.running = True

    def reset(self) -> None:
        """Reset to a clean state (keeps the world)."""
        self.tick = 0
        self.running = False
        self.event_manager.clear()
        self.entities = HashTable()
        self._next_id = 1
        self.stats_history = []
        self._ca_grid = [
            [self.world.get_terrain(c, r) for c in range(self.world.width)]
            for r in range(self.world.height)
        ]

    # ------------------------------------------------------------------ iteration
    def __len__(self) -> int:
        return len(self.entities)