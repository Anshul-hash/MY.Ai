"""Central Brain for ZENA."""

from __future__ import annotations

from localai_studio.memory.memory_manager import MemoryManager


class Brain:
    """Central coordinator for ZENA."""

    def __init__(self):

        self.memory = MemoryManager()

    # -------------------------
    # Memory
    # -------------------------

    def remember(
        self,
        category: str,
        content: str,
        importance: int = 5,
    ) -> None:

        self.memory.save(
            category=category,
            content=content,
            importance=importance,
        )

    def recall(self, keyword: str):

        return self.memory.search(keyword)

    def recent_memories(self, limit: int = 10):

        return self.memory.recent(limit)

    # -------------------------
    # Profile
    # -------------------------

    def set_name(self, name: str):

        self.remember(
            "profile",
            f"User's name is {name}",
            10,
        )

    # -------------------------
    # Projects
    # -------------------------

    def add_project(self, project: str):

        self.remember(
            "project",
            project,
            9,
        )

    # -------------------------
    # Preferences
    # -------------------------

    def add_preference(self, preference: str):

        self.remember(
            "preference",
            preference,
            8,
        )
