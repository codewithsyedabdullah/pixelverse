"""Tests for ai/q_learning.py (M11)."""

from __future__ import annotations

import random

import pytest

from ai.q_learning import QLearner


class TestQLearner:
    def test_initial_q_zero(self):
        ql = QLearner()
        assert ql.q_value("s", "a") == 0.0

    def test_best_action_picks_max(self):
        ql = QLearner()
        ql.update("s", "a", 1.0, "s2", [])
        ql.update("s", "b", 0.5, "s2", [])
        assert ql.best_action("s", ["a", "b"]) == "a"

    def test_update_increases_q(self):
        ql = QLearner(alpha=0.5, gamma=0.0)
        ql.update("s", "a", 1.0, "s2", [])
        assert ql.q_value("s", "a") == pytest.approx(0.5)

    def test_update_with_future(self):
        ql = QLearner(alpha=1.0, gamma=0.5)
        ql._table.put(("s2", "b"), 2.0)
        ql.update("s", "a", 1.0, "s2", ["b"])
        # Q = 0 + 1.0 * (1.0 + 0.5 * 2.0 - 0) = 2.0
        assert ql.q_value("s", "a") == pytest.approx(2.0)

    def test_choose_epsilon_greedy(self):
        ql = QLearner(epsilon=0.0)  # always exploit
        ql.update("s", "good", 1.0, "s2", [])
        ql.update("s", "bad", 0.0, "s2", [])
        rng = random.Random(0)
        # With epsilon=0 the best action is always chosen.
        for _ in range(20):
            assert ql.choose("s", ["good", "bad"], rng=rng) == "good"

    def test_choose_explores(self):
        ql = QLearner(epsilon=1.0)  # always explore
        rng = random.Random(0)
        actions = [ql.choose("s", ["a", "b"], rng=rng) for _ in range(10)]
        # At least one of each should appear over 10 draws.
        assert "a" in actions and "b" in actions

    def test_empty_actions(self):
        ql = QLearner()
        assert ql.best_action("s", []) is None
        assert ql.choose("s", []) is None

    def test_to_from_dict_roundtrip(self):
        ql = QLearner(alpha=0.2, gamma=0.8, epsilon=0.3)
        ql.update("s", "a", 1.0, "s2", [])
        data = ql.to_dict()
        ql2 = QLearner.from_dict(data)
        assert ql2.alpha == 0.2
        assert ql2.gamma == 0.8
        assert ql2.epsilon == 0.3
        assert ql2.q_value("s", "a") == ql.q_value("s", "a")

    def test_len(self):
        ql = QLearner()
        assert len(ql) == 0
        ql.update("s", "a", 1.0, "s2", [])
        assert len(ql) == 1