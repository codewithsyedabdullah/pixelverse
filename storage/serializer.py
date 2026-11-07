"""JSON serialisation for worlds (Milestone A).

A world serialises to a plain dict that can be saved to disk and reloaded.
The format is intentionally simple so it can be inspected by hand.
"""

from __future__ import annotations

import json
from typing import Any

from engine.world import World


def world_to_dict(world: World) -> dict[str, Any]:
    """Serialise a world to a plain dict."""
    return world.to_dict()


def world_from_dict(data: dict[str, Any]) -> World:
    """Rebuild a world from a serialised dict."""
    world = World(
        width=data["width"],
        height=data["height"],
        name=data.get("name", "Untitled World"),
        seed=data.get("seed", 0),
    )
    world.from_dict(data)
    return world


def save_world(world: World, path: str) -> None:
    """Write a world to *path* as JSON."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(world_to_dict(world), fh, indent=2, sort_keys=True)


def load_world(path: str) -> World:
    """Load a world from a JSON file."""
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return world_from_dict(data)