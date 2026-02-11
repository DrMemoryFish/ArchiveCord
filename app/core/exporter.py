from __future__ import annotations

import json
import os
from typing import Iterable

import logging
import requests

from .utils import ensure_dir, safe_filename


def save_json(messages: list, path: str) -> str:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(messages, handle, ensure_ascii=False, indent=2)
    return path


def save_txt(text: str, path: str) -> str:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return path


def export_attachments(messages: Iterable[dict], folder: str) -> int:
    ensure_dir(folder)
    logger = logging.getLogger("discordsorter.exporter")
    saved = 0
    session = requests.Session()
    for message in messages:
        attachments = message.get("attachments") or []
        for attachment in attachments:
            url = attachment.get("url")
            if not url:
                continue
            filename = safe_filename(attachment.get("filename") or "attachment")
            target = os.path.join(folder, f"{message.get('id')}_{filename}")
            if os.path.exists(target):
                continue
            try:
                with session.get(url, stream=True, timeout=30) as resp:
                    if resp.status_code != 200:
                        logger.warning("Attachment download failed (%s): %s", resp.status_code, url)
                        continue
                    with open(target, "wb") as handle:
                        for chunk in resp.iter_content(chunk_size=8192):
                            if chunk:
                                handle.write(chunk)
                saved += 1
            except Exception:
                logger.exception("Attachment download error: %s", url)
                continue
    return saved
