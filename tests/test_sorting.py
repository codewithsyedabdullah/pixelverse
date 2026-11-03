"""Tests for algorithms/sorting.py."""

from __future__ import annotations

import pytest

from algorithms.sorting import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    heap_sort,
)

SORTS = [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort, heap_sort]


@pytest.mark.parametrize("sort_fn", SORTS)
def test_empty(sort_fn):
    arr: list[int] = []
    assert sort_fn(arr) == []


@pytest.mark.parametrize("sort_fn", SORTS)
def test_single(sort_fn):
    arr = [1]
    assert sort_fn(arr) == [1]


@pytest.mark.parametrize("sort_fn", SORTS)
def test_sorted(sort_fn):
    arr = [3, 1, 2]
    assert sort_fn(arr) == [1, 2, 3]


@pytest.mark.parametrize("sort_fn", SORTS)
def test_duplicates(sort_fn):
    arr = [5, 5, 1, 1, 3]
    assert sort_fn(arr) == [1, 1, 3, 5, 5]


@pytest.mark.parametrize("sort_fn", SORTS)
def test_reverse(sort_fn):
    arr = list(range(20, 0, -1))
    assert sort_fn(arr) == list(range(1, 21))


@pytest.mark.parametrize("sort_fn", SORTS)
def test_key(sort_fn):
    arr = [(1, "b"), (2, "a"), (0, "c")]
    out = sort_fn(arr, key=lambda t: t[0])
    assert out == [(0, "c"), (1, "b"), (2, "a")]


def test_insertion_stable():
    pairs = [(1, "a"), (1, "b"), (0, "c")]
    out = insertion_sort(pairs, key=lambda p: p[0])
    assert out == [(0, "c"), (1, "a"), (1, "b")]


def test_merge_stable():
    pairs = [(1, "a"), (1, "b"), (0, "c")]
    out = merge_sort(pairs, key=lambda p: p[0])
    assert out == [(0, "c"), (1, "a"), (1, "b")]


def test_large_random():
    import random
    data = [random.randint(0, 1000) for _ in range(500)]
    expected = sorted(data)
    for sort_fn in SORTS:
        assert sort_fn(data[:]) == expected