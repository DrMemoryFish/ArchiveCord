from __future__ import annotations

import logging
import logging.handlers
import os
import queue
from typing import Optional

from app.core.paths import resolve_default_paths
from app.core.utils import ensure_dir

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%d-%m-%Y %H:%M:%S"


class LoggingController:
    def __init__(self, listener: logging.handlers.QueueListener):
        self._listener = listener

    def stop(self) -> None:
        if self._listener:
            self._listener.stop()


def setup_logging(log_dir: str | None = None) -> Optional[LoggingController]:
    if getattr(setup_logging, "_configured", False):
        return None

    if not log_dir:
        log_dir = resolve_default_paths().logs_dir
    ensure_dir(log_dir)
    log_path = os.path.join(log_dir, "archivecord.log")

    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    log_queue: queue.Queue = queue.Queue(-1)
    queue_handler = logging.handlers.QueueHandler(log_queue)

    file_handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    listener = logging.handlers.QueueListener(log_queue, file_handler)
    listener.start()

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(queue_handler)

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    setup_logging._configured = True
    return LoggingController(listener)
