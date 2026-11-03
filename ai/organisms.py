"""Glues the AI behaviour module (FSM + utility AI) onto living organisms.

This module is intentionally small: it shows how the from-scratch AI in
``ai.behaviour`` drives the Herbivore/Predator classes each tick.  The
simulation engine calls :func:`step_ai` once per tick after entity updates.
"""

from __future__ import annotations

from typing import List, Optional

from ai.behaviour import Action, UtilityAI
from engine.organisms import EntityRegistry, Herbivore, Predator


def _distance(a_row, a_col, b_row, b_col):
    return abs(a_row - b_row) + abs(a_col - b_col)


class HerbivoreAI:
    """Utility-AI controller for a single herbivore.

    Candidates each tick:
      * ``"seek_plant"`` — move toward the nearest plant.
      * ``"wander"``     — drift randomly.
    """

    def __init__(self, herbivore: Herbivore) -> None:
        self.herbivore = herbivore
        self.utility = UtilityAI()
        self.utility.add_scorer(self._score_seek_plant)
        self.utility.add_scorer(self._score_wander)

    def _score_seek_plant(self, action: Action, ctx) -> float:
        # Neutral (1.0) for actions we don't score; the product combiner
        # then only multiplies the relevant scorer's value.
        if action.name != "seek_plant":
            return 1.0
        plants = ctx["plants"]
        if not plants:
            return 0.0
        hunger = 1.0 - min(1.0, self.herbivore.energy / 60.0)
        return hunger

    def _score_wander(self, action: Action, ctx) -> float:
        if action.name != "wander":
            return 1.0
        if ctx["plants"]:
            return 0.0
        return 1.0

    def decide(self, registry: EntityRegistry) -> Optional[Action]:
        candidates = [
            Action("seek_plant"),
            Action("wander"),
        ]
        ctx = {"plants": registry.plants()}
        return self.utility.evaluate(candidates, ctx)

    def execute(self, action: Action, registry: EntityRegistry) -> None:
        h = self.herbivore
        if action.name == "seek_plant":
            plants = registry.plants()
            if not plants:
                return
            nearest = min(
                plants,
                key=lambda p: _distance(p.row, p.col, h.row, h.col),
            )
            h.seek(nearest.row, nearest.col)
        elif action.name == "wander":
            h.target = None


class PredatorAI:
    """Utility-AI controller for a single predator.

    Candidates each tick:
      * ``"hunt"``     — move toward the nearest herbivore.
      * ``"wander"``   — drift when no prey is visible.
    """

    def __init__(self, predator: Predator) -> None:
        self.predator = predator
        self.utility = UtilityAI()
        self.utility.add_scorer(self._score_hunt)
        self.utility.add_scorer(self._score_wander)

    def _score_hunt(self, action: Action, ctx) -> float:
        if action.name != "hunt":
            return 1.0
        prey = ctx["prey"]
        if not prey:
            return 0.0
        return 1.0 - min(1.0, self.predator.energy / 80.0)

    def _score_wander(self, action: Action, ctx) -> float:
        if action.name != "wander":
            return 1.0
        if ctx["prey"]:
            return 0.0
        return 1.0

    def decide(self, registry: EntityRegistry) -> Optional[Action]:
        candidates = [Action("hunt"), Action("wander")]
        ctx = {"prey": registry.herbivores()}
        return self.utility.evaluate(candidates, ctx)

    def execute(self, action: Action, registry: EntityRegistry) -> None:
        p = self.predator
        if action.name == "hunt":
            prey = registry.herbivores()
            if not prey:
                return
            nearest = min(
                prey,
                key=lambda h: _distance(h.row, h.col, p.row, p.col),
            )
            p.seek(nearest.row, nearest.col)
        elif action.name == "wander":
            p.target = None


def step_ai(simulation) -> None:
    """Run one AI decision cycle for every controlled organism."""
    registry = EntityRegistry(simulation.entities)
    for entity in list(simulation.entities.values()):
        if isinstance(entity, Herbivore) and entity.alive:
            ai = HerbivoreAI(entity)
            action = ai.decide(registry)
            if action is not None:
                ai.execute(action, registry)
        elif isinstance(entity, Predator) and entity.alive:
            ai = PredatorAI(entity)
            action = ai.decide(registry)
            if action is not None:
                ai.execute(action, registry)