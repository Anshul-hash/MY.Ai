"""Memory workspace placeholder."""

from localai_studio.ui.navigation import NavItem
from localai_studio.ui.pages.base_page import PlaceholderPage


class MemoryPage(PlaceholderPage):
    def __init__(self, parent=None) -> None:
        super().__init__(
            NavItem.MEMORY,
            headline="Memory",
            detail=(
                "Persistent memory stores facts, preferences, and session context "
                "across conversations. Memory management UI will appear here."
            ),
            parent=parent,
        )
