"""Tests for engine/organisms.py (M7)."""

from __future__ import annotations

import pytest

from engine.organisms import Herbivore, Predator, EntityRegistry
from engine.entities import Plant
from engine.simulation import Simulation
from engine.world import World


class TestHerbivore:
    def test_init(self):
        h = Herbivore(1, 5, 5)
        assert h.name == "herbivore"
        assert h.energy == 60.0
        assert h.alive

    def test_starvation(self):
        h = Herbivore(1, 0, 0)
        h.energy = 1.0
        h.update(None, None, 0)
        assert not h.alive

    def test_seek_and_consume(self):
        h = Herbivore(1, 0, 0)
        h.seek(0, 0)
        h.update(None, None, 0)
        assert h.target is None
        assert h.energy > 60.0


class TestPredator:
    def test_init(self):
        p = Predator(2, 3, 3)
        assert p.name == "predator"
        assert p.energy == 80.0

    def test_starvation(self):
        p = Predator(1, 0, 0)
        p.energy = 1.0
        p.update(None, None, 0)
        assert not p.alive

    def test_attack_kills_prey(self):
        p = Predator(1, 0, 0)
        prey = Herbivore(2, 0, 0)
        p.attack(prey)
        assert not prey.alive
        assert p.energy > 80.0


class TestEntityRegistry:
    def _sim(self):
        w = World(8, 8, seed=1)
        w.generate_random()
        return Simulation(w)

    def test_typed_lookups(self):
        sim = self._sim()
        sim.spawn_plant(0, 0)
        h = Herbivore(sim._next_id, 1, 1)
        sim._next_id += 1
        sim.add_entity(h)
        p = Predator(sim._next_id, 2, 2)
        sim._next_id += 1
        sim.add_entity(p)
        reg = EntityRegistry(sim.entities)
        assert len(reg.plants()) == 1
        assert len(reg.herbivores()) == 1
        assert len(reg.predators()) == 1

    def test_near(self):
        sim = self._sim()
        h = Herbivore(sim._next_id, 5, 5)
        sim._next_id += 1
        sim.add_entity(h)
        reg = EntityRegistry(sim.entities)
        nearby = reg.near(5, 5, 2)
        assert h in nearby
        far = reg.near(0, 0, 2)
        assert h not in far

    def test_closest(self):
        sim = self._sim()
        a = Herbivore(sim._next_id, 0, 0)
        sim._next_id += 1
        sim.add_entity(a)
        b = Herbivore(sim._next_id, 5, 5)
        sim._next_id += 1
        sim.add_entity(b)
        reg = EntityRegistry(sim.entities)
        assert reg.closest(0, 0, [a, b]) is a
        assert reg.closest(5, 5, [a, b]) is b