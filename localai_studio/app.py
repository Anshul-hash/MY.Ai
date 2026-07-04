"""Application bootstrap and lifecycle."""

from __future__ import annotations

from PySide6.QtWidgets import QApplication

from localai_studio import __app_name__, __version__
from localai_studio.config.theme import apply_dark_theme
from localai_studio.ui.main_window import MainWindow


class LocalAIStudioApp:
    """Encapsulates Qt application setup and the main window lifecycle."""

    def __init__(self, argv: list[str]) -> None:
        self._qt_app = QApplication(argv)
        self._qt_app.setApplicationName(__app_name__)
        self._qt_app.setApplicationVersion(__version__)
        self._qt_app.setOrganizationName("LocalAI Studio")
        apply_dark_theme(self._qt_app)

        self._main_window = MainWindow()

    def run(self) -> int:
        self._main_window.show()
        return self._qt_app.exec()
