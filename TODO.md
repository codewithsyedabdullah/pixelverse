# PIXELVERSE — Development Roadmap

Nobody pushes to `main` directly — work on a `milestone/<name>` branch
and open a PR.  One milestone per PR.

## MILESTONE 1 — Project foundation  ✅ COMPLETE (`b0ee154`)
- [x] Repository initialised on GitHub (public, default branch `main`)
- [x] Directory structure created
- [x] `.gitignore`, `requirements.txt`, `README.md`, `TODO.md`
- [x] `config.py` — constants, terrain properties, palette
- [x] `ui/theme.py` — dark theme + stylesheet
- [x] `ui/main_window.py` — main window skeleton with nav bar
- [x] `app.py` — entry point
- [x] Smoke test: application launches a window (offscreen)

## MILESTONE 2 — World canvas  ✅ COMPLETE (PR #8, merged `67ed71b`)
- [x] `engine/world.py` — grid 2D array, terrain types, coordinate system
- [x] `ui/canvas.py` — QGraphicsView pixel-art renderer, zoom, pan, grid toggle
- [x] Terrain rendering with sharp pixels (nearest-neighbour scaling)
- [x] Zoom in/out with wheel or toolbar buttons (clamped 0.25x–4.0x)
- [x] Pan by dragging with middle mouse button
- [x] Grid toggle shows/hides cell borders
- [x] Cell hover updates status bar with (x, y) and terrain type
- [x] 33 pytest cases covering world model and canvas
- [x] Acceptance: terrain renders correctly at multiple zoom levels

## MILESTONE 3 — World editing  (NOT STARTED)
- [ ] `ui/toolbar.py` — left vertical tool palette
- [ ] Terrain painting on canvas + eraser + selection
- [ ] `engine/commands.py` + `dsa/stack.py` — undo/redo
- [ ] `storage/serializer.py` — JSON save/load
- [ ] World configuration dialog (dimensions)
- [ ] Acceptance: paint → undo → redo → save → load round-trip

## MILESTONE 4 — DSA foundation  ✅ COMPLETE (PR #6, merged `ea154bb`)
- [x] `dsa/stack.py` — LIFO stack, backed by `dsa/linked_list.LinkedList`
- [x] `dsa/queue.py` — FIFO queue, backed by `dsa/linked_list.LinkedList`
- [x] `dsa/linked_list.py` — singly linked list, O(1) append/prepend
- [x] `dsa/hash_table.py` — separate-chaining hash map with auto-resize
- [x] `dsa/heap.py` — binary min-heap with stable tie-breaking
- [x] 55 pytest cases covering every structure

## MILESTONE 5 — Graph and pathfinding  (NOT STARTED)
- [ ] `algorithms/sorting.py` — bubble/insertion/merge/quick/heap sort
- [ ] `algorithms/flood_fill.py` — 4-connected paint bucket
- [ ] `algorithms/graph_search.py` — BFS, DFS, A* (A* must use `dsa/heap`)
- [ ] Path visualisation drawn on canvas
- [ ] Acceptance: BFS/DFS/A* find correct paths around obstacles

## MILESTONE 6 — Simulation engine  (NOT STARTED)
- [ ] `engine/simulation.py` — tick loop, statistics
- [ ] `engine/event_manager.py` — simulation event queue on `dsa/queue`
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

## MILESTONE 10 — Environmental simulation  ✅ COMPLETE (PR #7, merged `50d3e25`)
- [x] `engine/clock.py` — day/night, weather, seasons (tick-based, deterministic)
- [x] `algorithms/cellular_automata.py` — fire spread, plant growth (seeded RNG, pure)
- [x] 13 pytest cases covering clock and cellular automata
- [x] Environmental mechanics: 4 seasons (Spring/Summer/Autumn/Winter, 30 days each)
- [x] Weather system: Rain/Clear/Cloudy/Snow per season
- [x] Fire spreads to grass/forest neighbors with configurable probability
- [x] Plant growth on soil next to existing grass/forest
- [x] Acceptance: day/night cycle advances; fire spreads to combustible cells

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

## Progress summary

| Milestone | Status | Owner | Tests |
|-----------|--------|-------|-------|
| M1 — Foundation | ✅ COMPLETE | — | — |
| M2 — World canvas | ✅ COMPLETE | A | 33 |
| M3 — World editing | ⬜ NOT STARTED | A | — |
| M4 — DSA foundation | ✅ COMPLETE | B | 55 |
| M5 — Pathfinding | ⬜ NOT STARTED | A | — |
| M6 — Simulation engine | ⬜ NOT STARTED | B | — |
| M7 — Living organisms | ⬜ NOT STARTED | B | — |
| M8 — AI behaviour | ⬜ NOT STARTED | B | — |
| M9 — Analytics + DSA lab | ⬜ NOT STARTED | B | — |
| M10 — Environment | ✅ COMPLETE | C | 13 |
| M11 — Persistence + Q-learning | ⬜ NOT STARTED | C | — |
| M12 — Final polish | ⬜ NOT STARTED | C | — |

**Total: 101 tests, all passing. 4 of 12 milestones complete.**

## Team split (3 people)

| Person | Milestones | Owns |
|--------|-----------|------|
| **A** | M2, M3, M4, M5 | Canvas, editing, all DSA structures, sorting, flood fill, BFS/DFS/A* |
| **B** | M6, M7, M8, M9 | Simulation engine, organisms, FSM + utility AI, analytics + DSA lab |
| **C** | M10, M11, M12 | Clock/weather/seasons, SQLite + Q-learning, all docs, final polish |

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