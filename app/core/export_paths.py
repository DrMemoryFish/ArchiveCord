from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime

from app.core.models import ExportOptions


WINDOWS_RESERVED_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}


@dataclass(frozen=True)
class ExportPaths:
    conversation_dir: str
    export_dir: str
    txt_path: str
    json_path: str
    metadata_path: str
    attachments_dir: str


def _clean_segment(value: str, fallback: str) -> str:
    raw = (value or "").strip()
    cleaned = re.sub(r'[<>:"/\\\\|?*]+', "_", raw).strip(" .")
    if not cleaned:
        cleaned = fallback
    if cleaned.upper() in WINDOWS_RESERVED_NAMES:
        cleaned = f"{cleaned}_"
    return cleaned


def _slugify_label(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return cleaned[:40] or "export"


def _entity_segment(name: str | None, entity_key: str, entity_id: str, fallback: str) -> str:
    label = _clean_segment(name or "", fallback)
    return f"{label} [{entity_key}_{entity_id}]"


def build_export_paths(options: ExportOptions, *, export_started_at: datetime) -> ExportPaths:
    if options.target_kind == "dm":
        conversation_dir = os.path.join(
            options.output_root,
            "DMs",
            _entity_segment(options.dm_name, "channel", options.channel_id, "unknown-dm"),
        )
    else:
        guild_segment = _entity_segment(options.guild_name, "guild", options.guild_id or "unknown", "unknown-server")
        channel_segment = _entity_segment(
            options.channel_name,
            "channel",
            options.channel_id,
            "unknown-channel",
        )
        parts = [options.output_root, "Servers", guild_segment]
        if options.category_id:
            parts.append(
                _entity_segment(
                    options.category_name,
                    "category",
                    options.category_id,
                    "unknown-category",
                )
            )
        parts.append(channel_segment)
        conversation_dir = os.path.join(*parts)

    export_dir_name = f"export_{export_started_at.strftime('%Y%m%d_%H%M%S_%f')}"
    if options.export_label.strip():
        export_dir_name = f"{export_dir_name}_{_slugify_label(options.export_label)}"

    export_dir = os.path.join(conversation_dir, export_dir_name)
    return ExportPaths(
        conversation_dir=conversation_dir,
        export_dir=export_dir,
        txt_path=os.path.join(export_dir, "messages.txt"),
        json_path=os.path.join(export_dir, "messages.json"),
        metadata_path=os.path.join(export_dir, "metadata.json"),
        attachments_dir=os.path.join(export_dir, "attachments"),
    )
