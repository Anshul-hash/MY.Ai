"""Application status bar with connection and hardware indicators."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QStatusBar, QWidget

from localai_studio.config.theme import ThemeColors
from localai_studio.services.status_service import SystemStatus


class StatusIndicator(QLabel):
    """Compact labeled status pill for the status bar."""

    def __init__(self, label: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._label = label
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setTextFormat(Qt.TextFormat.RichText)
        self._set_value("—", ThemeColors.TEXT_MUTED)

    def _set_value(self, value: str, color: str) -> None:
        self.setText(
            f'<span style="color:{ThemeColors.TEXT_MUTED}">{self._label}:</span> '
            f'<span style="color:{color}; font-weight:500;">{value}</span>'
        )

    def update_status(self, value: str, *, healthy: bool | None = None) -> None:
        if healthy is True:
            color = ThemeColors.SUCCESS
        elif healthy is False:
            color = ThemeColors.ERROR
        else:
            color = ThemeColors.TEXT_SECONDARY
        self._set_value(value, color)


class AppStatusBar(QStatusBar):
    """Status bar showing Ollama, model, and compute backend state."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(28)

        self._ollama = StatusIndicator("Ollama", self)
        self._model = StatusIndicator("Model", self)
        self._compute = StatusIndicator("Compute", self)

        separator_style = f"color: {ThemeColors.BORDER}; padding: 0 4px;"
        sep1 = QLabel("|", self)
        sep1.setStyleSheet(separator_style)
        sep2 = QLabel("|", self)
        sep2.setStyleSheet(separator_style)

        self.addWidget(self._ollama)
        self.addWidget(sep1)
        self.addWidget(self._model)
        self.addWidget(sep2)
        self.addWidget(self._compute)
        self.addPermanentWidget(self._build_branding())

    def _build_branding(self) -> QLabel:
        label = QLabel("LocalAI Studio", self)
        label.setStyleSheet(
            f"color: {ThemeColors.TEXT_MUTED}; font-size: 11px; padding-right: 8px;"
        )
        return label

    def update_from_status(self, status: SystemStatus) -> None:
        self._ollama.update_status(
            status.ollama_connection,
            healthy=status.ollama_connected,
        )
        self._model.update_status(status.selected_model)
        self._compute.update_status(
            status.compute_backend,
            healthy=status.using_gpu,
        )
