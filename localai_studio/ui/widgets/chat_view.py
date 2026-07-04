"""Scrollable chat message history."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QScrollArea, QVBoxLayout, QWidget

from localai_studio.config.theme import ThemeColors


class MessageBubble(QFrame):
    """A single chat message bubble."""

    ROLE_STYLES = {
        "user": {
            "bg": ThemeColors.CHAT_USER_BG,
            "border": ThemeColors.ACCENT,
            "label": "You",
            "label_color": ThemeColors.ACCENT,
        },
        "assistant": {
            "bg": ThemeColors.CHAT_ASSISTANT_BG,
            "border": ThemeColors.BORDER,
            "label": "Assistant",
            "label_color": ThemeColors.SUCCESS,
        },
    }

    def __init__(self, role: str, content: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        style = self.ROLE_STYLES.get(role, self.ROLE_STYLES["assistant"])

        self.setStyleSheet(
            f"""
            MessageBubble {{
                background-color: {style["bg"]};
                border: 1px solid {style["border"]};
                border-radius: 12px;
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        role_label = QLabel(style["label"], self)
        role_label.setStyleSheet(
            f"font-size: 11px; font-weight: 600; color: {style['label_color']};"
        )

        body = QLabel(content, self)
        body.setWordWrap(True)
        body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        body.setStyleSheet(
            f"font-size: 13px; color: {ThemeColors.TEXT_PRIMARY}; line-height: 1.5;"
        )

        layout.addWidget(role_label)
        layout.addWidget(body)


class ChatView(QScrollArea):
    """Vertically scrollable list of chat messages."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._container = QWidget(self)
        self._layout = QVBoxLayout(self._container)
        self._layout.setContentsMargins(24, 20, 24, 20)
        self._layout.setSpacing(12)
        self._layout.addStretch()

        self.setWidget(self._container)
        self.setStyleSheet(f"background-color: {ThemeColors.BACKGROUND};")

    def add_message(self, role: str, content: str) -> None:
        bubble = MessageBubble(role, content, self._container)
        self._layout.insertWidget(self._layout.count() - 1, bubble)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
