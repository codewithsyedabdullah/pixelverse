"""DSA laboratory: live visualisation of data-structure operations (M9).

The panel lets the user run a demonstration (queue, stack, heap, hash table,
linked list, tree, graph, trie) and watch the structure's contents render in
real time.  Each demo returns a list of "frames" — snapshots of the structure
at each step — which the panel animates.
"""

from __future__ import annotations

from typing import Callable, List, Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QPlainTextEdit,
)

from dsa.queue import Queue
from dsa.stack import Stack
from dsa.heap import Heap
from dsa.hash_table import HashTable
from dsa.linked_list import LinkedList


class DSALabPanel(QWidget):
    """A widget that runs and visualises DSA demonstrations."""

    DEMOS: dict[str, Callable[[], List[str]]] = {}

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._frames: List[str] = []
        self._index = 0
        self._timer = QTimer(self)
        self._timer.setInterval(400)
        self._timer.timeout.connect(self._advance)
        self._setup_ui()
        self._populate_demos()

    # ------------------------------------------------------------------ UI
    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title = QLabel("DSA Laboratory")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        control_row = QHBoxLayout()
        self._demo_combo = QComboBox()
        self._demo_combo.currentIndexChanged.connect(self._on_demo_changed)
        control_row.addWidget(self._demo_combo, 1)

        self._run_button = QPushButton("Run")
        self._run_button.clicked.connect(self._run_selected)
        control_row.addWidget(self._run_button)

        self._step_button = QPushButton("Step")
        self._step_button.clicked.connect(self._step)
        control_row.addWidget(self._step_button)

        layout.addLayout(control_row)

        self._output = QPlainTextEdit()
        self._output.setReadOnly(True)
        self._output.setFont(self._output.font())
        layout.addWidget(self._output, 1)

        self._info = QLabel("Select a demo and press Run.")
        self._info.setStyleSheet("color: #888;")
        layout.addWidget(self._info)

    # ------------------------------------------------------------------ demos
    def _populate_demos(self) -> None:
        self.DEMOS = {
            "Queue": self._demo_queue,
            "Stack": self._demo_stack,
            "Heap": self._demo_heap,
            "Hash Table": self._demo_hash_table,
            "Linked List": self._demo_linked_list,
        }
        for name in self.DEMOS:
            self._demo_combo.addItem(name)

    def _demo_queue(self) -> List[str]:
        frames: List[str] = []
        q: Queue[str] = Queue()
        frames.append(self._render("Queue", "empty"))
        for value in ("alpha", "beta", "gamma"):
            q.enqueue(value)
            frames.append(self._render("Queue", f"enqueued {value}"))
        while q:
            q.dequeue()
            frames.append(self._render("Queue", "dequeue"))
        return frames

    def _demo_stack(self) -> List[str]:
        frames: List[str] = []
        s: Stack[str] = Stack()
        frames.append(self._render("Stack", "empty"))
        for value in ("one", "two", "three"):
            s.push(value)
            frames.append(self._render("Stack", f"pushed {value}"))
        while s:
            s.pop()
            frames.append(self._render("Stack", "pop"))
        return frames

    def _demo_heap(self) -> List[str]:
        frames: List[str] = []
        h: Heap[int] = Heap()
        frames.append(self._render("Heap", "empty"))
        for value in (7, 3, 9, 1, 5):
            h.push(value)
            frames.append(self._render("Heap", f"push {value}"))
        while h:
            h.pop()
            frames.append(self._render("Heap", "pop"))
        return frames

    def _demo_hash_table(self) -> List[str]:
        frames: List[str] = []
        ht: HashTable[str, int] = HashTable()
        frames.append(self._render("HashTable", "empty"))
        for key, val in (("apple", 3), ("banana", 5), ("cherry", 2)):
            ht.put(key, val)
            frames.append(self._render("HashTable", f"put {key}={val}"))
        ht.remove("banana")
        frames.append(self._render("HashTable", "remove banana"))
        return frames

    def _demo_linked_list(self) -> List[str]:
        frames: List[str] = []
        ll: LinkedList[str] = LinkedList()
        frames.append(self._render("LinkedList", "empty"))
        for value in ("first", "second", "third"):
            ll.append(value)
            frames.append(self._render("LinkedList", f"append {value}"))
        ll.remove("second")
        frames.append(self._render("LinkedList", "remove second"))
        return frames

    # ------------------------------------------------------------------ render
    def _render(self, name: str, action: str) -> str:
        return f"{name}: {action}"

    # ------------------------------------------------------------------ control
    def _run_selected(self) -> None:
        name = self._demo_combo.currentText()
        if name not in self.DEMOS:
            return
        self._frames = self.DEMOS[name]()
        self._index = 0
        self._info.setText(f"Running {name} ({len(self._frames)} frames)")
        self._show_frame()
        if len(self._frames) > 1:
            self._timer.start()

    def _step(self) -> None:
        if not self._frames:
            self._run_selected()
            return
        self._timer.stop()
        self._index = min(self._index + 1, len(self._frames) - 1)
        self._show_frame()

    def _advance(self) -> None:
        self._index += 1
        if self._index >= len(self._frames):
            self._timer.stop()
            return
        self._show_frame()

    def _on_demo_changed(self) -> None:
        self._timer.stop()
        self._frames = []
        self._index = 0
        self._output.setPlainText("")

    def _show_frame(self) -> None:
        if not self._frames:
            return
        self._output.setPlainText(self._frames[self._index])