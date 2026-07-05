"""User profile for ZENA."""

from __future__ import annotations

from localai_studio.memory.memory_manager import MemoryManager


class Profile:
    """Stores and retrieves long-term user profile information."""

    def __init__(self, memory: MemoryManager):
        self.memory = memory

    # -----------------------
    # Name
    # -----------------------

    def set_name(self, name: str) -> None:
        self.memory.save(
            category="profile",
            content=f"User's name is {name}",
            importance=10,
        )

    # -----------------------
    # Projects
    # -----------------------

    def add_project(self, project: str) -> None:
        self.memory.save(
            category="project",
            content=project,
            importance=9,
        )

    # -----------------------
    # Preferences
    # -----------------------

    def add_preference(self, preference: str) -> None:
        self.memory.save(
            category="preference",
            content=preference,
            importance=8,
        )

    # -----------------------
    # Search
    # -----------------------

    def search(self, keyword: str):
        return self.memory.search(keyword)

    def recent(self, limit: int = 10):
        return self.memory.recent(limit)
