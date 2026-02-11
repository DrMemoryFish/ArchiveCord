from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Optional


def local_tzinfo():
    return datetime.now().astimezone().tzinfo


def parse_discord_timestamp(value: str) -> datetime:
    if not value:
        raise ValueError("timestamp is empty")
    # Discord returns ISO 8601 with Z
    if value.endswith("Z"):
        value = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(value)
    return dt.astimezone(local_tzinfo())


def format_timestamp(dt: datetime) -> str:
    return dt.astimezone(local_tzinfo()).strftime("%d-%m-%Y %I:%M %p")


def format_log_timestamp(dt: datetime) -> str:
    return dt.astimezone(local_tzinfo()).strftime("%d-%m-%Y %H:%M:%S")


def build_dt(date_value, time_value) -> datetime:
    tz = local_tzinfo()
    return datetime.combine(date_value, time_value).replace(tzinfo=tz)


def safe_filename(name: str) -> str:
    if not name:
        return "file"
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._")
    return cleaned or "file"


def sanitize_path_segment(value: str) -> str:
    if not value:
        return "file"
    # Replace characters invalid on Windows/macOS/Linux file systems.
    cleaned = re.sub(r'[<>:"/\\\\|?*]+', "_", value)
    cleaned = cleaned.strip(" .")
    return cleaned or "file"


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path


def coalesce_text(value: Optional[str]) -> str:
    return value if value else ""
