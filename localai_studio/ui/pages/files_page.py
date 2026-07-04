"""Files workspace placeholder."""

from localai_studio.ui.navigation import NavItem
from localai_studio.ui.pages.base_page import PlaceholderPage


class FilesPage(PlaceholderPage):
    def __init__(self, parent=None) -> None:
        super().__init__(
            NavItem.FILES,
            headline="Files",
            detail=(
                "Browse project directories, attach context files, and manage "
                "documents for your AI sessions. File operations will be available here."
            ),
            parent=parent,
        )
