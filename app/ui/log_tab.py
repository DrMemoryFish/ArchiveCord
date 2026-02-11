from __future__ import annotations

import logging
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, List

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QObject,
    QSortFilterProxyModel,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from app.core.utils import format_log_timestamp


LEVEL_COLORS = {
    "DEBUG": QColor("#7a828f"),
    "INFO": QColor("#e6e8eb"),
    "WARNING": QColor("#f0b14b"),
    "ERROR": QColor("#e06c75"),
}


@dataclass(frozen=True)
class LogEntry:
    timestamp: datetime
    timestamp_str: str
    level: str
    levelno: int
    message: str


class LogTableModel(QAbstractTableModel):
    def __init__(self, max_entries: int = 5000) -> None:
        super().__init__()
        self._entries: List[LogEntry] = []
        self._max_entries = max_entries

    def rowCount(self, parent=None) -> int:
        return len(self._entries)

    def columnCount(self, parent=None) -> int:
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        entry = self._entries[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return entry.timestamp_str
            if index.column() == 1:
                return entry.level
            if index.column() == 2:
                return entry.message
        if role == Qt.ForegroundRole:
            color = LEVEL_COLORS.get(entry.level)
            if color:
                return QBrush(color)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None
        if section == 0:
            return "Timestamp"
        if section == 1:
            return "Level"
        if section == 2:
            return "Message"
        return None

    def entry(self, row: int) -> LogEntry:
        return self._entries[row]

    def append_entries(self, entries: List[LogEntry]) -> None:
        if not entries:
            return

        overflow = max(0, len(self._entries) + len(entries) - self._max_entries)
        if overflow:
            self.beginRemoveRows(QModelIndex(), 0, overflow - 1)
            del self._entries[:overflow]
            self.endRemoveRows()

        start = len(self._entries)
        end = start + len(entries) - 1
        self.beginInsertRows(QModelIndex(), start, end)
        self._entries.extend(entries)
        self.endInsertRows()

    def clear(self) -> None:
        if not self._entries:
            return
        self.beginRemoveRows(QModelIndex(), 0, len(self._entries) - 1)
        self._entries.clear()
        self.endRemoveRows()


class LogFilterProxyModel(QSortFilterProxyModel):
    def __init__(self) -> None:
        super().__init__()
        self._level_filter = "ALL"
        self._text_filter = ""
        self._include_debug = True

    def set_level_filter(self, value: str) -> None:
        self._level_filter = value.upper()
        self.invalidateFilter()

    def set_text_filter(self, text: str) -> None:
        self._text_filter = text.lower().strip()
        self.invalidateFilter()

    def set_include_debug(self, enabled: bool) -> None:
        self._include_debug = enabled
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent) -> bool:
        model: LogTableModel = self.sourceModel()  # type: ignore
        entry = model.entry(source_row)

        if self._level_filter == "ALL":
            if not self._include_debug and entry.levelno == logging.DEBUG:
                return False
        else:
            if entry.level.upper() != self._level_filter:
                return False

        if self._text_filter:
            haystack = f"{entry.timestamp_str} {entry.level} {entry.message}".lower()
            if self._text_filter not in haystack:
                return False

        return True


class QtLogHandler(QObject, logging.Handler):
    record_emitted = Signal(object)

    def __init__(self) -> None:
        QObject.__init__(self)
        logging.Handler.__init__(self)

    def emit(self, record: logging.LogRecord) -> None:
        self.record_emitted.emit(record)


class LogTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._pending: Deque[logging.LogRecord] = deque()
        self._flush_timer = QTimer(self)
        self._flush_timer.setInterval(100)
        self._flush_timer.timeout.connect(self._flush_pending)

        self._model = LogTableModel(max_entries=5000)
        self._proxy = LogFilterProxyModel()
        self._proxy.setSourceModel(self._model)

        self._build_ui()
        self._install_handler()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)

        controls = QHBoxLayout()

        self.level_filter = QComboBox()
        self.level_filter.addItems(["ALL", "INFO", "WARNING", "ERROR", "DEBUG"])
        self.level_filter.currentTextChanged.connect(self._proxy.set_level_filter)

        self.debug_toggle = QCheckBox("Show DEBUG")
        self.debug_toggle.setChecked(True)
        self.debug_toggle.toggled.connect(self._proxy.set_include_debug)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search logs")
        self.search_input.textChanged.connect(self._proxy.set_text_filter)

        self.auto_scroll = QCheckBox("Auto-scroll")
        self.auto_scroll.setChecked(True)

        self.copy_button = QPushButton("Copy Selected")
        self.copy_button.clicked.connect(self.copy_selected)

        self.clear_button = QPushButton("Clear Logs")
        self.clear_button.clicked.connect(self.clear_logs)

        controls.addWidget(QLabel("Level"))
        controls.addWidget(self.level_filter)
        controls.addWidget(self.debug_toggle)
        controls.addStretch(1)
        controls.addWidget(self.search_input, 2)
        controls.addWidget(self.auto_scroll)
        controls.addWidget(self.copy_button)
        controls.addWidget(self.clear_button)

        self.table = QTableView()
        self.table.setModel(self._proxy)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(False)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnWidth(0, 180)
        self.table.setColumnWidth(1, 90)

        layout.addLayout(controls)
        layout.addWidget(self.table, 1)

    def _install_handler(self) -> None:
        self._handler = QtLogHandler()
        self._handler.setLevel(logging.DEBUG)
        self._handler.record_emitted.connect(self._enqueue_record)
        logging.getLogger().addHandler(self._handler)

    def _enqueue_record(self, record: logging.LogRecord) -> None:
        self._pending.append(record)
        if not self._flush_timer.isActive():
            self._flush_timer.start()

    def _flush_pending(self) -> None:
        if not self._pending:
            return
        records = []
        while self._pending:
            records.append(self._pending.popleft())

        entries: List[LogEntry] = []
        for record in records:
            timestamp = datetime.fromtimestamp(record.created).astimezone()
            message = record.getMessage()
            if record.exc_info:
                try:
                    exc_text = self._handler.formatException(record.exc_info)
                    message = f"{message} | {exc_text}"
                except Exception:
                    pass
            entries.append(
                LogEntry(
                    timestamp=timestamp,
                    timestamp_str=format_log_timestamp(timestamp),
                    level=record.levelname,
                    levelno=record.levelno,
                    message=message,
                )
            )

        self._model.append_entries(entries)

        if self.auto_scroll.isChecked():
            self.table.scrollToBottom()

    def clear_logs(self) -> None:
        self._model.clear()

    def copy_selected(self) -> None:
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            return
        index = selection[0]
        source_index = self._proxy.mapToSource(index)
        entry = self._model.entry(source_index.row())
        text = f"[{entry.timestamp_str}] [{entry.level}] {entry.message}"
        QApplication.clipboard().setText(text)
