"""Simulation event queue backed by the from-scratch :class:`dsa.queue.Queue`.

Events are processed FIFO each tick.  Each event carries a *priority* so that
high-priority events (e.g. predator attacks) are dispatched before
low-priority ones (e.g. idle plant growth) when both are enqueued in the same
tick.
"""

from __future__ import annotations

from typing import Any, Callable, Optional

from dsa.queue import Queue


class Event:
    """A single simulation event."""

    __slots__ = ("type", "payload", "priority", "tick")

    def __init__(self, type: str, payload: Any = None, priority: int = 0) -> None:
        self.type = type
        self.payload = payload
        self.priority = priority
        self.tick: int = 0

    def __repr__(self) -> str:
        return f"Event({self.type!r}, priority={self.priority})"


class EventManager:
    """Holds pending events for the current tick and dispatches them in order.

    Higher-priority events are dispatched first.  Within the same priority the
    FIFO order of :class:`dsa.queue.Queue` is preserved.
    """

    def __init__(self) -> None:
        self._pending: Queue[Event] = Queue()
        self._current_tick = 0
        self._handlers: dict[str, Callable[[Event], None]] = {}

    # ------------------------------------------------------------------ handlers
    def register(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """Register a handler for *event_type*."""
        self._handlers[event_type] = handler

    def unregister(self, event_type: str) -> None:
        self._handlers.pop(event_type, None)

    # ------------------------------------------------------------------ enqueue
    def enqueue(self, event: Event) -> None:
        """Add *event* to the pending queue for the current tick."""
        event.tick = self._current_tick
        self._pending.enqueue(event)

    def enqueue_at(self, event: Event, tick: int) -> None:
        """Schedule *event* for a future tick (stored in the pending queue)."""
        event.tick = tick
        self._pending.enqueue(event)

    # ------------------------------------------------------------------ dispatch
    def dispatch(self) -> list[Event]:
        """Dispatch all pending events for the current tick, in priority order.

        Returns the list of events that were actually handled.
        """
        # Bucket events by priority, then drain each bucket FIFO.
        buckets: dict[int, list[Event]] = {}
        due_now: list[Event] = []
        leftover: Queue[Event] = Queue()

        while self._pending:
            event = self._pending.dequeue()
            assert event is not None
            if event.tick <= self._current_tick:
                buckets.setdefault(event.priority, []).append(event)
            else:
                leftover.enqueue(event)

        self._pending = leftover

        handled: list[Event] = []
        for priority in sorted(buckets, reverse=True):
            for event in buckets[priority]:
                handler = self._handlers.get(event.type)
                if handler is not None:
                    handler(event)
                handled.append(event)
        return handled

    # ------------------------------------------------------------------ lifecycle
    def begin_tick(self, tick: int) -> None:
        self._current_tick = tick

    def clear(self) -> None:
        self._pending.clear()

    def __len__(self) -> int:
        return len(self._pending)