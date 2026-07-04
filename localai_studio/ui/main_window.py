"""Primary application window."""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from localai_studio.ui.navigation import NavItem
from localai_studio.ui.pages.browser_page import BrowserPage
from localai_studio.ui.pages.chat_page import ChatPage
from localai_studio.ui.pages.files_page import FilesPage
from localai_studio.ui.pages.memory_page import MemoryPage
from localai_studio.ui.pages.plugins_page import PluginsPage
from localai_studio.ui.pages.settings_page import SettingsPage
from localai_studio.ui.pages.terminal_page import TerminalPage
from localai_studio.ui.sidebar import Sidebar
from localai_studio.ui.status_bar import AppStatusBar
from localai_studio.services.ollama_controller import OllamaController
from localai_studio.services.status_service import StatusService


class MainWindow(QMainWindow):
    """Root window composing sidebar navigation, pages, and status bar."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("LocalAI Studio")
        self.setMinimumSize(1100, 720)
        self.resize(1280, 800)

        self._status_service = StatusService()
        self._ollama_controller = OllamaController(parent=self)

        self._sidebar = Sidebar(self)
        self._stack = QStackedWidget(self)

        self._pages: dict[NavItem, QWidget] = {}
        self._chat_page: ChatPage | None = None

        self._register_pages()

        self._sidebar.navigation_changed.connect(
            self._on_navigation_changed
        )

        central = QWidget(self)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._sidebar)
        layout.addWidget(self._stack, stretch=1)

        self.setCentralWidget(central)

        self._status_bar = AppStatusBar(self)
        self.setStatusBar(self._status_bar)

        self._ollama_controller.connection_changed.connect(
            self._refresh_ollama_ui
        )
        self._ollama_controller.models_changed.connect(
            self._refresh_ollama_ui
        )
        self._ollama_controller.current_model_changed.connect(
            self._refresh_ollama_ui
        )

        self._ollama_controller.start()

        self._show_page(NavItem.CHAT)

    def _register_pages(self) -> None:
        self._chat_page = ChatPage(self._ollama_controller, self)

        page_map = {
            NavItem.CHAT: self._chat_page,
            NavItem.FILES: FilesPage(self),
            NavItem.BROWSER: BrowserPage(self),
            NavItem.TERMINAL: TerminalPage(self),
            NavItem.MEMORY: MemoryPage(self),
            NavItem.PLUGINS: PluginsPage(self),
            NavItem.SETTINGS: SettingsPage(self),
        }

        for nav_item, page in page_map.items():
            self._pages[nav_item] = page
            self._stack.addWidget(page)

    def _refresh_ollama_ui(self, *_args) -> None:
        client = self._ollama_controller.client
        self._status_bar.update_from_status(
            self._status_service.get_status(client)
        )

        if self._chat_page is not None:
            self._chat_page.sync_model_selector()

    def _on_navigation_changed(self, item: NavItem) -> None:
        self._show_page(item)

    def _show_page(self, item: NavItem) -> None:
        page = self._pages[item]
        self._stack.setCurrentWidget(page)

    def closeEvent(self, event) -> None:
        self._ollama_controller.stop()
        super().closeEvent(event)
