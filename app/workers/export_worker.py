from __future__ import annotations

import logging

from PySide6.QtCore import QThread, Signal

from app.core.discord_client import DiscordAPIError
from app.core.models import ExportOptions, ExportResult
from app.workers.export_pipeline import ExportCancelled, execute_export


class ExportWorker(QThread):
    status = Signal(str)
    error = Signal(str)
    preview = Signal(str)
    finished = Signal(ExportResult)

    def __init__(self, token: str, options: ExportOptions):
        super().__init__()
        self._token = token
        self._options = options

    def run(self) -> None:
        logger = logging.getLogger("discordsorter.export")
        try:
            result = execute_export(
                self._token,
                self._options,
                status_callback=self.status.emit,
                preview_callback=self.preview.emit,
            )
            self.finished.emit(result)
        except DiscordAPIError as exc:
            self.error.emit(str(exc))
            logger.error("Export failed: %s", exc)
        except ExportCancelled as exc:
            self.error.emit(str(exc))
            logger.info("Export cancelled: %s", exc)
        except Exception as exc:  # pragma: no cover - defensive
            self.error.emit(f"Unexpected error: {exc}")
            logger.exception("Unexpected export error.")
