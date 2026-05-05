from __future__ import annotations

import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from app.core.models import ExportOptions
from app.workers.export_pipeline import execute_export


class _FakeDiscordClient:
    def __init__(self, token: str):
        self.token = token

    def validate_token(self) -> None:
        return None

    def get_channel_messages(self, channel_id: str, before_id=None, limit: int = 100):
        return [
            {
                "id": "100",
                "timestamp": "2026-01-10T12:00:00.000000+00:00",
                "content": "hello",
                "author": {"username": "Fish", "discriminator": "1234"},
                "attachments": [],
            }
        ] if before_id is None else []

    def close(self) -> None:
        return None


class ExportPipelineTests(unittest.TestCase):
    def test_execute_export_writes_fixed_layout_and_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            options = ExportOptions(
                channel_id="333",
                before_dt=datetime(2026, 2, 11, 23, 59, tzinfo=timezone.utc),
                after_dt=datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc),
                export_json=True,
                export_txt=True,
                export_attachments=False,
                include_edits=False,
                include_pins=False,
                include_replies=False,
                output_root=tmpdir,
                target_kind="guild",
                dm_name=None,
                guild_id="111",
                guild_name="My Server",
                category_id="222",
                category_name="Work",
                channel_name="general",
                export_label="",
            )

            with patch("app.workers.export_pipeline.DiscordClient", _FakeDiscordClient):
                result = execute_export(
                    "token",
                    options,
                    export_started_at=datetime(2026, 5, 5, 10, 30, 45, 123456),
                )

            self.assertTrue(result.txt_path.endswith(os.path.join("messages.txt")))
            self.assertTrue(result.json_path.endswith(os.path.join("messages.json")))
            self.assertTrue(result.metadata_path.endswith(os.path.join("metadata.json")))
            self.assertEqual(result.export_dir, os.path.dirname(result.txt_path))

            with open(result.metadata_path, "r", encoding="utf-8") as handle:
                metadata = json.load(handle)

            self.assertEqual(metadata["target"]["guild"]["id"], "111")
            self.assertEqual(metadata["target"]["category"]["id"], "222")
            self.assertEqual(metadata["target"]["channel"]["id"], "333")
            self.assertEqual(metadata["artifacts"]["txt"], "messages.txt")
            self.assertEqual(metadata["message_count"], 1)
            self.assertEqual(
                metadata["package"]["export_dir_name"],
                "export_20260505_103045_123456",
            )
            self.assertEqual(metadata["package"]["export_dir"], result.export_dir)

    def test_attachment_export_uses_attachment_id_to_avoid_collisions(self) -> None:
        from app.core.exporter import export_attachments

        class _FakeResponse:
            status_code = 200

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def iter_content(self, chunk_size: int = 8192):
                yield b"data"

        class _FakeSession:
            def get(self, url: str, stream: bool = True, timeout: int = 30):
                return _FakeResponse()

        messages = [
            {
                "id": "10",
                "attachments": [
                    {"id": "a1", "filename": "same.png", "url": "https://example.com/1"},
                    {"id": "a2", "filename": "same.png", "url": "https://example.com/2"},
                ],
            }
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("app.core.exporter.requests.Session", return_value=_FakeSession()):
                saved = export_attachments(messages, tmpdir)

            self.assertEqual(saved, 2)
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "10_a1_same.png")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "10_a2_same.png")))


if __name__ == "__main__":
    unittest.main()
