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
from localai_studio.services.status_service import StatusService


class MainWindow(QMainWindow):
    """Root window composing sidebar navigation, pages, and status bar."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("LocalAI Studio")
        self.setMinimumSize(1100, 720)
        self.resize(1280, 800)

        self._status_service = StatusService()
        self._sidebar = Sidebar(self)
        self._stack = QStackedWidget(self)
        self._pages: dict[NavItem, QWidget] = {}

        self._register_pages()
        self._sidebar.navigation_changed.connect(self._on_navigation_changed)

        central = QWidget(self)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._sidebar)
        layout.addWidget(self._stack, stretch=1)

        self.setCentralWidget(central)

        self._status_bar = AppStatusBar(self)
        self.setStatusBar(self._status_bar)
        self._status_bar.update_from_status(self._status_service.get_status())

        self._show_page(NavItem.CHAT)

    def _register_pages(self) -> None:
        page_classes = {
            NavItem.CHAT: ChatPage,
            NavItem.FILES: FilesPage,
            NavItem.BROWSER: BrowserPage,
            NavItem.TERMINAL: TerminalPage,
            NavItem.MEMORY: MemoryPage,
            NavItem.PLUGINS: PluginsPage,
            NavItem.SETTINGS: SettingsPage,
        }
        for nav_item, page_class in page_classes.items():
            page = page_class(self)
            self._pages[nav_item] = page
            self._stack.addWidget(page)

    def _on_navigation_changed(self, item: NavItem) -> None:
        self._show_page(item)

    def _show_page(self, item: NavItem) -> None:
        page = self._pages[item]
        self._stack.setCurrentWidget(page)
