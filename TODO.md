# PIXELVERSE — Development Roadmap

Each milestone must work and pass its acceptance tests before the next begins.

## MILESTONE 1 — Project foundation  ✅ COMPLETE
- [x] Repository initialised on GitHub (public, default branch `main`)
- [x] Directory structure created
- [x] `.gitignore`, `requirements.txt`, `README.md`, `TODO.md`
- [x] `config.py` — constants, terrain properties, palette
- [x] `ui/theme.py` — dark theme + stylesheet
- [x] `ui/main_window.py` — main window skeleton with nav bar
- [x] `app.py` — entry point
- [x] Smoke test: application launches a window (offscreen)

## MILESTONE 2 — World canvas  ✅ COMPLETE (PR #1)
- [x] `engine/world.py` — grid 2D array, terrain types, coordinate system
- [x] `ui/canvas.py` — QGraphicsView pixel-art renderer, zoom, pan, grid toggle
- [x] Terrain rendering with sharp pixels (nearest-neighbour scaling)
- [x] Acceptance: terrain renders correctly at multiple zoom levels (256 tiles, zoom in/out verified)

## MILESTONE 3 — World editing
- [ ] `ui/toolbar.py` — left vertical tool palette (select, terrain, eraser, fill, water, plant, animal, object, inspect)
- [ ] Terrain painting on canvas + eraser + selection
- [ ] `engine/commands.py` + `dsa/stack.py` — undo/redo
- [ ] `storage/serializer.py` — JSON save/load
- [ ] World configuration dialog (dimensions)
- [ ] Acceptance: paint → undo → redo → save → load round-trip

## MILESTONE 4 — DSA foundation  ✅ COMPLETE (PR #2)
- [x] `dsa/queue.py` + tests
- [x] `dsa/stack.py` + tests
- [x] `dsa/linked_list.py` + tests
- [x] `dsa/hash_table.py` + tests (collision handling)
- [x] `dsa/heap.py` + tests (binary heap ordering)
- [x] Acceptance: all pytest tests pass

## MILESTONE 5 — Graph and pathfinding  ✅ COMPLETE (PR #2)
- [x] `algorithms/graph_search.py` — BFS / DFS / A* over world cells (uses `dsa/heap`)
- [x] `algorithms/flood_fill.py` — 4-connected region fill
- [x] `algorithms/sorting.py` — bubble/insertion/merge/quick/heap sort
- [x] `algorithms/cellular_automata.py` — fire spread + plant growth
- [x] Acceptance: BFS/DFS/A* find correct paths around obstacles (20 tests)

## MILESTONE 6 — Simulation engine
- [ ] `engine/simulation.py` — tick loop, statistics
- [ ] `engine/event_manager.py` — simulation event queue
- [ ] `entities/base_entity.py` — Entity base class
- [ ] `entities/plant.py` — growth, regeneration, food value
- [ ] Resource management
- [ ] Acceptance: tick advances plant state deterministically

## MILESTONE 7 — Living organisms
- [ ] `entities/herbivore.py` — seek food, move (A*), eat, energy, flee
- [ ] `entities/predator.py` — chase, hunt, consume, energy
- [ ] Death and reproduction conditions
- [ ] `entities/entity_registry.py` — hash-table-backed lookup
- [ ] Acceptance: herbivores eat and lose energy; predators hunt

## MILESTONE 8 — AI behaviour
- [ ] `ai/state_machine.py` — FSM states and transitions
- [ ] `ai/utility_ai.py` — utility scoring for action selection
- [ ] Predator avoidance and intelligent food searching
- [ ] Inspector displays decision reasoning and per-action scores
- [ ] Acceptance: organism switches states and inspector shows computed scores

## MILESTONE 9 — Analytics and DSA laboratory
- [ ] `ui/analytics_panel.py` — population charts (matplotlib)
- [ ] `ui/dsa_lab.py` — live visualisation of queue/heap/stack/frontier/visited
- [ ] `ui/simulation_controls.py` — run/pause/step/reset/speed
- [ ] Acceptance: charts show live data; DSA lab updates during pathfinding

## MILESTONE 10 — Environmental simulation
- [ ] `engine/clock.py` — day/night, weather, seasons
- [ ] `algorithms/cellular_automata.py` — fire spread, plant growth
- [ ] Environmental mechanics affect the simulation
- [ ] Acceptance: day/night cycle advances; fire spreads to combustible cells

## MILESTONE 11 — Persistence and Q-learning
- [ ] `storage/database.py` — SQLite snapshots
- [ ] `ai/q_learning.py` — optional adaptive behaviour
- [ ] Reproducible random seeds / deterministic mode
- [ ] Acceptance: same seed → same outcome; snapshots save/load

## MILESTONE 12 — Final polish
- [ ] Integration testing across all modules
- [ ] Bug fixes and performance profiling
- [ ] Demo scenarios
- [ ] Documentation: `docs/ARCHITECTURE.md`, `DSA_MAPPING.md`, `AI_EXPLANATION.md`, `USER_GUIDE.md`, `COMPLEXITY.md`
- [ ] README and TODO finalised
- [ ] Acceptance: MVP checklist complete, all tests pass, app runs clean

---

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