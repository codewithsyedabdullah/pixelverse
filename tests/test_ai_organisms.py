"""Tests for the AI-to-organism glue (M8)."""

from __future__ import annotations

import pytest

from ai.organisms import HerbivoreAI, PredatorAI, step_ai
from engine.organisms import Herbivore, Predator, EntityRegistry
from engine.entities import Plant
from engine.simulation import Simulation
from engine.world import World


class TestHerbivoreAI:
    def _sim(self):
        w = World(8, 8, seed=1)
        w.generate_random()
        return Simulation(w)

    def test_seeks_plant_when_hungry(self):
        sim = self._sim()
        plant = sim.spawn_plant(3, 3)
        h = Herbivore(sim._next_id, 0, 0)
        sim._next_id += 1
        sim.add_entity(h)
        h.energy = 5.0  # very hungry
        ai = HerbivoreAI(h)
        action = ai.decide(EntityRegistry(sim.entities))
        assert action is not None
        assert action.name == "seek_plant"
        ai.execute(action, EntityRegistry(sim.entities))
        assert h.target == (3, 3)

    def test_wanders_when_no_plants(self):
        # Use a fresh world that has not generated plants.
        sim = Simulation(World(8, 8, seed=1))
        h = Herbivore(sim._next_id, 0, 0)
        sim._next_id += 1
        sim.add_entity(h)
        ai = HerbivoreAI(h)
        action = ai.decide(EntityRegistry(sim.entities))
        assert action is not None
        assert action.name == "wander"


class TestPredatorAI:
    def _sim(self):
        w = World(8, 8, seed=1)
        w.generate_random()
        return Simulation(w)

    def test_hunts_prey_when_low_energy(self):
        sim = self._sim()
        prey = Herbivore(sim._next_id, 0, 0)
        sim._next_id += 1
        sim.add_entity(prey)
        p = Predator(sim._next_id, 5, 5)
        sim._next_id += 1
        sim.add_entity(p)
        p.energy = 10.0  # hungry
        ai = PredatorAI(p)
        action = ai.decide(EntityRegistry(sim.entities))
        assert action is not None
        assert action.name == "hunt"
        ai.execute(action, EntityRegistry(sim.entities))
        assert p.target == (0, 0)

    def test_wanders_when_no_prey(self):
        sim = Simulation(World(8, 8, seed=1))
        p = Predator(sim._next_id, 0, 0)
        sim._next_id += 1
        sim.add_entity(p)
        ai = PredatorAI(p)
        action = ai.decide(EntityRegistry(sim.entities))
        assert action is not None
        assert action.name == "wander"


class TestStepAI:
    def test_runs_without_error(self):
        sim = Simulation(World(8, 8, seed=1))
        sim.world.generate_random()
        sim.spawn_plant(0, 0)
        h = Herbivore(sim._next_id, 1, 1)
        sim._next_id += 1
        sim.add_entity(h)
        p = Predator(sim._next_id, 2, 2)
        sim._next_id += 1
        sim.add_entity(p)
        step_ai(sim)  # should not raise