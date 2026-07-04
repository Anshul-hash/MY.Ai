"""Left navigation sidebar."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from localai_studio import __app_name__
from localai_studio.config.theme import ThemeColors
from localai_studio.ui.navigation import NavItem


class SidebarButton(QPushButton):
    """A single navigation entry in the sidebar."""

    def __init__(self, item: NavItem, parent: QWidget | None = None) -> None:
        super().__init__(f"  {item.icon}   {item.label}", parent)
        self.item = item
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(item.description)
        self.setFixedHeight(40)
        self._apply_style(active=False)

    def set_active(self, active: bool) -> None:
        self.setChecked(active)
        self._apply_style(active=active)

    def _apply_style(self, active: bool) -> None:
        c = ThemeColors
        if active:
            bg = c.SIDEBAR_ACTIVE
            border = c.ACCENT
            color = c.TEXT_PRIMARY
        else:
            bg = "transparent"
            border = "transparent"
            color = c.TEXT_SECONDARY

        self.setStyleSheet(
            f"""
            SidebarButton {{
                text-align: left;
                padding-left: 12px;
                border: none;
                border-left: 3px solid {border};
                border-radius: 0;
                background-color: {bg};
                color: {color};
                font-size: 13px;
                font-weight: {"600" if active else "400"};
            }}
            SidebarButton:hover {{
                background-color: {c.SIDEBAR_HOVER};
                color: {c.TEXT_PRIMARY};
            }}
            """
        )


class Sidebar(QFrame):
    """Vertical sidebar with app branding and navigation buttons."""

    navigation_changed = Signal(NavItem)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        self._buttons: dict[NavItem, SidebarButton] = {}
        self._active_item = NavItem.CHAT

        self.setStyleSheet(
            f"""
            QFrame#sidebar {{
                background-color: {ThemeColors.SIDEBAR_BG};
                border-right: 1px solid {ThemeColors.BORDER_SUBTLE};
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 12)
        layout.setSpacing(2)

        layout.addWidget(self._build_header())
        layout.addSpacing(8)

        for item in NavItem:
            button = SidebarButton(item, self)
            button.clicked.connect(lambda checked, nav=item: self._on_button_clicked(nav))
            self._buttons[item] = button
            layout.addWidget(button)

        layout.addStretch()
        layout.addWidget(self._build_footer())

        self._buttons[NavItem.CHAT].set_active(True)

    def _build_header(self) -> QWidget:
        header = QWidget(self)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(16, 20, 16, 8)
        header_layout.setSpacing(2)

        title = QLabel(__app_name__, header)
        title.setStyleSheet(
            f"font-size: 15px; font-weight: 700; color: {ThemeColors.TEXT_PRIMARY};"
        )

        subtitle = QLabel("Local-first AI workspace", header)
        subtitle.setStyleSheet(
            f"font-size: 11px; color: {ThemeColors.TEXT_MUTED};"
        )

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        return header

    def _build_footer(self) -> QWidget:
        footer = QLabel("v0.1.0  ·  Offline ready", self)
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet(
            f"color: {ThemeColors.TEXT_MUTED}; font-size: 11px; padding: 8px;"
        )
        return footer

    def _on_button_clicked(self, item: NavItem) -> None:
        if item == self._active_item:
            return
        self.set_active_item(item)
        self.navigation_changed.emit(item)

    def set_active_item(self, item: NavItem) -> None:
        self._active_item = item
        for nav_item, button in self._buttons.items():
            button.set_active(nav_item == item)
