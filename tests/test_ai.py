"""Tests for the AI behaviour module (M8)."""

from __future__ import annotations

import pytest

from ai.behaviour import Action, AIBehaviour, State, StateMachine, UtilityAI


# --------------------------------------------------------------------------- FSM
class TestStateMachine:
    def test_initial_state(self):
        sm = StateMachine("idle")
        assert sm.current_name == "idle"

    def test_update_runs(self):
        sm = StateMachine("idle")
        sm.add_state("idle")
        sm.add_state("active")
        calls = []
        sm.get_state("idle").on_update(lambda m, c: calls.append("idle"))
        sm.update(None)
        assert calls == ["idle"]

    def test_transition(self):
        sm = StateMachine("idle")
        sm.add_state("idle")
        sm.add_state("active")
        sm.add_transition("idle", "active", lambda ctx: ctx.go)
        sm.update(type("Ctx", (), {"go": False})())
        assert sm.current_name == "idle"
        sm.update(type("Ctx", (), {"go": True})())
        assert sm.current_name == "active"

    def test_force(self):
        sm = StateMachine("a")
        sm.add_state("a")
        sm.add_state("b")
        sm.force("b", None)
        assert sm.current_name == "b"

    def test_enter_exit_hooks(self):
        sm = StateMachine("a")
        sm.add_state("a")
        sm.add_state("b")
        events = []
        sm.get_state("a").on_exit(lambda m, c: events.append("exit-a"))
        sm.get_state("b").on_enter(lambda m, c: events.append("enter-b"))
        sm.force("b", None)
        assert events == ["exit-a", "enter-b"]


# --------------------------------------------------------------------------- Utility AI
class TestUtilityAI:
    def test_empty_returns_none(self):
        ai = UtilityAI()
        assert ai.evaluate([], None) is None

    def test_picks_highest(self):
        ai = UtilityAI()
        a = Action("low")
        b = Action("high")
        ai.add_scorer(lambda act, ctx: 1.0 if act.name == "high" else 0.0)
        chosen = ai.evaluate([a, b], None)
        assert chosen is b
        assert b.score == 1.0
        assert a.score == 0.0

    def test_product_combiner_vetoes(self):
        ai = UtilityAI()  # default product combiner
        a = Action("a")
        ai.add_scorer(lambda act, ctx: 0.0)  # vetoes everything
        ai.add_scorer(lambda act, ctx: 1.0)
        chosen = ai.evaluate([a], None)
        assert chosen.score == 0.0

    def test_sum_combiner(self):
        ai = UtilityAI(combiner="sum")
        a = Action("a")
        ai.add_scorer(lambda act, ctx: 0.4)
        ai.add_scorer(lambda act, ctx: 0.4)
        chosen = ai.evaluate([a], None)
        assert abs(chosen.score - 0.8) < 1e-9

    def test_no_scorers_returns_one(self):
        ai = UtilityAI()
        a = Action("a")
        chosen = ai.evaluate([a], None)
        assert chosen is a
        assert chosen.score == 1.0


# --------------------------------------------------------------------------- AIBehaviour
class TestAIBehaviour:
    def test_decide_without_utility(self):
        ab = AIBehaviour()
        a = Action("a")
        assert ab.decide([a], None) is a

    def test_decide_with_utility(self):
        ab = AIBehaviour()
        ab.utility = UtilityAI()
        ab.utility.add_scorer(lambda act, ctx: 1.0 if act.name == "best" else 0.0)
        chosen = ab.decide([Action("bad"), Action("best")], None)
        assert chosen.name == "best"
        assert ab.last_action is chosen

    def test_decide_no_candidates(self):
        ab = AIBehaviour()
        assert ab.decide([], None) is None

    def test_fsm_update_hooked(self):
        ab = AIBehaviour()
        sm = StateMachine("idle")
        sm.add_state("idle")
        sm.add_state("run")
        sm.add_transition("idle", "run", lambda ctx: ctx.go)
        ab.fsm = sm
        ab.update(type("Ctx", (), {"go": True})())
        assert sm.current_name == "run"