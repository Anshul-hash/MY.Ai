"""Browser workspace placeholder."""

from localai_studio.ui.navigation import NavItem
from localai_studio.ui.pages.base_page import PlaceholderPage


class BrowserPage(PlaceholderPage):
    def __init__(self, parent=None) -> None:
        super().__init__(
            NavItem.BROWSER,
            headline="Browser",
            detail=(
                "An embedded browser for research, documentation lookup, and web "
                "context. Browser automation is not implemented in this skeleton."
            ),
            parent=parent,
        )
