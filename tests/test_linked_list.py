"""Tests for dsa/linked_list.py."""

from __future__ import annotations

import pytest

from dsa.linked_list import LinkedList


class TestLinkedList:
    def test_empty(self):
        ll = LinkedList()
        assert len(ll) == 0
        assert not ll
        assert list(ll) == []
        assert "x" not in ll

    def test_append(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        assert len(ll) == 2
        assert list(ll) == [1, 2]
        assert ll.to_list() == [1, 2]

    def test_prepend(self):
        ll = LinkedList()
        ll.append(2)
        ll.prepend(1)
        assert list(ll) == [1, 2]

    def test_append_and_prepend_combined(self):
        ll = LinkedList()
        ll.append("b")
        ll.prepend("a")
        ll.append("c")
        assert list(ll) == ["a", "b", "c"]

    def test_remove_head(self):
        ll = LinkedList()
        for v in (1, 2, 3):
            ll.append(v)
        assert ll.remove(1)
        assert list(ll) == [2, 3]

    def test_remove_tail(self):
        ll = LinkedList()
        for v in (1, 2, 3):
            ll.append(v)
        assert ll.remove(3)
        assert list(ll) == [1, 2]

    def test_remove_middle(self):
        ll = LinkedList()
        for v in (1, 2, 3):
            ll.append(v)
        assert ll.remove(2)
        assert list(ll) == [1, 3]

    def test_remove_missing(self):
        ll = LinkedList()
        ll.append(1)
        assert not ll.remove(99)
        assert list(ll) == [1]

    def test_remove_all_doubles(self):
        ll = LinkedList()
        for v in (1, 2, 1, 3, 1):
            ll.append(v)
        assert ll.remove(1)
        assert list(ll) == [2, 1, 3, 1]

    def test_contains(self):
        ll = LinkedList()
        for v in ("a", "b", "c"):
            ll.append(v)
        assert "b" in ll
        assert "z" not in ll

    def test_clear(self):
        ll = LinkedList()
        for v in (1, 2, 3):
            ll.append(v)
        ll.clear()
        assert len(ll) == 0
        assert not ll

    def test_repr(self):
        ll = LinkedList()
        ll.append(1)
        assert "1" in repr(ll)