from __future__ import annotations

import logging
from typing import Any, Dict, Tuple

from .utils import format_timestamp, parse_discord_timestamp


def _author_label(author: Dict[str, Any]) -> str:
    username = author.get("username", "Unknown")
    discriminator = author.get("discriminator")
    if discriminator is None:
        return username
    return f"{username}#{discriminator}"


def _member_nick(message: Dict[str, Any]) -> str | None:
    member = message.get("member") or {}
    nick = member.get("nick")
    if nick:
        return nick
    return None


def _message_content(message: Dict[str, Any]) -> str:
    content = message.get("content") or ""
    if content:
        return content
    attachments = message.get("attachments") or []
    if attachments:
        return "[Attachments]"
    return "[No content]"


def format_message(
    message: Dict[str, Any],
    lookup: Dict[str, Tuple[str, str]],
    include_edits: bool,
    include_pins: bool,
    include_replies: bool,
) -> str:
    logger = logging.getLogger("discordsorter.formatter")
    author = message.get("author") or {}
    label = _author_label(author)
    nickname = _member_nick(message)
    if nickname:
        label = f"{label} ({nickname})"

    created_ts = format_timestamp(parse_discord_timestamp(message.get("timestamp")))
    prefix = "[PINNED] " if include_pins and message.get("pinned") else ""

    header = f"{prefix}{label} {created_ts}"
    if include_edits and message.get("edited_timestamp"):
        edited_ts = format_timestamp(parse_discord_timestamp(message.get("edited_timestamp")))
        header = f"{header} (edited at {edited_ts})"

    lines = [header]

    if include_replies and message.get("message_reference"):
        ref_id = message.get("message_reference", {}).get("message_id")
        ref_author = "Unknown User"
        ref_content = "Original message not found"
        if message.get("referenced_message"):
            ref = message.get("referenced_message")
            ref_author = _author_label(ref.get("author") or {})
            ref_content = _message_content(ref)
        elif ref_id and ref_id in lookup:
            ref_author, ref_content = lookup[ref_id]
        else:
            logger.warning("Reply reference not found for message id=%s", message.get("id"))
        lines.append(f"(Replying to {ref_author}: {ref_content})")

    lines.append(_message_content(message))
    return "\n".join(lines)
