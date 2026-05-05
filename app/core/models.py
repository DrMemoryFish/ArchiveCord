from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class ConversationItem:
    id: str
    name: str
    kind: str  # "dm" or "guild_channel"
    guild_id: Optional[str] = None
    guild_name: Optional[str] = None


@dataclass(frozen=True)
class ExportOptions:
    channel_id: str
    before_dt: Optional[datetime]
    after_dt: Optional[datetime]
    export_json: bool
    export_txt: bool
    export_attachments: bool
    include_edits: bool
    include_pins: bool
    include_replies: bool
    output_root: str
    target_kind: str
    dm_name: Optional[str]
    guild_id: Optional[str]
    guild_name: Optional[str]
    category_id: Optional[str]
    category_name: Optional[str]
    channel_name: Optional[str]
    export_label: str


@dataclass(frozen=True)
class ExportResult:
    formatted_text: str
    messages: list
    export_dir: str
    json_path: Optional[str]
    txt_path: Optional[str]
    metadata_path: str
    attachments_dir: Optional[str]
    attachments_saved: int
