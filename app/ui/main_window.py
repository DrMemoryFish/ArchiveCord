from __future__ import annotations

import logging
import os
from datetime import datetime

from PySide6.QtCore import Qt, QDate, QTime, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDateEdit,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSplitter,
    QTabWidget,
    QTimeEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.core.models import ExportOptions
from app.core.token_store import TokenStoreError, delete_token, load_token, save_token
from app.core.utils import build_dt, ensure_dir, sanitize_path_segment
from app.ui.log_tab import LogTab
from app.workers.conversation_worker import ConversationWorker
from app.workers.export_worker import ExportWorker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Discord Conversation Processor")
        self.resize(1280, 820)
        self.setMinimumSize(1100, 720)

        self._conversation_worker: ConversationWorker | None = None
        self._export_worker: ExportWorker | None = None
        self._connected_user: dict | None = None
        self._logger = logging.getLogger("discordsorter.ui")

        self._build_ui()
        self._load_saved_token()

    def _build_ui(self) -> None:
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(14)

        # Top bar
        top_bar = QHBoxLayout()
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Discord user token")
        self.token_input.setEchoMode(QLineEdit.Password)

        self.remember_token = QCheckBox("Remember token (encrypted)")

        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.on_connect)

        self.status_dot = QLabel()
        self.status_dot.setObjectName("StatusDot")
        self.status_dot.setProperty("connected", False)

        self.status_label = QLabel("Disconnected")

        top_bar.addWidget(self.token_input, 3)
        top_bar.addWidget(self.remember_token, 1)
        top_bar.addWidget(self.connect_button)
        top_bar.addSpacing(10)
        top_bar.addWidget(self.status_dot)
        top_bar.addWidget(self.status_label)

        root_layout.addLayout(top_bar)

        # Main panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        # Left panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search conversations")
        self.search_input.textChanged.connect(self.filter_tree)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemSelectionChanged.connect(self.on_selection_changed)

        left_layout.addWidget(self.search_input)
        left_layout.addWidget(self.tree, 1)

        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(12)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()

        export_tab = QWidget()
        export_layout = QVBoxLayout(export_tab)
        export_layout.setSpacing(12)
        export_layout.setContentsMargins(8, 8, 8, 8)

        # Filters group
        filters_group = QGroupBox("Export Filters")
        filters_layout = QVBoxLayout(filters_group)
        filters_layout.setSpacing(8)

        self.before_check = QCheckBox("Enable Before")
        self.before_date = QDateEdit()
        self.before_date.setCalendarPopup(True)
        self.before_date.setDate(QDate.currentDate())
        self.before_time = QTimeEdit()
        self.before_time.setTime(QTime(23, 59))

        before_row = QHBoxLayout()
        before_row.addWidget(self.before_check)
        before_row.addWidget(self.before_date)
        before_row.addWidget(self.before_time)
        filters_layout.addLayout(before_row)

        self.after_check = QCheckBox("Enable After")
        self.after_date = QDateEdit()
        self.after_date.setCalendarPopup(True)
        self.after_date.setDate(QDate.currentDate())
        self.after_time = QTimeEdit()
        self.after_time.setTime(QTime(0, 0))

        after_row = QHBoxLayout()
        after_row.addWidget(self.after_check)
        after_row.addWidget(self.after_date)
        after_row.addWidget(self.after_time)
        filters_layout.addLayout(after_row)

        self.before_date.setEnabled(False)
        self.before_time.setEnabled(False)
        self.after_date.setEnabled(False)
        self.after_time.setEnabled(False)

        self.before_check.toggled.connect(self.update_filter_controls)
        self.after_check.toggled.connect(self.update_filter_controls)

        # Options group
        options_group = QGroupBox("Export Options")
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(6)

        self.export_json = QCheckBox("Export JSON")
        self.export_txt = QCheckBox("Export formatted TXT")
        self.export_attachments = QCheckBox("Export attachments/assets")
        self.include_edits = QCheckBox("Include edited timestamps")
        self.include_pins = QCheckBox("Include pinned markers")
        self.include_replies = QCheckBox("Include reply references")

        self.export_txt.setChecked(True)
        self.include_edits.setChecked(True)
        self.include_pins.setChecked(True)
        self.include_replies.setChecked(True)

        options_layout.addWidget(self.export_json)
        options_layout.addWidget(self.export_txt)
        options_layout.addWidget(self.export_attachments)
        options_layout.addWidget(self.include_edits)
        options_layout.addWidget(self.include_pins)
        options_layout.addWidget(self.include_replies)

        # Output group
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout(output_group)
        output_layout.setSpacing(6)

        self.output_dir_input = QLineEdit()
        self.output_dir_input.setPlaceholderText("Output folder")
        self.output_dir_input.setText(os.path.join(os.getcwd(), "exports"))

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_output_dir)

        output_dir_row = QHBoxLayout()
        output_dir_row.addWidget(self.output_dir_input, 3)
        output_dir_row.addWidget(browse_btn)

        self.base_filename_input = QLineEdit()
        self.base_filename_input.setPlaceholderText("Base filename (optional suffix)")
        self.base_filename_input.setText("")

        output_layout.addLayout(output_dir_row)
        output_layout.addWidget(self.base_filename_input)

        self.open_folder_toggle = QCheckBox("Open folder after export")

        # Action controls
        self.export_button = QPushButton("Export & Process")
        self.export_button.setObjectName("PrimaryButton")
        self.export_button.clicked.connect(self.on_export)

        self.progress = QProgressBar()
        self.progress.setValue(0)

        # Output preview
        preview_label = QLabel("Output Preview")
        self.preview = QPlainTextEdit()
        self.preview.setReadOnly(True)

        export_layout.addWidget(filters_group)
        export_layout.addWidget(options_group)
        export_layout.addWidget(output_group)
        export_layout.addWidget(self.open_folder_toggle)
        export_layout.addWidget(self.export_button)
        export_layout.addWidget(self.progress)
        export_layout.addWidget(preview_label)
        export_layout.addWidget(self.preview, 1)

        self.log_tab = LogTab()
        self.tabs.addTab(export_tab, "Export")
        self.tabs.addTab(self.log_tab, "Logs")
        right_layout.addWidget(self.tabs, 1)

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([320, 900])

        root_layout.addWidget(splitter, 1)

        self.setCentralWidget(root)

    def _load_saved_token(self) -> None:
        try:
            stored = load_token()
        except TokenStoreError as exc:
            self.set_status("Token store error: " + str(exc), connected=False)
            return
        if stored:
            self.token_input.setText(stored)
            self.remember_token.setChecked(True)

    def set_status(self, message: str, connected: bool | None = None) -> None:
        self.status_label.setText(message)
        if connected is not None:
            self.status_dot.setProperty("connected", connected)
            self.status_dot.style().unpolish(self.status_dot)
            self.status_dot.style().polish(self.status_dot)

    def update_filter_controls(self) -> None:
        self.before_date.setEnabled(self.before_check.isChecked())
        self.before_time.setEnabled(self.before_check.isChecked())
        self.after_date.setEnabled(self.after_check.isChecked())
        self.after_time.setEnabled(self.after_check.isChecked())

    def browse_output_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.output_dir_input.setText(path)

    def on_connect(self) -> None:
        token = self._validated_token()
        self._logger.info("Connect initiated.")
        if not token:
            return

        if self._conversation_worker and self._conversation_worker.isRunning():
            return

        self.set_status("Connecting...", connected=False)
        self.connect_button.setEnabled(False)
        self.tree.clear()
        self.preview.clear()

        if self.remember_token.isChecked():
            try:
                save_token(token)
                self._logger.info("Token saved to OS keychain.")
            except TokenStoreError as exc:
                self.set_status("Token save failed: " + str(exc), connected=False)
                self._logger.error("Token save failed: %s", exc)
        else:
            try:
                delete_token()
            except TokenStoreError:
                pass

        self._conversation_worker = ConversationWorker(token)
        self._conversation_worker.status.connect(lambda msg: self.set_status(msg, connected=False))
        self._conversation_worker.error.connect(self.on_conversation_error)
        self._conversation_worker.result.connect(self.on_conversations_loaded)
        self._conversation_worker.finished.connect(lambda: self.connect_button.setEnabled(True))
        self._conversation_worker.start()
        self._logger.info("Conversation load started.")

    def on_conversation_error(self, message: str) -> None:
        self.set_status(message, connected=False)
        self.connect_button.setEnabled(True)
        self._logger.error("Conversation load failed: %s", message)

    def on_conversations_loaded(self, payload: dict) -> None:
        self._connected_user = payload.get("me")
        user_label = self._connected_user.get("username", "Unknown") if self._connected_user else "Unknown"
        self.set_status(f"Connected as {user_label}", connected=True)
        dm_count = len(payload.get("dms", []))
        guild_count = len(payload.get("guilds", []))
        self._logger.info("Conversations loaded. DMs: %s, Guilds: %s", dm_count, guild_count)

        self.tree.setUpdatesEnabled(False)
        dms_root = QTreeWidgetItem(["Direct Messages"])
        dms_root.setFlags(dms_root.flags() & ~Qt.ItemIsSelectable)
        self.tree.addTopLevelItem(dms_root)

        for dm in payload.get("dms", []):
            name = self._dm_name(dm)
            item = QTreeWidgetItem([name])
            item.setData(0, Qt.UserRole, {"channel_id": dm.get("id"), "type": "dm", "dm_name": name})
            dms_root.addChild(item)

        servers_root = QTreeWidgetItem(["Servers"])
        servers_root.setFlags(servers_root.flags() & ~Qt.ItemIsSelectable)
        self.tree.addTopLevelItem(servers_root)

        for guild in payload.get("guilds", []):
            guild_name = guild.get("name", "Unknown Server")
            guild_item = QTreeWidgetItem([guild_name])
            guild_item.setFlags(guild_item.flags() & ~Qt.ItemIsSelectable)
            servers_root.addChild(guild_item)
            for channel in guild.get("channels", []):
                name = channel.get("name", "unnamed")
                channel_item = QTreeWidgetItem([f"# {name}"])
                channel_item.setData(
                    0,
                    Qt.UserRole,
                    {
                        "channel_id": channel.get("id"),
                        "type": "guild",
                        "guild_name": guild_name,
                        "channel_name": name,
                    },
                )
                guild_item.addChild(channel_item)
            guild_item.setExpanded(False)

        dms_root.setExpanded(True)
        servers_root.setExpanded(True)
        self.tree.setUpdatesEnabled(True)
        self.tree.expandItem(dms_root)
        self.tree.expandItem(servers_root)
        self.filter_tree(self.search_input.text())
        self.connect_button.setEnabled(True)

    def _dm_name(self, dm: dict) -> str:
        if dm.get("name"):
            return dm.get("name")
        recipients = dm.get("recipients") or []
        if not recipients:
            return "Direct Message"
        return ", ".join([r.get("username", "Unknown") for r in recipients])

    def filter_tree(self, text: str) -> None:
        text = text.lower().strip()
        for i in range(self.tree.topLevelItemCount()):
            root = self.tree.topLevelItem(i)
            self._filter_item(root, text)

    def _filter_item(self, item: QTreeWidgetItem, text: str) -> bool:
        match = text in item.text(0).lower()
        child_match = False
        for i in range(item.childCount()):
            if self._filter_item(item.child(i), text):
                child_match = True
        visible = match or child_match or text == ""
        item.setHidden(not visible)
        return visible

    def on_selection_changed(self) -> None:
        item = self.tree.currentItem()
        if not item:
            return
        data = item.data(0, Qt.UserRole)
        if not data:
            return
        channel_id = data.get("channel_id")
        if channel_id:
            self.set_status(f"Selected channel {channel_id}", connected=True)
            self._logger.debug("Channel selected: %s", channel_id)

    def on_export(self) -> None:
        token = self._validated_token()
        if not token:
            return

        selection = self._selected_item_data()
        if not selection:
            self._logger.warning("Export blocked: no channel selected.")
            self.set_status("Select a channel or DM", connected=True)
            return
        channel_id = selection.get("channel_id")
        if not channel_id:
            self._logger.warning("Export blocked: selection missing channel id.")
            self.set_status("Select a channel or DM", connected=True)
            return

        if not (self.export_json.isChecked() or self.export_txt.isChecked() or self.export_attachments.isChecked()):
            self._logger.warning("Export blocked: no export format selected.")
            self.set_status("Select at least one export option", connected=True)
            return

        output_root = self.output_dir_input.text().strip()
        if not output_root:
            self._logger.warning("Export blocked: output directory missing.")
            self.set_status("Output folder required", connected=True)
            return
        output_dir, base_filename = self._build_export_target(selection, output_root)
        ensure_dir(output_dir)

        before_dt = None
        after_dt = None
        if self.before_check.isChecked():
            before_dt = build_dt(self.before_date.date().toPython(), self.before_time.time().toPython())
        if self.after_check.isChecked():
            after_dt = build_dt(self.after_date.date().toPython(), self.after_time.time().toPython())

        options = ExportOptions(
            channel_id=channel_id,
            before_dt=before_dt,
            after_dt=after_dt,
            export_json=self.export_json.isChecked(),
            export_txt=self.export_txt.isChecked(),
            export_attachments=self.export_attachments.isChecked(),
            include_edits=self.include_edits.isChecked(),
            include_pins=self.include_pins.isChecked(),
            include_replies=self.include_replies.isChecked(),
            output_dir=output_dir,
            base_filename=base_filename,
        )

        if self._export_worker and self._export_worker.isRunning():
            return

        self.export_button.setEnabled(False)
        self.progress.setRange(0, 0)
        self.preview.clear()
        self.set_status("Exporting...", connected=True)
        self._logger.info(
            "Export started. Channel=%s JSON=%s TXT=%s Attachments=%s",
            channel_id,
            self.export_json.isChecked(),
            self.export_txt.isChecked(),
            self.export_attachments.isChecked(),
        )

        self._export_worker = ExportWorker(token, options)
        self._export_worker.status.connect(lambda msg: self.set_status(msg, connected=True))
        self._export_worker.preview.connect(self.preview.setPlainText)
        self._export_worker.error.connect(self.on_export_error)
        self._export_worker.finished.connect(self.on_export_finished)
        self._export_worker.start()

    def on_export_error(self, message: str) -> None:
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.export_button.setEnabled(True)
        self.set_status(message, connected=True)
        self._logger.error("Export failed: %s", message)

    def on_export_finished(self, result) -> None:
        self.progress.setRange(0, 100)
        self.progress.setValue(100)
        self.export_button.setEnabled(True)
        status_parts = ["Export complete"]
        if result.json_path:
            status_parts.append(f"JSON: {result.json_path}")
        if result.txt_path:
            status_parts.append(f"TXT: {result.txt_path}")
        if result.attachments_dir:
            status_parts.append(f"Attachments: {result.attachments_saved}")
        self.set_status(" | ".join(status_parts), connected=True)
        self._logger.info("Export completed successfully.")
        if self.open_folder_toggle.isChecked():
            target = result.txt_path or result.json_path or result.attachments_dir
            if target:
                QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(target)))

    def _selected_item_data(self) -> dict | None:
        item = self.tree.currentItem()
        if not item:
            return None
        data = item.data(0, Qt.UserRole)
        if not data:
            return None
        return dict(data)

    def _build_export_target(self, selection: dict, output_root: str) -> tuple[str, str]:
        chat_type = selection.get("type")
        if chat_type == "dm":
            dm_name = selection.get("dm_name") or "Direct Message"
            chat_label = dm_name
            output_dir = os.path.join(output_root, "DMs")
        else:
            guild_name = selection.get("guild_name") or "Server"
            channel_name = selection.get("channel_name") or "channel"
            chat_label = f"{guild_name} #{channel_name}"
            output_dir = os.path.join(output_root, "Servers", sanitize_path_segment(guild_name))

        parts = [sanitize_path_segment(chat_label)]

        date_part = self._build_date_part()
        time_part = self._build_time_part()
        if date_part:
            parts.append(date_part)
        if time_part:
            parts.append(time_part)

        exported_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        parts.append(f"[Exported {exported_stamp}]")

        suffix = self.base_filename_input.text().strip()
        if suffix:
            parts.insert(1, sanitize_path_segment(suffix))
        base_filename = " ".join(parts)
        return output_dir, base_filename

    def _build_date_part(self) -> str:
        if not (self.before_check.isChecked() or self.after_check.isChecked()):
            return ""
        start = None
        end = None
        if self.after_check.isChecked():
            start = self.after_date.date().toPython().strftime("%Y-%m-%d")
        if self.before_check.isChecked():
            end = self.before_date.date().toPython().strftime("%Y-%m-%d")
        if start and end:
            return f"[{start}-{end}]"
        if start:
            return f"[From {start}]"
        if end:
            return f"[To {end}]"
        return ""

    def _build_time_part(self) -> str:
        if not (self.before_check.isChecked() or self.after_check.isChecked()):
            return ""
        start = None
        end = None
        if self.after_check.isChecked():
            start = self.after_time.time().toPython().strftime("%H%M")
        if self.before_check.isChecked():
            end = self.before_time.time().toPython().strftime("%H%M")
        if start and end:
            return f"[{start}-{end}]"
        if start:
            return f"[From {start}]"
        if end:
            return f"[To {end}]"
        return ""

    def _validated_token(self) -> str | None:
        token = self.token_input.text().strip()
        if not token:
            self._logger.warning("Token missing.")
            self.set_status("Token required", connected=False)
            return None
        if any(ch.isspace() for ch in token):
            self._logger.warning("Token contains whitespace or line breaks.")
            self.set_status("Token must be a single line with no spaces.", connected=False)
            return None
        return token


def run() -> None:
    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    run()
