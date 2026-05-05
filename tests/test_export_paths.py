from __future__ import annotations

import os
import unittest
from datetime import datetime, timezone

from app.core.models import ExportOptions


class ExportPathBuilderTests(unittest.TestCase):
    def test_builds_category_aware_guild_export_paths_with_stable_ids(self) -> None:
        from app.core.export_paths import build_export_paths

        options = ExportOptions(
            channel_id="333",
            before_dt=datetime(2026, 2, 11, 23, 59, tzinfo=timezone.utc),
            after_dt=datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc),
            export_json=True,
            export_txt=True,
            export_attachments=True,
            include_edits=False,
            include_pins=False,
            include_replies=False,
            output_root="C:/exports",
            target_kind="guild",
            dm_name=None,
            guild_id="111",
            guild_name="My Server",
            category_id="222",
            category_name="Work",
            channel_name="general",
            export_label="Sprint Review",
        )

        paths = build_export_paths(options, export_started_at=datetime(2026, 5, 5, 10, 30, 45))

        self.assertEqual(
            paths.conversation_dir,
            os.path.join(
                "C:/exports",
                "Servers",
                "My Server [guild_111]",
                "Work [category_222]",
                "general [channel_333]",
            ),
        )
        self.assertEqual(
            paths.export_dir,
            os.path.join(
                "C:/exports",
                "Servers",
                "My Server [guild_111]",
                "Work [category_222]",
                "general [channel_333]",
                "export_20260505_103045_sprint_review",
            ),
        )
        self.assertEqual(paths.txt_path, os.path.join(paths.export_dir, "messages.txt"))
        self.assertEqual(paths.json_path, os.path.join(paths.export_dir, "messages.json"))
        self.assertEqual(paths.attachments_dir, os.path.join(paths.export_dir, "attachments"))
        self.assertEqual(paths.metadata_path, os.path.join(paths.export_dir, "metadata.json"))

    def test_empty_dm_name_falls_back_to_stable_unknown_segment(self) -> None:
        from app.core.export_paths import build_export_paths

        options = ExportOptions(
            channel_id="789",
            before_dt=None,
            after_dt=None,
            export_json=True,
            export_txt=False,
            export_attachments=False,
            include_edits=False,
            include_pins=False,
            include_replies=False,
            output_root="C:/exports",
            target_kind="dm",
            dm_name="...",
            guild_id=None,
            guild_name=None,
            category_id=None,
            category_name=None,
            channel_name=None,
            export_label="",
        )

        paths = build_export_paths(options, export_started_at=datetime(2026, 5, 5, 11, 0, 0))

        self.assertEqual(
            paths.conversation_dir,
            os.path.join("C:/exports", "DMs", "unknown-dm [channel_789]"),
        )


if __name__ == "__main__":
    unittest.main()
