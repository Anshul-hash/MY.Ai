"""Project manager for ZENA."""

from __future__ import annotations

from localai_studio.memory.memory_manager import MemoryManager


class Projects:
    """Stores and manages user projects."""

    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def add(self, name: str, description: str = "") -> None:
        """Add a new project."""

        content = name

        if description:
            content += f" | {description}"

        self.memory.save(
            category="project",
            content=content,
            importance=9,
        )

    def search(self, keyword: str):
        """Search projects."""

        return [
            row
            for row in self.memory.search(keyword)
            if row["category"] == "project"
        ]

    def all(self):
        """Return all projects."""

        return [
            row
            for row in self.memory.search("")
            if row["category"] == "project"
        ]

    def recent(self, limit: int = 10):
        """Return recent projects."""

        return [
            row
            for row in self.memory.recent(limit)
            if row["category"] == "project"
        ]
