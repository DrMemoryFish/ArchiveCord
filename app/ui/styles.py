STYLESHEET = """
* {
    font-family: 'Bahnschrift', 'Segoe UI Variable', 'Segoe UI';
    font-size: 10.5pt;
    color: #e6e8eb;
}

QMainWindow {
    background: #0f1115;
}

QWidget {
    background: #0f1115;
}

QLineEdit, QPlainTextEdit, QTreeWidget, QDateEdit, QTimeEdit, QComboBox {
    background: #151a21;
    border: 1px solid #2a2f38;
    border-radius: 6px;
    padding: 6px 8px;
    selection-background-color: #2c8f7a;
}

QLineEdit:focus, QPlainTextEdit:focus, QTreeWidget:focus, QDateEdit:focus, QTimeEdit:focus, QComboBox:focus {
    border: 1px solid #3bb29a;
}

QPushButton {
    background: #1f2733;
    border: 1px solid #2d3a4a;
    border-radius: 8px;
    padding: 8px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background: #233041;
}

QPushButton:pressed {
    background: #1b2431;
}

QPushButton#PrimaryButton {
    background: #2c8f7a;
    border: 1px solid #36a88f;
    color: #eaf7f4;
}

QPushButton#PrimaryButton:hover {
    background: #2fa287;
}

QPushButton:disabled {
    color: #7c8796;
    background: #151a21;
    border: 1px solid #2a2f38;
}

QGroupBox {
    border: 1px solid #222831;
    border-radius: 8px;
    margin-top: 10px;
    padding: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px 0 6px;
    color: #cfd6dd;
}

QTreeWidget {
    border: 1px solid #222831;
}

QTreeWidget::item {
    padding: 6px 4px;
}

QTreeWidget::item:selected {
    background: #203246;
    color: #eaf7f4;
}

QScrollBar:vertical {
    background: #0f1115;
    width: 10px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #2b3442;
    min-height: 20px;
    border-radius: 5px;
}

QProgressBar {
    border: 1px solid #2a2f38;
    border-radius: 6px;
    text-align: center;
    background: #151a21;
}

QProgressBar::chunk {
    background: #2c8f7a;
}

QTabWidget::pane {
    border: 1px solid #222831;
    border-radius: 8px;
    top: -1px;
    background: #0f1115;
}

QTabBar::tab {
    background: #151a21;
    border: 1px solid #222831;
    padding: 8px 14px;
    margin-right: 4px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background: #1f2733;
    border-color: #2d3a4a;
}

QTabBar::tab:hover {
    background: #1b2230;
}

QHeaderView::section {
    background: #151a21;
    color: #cfd6dd;
    padding: 6px 8px;
    border: 1px solid #222831;
}

QTableView {
    background: #0f1115;
    border: 1px solid #222831;
    gridline-color: #222831;
    alternate-background-color: #131820;
}

QTableView::item {
    padding: 4px 6px;
}

QTableView::item:selected {
    background: #203246;
    color: #eaf7f4;
}

QLabel#StatusDot {
    background: #5b6472;
    border-radius: 6px;
    min-width: 12px;
    min-height: 12px;
    max-width: 12px;
    max-height: 12px;
}

QLabel#StatusDot[connected="true"] {
    background: #2c8f7a;
}
"""
