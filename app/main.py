from __future__ import annotations

import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from app.core.logging_setup import setup_logging
from app.core.paths import resolve_default_paths
from app.core.resources import resource_path
from app.ui.main_window import MainWindow
from app.ui.styles import STYLESHEET


def main() -> int:
    defaults = resolve_default_paths()
    controller = setup_logging(log_dir=defaults.logs_dir)
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    icon_path = resource_path(os.path.join("exe", "app_logo.ico"))
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    window = MainWindow(
        default_export_root=defaults.export_root,
        logs_dir=defaults.logs_dir,
        export_default_fallback_used=defaults.export_fallback_used,
        logs_fallback_used=defaults.logs_fallback_used,
        startup_warnings=defaults.warnings,
    )
    window.show()
    if controller:
        app.aboutToQuit.connect(controller.stop)
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
