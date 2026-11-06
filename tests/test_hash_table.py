"""Tests for dsa/hash_table.py."""

from __future__ import annotations

import pytest

from dsa.hash_table import HashTable


class TestHashTable:
    def test_empty(self):
        ht = HashTable()
        assert len(ht) == 0
        assert not ht
        assert "x" not in ht
        assert ht.get("x") is None
        assert ht.get("x", "default") == "default"

    def test_put_and_get(self):
        ht = HashTable()
        ht.put("a", 1)
        ht.put("b", 2)
        assert len(ht) == 2
        assert ht.get("a") == 1
        assert ht.get("b") == 2

    def test_put_overwrites(self):
        ht = HashTable()
        ht.put("a", 1)
        ht.put("a", 2)
        assert len(ht) == 1
        assert ht.get("a") == 2

    def test_contains(self):
        ht = HashTable()
        ht.put("a", 1)
        assert "a" in ht
        assert "b" not in ht

    def test_remove(self):
        ht = HashTable()
        ht.put("a", 1)
        ht.put("b", 2)
        assert ht.remove("a") == 1
        assert "a" not in ht
        assert len(ht) == 1
        assert ht.get("b") == 2

    def test_remove_missing(self):
        ht = HashTable()
        assert ht.remove("nope") is None

    def test_keys_values_items(self):
        ht = HashTable()
        ht.put("a", 1)
        ht.put("b", 2)
        assert set(ht.keys()) == {"a", "b"}
        assert set(ht.values()) == {1, 2}
        assert dict(ht.items()) == {"a": 1, "b": 2}

    def test_clear(self):
        ht = HashTable()
        for i in range(10):
            ht.put(i, i)
        ht.clear()
        assert len(ht) == 0
        assert not ht

    def test_iter(self):
        ht = HashTable()
        for i in range(5):
            ht.put(i, i * 10)
        assert set(iter(ht)) == {0, 1, 2, 3, 4}

    def test_collision_handling(self):
        """Force many collisions by using a tiny table."""
        ht = HashTable(capacity=4)
        # All these keys should coexist even though the table is tiny.
        for i in range(20):
            ht.put(i, i)
        for i in range(20):
            assert ht.get(i) == i
        assert len(ht) == 20

    def test_resize_increases_capacity(self):
        ht = HashTable(capacity=4, load_factor=0.5)
        for i in range(10):
            ht.put(i, i)
        # After several resizes the capacity should be well above 4.
        assert ht._capacity > 4
        for i in range(10):
            assert ht.get(i) == i

    def test_resize_preserves_data(self):
        ht = HashTable(capacity=8)
        data = {f"key{i}": i for i in range(50)}
        for k, v in data.items():
            ht.put(k, v)
        for k, v in data.items():
            assert ht.get(k) == v
        assert len(ht) == 50

    def test_invalid_capacity(self):
        with pytest.raises(ValueError):
            HashTable(capacity=0)

    def test_invalid_load_factor(self):
        with pytest.raises(ValueError):
            HashTable(load_factor=1.5)

    def test_repr(self):
        ht = HashTable()
        ht.put("a", 1)
        assert "HashTable" in repr(ht)