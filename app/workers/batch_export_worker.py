from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List, Optional

from PySide6.QtCore import QThread, Signal

from app.core.discord_client import DiscordAPIError
from app.core.models import ExportOptions, ExportResult
from app.workers.export_pipeline import ExportCancelled, execute_export


@dataclass(frozen=True)
class BatchExportTarget:
    stable_id: str
    label: str
    options: ExportOptions


@dataclass(frozen=True)
class BatchExportItemResult:
    stable_id: str
    label: str
    success: bool
    error: Optional[str] = None
    result: Optional[ExportResult] = None


@dataclass(frozen=True)
class BatchExportResult:
    attempted: int
    succeeded: int
    failed: int
    cancelled: bool
    last_success: Optional[ExportResult]
    items: list[BatchExportItemResult]


class BatchExportWorker(QThread):
    status = Signal(str)
    error = Signal(str)
    preview = Signal(str)
    item_started = Signal(int, int, str)
    batch_progress = Signal(int, int)
    finished = Signal(object)

    def __init__(self, token: str, targets: List[BatchExportTarget]):
        super().__init__()
        self._token = token
        self._targets = targets
        self._cancel_requested = False

    def cancel(self) -> None:
        self._cancel_requested = True

    def run(self) -> None:
        logger = logging.getLogger("discordsorter.batch")
        total = len(self._targets)
        attempted = 0
        succeeded = 0
        failed = 0
        cancelled = False
        last_success: Optional[ExportResult] = None
        item_results: list[BatchExportItemResult] = []

        try:
            logger.info("Batch export started. Total items: %s", total)
            self.status.emit(f"Batch export started: {total} items")
            self.batch_progress.emit(0, total)

            for idx, target in enumerate(self._targets, start=1):
                if self._cancel_requested:
                    cancelled = True
                    logger.warning(
                        "Batch export cancelled before item %s/%s. Attempted=%s Succeeded=%s Failed=%s",
                        idx,
                        total,
                        attempted,
                        succeeded,
                        failed,
                    )
                    break

                self.item_started.emit(idx, total, target.label)
                logger.info("Batch item %s/%s started: %s", idx, total, target.label)

                try:
                    result = execute_export(
                        self._token,
                        target.options,
                        status_callback=lambda msg, i=idx, t=total: self.status.emit(
                            f"[{i}/{t}] {msg}"
                        ),
                        preview_callback=self.preview.emit,
                    )
                    attempted += 1
                    succeeded += 1
                    last_success = result
                    item_results.append(
                        BatchExportItemResult(
                            stable_id=target.stable_id,
                            label=target.label,
                            success=True,
                            result=result,
                        )
                    )
                    logger.info("Batch item %s/%s completed: %s", idx, total, target.label)
                except (DiscordAPIError, ExportCancelled) as exc:
                    attempted += 1
                    failed += 1
                    item_results.append(
                        BatchExportItemResult(
                            stable_id=target.stable_id,
                            label=target.label,
                            success=False,
                            error=str(exc),
                        )
                    )
                    logger.error("Batch item %s/%s failed: %s | %s", idx, total, target.label, exc)
                    self.status.emit(f"[{idx}/{total}] Failed: {target.label} ({exc})")
                except Exception as exc:  # pragma: no cover - defensive
                    attempted += 1
                    failed += 1
                    item_results.append(
                        BatchExportItemResult(
                            stable_id=target.stable_id,
                            label=target.label,
                            success=False,
                            error=f"Unexpected error: {exc}",
                        )
                    )
                    logger.exception(
                        "Unexpected batch error on item %s/%s: %s", idx, total, target.label
                    )
                    self.status.emit(f"[{idx}/{total}] Failed: {target.label} (Unexpected error)")

                self.batch_progress.emit(attempted, total)

            if cancelled:
                logger.warning(
                    "Batch export cancelled. Attempted=%s Succeeded=%s Failed=%s Total=%s",
                    attempted,
                    succeeded,
                    failed,
                    total,
                )
                self.status.emit(
                    f"Batch export cancelled. Attempted {attempted}/{total}, succeeded {succeeded}, failed {failed}"
                )
            else:
                logger.info(
                    "Batch export completed. Attempted=%s Succeeded=%s Failed=%s Total=%s",
                    attempted,
                    succeeded,
                    failed,
                    total,
                )
                self.status.emit(
                    f"Batch export complete. Attempted {attempted}/{total}, succeeded {succeeded}, failed {failed}"
                )

            self.finished.emit(
                BatchExportResult(
                    attempted=attempted,
                    succeeded=succeeded,
                    failed=failed,
                    cancelled=cancelled,
                    last_success=last_success,
                    items=item_results,
                )
            )
        except Exception as exc:  # pragma: no cover - defensive
            self.error.emit(f"Unexpected batch error: {exc}")
            logger.exception("Unexpected batch worker failure.")
