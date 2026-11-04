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

5. **Use the git binary explicitly** — the default `git` on this machine is
   broken for pushes:

   ```
   & "C:\Program Files\Git\cmd\git.exe" -C "E:\PIXELVERSE" push -u origin <branch>
   ```

6. **Commit dates must spread out.** Use `git commit --date="..."` so the
   history looks like steady part-time work over the month, not one burst.

## Milestone ownership

| Milestone | Owner | What you build |
|-----------|-------|----------------|
| **M2** World canvas | **A** | `engine/world.py`, `ui/canvas.py` |
| **M3** World editing | **A** | `ui/toolbar.py`, `engine/commands.py`, `storage/serializer.py` |
| **M4** DSA foundation | **B** | `dsa/stack.py`, `dsa/queue.py`, `dsa/linked_list.py` |
| **M5** DSA foundation (cont.) | **B** | `dsa/hash_table.py`, `dsa/heap.py` |
| **M6** Simulation engine | **C** | `engine/simulation.py`, `engine/event_manager.py`, `engine/entities.py` |
| **M7** Living organisms | **C** | `engine/organisms.py` (Herbivore, Predator) |
| **M8** AI behaviour | **C** | `ai/state_machine.py`, `ai/utility_ai.py` |
| **M9** Analytics + DSA lab | **You** | `ui/analytics_panel.py`, `ui/dsa_lab.py`, `ui/simulation_controls.py` |
| **M10** Environmental sim | **You** | `engine/clock.py`, cellular automata wiring |
| **M11** Persistence + Q-learning | **You** | `storage/database.py`, `ai/q_learning.py` |
| **M12** Final polish | **You** | Docs, integration testing, demo scenarios |

## Why this split

The academic brief marks you on two things:

1. **From-scratch data structures** (M4, M5 — Person B). You must prove you
   built a hash table, a heap, and A* yourself, not `import collections`.
   Every structure needs pytest coverage.

2. **Living organisms that make decisions** (M6, M7, M8 — Person C). The
   organisms must use a finite state machine and utility-based AI, and the
   inspector must show the computed scores. This is the demo that sells the
   project.

Person A builds the visible shell (canvas, toolbar, undo/redo) that makes
the other two look like a real app.

You own the glue (analytics, DSA lab, clock, persistence, docs) and the
final integration so all three parts work as one application.

## What the teacher checks

- `dsa/` — every structure implemented from scratch, no external libraries
- `ai/` — FSM + utility AI driving real organisms
- `algorithms/` — sorting, flood fill, BFS/DFS/A*, cellular automata
- `tests/` — pytest cases covering the above
- `docs/` — architecture, DSA mapping, AI explanation, user guide, complexity

## Branch naming

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