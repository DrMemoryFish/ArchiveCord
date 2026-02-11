from __future__ import annotations

import logging
import os
from typing import Dict, Tuple

from PySide6.QtCore import QThread, Signal

from app.core.discord_client import DiscordAPIError, DiscordClient
from app.core.exporter import export_attachments, save_json, save_txt
from app.core.formatter import format_message
from app.core.models import ExportOptions, ExportResult
from app.core.utils import parse_discord_timestamp


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
        client = None
        logger = logging.getLogger("discordsorter.export")
        try:
            client = DiscordClient(self._token)
            self.status.emit("Validating token...")
            logger.info("Validating token.")
            client.validate_token()

            self.status.emit("Fetching messages...")
            logger.info("Fetching messages for channel %s", self._options.channel_id)
            messages: list = []
            before_id = None
            stop_due_to_after = False

            while True:
                batch = client.get_channel_messages(self._options.channel_id, before_id=before_id, limit=100)
                if not batch:
                    break

                for message in batch:
                    ts = parse_discord_timestamp(message.get("timestamp"))
                    if self._options.before_dt and ts > self._options.before_dt:
                        continue
                    if self._options.after_dt and ts < self._options.after_dt:
                        stop_due_to_after = True
                        continue
                    messages.append(message)

                before_id = batch[-1].get("id")
                if stop_due_to_after:
                    break

            self.status.emit("Formatting output...")
            logger.info("Formatting %s messages.", len(messages))
            lookup: Dict[str, Tuple[str, str]] = {}
            for message in messages:
                author = message.get("author") or {}
                if not author:
                    logger.warning("Message missing author field (id=%s).", message.get("id"))
                username = author.get("username", "Unknown")
                discriminator = author.get("discriminator")
                label = f"{username}#{discriminator}" if discriminator is not None else username
                content = message.get("content") or ""
                if not content and message.get("attachments"):
                    content = "[Attachments]"
                if not content:
                    content = "[No content]"
                lookup[message.get("id")] = (label, content)

            # Sort messages ascending by timestamp for output
            messages_sorted = sorted(
                messages,
                key=lambda m: parse_discord_timestamp(m.get("timestamp")),
            )

            blocks = []
            for idx, message in enumerate(messages_sorted, start=1):
                blocks.append(
                    format_message(
                        message,
                        lookup,
                        include_edits=self._options.include_edits,
                        include_pins=self._options.include_pins,
                        include_replies=self._options.include_replies,
                    )
                )
                if idx % 200 == 0:
                    self.preview.emit("\n\n".join(blocks))
                    logger.debug("Formatted %s messages...", idx)

            formatted_text = "\n\n".join(blocks)
            self.preview.emit(formatted_text)

            json_path = None
            txt_path = None
            attachments_dir = None
            attachments_saved = 0

            if self._options.export_json:
                json_path = save_json(
                    messages_sorted,
                    os.path.join(self._options.output_dir, f"{self._options.base_filename}.json"),
                )

            if self._options.export_txt:
                txt_path = save_txt(
                    formatted_text,
                    os.path.join(self._options.output_dir, f"{self._options.base_filename}.txt"),
                )

            if self._options.export_attachments:
                attachments_dir = os.path.join(
                    self._options.output_dir, f"{self._options.base_filename}_attachments"
                )
                attachments_saved = export_attachments(messages_sorted, attachments_dir)

            self.status.emit("Export complete.")
            logger.info(
                "Export finished. JSON=%s TXT=%s Attachments=%s",
                json_path or "none",
                txt_path or "none",
                attachments_dir or "none",
            )
            self.finished.emit(
                ExportResult(
                    formatted_text=formatted_text,
                    messages=messages_sorted,
                    json_path=json_path,
                    txt_path=txt_path,
                    attachments_dir=attachments_dir,
                    attachments_saved=attachments_saved,
                )
            )
        except DiscordAPIError as exc:
            self.error.emit(str(exc))
            logger.error("Export failed: %s", exc)
        except Exception as exc:  # pragma: no cover - defensive
            self.error.emit(f"Unexpected error: {exc}")
            logger.exception("Unexpected export error.")
        finally:
            if client:
                client.close()
