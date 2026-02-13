from __future__ import annotations

import logging
import os
from typing import Callable, Dict, Optional, Tuple

from app.core.discord_client import DiscordClient
from app.core.exporter import export_attachments, save_json, save_txt
from app.core.formatter import format_message
from app.core.models import ExportOptions, ExportResult
from app.core.utils import parse_discord_timestamp


StatusCallback = Callable[[str], None]
PreviewCallback = Callable[[str], None]
CancelCallback = Callable[[], bool]


class ExportCancelled(RuntimeError):
    pass


def _emit_status(callback: Optional[StatusCallback], message: str) -> None:
    if callback:
        callback(message)


def _emit_preview(callback: Optional[PreviewCallback], content: str) -> None:
    if callback:
        callback(content)


def _check_cancel(cancel_check: Optional[CancelCallback]) -> None:
    if cancel_check and cancel_check():
        raise ExportCancelled("Export cancelled.")


def execute_export(
    token: str,
    options: ExportOptions,
    *,
    status_callback: Optional[StatusCallback] = None,
    preview_callback: Optional[PreviewCallback] = None,
    cancel_check: Optional[CancelCallback] = None,
) -> ExportResult:
    client = None
    logger = logging.getLogger("discordsorter.export")
    try:
        client = DiscordClient(token)
        _emit_status(status_callback, "Validating token...")
        logger.info("Validating token.")
        client.validate_token()
        _check_cancel(cancel_check)

        _emit_status(status_callback, "Fetching messages...")
        logger.info("Fetching messages for channel %s", options.channel_id)
        messages: list = []
        before_id = None
        stop_due_to_after = False

        while True:
            _check_cancel(cancel_check)
            batch = client.get_channel_messages(options.channel_id, before_id=before_id, limit=100)
            if not batch:
                break

            for message in batch:
                ts = parse_discord_timestamp(message.get("timestamp"))
                if options.before_dt and ts > options.before_dt:
                    continue
                if options.after_dt and ts < options.after_dt:
                    stop_due_to_after = True
                    continue
                messages.append(message)

            before_id = batch[-1].get("id")
            if stop_due_to_after:
                break

        _emit_status(status_callback, "Formatting output...")
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

        messages_sorted = sorted(
            messages,
            key=lambda m: parse_discord_timestamp(m.get("timestamp")),
        )

        blocks = []
        for idx, message in enumerate(messages_sorted, start=1):
            _check_cancel(cancel_check)
            blocks.append(
                format_message(
                    message,
                    lookup,
                    include_edits=options.include_edits,
                    include_pins=options.include_pins,
                    include_replies=options.include_replies,
                )
            )
            if idx % 200 == 0:
                _emit_preview(preview_callback, "\n\n".join(blocks))
                logger.debug("Formatted %s messages...", idx)

        formatted_text = "\n\n".join(blocks)
        _emit_preview(preview_callback, formatted_text)

        json_path = None
        txt_path = None
        attachments_dir = None
        attachments_saved = 0

        if options.export_json:
            _check_cancel(cancel_check)
            json_path = save_json(
                messages_sorted,
                os.path.join(options.output_dir, f"{options.base_filename}.json"),
            )

        if options.export_txt:
            _check_cancel(cancel_check)
            txt_path = save_txt(
                formatted_text,
                os.path.join(options.output_dir, f"{options.base_filename}.txt"),
            )

        if options.export_attachments:
            _check_cancel(cancel_check)
            attachments_dir = os.path.join(
                options.output_dir, f"{options.base_filename}_attachments"
            )
            attachments_saved = export_attachments(messages_sorted, attachments_dir)

        _emit_status(status_callback, "Export complete.")
        logger.info(
            "Export finished. JSON=%s TXT=%s Attachments=%s",
            json_path or "none",
            txt_path or "none",
            attachments_dir or "none",
        )
        return ExportResult(
            formatted_text=formatted_text,
            messages=messages_sorted,
            json_path=json_path,
            txt_path=txt_path,
            attachments_dir=attachments_dir,
            attachments_saved=attachments_saved,
        )
    finally:
        if client:
            client.close()
