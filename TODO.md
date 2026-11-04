# PIXELVERSE — Development Roadmap

All prior milestone work (DSA, algorithms, simulation, AI, clock, persistence,
UI panels) is merged to `main` via PRs #1–#7.  Remaining work is grouped into
three milestones.

## MILESTONE A — World editing + toolbar  (NOT STARTED)
- [ ] `ui/toolbar.py` — left vertical tool palette (select, terrain, eraser, fill, water, plant, animal, object, inspect)
- [ ] Terrain painting on canvas + eraser + selection
- [ ] `engine/commands.py` + `dsa/stack.py` — undo/redo command pattern
- [ ] `storage/serializer.py` — JSON save/load
- [ ] World configuration dialog (dimensions)
- [ ] Acceptance: paint → undo → redo → save → load round-trip

## MILESTONE B — Inspector + integration  (NOT STARTED)
- [ ] `ui/inspector.py` — entity detail panel with decision reasoning + per-action scores
- [ ] Wire `app.py` / `main_window.py` to the canvas, panels, and simulation controls
- [ ] Demo scenarios / scenario loader
- [ ] Acceptance: app launches clean; clicking an entity shows its utility scores

## MILESTONE C — Polish + docs  (NOT STARTED)
- [ ] `docs/ARCHITECTURE.md`, `docs/DSA_MAPPING.md`, `docs/AI_EXPLANATION.md`
- [ ] `docs/USER_GUIDE.md`, `docs/COMPLEXITY.md`
- [ ] README finalised; TODO finalised
- [ ] Performance profiling + bug sweep
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