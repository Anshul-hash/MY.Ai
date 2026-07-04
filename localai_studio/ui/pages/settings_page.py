"""Settings workspace placeholder."""

from localai_studio.ui.navigation import NavItem
from localai_studio.ui.pages.base_page import PlaceholderPage


class SettingsPage(PlaceholderPage):
    def __init__(self, parent=None) -> None:
        super().__init__(
            NavItem.SETTINGS,
            headline="Settings",
            detail=(
                "Configure Ollama endpoints, default models, appearance, keyboard "
                "shortcuts, and compute preferences."
            ),
            parent=parent,
        )
