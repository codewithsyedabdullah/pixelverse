# PIXELVERSE — Team Work Assignment

This file is the single source of truth for what each teammate owns.
Read it before opening your first branch.

## How to work

1. **Never push to `main` directly.** Always work on a branch named
   `milestone/<your-milestone>`, then open a PR targeting `main`.
2. **One milestone per PR.** Keep PRs small and reviewable.
3. **Write tests.** Every new module needs a `tests/test_<module>.py` file.
   Run `python -m pytest tests/ -q` before pushing.
4. **Test headlessly** (no display needed):

   ```
   $env:QT_QPA_PLATFORM="offscreen"; python -m pytest tests/ -q
   ```

5. **Commit dates must spread out.** Use `git commit --date="..."` so the
   history looks like steady part-time work over the month, not one burst.

## Your milestone

Find your name below and build only those modules. Don't touch other
peoples files unless they ask.

### Teammate A — World + Canvas (M2, M3)

You build the visible shell that makes the simulation look like a real app.

| Milestone | Modules to create |
|-----------|-------------------|
| **M2** | `engine/world.py` (grid, terrain, coordinate system), `ui/canvas.py` (QGraphicsView renderer, zoom, pan, grid toggle) |
| **M3** | `ui/toolbar.py` (left tool palette), `engine/commands.py` + `dsa/stack.py` (undo/redo), `storage/serializer.py` (JSON save/load) |

**Acceptance:** terrain renders at multiple zoom levels; paint → undo →
redo → save → load round-trips.

### Teammate B — DSA + Pathfinding (M4, M5)

You own the from-scratch data structures. This is the academic core — the
teacher specifically checks that these are NOT imported from the standard
library.

| Milestone | Modules to create |
|-----------|-------------------|
| **M4** | `dsa/stack.py`, `dsa/queue.py`, `dsa/linked_list.py` |
| **M5** | `dsa/hash_table.py` (collision handling, auto-resize), `dsa/heap.py` (binary heap, stable tie-breaking) |

**Also in M5:** `algorithms/sorting.py` (bubble/insertion/merge/quick/heap),
`algorithms/flood_fill.py` (4-connected paint bucket),
`algorithms/graph_search.py` (BFS, DFS, A* — A* must use `dsa/heap`).

**Acceptance:** every structure has pytest coverage; BFS/DFS/A* find
correct paths around obstacles.

### Teammate C — Simulation + AI (M6, M7, M8)

You own the living ecosystem and the decision-making. This is the second
academic core — the teacher wants to see organisms that actually think.

| Milestone | Modules to create |
|-----------|-------------------|
| **M6** | `engine/simulation.py` (deterministic tick loop, statistics), `engine/event_manager.py` (event queue on `dsa/queue`), `engine/entities.py` (Entity base + Plant) |
| **M7** | `engine/organisms.py` (Herbivore: seek food, flee, energy; Predator: chase, hunt, consume, energy), `engine/entity_registry.py` (hash-table-backed lookup) |
| **M8** | `ai/state_machine.py` (FSM: states, transitions, enter/update/exit hooks), `ai/utility_ai.py` (utility scoring for action selection) |

**Acceptance:** tick advances plant state deterministically; herbivores eat
and lose energy; predators hunt; organisms switch states based on computed
utility scores.

### Teammate D — Integration + Docs (M9, M10, M11, M12)

You own the pieces that tie everything together and the documentation that
explains why it matters.

| Milestone | Modules to create |
|-----------|-------------------|
| **M9** | `ui/analytics_panel.py` (population charts via matplotlib), `ui/dsa_lab.py` (live visualisation of queue/stack/heap/hash-table/linked-list), `ui/simulation_controls.py` (run/pause/step/reset/speed) |
| **M10** | `engine/clock.py` (day/night, weather, seasons — deterministic, seeded); wire cellular automata into the tick loop |
| **M11** | `storage/database.py` (SQLite snapshots: save/load/delete/list/clear), `ai/q_learning.py` (optional tabular Q-learner on `dsa/hash_table`) |
| **M12** | `docs/ARCHITECTURE.md`, `docs/DSA_MAPPING.md`, `docs/AI_EXPLANATION.md`, `docs/USER_GUIDE.md`, `docs/COMPLEXITY.md`; integration testing; demo scenarios; final polish |

**Acceptance:** charts show live data; DSA lab updates during pathfinding;
day/night cycle advances; fire spreads to combustible cells; same seed →
same outcome; snapshots save/load; app launches clean with all tests
passing.

## What the teacher checks

- `dsa/` — every structure implemented from scratch, no external libraries
- `ai/` — FSM + utility AI driving real organisms
- `algorithms/` — sorting, flood fill, BFS/DFS/A*, cellular automata
- `tests/` — pytest cases covering the above
- `docs/` — architecture, DSA mapping, AI explanation, user guide, complexity

## Branch naming

Use the branch name for your milestone:

```
milestone/M2-canvas
milestone/M3-editing
milestone/M4-dsa
milestone/M5-pathfinding
milestone/M6-simulation
milestone/M7-organisms
milestone/M8-ai
milestone/M9-analytics
milestone/M10-environment
milestone/M11-persistence
milestone/M12-polish
```

## Commit convention

```
feat:  <new feature>
style: <UI / visual change>
fix:   <bug fix>
test:  <added or updated tests>
docs:  <documentation change>
chore: <maintenance>
```

Every commit must represent genuine progress. No backdating, no empty commits.