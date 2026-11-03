"""PIXELVERSE configuration constants.

This module holds all the "knobs" of the application in one place so that
other modules never hard-code magic numbers.  Keeping everything here makes
the project easy to tune and beginner-friendly to read.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Application metadata
# ---------------------------------------------------------------------------
APP_NAME = "PIXELVERSE"
APP_VERSION = "0.1.0"
APP_ORGANIZATION = "PIXELVERSE"
APP_DESCRIPTION = "A 2D pixel-world building and ecosystem simulation."

# ---------------------------------------------------------------------------
# World dimensions (user can pick one when creating a new world)
# ---------------------------------------------------------------------------
WORLD_PRESETS = {
    "Small (40 x 30)": (40, 30),
    "Medium (60 x 40)": (60, 40),
    "Large (80 x 60)": (80, 60),
}

DEFAULT_WORLD_WIDTH = 60
DEFAULT_WORLD_HEIGHT = 40

# Tile rendering size in screen pixels at zoom level 1.0.
TILE_SIZE = 16

# ---------------------------------------------------------------------------
# Terrain types
# ---------------------------------------------------------------------------
class TerrainType:
    """The six terrain kinds that make up a world.

    Each terrain has properties that the simulation engine reads:
      - walkable: can an organism stand on this cell?
      - movement_cost: how expensive is it to cross (used as graph edge weight)?
      - blocks_movement: if True, organisms cannot enter at all.
      - provides_food: can herbivores find plants here?
      - supports_plant_growth: can plants regenerate on this cell?
      - resource_amount: how much food/resource this cell holds.
    """

    GRASS = "grass"
    WATER = "water"
    SAND = "sand"
    ROCK = "rock"
    FOREST = "forest"
    SOIL = "soil"

    ALL = (GRASS, WATER, SAND, ROCK, FOREST, SOIL)


# Per-terrain properties.  Keys are terrain names, values are property dicts.
# Movement cost doubles as the graph edge weight for A* pathfinding.
TERRAIN_PROPERTIES = {
    TerrainType.GRASS: {
        "walkable": True,
        "movement_cost": 1.0,
        "blocks_movement": False,
        "provides_food": True,
        "supports_plant_growth": True,
        "resource_amount": 8,
        "color": "#5BA46A",
    },
    TerrainType.WATER: {
        "walkable": False,
        "movement_cost": 10.0,
        "blocks_movement": True,
        "provides_food": False,
        "supports_plant_growth": False,
        "resource_amount": 0,
        "color": "#3A86C8",
    },
    TerrainType.SAND: {
        "walkable": True,
        "movement_cost": 2.0,
        "blocks_movement": False,
        "provides_food": False,
        "supports_plant_growth": False,
        "resource_amount": 0,
        "color": "#D8C48F",
    },
    TerrainType.ROCK: {
        "walkable": False,
        "movement_cost": 100.0,
        "blocks_movement": True,
        "provides_food": False,
        "supports_plant_growth": False,
        "resource_amount": 0,
        "color": "#7A7A7A",
    },
    TerrainType.FOREST: {
        "walkable": True,
        "movement_cost": 1.5,
        "blocks_movement": False,
        "provides_food": True,
        "supports_plant_growth": True,
        "resource_amount": 12,
        "color": "#3A7D4A",
    },
    TerrainType.SOIL: {
        "walkable": True,
        "movement_cost": 1.0,
        "blocks_movement": False,
        "provides_food": False,
        "supports_plant_growth": True,
        "resource_amount": 6,
        "color": "#6B4A2F",
    },
}


# ---------------------------------------------------------------------------
# Simulation timing
# ---------------------------------------------------------------------------
SIMULATION_TICK_INTERVAL_MS = 100  # how often the engine advances one tick
SIMULATION_SPEEDS = (1, 2, 4, 8, 16)  # ticks per real second when running
DEFAULT_SIMULATION_SPEED = 4

# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------
DEFAULT_RANDOM_SEED = 42

# ---------------------------------------------------------------------------
# Application colour palette (dark theme)
# ---------------------------------------------------------------------------
class Palette:
    """A sophisticated dark palette inspired by professional creative software."""

    # Backgrounds
    BG_DEEP = "#0B1220"        # deepest navy / charcoal
    BG_PANEL = "#161E2E"       # secondary panels
    BG_CARD = "#1C2740"        # cards / raised surfaces
    BG_HOVER = "#243256"       # hover state

    # Accents
    ACCENT_TEAL = "#2DD4BF"    # primary accent
    ACCENT_PURPLE = "#7C9CF5"  # secondary accent
    ACCENT_AMBER = "#FBBF24"   # warnings
    ACCENT_RED = "#F87171"     # errors / critical

    # Text
    TEXT_PRIMARY = "#E6EDF3"   # off-white
    TEXT_SECONDARY = "#94A3B8" # readable grey
    TEXT_DISABLED = "#5A6577"

    # Borders
    BORDER = "#2A3A55"

    # Entity colours (used by the canvas for organisms)
    PLANT_COLOR = "#5BA46A"
    HERBIVORE_COLOR = "#F59E0B"
    PREDATOR_COLOR = "#F87171"
    SELECTION_COLOR = "#FFFFFF"
    PATH_COLOR = "#2DD4BF"
    GRID_COLOR = "#1C2740"


# ---------------------------------------------------------------------------
# File extensions
# ---------------------------------------------------------------------------
WORLD_FILE_EXTENSION = ".pvworld"
SNAPSHOT_FILE_EXTENSION = ".pvsnap"