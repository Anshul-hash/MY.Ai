"""Base class for sidebar content pages."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from localai_studio.config.theme import ThemeColors
from localai_studio.ui.navigation import NavItem


class BasePage(QWidget):
    """Shared layout for full-page views."""

    def __init__(self, nav_item: NavItem, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.nav_item = nav_item
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(32, 28, 32, 28)
        self._layout.setSpacing(12)

    def add_stretch(self) -> None:
        self._layout.addStretch()


class PlaceholderPage(BasePage):
    """Generic placeholder for features not yet implemented."""

    def __init__(
        self,
        nav_item: NavItem,
        *,
        headline: str | None = None,
        detail: str | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(nav_item, parent)

        title = QLabel(headline or nav_item.label, self)
        title.setStyleSheet(
            f"font-size: 22px; font-weight: 700; color: {ThemeColors.TEXT_PRIMARY};"
        )

        subtitle = QLabel(
            detail or f"{nav_item.label} workspace — coming soon.",
            self,
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            f"font-size: 14px; color: {ThemeColors.TEXT_SECONDARY}; max-width: 520px;"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft)

        badge = QLabel("Placeholder", self)
        badge.setStyleSheet(
            f"""
            background-color: {ThemeColors.SURFACE_ELEVATED};
            color: {ThemeColors.TEXT_MUTED};
            border: 1px solid {ThemeColors.BORDER};
            border-radius: 12px;
            padding: 4px 10px;
            font-size: 11px;
            max-width: 90px;
            """
        )

        self._layout.addWidget(title)
        self._layout.addWidget(subtitle)
        self._layout.addWidget(badge)
        self.add_stretch()
