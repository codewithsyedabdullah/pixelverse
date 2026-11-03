"""Tests for algorithms/cellular_automata.py."""

from __future__ import annotations

import pytest

from algorithms.cellular_automata import (
    cellular_step,
    FireSpreadRule,
    PlantGrowthRule,
    fire_spread_step,
    plant_growth_step,
)


def grid(rows):
    """Build a grid where each *row* is a string of single-character cells."""
    return [list(r) for r in rows]


def word_grid(rows):
    """Build a grid where each *row* is a list of multi-character cells."""
    return [list(r) for r in rows]


FIRE = FireSpreadRule.FIRE
FUEL = FireSpreadRule.FUEL
ASH = FireSpreadRule.ASH
PLANT = PlantGrowthRule.PLANT
WATER = PlantGrowthRule.WATER
EMPTY = "empty"


class TestCellularStep:
    def test_identity(self):
        g = grid(["abc", "def"])
        out = cellular_step(g, lambda cur, nb: cur)
        assert out == g
        assert out is not g

    def test_rule_sees_neighbours(self):
        g = grid([".#.", "..."])
        seen = []

        def rule(cur, nb):
            seen.append((cur, sorted(nb)))
            return cur

        cellular_step(g, rule)
        # Corner cell (0,0) has 3 Moore neighbours: (0,1)='#', (1,0)='.', (1,1)='.'
        assert seen[0][0] == "."
        assert sorted(seen[0][1]) == ["#", ".", "."]


class TestFireSpread:
    def test_fire_becomes_ash(self):
        assert FireSpreadRule().step(word_grid([[FIRE]])) == word_grid([[ASH]])

    def test_fuel_becomes_fire_next_to_fire(self):
        assert FireSpreadRule().step(word_grid([[FIRE, FUEL]])) == word_grid([[ASH, FIRE]])

    def test_fuel_far_from_fire(self):
        assert FireSpreadRule().step(word_grid([[FIRE, EMPTY, FUEL]])) == word_grid([[ASH, EMPTY, FUEL]])

    def test_spreads_diagonally(self):
        g = word_grid([
            [FIRE, EMPTY, EMPTY],
            [EMPTY, FUEL, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ])
        out = FireSpreadRule().step(g)
        assert out[0][0] == ASH
        assert out[1][1] == FIRE

    def test_convenience_alias(self):
        assert fire_spread_step(word_grid([[FIRE, FUEL]])) == word_grid([[ASH, FIRE]])


class TestPlantGrowth:
    def test_no_plant_no_growth(self):
        rule = PlantGrowthRule(spread=1.0)
        g = word_grid([[EMPTY, EMPTY], [EMPTY, EMPTY]])
        assert rule.step(g) == g

    def test_empty_next_to_plant_grows(self):
        rule = PlantGrowthRule(spread=1.0)
        out = rule.step(word_grid([[PLANT, EMPTY]]))
        assert out[0][1] == PLANT

    def test_plant_stays_plant(self):
        assert PlantGrowthRule(spread=1.0).step(word_grid([[PLANT]])) == word_grid([[PLANT]])

    def test_water_blocks(self):
        rule = PlantGrowthRule(spread=1.0)
        out = rule.step(word_grid([[PLANT], [WATER], [EMPTY]]))
        assert out[2][0] == EMPTY

    def test_deterministic_with_rng(self):
        import random
        g = word_grid([[PLANT, EMPTY]])
        a = PlantGrowthRule(spread=1.0, rng=random.Random(42)).step(g)
        b = PlantGrowthRule(spread=1.0, rng=random.Random(42)).step(g)
        assert a == b
        assert a[0][1] == PLANT