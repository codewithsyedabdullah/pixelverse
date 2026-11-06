"""Tests for dsa/heap.py."""

from __future__ import annotations

import pytest

from dsa.heap import Heap


class TestHeap:
    def test_empty(self):
        h = Heap()
        assert len(h) == 0
        assert not h
        assert h.pop() is None
        assert h.peek() is None
        assert h.peek_priority() is None

    def test_push_pop_min(self):
        h = Heap()
        h.push(5)
        h.push(2)
        h.push(8)
        h.push(1)
        assert h.peek() == 1
        assert h.pop() == 1
        assert h.pop() == 2
        assert h.pop() == 5
        assert h.pop() == 8
        assert h.pop() is None

    def test_peek_does_not_remove(self):
        h = Heap()
        h.push(3)
        h.push(1)
        assert h.peek() == 1
        assert h.peek() == 1
        assert len(h) == 2

    def test_push_with_priority(self):
        h = Heap()
        h.push("low", priority=5.0)
        h.push("high", priority=1.0)
        h.push("mid", priority=3.0)
        assert h.peek() == "high"
        assert h.pop() == "high"
        assert h.pop() == "mid"
        assert h.pop() == "low"

    def test_default_priority_zero(self):
        h = Heap()
        h.push("a")
        h.push("b")
        # Both priority 0 — stable order means first inserted wins.
        assert h.pop() == "a"
        assert h.pop() == "b"

    def test_contains(self):
        h = Heap()
        h.push("x")
        assert "x" in h
        assert "y" not in h

    def test_remove(self):
        h = Heap()
        for v in (3, 1, 2):
            h.push(v)
        assert h.remove(1)
        assert 1 not in h
        assert h.pop() == 2
        assert h.pop() == 3

    def test_remove_missing(self):
        h = Heap()
        h.push(1)
        assert not h.remove(99)

    def test_clear(self):
        h = Heap()
        for v in range(10):
            h.push(v)
        h.clear()
        assert len(h) == 0
        assert not h

    def test_push_all(self):
        h = Heap()
        h.push_all([3, 1, 2])
        assert h.to_list() == [1, 2, 3]

    def test_to_list_sorted(self):
        h = Heap()
        import random
        data = [random.randint(0, 1000) for _ in range(200)]
        h.push_all(data)
        out = h.to_list()
        assert out == sorted(data)

    def test_stable_tie_breaking(self):
        h = Heap()
        h.push("a", priority=1.0)
        h.push("b", priority=1.0)
        h.push("c", priority=1.0)
        # First inserted should come out first.
        assert h.pop() == "a"
        assert h.pop() == "b"
        assert h.pop() == "c"

    def test_iter_snapshot(self):
        h = Heap()
        for v in (3, 1, 2):
            h.push(v)
        assert set(iter(h)) == {1, 2, 3}

    def test_large_heap(self):
        h = Heap()
        import random
        rng = random.Random(42)
        data = [rng.randint(0, 100000) for _ in range(500)]
        for v in data:
            h.push(v)
        out = []
        while h:
            out.append(h.pop())
        assert out == sorted(data)
        assert len(out) == 500