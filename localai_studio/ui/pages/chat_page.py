"""Primary chat workspace page."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from localai_studio.config.theme import ThemeColors
from localai_studio.ui.navigation import NavItem
from localai_studio.ui.pages.base_page import BasePage
from localai_studio.ui.widgets.chat_view import ChatView
from localai_studio.ui.widgets.message_input import MessageInput


class ChatPage(BasePage):
    """Main conversational interface with message history and input."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(NavItem.CHAT, parent)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        header = self._build_header()
        self._chat_view = ChatView(self)
        self._message_input = MessageInput(self)

        self._message_input.message_submitted.connect(self._on_message_submitted)

        self._layout.addWidget(header)
        self._layout.addWidget(self._chat_view, stretch=1)
        self._layout.addWidget(self._message_input)

        self._seed_welcome_message()

    def _build_header(self) -> QWidget:
        header = QWidget(self)
        header.setStyleSheet(
            f"""
            background-color: {ThemeColors.SURFACE};
            border-bottom: 1px solid {ThemeColors.BORDER_SUBTLE};
            """
        )
        layout = QVBoxLayout(header)
        layout.setContentsMargins(24, 16, 24, 12)
        layout.setSpacing(2)

        title = QLabel("Chat", header)
        title.setStyleSheet(
            f"font-size: 16px; font-weight: 600; color: {ThemeColors.TEXT_PRIMARY};"
        )

        subtitle = QLabel(
            "Start a conversation with your locally hosted models.",
            header,
        )
        subtitle.setStyleSheet(
            f"font-size: 12px; color: {ThemeColors.TEXT_MUTED};"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        return header

    def _seed_welcome_message(self) -> None:
        self._chat_view.add_message(
            role="assistant",
            content=(
                "Welcome to **LocalAI Studio**. Connect Ollama and select a model "
                "from Settings to begin chatting locally."
            ),
        )

    def _on_message_submitted(self, text: str) -> None:
        self._chat_view.add_message(role="user", content=text)
        self._chat_view.add_message(
            role="assistant",
            content=(
                "_Model integration is not wired yet._ "
                "Your message was received and will be routed once Ollama is connected."
            ),
        )
