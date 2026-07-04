"""Navigation identifiers for sidebar pages."""

from __future__ import annotations

from enum import Enum, auto


class NavItem(Enum):
    CHAT = auto()
    FILES = auto()
    BROWSER = auto()
    TERMINAL = auto()
    MEMORY = auto()
    PLUGINS = auto()
    SETTINGS = auto()

    @property
    def label(self) -> str:
        return self.name.capitalize()

    @property
    def icon(self) -> str:
        icons = {
            NavItem.CHAT: "💬",
            NavItem.FILES: "📁",
            NavItem.BROWSER: "🌐",
            NavItem.TERMINAL: ">_",
            NavItem.MEMORY: "🧠",
            NavItem.PLUGINS: "🔌",
            NavItem.SETTINGS: "⚙",
        }
        return icons[self]

    @property
    def description(self) -> str:
        descriptions = {
            NavItem.CHAT: "Converse with your local models",
            NavItem.FILES: "Browse and manage project files",
            NavItem.BROWSER: "Embedded web browsing",
            NavItem.TERMINAL: "Integrated shell access",
            NavItem.MEMORY: "Long-term context and recall",
            NavItem.PLUGINS: "Extend with custom tools",
            NavItem.SETTINGS: "Configure models and preferences",
        }
        return descriptions[self]
