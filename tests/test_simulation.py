"""Tests for the simulation engine (M6)."""

from __future__ import annotations

import copy

import pytest

from engine.world import World
from engine.entities import Entity, Plant
from engine.event_manager import Event, EventManager
from engine.simulation import Simulation, SimulationStats


# --------------------------------------------------------------------------- EventManager
class TestEventManager:
    def test_empty(self):
        em = EventManager()
        assert len(em) == 0
        assert em.dispatch() == []

    def test_fifo_within_priority(self):
        em = EventManager()
        em.begin_tick(0)
        em.enqueue(Event("a"))
        em.enqueue(Event("b"))
        em.enqueue(Event("c"))
        handled = em.dispatch()
        assert [e.type for e in handled] == ["a", "b", "c"]

    def test_priority_order(self):
        em = EventManager()
        em.begin_tick(0)
        em.enqueue(Event("low", priority=1))
        em.enqueue(Event("high", priority=10))
        em.enqueue(Event("mid", priority=5))
        handled = em.dispatch()
        assert [e.type for e in handled] == ["high", "mid", "low"]

    def test_handler_called(self):
        em = EventManager()
        seen = []
        em.register("ping", lambda e: seen.append(e.payload))
        em.begin_tick(0)
        em.enqueue(Event("ping", payload=42))
        em.dispatch()
        assert seen == [42]

    def test_future_tick_deferred(self):
        em = EventManager()
        em.begin_tick(0)
        em.enqueue_at(Event("later"), 5)
        assert len(em) == 1
        assert em.dispatch() == []  # not due yet
        em.begin_tick(5)
        assert len(em.dispatch()) == 1


# --------------------------------------------------------------------------- Simulation
class TestSimulation:
    def _make(self, seed=1):
        w = World(8, 8, seed=seed)
        w.generate_random()
        return Simulation(w)

    def test_empty_world(self):
        sim = self._make()
        stats = sim.step()
        assert isinstance(stats, SimulationStats)
        assert stats.tick == 1
        assert stats.total_entities == 0

    def test_plant_growth(self):
        sim = self._make()
        sim.spawn_plant(0, 0)
        sim.run(10)
        plant = next(e for e in sim.entities.values() if isinstance(e, Plant))
        assert plant.growth_stage > 0.0
        assert plant.energy > 0.0

    def test_plant_dies_off_terrain(self):
        sim = self._make()
        # Place the world on a non-walkable cell.
        sim.world.set_terrain(0, 0, "rock")
        sim.spawn_plant(0, 0)
        sim.run(200)
        plant = next(e for e in sim.entities.values() if isinstance(e, Plant))
        assert not plant.alive

    def test_determinism(self):
        sim_a = self._make(seed=42)
        sim_a.spawn_plant(0, 0)
        sim_a.spawn_plant(1, 0)
        sim_a.run(50)

        sim_b = self._make(seed=42)
        sim_b.spawn_plant(0, 0)
        sim_b.spawn_plant(1, 0)
        sim_b.run(50)

        # Same entity states after identical runs.
        for ea, eb in zip(sim_a.entities.values(), sim_b.entities.values()):
            assert ea.energy == pytest.approx(eb.energy)
            assert ea.growth_stage == pytest.approx(eb.growth_stage)
            assert ea.alive == eb.alive

    def test_event_dispatch_per_tick(self):
        sim = self._make()
        seen = []
        sim.event_manager.register("ping", lambda e: seen.append(e.payload))
        sim.post("ping", payload="x")
        sim.step()
        assert seen == ["x"]

    def test_stats_history(self):
        sim = self._make()
        sim.spawn_plant(0, 0)
        sim.run(5)
        assert len(sim.stats_history) == 5
        assert sim.stats_history[-1].tick == 5
        assert sim.stats_history[-1].plants == 1

    def test_reset(self):
        sim = self._make()
        sim.spawn_plant(0, 0)
        sim.run(5)
        assert len(sim.entities) == 1
        sim.reset()
        assert len(sim.entities) == 0
        assert sim.tick == 0
        assert len(sim.stats_history) == 0

    def test_entity_registry_lookup(self):
        sim = self._make()
        p = sim.spawn_plant(0, 0)
        assert sim.entities.get(p.id) is p
        assert p.id in sim.entities
        assert sim.entities.get(99999) is None