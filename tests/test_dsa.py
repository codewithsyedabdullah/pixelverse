"""Tests for the from-scratch DSA structures in ``dsa/``."""

from __future__ import annotations

import pytest

from dsa.stack import Stack
from dsa.queue import Queue
from dsa.linked_list import LinkedList
from dsa.hash_table import HashTable
from dsa.heap import Heap, HeapEntry


# --------------------------------------------------------------------------- Stack
class TestStack:
    def test_empty(self):
        s = Stack()
        assert len(s) == 0
        assert not s
        assert s.pop() is None
        assert s.peek() is None

    def test_lifo(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        assert len(s) == 3
        assert s.peek() == 3
        assert s.pop() == 3
        assert s.pop() == 2
        assert s.pop() == 1
        assert s.pop() is None
        assert len(s) == 0

    def test_iter_top_to_bottom(self):
        s = Stack()
        for i in range(5):
            s.push(i)
        assert list(s) == [4, 3, 2, 1, 0]

    def test_clear(self):
        s = Stack()
        s.push("a")
        s.clear()
        assert len(s) == 0
        assert not s


# --------------------------------------------------------------------------- Queue
class TestQueue:
    def test_empty(self):
        q = Queue()
        assert len(q) == 0
        assert not q
        assert q.dequeue() is None
        assert q.peek() is None

    def test_fifo(self):
        q = Queue()
        for i in range(5):
            q.enqueue(i)
        assert q.peek() == 0
        assert q.dequeue() == 0
        assert q.dequeue() == 1
        assert len(q) == 3
        assert list(q) == [2, 3, 4]

    def test_mixed(self):
        q = Queue()
        q.enqueue("a")
        q.enqueue("b")
        assert q.dequeue() == "a"
        q.enqueue("c")
        assert q.dequeue() == "b"
        assert q.dequeue() == "c"
        assert q.dequeue() is None

    def test_clear(self):
        q = Queue()
        q.enqueue(1)
        q.clear()
        assert len(q) == 0


# --------------------------------------------------------------------------- LinkedList
class TestLinkedList:
    def test_empty(self):
        ll = LinkedList()
        assert len(ll) == 0
        assert not ll
        assert list(ll) == []
        assert ll.pop() is None

    def test_append_and_iter(self):
        ll = LinkedList([1, 2, 3])
        assert len(ll) == 3
        assert list(ll) == [1, 2, 3]

    def test_prepend(self):
        ll = LinkedList()
        ll.append(2)
        ll.prepend(1)
        ll.append(3)
        assert list(ll) == [1, 2, 3]

    def test_pop_tail(self):
        ll = LinkedList([1, 2, 3])
        assert ll.pop() == 3
        assert ll.pop() == 2
        assert ll.pop() == 1
        assert ll.pop() is None
        assert len(ll) == 0


# --------------------------------------------------------------------------- HashTable
class TestHashTable:
    def test_basic(self):
        ht = HashTable()
        ht.put("a", 1)
        ht.put("b", 2)
        assert ht.get("a") == 1
        assert ht.get("b") == 2
        assert ht.get("c") is None
        assert ht.get("c", "default") == "default"
        assert "a" in ht
        assert "c" not in ht
        assert len(ht) == 2

    def test_overwrite(self):
        ht = HashTable()
        ht.put("k", 1)
        ht.put("k", 2)
        assert ht.get("k") == 2
        assert len(ht) == 1

    def test_remove(self):
        ht = HashTable()
        ht.put("x", 10)
        assert ht.remove("x") is True
        assert ht.remove("x") is False
        assert "x" not in ht
        assert len(ht) == 0

    def test_resize_under_load(self):
        ht = HashTable(capacity=4)
        for i in range(100):
            ht.put(f"key{i}", i)
        assert len(ht) == 100
        for i in range(100):
            assert ht.get(f"key{i}") == i

    def test_dict_protocol(self):
        ht = HashTable()
        ht["k"] = "v"
        assert ht["k"] == "v"
        with pytest.raises(KeyError):
            _ = ht["missing"]
        del ht["k"]
        assert "k" not in ht

    def test_items_keys_values(self):
        ht = HashTable()
        for i in range(5):
            ht.put(i, i * 10)
        assert sorted(ht.keys()) == [0, 1, 2, 3, 4]
        assert sorted(ht.values()) == [0, 10, 20, 30, 40]
        assert sorted(ht.items()) == [(0, 0), (1, 10), (2, 20), (3, 30), (4, 40)]


# --------------------------------------------------------------------------- Heap
class TestHeap:
    def test_empty(self):
        h = Heap()
        assert len(h) == 0
        assert not h
        assert h.pop() is None
        assert h.peek() is None

    def test_ordering(self):
        h = Heap()
        for v in [5, 1, 3, 2, 4]:
            h.push(v, v)
        out = []
        while h:
            out.append(h.pop())
        assert out == [1, 2, 3, 4, 5]

    def test_priority_not_value(self):
        h = Heap()
        h.push("low", 10)
        h.push("high", 1)
        h.push("mid", 5)
        assert h.pop() == "high"
        assert h.pop() == "mid"
        assert h.pop() == "low"

    def test_stable_tiebreak(self):
        h = Heap()
        h.push("a", 1)
        h.push("b", 1)
        h.push("c", 1)
        assert h.pop() == "a"
        assert h.pop() == "b"
        assert h.pop() == "c"

    def test_mixed_priorities(self):
        h = Heap()
        h.push("z", 3.0)
        h.push("a", 1.0)
        h.push("m", 2.0)
        assert [h.pop() for _ in range(3)] == ["a", "m", "z"]

    def test_peek_does_not_remove(self):
        h = Heap()
        h.push("only", 0)
        assert h.peek() == "only"
        assert len(h) == 1
        assert h.peek() == "only"

    def test_clear(self):
        h = Heap()
        for i in range(10):
            h.push(i, i)
        h.clear()
        assert len(h) == 0
        assert h.pop() is None