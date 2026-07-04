"""Terminal workspace placeholder."""

from localai_studio.ui.navigation import NavItem
from localai_studio.ui.pages.base_page import PlaceholderPage


class TerminalPage(PlaceholderPage):
    def __init__(self, parent=None) -> None:
        super().__init__(
            NavItem.TERMINAL,
            headline="Terminal",
            detail=(
                "Run shell commands alongside your AI assistant. "
                "Terminal execution will be integrated in a future release."
            ),
            parent=parent,
        )
