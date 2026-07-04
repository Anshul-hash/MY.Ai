"""Modern dark theme for LocalAI Studio."""

from __future__ import annotations

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication


class ThemeColors:
    """Central palette tokens for the dark theme."""

    BACKGROUND = "#0f1117"
    SURFACE = "#161b22"
    SURFACE_ELEVATED = "#1c2333"
    BORDER = "#2d333b"
    BORDER_SUBTLE = "#21262d"

    TEXT_PRIMARY = "#e6edf3"
    TEXT_SECONDARY = "#8b949e"
    TEXT_MUTED = "#6e7681"

    ACCENT = "#58a6ff"
    ACCENT_HOVER = "#79b8ff"
    ACCENT_PRESSED = "#388bfd"

    SUCCESS = "#3fb950"
    WARNING = "#d29922"
    ERROR = "#f85149"

    SIDEBAR_BG = "#0d1117"
    SIDEBAR_HOVER = "#21262d"
    SIDEBAR_ACTIVE = "#1f6feb33"

    CHAT_USER_BG = "#1f6feb22"
    CHAT_ASSISTANT_BG = "#21262d"
    INPUT_BG = "#0d1117"


def _build_stylesheet() -> str:
    c = ThemeColors
    return f"""
    QMainWindow, QWidget {{
        background-color: {c.BACKGROUND};
        color: {c.TEXT_PRIMARY};
        font-family: "Segoe UI", "Inter", "SF Pro Text", sans-serif;
        font-size: 13px;
    }}

    QMenuBar {{
        background-color: {c.SURFACE};
        border-bottom: 1px solid {c.BORDER_SUBTLE};
        padding: 2px 0;
    }}

    QMenuBar::item {{
        padding: 4px 10px;
        background: transparent;
    }}

    QMenuBar::item:selected {{
        background-color: {c.SIDEBAR_HOVER};
        border-radius: 4px;
    }}

    QMenu {{
        background-color: {c.SURFACE_ELEVATED};
        border: 1px solid {c.BORDER};
        border-radius: 6px;
        padding: 4px;
    }}

    QMenu::item {{
        padding: 6px 24px 6px 12px;
        border-radius: 4px;
    }}

    QMenu::item:selected {{
        background-color: {c.ACCENT_PRESSED};
    }}

    QScrollBar:vertical {{
        background: transparent;
        width: 10px;
        margin: 0;
    }}

    QScrollBar::handle:vertical {{
        background: {c.BORDER};
        border-radius: 5px;
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {c.TEXT_MUTED};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0;
    }}

    QScrollBar:horizontal {{
        background: transparent;
        height: 10px;
    }}

    QScrollBar::handle:horizontal {{
        background: {c.BORDER};
        border-radius: 5px;
        min-width: 30px;
    }}

    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: {c.INPUT_BG};
        border: 1px solid {c.BORDER};
        border-radius: 8px;
        padding: 8px 12px;
        selection-background-color: {c.ACCENT_PRESSED};
    }}

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border-color: {c.ACCENT};
    }}

    QPushButton {{
        background-color: {c.SURFACE_ELEVATED};
        border: 1px solid {c.BORDER};
        border-radius: 8px;
        padding: 8px 16px;
        color: {c.TEXT_PRIMARY};
        font-weight: 500;
    }}

    QPushButton:hover {{
        background-color: {c.SIDEBAR_HOVER};
        border-color: {c.TEXT_MUTED};
    }}

    QPushButton:pressed {{
        background-color: {c.BORDER_SUBTLE};
    }}

    QPushButton#primaryButton {{
        background-color: {c.ACCENT};
        border-color: {c.ACCENT};
        color: #ffffff;
    }}

    QPushButton#primaryButton:hover {{
        background-color: {c.ACCENT_HOVER};
        border-color: {c.ACCENT_HOVER};
    }}

    QPushButton#primaryButton:pressed {{
        background-color: {c.ACCENT_PRESSED};
    }}

    QStatusBar {{
        background-color: {c.SURFACE};
        border-top: 1px solid {c.BORDER_SUBTLE};
        color: {c.TEXT_SECONDARY};
        font-size: 12px;
    }}

    QStatusBar::item {{
        border: none;
    }}

    QSplitter::handle {{
        background-color: {c.BORDER_SUBTLE};
    }}

    QToolTip {{
        background-color: {c.SURFACE_ELEVATED};
        color: {c.TEXT_PRIMARY};
        border: 1px solid {c.BORDER};
        border-radius: 4px;
        padding: 4px 8px;
    }}
    """


def apply_dark_theme(app: QApplication) -> None:
    """Apply a cohesive dark palette and global stylesheet."""
    app.setStyle("Fusion")

    palette = QPalette()
    c = ThemeColors

    palette.setColor(QPalette.ColorRole.Window, QColor(c.BACKGROUND))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(c.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Base, QColor(c.INPUT_BG))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(c.SURFACE))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(c.SURFACE_ELEVATED))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(c.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Text, QColor(c.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.Button, QColor(c.SURFACE_ELEVATED))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(c.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.BrightText, QColor(c.ACCENT))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(c.ACCENT_PRESSED))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.Link, QColor(c.ACCENT))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(c.TEXT_MUTED))

    app.setPalette(palette)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(_build_stylesheet())
