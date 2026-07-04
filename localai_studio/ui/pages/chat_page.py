"""Primary chat workspace page."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from localai_studio.config.theme import ThemeColors
from localai_studio.services.ollama_controller import OllamaController
from localai_studio.ui.navigation import NavItem
from localai_studio.ui.pages.base_page import BasePage
from localai_studio.ui.widgets.chat_view import ChatView
from localai_studio.ui.widgets.message_input import MessageInput
from localai_studio.ui.widgets.model_selector import ModelSelector


class ChatPage(BasePage):
    """Main conversational interface with message history and input."""

    def __init__(
        self,
        ollama_controller: OllamaController,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(NavItem.CHAT, parent)
        self._ollama = ollama_controller
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._model_selector = ModelSelector(self)
        self._model_selector.model_selected.connect(self._ollama.select_model)

        header = self._build_header()
        self._chat_view = ChatView(self)
        self._message_input = MessageInput(self)

        self._message_input.message_submitted.connect(self._on_message_submitted)

        self._layout.addWidget(header)
        self._layout.addWidget(self._chat_view, stretch=1)
        self._layout.addWidget(self._message_input)

        self._seed_welcome_message()
        self.sync_model_selector()

    def _build_header(self) -> QWidget:
        header = QWidget(self)
        header.setStyleSheet(
            f"""
            background-color: {ThemeColors.SURFACE};
            border-bottom: 1px solid {ThemeColors.BORDER_SUBTLE};
            """
        )
        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 16, 24, 12)
        layout.setSpacing(16)

        title_block = QVBoxLayout()
        title_block.setSpacing(2)

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

        title_block.addWidget(title)
        title_block.addWidget(subtitle)

        model_label = QLabel("Model", header)
        model_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        model_label.setStyleSheet(
            f"font-size: 11px; color: {ThemeColors.TEXT_MUTED};"
        )

        selector_block = QVBoxLayout()
        selector_block.setSpacing(4)
        selector_block.addWidget(model_label, alignment=Qt.AlignmentFlag.AlignRight)
        selector_block.addWidget(self._model_selector, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(title_block, stretch=1)
        layout.addLayout(selector_block)
        return header

    def sync_model_selector(self) -> None:
        client = self._ollama.client
        self._model_selector.set_models(
            client.list_models(),
            current=client.current_model(),
            connected=client.is_connected(),
        )

    def _seed_welcome_message(self) -> None:
        self._chat_view.add_message(
            role="assistant",
            content=(
                "Welcome to **LocalAI Studio**. When Ollama is running, choose a model "
                "from the selector above to begin chatting locally."
            ),
        )

    def _on_message_submitted(self, text: str) -> None:
        self._chat_view.add_message(role="user", content=text)

        client = self._ollama.client

        if not client.is_connected():
            reply = (
                "_Ollama is disconnected._ "
                "Start Ollama and wait for the status bar to show Connected."
            )

        elif client.current_model() is None:
            reply = (
                "_No model selected._ "
                "Install a model in Ollama, then pick one from the selector."
            )

        else:
            try:
                reply = client.chat(text)
            except Exception as e:
                reply = f"Error: {e}"

        self._chat_view.add_message(
            role="assistant",
            content=reply,
        )
