"""PIXELVERSE engine package — world, entities, events and simulation."""

from __future__ import annotations

from .world import World
from .entities import Entity, Plant
from .event_manager import Event, EventManager
from .simulation import Simulation, SimulationStats

__all__ = [
    "World",
    "Entity",
    "Plant",
    "Event",
    "EventManager",
    "Simulation",
    "SimulationStats",
]