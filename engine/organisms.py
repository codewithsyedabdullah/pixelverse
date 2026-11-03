"""Living organisms for the PIXELVERSE simulation (M7).

Herbivores seek plants, predators chase herbivores, and both flee when
endangered.  The :class:`EntityRegistry` wraps the simulation's hash-table
entity store with convenience lookups.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from engine.entities import Entity, Plant


def _manhattan(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Herbivore(Entity):
    """A plant-eating organism that wanders, seeks food, and flees predators."""

    SIGHT_RADIUS = 6
    ENERGY_COST = 1.0
    STARVE_THRESHOLD = 10.0

    def __init__(self, entity_id: int, row: int, col: int) -> None:
        super().__init__(entity_id, "herbivore", row, col)
        self.energy = 60.0
        self.target: Optional[Tuple[int, int]] = None

    def update(self, world, event_manager, tick: int) -> None:
        if not self.alive:
            return
        self.energy -= self.ENERGY_COST
        if self.energy <= 0.0:
            self.die()
            return
        # Simplified behaviour: stay put if no target; the simulation
        # engine handles actual movement via events.
        if self.target is not None:
            tr, tc = self.target
            if (tr, tc) == (self.row, self.col):
                self.target = None
                self.energy += 20.0

    def seek(self, row: int, col: int) -> None:
        self.target = (row, col)

    def flee_from(self, predator_row: int, predator_col: int) -> None:
        dr = self.row - predator_row
        dc = self.col - predator_col
        self.row += 1 if dr > 0 else (-1 if dr < 0 else 0)
        self.col += 1 if dc > 0 else (-1 if dc < 0 else 0)


class Predator(Entity):
    """A meat-eating organism that hunts herbivores and starves without food."""

    SIGHT_RADIUS = 8
    ENERGY_COST = 1.2
    STARVE_THRESHOLD = 15.0
    HUNT_ENERGY_GAIN = 40.0

    def __init__(self, entity_id: int, row: int, col: int) -> None:
        super().__init__(entity_id, "predator", row, col)
        self.energy = 80.0
        self.target: Optional[Tuple[int, int]] = None

    def update(self, world, event_manager, tick: int) -> None:
        if not self.alive:
            return
        self.energy -= self.ENERGY_COST
        if self.energy <= 0.0:
            self.die()
            return
        if self.target is not None:
            tr, tc = self.target
            if (tr, tc) == (self.row, self.col):
                self.target = None
                self.energy += self.HUNT_ENERGY_GAIN

    def seek(self, row: int, col: int) -> None:
        self.target = (row, col)

    def attack(self, prey: Entity) -> None:
        prey.die()
        self.energy += self.HUNT_ENERGY_GAIN


class EntityRegistry:
    """Convenience wrapper around the simulation's hash-table entity store.

    Provides typed lookups (plants, herbivores, predators) and spatial
    queries used by the AI decision maker.
    """

    def __init__(self, entities) -> None:
        self._entities = entities

    def get(self, entity_id: int) -> Optional[Entity]:
        return self._entities.get(entity_id)

    def all(self) -> List[Entity]:
        return list(self._entities.values())

    def plants(self) -> List[Plant]:
        return [e for e in self._entities.values() if isinstance(e, Plant)]

    def herbivores(self) -> List[Herbivore]:
        return [e for e in self._entities.values() if isinstance(e, Herbivore)]

    def predators(self) -> List[Predator]:
        return [e for e in self._entities.values() if isinstance(e, Predator)]

    def near(self, row: int, col: int, radius: int) -> List[Entity]:
        out: List[Entity] = []
        for e in self._entities.values():
            if not e.alive:
                continue
            if abs(e.row - row) <= radius and abs(e.col - col) <= radius:
                out.append(e)
        return out

    def closest(self, row: int, col: int, entities: List[Entity]) -> Optional[Entity]:
        best: Optional[Entity] = None
        best_dist = -1
        for e in entities:
            if not e.alive:
                continue
            d = _manhattan((row, col), (e.row, e.col))
            if best is None or d < best_dist:
                best = e
                best_dist = d
        return best

    def __len__(self) -> int:
        return len(self._entities)