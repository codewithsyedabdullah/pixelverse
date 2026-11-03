"""AI behaviour: finite state machine + utility-based decision making.

Both patterns are implemented from scratch:

* :class:`StateMachine` — explicit states and transitions, used for high-level
  behaviour (idle / wandering / seeking / fleeing / attacking).
* :class:`UtilityAI` — scores a set of candidate actions and picks the highest,
  used for fine-grained action selection (which food to approach, when to rest).

The :class:`AIBehaviour` base class wires them together and exposes a single
``decide`` method that returns the chosen action each tick.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Optional, TypeVar

T = TypeVar("T")


# --------------------------------------------------------------------------- FSM
class State:
    """A named state in a finite state machine."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._on_enter: List[Callable[["StateMachine", object], None]] = []
        self._on_update: List[Callable[["StateMachine", object], None]] = []
        self._on_exit: List[Callable[["StateMachine", object], None]] = []

    def on_enter(self, fn: Callable[["StateMachine", object], None]) -> None:
        self._on_enter.append(fn)

    def on_update(self, fn: Callable[["StateMachine", object], None]) -> None:
        self._on_update.append(fn)

    def on_exit(self, fn: Callable[["StateMachine", object], None]) -> None:
        self._on_exit.append(fn)

    def enter(self, machine: "StateMachine", ctx: object) -> None:
        for fn in self._on_enter:
            fn(machine, ctx)

    def update(self, machine: "StateMachine", ctx: object) -> None:
        for fn in self._on_update:
            fn(machine, ctx)

    def exit(self, machine: "StateMachine", ctx: object) -> None:
        for fn in self._on_exit:
            fn(machine, ctx)


class StateMachine:
    """A simple finite state machine with named states and transitions.

    Transitions are evaluated in registration order; the first matching
    condition wins.
    """

    def __init__(self, initial: str) -> None:
        self._states: Dict[str, State] = {}
        self._transitions: List[tuple[str, str, Callable[[object], bool]]] = []
        self.current: Optional[State] = None
        self.current_name = initial

    def add_state(self, name: str) -> State:
        state = State(name)
        self._states[name] = state
        if self.current is None:
            self.current = state
        return state

    def get_state(self, name: str) -> State:
        return self._states[name]

    def add_transition(
        self,
        from_state: str,
        to_state: str,
        condition: Callable[[object], bool],
    ) -> None:
        self._transitions.append((from_state, to_state, condition))

    def update(self, ctx: object) -> None:
        if self.current is None:
            return
        for from_state, to_state, cond in self._transitions:
            if from_state == self.current.name and cond(ctx):
                self._change(to_state, ctx)
                break
        if self.current is not None:
            self.current.update(self, ctx)

    def _change(self, name: str, ctx: object) -> None:
        if self.current is not None:
            self.current.exit(self, ctx)
        self.current = self._states[name]
        self.current_name = name
        self.current.enter(self, ctx)

    def force(self, name: str, ctx: object) -> None:
        self._change(name, ctx)


# --------------------------------------------------------------------------- Utility AI
class Action:
    """A candidate action with a name and an optional context payload."""

    def __init__(self, name: str, context: object = None, score: float = 0.0) -> None:
        self.name = name
        self.context = context
        self.score = score

    def __repr__(self) -> str:
        return f"Action({self.name!r}, score={self.score:.3f})"


class UtilityAI:
    """Utility-based action selection.

    Each candidate :class:`Action` is scored by a list of *scorers*
    (callables returning a value in ``[0, 1]``).  The final score is the
    product of all scorers (so a low scorer can veto an action entirely).
    The action with the highest final score is selected.
    """

    def __init__(self, combiner: str = "product") -> None:
        self._scorers: List[Callable[[Action, object], float]] = []
        self.combiner = combiner

    def add_scorer(self, fn: Callable[[Action, object], float]) -> None:
        self._scorers.append(fn)

    def evaluate(self, candidates: List[Action], ctx: object) -> Optional[Action]:
        if not candidates:
            return None
        best: Optional[Action] = None
        best_score = -1.0
        for action in candidates:
            score = self._score(action, ctx)
            action.score = score
            if score > best_score:
                best_score = score
                best = action
        return best

    def _score(self, action: Action, ctx: object) -> float:
        if not self._scorers:
            return 1.0
        values = [fn(action, ctx) for fn in self._scorers]
        if self.combiner == "sum":
            return max(0.0, min(1.0, sum(values)))
        prod = 1.0
        for v in values:
            prod *= max(0.0, min(1.0, v))
        return prod


# --------------------------------------------------------------------------- base behaviour
class AIBehaviour:
    """Base class providing the shared FSM + utility-AI plumbing.

    Subclasses populate the state machine and the utility scorers in
    ``__init__`` and override :meth:`update` to feed the decision back to the
    entity.
    """

    def __init__(self) -> None:
        self.fsm: Optional[StateMachine] = None
        self.utility: Optional[UtilityAI] = None
        self.last_action: Optional[Action] = None

    def decide(self, candidates: List[Action], ctx: object) -> Optional[Action]:
        if self.utility is None:
            return candidates[0] if candidates else None
        chosen = self.utility.evaluate(candidates, ctx)
        self.last_action = chosen
        return chosen

    def update(self, ctx: object) -> None:
        if self.fsm is not None:
            self.fsm.update(ctx)