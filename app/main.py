from __future__ import annotations

import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from app.core.logging_setup import setup_logging
from app.core.resources import resource_path
from app.ui.main_window import MainWindow
from app.ui.styles import STYLESHEET


def main() -> int:
    controller = setup_logging()
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    icon_path = resource_path(os.path.join("exe", "app_logo.ico"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    window = MainWindow()
    window.show()
    if controller:
        app.aboutToQuit.connect(controller.stop)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
