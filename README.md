# PIXELVERSE

> A polished 2D pixel-world building and ecosystem simulation application.
>
> BSCS Academic Project — Data Structures and Algorithms (DSA) + Artificial Intelligence (AI).

## What is PIXELVERSE?

PIXELVERSE is three products fused into one desktop application:

1. **A world-building studio** — paint terrain, place organisms, zoom/pan, undo/redo, save/load.
2. **A living ecosystem simulation** — a tick-based engine where plants, herbivores and predators eat, move, flee, chase, reproduce and die, driven by *real simulation rules*, not random animation.
3. **An interactive DSA/AI laboratory** — every data structure and algorithm is your own Python implementation, and the app visualises them in real time.

The academic focus is **DSA + AI**. The simulation is legitimately built on custom graph traversal, priority queues, hash tables, linked lists, finite-state machines and utility AI — not on a game engine or external library.

## Features

- Create, paint and save custom worlds (grass, water, sand, rock, forest, soil).
- Configurable dimensions: 40x30, 60x40, 80x60.
- Crisp pixel-art rendering with zoom, pan and grid toggle.
- Terrain brushes, eraser, fill, selection and inspection.
- Full undo/redo.
- JSON world serialisation + SQLite snapshot persistence.
- Three entity categories: plants, herbivores, predators.
- Tick-based simulation with run / pause / step / reset / speed control.
- Finite-State Machine behaviour (WANDER, SEEK_FOOD, EAT, FLEE, CHASE, REST, REPRODUCE).
- Utility-based decision making with visible per-action scoring in the inspector.
- Optional Q-learning experiments for adaptive creature behaviour.
- Environmental mechanics: day/night cycle, weather, seasons, fire spread (cellular automata).
- Analytics charts (population, resources, health, history).
- A collapsible DSA laboratory that visualises queues, heaps, stacks, BFS/DFS/A* frontiers and visited nodes.
- Deterministic mode: same world + same seed → same outcome.

## Custom Data Structures (implemented from scratch)

| Data structure | File | Used for |
|---|---|---|
| 2D Array | `engine/world.py` | World grid |
| Graph | `dsa/graph.py` | Traversable cells and weighted movement costs |
| Queue | `dsa/queue.py` | BFS frontier, event processing |
| Stack | `dsa/stack.py` | Undo/redo, DFS |
| Binary Heap | `dsa/heap.py` | A* open set, event scheduling |
| Hash Table | `dsa/hash_table.py` | Entity lookup (custom collision handling) |
| Linked List | `dsa/linked_list.py` | Simulation event history |
| Tree | `dsa/tree.py` | Entity hierarchy / behaviour representation |
| Trie | `dsa/trie.py` | Optional tool/command prefix search |

## Custom Algorithms

BFS, DFS, A* pathfinding, Flood Fill, Cellular Automata, Sorting, Binary Search.

## Technology

- **Python 3.11+**
- **PySide6** — complete desktop GUI (QPainter / QGraphicsView)
- **SQLite** — persistent application data
- **JSON** — portable world files
- **Matplotlib** — charts and analytics
- **Pytest** — automated tests

Strictly no JavaScript, TypeScript, HTML, CSS, React, Vue, Electron, Node.js or browser-based frontend. Everything — UI, simulation, algorithms, rendering — is Python.

## Installation

```bash
pip install -r requirements.txt
python app.py
```

## Project Structure

See `docs/ARCHITECTURE.md` for a full breakdown.

## Testing

```bash
pytest tests/ -v
```

## Documentation

- `docs/ARCHITECTURE.md` — module map and design rules
- `docs/DSA_MAPPING.md` — which data structure is used where, and why
- `docs/AI_EXPLANATION.md` — FSM transitions and utility scoring maths
- `docs/USER_GUIDE.md` — how to use the application
- `docs/COMPLEXITY.md` — time and space complexity of every algorithm

## License

Academic use. See `TODO.md` for the development roadmap.