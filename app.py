"""PIXELVERSE application entry point.

Run with::

    python app.py

This module creates the QApplication, applies the dark theme, opens the
main window and starts the Qt event loop.  It contains no simulation logic.
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> int:
    """Create the application, open the main window and run the event loop."""
    # Qt uses sys.argv; allow future command-line options here.
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())