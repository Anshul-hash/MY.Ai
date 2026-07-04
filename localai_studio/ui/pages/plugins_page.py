"""Plugins workspace placeholder."""

from localai_studio.ui.navigation import NavItem
from localai_studio.ui.pages.base_page import PlaceholderPage


class PluginsPage(PlaceholderPage):
    def __init__(self, parent=None) -> None:
        super().__init__(
            NavItem.PLUGINS,
            headline="Plugins",
            detail=(
                "Discover and configure extensions that add tools, model providers, "
                "and custom workflows to LocalAI Studio."
            ),
            parent=parent,
        )
