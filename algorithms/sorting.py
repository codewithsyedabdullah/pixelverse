"""Classic comparison sorts, implemented from scratch.

Every function sorts a list in place and returns it for convenience.  The
``key`` argument mirrors ``list.sort``: a callable extracting a comparison key
from each element.
"""

from __future__ import annotations

from typing import Callable, List, TypeVar

T = TypeVar("T")
Key = Callable[[T], object]


def _key_func(key: Key[T] | None) -> Key[T]:
    return key if key is not None else (lambda x: x)  # type: ignore[return-value]


def bubble_sort(arr: List[T], key: Key[T] | None = None) -> List[T]:
    """Bubble sort — O(n^2) time, O(1) space, stable."""
    k = _key_func(key)
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if k(arr[j]) > k(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr: List[T], key: Key[T] | None = None) -> List[T]:
    """Selection sort — O(n^2) time, O(1) space, not stable."""
    k = _key_func(key)
    n = len(arr)
    for i in range(n):
        best = i
        for j in range(i + 1, n):
            if k(arr[j]) < k(arr[best]):
                best = j
        arr[i], arr[best] = arr[best], arr[i]
    return arr


def insertion_sort(arr: List[T], key: Key[T] | None = None) -> List[T]:
    """Insertion sort — O(n^2) worst, O(n) best, O(1) space, stable."""
    k = _key_func(key)
    for i in range(1, len(arr)):
        val = arr[i]
        j = i - 1
        while j >= 0 and k(arr[j]) > k(val):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = val
    return arr


def _merge(arr: List[T], lo: int, mid: int, hi: int, k: Key[T]) -> None:
    left = arr[lo:mid + 1]
    right = arr[mid + 1:hi + 1]
    i = j = 0
    idx = lo
    while i < len(left) and j < len(right):
        if k(left[i]) <= k(right[j]):
            arr[idx] = left[i]
            i += 1
        else:
            arr[idx] = right[j]
            j += 1
        idx += 1
    while i < len(left):
        arr[idx] = left[i]
        i += 1
        idx += 1
    while j < len(right):
        arr[idx] = right[j]
        j += 1
        idx += 1


def _merge_sort(arr: List[T], lo: int, hi: int, k: Key[T]) -> None:
    if lo >= hi:
        return
    mid = (lo + hi) // 2
    _merge_sort(arr, lo, mid, k)
    _merge_sort(arr, mid + 1, hi, k)
    _merge(arr, lo, mid, hi, k)


def merge_sort(arr: List[T], key: Key[T] | None = None) -> List[T]:
    """Merge sort — O(n log n) time, O(n) space, stable."""
    _merge_sort(arr, 0, len(arr) - 1, _key_func(key))
    return arr


def _partition(arr: List[T], lo: int, hi: int, k: Key[T]) -> int:
    pivot = arr[hi]
    i = lo - 1
    for j in range(lo, hi):
        if k(arr[j]) <= k(pivot):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


def _quick_sort(arr: List[T], lo: int, hi: int, k: Key[T]) -> None:
    if lo < hi:
        p = _partition(arr, lo, hi, k)
        _quick_sort(arr, lo, p - 1, k)
        _quick_sort(arr, p + 1, hi, k)


def quick_sort(arr: List[T], key: Key[T] | None = None) -> List[T]:
    """Quicksort — O(n log n) average, O(n^2) worst, O(log n) stack, not stable."""
    _quick_sort(arr, 0, len(arr) - 1, _key_func(key))
    return arr


def heap_sort(arr: List[T], key: Key[T] | None = None) -> List[T]:
    """Heapsort — O(n log n) time, O(1) space, not stable.

    Builds a max-heap and repeatedly extracts the maximum to the end.
    """
    from dsa.heap import Heap, HeapEntry

    k = _key_func(key)
    heap: Heap[T] = Heap()
    for item in arr:
        heap.push(item, -k(item))  # type: ignore[arg-type]
    for i in range(len(arr) - 1, -1, -1):
        arr[i] = heap.pop()  # type: ignore[assignment]
    return arr