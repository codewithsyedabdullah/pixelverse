"""Tests for dsa/stack.py and dsa/queue.py."""

from __future__ import annotations

import pytest

from dsa.stack import Stack
from dsa.queue import Queue


class TestStack:
    def test_empty(self):
        s = Stack()
        assert len(s) == 0
        assert not s
        assert s.pop() is None
        assert s.peek() is None

    def test_push_pop(self):
        s = Stack()
        s.push(1)
        s.push(2)
        assert len(s) == 2
        assert s.pop() == 2
        assert s.pop() == 1
        assert s.pop() is None
        assert len(s) == 0

    def test_peek(self):
        s = Stack()
        s.push("a")
        assert s.peek() == "a"
        assert s.peek() == "a"  # does not remove
        assert len(s) == 1

    def test_contains(self):
        s = Stack()
        for v in (1, 2, 3):
            s.push(v)
        assert 2 in s
        assert 99 not in s

    def test_clear(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.clear()
        assert len(s) == 0

    def test_iter(self):
        s = Stack()
        for v in (1, 2, 3):
            s.push(v)
        # Iteration order is insertion order (backing list).
        assert list(s) == [3, 2, 1]

    def test_lifo_order(self):
        s = Stack()
        for v in "abcdef":
            s.push(v)
        out = []
        while s:
            out.append(s.pop())
        assert out == list("fedcba")


class TestQueue:
    def test_empty(self):
        q = Queue()
        assert len(q) == 0
        assert not q
        assert q.dequeue() is None
        assert q.peek() is None

    def test_enqueue_dequeue(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        assert len(q) == 2
        assert q.dequeue() == 1
        assert q.dequeue() == 2
        assert q.dequeue() is None
        assert len(q) == 0

    def test_peek(self):
        q = Queue()
        q.enqueue("a")
        assert q.peek() == "a"
        assert q.peek() == "a"
        assert len(q) == 1

    def test_contains(self):
        q = Queue()
        for v in (1, 2, 3):
            q.enqueue(v)
        assert 2 in q
        assert 99 not in q

    def test_clear(self):
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        q.clear()
        assert len(q) == 0

    def test_iter(self):
        q = Queue()
        for v in (1, 2, 3):
            q.enqueue(v)
        assert list(q) == [1, 2, 3]

    def test_fifo_order(self):
        q = Queue()
        for v in "abcdef":
            q.enqueue(v)
        out = []
        while q:
            out.append(q.dequeue())
        assert out == list("abcdef")