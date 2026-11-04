"""Optional Q-learning for adaptive organism behaviour (M11).

Q-learning lets organisms learn which actions lead to higher rewards over
time.  This module is intentionally lightweight: it stores a Q-table in a
``dsa/hash_table`` and exposes a simple ``learn`` / ``choose`` API.

States are hashed strings (e.g. ``"hungry_near_plant"``); actions are named
strings (e.g. ``"seek"``).  The default epsilon-greedy policy balances
exploration with exploitation.
"""

from __future__ import annotations

from typing import Hashable, Optional, Tuple

from dsa.hash_table import HashTable


class QLearner:
    """A tabular Q-learner backed by ``dsa/hash_table``.

    The Q-table maps ``(state, action)`` -> float.  States and actions may be
    any hashable value.
    """

    def __init__(self, alpha: float = 0.1, gamma: float = 0.9,
                 epsilon: float = 0.1) -> None:
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self._table: HashTable[Tuple[Hashable, Hashable], float] = HashTable()

    # ------------------------------------------------------------------ API
    def q_value(self, state: Hashable, action: Hashable) -> float:
        return self._table.get((state, action), 0.0)

    def best_action(self, state: Hashable,
                    actions: list[Hashable]) -> Optional[Hashable]:
        if not actions:
            return None
        best = actions[0]
        best_val = self.q_value(state, best)
        for action in actions[1:]:
            v = self.q_value(state, action)
            if v > best_val:
                best_val = v
                best = action
        return best

    def choose(self, state: Hashable, actions: list[Hashable],
               rng=None) -> Optional[Hashable]:
        """Epsilon-greedy action selection."""
        import random
        if rng is None:
            rng = random
        if not actions:
            return None
        if rng.random() < self.epsilon:
            return rng.choice(actions)
        return self.best_action(state, actions)

    def update(self, state: Hashable, action: Hashable, reward: float,
               next_state: Hashable, next_actions: list[Hashable]) -> None:
        """Apply the Q-learning update rule.

        ``Q(s,a) = Q(s,a) + alpha * (r + gamma * max_a' Q(s',a') - Q(s,a))``
        """
        current = self.q_value(state, action)
        future = 0.0
        if next_actions:
            best_next = max((self.q_value(next_state, a) for a in next_actions),
                            default=0.0)
            future = self.gamma * best_next
        new_value = current + self.alpha * (reward + future - current)
        self._table.put((state, action), new_value)

    # ------------------------------------------------------------------ helpers
    def to_dict(self) -> dict:
        return {
            "alpha": self.alpha,
            "gamma": self.gamma,
            "epsilon": self.epsilon,
            "table": {f"{k[0]}::{k[1]}": v for k, v in self._table.items()},
        }

    @classmethod
    def from_dict(cls, data: dict) -> "QLearner":
        learner = cls(alpha=data["alpha"], gamma=data["gamma"],
                      epsilon=data["epsilon"])
        for key, value in data.get("table", {}).items():
            state, action = key.split("::", 1)
            learner._table.put((state, action), value)
        return learner

    def __len__(self) -> int:
        return len(self._table)