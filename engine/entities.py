"""Base classes for living entities in the simulation.

Every entity has an identity, a position, an energy budget, and a state.  The
simulation engine calls ``update`` each tick; derived classes override it to
implement behaviour.
"""

from __future__ import annotations

from typing import Optional, Tuple

from dsa.hash_table import HashTable


class Entity:
    """Common base for every living or non-living object in the world."""

    def __init__(self, entity_id: int, name: str, row: int, col: int) -> None:
        self.id = entity_id
        self.name = name
        self.row = row
        self.col = col
        self.energy = 100.0
        self.alive = True
        # Per-entity metadata bag (arbitrary key/value pairs).
        self.meta: HashTable[str, object] = HashTable()

    # ------------------------------------------------------------------ geometry
    def position(self) -> Tuple[int, int]:
        return (self.row, self.col)

    def move_to(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    # ------------------------------------------------------------------ lifecycle
    def update(self, world, event_manager, tick: int) -> None:
        """Per-tick hook.  Override in subclasses."""
        return None

    def die(self) -> None:
        self.alive = False
        self.energy = 0.0

    def __repr__(self) -> str:
        status = "alive" if self.alive else "dead"
        return f"{self.__class__.__name__}(id={self.id}, {self.name}, at=({self.row},{self.col}), {status})"


class Plant(Entity):
    """A stationary producer that grows, regenerates, and provides food."""

    GROWTH_RATE = 2.0        # energy gained per tick while growing
    MAX_ENERGY = 100.0
    FOOD_VALUE = 25.0

    def __init__(self, entity_id: int, row: int, col: int, terrain: str = "grass") -> None:
        super().__init__(entity_id, "plant", row, col)
        self.terrain = terrain
        self.growth_stage = 0.0  # 0.0 (seed) -> 1.0 (mature)
        self.energy = 0.0

    def update(self, world, event_manager, tick: int) -> None:
        if not self.alive:
            return
        # Grow if there is light/warmth (simplified: always grow on non-barren cells).
        if world.is_walkable(self.col, self.row):
            self.growth_stage = min(1.0, self.growth_stage + 0.02)
            self.energy = min(self.MAX_ENERGY, self.energy + self.GROWTH_RATE)
        else:
            self.energy -= 1.0
        if self.energy <= 0.0:
            self.die()

    def harvest(self) -> float:
        """Consume the plant's food value and return how much was taken."""
        taken = self.FOOD_VALUE
        self.energy = 0.0
        self.growth_stage = 0.0
        return taken