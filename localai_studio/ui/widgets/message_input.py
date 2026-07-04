"""Bottom message input bar."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QHBoxLayout, QPlainTextEdit, QPushButton, QWidget

from localai_studio.config.theme import ThemeColors


class ChatTextEdit(QPlainTextEdit):
    """Plain text editor that emits on Enter (without Shift)."""

    submit_requested = Signal()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if (
            event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter)
            and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        ):
            self.submit_requested.emit()
            event.accept()
            return
        super().keyPressEvent(event)


class MessageInput(QWidget):
    """Multi-line input with send button for chat messages."""

    message_submitted = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            f"""
            MessageInput {{
                background-color: {ThemeColors.SURFACE};
                border-top: 1px solid {ThemeColors.BORDER_SUBTLE};
            }}
            """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(12)

        self._editor = ChatTextEdit(self)
        self._editor.setPlaceholderText("Message LocalAI Studio…  (Enter to send, Shift+Enter for new line)")
        self._editor.submit_requested.connect(self._submit)
        self._editor.setFixedHeight(72)
        self._editor.setTabChangesFocus(True)
        self._editor.setStyleSheet(
            f"""
            QPlainTextEdit {{
                background-color: {ThemeColors.INPUT_BG};
                border: 1px solid {ThemeColors.BORDER};
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 13px;
            }}
            QPlainTextEdit:focus {{
                border-color: {ThemeColors.ACCENT};
            }}
            """
        )

        self._send_button = QPushButton("Send", self)
        self._send_button.setObjectName("primaryButton")
        self._send_button.setFixedSize(88, 40)
        self._send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._send_button.clicked.connect(self._submit)

        layout.addWidget(self._editor, stretch=1)
        layout.addWidget(self._send_button, alignment=Qt.AlignmentFlag.AlignBottom)

    def _submit(self) -> None:
        text = self._editor.toPlainText().strip()
        if not text:
            return
        self.message_submitted.emit(text)
        self._editor.clear()
