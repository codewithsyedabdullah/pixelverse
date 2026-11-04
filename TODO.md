# PIXELVERSE — Development Roadmap

Repo reset to the M1 scaffold on 2026-11-04 so the 3-person team can
distribute the work over the remaining weeks.  Nobody pushes to `main`
directly — work on a `milestone/<name>` branch and open a PR.

## MILESTONE 1 — Project foundation  ✅ COMPLETE (committed `b0ee154`)
- [x] Repository initialised on GitHub (public, default branch `main`)
- [x] Directory structure created
- [x] `.gitignore`, `requirements.txt`, `README.md`, `TODO.md`
- [x] `config.py` — constants, terrain properties, palette
- [x] `ui/theme.py` — dark theme + stylesheet
- [x] `ui/main_window.py` — main window skeleton with nav bar
- [x] `app.py` — entry point
- [x] Smoke test: application launches a window (offscreen)

## MILESTONE 2 — World canvas  (NOT STARTED)
- [ ] `engine/world.py` — grid 2D array, terrain types, coordinate system
- [ ] `ui/canvas.py` — QGraphicsView pixel-art renderer, zoom, pan, grid toggle
- [ ] Terrain rendering with sharp pixels (nearest-neighbour scaling)
- [ ] Acceptance: terrain renders correctly at multiple zoom levels

## MILESTONE 3 — World editing  (NOT STARTED)
- [ ] `ui/toolbar.py` — left vertical tool palette
- [ ] Terrain painting on canvas + eraser + selection
- [ ] `engine/commands.py` + `dsa/stack.py` — undo/redo
- [ ] `storage/serializer.py` — JSON save/load
- [ ] World configuration dialog (dimensions)
- [ ] Acceptance: paint → undo → redo → save → load round-trip

## MILESTONE 4 — DSA foundation  (NOT STARTED)
- [ ] `dsa/queue.py` + tests
- [ ] `dsa/stack.py` + tests
- [ ] `dsa/linked_list.py` + tests
- [ ] `dsa/hash_table.py` + tests (collision handling)
- [ ] `dsa/heap.py` + tests (binary heap ordering)
- [ ] Acceptance: all pytest tests pass

## MILESTONE 5 — Graph and pathfinding  (NOT STARTED)
- [ ] `dsa/graph.py` — custom weighted graph over world cells
- [ ] `algorithms/bfs.py` + tests
- [ ] `algorithms/dfs.py` + tests
- [ ] `algorithms/astar.py` + tests (uses `dsa/heap.py`)
- [ ] Path visualisation drawn on canvas
- [ ] Acceptance: BFS/DFS/A* find correct paths around obstacles

## MILESTONE 6 — Simulation engine  (NOT STARTED)
- [ ] `engine/simulation.py` — tick loop, statistics
- [ ] `engine/event_manager.py` — simulation event queue
- [ ] `engine/entities.py` — Entity base class + Plant
- [ ] Resource management
- [ ] Acceptance: tick advances plant state deterministically

## MILESTONE 7 — Living organisms  (NOT STARTED)
- [ ] `engine/organisms.py` — Herbivore + Predator
- [ ] Death and reproduction conditions
- [ ] `engine/entity_registry.py` — hash-table-backed lookup
- [ ] Acceptance: herbivores eat and lose energy; predators hunt

## MILESTONE 8 — AI behaviour  (NOT STARTED)
- [ ] `ai/state_machine.py` — FSM states and transitions
- [ ] `ai/utility_ai.py` — utility scoring for action selection
- [ ] Predator avoidance and intelligent food searching
- [ ] Inspector displays decision reasoning and per-action scores
- [ ] Acceptance: organism switches states and inspector shows computed scores

## MILESTONE 9 — Analytics and DSA laboratory  (NOT STARTED)
- [ ] `ui/analytics_panel.py` — population charts (matplotlib)
- [ ] `ui/dsa_lab.py` — live visualisation of queue/heap/stack/frontier/visited
- [ ] `ui/simulation_controls.py` — run/pause/step/reset/speed
- [ ] Acceptance: charts show live data; DSA lab updates during pathfinding

## MILESTONE 10 — Environmental simulation  (NOT STARTED)
- [ ] `engine/clock.py` — day/night, weather, seasons
- [ ] `algorithms/cellular_automata.py` — fire spread, plant growth
- [ ] Environmental mechanics affect the simulation
- [ ] Acceptance: day/night cycle advances; fire spreads to combustible cells

## MILESTONE 11 — Persistence and Q-learning  (NOT STARTED)
- [ ] `storage/database.py` — SQLite snapshots
- [ ] `ai/q_learning.py` — optional adaptive behaviour
- [ ] Reproducible random seeds / deterministic mode
- [ ] Acceptance: same seed → same outcome; snapshots save/load

## MILESTONE 12 — Final polish  (NOT STARTED)
- [ ] Integration testing across all modules
- [ ] Bug fixes and performance profiling
- [ ] Demo scenarios
- [ ] Documentation: `docs/ARCHITECTURE.md`, `DSA_MAPPING.md`, `AI_EXPLANATION.md`, `USER_GUIDE.md`, `COMPLEXITY.md`
- [ ] README and TODO finalised
- [ ] Acceptance: MVP checklist complete, all tests pass, app runs clean

---

## Suggested team split

| Person | Milestones | Notes |
|--------|-----------|-------|
| **Teammate A** | M2, M3 | World canvas + editing toolbar + undo/redo |
| **Teammate B** | M4, M5 | DSA structures + graph search + pathfinding |
| **Teammate C** | M6, M7, M8 | Simulation engine + organisms + AI behaviour |
| **You** | M9, M10, M11, M12 | Analytics panel, DSA lab, clock, persistence, Q-learning, docs, polish |

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