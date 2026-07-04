"""Dropdown for choosing an Ollama model."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QComboBox, QWidget

from localai_studio.config.theme import ThemeColors


class ModelSelector(QComboBox):
    """Combo box populated from the live Ollama model catalog."""

    model_selected = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumWidth(220)
        self.setPlaceholderText("No models available")
        self.currentTextChanged.connect(self._on_text_changed)
        self._apply_style()
        self.setEnabled(False)

    def _apply_style(self) -> None:
        c = ThemeColors
        self.setStyleSheet(
            f"""
            QComboBox {{
                background-color: {c.INPUT_BG};
                border: 1px solid {c.BORDER};
                border-radius: 8px;
                padding: 6px 12px;
                color: {c.TEXT_PRIMARY};
                font-size: 12px;
            }}
            QComboBox:hover {{
                border-color: {c.TEXT_MUTED};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {c.SURFACE_ELEVATED};
                border: 1px solid {c.BORDER};
                selection-background-color: {c.ACCENT_PRESSED};
                color: {c.TEXT_PRIMARY};
            }}
            """
        )

    def set_models(
        self,
        models: list[str],
        *,
        current: str | None = None,
        connected: bool,
    ) -> None:
        self.blockSignals(True)
        self.clear()

        if not connected:
            self.addItem("Ollama disconnected")
            self.setEnabled(False)
            self.blockSignals(False)
            return

        if not models:
            self.addItem("No models installed")
            self.setEnabled(False)
            self.blockSignals(False)
            return

        self.addItems(models)
        self.setEnabled(True)

        if current and current in models:
            self.setCurrentText(current)
        else:
            self.setCurrentIndex(0)

        self.blockSignals(False)

    def _on_text_changed(self, text: str) -> None:
        if not self.isEnabled():
            return
        if text in {"Ollama disconnected", "No models installed"}:
            return
        self.model_selected.emit(text)
